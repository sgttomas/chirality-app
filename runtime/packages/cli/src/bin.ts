#!/usr/bin/env node
import {
  createDefaultCliDependencies,
  processCliIo,
  runCli
} from "./cli.js";

process.exitCode = await runCli(
  process.argv.slice(2),
  processCliIo,
  createDefaultCliDependencies()
);
