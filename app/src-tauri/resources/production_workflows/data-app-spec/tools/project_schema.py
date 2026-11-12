#!/usr/bin/env python3
"""Projector: LinkML ontology subset -> JSON Schema 2020-12 (data-app-spec workflow).

The projection rules are stated in formats/PROJECTION.md; this script implements exactly
those rules and fails on LinkML constructs it does not support rather than guessing. A
project may use the LinkML generators instead. Requires PyYAML.

Usage:
    python3 -I project_schema.py ONTOLOGY.yaml OUTPUT.json [--root CLASS]
    python3 -I project_schema.py ONTOLOGY.yaml OUTPUT.json [--root CLASS] --check   # fail if OUTPUT differs

The root defaults to the ontology's single local tree_root class. Local imports (any
import other than linkml:*) are read from the ontology's directory as NAME.yaml; their
classes, enums and types are merged, and their tree_root flags are ignored. Every local
definition is emitted; an imported definition is emitted only when it is reachable from
the root. Definitions keep declaration order.
"""
import hashlib
import json
import sys
from pathlib import Path

import yaml

BUILTIN_TYPES = {
    "string": {"type": "string"},
    "integer": {"type": "integer"},
    "float": {"type": "number"},
    "double": {"type": "number"},
    "boolean": {"type": "boolean"},
    "date": {"type": "string", "format": "date"},
    "datetime": {"type": "string", "format": "date-time"},
    "uri": {"type": "string", "format": "uri"},
    "uriorcurie": {"type": "string"},
}
SUPPORTED_SLOT_KEYS = {
    "range", "required", "multivalued", "inlined", "inlined_as_list", "identifier",
    "designates_type", "description", "pattern", "minimum_value", "maximum_value", "any_of",
}
SUPPORTED_CLASS_KEYS = {
    "description", "attributes", "is_a", "mixins", "mixin", "abstract", "tree_root",
    "class_uri", "exact_mappings", "close_mappings", "related_mappings", "annotations",
}


class ProjectionError(Exception):
    pass


def load(path):
    text = Path(path).read_text(encoding="utf-8")
    return yaml.safe_load(text), hashlib.sha256(text.encode("utf-8")).hexdigest()


def merge_imports(model, path):
    """Merge local imports into the model. Returns (local class names, local enum names, [(file, sha)])."""
    local = set(model.get("classes", {}) or {})
    local_enums = set(model.get("enums", {}) or {})
    imported = []
    for name in model.get("imports", []) or []:
        if name.startswith("linkml:"):
            continue
        ipath = Path(path).parent / f"{name}.yaml"
        if not ipath.is_file():
            raise ProjectionError(f"import {name}: {ipath} not found")
        imodel, isha = load(ipath)
        if [i for i in imodel.get("imports", []) or [] if not i.startswith("linkml:")]:
            raise ProjectionError(f"import {name}: nested local imports are not supported")
        for section in ("classes", "enums", "types"):
            target = model.setdefault(section, {}) or {}
            model[section] = target
            for key, value in (imodel.get(section, {}) or {}).items():
                if key in target:
                    raise ProjectionError(f"import {name}: {section[:-1]} {key} is defined twice")
                target[key] = value
        imported.append((ipath.name, isha))
    return local, local_enums, imported


