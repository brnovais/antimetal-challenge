# ANTIMETAL API

ANTIMETAL API is a back-end that receives requests from users to access our middleware cloud platform.

## Install

This challenge doesn’t provide an easy to install container.
It's easy to create a container using CI/CD and deploy it to Docker Hub or similar registry.
To use this CLI, first download the GitHub repository.

```sh
git clone https://github.com/ANTIMETAL/backend-dev-challenge-bruno.git
```

Switch to the `api` directory.

```sh
cd api
```

If you don't want to use the container, install the requirements.

```sh
pip install -r requirements.txt
```

Build the container locally so we can run it.

```sh
sudo docker build . --tag antimetal
```

## Run

You can run the api directly with python. Docker host can be the unix socket if it's a local instance.

```sh
DOCKER_HOST=tcp://192.168.1.1:2375 python3 run.py
```

If you are using the container, use the docker sock for simplicity.

```sh
sudo docker run -p 8080:8080 --restart always -v /var/run/docker.sock:/var/run/docker.sock -d antimetal
```
