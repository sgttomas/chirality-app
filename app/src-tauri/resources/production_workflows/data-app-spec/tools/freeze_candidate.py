#!/usr/bin/env python3
"""Freeze a specification candidate (data-app-spec workflow, method §8).

Usage:
    python3 -I freeze_candidate.py --spec SPEC.yaml --out CANDIDATE_DIR --root CLOSURE_ROOT
        [--schema SCHEMA.json] [--member PATH=ROLE ...] [--members-file FILE]
        [--supporting PATH ...]

Writes into CANDIDATE_DIR, which must not exist yet:
- appspec.json: the authoring YAML parsed with check_spec.py's own loader, written as
  canonical JSON (sorted keys, no insignificant whitespace, UTF-8);
- appspec.lock: the closure lock. It records the spec, the schema hash (and the ontology
  hash the schema records), and every member with size, SHA-256 and role;
- validation.txt: check_spec.py's report on appspec.json, parsed as JSON;
- CANDIDATE_MANIFEST.csv: `Path,SHA256,Role` for the files above and any --supporting
  files. The manifest does not list itself.

CLOSURE_ROOT anchors the paths: members are given relative to it. Paths outside it are
recorded as absolute paths. A member's role is `normative` or `supporting`; the
default is `normative`. --members-file holds one `PATH ROLE` pair per line, and lines
starting with # are skipped. --schema defaults to ../formats/app-spec.schema.json
beside this script.

Exit status: 0 when the candidate is written and validates with no errors; 1 when it is
written but validation reports errors, so the candidate is not buildable as frozen;
2 on bad invocation or a failed integrity check, when nothing is kept.
Requires PyYAML and jsonschema.
"""
import argparse
import csv
import datetime
import hashlib
import importlib.util
import io
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent


def load_check_spec():
    spec = importlib.util.spec_from_file_location("check_spec", HERE / "check_spec.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def assert_json_scalars(value, path="$"):
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"non-string key at {path}")
            assert_json_scalars(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_json_scalars(item, f"{path}[{index}]")
    elif not (value is None or isinstance(value, (str, int, float, bool))):
        raise ValueError(f"non-JSON value of type {type(value).__name__} at {path}")


def relative(path, root):
    path = path.resolve()
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def parse_members(args):
    members = []
    for item in args.member or []:
        path, _, role = item.partition("=")
        members.append((path, role or "normative"))
    if args.members_file:
        for line in Path(args.members_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            members.append((parts[0], parts[1] if len(parts) > 1 else "normative"))
    for path, role in members:
        if role not in ("normative", "supporting"):
            raise ValueError(f"member {path}: role must be normative or supporting, not {role!r}")
    return members


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--schema", default=str(HERE.parent / "formats" / "app-spec.schema.json"))
    parser.add_argument("--member", action="append")
    parser.add_argument("--members-file")
    parser.add_argument("--supporting", action="append")
    args = parser.parse_args(argv[1:])

    root = Path(args.root).resolve()
    out = Path(args.out)
    spec_path = Path(args.spec)
    schema_path = Path(args.schema)
    if out.exists():
        print(f"refusing: {out} exists; a frozen candidate is never overwritten", file=sys.stderr)
        return 2
    try:
        members = parse_members(args)
    except (OSError, ValueError) as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 2

    check_spec = load_check_spec()
    authored = spec_path.read_bytes()
    document = yaml.load(authored.decode("utf-8"), Loader=check_spec.Yaml12Loader)
    try:
        assert_json_scalars(document)
    except ValueError as exc:
        print(f"refusing: {exc}", file=sys.stderr)
        return 2
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    if json.loads(canonical) != document:
        print("refusing: canonical JSON is not equivalent to the authoring form", file=sys.stderr)
        return 2

    schema_bytes = schema_path.read_bytes()
    schema = json.loads(schema_bytes)
    ontology = re.search(r"ontology_sha256=([0-9a-f]{64})", json.dumps(schema.get("$comment", "")))

    out.mkdir(parents=True)
    try:
        (out / "appspec.json").write_bytes(canonical)

        entries = [((out / "appspec.json"), "normative", "canonical specification"),
                   (spec_path, "supporting", "authoring form, parsed with the validator's loader")]
        entries += [(root / path, role, "") for path, role in members]
        lines = [f"# appspec.lock: frozen candidate {out.name}", "# Paths are relative to the closure root unless absolute.",
                 "lock_version: 0.1", f'created: "{datetime.datetime.now(datetime.timezone.utc).date().isoformat()}"',
                 f"spec: {relative(out / 'appspec.json', root)}", f"schema_sha256: {sha256(schema_bytes)}"]
        if ontology:
            lines.append(f"ontology_sha256: {ontology.group(1)}")
        lines.append("members:")
        for path, role, note in entries:
            data = Path(path).read_bytes()
            note_text = f', note: "{note}"' if note else ""
            lines.append(f"  - {{path: {relative(Path(path), root)}, size_bytes: {len(data)}, sha256: {sha256(data)}, role: {role}{note_text}}}")
        (out / "appspec.lock").write_text("\n".join(lines) + "\n", encoding="utf-8")

        lock = yaml.safe_load((out / "appspec.lock").read_text(encoding="utf-8"))
        for member in lock["members"]:
            target = Path(member["path"]) if Path(member["path"]).is_absolute() else root / member["path"]
            data = target.read_bytes()
            if len(data) != member["size_bytes"] or sha256(data) != member["sha256"]:
                raise ValueError(f"lock member {member['path']} does not verify")

        report, errors, _warnings = check_spec.check(schema, str(out / "appspec.json"))
        (out / "validation.txt").write_text(report + "\n", encoding="utf-8")

        rows = [(out / name, "normative" if name != "validation.txt" else "supporting") for name in ("appspec.json", "appspec.lock", "validation.txt")]
        rows += [(Path(path), "supporting") for path in args.supporting or []]
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["Path", "SHA256", "Role"])
        for path, role in rows:
            writer.writerow([relative(path, root), sha256(path.read_bytes()), role])
        (out / "CANDIDATE_MANIFEST.csv").write_text(buffer.getvalue(), encoding="utf-8")
    except (OSError, ValueError, KeyError) as exc:
        shutil.rmtree(out)
        print(f"refusing: {exc}", file=sys.stderr)
        return 2

    print(f"froze {out}: appspec.json {sha256(canonical)}; {len(entries)} lock members verified; "
          f"validation {'clean' if errors == 0 else f'{errors} error(s)'}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
