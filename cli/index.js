#!/usr/bin/env node
const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs/promises");
const { program } = require("commander");

const CREDENTIAL_FILE = ".credentials";

program
  .description("ANTIMETAL CLI")
  .version("0.1.0")
  .option("-H, --host <string>", "api host address", "localhost")
  .option("-P, --port <int>", "api host port", 5000)
  .option("-S, --tls <bool>", "api protocol tls", false);

program
  .command("deploy")
  .description("Deploy a workload to ANTIMETAL server")
  .argument("<workload path>", "path to code file")
  .option("-v, --version <string>", "python version", 3.0) // default is Python 3.0
  .action(deploy);

program
  .command("login")
  .description("Save a credential file with your username")
  .argument("<username>", "username to login")
  .action(login);

program.command("list").description("List my deployments").action(list);

program
  .command("get")
  .description("Get deployment by id")
  .argument("<id>", "Deployment identifier")
  .action(get);

program.parse();

async function deploy(workloadPath, options) {
  const username = await fs.readFile(CREDENTIAL_FILE, "utf-8");
  const script = await fs.readFile(workloadPath);

  var form = new FormData();
  form.append("script", script, "script.py");
  form.append("version", options["version"]);

  console.log(
    "This might take some time if the image has not been pulled before."
  );
  console.log("We can optmize that with a async endpoint for pulling images.");
  console.log("Sending request to run:", workloadPath);
  const response = await axios.post("/run", form, {
    baseURL: getBaseURL(),
    headers: {
      ...form.getHeaders(),
    },
    auth: {
      username,
    },
  });

  console.log("Running script with id:", response.data.id);
  console.log("To view more information, use: am get", response.data.id);
}

async function login(username) {
  await fs.writeFile(CREDENTIAL_FILE, username);
  console.log("Successfully authenticated:", username);
}

async function list() {
  const username = await fs.readFile(CREDENTIAL_FILE, "utf-8");

  console.log("Requesting deployments of:", username);
  const response = await axios.get("/list", {
    baseURL: getBaseURL(),
    auth: {
      username,
    },
  });

  console.log(username, "has", response.data.length, "deployments");
  console.table(response.data);
}

async function get(id) {
  const username = await fs.readFile(CREDENTIAL_FILE, "utf-8");

  try {
    console.log("Requesting status of:", id);
    const response = await axios.get("/get", {
      baseURL: getBaseURL(),
      params: {
        id,
      },
      auth: {
        username,
      },
    });

    console.log(
      "Deployment",
      response.data.status,
      "with code",
      response.data.exitcode
    );
    console.log(response.data.logs);
  } catch (error) {
    if (error.response.data) {
      console.error(error.response.data);
    } else {
      console.error(error);
    }
  }
}

function getBaseURL() {
  const opts = program.opts();
  const protocol = opts.tls ? "https" : "http";
  return protocol + "://" + opts.host + ":" + opts.port;
}
