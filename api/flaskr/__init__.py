from flask import Flask, jsonify, request
from io import BytesIO
import docker
import tarfile

from flaskr.auth import extract_user


def create_app():
    app = Flask(__name__)

    @app.route("/run", methods=["POST"])
    def run_script():
        """
        Implement a POST method on the API endpoint that accepts a single Python script file and a Python version.
            - The API should receive the file itself, not just the name of the file. The client is effectively uploading the file to the server via this POST method.
            - The choice of how to persist the file is up to you; saving it locally is fine with us.
        """

        # The script represente as a file is a mandatory parameter.
        file = request.files["script"]
        if file is None:
            return "Script not uploaded", 400

        # Never trust user input. We probably should check version more carefully,
        # since we are concatenating directly to the container tag. Since this is
        # a timed challenge, I won't think about possible injections.
        version = request.form.get("version")
        # The endpoint should then spin up a Docker container using the python:v base image
        # (where v is the user-specified version) and run the script within that container.
        tag = "python:latest"
        if version is not None:
            tag = "python:" + version

        # Symbolic user authentication that's not secure. :}
        user = extract_user(request)
        if user is None:
            return "Unauthorized", 401

        # Create a new tar file to save the script inside the container.
        # This way we have an isolated container without any mounts.
        tar_stream = BytesIO()
        tar_file = tarfile.TarFile(fileobj=tar_stream, mode="w")
        tar_data = file.stream.read()
        tar_info = tarfile.TarInfo(name="script.py")
        tar_info.size = len(tar_data)
        tar_file.addfile(tar_info, BytesIO(tar_data))
        tar_file.close()
        tar_stream.seek(0)

        # Create a new client to access the docker engine api.
        client = docker.from_env()

        try:
            # Make sure the image is cached. If it's not cached, get returns really fast.
            client.images.get(tag)
        except:
            # Since we are using create, we need to pull the image before creating a container.
            # Pull has a huge delay compared to get, even when the image exists.
            client.images.pull(tag)

        # Assume that none of our Python scripts have any external library dependencies,
        # so the base Python image should be sufficient to run the code.
        container = client.containers.create(
            # This tag should be available locally by now.
            tag,
            # Detach make the container run in the background.
            detach=True,
            # Labels will be used to search for containers owned by users.
            labels={"owner": user},
            # For now, use the nobody user.
            user="nobody",
            # Simple safety memory limit.
            mem_limit="10M",
            # Simple safety cpu limit.
            cpu_count=1,
            # Make sure our container is not privileged.
            privileged=False,
            # For now, we don't need network access.
            network_disabled=True,
            # Use a command with timeout to execute containers.
            # This is a safety measure so scripts don't run eternally.
            command="timeout 10 python /tmp/script.py",
        )

        # Not that we have a valid container we can save the script.
        success = container.put_archive("/tmp/", tar_stream)
        if not success:
            return "Internal Server Error", 500

        # Start the container in detach mode.
        container.start()

        return jsonify({"id": container.id}), 200

    @app.route("/list", methods=["GET"])
    def list_scripts():
        # Symbolic user authentication that's not secure. :}
        user = extract_user(request)
        if user is None:
            return "Unauthorized", 401

        # Create a new client to access the docker engine api.
        client = docker.from_env()

        filter = {}
        if user != "admin":
            # Any user other than the admin, we filter by its owner.
            filter = {"label": "owner=" + user}

        containers = client.containers.list(all=True, filters=filter)
        return [c.id for c in containers], 200

    @app.route("/get", methods=["GET"])
    def get_script():
        # Symbolic user authentication that's not secure. :}
        user = extract_user(request)
        if user is None:
            return "Unauthorized", 401

        # Get the container identifier.
        id = request.args.get("id", type=str)
        if id is None:
            return "Invalid identifier", 400

        # Create a new client to access the docker engine api.
        client = docker.from_env()

        # Get container information.
        # Improve except when the id doesn't exist.
        container = client.containers.get(id)

        if container.labels["owner"] != user:
            return "Unauthorized", 401

        logs = container.logs().decode("utf-8")
        return (
            jsonify(
                {
                    "status": container.status,
                    "exitcode": container.attrs["State"]["ExitCode"],
                    "logs": logs,
                }
            ),
            200,
        )

    return app