class Projector:
    def __init__(self, model, local=None, local_enums=None):
        self.m = model
        self.local = set(model.get("classes", {}) or {}) if local is None else local
        self.local_enums = set(model.get("enums", {}) or {}) if local_enums is None else local_enums
        self.classes = model.get("classes", {})
        self.enums = model.get("enums", {})
        self.types = model.get("types", {})
        for name, cls in self.classes.items():
            unknown = set(cls or {}) - SUPPORTED_CLASS_KEYS
            if unknown:
                raise ProjectionError(f"class {name}: unsupported keys {sorted(unknown)}")
            for sname, slot in ((cls or {}).get("attributes") or {}).items():
                unknown = set(slot or {}) - SUPPORTED_SLOT_KEYS
                if unknown:
                    raise ProjectionError(f"{name}.{sname}: unsupported keys {sorted(unknown)}")

    # ----- class structure -----
    def ancestors(self, name):
        chain = []
        cur = name
        while cur:
            chain.append(cur)
            cur = (self.classes[cur] or {}).get("is_a")
        return list(reversed(chain))

    def induced_slots(self, name):
        slots = {}
        for cname in self.ancestors(name):
            cls = self.classes[cname] or {}
            for mixin in cls.get("mixins", []) or []:
                for sname, slot in ((self.classes[mixin] or {}).get("attributes") or {}).items():
                    slots[sname] = slot or {}
            for sname, slot in (cls.get("attributes") or {}).items():
                slots[sname] = slot or {}
        return slots

    def descendants(self, name):
        out = []
        for cname, cls in self.classes.items():
            if cname != name and name in self.ancestors(cname):
                out.append(cname)
        return out

    def concrete_descendants(self, name):
        return [c for c in self.descendants(name) if not (self.classes[c] or {}).get("abstract")]

    def identifier_slot(self, name):
        for sname, slot in self.induced_slots(name).items():
            if slot.get("identifier"):
                return sname
        return None

    def designator_slot(self, name):
        for sname, slot in self.induced_slots(name).items():
            if slot.get("designates_type"):
                return sname
        return None

    def is_mixin(self, name):
        return bool((self.classes[name] or {}).get("mixin"))

    # ----- type projection -----
    def type_schema(self, tname):
        if tname in BUILTIN_TYPES:
            return dict(BUILTIN_TYPES[tname])
        if tname in self.types:
            t = self.types[tname]
            base = self.type_schema(t["typeof"])
            if "pattern" in t:
                base["pattern"] = t["pattern"]
            if "description" in t:
                base["description"] = t["description"].strip()
            base["x-appspec-type"] = tname
            return base
        raise ProjectionError(f"unknown type {tname}")

    def range_schema(self, rng, slot):
        if rng in BUILTIN_TYPES or rng in self.types:
            return self.type_schema(rng)
        if rng in self.enums:
            return {"$ref": f"#/$defs/{rng}"}
        if rng in self.classes:
            if rng == "Any":
                return {}
            inlined = slot.get("inlined") or slot.get("inlined_as_list")
            ident = self.identifier_slot(rng)
            if ident and not inlined:
                id_slot = self.induced_slots(rng)[ident]
                ref = self.type_schema(id_slot.get("range", "string"))
                ref.pop("description", None)
                ref["x-appspec-ref"] = rng
                return ref
            if (self.classes[rng] or {}).get("abstract") and not self.designator_slot(rng):
                raise ProjectionError(f"abstract class {rng} without a type designator cannot be inlined")
            return {"$ref": f"#/$defs/{rng}"}
        raise ProjectionError(f"unknown range {rng}")

    def slot_schema(self, cname, sname, slot):
        if slot.get("designates_type"):
            return {"const": cname, "description": "Type designator: the ontology class of this object."}
        if "any_of" in slot:
            item = {"anyOf": [self.range_schema(alt["range"], slot) for alt in slot["any_of"]]}
        else:
            item = self.range_schema(slot.get("range", self.m.get("default_range", "string")), slot)
        if "pattern" in slot:
            item = dict(item)
            item["pattern"] = slot["pattern"]
        if "minimum_value" in slot:
            item = dict(item)
            item["minimum"] = slot["minimum_value"]
        if "maximum_value" in slot:
            item = dict(item)
            item["maximum"] = slot["maximum_value"]
        if slot.get("multivalued"):
            schema = {"type": "array", "items": item}
        else:
            schema = item
        if slot.get("description"):
            schema = dict(schema)
            schema["description"] = " ".join(slot["description"].split())
        return schema

    def class_def(self, cname):
        cls = self.classes[cname] or {}
        level = (cls.get("annotations") or {}).get("level")
        if cls.get("abstract"):
            disc = self.designator_slot(cname)
            if not disc:
                return None
            kinds = self.concrete_descendants(cname)
            d = {
                "type": "object",
                "required": [disc],
                "properties": {disc: {"enum": kinds}},
                "allOf": [
                    {"if": {"properties": {disc: {"const": k}}, "required": [disc]},
                     "then": {"$ref": f"#/$defs/{k}"}}
                    for k in kinds
                ],
                "x-appspec-abstract": True,
            }
        else:
            props, required = {}, []
            for sname, slot in self.induced_slots(cname).items():
                props[sname] = self.slot_schema(cname, sname, slot)
                if slot.get("required") or slot.get("identifier") or slot.get("designates_type"):
                    required.append(sname)
            d = {"type": "object", "properties": props}
            if required:
                d["required"] = required
            d["patternProperties"] = {"^x-": {"description": "Visible extension: a need the schema does not meet. Builders must not rely on it."}}
            d["additionalProperties"] = False
        if cls.get("description"):
            d["description"] = " ".join(cls["description"].split())
        if level:
            d["x-appspec-level"] = level
        perspective = (cls.get("annotations") or {}).get("perspective")
        if perspective:
            d["x-appspec-perspective"] = perspective
        parent = cls.get("is_a")
        if parent:
            d["x-appspec-is-a"] = parent
        return d

    def enum_def(self, ename):
        e = self.enums[ename] or {}
        values = list((e.get("permissible_values") or {}).keys())
        d = {"type": "string", "enum": values}
        if e.get("description"):
            d["description"] = " ".join(e["description"].split())
        return d

    def reachable(self, root):
        """Classes and enums reachable from root through slot ranges, ancestors and designated subclasses."""
        classes, enums, stack = set(), set(), [root]
        while stack:
            cname = stack.pop()
            if cname in classes or cname == "Any":
                continue
            classes.add(cname)
            cls = self.classes[cname] or {}
            stack.extend(self.ancestors(cname)[:-1])
            if cls.get("abstract") and self.designator_slot(cname):
                stack.extend(self.concrete_descendants(cname))
            for slot in self.induced_slots(cname).values():
                ranges = [alt["range"] for alt in slot.get("any_of", [])] or [slot.get("range", self.m.get("default_range", "string"))]
                for rng in ranges:
                    if rng in self.classes:
                        stack.append(rng)
                    elif rng in self.enums:
                        enums.add(rng)
        return classes, enums

    def project(self, source_sha, root=None, source_name="app_family.linkml.yaml", output_name="app-spec.schema.json", imported=()):
        roots = [c for c, cls in self.classes.items() if c in self.local and (cls or {}).get("tree_root")]
        if root is None:
            if len(roots) != 1:
                raise ProjectionError(f"expected exactly one local tree_root, found {roots}")
            root = roots[0]
        if root not in self.classes:
            raise ProjectionError(f"root class {root} is not defined")
        keep_classes, keep_enums = self.reachable(root)
        for cname in self.local:
            more_classes, more_enums = self.reachable(cname)
            keep_classes |= more_classes
            keep_enums |= more_enums
        keep_classes |= self.local
        keep_enums |= self.local_enums
        defs = {}
        for cname in self.classes:
            if cname == "Any" or self.is_mixin(cname) or cname not in keep_classes:
                continue
            d = self.class_def(cname)
            if d is not None:
                defs[cname] = d
        for ename in self.enums:
            if ename in keep_enums:
                defs[ename] = self.enum_def(ename)
        major_minor = ".".join(str(self.m.get("version", "0.1")).split("-")[0].split(".")[:2])
        if not output_name.endswith(".schema.json"):
            raise ProjectionError(f"output {output_name} must end in .schema.json")
        schema_file = output_name[: -len(".schema.json")] + f"-{major_minor}.schema.json"
        title = ((self.classes[root] or {}).get("annotations") or {}).get("title", "App specification")
        comment = "ontology_sha256=" + source_sha + "".join(f"; import {name} sha256={sha}" for name, sha in imported)
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": self.m["id"].rstrip("/") + "/" + schema_file,
            "title": title + " (projection of " + self.m["name"] + " " + str(self.m.get("version")) + ")",
            "description": "Generated by tools/project_schema.py from formats/" + source_name + ". Do not edit by hand; edit the ontology and re-project.",
            "$comment": comment,
            "$ref": f"#/$defs/{root}",
            "$defs": defs,
        }


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    root = None
    if "--root" in argv:
        position = argv.index("--root")
        if position + 1 >= len(argv):
            print("--root needs a class name")
            return 2
        root = argv[position + 1]
    model, sha = load(argv[1])
    local, local_enums, imported = merge_imports(model, argv[1])
    schema = Projector(model, local, local_enums).project(
        sha, root=root, source_name=Path(argv[1]).name, output_name=Path(argv[2]).name, imported=imported)
    text = json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
    out = Path(argv[2])
    if "--check" in argv:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != text:
            print(f"DRIFT: {out} is not the projection of {argv[1]}")
            return 1
        print(f"OK: {out} matches the projection of {argv[1]}")
        return 0
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out} ({len(schema['$defs'])} definitions; ontology sha256 {sha[:12]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
