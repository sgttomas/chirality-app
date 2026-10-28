#!/usr/bin/env python3
"""W11 pin spike — method inventory from the generated JSON Schema (Codex 0.158.0).

Usage: inventory.py <schema-stable-dir> <schema-experimental-dir>

Reads ClientRequest.json, ClientNotification.json, ServerRequest.json and
ServerNotification.json in each directory (as written by
`codex app-server generate-json-schema [--experimental] --out DIR`), lists the
`method` enum value of every oneOf branch, and prints counts plus the
methods present only in the experimental output. Spike evidence only.
"""
import json
import sys
from pathlib import Path

FILES = ["ClientRequest", "ClientNotification", "ServerRequest", "ServerNotification"]


def methods(schema_dir: Path, name: str):
    doc = json.loads((schema_dir / f"{name}.json").read_text())
    out = []
    for branch in doc.get("oneOf", []):
        m = branch.get("properties", {}).get("method", {})
        vals = m.get("enum") or ([m["const"]] if "const" in m else [])
        out.extend(vals)
    return out


def main():
    stable, exp = Path(sys.argv[1]), Path(sys.argv[2])
    for name in FILES:
        s, e = methods(stable, name), methods(exp, name)
        only_e = [m for m in e if m not in s]
        only_s = [m for m in s if m not in e]
        print(f"## {name}: stable={len(s)} experimental={len(e)} "
              f"experimental-only={len(only_e)} stable-only={len(only_s)}")
        print("stable: " + ", ".join(s))
        if only_e:
            print("experimental-only: " + ", ".join(only_e))
        if only_s:
            print("stable-only: " + ", ".join(only_s))
        print()


if __name__ == "__main__":
    main()
