#!/usr/bin/env python3
"""Compare a Codex pin with the prior pin before the App relies on it (DEL-01-01 REQ-006, VER-006).

The comparison covers the generated schema, the supplement and the recorded exchanges
of both pins, derives what the App relies on from its host source, and returns a verdict:
"passed" only when every finding that touches what the App relies on has a disposition
citing a recorded decision and no input was missing; otherwise "returned for decision"
(CLM-003). The tool executes no supplier and no model and reads only the files named by
its arguments.

Usage, from `app/`:
  python3 supplier_checks/version_advance.py compare --from 0.160.0 --to 0.167.0 \
      --out supplier_checks/version_advance/0.160.0-to-0.167.0.json

Every input location is an argument with a repository default:
  --resources DIR         folder holding <pin>/ with the generated bundles and MANIFEST.sha256
                          (default src-tauri/resources/supplier); --from-resources and
                          --to-resources override it for one pin
  --from-recordings DIR   recordings of the prior pin (default supplier_checks/recordings/<pin>,
  --to-recordings DIR     and supplier_checks/recordings for 0.160.0, where they were first kept)
  --from-supplement FILE  optional supplement per pin (default <resources>/<pin>/SUPPLEMENT.json);
  --to-supplement FILE    absence is read as an empty supplement and stated in the result
  --source DIR            the App's host source (default src-tauri/src)
  --dispositions FILE     authored decisions on findings (default
                          supplier_checks/version_advance/<from>-to-<to>.dispositions.json)

Exit status: 0 passed, 1 returned for decision, 2 refused (unknown pin or unusable argument).
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
APP = HERE.parent
REPO = APP.parent
FORMAT = "chirality.app-v4.version-advance.v1"
SCENARIOS = ("nv04", "st5", "st5-race")
RECORDING_FORMATS = ("chirality.app-v4.hosting-capture.st5.v1", "chirality.app-v4.supplier-capture.v2")
BUNDLE = "codex_app_server_protocol.schemas.json"
V2_BUNDLE = "codex_app_server_protocol.v2.schemas.json"
MANIFEST = "MANIFEST.sha256"
SUPPLEMENT = "SUPPLEMENT.json"
UNIONS = {"ClientRequest": "client_requests", "ClientNotification": "client_notifications",
          "ServerRequest": "server_requests", "ServerNotification": "server_notifications"}
PIN = re.compile(r"^\d+\.\d+\.\d+$")
ANNOTATIONS = ("description", "title")
LOWER_BOUNDS = ("minItems", "minLength", "minimum")
UPPER_BOUNDS = ("maxItems", "maxLength", "maximum")
ID_KEY = re.compile(r"^(?:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|\d+)$")

RULES = {
    "classification": {
        "documentation only": "only the description or title keyword of a schema object differs (never a "
                              "property or definition of that name)",
        "additive": "a new optional property, a new enum value, a new anyOf member, a new oneOf member that is "
                    "disjoint from every other member, the previous form kept as one alternative (anyOf, or "
                    "oneOf with the kept form disjoint from every other member; constraints placed beside the "
                    "choice are compared with the previous form's separately), a widened type (a type added to "
                    "the type set, integer to number, a lower bound lowered or removed, an upper bound raised or "
                    "removed, a format, enum, allOf member or items constraint removed, additionalProperties "
                    "opened), oneOf turned into anyOf",
        "breaking": "a removed property, enum value or alternative, a narrowed or changed type (a type removed "
                    "or replaced, a reference to a different definition, a form replaced, a constraint added or "
                    "tightened, additionalProperties closed), a newly required property, anyOf turned into oneOf",
        "unclassified": "anything else, including a property that is no longer required, a changed default, a "
                        "changed format, a changed $schema, a type set rewritten with the same effect, a new oneOf "
                        "member that is not shown disjoint from every other member, and a widening inside a oneOf "
                        "member that is not shown disjoint from every other member; never counted as additive",
        "oneOf": "two members are shown disjoint when the JSON types they can accept (from type, enum or const; "
                 "number admits integer) do not overlap, or both require a property whose schema admits one value "
                 "(a single-value enum or a const) and the values differ, or both are enums or consts with no "
                 "common value; a member given by $ref is never shown disjoint",
        "alternatives": "anyOf/oneOf/allOf members are matched by their method or type discriminator, their "
                        "$ref, a single enum value, a bare type, their title, or else their exact content",
        "new_optional_property": "a newly named optional property is classed additive although, where additional "
                                 "properties were open, it constrains a value an earlier sender could have sent "
                                 "under that name; the generated schemas leave additional properties open because "
                                 "the supplier ignores unknown fields, not to admit any value under future names",
    },
    "standing": "read from MANIFEST.sha256 at file level: an element is experimental exactly when its file is "
                "in json-schema/experimental and not json-schema/stable; variants_differ says the two variants "
                "of a file present in both have different digests; ts/ lines and comment lines are not read",
    "relied_on": "a protocol method is relied on when its exact name appears as a Rust string literal in the "
                 "host source outside files ending _tests.rs and outside modules gated by #[cfg(test)] or "
                 "#[cfg(all(test, ...))]; a definition is relied on when it is reachable by $ref, at either pin, "
                 "from the params of a relied-on client request or notification, from that request's response "
                 "definition, or from the params and response of a relied-on server request or the params of "
                 "a relied-on server notification; a response definition is <Name>Response for params "
                 "<Name>Params, else the method's segments in PascalCase followed by Response, in the same "
                 "namespace",
    "shape": "per scenario and per supplier notification, server request and reply to a request made at both "
             "pins: the set of key paths with their JSON value types and whether each path is present in every "
             "such frame; every scalar value is ignored (so identifiers, times, paths and text), as are array "
             "lengths, the order of array items and keys, and object keys that are UUIDs or digit strings "
             "(read as <id>)",
    "validation": "jsonschema Draft 7 against the to-pin bundle's ServerNotification (frames from the supplier "
                  "with a method and no id) and ServerRequest (frames from the supplier with an id and a method); "
                  "the supplier's replies to App requests and the App's own frames are not validated (replies are "
                  "compared by shape only); formats are not asserted",
    "absent_groups": "a supplier notification or server request group recorded at the prior pin is judged driven "
                     "at the new pin when the App-side frame that precedes its first occurrence in the prior "
                     "recording (same generation, direction, kind and method, counted by occurrence) also occurs "
                     "in the new recording; a reply group is judged driven when the App request it answers occurs "
                     "in the new recording; a group that is driven and absent is a finding when its method is "
                     "relied on, and a group that is not driven is listed as not driven",
    "inputs": "each pin needs a main bundle whose definitions hold the four method unions, each with members, and "
              "non-empty v2 definitions; a v2 bundle equal to the main bundle's v2 definitions in both "
              "directions (references rewritten to the flat form); a manifest listing files in both variants; "
              "a recording of every scenario with frames; the host source must yield at least one relied-on "
              "method; a file that is absent where it is optional is read as empty, while a path that exists "
              "and cannot be read as a file is an input problem",
    "findings": "a breaking or unclassified schema change, a removed method or definition, a standing change, a "
                "failed validation, a removed or retyped recorded key path, a recorded group absent although "
                "driven, or a changed or unobservable "
                "mechanism that involves a relied-on method or definition; its id is VA- and the first 12 hex "
                "digits of the SHA-256 of its kind, subject and detail",
    "additive_rule": "additive and documentation-only changes to relied-on elements need no decision because a "
                     "receiver must accept unknown enum values and extra fields and a sender is not obliged to "
                     "send new optional fields",
    "verdict": "passed only when every finding has a disposition, every disposition names a finding of this "
               "comparison and no input was missing or unusable; otherwise returned for decision",
}


class Refused(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


# ---------- inputs ----------
class Inputs:
    """Reads files and keeps the identity of every input, missing or unusable inputs included."""

    def __init__(self):
        self.read, self.missing, self.problems = [], [], []

    @staticmethod
    def label(path, argument, base):
        path = Path(os.path.abspath(path))
        try:
            return path.relative_to(REPO).as_posix()
        except ValueError:
            return "<%s>/%s" % (argument, os.path.relpath(path, os.path.abspath(base)).replace(os.sep, "/"))

    def bytes(self, role, path, argument, base, required=True):
        label = self.label(path, argument, base)
        try:
            if Path(path).exists() and not Path(path).is_file():
                raise IsADirectoryError(path)
            data = Path(path).read_bytes()
        except FileNotFoundError:
            entry = {"role": role, "path": label, "state": "missing" if required else "absent, read as empty"}
            (self.missing if required else self.read).append(entry)
            return None
        except OSError as error:
            self.problems.append({"role": role, "path": label,
                                  "problem": "present but not readable as a file (%s)" % type(error).__name__})
            return None
        self.read.append({"role": role, "path": label, "sha256": digest(data)})
        return data

    def json(self, role, path, argument, base, required=True):
        data = self.bytes(role, path, argument, base, required)
        if data is None:
            return None
        try:
            return json.loads(data)
        except ValueError:
            self.problems.append({"role": role, "path": self.label(path, argument, base), "problem": "not JSON"})
            return None


# ---------- schema ----------
def definitions(bundle):
    """{"Name": node, "v2/Name": node} from an experimental bundle."""
    found = {name: node for name, node in bundle.get("definitions", {}).items() if name != "v2"}
    found.update(("v2/" + name, node) for name, node in bundle.get("definitions", {}).get("v2", {}).items())
    return found


def bundle_problems(bundle):
    """What makes a main bundle unusable for the comparison; [] when it is usable."""
    if not isinstance(bundle, dict) or not isinstance(bundle.get("definitions"), dict):
        return ["no definitions object"]
    problems = []
    if not isinstance(bundle["definitions"].get("v2"), dict) or not bundle["definitions"]["v2"]:
        problems.append("no v2 definitions")
    for union in UNIONS:
        members = (bundle["definitions"].get(union) or {}).get("oneOf") if isinstance(
            bundle["definitions"].get(union), dict) else None
        if not isinstance(members, list) or not members or not all(
                isinstance(m, dict) and ((m.get("properties") or {}).get("method") or {}).get("enum")
                for m in members):
            problems.append("no usable %s union (members naming their method)" % union)
    return problems


def v2_bundle_differences(defs, v2_bundle):
    """Names whose v2-bundle copy differs from the main bundle's (references rewritten to the flat form),
    including every main-bundle v2 definition the v2 bundle lacks."""
    flat_defs = v2_bundle.get("definitions") if isinstance(v2_bundle, dict) else None
    if not isinstance(flat_defs, dict):
        return ["<no definitions object>"]
    differences = []
    for name, node in sorted(flat_defs.items()):
        main = defs.get("v2/" + name, defs.get(name))
        flat = None if main is None else json.loads(canonical(main).replace('"#/definitions/v2/', '"#/definitions/'))
        if flat != node:
            differences.append(name)
    differences += ["%s (absent from the v2 bundle)" % name[len("v2/"):] for name in sorted(defs)
                    if name.startswith("v2/") and name[len("v2/"):] not in flat_defs]
    return differences


def ref_name(ref):
    return ref[len("#/definitions/"):] if ref.startswith("#/definitions/") else None


def union_methods(defs, union):
    methods = {}
    for alternative in (defs.get(union) or {}).get("oneOf", []):
        names = ((alternative.get("properties") or {}).get("method") or {}).get("enum") or []
        for name in names:
            methods[name] = alternative
    return methods


def params_of(alternative):
    params = (alternative.get("properties") or {}).get("params") or {}
    return ref_name(params.get("$ref", ""))


def response_of(method, alternative, defs):
    params = params_of(alternative)
    namespace = "v2/" if params and params.startswith("v2/") else ""
    candidates = []
    if params and params.endswith("Params"):
        candidates.append(params[:-len("Params")] + "Response")
    pascal = "".join(part[:1].upper() + part[1:] for part in re.split(r"[/_]", method) if part) + "Response"
    candidates += [namespace + pascal, pascal, "v2/" + pascal]
    return next((name for name in candidates if name in defs), None)


def refs_in(node, found):
    if isinstance(node, dict):
        name = ref_name(node.get("$ref", "")) if isinstance(node.get("$ref"), str) else None
        if name:
            found.add(name)
        for value in node.values():
            refs_in(value, found)
    elif isinstance(node, list):
        for value in node:
            refs_in(value, found)
    return found


def refs_all(node, found):
    """Every $ref string in the node."""
    if isinstance(node, dict):
        if isinstance(node.get("$ref"), str):
            found.add(node["$ref"])
        for value in node.values():
            refs_all(value, found)
    elif isinstance(node, list):
        for value in node:
            refs_all(value, found)
    return found


def closure(roots, defs):
    seen, stack = set(), [root for root in roots if root in defs]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        stack += [ref for ref in refs_in(defs[name], set()) if ref in defs and ref not in seen]
    return seen


SCHEMA_MAPS = ("properties", "patternProperties", "definitions")
SCHEMA_LISTS = ("anyOf", "oneOf", "allOf")
SCHEMA_SINGLE = ("items", "additionalItems", "additionalProperties", "contains", "propertyNames", "not", "if",
                 "then", "else")


def strip_annotations(node):
    """The schema without description and title, removed only where they are keywords of a
    schema object, never where they name a property or a definition."""
    if not isinstance(node, dict):
        return node
    out = {}
    for key, value in node.items():
        if key in ANNOTATIONS:
            continue
        if key in SCHEMA_MAPS and isinstance(value, dict):
            out[key] = {name: strip_annotations(inner) for name, inner in value.items()}
        elif key in SCHEMA_LISTS and isinstance(value, list):
            out[key] = [strip_annotations(inner) for inner in value]
        elif key in SCHEMA_SINGLE:
            out[key] = [strip_annotations(inner) for inner in value] if isinstance(value, list) \
                else strip_annotations(value)
        else:
            out[key] = value
    return out


def core(node):
    """strip_annotations, also without the $schema keyword of the node itself."""
    stripped = strip_annotations(node)
    if isinstance(stripped, dict):
        stripped.pop("$schema", None)
    return stripped


def alternative_key(node):
    if not isinstance(node, dict):
        return "json:" + canonical(node)
    rest = set(node) - set(ANNOTATIONS) - {"$schema"}
    if "$ref" in node and rest == {"$ref"}:
        return "$ref=" + str(ref_name(node["$ref"]) or node["$ref"])
    properties = node.get("properties") or {}
    for discriminator in ("method", "type"):
        values = (properties.get(discriminator) or {}).get("enum")
        if isinstance(values, list) and len(values) == 1:
            return "%s=%s" % (discriminator, values[0])
    if isinstance(node.get("enum"), list):
        return "enum=" + canonical(node["enum"][0]) if len(node["enum"]) == 1 else \
            "enum of " + canonical(node.get("type"))
    if "type" in node and rest <= {"type", "format", "items", "additionalProperties"}:
        return "type=" + canonical(node["type"])
    if "title" in node:
        return "title=" + str(node["title"])
    return "content=" + digest(canonical(core(node)).encode())[:12]


def keyed(alternatives):
    keyed_list, counts = {}, {}
    for alternative in alternatives:
        key = alternative_key(alternative)
        counts[key] = counts.get(key, 0) + 1
        keyed_list[key if counts[key] == 1 else "%s#%d" % (key, counts[key])] = alternative
    return keyed_list


def types_of(node):
    value = node.get("type")
    return set(value) if isinstance(value, list) else {value}


def covers(wider, narrower):
    """True when the JSON type set `wider` admits every type of `narrower` (number admits integer)."""
    return all(kind in wider or (kind == "integer" and "number" in wider) for kind in narrower)


def possible_types(node):
    """The JSON types a schema object can accept, or None when that is not evident from the node."""
    if not isinstance(node, dict) or "$ref" in node:
        return None
    if isinstance(node.get("enum"), list):
        kinds = {json_type(value) for value in node["enum"]}
    elif "const" in node:
        kinds = {json_type(node["const"])}
    elif "type" in node:
        return types_of(node)
    else:
        return None
    return {kind for kind in kinds if covers(types_of(node), {kind})} if "type" in node else kinds


def tags(node):
    """{property: value} for each required property whose schema admits a single value (enum or const)."""
    if not isinstance(node, dict) or "$ref" in node:
        return {}
    required, found = set(node.get("required") or []), {}
    for name, schema in (node.get("properties") or {}).items():
        if name in required and isinstance(schema, dict):
            if isinstance(schema.get("enum"), list) and len(schema["enum"]) == 1:
                found[name] = canonical(schema["enum"][0])
            elif "const" in schema:
                found[name] = canonical(schema["const"])
    return found


def enum_values(node):
    if not isinstance(node, dict) or "$ref" in node:
        return None
    if isinstance(node.get("enum"), list):
        return {canonical(value) for value in node["enum"]}
    if "const" in node:
        return {canonical(node["const"])}
    return None


def disjoint(first, second):
    """True only when no instance can satisfy both schemas, shown by RULES["oneOf"]."""
    kinds = possible_types(first), possible_types(second)
    if None not in kinds and not (any(covers(kinds[1], {k}) for k in kinds[0])
                                  or any(covers(kinds[0], {k}) for k in kinds[1])):
        return True
    first_tags, second_tags = tags(first), tags(second)
    if any(name in second_tags and second_tags[name] != value for name, value in first_tags.items()):
        return True
    values = enum_values(first), enum_values(second)
    return None not in values and not (values[0] & values[1])


def diff_schema(before, after, path=""):
    """Every change between two schema nodes, each classified by RULES["classification"]."""
    changes = []

    def change(where, kind, what, old=None, new=None):
        record = {"path": where, "class": kind, "change": what}
        if old is not None:
            record["before"] = old
        if new is not None:
            record["after"] = new
        changes.append(record)

    if before == after:
        return changes
    if not (isinstance(before, dict) and isinstance(after, dict)):
        change(path, "unsupported", "schema is not an object on both sides (boolean schemas are not supported)",
               before, after)
        return changes
    for key in ANNOTATIONS:
        if before.get(key) != after.get(key):
            change(path + "/" + key, "documentation only", key + " changed", before.get(key), after.get(key))
    if before.get("$schema") != after.get("$schema"):
        change(path + "/$schema", "unclassified", "$schema (dialect) changed", before.get("$schema"),
               after.get("$schema"))
    choices = ("anyOf", "oneOf")
    old_choice = [k for k in choices if k in before]
    new_choice = [k for k in choices if k in after]
    if not old_choice and len(new_choice) == 1:
        choice = new_choice[0]
        members = after[choice]
        kept = [i for i, alt in enumerate(members) if core(alt) == core(before)]
        if kept:
            others = [alt for i, alt in enumerate(members) if i != kept[0]]
            if choice == "oneOf" and not all(disjoint(members[kept[0]], other) for other in others):
                change(path, "unclassified", "new alternative (the previous form is kept as one oneOf alternative, "
                                             "which another alternative may also match)")
            else:
                change(path, "additive", "new alternative (the previous form is kept as one alternative)")
            # Constraints beside the choice now apply to the previous form too.
            siblings = {k: v for k, v in after.items() if k not in ANNOTATIONS + ("$schema", choice)}
            previous = {k: v for k, v in before.items() if k in siblings}
            changes.extend(diff_schema(previous, siblings, path))
            return changes
    if not new_choice and any(core(alt) == core(after) for k in old_choice for alt in before[k]):
        change(path, "breaking", "alternative removed (the form is now one former alternative)")
        return changes
    if before.get("$ref") != after.get("$ref"):
        change(path, "breaking", "changed type (reference to a different definition)" if "$ref" in before
               and "$ref" in after else "changed type (form replaced)", before.get("$ref"), after.get("$ref"))
        return changes
    if old_choice == ["oneOf"] and new_choice == ["anyOf"]:
        change(path, "additive", "oneOf became anyOf (an instance may now match several alternatives)")
        before = dict(before, anyOf=before["oneOf"])
        del before["oneOf"]
    elif old_choice == ["anyOf"] and new_choice == ["oneOf"]:
        change(path, "breaking", "anyOf became oneOf (an instance must now match exactly one alternative)")
        before = dict(before, oneOf=before["anyOf"])
        del before["anyOf"]
    for key in sorted((set(before) | set(after)) - set(ANNOTATIONS) - {"$ref", "$schema"}):
        old, new, where = before.get(key), after.get(key), path + "/" + key
        if old == new:
            continue
        if key == "properties":
            old, new = old or {}, new or {}
            required = set(after.get("required") or [])
            for name in sorted(set(old) | set(new)):
                if name not in new:
                    kept = sorted(str(alt.get("title", alternative_key(alt))) for k in choices
                                  for alt in after.get(k, []) if isinstance(alt, dict)
                                  and core((alt.get("properties") or {}).get(name)) == core(old[name]))
                    change(where + "/" + name, "breaking", "property removed" + (
                        " (kept only in the alternative %s)" % ", ".join(kept) if kept else ""))
                elif name not in old:
                    if name in required:
                        change(where + "/" + name, "breaking", "required property added")
                    else:
                        change(where + "/" + name, "additive", "optional property added")
                else:
                    changes.extend(diff_schema(old[name], new[name], where + "/" + name))
        elif key == "required":
            old_set, new_set = set(old or []), set(new or [])
            old_properties, new_properties = before.get("properties") or {}, after.get("properties") or {}
            for name in sorted(new_set - old_set):
                if not (name in new_properties and name not in old_properties):  # else "required property added"
                    change(where + "/" + name, "breaking", "property newly required")
            for name in sorted(old_set - new_set):
                if not (name in old_properties and name not in new_properties):  # else "property removed"
                    change(where + "/" + name, "unclassified", "property no longer required")
        elif key == "enum":
            if old is None:
                change(where, "breaking", "enum constraint added")
            elif new is None:
                change(where, "additive", "enum constraint removed")
            else:
                for value in sorted(map(canonical, old)):
                    if value not in map(canonical, new):
                        change(where + "/" + value, "breaking", "enum value removed")
                for value in sorted(map(canonical, new)):
                    if value not in map(canonical, old):
                        change(where + "/" + value, "additive", "enum value added")
        elif key == "type":
            old_set, new_set = types_of(before), types_of(after)
            if old is None:
                alternatives = before.get("anyOf", []) + before.get("oneOf", [])
                already = alternatives and all(isinstance(a, dict) and "type" in a and types_of(a) <= new_set
                                               for a in alternatives)
                change(where, "breaking", "type narrowed (type constraint added%s)" % (
                    "; every alternative already had this type" if already else ""), None, new)
            elif new is None:
                change(where, "additive", "type widened (type constraint removed)", old, None)
            elif covers(new_set, old_set) and not covers(old_set, new_set):
                change(where, "additive", "type widened", old, new)
            elif covers(old_set, new_set) and not covers(new_set, old_set):
                change(where, "breaking", "type narrowed", old, new)
            elif covers(old_set, new_set):
                change(where, "unclassified", "type set rewritten", old, new)
            else:
                change(where, "breaking", "type changed", old, new)
        elif key in ("anyOf", "oneOf", "allOf") and (old is None or new is None):
            change(where, "breaking" if old is None else "additive",
                   "%s constraint %s" % (key, "added" if old is None else "removed"))
        elif key in ("anyOf", "oneOf", "allOf"):
            old_keyed, new_keyed = keyed(old or []), keyed(new or [])
            for name in sorted(set(old_keyed) | set(new_keyed)):
                at = "%s[%s]" % (where, name)
                apart = key != "oneOf" or name not in new_keyed or all(
                    disjoint(new_keyed[name], other) for other_name, other in new_keyed.items() if other_name != name)
                if name not in new_keyed:
                    change(at, "additive" if key == "allOf" else "breaking",
                           "allOf member removed" if key == "allOf" else "alternative removed")
                elif name not in old_keyed:
                    if key == "allOf":
                        change(at, "breaking", "allOf member added")
                    elif apart:
                        change(at, "additive", "alternative added")
                    else:
                        change(at, "unclassified", "oneOf alternative added that another alternative may also match")
                else:
                    inner = diff_schema(old_keyed[name], new_keyed[name], at)
                    if not apart:  # widening a oneOf member may make it overlap another member
                        inner = [dict(item, **{"class": "unclassified", "change": item["change"] +
                                               " (in a oneOf alternative that another alternative may also match)"})
                                 if item["class"] == "additive" else item for item in inner]
                    changes.extend(inner)
        elif key == "items":
            if isinstance(old, dict) and isinstance(new, dict):
                changes.extend(diff_schema(old, new, where))
            elif old is None:
                change(where, "breaking", "items constraint added")
            elif new is None:
                change(where, "additive", "items constraint removed")
            else:
                change(where, "unsupported", "items as a list or boolean is not supported", old, new)
        elif key == "additionalProperties":
            if isinstance(old, dict) and isinstance(new, dict):
                changes.extend(diff_schema(old, new, where))
            else:
                openness = {None: 2, True: 2, False: 0}
                old_open = 1 if isinstance(old, dict) else openness.get(old)
                new_open = 1 if isinstance(new, dict) else openness.get(new)
                if old_open is None or new_open is None:
                    change(where, "unsupported", "additionalProperties value is not a boolean or schema", old, new)
                elif old_open == new_open:
                    change(where, "unclassified", "additionalProperties written differently (true or omitted)",
                           old, new)
                elif new_open > old_open:
                    change(where, "additive", "additionalProperties opened", old, new)
                else:
                    change(where, "breaking", "additionalProperties closed", old, new)
        elif key in LOWER_BOUNDS + UPPER_BOUNDS:
            lower = key in LOWER_BOUNDS
            if old is None:
                change(where, "breaking", "bound added", None, new)
            elif new is None:
                change(where, "additive", "bound removed", old, None)
            elif not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (old, new)):
                change(where, "unclassified", "bound changed", old, new)
            elif (new > old) == lower:
                change(where, "breaking", "bound tightened", old, new)
            else:
                change(where, "additive", "bound relaxed", old, new)
        elif key == "format":
            if old is None:
                change(where, "breaking", "format added", None, new)
            elif new is None:
                change(where, "additive", "format removed", old, None)
            else:
                change(where, "unclassified", "format changed", old, new)
        else:
            change(where, "unclassified" if key == "default" else "unsupported",
                   "default changed" if key == "default" else "keyword %s is not supported" % key, old, new)
    return changes


def union_method_of(path):
    match = re.match(r"^(ClientRequest|ClientNotification|ServerRequest|ServerNotification)/oneOf\[method=([^\]]+)\]",
                     path)
    return match.groups() if match else (None, None)


# ---------- standing ----------
def manifest_elements(text):
    variants = {"stable": {}, "experimental": {}}
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        sha, _, path = line.partition("  ")
        match = re.match(r"^json-schema/(stable|experimental)/(.+)\.json$", path.strip())
        if match and not match.group(2).startswith("codex_app_server_protocol."):
            variants[match.group(1)][match.group(2)] = sha.strip()
    elements = {}
    for name in sorted(set(variants["stable"]) | set(variants["experimental"])):
        stable, experimental = variants["stable"].get(name), variants["experimental"].get(name)
        elements[name] = {"standing": "experimental" if experimental and not stable else "stable",
                          "variants_differ": bool(stable and experimental and stable != experimental),
                          "in_experimental": bool(experimental), "in_stable": bool(stable)}
    return elements


def element_definition(element):
    return element[len("v1/"):] if element.startswith("v1/") else element


# ---------- host source ----------
LITERAL = re.compile(r'//[^\n]*|/\*|(?<![A-Za-z0-9_])b?r(#*)"|"((?:[^"\\]|\\.)*)"|'
                     r"'(?:\\(?:'|[^'\n]*)|[^\\'\n])'", re.S)
TEST_MODULE = re.compile(r"#\s*\[\s*cfg\s*\(\s*(?:test|all\s*\([^)\]]*\btest\b[^\]]*)\)\s*\]\s*"
                         r"(?:#\s*\[[^\]]*\]\s*)*(?:pub(?:\s*\([^)]*\))?\s+)?mod\s+\w+\s*\{")


def rust_literals(text):
    """([(offset, value)], masked text) for the string literals of a Rust file; comments and
    literals are blanked in the masked text so that braces can be counted."""
    literals, masked, position = [], list(text), 0

    def blank(start, end):
        for index in range(start, end):
            if masked[index] != "\n":
                masked[index] = " "

    while True:
        match = LITERAL.search(text, position)
        if not match:
            break
        start, token = match.start(), match.group(0)
        if token == "/*":
            depth, end = 1, start + 2
            while end < len(text) and depth:
                if text.startswith("/*", end):
                    depth, end = depth + 1, end + 2
                elif text.startswith("*/", end):
                    depth, end = depth - 1, end + 2
                else:
                    end += 1
        elif token.startswith("//"):
            end = match.end()
        elif match.group(1) is not None:
            close = text.find('"' + match.group(1), match.end())
            close = len(text) if close < 0 else close
            literals.append((start, text[match.end():close]))
            end = close + 1 + len(match.group(1))
        elif match.group(2) is not None:
            value = re.sub(r'\\(["\\nrt0])', lambda m: {"n": "\n", "r": "\r", "t": "\t", "0": "\0"}.get(
                m.group(1), m.group(1)), match.group(2))
            literals.append((start, value))
            end = match.end()
        else:
            end = match.end()
        blank(start, end)
        position = max(end, start + 1)
    return literals, "".join(masked)


def test_module_ranges(masked):
    ranges = []
    for match in TEST_MODULE.finditer(masked):
        depth, index = 0, match.end() - 1
        while index < len(masked):
            depth += {"{": 1, "}": -1}.get(masked[index], 0)
            if depth == 0:
                break
            index += 1
        ranges.append((match.start(), index + 1))
    return ranges


def relied_methods(source, names, inputs):
    """{method: [files]} for the protocol method names found as literals in the host source."""
    found = {}
    files = sorted(path for path in Path(source).rglob("*.rs") if not path.name.endswith("_tests.rs"))
    if not files:
        inputs.missing.append({"role": "host source", "path": Inputs.label(source, "source", source),
                               "state": "missing"})
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        literals, masked = rust_literals(text)
        excluded = test_module_ranges(masked)
        relative = Path(os.path.relpath(path, source)).as_posix()
        for offset, value in literals:
            if value in names and not any(start <= offset < end for start, end in excluded):
                found.setdefault(value, set()).add(relative)
    return {name: sorted(paths) for name, paths in sorted(found.items())}, len(files)


# ---------- recordings ----------
def recording_pin(record):
    if "pin" in record:
        return record["pin"]
    begin = next((event for event in record.get("events", []) if event.get("event") == "begin"), {})
    return begin.get("pin")


def frame_rows(record):
    return [row for row in record.get("frames", []) if isinstance(row.get("frame"), dict)]


def classify(rows):
    """[(row, kind, method)] with replies attributed to the method of the request they answer."""
    requests, out = {}, []
    for row in rows:
        frame, direction = row["frame"], row["direction"]
        if "method" in frame and "id" in frame:
            requests[(row["generation"], direction, canonical(frame["id"]))] = frame["method"]
            out.append((row, "request", frame["method"]))
        elif "method" in frame:
            out.append((row, "notification", frame["method"]))
        else:
            other = "codex->app" if direction == "app->codex" else "app->codex"
            method = requests.get((row["generation"], other, canonical(frame.get("id"))))
            out.append((row, "error-reply" if "error" in frame else "reply", method or "<unmatched>"))
    return out


def recording_problem(record, scenario, pin):
    """Why a recording cannot be compared, or None."""
    if not isinstance(record, dict):
        return "not a recording object"
    if record.get("format") not in RECORDING_FORMATS or record.get("scenario") != scenario \
            or recording_pin(record) != pin:
        return "format, scenario or pin is not the one expected"
    frames = record.get("frames")
    if not isinstance(frames, list) or not frames:
        return "no frames"
    if "events" in record and not (isinstance(record["events"], list)
                                   and all(isinstance(event, dict) for event in record["events"])):
        return "events is not a list of objects"
    keys = {"generation", "direction", "position", "frame"}
    if not all(isinstance(row, dict) and keys <= set(row) and row["direction"] in ("app->codex", "codex->app")
               and isinstance(row["frame"], dict) for row in frames):
        return "a frame row lacks generation, direction, position or a JSON object frame"
    return None


def token(row, kind, method):
    return "g%s %s %s %s" % (row["generation"], row["direction"], kind, method)


def absent_groups(before_rows, after_rows, before_shapes, after_shapes):
    """{group: {"driven": bool, "driven_by": str}} for the supplier groups of the prior recording that the
    new recording lacks, judged by RULES["absent_groups"]."""
    before, after = classify(before_rows), classify(after_rows)
    after_tokens = [token(row, kind, method) for row, kind, method in after]
    out = {}
    for group in sorted(set(before_shapes) - set(after_shapes)):
        kind, method = group.rsplit(" ", 1)
        if kind == "reply to":
            needed = [t for t in after_tokens if t.endswith(" app->codex request " + method)]
            out[group] = {"driven": bool(needed), "driven_by": "the App request " + method}
            continue
        wanted = {"notification": "notification", "server request": "request"}[kind]
        first = next(i for i, (row, k, m) in enumerate(before)
                     if row["direction"] == "codex->app" and k == wanted and m == method)
        previous = next((i for i in range(first - 1, -1, -1) if before[i][0]["direction"] == "app->codex"), None)
        if previous is None:
            out[group] = {"driven": True, "driven_by": "the start of the recording"}
            continue
        step = token(*before[previous])
        occurrence = sum(token(*item) == step for item in before[:previous + 1])
        out[group] = {"driven": after_tokens.count(step) >= occurrence,
                      "driven_by": "%s (occurrence %d)" % (step, occurrence)}
    return out


def sequence(rows):
    return ["g%s %s %s %s" % (row["generation"], row["direction"], kind, method)
            for row, kind, method in classify(rows)]


def sequence_differences(before, after):
    matcher = difflib.SequenceMatcher(None, before, after, autojunk=False)
    return [{"op": op, "from": before[i1:i2], "to": after[j1:j2]}
            for op, i1, i2, j1, j2 in matcher.get_opcodes() if op != "equal"]


def json_type(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    return {float: "number", str: "string", list: "array", dict: "object"}[type(value)]


def shape_paths(value, prefix, out):
    out.setdefault(prefix or "$", set()).add(json_type(value))
    if isinstance(value, dict):
        for key, inner in value.items():
            shape_paths(inner, "%s.%s" % (prefix or "$", "<id>" if ID_KEY.match(key) else key), out)
    elif isinstance(value, list):
        for inner in value:
            shape_paths(inner, (prefix or "$") + "[]", out)
    return out


def shapes(rows, from_supplier_only=True):
    """{group: {path: {"types": [...], "in_every_frame": bool}}} for supplier frames."""
    grouped = {}
    for row, kind, method in classify(rows):
        if from_supplier_only and row["direction"] != "codex->app":
            continue
        group = {"request": "server request", "notification": "notification"}.get(kind, "reply to") + " " + method
        grouped.setdefault(group, []).append(shape_paths(row["frame"], "", {}))
    result = {}
    for group, frames in grouped.items():
        paths = {}
        for frame in frames:
            for path, kinds in frame.items():
                entry = paths.setdefault(path, {"types": set(), "count": 0})
                entry["types"] |= kinds
                entry["count"] += 1
        result[group] = {path: {"types": sorted(entry["types"]), "in_every_frame": entry["count"] == len(frames)}
                         for path, entry in paths.items()}
    return result


def shape_differences(before, after):
    out = {}
    for group in sorted(set(before) & set(after)):
        old, new = before[group], after[group]
        entry = {
            "paths_only_before": sorted(set(old) - set(new)),
            "paths_only_after": sorted(set(new) - set(old)),
            "types_changed": [{"path": path, "before": old[path]["types"], "after": new[path]["types"]}
                              for path in sorted(set(old) & set(new)) if old[path]["types"] != new[path]["types"]],
            "no_longer_in_every_frame": sorted(path for path in set(old) & set(new)
                                               if old[path]["in_every_frame"] and not new[path]["in_every_frame"]),
        }
        if any(entry.values()):
            out[group] = entry
    return out


class Validators:
    def __init__(self, bundle):
        root = {"definitions": bundle.get("definitions", {})}
        self.union = {name: jsonschema.Draft7Validator(dict(root, allOf=[{"$ref": "#/definitions/" + name}]))
                      for name in ("ServerNotification", "ServerRequest")}
        self.root = root

    def check(self, union, frame, method):
        if self.union[union].is_valid(frame):
            return None
        alternative = union_methods(definitions(self.root), union).get(method)
        if alternative is None:
            return [{"message": "method %s is not in %s" % (method, union)}]
        validator = jsonschema.Draft7Validator(dict(self.root, **alternative))
        errors = sorted(validator.iter_errors(frame), key=lambda e: (list(e.absolute_path), e.message))
        if not errors:  # valid against its alternative, so the union's own properties fail
            errors = sorted(self.union[union].iter_errors(frame), key=lambda e: (list(e.absolute_path), e.message))
        return [{"instance_path": "/".join(map(str, error.absolute_path)), "validator": error.validator,
                 "message": error.message[:400]} for error in errors]


def validate(rows, validators):
    counts = {"notifications": {"checked": 0, "valid": 0}, "server_requests": {"checked": 0, "valid": 0}}
    failures = []
    for row, kind, method in classify(rows):
        if row["direction"] != "codex->app" or kind not in ("request", "notification"):
            continue
        union, bucket = ("ServerRequest", "server_requests") if kind == "request" else \
            ("ServerNotification", "notifications")
        counts[bucket]["checked"] += 1
        errors = validators.check(union, row["frame"], method)
        if errors is None:
            counts[bucket]["valid"] += 1
        else:
            failures.append({"generation": row["generation"], "position": row["position"], "method": method,
                             "against": union, "redacted_frame": bool(row.get("redacted")), "errors": errors})
    return {"counts": counts, "failures": failures}


def spawn_items(value):
    found = []
    if isinstance(value, dict):
        if value.get("type") == "collabAgentToolCall":
            found.append(value)
        for inner in value.values():
            found += spawn_items(inner)
    elif isinstance(value, list):
        for inner in value:
            found += spawn_items(inner)
    return found


ST5_METHODS = ["item/commandExecution/requestApproval", "serverRequest/resolved", "thread/resume"]
NV04_METHODS = ["item/completed", "item/started", "thread/items/list", "thread/read", "thread/turns/list",
                "turn/completed"]


def st5_mechanism(record, frozen):
    rows = frame_rows(record)
    first = [row for row in rows if row["generation"] == 1]
    request = next((row for row in first if row["direction"] == "codex->app"
                    and row["frame"].get("method") == ST5_METHODS[0] and "id" in row["frame"]), None)
    answer = None if request is None else next(
        (row for row in first if row["direction"] == "app->codex" and "method" not in row["frame"]
         and row["frame"].get("id") == request["frame"]["id"]), None)
    events = [event.get("event") for event in record.get("events", [])]
    after = [] if answer is None else first[first.index(answer) + 1:]
    resume = next((row for row in rows if row["generation"] == 2 and row["frame"].get("method") == "thread/resume"),
                  None)
    later = [] if resume is None else [row for row in rows[rows.index(resume) + 1:] if row["generation"] == 2
                                       and row["direction"] == "codex->app" and "method" in row["frame"]
                                       and "id" in row["frame"]]
    mechanism = {
        "approval_request_raised": request is not None,
        "answer_written": answer is not None,
        "acknowledged": None if answer is None else any(
            row["direction"] == "codex->app" and row["frame"].get("method") == "serverRequest/resolved"
            for row in after),
        "re_raised_after_resume": None if resume is None else bool(later),
    }
    if frozen:
        mechanism["frozen_before_answer"] = (
            "process-group-frozen" in events and "answer-written" in events
            and events.index("process-group-frozen") < events.index("answer-written"))
    expected = {"approval_request_raised": True, "answer_written": True, "re_raised_after_resume": False}
    if frozen:
        expected.update(acknowledged=False, frozen_before_answer=True)
    return mechanism, expected, {"supplier_frames_after_answer_in_generation_1": sum(
        row["direction"] == "codex->app" for row in after)}


def nv04_mechanism(record):
    rows = frame_rows(record)
    live = [(row, item) for row in rows if row["frame"].get("method") in ("item/started", "item/completed")
            for item in [((row["frame"].get("params") or {}).get("item") or {})]
            if item.get("type") == "collabAgentToolCall"]
    completed = [item for row, item in live if row["frame"]["method"] == "item/completed"]
    parent = completed[0].get("senderThreadId") if completed else None
    child = (completed[0].get("receiverThreadIds") or [None])[0] if completed else None
    order = [(row["frame"].get("params") or {}).get("threadId") for row in rows
             if row["direction"] == "codex->app" and row["frame"].get("method") == "turn/completed"]
    history = []
    for row, kind, method in classify(rows):
        if kind == "reply" and method in ("thread/read", "thread/turns/list", "thread/items/list"):
            history += [item for item in spawn_items(row["frame"].get("result"))
                        if item.get("senderThreadId") == parent]
    mechanism = {
        "spawn_item_carries_prompt": bool(live) and all(isinstance(item.get("prompt"), str) and item["prompt"]
                                                       for row, item in live)
        and len({item["prompt"] for row, item in live}) == 1,
        "parent_turn_completed_before_child": None if not (parent and child and parent in order and child in order)
        else order.index(parent) < order.index(child),
        "history_reads_carry_prompt": None if not history else all(item.get("prompt") for item in history),
    }
    expected = {"spawn_item_carries_prompt": True, "parent_turn_completed_before_child": True}
    return mechanism, expected, {"spawn_items_live": len(live), "spawn_items_in_history_reads": len(history)}


COVERAGE = {
    "st5": ["a supplier server request item/commandExecution/requestApproval with an id in generation 1",
            "the App's answer to that request in generation 1",
            "an App thread/resume request in generation 2",
            "the events process-group-frozen and answer-written",
            "at least one supplier notification to validate"],
    "st5-race": ["a supplier server request item/commandExecution/requestApproval with an id in generation 1",
                 "the App's answer to that request in generation 1",
                 "an App thread/resume request in generation 2",
                 "at least one supplier notification to validate"],
    "nv04": ["a collabAgentToolCall item in an item/started and an item/completed notification",
             "turn/completed notifications for the spawning thread and for the spawned thread",
             "at least one supplier notification to validate"],
}


def coverage_gaps(scenario, record):
    """The COVERAGE requirements of the scenario that the recording does not meet."""
    rows = frame_rows(record)
    supplier = [row for row in rows if row["direction"] == "codex->app"]
    notes = [row for row in supplier if "method" in row["frame"] and "id" not in row["frame"]]
    met = {"at least one supplier notification to validate": bool(notes)}
    if scenario in ("st5", "st5-race"):
        request = next((row for row in supplier if row["generation"] == 1 and "id" in row["frame"]
                        and row["frame"].get("method") == ST5_METHODS[0]), None)
        met[COVERAGE[scenario][0]] = request is not None
        met[COVERAGE[scenario][1]] = request is not None and any(
            row["generation"] == 1 and row["direction"] == "app->codex" and "method" not in row["frame"]
            and row["frame"].get("id") == request["frame"]["id"] for row in rows)
        met[COVERAGE[scenario][2]] = any(row["generation"] == 2 and row["direction"] == "app->codex"
                                         and row["frame"].get("method") == "thread/resume" for row in rows)
        if scenario == "st5":
            events = record.get("events") or []
            names = {event.get("event") for event in events if isinstance(event, dict)}
            met[COVERAGE["st5"][3]] = {"process-group-frozen", "answer-written"} <= names
    else:
        live = {row["frame"]["method"]: ((row["frame"].get("params") or {}).get("item") or {}) for row in notes
                if row["frame"]["method"] in ("item/started", "item/completed")
                and ((row["frame"].get("params") or {}).get("item") or {}).get("type") == "collabAgentToolCall"}
        met[COVERAGE["nv04"][0]] = set(live) == {"item/started", "item/completed"}
        completed = live.get("item/completed") or {}
        threads = {(n["frame"].get("params") or {}).get("threadId") for n in notes
                   if n["frame"]["method"] == "turn/completed"}
        met[COVERAGE["nv04"][1]] = bool(completed.get("senderThreadId") in threads and (
            completed.get("receiverThreadIds") or [None])[0] in threads)
    return [requirement for requirement in COVERAGE[scenario] if not met.get(requirement)]


def mechanism_of(scenario, record):
    if scenario == "nv04":
        return nv04_mechanism(record) + (NV04_METHODS,)
    return st5_mechanism(record, scenario == "st5") + (ST5_METHODS,)


# ---------- comparison ----------
def finding(kind, subject, detail, involves):
    body = {"kind": kind, "subject": subject, "detail": detail}
    return dict(body, id="VA-" + digest(canonical(body).encode())[:12], involves=sorted(set(involves)))


def default_recordings(pin):
    return HERE / "recordings" if pin == "0.160.0" else HERE / "recordings" / pin


def compare(from_pin, to_pin, resources=None, from_resources=None, to_resources=None, from_recordings=None,
            to_recordings=None, from_supplement=None, to_supplement=None, source=None, dispositions=None,
            scenarios=SCENARIOS):
    for pin in (from_pin, to_pin):
        if not isinstance(pin, str) or not PIN.match(pin):
            raise Refused("refused: %r is not a pin of the form major.minor.patch" % (pin,))
    if from_pin == to_pin:
        raise Refused("refused: the two pins are the same")
    resources = Path(resources or APP / "src-tauri/resources/supplier")
    pins = {"from": from_pin, "to": to_pin}
    folders = {"from": Path(from_resources or resources), "to": Path(to_resources or resources)}
    for side, pin in pins.items():
        if not (folders[side] / pin).is_dir():
            raise Refused("refused: unknown pin %s: no folder %s holds its generated schema" % (
                pin, Inputs.label(folders[side] / pin, side + "-resources", folders[side])))
    inputs = Inputs()
    argument = {"from": "from-resources" if from_resources else "resources",
                "to": "to-resources" if to_resources else "resources"}

    # schema
    bundles, defs, manifests, v2_checks = {}, {}, {}, {}
    for side, pin in pins.items():
        folder = folders[side] / pin
        bundles[side] = inputs.json("generated schema bundle at " + pin, folder / BUNDLE, argument[side], folders[side])
        v2 = inputs.json("generated v2 schema bundle at " + pin, folder / V2_BUNDLE, argument[side], folders[side])
        text = inputs.bytes("generator output manifest at " + pin, folder / MANIFEST, argument[side], folders[side])
        if bundles[side] is not None:
            for problem in bundle_problems(bundles[side]):
                inputs.problems.append({"role": "generated schema bundle", "pin": pin, "problem": problem})
            if bundle_problems(bundles[side])[:1] == ["no definitions object"]:
                bundles[side] = None
        defs[side] = definitions(bundles[side] or {})
        try:
            manifests[side] = manifest_elements(text.decode("utf-8")) if text is not None else {}
        except UnicodeDecodeError:
            manifests[side] = {}
            inputs.problems.append({"role": "generator output manifest", "pin": pin, "problem": "not UTF-8 text"})
        if text is not None:
            variants = {variant for element in manifests[side].values() for variant in ("stable", "experimental")
                        if element["in_" + variant]}
            if variants != {"stable", "experimental"}:
                inputs.problems.append({"role": "generator output manifest", "pin": pin,
                                        "problem": "lists no json-schema file in variant(s) %s" % ", ".join(
                                            sorted({"stable", "experimental"} - variants))})
        if bundles[side] is not None and v2 is not None:
            v2_checks[pin] = v2_bundle_differences(defs[side], v2)
            if v2_checks[pin]:
                inputs.problems.append({"role": "generated v2 schema bundle", "pin": pin,
                                        "problem": "differs from the main bundle for %d definitions"
                                                   % len(v2_checks[pin])})
    method_sets = {}
    for union, label in UNIONS.items():
        before, after = union_methods(defs["from"], union), union_methods(defs["to"], union)
        method_sets[label] = {"at_from": sorted(before), "at_to": sorted(after), "count_from": len(before),
                              "count_to": len(after), "added": sorted(set(after) - set(before)),
                              "removed": sorted(set(before) - set(after))}
    root_from = sorted(name for name in defs["from"] if not name.startswith("v2/"))
    root_to = sorted(name for name in defs["to"] if not name.startswith("v2/"))
    changed = {}
    for name in sorted(set(defs["from"]) & set(defs["to"])):
        if defs["from"][name] != defs["to"][name]:
            changed[name] = diff_schema(defs["from"][name], defs["to"][name], name)
    added_defs = sorted(set(defs["to"]) - set(defs["from"]))
    removed_defs = sorted(set(defs["from"]) - set(defs["to"]))

    def namespace_counts(names):
        return {"root": sum(not n.startswith("v2/") for n in names), "v2": sum(n.startswith("v2/") for n in names)}

    standing_changes, standing_added, standing_removed, parts_changed = [], [], [], []
    for element in sorted(set(manifests["from"]) | set(manifests["to"])):
        old, new = manifests["from"].get(element), manifests["to"].get(element)
        if old is None:
            standing_added.append({"element": element, "standing": new["standing"]})
        elif new is None:
            standing_removed.append({"element": element, "standing": old["standing"]})
        elif old["standing"] != new["standing"]:
            standing_changes.append({"element": element, "before": old["standing"], "after": new["standing"]})
        elif old["variants_differ"] != new["variants_differ"]:
            parts_changed.append({"element": element, "before": old["variants_differ"],
                                  "after": new["variants_differ"]})

    # what the App relies on
    names = set()
    for side in pins:
        for union in UNIONS:
            names |= set(union_methods(defs[side], union))
    source = Path(source or APP / "src-tauri/src")
    relied, files_read = relied_methods(source, names, inputs) if source.is_dir() else ({}, 0)
    if not source.is_dir():
        inputs.missing.append({"role": "host source", "path": Inputs.label(source, "source", source),
                               "state": "missing"})
    elif files_read and not relied:
        inputs.problems.append({"role": "host source", "path": Inputs.label(source, "source", source),
                                "problem": "no protocol method of either pin appears in it as a string literal"})
    roots, unmapped = {"from": set(), "to": set()}, []
    for side in pins:
        for union in UNIONS:
            for method, alternative in union_methods(defs[side], union).items():
                if method not in relied:
                    continue
                params = params_of(alternative)
                if params:
                    roots[side].add(params)
                if union in ("ClientRequest", "ServerRequest"):
                    response = response_of(method, alternative, defs[side])
                    if response:
                        roots[side].add(response)
                    else:
                        unmapped.append({"method": method, "pin": pins[side], "params": params})
    relied_defs = closure(roots["from"], defs["from"]) | closure(roots["to"], defs["to"])
    relied_source = {"rule": RULES["relied_on"], "files_read": files_read, "methods": relied,
                     "unmapped_responses": sorted(unmapped, key=canonical),
                     "definitions": sorted(relied_defs)}
    inputs.read.append({"role": "host source (identity of what was derived from it)",
                        "path": Inputs.label(source, "source", source),
                        "sha256": digest(canonical(relied).encode()),
                        "note": "digest of the relied-on method map; file bytes are not pinned so that the "
                                "result changes only when what the App relies on changes"})

    def touches(path):
        union, method = union_method_of(path)
        if union:
            return [method] if method in relied else []
        name = path.split("/")[0] if not path.startswith("v2/") else "/".join(path.split("/")[:2])
        return [name] if name in relied_defs else []

    findings, additive, documentation = [], [], []
    for name, changes in changed.items():
        for item in changes:
            involved = touches(item["path"])
            if not involved:
                continue
            if item["class"] in ("breaking", "unclassified"):
                findings.append(finding("schema change (%s)" % item["class"], item["path"], item["change"], involved))
            elif item["class"] == "additive":
                additive.append(dict(item, involves=involved))
            elif item["class"] == "documentation only":
                documentation.append(dict(item, involves=involved))
    for label, sets in method_sets.items():
        for method in sets["removed"]:
            if method in relied:
                findings.append(finding("method removed", method, label, [method]))
        for method in sets["added"]:
            if method in relied:
                additive.append({"path": method, "class": "additive", "change": "method added to " + label,
                                 "involves": [method]})
    for name in removed_defs:
        if name in relied_defs:
            findings.append(finding("definition removed", name, "absent at the new pin", [name]))
    for entry in standing_changes + standing_removed:
        definition = element_definition(entry["element"])
        if definition in relied_defs or definition in UNIONS:
            findings.append(finding("standing change", entry["element"],
                                    "%s -> %s" % (entry.get("before", entry.get("standing")),
                                                  entry.get("after", "absent")), [definition]))

    # supplement
    supplement = {}
    for side, pin in pins.items():
        path = Path((from_supplement if side == "from" else to_supplement) or folders[side] / pin / SUPPLEMENT)
        given = from_supplement if side == "from" else to_supplement
        entries = inputs.json("supplement at " + pin, path, side + "-supplement" if given else argument[side],
                              path.parent if given else folders[side], required=bool(given))
        if entries is not None and not (isinstance(entries, list) and all(
                isinstance(e, dict) and {"element", "pin", "evidence"} <= set(e) for e in entries)):
            inputs.problems.append({"role": "supplement", "pin": pin,
                                    "problem": "not a list of entries naming element, pin and evidence"})
            entries = None
        supplement[side] = entries or []
    generated_to = set(defs["to"]) | {m for union in UNIONS for m in union_methods(defs["to"], union)}
    supplement_result = {
        "at_from": supplement["from"], "at_to": supplement["to"],
        "in_generated_output_at_to": {e["element"]: e["element"] in generated_to
                                      for e in supplement["from"] + supplement["to"]},
    }
    carried = {e["element"] for e in supplement["to"]}
    for entry in supplement["from"]:
        if entry["element"] not in generated_to and entry["element"] not in carried:
            findings.append(finding("supplement element lost", entry["element"],
                                    "neither generated nor supplemented at the new pin", [entry["element"]]))

    # recorded exchanges
    validators = Validators(bundles["to"]) if bundles["to"] is not None else None
    coverage = []
    recordings, folders_rec = {}, {"from": Path(from_recordings or default_recordings(from_pin)),
                                   "to": Path(to_recordings or default_recordings(to_pin))}
    for scenario in scenarios:
        records = {}
        for side, pin in pins.items():
            given = from_recordings if side == "from" else to_recordings
            record = inputs.json("recording %s at %s" % (scenario, pin),
                                 folders_rec[side] / (scenario + ".recording.json"),
                                 side + "-recordings" if given else "recordings", folders_rec[side])
            problem = None if record is None else recording_problem(record, scenario, pin)
            if problem:
                inputs.problems.append({"role": "recording " + scenario, "pin": pin, "problem": problem})
                record = None
            records[side] = record
        if None in records.values():
            continue
        for side in pins:
            for requirement in coverage_gaps(scenario, records[side]):
                coverage.append({"scenario": scenario, "pin": pins[side], "lacks": requirement})
        rows = {side: frame_rows(records[side]) for side in pins}
        sequences = {side: sequence(rows[side]) for side in pins}
        shape = {side: shapes(rows[side]) for side in pins}
        common = sorted(set(shape["from"]) & set(shape["to"]))
        differences = shape_differences(shape["from"], shape["to"])
        entry = {
            "frames": {pins[side]: len(rows[side]) for side in pins},
            "sequence": {pins[side]: sequences[side] for side in pins},
            "sequence_differences": sequence_differences(sequences["from"], sequences["to"]),
            "shape_groups_compared": common,
            "shape_groups_only_from": sorted(set(shape["from"]) - set(shape["to"])),
            "shape_groups_only_to": sorted(set(shape["to"]) - set(shape["from"])),
            "shape_differences": differences,
        }
        absent = absent_groups(rows["from"], rows["to"], shape["from"], shape["to"])
        entry["groups_absent_at_to"] = absent
        for group, judgement in sorted(absent.items()):
            method = group.split(" ")[-1]
            if judgement["driven"] and method in relied:
                findings.append(finding("recorded group absent although driven", "%s %s" % (scenario, group),
                                        "driven by " + judgement["driven_by"], [method]))
        for group, difference in differences.items():
            method = group.split(" ")[-1]
            if method not in relied:
                continue
            for path in difference["paths_only_before"]:
                findings.append(finding("recorded key path missing", "%s %s" % (scenario, group), path, [method]))
            for change in difference["types_changed"]:
                findings.append(finding("recorded type changed", "%s %s" % (scenario, group),
                                        "%s %s -> %s" % (change["path"], change["before"], change["after"]),
                                        [method]))
            for path in difference["no_longer_in_every_frame"]:
                findings.append(finding("recorded key path no longer in every frame", "%s %s" % (scenario, group),
                                        path, [method]))
        if validators is not None:
            entry["validation_against_to"] = {pins[side]: validate(rows[side], validators) for side in pins}
            for side in pins:
                for failure in entry["validation_against_to"][pins[side]]["failures"]:
                    if failure["method"] in relied:
                        findings.append(finding("failed validation", "%s recorded at %s" % (scenario, pins[side]),
                                                "%s g%s/%s against %s at %s" % (
                                                    failure["method"], failure["generation"], failure["position"],
                                                    failure["against"], to_pin), [failure["method"]]))
        mechanisms = {}
        for side in pins:
            observed, expected, context, involved = mechanism_of(scenario, records[side])
            mechanisms[pins[side]] = {"observed": observed, "context": context}
        entry["mechanism"] = dict(mechanisms, expected=expected, involves=involved)
        relied_involved = [method for method in involved if method in relied]
        before, after = mechanisms[from_pin]["observed"], mechanisms[to_pin]["observed"]
        # A value first observed at the new pin is an observation, not a change; an expected
        # mechanism that does not hold at the new pin is a finding even if it did not hold before.
        for key in sorted(set(after) | set(expected)):
            old, new = before.get(key), after.get(key)
            if old is not None and new is None:
                findings.append(finding("mechanism no longer observable", scenario, key, relied_involved))
            elif old is not None and new != old:
                findings.append(finding("mechanism changed", scenario, "%s %s -> %s" % (key, old, new),
                                        relied_involved))
            elif key in expected and new != expected[key]:
                findings.append(finding("mechanism not as expected at the new pin", scenario,
                                        "%s is %s" % (key, new), relied_involved))
        recordings[scenario] = entry
    findings = [f for f in findings if f["involves"]]

    # dispositions
    path = Path(dispositions or HERE / "version_advance" / ("%s-to-%s.dispositions.json" % (from_pin, to_pin)))
    authored = inputs.json("dispositions", path, "dispositions", path.parent, required=bool(dispositions))
    entries = []
    if authored is not None:
        fields = ("decided_by", "decision", "finding", "where_recorded")
        if isinstance(authored, list) and all(isinstance(e, dict) and set(e) == set(fields) and all(
                isinstance(e[k], str) and e[k].strip() for k in fields) for e in authored):
            entries = authored
        else:
            inputs.problems.append({"role": "dispositions", "path": Inputs.label(path, "dispositions", path.parent),
                                    "problem": "not a list of {finding, decided_by, decision, where_recorded} "
                                               "with every field non-empty"})
    unique = {}
    for item in findings:
        unique[item["id"]] = item
    findings = [unique[key] for key in sorted(unique)]
    disposed = {entry["finding"] for entry in entries}
    undisposed = [item["id"] for item in findings if item["id"] not in disposed]
    unsupported = [{"path": item["path"], "construct": item["change"]}
                   for changes in changed.values() for item in changes if item["class"] == "unsupported"]
    for side in pins:
        for name, node in defs[side].items():
            for ref in sorted(refs_all(node, set())):
                if ref_name(ref) not in defs[side]:
                    unsupported.append({"path": "%s at %s" % (name, pins[side]),
                                        "construct": "reference %s does not name a definition of the bundle" % ref})
    unsupported = sorted({canonical(u): u for u in unsupported}.values(), key=canonical)
    stale = sorted(disposed - set(unique))
    fail_closed = {
        "missing_inputs": sorted(inputs.missing, key=canonical),
        "missing_structure": sorted(inputs.problems, key=canonical),
        "unsupported_constructs": unsupported,
        "insufficient_coverage": sorted(coverage, key=canonical),
        "coverage_required": {scenario: COVERAGE[scenario] for scenario in scenarios},
    }
    reasons = []
    if undisposed:
        reasons.append("%d finding(s) without a disposition" % len(undisposed))
    reasons += ["a disposition names no finding of this comparison: " + item for item in stale]
    reasons += ["missing input: %s %s" % (item["role"], item["path"]) for item in fail_closed["missing_inputs"]]
    reasons += ["missing structure: %s %s: %s" % (item["role"], item.get("pin", item.get("path", "")),
                                                  item["problem"]) for item in fail_closed["missing_structure"]]
    reasons += ["unsupported construct: %s: %s" % (item["path"], item["construct"]) for item in unsupported]
    reasons += ["insufficient coverage: %s at %s lacks %s" % (item["scenario"], item["pin"], item["lacks"])
                for item in fail_closed["insufficient_coverage"]]
    passed = not reasons
    return {
        "format": FORMAT,
        "from": from_pin,
        "to": to_pin,
        "rules": RULES,
        "scenarios": list(scenarios),
        "inputs": {"read": sorted(inputs.read, key=canonical)},
        "unusable": fail_closed,
        "schema": {
            "method_sets": method_sets,
            "definitions": {
                "count_from": namespace_counts(defs["from"]), "count_to": namespace_counts(defs["to"]),
                "root_names_unchanged": root_from == root_to,
                "added": added_defs, "removed": removed_defs,
                "changed": {name: sorted(changes, key=canonical) for name, changes in changed.items()},
                "changed_count": namespace_counts(changed),
            },
            "v2_bundle_differs_from_main_bundle": v2_checks,
            "standing": {"changed": standing_changes, "elements_added": standing_added,
                         "elements_removed": standing_removed, "experimental_parts_changed": parts_changed},
        },
        "supplement": supplement_result,
        "recorded_exchanges": recordings,
        "relied_on": relied_source,
        "findings": findings,
        "not_requiring_decision": {"rule": RULES["additive_rule"],
                                   "additive": sorted(additive, key=canonical),
                                   "documentation_only": sorted(documentation, key=canonical)},
        "verdict": {
            "verdict": "passed" if passed else "returned for decision",
            "undisposed_findings": undisposed,
            "disposed_findings": sorted(i for i in disposed if i in unique),
            "dispositions_naming_no_finding": stale,
            "reasons": reasons,
            "dispositions": sorted(entries, key=canonical),
        },
    }


def render(result):
    return json.dumps(result, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("compare")
    command.add_argument("--from", dest="from_pin", required=True)
    command.add_argument("--to", dest="to_pin", required=True)
    for name in ("resources", "from-resources", "to-resources", "from-recordings", "to-recordings",
                 "from-supplement", "to-supplement", "source", "dispositions"):
        command.add_argument("--" + name)
    command.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        result = compare(args.from_pin, args.to_pin, args.resources, args.from_resources, args.to_resources,
                         args.from_recordings, args.to_recordings, args.from_supplement, args.to_supplement,
                         args.source, args.dispositions)
    except Refused as refusal:
        sys.stderr.write("%s\n" % refusal)
        return 2
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(render(result), encoding="utf-8")
    verdict = result["verdict"]
    print("%s: %d findings, %d undisposed" % (verdict["verdict"], len(result["findings"]),
                                              len(verdict["undisposed_findings"])))
    return 0 if verdict["verdict"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
