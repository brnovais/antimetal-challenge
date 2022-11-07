#!/usr/bin/env node
const { program } = require("commander");

program.version("0.0.1");

program
  .command("deploy")
  .description("Deploy a workload to ANTIMETAL server")
  .argument("<workload path>", "path to code file")
  .option("-v, --version <float>", "python version", 3.0) // default is Python 3.0
  .action(deploy);

program.parse();

function deploy(workloadPath, options) {
  // EDIT THIS CODE TO CONNECT TO API
  console.log(workloadPath);
  console.log(options["version"]);

  var FormData = require("form-data");
  var fs = require("fs");

  var form = new FormData();

  form.append("script", fs.createReadStream(workloadPath));
  form.append("version", options["version"]);

  let url = "http://localhost:5000/run";

  form.submit(url, function (err, res) {
    console.log(err);
    res.resume();
  });
}
