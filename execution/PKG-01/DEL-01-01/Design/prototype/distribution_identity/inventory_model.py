"""Pure value model for CC-HOSTING-DISTRIBUTION-01; never reads supplier trees.

Not a runtime verifier: caller must separately establish actual filesystem facts,
qualified-reference provenance, stable custody and complete observations.
"""
import hashlib
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[2] / "hosting.distribution-inventory.schema.json"
VALIDATOR = Draft202012Validator(json.loads(SCHEMA.read_text()))


def valid_digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def manifest(entries):
    files = sorted((e for e in entries if e["kind"] == "file"),
                   key=lambda e: e["path"].encode("utf-8", "strict"))
    if any(not valid_digest(e["sha256"]) for e in files):
        raise ValueError("invalid file SHA-256")
    data = "".join(e["sha256"] + "  " + e["path"] + "\n" for e in files)
    return hashlib.sha256(data.encode("utf-8", "strict")).hexdigest()


def validate(value):
    errors = ["schema: " + e.message for e in VALIDATOR.iter_errors(value)]
    if errors:
        return errors
    if not valid_digest(value["manifest_sha256"]):
        errors.append("invalid manifest SHA-256")
    entries = value["entries"]
    paths = {}
    for entry in entries:
        if entry["kind"] == "file" and not valid_digest(entry["sha256"]):
            errors.append("invalid file SHA-256")
        path = entry["path"]
        try:
            path.encode("utf-8", "strict")
        except UnicodeError:
            errors.append("invalid UTF-8 path")
        if path == ".":
            if entry["kind"] != "dir":
                errors.append("root must be directory")
        elif (any(c in path for c in "\\\r\n\0") or
              any(c in ("", ".", "..") for c in path.split("/"))):
            errors.append("invalid descendant path: " + repr(path))
        if path in paths:
            errors.append("duplicate path: " + repr(path))
        paths[path] = entry
    if paths.get(".", {}).get("kind") != "dir":
        errors.append("missing root directory")
    for path in paths:
        if path != ".":
            parent = path.rsplit("/", 1)[0] if "/" in path else "."
            if paths.get(parent, {}).get("kind") != "dir":
                errors.append("missing parent directory: " + repr(parent))
    for path in ("bin", "codex-path", "codex-resources"):
        if paths.get(path, {}).get("kind") != "dir":
            errors.append("missing vendor directory: " + path)
    for path in ("bin/codex", "codex-package.json"):
        if paths.get(path, {}).get("kind") != "file":
            errors.append("missing vendor file: " + path)
    if not errors and manifest(entries) != value["manifest_sha256"]:
        errors.append("manifest mismatch")
    return errors


def compare(expected, observed):
    errors = validate(expected) + validate(observed)
    if errors:
        return {"equal": False, "invalid": errors}
    left = {e["path"]: e for e in expected["entries"]}
    right = {e["path"]: e for e in observed["entries"]}
    return {"equal": left == right, "missing": sorted(left.keys() - right.keys()),
            "extra": sorted(right.keys() - left.keys()),
            "changed": sorted(p for p in left.keys() & right.keys() if left[p] != right[p])}


def prepend_path(prefix, inherited):
    """Model explicit PATH-prefix representability, not resolution or custody."""
    if not prefix or any(c in prefix for c in (":", "\0")):
        raise ValueError("unrepresentable PATH prefix")
    # Absence and explicit empty PATH differ. Never manufacture an empty entry.
    return prefix if inherited is None else prefix + ":" + inherited
