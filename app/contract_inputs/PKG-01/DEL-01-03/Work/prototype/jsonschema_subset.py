#!/usr/bin/env python3
"""Minimal JSON Schema validator for the keyword subset this prototype uses.

Prototype only (DEL-01-01 Design, Wave B node B6); not product code.
Python 3 standard library only.

Supported keywords (draft 2020-12 for Chirality's own schemas; the same subset
also covers the draft-07 bundles the 0.158.0 generator wrote):
  type (string or list), enum, const, properties, required,
  additionalProperties (boolean or schema), items (single schema), minItems,
  minimum, minLength, pattern, oneOf, anyOf, allOf, if/then/else, not,
  $ref (local JSON pointer only: "#/$defs/..." or "#/definitions/...", nested
  segments allowed), boolean schemas.
Ignored annotations: $schema, $id, $comment, title, description, default,
format, examples, deprecated.
Any other keyword raises UnsupportedKeyword, so a schema never silently
relies on something this validator does not check.
"""
import re

ANNOTATIONS = {"$schema", "$id", "$comment", "title", "description", "default",
               "format", "examples", "deprecated", "$defs", "definitions"}
SUPPORTED = {"type", "enum", "const", "properties", "required",
             "additionalProperties", "items", "minItems", "minimum", "minLength",
             "pattern", "oneOf", "anyOf", "allOf", "if", "then", "else", "not",
             "$ref"}


class UnsupportedKeyword(Exception):
    pass


def _is_type(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise UnsupportedKeyword("type " + str(t))


def _resolve(root, ref):
    if not ref.startswith("#/"):
        raise UnsupportedKeyword("non-local $ref " + ref)
    node = root
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[part]
    return node


def errors(instance, schema, root=None, path="$"):
    """Return a list of error strings (empty when valid)."""
    if root is None:
        root = schema
    if schema is True:
        return []
    if schema is False:
        return [path + ": false schema"]
    out = []
    for key in schema:
        if key not in SUPPORTED and key not in ANNOTATIONS:
            raise UnsupportedKeyword(key + " at " + path)
    if "$ref" in schema:
        out += errors(instance, _resolve(root, schema["$ref"]), root, path)
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(instance, t) for t in types):
            return out + [path + ": type " + "/".join(types) + " expected"]
    if "enum" in schema and instance not in schema["enum"]:
        out.append(path + ": not in enum " + repr(schema["enum"])[:120])
    if "const" in schema and instance != schema["const"]:
        out.append(path + ": const " + repr(schema["const"]))
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in instance:
                out.append(path + ": missing required " + req)
        for k, v in instance.items():
            if k in props:
                out += errors(v, props[k], root, path + "." + k)
            elif "additionalProperties" in schema:
                ap = schema["additionalProperties"]
                if ap is False:
                    out.append(path + ": additional property " + k)
                elif ap is not True:
                    out += errors(v, ap, root, path + "." + k)
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            out.append(path + ": fewer than %d items" % schema["minItems"])
        if "items" in schema:
            for i, v in enumerate(instance):
                out += errors(v, schema["items"], root, "%s[%d]" % (path, i))
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            out.append(path + ": shorter than %d" % schema["minLength"])
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            out.append(path + ": pattern " + schema["pattern"])
    if _is_type(instance, "number") and "minimum" in schema and instance < schema["minimum"]:
        out.append(path + ": below minimum %s" % schema["minimum"])
    if "allOf" in schema:
        for sub in schema["allOf"]:
            out += errors(instance, sub, root, path)
    if "anyOf" in schema:
        if not any(not errors(instance, sub, root, path) for sub in schema["anyOf"]):
            out.append(path + ": no anyOf branch matches")
    if "oneOf" in schema:
        n = sum(1 for sub in schema["oneOf"] if not errors(instance, sub, root, path))
        if n != 1:
            out.append(path + ": %d oneOf branches match (exactly 1 required)" % n)
    if "not" in schema and not errors(instance, schema["not"], root, path):
        out.append(path + ": matches a 'not' schema")
    if "if" in schema:
        if not errors(instance, schema["if"], root, path):
            if "then" in schema:
                out += errors(instance, schema["then"], root, path)
        elif "else" in schema:
            out += errors(instance, schema["else"], root, path)
    return out


def validate_against(instance, root, ref):
    """Validate `instance` against the definition `ref` inside bundle `root`."""
    return errors(instance, {"$ref": ref}, root)
