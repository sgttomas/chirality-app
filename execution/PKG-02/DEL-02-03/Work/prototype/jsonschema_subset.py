"""Minimal JSON Schema 2020-12 validator for the keyword subset EXEC's schemas use.

Design prototype for DEL-02-03 (EXEC-v0.6). Not product code. Python 3 standard
library only.

Supported keywords: $schema, $id, $defs, $ref (local "#/$defs/<name>" only),
title, description, $comment, type, properties, required,
additionalProperties (false or a schema), enum, const, items, minItems,
minLength, pattern, minimum, oneOf, anyOf.

Any other keyword raises UnsupportedKeyword, so a schema cannot silently rely
on a keyword this validator ignores.
"""

import re

ANNOTATIONS = {"$schema", "$id", "$defs", "title", "description", "$comment"}
SUPPORTED = ANNOTATIONS | {
    "$ref", "type", "properties", "required", "additionalProperties", "enum",
    "const", "items", "minItems", "minLength", "pattern", "minimum", "oneOf",
    "anyOf",
}


class UnsupportedKeyword(Exception):
    pass


def _type_ok(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    raise UnsupportedKeyword("type " + t)


def validate(instance, schema, root=None, path="$"):
    """Return a list of error strings (empty when the instance is valid)."""
    root = schema if root is None else root
    errors = []
    if schema is True:
        return errors
    if schema is False:
        return [path + ": no value allowed here"]
    for key in schema:
        if key not in SUPPORTED:
            raise UnsupportedKeyword(key)
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            raise UnsupportedKeyword("$ref " + ref)
        target = root["$defs"][ref[len("#/$defs/"):]]
        errors += validate(instance, target, root, path)
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(instance, t) for t in types):
            return errors + [f"{path}: expected type {types}, got {type(instance).__name__}"]
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum {schema['enum']}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match {schema['pattern']!r}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in instance:
                errors.append(f"{path}: missing required property {name!r}")
        for name, value in instance.items():
            if name in props:
                errors += validate(value, props[name], root, f"{path}.{name}")
            elif "additionalProperties" in schema:
                errors += validate(value, schema["additionalProperties"], root, f"{path}.{name}")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, value in enumerate(instance):
                errors += validate(value, schema["items"], root, f"{path}[{i}]")
    if "oneOf" in schema:
        results = [validate(instance, sub, root, path) for sub in schema["oneOf"]]
        passing = [r for r in results if not r]
        if len(passing) != 1:
            best = min(results, key=len)
            errors.append(f"{path}: matched {len(passing)} of oneOf (need exactly 1)")
            if not passing:
                errors += ["  " + e for e in best]
    if "anyOf" in schema:
        results = [validate(instance, sub, root, path) for sub in schema["anyOf"]]
        if not any(not r for r in results):
            errors.append(f"{path}: matched none of anyOf")
    return errors
