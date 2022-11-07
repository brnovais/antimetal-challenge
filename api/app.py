from flask import Flask, request, jsonify
import os
import docker
import tarfile
from io import BytesIO

app = Flask(__name__)


@app.route("/run", methods=["POST"])
def api_run():
    file = request.files["script"]
    version = request.form.get("version")

    pw_tarstream = BytesIO()
    pw_tar = tarfile.TarFile(fileobj=pw_tarstream, mode="w")
    file_data = file.stream.read()
    tarinfo = tarfile.TarInfo(name="script.py")
    tarinfo.size = len(file_data)
    pw_tar.addfile(tarinfo, BytesIO(file_data))
    pw_tar.close()
    print(pw_tarstream.tell())
    pw_tarstream.seek(0)

    if version is None:
        version = "latest"

    if not version.isnumeric():
        return "Invalid version number", 400

    client = docker.from_env()
    # teste = client.containers.run("python:" + version, detach=True)#, command="python /tmp/script.py")
    teste = client.containers.create(
        "python:" + version, command="python /tmp/script.py"
    )
    print(teste)
    print(teste.status)

    success = container.put_archive("/tmp/", pw_tarstream)
    print(success)

    container.start()

    return jsonify({})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
