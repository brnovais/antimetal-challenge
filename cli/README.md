# ANTIMETAL CLI

ANTIMETAL CLI is a front-end to access our API back-end servers.

## Install

This challenge doesn’t provide an easy to install package.
It's easy to create a package using CI/CD and deploy it to NPM.
To use this CLI, first download the GitHub repository.

```sh
git clone https://github.com/ANTIMETAL/backend-dev-challenge-bruno.git
```

Switch to the `cli` directory.

```sh
cd cli
```

Install `Node.js` dependecies.

```sh
npm install
```

## Login

To authenticate a user, use the `login` command.
For now, `admin` is used to give you access to everything.
Use only lowercase ASCII characters to username.

```sh
node . login admin
node . login coolusername
```

## Deploy

To deploy a script, the `deploy` command is used.

```sh
node . deploy script.py -v 3.8
```

## List

To list my deployments, the `list` command is used.

```sh
node . list
```

## Get

To get a specific deployment, the `get` command is used.

```sh
node . get 77ad17dff40fb984e89795091f1733314fd1354af03a35f9b302403d725997c5
```

## Examples

Simple Python code.

```python
print('hello')
```

Invalid Python code.

```python
NOT A VALID PYTHON CODE
```

Endless Python code.

```python
import time
time.sleep(1000)
```

Sensitive Python code.

```python
import pwd, grp
for p in pwd.getpwall():
    print(p[0], grp.getgrgid(p[3])[0])
```

Breaking Python code (v3.6 works fine, v3.[7-8] deprecated warning, v3.9 error).

```python
import sys
sys.callstats()
```
