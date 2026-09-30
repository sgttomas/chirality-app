"""A small JSON Schema 2020-12 validator for the keyword subset the PKG-03
PROPOSED schemas use. Prototype only (R12-3): not product code, Python 3
standard library only.

Supported keywords (the subset; any other keyword in a schema is reported as
an error by `check_subset`, so a schema cannot silently rely on an
unsupported keyword):

  annotations, ignored for validation: $schema, $id, $comment, title,
      description, examples, default
  $defs, $ref (local "#/$defs/..." and cross-schema "<$id>#/$defs/...")
  type (string, integer, number, boolean, object, array, null, or a list)
  enum, const
  properties, required, additionalProperties (boolean or schema)
  items (single schema), minItems, maxItems, uniqueItems
  minLength, pattern
  minimum
  oneOf, anyOf, allOf, not
  if / then / else
"""

import json
import re
from pathlib import Path

ANNOTATIONS = {"$schema", "$id", "$comment", "title", "description",
               "examples", "default"}
ASSERTIONS = {"$defs", "$ref", "type", "enum", "const", "properties",
              "required", "additionalProperties", "items", "minItems",
              "maxItems", "uniqueItems", "minLength", "pattern", "minimum",
              "oneOf", "anyOf", "allOf", "not", "if", "then", "else"}
SUBSET = ANNOTATIONS | ASSERTIONS


class Registry:
    """Maps each schema's $id to the schema, for cross-schema $ref."""

    def __init__(self):
        self.by_id = {}

    def add(self, schema):
        sid = schema.get("$id")
        if not sid:
            raise ValueError("schema without $id")
        self.by_id[sid] = schema

    def add_file(self, path):
        schema = json.loads(Path(path).read_text())
        self.add(schema)
        return schema

    def resolve(self, ref, root):
        base, _, frag = ref.partition("#")
        target = self.by_id[base] if base else root
        node = target
        if frag:
            for part in frag.lstrip("/").split("/"):
                node = node[part]
        return node, target


def check_subset(schema, path="#"):
    """Return the keywords used in `schema` that are outside the subset."""
    bad = []
    if isinstance(schema, dict):
        for k, v in schema.items():
            if k not in SUBSET:
                bad.append(f"{path}/{k}")
            if k in ("properties", "$defs"):
                for name, sub in v.items():
                    bad += check_subset(sub, f"{path}/{k}/{name}")
            elif k in ("items", "additionalProperties", "not", "if", "then",
                       "else") and isinstance(v, dict):
                bad += check_subset(v, f"{path}/{k}")
            elif k in ("oneOf", "anyOf", "allOf"):
                for i, sub in enumerate(v):
                    bad += check_subset(sub, f"{path}/{k}/{i}")
    return bad


def _type_ok(value, t):
    if t == "null":
        return value is None
    if t == "boolean":
        return isinstance(value, bool)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "string":
        return isinstance(value, str)
    if t == "array":
        return isinstance(value, list)
    if t == "object":
        return isinstance(value, dict)
    raise ValueError(f"unknown type {t}")


def validate(instance, schema, registry, root=None, path="$"):
    """Return a list of error strings (empty when valid)."""
    root = root if root is not None else schema
    errs = []
    if schema is True:
        return errs
    if schema is False:
        return [f"{path}: schema false"]
    if "$ref" in schema:
        target, new_root = registry.resolve(schema["$ref"], root)
        errs += validate(instance, target, registry, new_root, path)
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(instance, t) for t in types):
            return errs + [f"{path}: expected type {types}"]
    if "enum" in schema and instance not in schema["enum"]:
        errs.append(f"{path}: {instance!r} not in enum {schema['enum']}")
    if "const" in schema and instance != schema["const"]:
        errs.append(f"{path}: {instance!r} != const {schema['const']!r}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errs.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errs.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errs.append(f"{path}: below minimum {schema['minimum']}")
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in instance:
                errs.append(f"{path}: missing required '{req}'")
        for k, v in instance.items():
            if k in props:
                errs += validate(v, props[k], registry, root, f"{path}.{k}")
            elif "additionalProperties" in schema:
                ap = schema["additionalProperties"]
                if ap is False:
                    errs.append(f"{path}: additional property '{k}'")
                elif isinstance(ap, dict):
                    errs += validate(v, ap, registry, root, f"{path}.{k}")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errs.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errs.append(f"{path}: more than {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            seen = [json.dumps(i, sort_keys=True) for i in instance]
            if len(seen) != len(set(seen)):
                errs.append(f"{path}: items not unique")
        if "items" in schema:
            for i, v in enumerate(instance):
                errs += validate(v, schema["items"], registry, root, f"{path}[{i}]")
    for sub in schema.get("allOf", []):
        errs += validate(instance, sub, registry, root, path)
    if "anyOf" in schema:
        if not any(not validate(instance, s, registry, root, path) for s in schema["anyOf"]):
            errs.append(f"{path}: matches none of anyOf")
    if "oneOf" in schema:
        results = [validate(instance, s, registry, root, path) for s in schema["oneOf"]]
        n = sum(1 for r in results if not r)
        if n != 1:
            msg = f"{path}: matches {n} of oneOf (exactly 1 required)"
            if n == 0:
                closest = min(results, key=len)
                msg += f"; closest branch: {closest[0]}"
            errs.append(msg)
    if "not" in schema and not validate(instance, schema["not"], registry, root, path):
        errs.append(f"{path}: matches 'not'")
    if "if" in schema:
        if not validate(instance, schema["if"], registry, root, path):
            if "then" in schema:
                errs += validate(instance, schema["then"], registry, root, path)
        elif "else" in schema:
            errs += validate(instance, schema["else"], registry, root, path)
    return errs


def load_registry(schema_paths):
    reg = Registry()
    schemas = {}
    for p in schema_paths:
        schemas[str(p)] = reg.add_file(p)
    return reg, schemas
