"""Minimal JSON Schema (draft 2020-12) validator for the subset used by the
DEL-05-01 and DEL-05-02 Design schemas. Prototype only, not product code.

Supported keywords: type (string or list; "integer" excludes booleans),
properties, required, additionalProperties (boolean only), enum, const,
items (single schema), minItems, minLength, minimum, oneOf, anyOf,
$ref to "#/$defs/<name>". Annotation keywords ($schema, $id, title,
description, $comment, examples) are ignored. Any other keyword raises
UnsupportedKeyword, so a schema never silently uses more than this subset.

Usage: python3 schema_subset.py SCHEMA INSTANCE [INSTANCE ...]
Exit 0 when every instance is valid; 1 otherwise.
"""
import json
import sys

ANNOTATIONS = {"$schema", "$id", "title", "description", "$comment", "examples", "$defs"}
SUPPORTED = {"type", "properties", "required", "additionalProperties", "enum", "const",
             "items", "minItems", "minLength", "minimum", "oneOf", "anyOf", "$ref"}


class UnsupportedKeyword(Exception):
    pass


def _type_ok(value, name):
    if name == "null":
        return value is None
    if name == "boolean":
        return isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "string":
        return isinstance(value, str)
    if name == "array":
        return isinstance(value, list)
    if name == "object":
        return isinstance(value, dict)
    raise UnsupportedKeyword("type " + name)


def validate(instance, schema, root=None, path="$"):
    """Return a list of error strings (empty when valid)."""
    root = schema if root is None else root
    errors = []
    for key in schema:
        if key not in SUPPORTED and key not in ANNOTATIONS:
            raise UnsupportedKeyword(key)
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            raise UnsupportedKeyword("$ref " + ref)
        errors += validate(instance, root["$defs"][ref[len("#/$defs/"):]], root, path)
    if "type" in schema:
        names = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(instance, n) for n in names):
            errors.append(f"{path}: type {names} expected, got {type(instance).__name__}")
            return errors
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: const {schema['const']!r} expected, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum")
    if isinstance(instance, str) and "minLength" in schema and len(instance) < schema["minLength"]:
        errors.append(f"{path}: shorter than {schema['minLength']}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool) and "minimum" in schema:
        if instance < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")
    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required {req!r}")
        props = schema.get("properties", {})
        for k, v in instance.items():
            if k in props:
                errors += validate(v, props[k], root, f"{path}.{k}")
            elif schema.get("additionalProperties", True) is False:
                errors.append(f"{path}: unexpected property {k!r}")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, item in enumerate(instance):
                errors += validate(item, schema["items"], root, f"{path}[{i}]")
    if "oneOf" in schema:
        passing = [i for i, s in enumerate(schema["oneOf"]) if not validate(instance, s, root, path)]
        if len(passing) != 1:
            errors.append(f"{path}: oneOf matched {len(passing)} branches {passing}, exactly 1 required")
    if "anyOf" in schema:
        if not any(not validate(instance, s, root, path) for s in schema["anyOf"]):
            errors.append(f"{path}: anyOf matched no branch")
    return errors


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        schema = json.load(fh)
    ok = True
    for inst_path in argv[2:]:
        with open(inst_path, encoding="utf-8") as fh:
            instance = json.load(fh)
        errs = validate(instance, schema)
        print(("VALID   " if not errs else "INVALID ") + inst_path)
        for e in errs:
            print("    " + e)
        ok = ok and not errs
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
