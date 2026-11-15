#!/usr/bin/env node
// Thin launcher: the tool itself is Python 3 (standard library only), so `npm i -g 3w-map` needs no other dependency.
const { spawnSync } = require("node:child_process");
const path = require("node:path");
const script = path.join(__dirname, "pmap");
for (const py of ["python3", "python"]) {
  const r = spawnSync(py, [script, ...process.argv.slice(2)], { stdio: "inherit" });
  if (r.error && r.error.code === "ENOENT") continue;
  process.exit(r.status ?? 1);
}
console.error("3w needs Python 3 on your PATH (python3 --version). Install it and retry.");
process.exit(127);
