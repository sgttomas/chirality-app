#!/usr/bin/env python3
"""Minimal JSON Schema (2020-12 keyword subset) validator for the DEL-02-04 prototype.

Prototype only (ROLE-v0.1 §10); not product code. Python 3 standard library only.
Written for this folder after the pattern of DEL-01-01's prototype validator
(HOSTING-v0.8 §9.6), which is not imported, so this folder runs on its own.

Supported: type (string or list), enum, const, properties, required,
additionalProperties (boolean or schema), items (single schema), minItems,
minimum, minLength, pattern, oneOf, anyOf, allOf, if/then/else, not,
$ref (local "#/$defs/..." only).
Annotations ignored: $schema, $id, title, description, $defs.
Any other keyword raises UnsupportedKeyword, so a schema never silently relies
on a keyword this validator does not check.
"""
import re

ANNOTATIONS = {"$schema", "$id", "title", "description", "$defs", "$comment"}
SUPPORTED = {"type", "enum", "const", "properties", "required", "additionalProperties",
             "items", "minItems", "minimum", "minLength", "pattern", "oneOf", "anyOf",
             "allOf", "if", "then", "else", "not", "$ref"}


class UnsupportedKeyword(Exception):
    pass


def _is_type(v, t):
    if t == "object":
        return isinstance(v, dict)
    if t == "array":
        return isinstance(v, list)
    if t == "string":
        return isinstance(v, str)
    if t == "boolean":
        return isinstance(v, bool)
    if t == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "null":
        return v is None
    raise UnsupportedKeyword("type " + t)


def _resolve(root, ref):
    if not ref.startswith("#/"):
        raise UnsupportedKeyword("non-local $ref " + ref)
    node = root
    for seg in ref[2:].split("/"):
        node = node[seg]
    return node


def errors(inst, schema, root=None, path="$"):
    if root is None:
        root = schema
    if schema is True:
        return []
    if schema is False:
        return [path + ": schema false"]
    for k in schema:
        if k not in SUPPORTED and k not in ANNOTATIONS:
            raise UnsupportedKeyword(k)
    out = []
    if "$ref" in schema:
        out += errors(inst, _resolve(root, schema["$ref"]), root, path)
    if "type" in schema:
        ts = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(inst, t) for t in ts):
            return out + ["%s: type %s expected" % (path, "/".join(ts))]
    if "enum" in schema and inst not in schema["enum"]:
        out.append("%s: %r not in enum" % (path, inst))
    if "const" in schema and inst != schema["const"]:
        out.append("%s: %r is not const %r" % (path, inst, schema["const"]))
    if isinstance(inst, dict):
        for r in schema.get("required", []):
            if r not in inst:
                out.append("%s: required %s missing" % (path, r))
        props = schema.get("properties", {})
        for k, v in inst.items():
            if k in props:
                out += errors(v, props[k], root, path + "." + k)
            elif "additionalProperties" in schema:
                ap = schema["additionalProperties"]
                if ap is False:
                    out.append("%s: additional property %s" % (path, k))
                elif isinstance(ap, dict):
                    out += errors(v, ap, root, path + "." + k)
    if isinstance(inst, list):
        if "minItems" in schema and len(inst) < schema["minItems"]:
            out.append("%s: fewer than %d items" % (path, schema["minItems"]))
        if "items" in schema:
            for i, v in enumerate(inst):
                out += errors(v, schema["items"], root, "%s[%d]" % (path, i))
    if isinstance(inst, str):
        if "minLength" in schema and len(inst) < schema["minLength"]:
            out.append("%s: shorter than %d" % (path, schema["minLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], inst):
            out.append("%s: %r does not match %s" % (path, inst, schema["pattern"]))
    if isinstance(inst, (int, float)) and not isinstance(inst, bool):
        if "minimum" in schema and inst < schema["minimum"]:
            out.append("%s: below minimum %s" % (path, schema["minimum"]))
    for sub in schema.get("allOf", []):
        out += errors(inst, sub, root, path)
    if "anyOf" in schema and not any(not errors(inst, s, root, path) for s in schema["anyOf"]):
        out.append(path + ": no anyOf branch matches")
    if "oneOf" in schema:
        n = sum(1 for s in schema["oneOf"] if not errors(inst, s, root, path))
        if n != 1:
            out.append("%s: %d oneOf branches match (exactly 1 required)" % (path, n))
    if "not" in schema and not errors(inst, schema["not"], root, path):
        out.append(path + ": matches a 'not' schema")
    if "if" in schema:
        if not errors(inst, schema["if"], root, path):
            if "then" in schema:
                out += errors(inst, schema["then"], root, path)
        elif "else" in schema:
            out += errors(inst, schema["else"], root, path)
    return out
