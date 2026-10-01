"""Minimal JSON Schema (draft 2020-12) validator for a declared subset.

Prototype only (R12-3). Not product code. Python 3 standard library only.

Supported keywords (the subset the DEL-04-0x schemas use):
  $schema, $id, $defs, $ref, $comment, title, description, examples (annotations or
  structure); type, enum, const, required, properties, additionalProperties
  (boolean or schema), items (single schema), minItems, minLength, pattern,
  minimum, oneOf, anyOf, allOf, not.

Any other keyword makes the schema itself fail with "unsupported keyword", so a
schema cannot silently rely on something this validator ignores.

$ref: "#/..." JSON pointers inside the current schema resource; absolute
references "<$id>#/..." resolved through a registry of loaded schemas; and
relative file references "<path>#/..." (percent-encoded, as RS's references to
EXEC's CE bodies are written, R14-1), resolved against the directory of the
file the referring schema was loaded from, then loaded and subset-checked once.
A general validator needs the same mapping: RS's $id is a URN, so a relative
reference cannot resolve against it.
"""

import json
import os
import re
from urllib.parse import unquote

ANNOTATIONS = {"$schema", "$id", "$defs", "$comment", "title", "description", "examples"}
ASSERTIONS = {
    "$ref", "type", "enum", "const", "required", "properties", "additionalProperties",
    "items", "minItems", "minLength", "pattern", "minimum", "oneOf", "anyOf", "allOf", "not",
}
SUPPORTED = ANNOTATIONS | ASSERTIONS


class SchemaError(Exception):
    pass


class Registry:
    def __init__(self):
        self.by_id = {}
        self.dir_of = {}            # id(schema root) -> directory it was loaded from
        self.by_path = {}           # absolute file path -> schema root

    def add(self, schema):
        sid = schema.get("$id")
        if not sid:
            raise SchemaError("schema has no $id")
        self.by_id[sid] = schema
        return sid

    def load(self, path):
        path = os.path.abspath(path)
        with open(path, encoding="utf-8") as fh:
            schema = json.load(fh)
        check_supported(schema, path)
        self.dir_of[id(schema)] = os.path.dirname(path)
        self.by_path[path] = schema
        return self.add(schema)

    def resolve_file(self, base, root):
        """A relative file reference, against the directory of the referring root."""
        d = self.dir_of.get(id(root))
        if d is None:
            return None
        path = os.path.normpath(os.path.join(d, unquote(base)))
        if path not in self.by_path:
            if not os.path.exists(path):
                return None
            self.load(path)
        return self.by_path[path]


def check_supported(node, where="schema", path="#"):
    """Reject keywords outside the subset, walking every subschema."""
    if isinstance(node, bool):
        return
    if not isinstance(node, dict):
        raise SchemaError(f"{where} {path}: schema must be object or boolean")
    for key, val in node.items():
        if key not in SUPPORTED:
            raise SchemaError(f"{where} {path}: unsupported keyword {key!r}")
        if key in ("$defs", "properties"):
            for k, sub in val.items():
                check_supported(sub, where, f"{path}/{key}/{k}")
        elif key in ("items", "additionalProperties", "not") and not isinstance(val, bool):
            check_supported(val, where, f"{path}/{key}")
        elif key in ("oneOf", "anyOf", "allOf"):
            for i, sub in enumerate(val):
                check_supported(sub, where, f"{path}/{key}/{i}")


def _pointer(doc, frag):
    if frag in ("", "#"):
        return doc
    if not frag.startswith("#/"):
        raise SchemaError(f"unsupported fragment {frag!r}")
    node = doc
    for part in frag[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[part]
    return node


TYPES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def validate(instance, schema, registry, root=None, path="$"):
    """Return a list of error strings (empty when valid)."""
    root = root if root is not None else schema
    errors = []
    if schema is True:
        return errors
    if schema is False:
        return [f"{path}: false schema"]

    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#"):
            target, target_root = _pointer(root, ref), root
        else:
            base, _, frag = ref.partition("#")
            if base in registry.by_id:
                target_root = registry.by_id[base]
            elif ":" not in base and (target_root := registry.resolve_file(base, root)) is not None:
                pass
            else:
                return [f"{path}: unresolved $ref {ref}"]
            target = _pointer(target_root, "#" + frag if frag else "#")
        errors += validate(instance, target, registry, target_root, path)

    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(TYPES[t](instance) for t in types):
            return errors + [f"{path}: expected type {types}, got {type(instance).__name__}"]

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: does not match pattern {schema['pattern']!r}")
    if TYPES["number"](instance) and "minimum" in schema and instance < schema["minimum"]:
        errors.append(f"{path}: below minimum {schema['minimum']}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required {req!r}")
        props = schema.get("properties", {})
        for key, val in instance.items():
            if key in props:
                errors += validate(val, props[key], registry, root, f"{path}.{key}")
            elif "additionalProperties" in schema:
                ap = schema["additionalProperties"]
                if ap is False:
                    errors.append(f"{path}: additional property {key!r} not allowed")
                elif isinstance(ap, dict):
                    errors += validate(val, ap, registry, root, f"{path}.{key}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, item in enumerate(instance):
                errors += validate(item, schema["items"], registry, root, f"{path}[{i}]")

    for sub in schema.get("allOf", []):
        errors += validate(instance, sub, registry, root, path)
    if "anyOf" in schema:
        if not any(not validate(instance, s, registry, root, path) for s in schema["anyOf"]):
            errors.append(f"{path}: matches no anyOf branch")
    if "oneOf" in schema:
        results = [validate(instance, s, registry, root, path) for s in schema["oneOf"]]
        passing = sum(1 for r in results if not r)
        if passing != 1:
            best = min(results, key=len) if results else []
            detail = f"; closest branch: {best[:3]}" if passing == 0 else ""
            errors.append(f"{path}: matches {passing} oneOf branches (need exactly 1){detail}")
    if "not" in schema and not validate(instance, schema["not"], registry, root, path):
        errors.append(f"{path}: matches a 'not' schema")
    return errors
