#!/usr/bin/env node
const fs = require("fs");
const { program } = require("commander");

program
  .description("ANTIMETAL CLI")
  .version("0.1.0")
  .option("-H, --host <string>", "api host address", "localhost")
  .option("-P, --port <int>", "api host port", 5000);

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

program.parse();

function deploy(workloadPath, options) {
  var FormData = require("form-data");
  var form = new FormData();

  form.append("script", fs.createReadStream(workloadPath));
  form.append("version", options["version"]);

  fs.readFile(".credentials", "utf8", (err, username) => {
    if (err) {
      console.error(err);
      return;
    }

    const opts = program.opts();
    form.submit(
      {
        host: opts.host,
        port: opts.port,
        path: "/run",
        auth: username,
      },
      function (err, res) {
        console.log(err);
        res.resume();
      }
    );
  });
}

function login(username) {
  fs.writeFile(".credentials", username, (err) => {
    if (err) {
      console.error(err);
    } else {
      console.log("Successfully authenticated:", username);
    }
  });
}
