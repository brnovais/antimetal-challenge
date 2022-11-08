# Simple tutorial

The main goal of this tutorial is to show a step-by-step workflow that uses all available commands.

## Install

Download the repository.

```sh
git clone https://github.com/ANTIMETAL/backend-dev-challenge-bruno.git
```

Enter the local repository folder CLI.

```sh
cd backend-dev-challenge-bruno/cli
```

Install package dependencies[^1].

```sh
npm install
```

## Login

First we need to authenticate our user. For now, we don’t need to provide any credentials (passwords). We can even use the admin account to show information about all users.

```console
ubuntu@instance:~$ node . login my_cool_user_name
Successfully authenticated: my_cool_user_name
```

You can use help to see more information.

```sh
node . login --help
```

## Deploy

To run scripts we first need to create our script file.

```sh
tee -a script.py <<EOF
print(‘Hello World’)
EOF
```

Now we can deploy the script to the API server

```console
ubuntu@instance:~$ node . deploy script.py
This might take some time if the image has not been pulled before.
We can optmize that with an async endpoint for pulling images.
Sending request to run: script.py
Running script with id: c0cd81baf49a2150262b608ad272d7244cc1930335a13307e65d2493fe9d9ece
To view more information, use: am get c0cd81baf49a2150262b608ad272d7244cc1930335a13307e65d2493fe9d9ece
```

You can use help to see more information.

```sh
node . deploy --help
```

## List

List all deployments made so far.

```console
ubuntu@instance:~$ node . list
Requesting deployments of: my_cool_user_name
my_cool_user_name has 1 deployments
┌─────────┬────────────────────────────────────────────────────────────────────┐
│ (index) │                               Values                               │
├─────────┼────────────────────────────────────────────────────────────────────┤
│    0    │ 'c0cd81baf49a2150262b608ad272d7244cc1930335a13307e65d2493fe9d9ece' │
└─────────┴────────────────────────────────────────────────────────────────────┘
```

## Get

Get information about a specific deployment.

```console
ubuntu@instance:~$ node . get c0cd81baf49a2150262b608ad272d7244cc1930335a13307e65d2493fe9d9ece
Requesting status of: c0cd81baf49a2150262b608ad272d7244cc1930335a13307e65d2493fe9d9ece
Deployment exited with code 0
Hello World
```

[^1]: You need Node.js to run this code.
