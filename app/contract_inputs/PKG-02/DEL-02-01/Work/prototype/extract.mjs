// extract.mjs - NOT PRODUCT CODE. Design prototype for DEL-02-01 WD-v0.8 §3.5.
// An independent second implementation of the carriage rule (CR-1..CR-6) in
// node's standard library, used by wdproto.py S-9 to show that the declared
// part is extracted and parsed the same way outside Python.
// Usage: node extract.mjs <path/to/WORKFLOW.md>  -> prints canonical JSON (sorted keys).
import { readFileSync } from "node:fs";

const text = readFileSync(process.argv[2], "utf8").replace(/\r\n?/g, "\n");
const lines = text.split("\n");
let i = 0;
if (lines[0] === "---") {
  const end = lines.indexOf("---", 1);
  if (end > 0) i = end + 1;
}
const fence = /^( {0,3})(`{3,}|~{3,})(.*)$/;
const blocks = [];
while (i < lines.length) {
  const m = lines[i].match(fence);
  if (!m) { i++; continue; }
  const f = m[2];
  const info = m[3].trim();
  if (f[0] === "`" && info.includes("`")) { i++; continue; }
  const close = new RegExp("^ {0,3}" + (f[0] === "`" ? "`" : "~") + "{" + f.length + ",}\\s*$");
  let j = i + 1;
  while (j < lines.length && !close.test(lines[j])) j++;
  if (info === "workflow-declaration") blocks.push(lines.slice(i + 1, j).join("\n"));
  i = j + 1;
}
if (blocks.length !== 1) {
  console.error(blocks.length === 0 ? "absent" : "more_than_one_block");
  process.exit(2);
}
const sortKeys = (v) =>
  Array.isArray(v) ? v.map(sortKeys)
  : v && typeof v === "object" ? Object.fromEntries(Object.keys(v).sort().map((k) => [k, sortKeys(v[k])]))
  : v;
console.log(JSON.stringify(sortKeys(JSON.parse(blocks[0]))));
