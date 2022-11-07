# Introduction

Infrastructure components for this challenge.

This file represents all commands used to configure the `ubuntu` instance.

Ideally, tools such as Terraform or Ansible should be used to configure instances.

## Update

Update local package database.

```sh
sudo apt-get update
```

First run upgrade the whole distribution - including the Kernel and core packages.

```sh
sudo apt-get dist-upgrade
```

Now is a good time to reboot the system and load the upgraded distribution

```sh
sudo reboot
```

Clean unused packages

```sh
sudo apt-get autoremove
```

Usually not necessary, but clean old packages from the local database

```sh
sudo apt-get clean
```

## Docker

Docker will be the base task runner for this challenge.

Not all distributions share the same container engine and version, thus I prefer to use the official docker package with the latest version and additional plugins.

https://docs.docker.com/engine/install/ubuntu/
