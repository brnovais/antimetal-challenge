# Antimetal Backend Developer Take Home Challenge

Antimetal is a middleware cloud platform takes a workload defined by a user and runs in on one of many instances that we have available. In this challenge, you'll be building a simplified version of a deployment pipeline for Python scripts.

The deployment process begins when a user inputs workload information through the Antimetal CLI tool through a command such as `am deploy script.py -v 3.8`. This command indicates that the user wants to deploy and run the script `script.py` with Python version 3.8. We've provided an outline of this CLI tool to you in the `cli` directory. Your job is to build a server-side API that consumes this information and runs the Python workload. Additionally, you'll connect the CLI tool to this API.

To better segment the work you have to do, we've broken it into two discrete tasks.

## Task A: Server-Side API

For a user to interact with Antimetal, we need to create an API endpoint that allows them to send and deploy their workloads. After the server receives the workload, it should then spin up a new Docker container and run the workload (on the same machine).

(In reality, Antimetal separates the server from the instance where the workload runs, but we made the simplifying assumption that both are the same for the sake of this challenge.)

### Sub-Tasks

- Implement a POST method on the API endpoint that accepts a single Python script file and a Python version.
  - The API should receive _the file itself_, not just the name of the file. The client is effectively uploading the file to the server via this POST method.
  - The choice of how to persist the file is up to you; saving it locally is fine with us.
- The endpoint should then spin up a Docker container using the `python:v` base image (where `v` is the user-specified version) and run the script within that container.
  - Assume that none of our Python scripts have any external library dependencies, so the base Python image should be sufficient to run the code.
- **Stretch Goal** (Optional): If you finish the project early or are looking for a challenge, implement a GET method on the API endpoint that accepts a unique workload ID and returns the status.
  - You'll have the change the POST method to assign an incoming workload a unique id and include this id in the response sent back to the client.
  - Keep the status simple, such as "deploying", "running", or "finished".
  - You will want to utilize some data store to maintain a mapping of workload IDs to statuses.

You can complete this task in any language which you choose; however, we recommend Python or Golang since they have very easy-to-use [Docker SDKs](https://docs.docker.com/engine/api/sdk/).

## Task B: Deploy the API and Connect the CLI

Now that we have an server-side API, we will deploy it to the cloud and connect our CLI to it.

### Sub-Tasks

- We've given you access to an AWS instance (details were sent via email). Deploy a containerized version of the API to the instance.
  - Don't worry about authorization, rate limiting, or the API gateway in general; we're fine with the API endpoint being direct accessible and publicly available for the sake of this challenge.
- Edit the existing `deploy` function in `cli/index.js` to connect to the API endpoint you've just deployed.
  - Now, in the `cli` directory, you can run `node . deploy script.py -v 3.8` and see the workload run on the AWS instance.
- Run some tests! Write a few different Python scripts, preferably ones that have version dependencies.

## Getting Started

- The `cli` code is built using Node.js. The only dependency it uses is the `commander` framework. To ensure you have no dependency issues, we have included the `node_modules` folder; however, you can install it again via `npm i commander`.
- The AWS instance details have been emailed to you. It's an Ubuntu EC2 instance. You should be able to ssh into the machine using the RSA private key. Additionally, we have enabled the following inbound traffic: all HTTPS traffic (but not HTTP), all ICMP traffic (v4 and v6), and TCP traffic on port 3000.

## Questions

Email Shreyas at shreyas@antimetal.com

## I finished! What now?

- Answer the questions in `answers.md`
- Commit your final submission to the main branch of the repo.
- Do not tear down the AWS deployment. We want to see it in action and test it ourselves.
- Ping Shreyas at shreyas@antimetal.com to let him know you are finished
