#!/usr/bin/env python3
"""Inventory, difference and evidence check for a Codex pin advance (DEL-01-01 REQ-006, VER-006).

It establishes what the App relies on, reports each relied-on definition (and every
definition reached from one by reference) as unchanged or changed with its exact
difference, and checks the recorded exchanges of both pins as evidence. It classifies no
change: every change to what the App relies on is a finding that needs an explicit
disposition naming exactly that change (CLM-003).

The rule it is built from: a result is produced only from inputs each bound to the supplier
identity it claims and each read in full. An input that is not bound, or not read, is
either inadmissible, which prevents passing whatever is disposed, or one of the bindings
the table EXCEPTIONS names for a pin, which the result lists as not checked; it is never
simply absent. A disposition never stands in for evidence.

A pin is a key of intake.py's table PINS, or 0.160.0, the pin whose inputs predate the
records that table rests on. Every input is read from its place in the repository; no
location is an argument. It executes no supplier and no model.

Usage, from `app/`:
  python3 supplier_checks/version_advance.py --from 0.160.0 --to 0.167.0

It writes `supplier_checks/version_advance/<from>-to-<to>.json` and reads the authored
decisions beside it, `<from>-to-<to>.dispositions.json`.

Exit status: 0 passed, 1 returned for decision, 2 refused (a pin outside the table, or
one whose generated schema is not in the repository).

These are operator-run checks on stable inputs. They are built so that an observation that
was not made, that failed or that is incomplete cannot come out as passed. They are not
built to withstand a writer changing the inputs during the run, nor someone with write
access forging a consistent set of records.
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
sys.path.insert(0, str(HERE))
import intake  # noqa: E402

APP = HERE.parent
# Where every input is read from. Tests point these at invented trees; no argument does.
RECORDINGS = HERE / "recordings"
SOURCE = APP / "src-tauri/src"
RESULTS = HERE / "version_advance"
LEGACY = "0.160.0"  # no distribution or generation record was kept for it; see EXCEPTIONS
FORMAT = "chirality.app-v4.version-advance.v3"
GENERATION = "GENERATION.json"
SCENARIOS = ("nv04", "st5")
RECORDING_FORMATS = ("chirality.app-v4.hosting-capture.st5.v1", "chirality.app-v4.supplier-capture.v2")
BUNDLE = "codex_app_server_protocol.schemas.json"
V2_BUNDLE = "codex_app_server_protocol.v2.schemas.json"
MANIFEST = "MANIFEST.sha256"
SUPPLEMENT = "SUPPLEMENT.json"
UNIONS = {"ClientRequest": "client_requests", "ClientNotification": "client_notifications",
          "ServerRequest": "server_requests", "ServerNotification": "server_notifications"}
ID_KEY = re.compile(r"^(?:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|\d+)$")
LONG = 1000  # a differing value whose canonical text is longer is given by digest and length
LOOPBACK = ("127.0.0.1", "::1")

RULES = {
    "identity": "a definition is unchanged exactly when its parsed JSON value written canonically (object keys "
                "sorted, no insignificant whitespace, strings and numbers as Python's json writes them, so 1 and "
                "1.0 differ) is the same text at both pins; nothing is stripped or normalised beyond that; "
                "otherwise it is changed, and its difference is listed path by path (object keys, list indexes; "
                "lists of different length are compared as sequences, each item removed or inserted given "
                "by its index at the pin that has it), each value in full or, when its canonical text "
                "is longer than %d characters, by SHA-256 and length" % LONG,
    "relied_on": "a protocol method is relied on when its exact name appears as a Rust string literal in the "
                 "host source outside files ending _tests.rs and outside modules gated by #[cfg(test)] or "
                 "#[cfg(all(test, ...))]; its root definitions are the params of a relied-on request or "
                 "notification and the response of a relied-on request (<Name>Response for params <Name>Params, "
                 "else the method's segments in PascalCase followed by Response); every definition reachable "
                 "from a root by $ref at either pin is reached and compared like a root",
    "findings": "each needs a disposition: a relied-on or reached definition changed, added or removed; a "
                "relied-on method's member of its method union changed; a relied-on method removed; a standing "
                "change of a relied-on element; a supplement element lost; for a relied-on method, a recorded "
                "group present at the prior pin and absent at the new pin, a shape difference of a recorded "
                "group, or a prior-pin recorded frame that fails validation against the new pin's schema",
    "bound_and_read": "a result is produced only from inputs each bound to the supplier identity it claims and "
                      "each read in full. Per pin: the manifest names the digests of the two compiled bundles; "
                      "the distribution record names the archive of intake.py's table; the generation record "
                      "names the pin, the manifest and the bundles, and the distribution record's entrypoint, "
                      "tree and archive; every recording names the pin (also in its begin event), the pin's "
                      "version label, and the distribution record's entrypoint, archive and tree; the "
                      "recordings of a pin name one binary. A binding that fails, or cannot be made and is "
                      "not in EXCEPTIONS for that pin, is inadmissible; one in EXCEPTIONS is listed under "
                      "identity as not checked with its reason. Host source that cannot be listed or read "
                      "in full is inadmissible",
    "finding_id": "VA- and the first 12 hex digits of the SHA-256 of the canonical JSON of the finding's kind, "
                  "subject and the SHA-256 of its exact old and new content (null where absent), so a "
                  "disposition stops applying when the change is other than the one decided",
    "inadmissible": "never disposable and each prevents passing: a missing or unusable input or one lacking a "
                    "required structure; an identity binding that fails or is not made (bound_and_read); a "
                    "reached definition that is not a valid Draft 7 schema or refers to a definition its "
                    "bundle lacks; a recording whose frames are not in order (generations not descending, "
                    "positions counting from 1 without a gap in each generation and direction); a recording "
                    "lacking a step of its scenario's script in any generation (coverage_required); a new-pin "
                    "recording not of the current format; a current-format recording whose socket_watch is "
                    "absent or does not have samples an integer greater than zero and equal to the sum of "
                    "samples_by_generation, failed_samples exactly zero, samples_by_generation with at least "
                    "one for every generation that has frames and for no other, non_loopback_peers empty and "
                    "loopback_peers only 127.0.0.1 or ::1; a new-pin supplier notification or server request "
                    "that fails validation against the new pin's schema; an expected mechanism not observed "
                    "at the new pin; a supplement entry that does not name its own pin and its evidence; "
                    "two dispositions naming one finding",
    "shape": "per scenario and per supplier notification, server request and reply to a request: the set of "
             "key paths with their JSON value types and whether each path is present in every such frame; "
             "every scalar value is ignored (so identifiers, times, paths and text), as are array lengths, "
             "the order of array items and keys, and object keys that are UUIDs or digit strings (read as <id>)",
    "validation": "jsonschema Draft 7 against the new pin's ServerNotification (supplier frames with a method "
                  "and no id) and ServerRequest (supplier frames with an id and a method); the supplier's "
                  "replies and the App's frames are not validated; formats are not asserted",
    "standing": "read from MANIFEST.sha256 at file level: experimental exactly when the file is in "
                "json-schema/experimental and not json-schema/stable",
    "inputs": "each pin needs a main bundle whose definitions hold the four method unions with members naming "
              "their method and non-empty v2 definitions, a v2 bundle equal to the main bundle's v2 "
              "definitions in both directions (references rewritten to the flat form), a manifest listing "
              "files in both variants, and a recording of every scenario with frames; the host source must "
              "yield at least one relied-on method; an optional file that is absent is read as empty, a path "
              "that exists and cannot be read as a file is unusable",
    "verdict": "passed only when every finding has a disposition naming its identifier, every disposition names "
               "a finding of this comparison and nothing is inadmissible; otherwise returned for decision",
}


class Refused(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def no_repeated_key(pairs):
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("a key is repeated")
    return dict(pairs)


# ---------- inputs ----------
class Inputs:
    """Reads files and keeps the identity of every input, missing or unusable inputs included."""

    def __init__(self):
        self.read, self.missing, self.problems, self.sha256 = [], [], [], {}

    @staticmethod
    def label(path):
        """The path as the repository names it; a path outside it (a test's invented tree) by its last parts."""
        path = Path(os.path.abspath(path))
        try:
            return path.relative_to(APP.parent).as_posix()
        except ValueError:
            return "<outside the repository>/" + "/".join(path.parts[-3:])

    def bytes(self, role, path, required=True):
        label = self.label(path)
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
        self.sha256[str(path)] = digest(data)
        return data

    def json(self, role, path, required=True):
        data = self.bytes(role, path, required)
        if data is None:
            return None
        try:
            return json.loads(data, object_pairs_hook=no_repeated_key)
        except ValueError:
            self.problems.append({"role": role, "path": self.label(path),
                                  "problem": "not JSON, or JSON with a key repeated in one object"})
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
    """(names reached from the roots by $ref, references that name nothing the bundle defines)."""
    seen, dangling, stack = set(), set(), [root for root in roots if root in defs]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        for ref in refs_all(defs[name], set()):
            target = ref_name(ref)
            if target is None or target not in defs:
                dangling.add("%s refers to %s" % (name, ref))
            elif target not in seen:
                stack.append(target)
    return seen, dangling


def schema_problems(names, defs):
    """Reached definitions that are not valid Draft 7 schemas."""
    problems = []
    for name in sorted(names):
        try:
            jsonschema.Draft7Validator.check_schema(defs[name])
        except jsonschema.SchemaError as error:
            problems.append("%s is not a valid schema at /%s" % (name, "/".join(map(str, error.absolute_path))))
    return problems


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
    """({method: [files]}, files read) for the protocol method names found as literals in the host source.

    The source is read in full or the comparison is inadmissible: a folder that cannot be listed
    or a file that cannot be read as UTF-8 is a problem, never a smaller relied-on set.
    """
    found, files, label = {}, [], Inputs.label(source)

    def unlisted(error):
        inputs.problems.append({"role": "host source", "path": label,
                                "problem": "a folder could not be listed (%s)" % type(error).__name__})
    for folder, directories, names_here in os.walk(source, onerror=unlisted, followlinks=False):
        directories.sort()
        files += [Path(folder) / name for name in sorted(names_here)
                  if name.endswith(".rs") and not name.endswith("_tests.rs")]
    if not files:
        inputs.missing.append({"role": "host source", "path": label, "state": "missing"})
    for path in files:
        relative = Path(os.path.relpath(path, source)).as_posix()
        try:
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            inputs.problems.append({"role": "host source", "path": label, "problem": "%s could not be read as "
                                    "UTF-8 text (%s)" % (relative, type(error).__name__)})
            continue
        literals, masked = rust_literals(text)
        excluded = test_module_ranges(masked)
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
    counted, last = {}, 0
    for row in frames:
        generation, position = row["generation"], row["position"]
        if type(generation) is not int or type(position) is not int or generation < 1:
            return "a frame row's generation or position is not a counting number"
        if generation < last:
            return "frames of generation %d come after frames of generation %d" % (generation, last)
        last = generation
        key = (generation, row["direction"])
        if position != counted.get(key, 0) + 1:
            return "generation %d %s positions do not count from 1 without a gap (position %d follows %d)" % (
                generation, row["direction"], position, counted.get(key, 0))
        counted[key] = position
    begin = [event.get("pin") for event in record.get("events") or [] if event.get("event") == "begin"]
    if "pin" in record and any(named != pin for named in begin):
        return "the begin event names another pin"
    return None


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


def st5_mechanism(record):
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
    mechanism["frozen_before_answer"] = (
        "process-group-frozen" in events and "answer-written" in events
        and events.index("process-group-frozen") < events.index("answer-written"))
    expected = {"approval_request_raised": True, "answer_written": True, "re_raised_after_resume": False,
                "acknowledged": False, "frozen_before_answer": True}
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
    prompts = {item.get("prompt") for row, item in live}
    asked = {(row["generation"], canonical(row["frame"]["id"])): row["frame"] for row in rows
             if row["direction"] == "app->codex" and "method" in row["frame"] and "id" in row["frame"]}
    history, parent_reads, child_reads, reads_as_expected = [], 0, 0, True
    for row in rows:
        frame = row["frame"]
        request = asked.get((row["generation"], canonical(frame.get("id")))) if "method" not in frame else None
        if row["direction"] != "codex->app" or request is None or request["method"] not in (
                "thread/read", "thread/turns/list", "thread/items/list"):
            continue
        thread = (request.get("params") or {}).get("threadId")
        items = spawn_items(frame.get("result"))
        history += [item for item in items if item.get("senderThreadId") == parent]
        if thread == parent and parent:
            parent_reads += 1
            reads_as_expected &= (len(items) == 1 and items[0].get("prompt") in prompts and len(prompts) == 1
                                  and bool(items[0].get("prompt")) and items[0].get("senderThreadId") == parent
                                  and items[0].get("receiverThreadIds") == [child])
        elif thread == child and child:
            child_reads += 1
            reads_as_expected &= ((frame.get("result") or {}).get("thread") or {}).get("parentThreadId") == parent
    mechanism = {
        "spawn_item_carries_prompt": bool(live) and all(isinstance(item.get("prompt"), str) and item["prompt"]
                                                       for row, item in live) and len(prompts) == 1,
        "parent_turn_completed_before_child": None if not (parent and child and parent in order and child in order)
        else order.index(parent) < order.index(child),
        "history_reads_carry_prompt": None if not history else all(item.get("prompt") for item in history),
        # The current script reads the parent three ways and the child once, before and after a restart.
        "every_history_read_carries_the_spawn_item_and_the_child_names_its_parent":
            None if not (parent_reads or child_reads) else reads_as_expected and parent_reads == 6
            and child_reads == 2,
    }
    expected = {"spawn_item_carries_prompt": True, "parent_turn_completed_before_child": True}
    if record.get("format") == RECORDING_FORMATS[1]:
        expected["every_history_read_carries_the_spawn_item_and_the_child_names_its_parent"] = True
    return mechanism, expected, {"spawn_items_live": len(live), "spawn_items_in_history_reads": len(history),
                                 "history_reads_of_the_parent": parent_reads, "reads_of_the_child": child_reads}


OLDER, CURRENT = RECORDING_FORMATS
ST5_SCRIPT = [(1, "reply", "initialize"), (1, "sent", "initialized"), (1, "reply", "thread/start"),
              (1, "reply", "turn/start"), (1, "server request", ST5_METHODS[0]), (1, "answer", ST5_METHODS[0]),
              (1, "sent", "thread/turns/list"), (2, "reply", "initialize"), (2, "sent", "initialized"),
              (2, "reply", "thread/read"), (2, "reply", "thread/turns/list"), (2, "reply", "thread/loaded/list"),
              (2, "reply", "thread/resume"), (0, "notification", "any")]
ST5_EVENTS = [(0, "event", "process-group-frozen"), (0, "event", "answer-written")]
NV04_FIRST = [(1, "reply", "initialize"), (1, "sent", "initialized"), (1, "reply", "thread/start"),
              (1, "reply", "turn/start"), (1, "spawn item", "item/started"), (1, "spawn item", "item/completed"),
              (1, "completion", "parent"), (1, "completion", "child"), (1, "reply", "thread/loaded/list"),
              (0, "notification", "any")]


def history(generation):
    return [(generation, "reply", "thread/read parent"), (generation, "reply", "thread/turns/list"),
            (generation, "reply", "thread/items/list"), (generation, "reply", "thread/read child")]


# Every step of each scenario's script that the comparison reads: the script of the harness that made
# the current-format recordings (readable at commit 696f8170), and the 0.160.0 harness's shorter nv04
# script for the older format.
SCRIPTS = {
    (CURRENT, "st5"): ST5_SCRIPT + ST5_EVENTS,
    (CURRENT, "nv04"): NV04_FIRST + history(1) + [(2, "reply", "initialize"), (2, "sent", "initialized")]
    + history(2),
    (OLDER, "st5"): ST5_SCRIPT + ST5_EVENTS, (OLDER, "nv04"): NV04_FIRST,
}


def step_label(step):
    generation, kind, what = step
    where = "generation %d: " % generation if generation else ""
    return where + {"reply": "App request %s with its result", "sent": "App frame %s",
                    "server request": "supplier server request %s", "answer": "App answer to %s",
                    "spawn item": "supplier %s carrying a collabAgentToolCall item",
                    "completion": "supplier turn/completed of the %s thread", "event": "event %s",
                    "notification": "a supplier notification to validate (%s)"}[kind] % what


def coverage_gaps(scenario, record):
    """The steps of SCRIPTS the recording lacks."""
    rows = frame_rows(record)
    completed = [((row["frame"].get("params") or {}).get("item") or {}) for row in rows
                 if row["direction"] == "codex->app" and row["frame"].get("method") == "item/completed"
                 and ((row["frame"].get("params") or {}).get("item") or {}).get("type") == "collabAgentToolCall"]
    threads = {"parent": completed[0].get("senderThreadId") if completed else None,
               "child": (completed[0].get("receiverThreadIds") or [None])[0] if completed else None}
    replies = {(row["generation"], canonical(row["frame"].get("id"))) for row in rows
               if row["direction"] == "codex->app" and "method" not in row["frame"] and "result" in row["frame"]}

    def present(generation, kind, what):
        mine = [row for row in rows if row["generation"] == generation or not generation]
        frame = lambda row: row["frame"]
        if kind == "reply":
            method, _, which = what.partition(" ")
            return any(row["direction"] == "app->codex" and frame(row).get("method") == method and "id" in frame(row)
                       and (not which or (frame(row).get("params") or {}).get("threadId") == threads[which])
                       and (generation, canonical(frame(row)["id"])) in replies for row in mine)
        if kind == "sent":
            return any(row["direction"] == "app->codex" and frame(row).get("method") == what for row in mine)
        if kind in ("server request", "answer"):
            asked = [frame(row)["id"] for row in mine if row["direction"] == "codex->app"
                     and frame(row).get("method") == what and "id" in frame(row)]
            return bool(asked) if kind == "server request" else any(
                row["direction"] == "app->codex" and "method" not in frame(row) and frame(row).get("id") in asked
                for row in mine)
        if kind == "spawn item":
            return any(row["direction"] == "codex->app" and frame(row).get("method") == what
                       and ((frame(row).get("params") or {}).get("item") or {}).get("type") == "collabAgentToolCall"
                       for row in mine)
        if kind == "completion":
            return threads[what] is not None and any(
                row["direction"] == "codex->app" and frame(row).get("method") == "turn/completed"
                and (frame(row).get("params") or {}).get("threadId") == threads[what] for row in mine)
        if kind == "event":
            return any(event.get("event") == what for event in record.get("events") or [])
        return any(row["direction"] == "codex->app" and "method" in frame(row) and "id" not in frame(row)
                   for row in mine)

    return [step_label(step) for step in SCRIPTS[(record["format"], scenario)] if not present(*step)]


def mechanism_of(scenario, record):
    if scenario == "nv04":
        return nv04_mechanism(record) + (NV04_METHODS,)
    return st5_mechanism(record) + (ST5_METHODS,)


# ---------- comparison ----------
def content_sha(value):
    return None if value is None else digest(canonical(value).encode())


def shown(value):
    text = canonical(value)
    return value if len(text) <= LONG else {"sha256": digest(text.encode()), "length": len(text)}


def diff_paths(before, after, path=""):
    """[{path, before, after}] for every place where two JSON values differ (RULES["identity"])."""
    if canonical(before) == canonical(after):
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        out = []
        for key in sorted(set(before) | set(after)):
            where = "%s/%s" % (path, key)
            if key not in after:
                out.append({"path": where, "before": shown(before[key]), "after": "<absent>"})
            elif key not in before:
                out.append({"path": where, "before": "<absent>", "after": shown(after[key])})
            else:
                out += diff_paths(before[key], after[key], where)
        return out
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return [d for index, (old, new) in enumerate(zip(before, after))
                for d in diff_paths(old, new, "%s/%d" % (path, index))]
    if isinstance(before, list) and isinstance(after, list):
        # Compared as sequences, so a reordering is reported: each item removed or inserted, by its
        # index at the pin that has it.
        old_texts, new_texts = [canonical(v) for v in before], [canonical(v) for v in after]
        removed, inserted = [], []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old_texts, new_texts, autojunk=False).get_opcodes():
            if op != "equal":
                removed += [{"path": "%s/%d" % (path, i), "before": shown(before[i]), "after": "<absent>"}
                            for i in range(i1, i2)]
                inserted += [{"path": "%s/%d" % (path, j), "before": "<absent>", "after": shown(after[j])}
                             for j in range(j1, j2)]
        return removed + inserted
    return [{"path": path or "/", "before": shown(before), "after": shown(after)}]


def finding(kind, subject, before, after, detail=""):
    body = {"kind": kind, "subject": subject, "before_sha256": content_sha(before),
            "after_sha256": content_sha(after)}
    result = dict(body, id="VA-" + digest(canonical(body).encode())[:12])
    if detail:
        result["detail"] = detail
    return result


def socket_gaps(record):
    """Why a current-format recording's socket_watch report does not meet RULES["inadmissible"]."""
    watch = record.get("socket_watch")
    if not isinstance(watch, dict):
        return ["a socket_watch report"]
    gaps = []
    samples, failed, by_generation = watch.get("samples"), watch.get("failed_samples"), watch.get(
        "samples_by_generation")
    if not (type(samples) is int and samples > 0):
        gaps.append("socket_watch samples an integer greater than zero")
    if not (type(failed) is int and failed == 0):
        gaps.append("socket_watch failed_samples present and zero")
    generations = sorted({str(row["generation"]) for row in frame_rows(record)})
    if not (isinstance(by_generation, dict) and all(
            type(by_generation.get(g)) is int and by_generation[g] >= 1 for g in generations)):
        gaps.append("socket_watch samples_by_generation of at least one for generation(s) %s" % ", ".join(generations))
    elif sorted(by_generation) != generations or not all(type(v) is int for v in by_generation.values()) \
            or sum(by_generation.values()) != samples:
        gaps.append("socket_watch samples_by_generation naming exactly generation(s) %s and summing to samples"
                    % ", ".join(generations))
    if watch.get("non_loopback_peers") != []:
        gaps.append("socket_watch non_loopback_peers present and empty")
    peers = watch.get("loopback_peers")
    if not (isinstance(peers, list) and all(peer in LOOPBACK for peer in peers)):
        gaps.append("socket_watch loopback_peers only 127.0.0.1 or ::1")
    return gaps


# The recordings are evidence kept as files; the harness that made them is not maintained and its
# refusals are not relied on (see the note beside the recordings).
EVIDENCE_LIMIT = ("the recorded evidence at each pin is established up to each scenario's last required reply "
                  "and no further: what the supplier sent after it is not established by the recordings. The "
                  "schema comparison does not depend on this; the comparison of recorded groups and shapes does. "
                  "The st5-race scenario is not compared: its outcome is a race, not a property of the supplier")


# The bindings a pin's inputs do not make, each with its reason. A binding that fails or cannot be
# made for a pin and is not named here is inadmissible. Adding a row is a reviewed decision.
EXCEPTIONS = {
    (LEGACY, "distribution record to the table's archive"):
        "no distribution record was kept for 0.160.0, so nothing binds its inputs to a release archive",
    (LEGACY, "generation record to the pin, the manifest and the bundles"):
        "no generation record was kept for 0.160.0",
    (LEGACY, "generation record to the distribution record's entrypoint"):
        "no generation or distribution record was kept for 0.160.0",
    (LEGACY, "generation record to the distribution record's tree and archive"):
        "no generation or distribution record was kept for 0.160.0",
    (LEGACY, "recording to the distribution record"):
        "no distribution record was kept for 0.160.0; its recordings' binary digest is compared only among "
        "themselves",
    ("0.167.0", "generation record to the distribution record's tree and archive"):
        "the 0.167.0 generation record was made from the npm platform package, whose tree is not the release "
        "archive's by the record's own statement (canonical_archive_equivalence false); the entrypoint's digest "
        "is bound",
}


def manifest_rows(text):
    return {path.strip(): sha.strip() for sha, _, path in (line.partition("  ") for line in text.splitlines())
            if path.strip()}


def identity(pin, folder, manifest, records, inputs):
    """([{pin, binding, state}], problems) for RULES["bound_and_read"] at one pin."""
    rows, problems = [], []

    def check(binding, holds, scenario=None):
        reason = EXCEPTIONS.get((pin, binding))
        state = "bound" if holds else "not checked: " + reason if reason else "not bound"
        row = {"pin": pin, "binding": binding, "state": state}
        if scenario:
            row["scenario"] = scenario
        rows.append(row)
        if state == "not bound":
            problems.append(dict(row, problem="the binding does not hold or its inputs are not there"))

    listed = manifest_rows(manifest.decode("utf-8", "replace")) if manifest is not None else {}
    bundles = {name: inputs.sha256.get(str(folder / name)) for name in (BUNDLE, V2_BUNDLE)}
    check("manifest to the compiled bundles", all(
        sha and listed.get("json-schema/experimental/" + name) == sha for name, sha in bundles.items()))
    record = None
    if (folder / "CANONICAL_DISTRIBUTION.json").exists():
        inputs.bytes("distribution record at " + pin, folder / "CANONICAL_DISTRIBUTION.json")
        try:
            record = intake.expected_distribution(pin)
        except intake.Refused:
            record = None
    check("distribution record to the table's archive", record is not None)
    entry = {} if record is None else next(
        (e for e in record["inventory"]["entries"] if e["path"] == record["package_metadata"].get("entrypoint")), {})
    generation = inputs.json("generation record at " + pin, folder / GENERATION) \
        if (folder / GENERATION).exists() else None
    supplier = generation.get("supplier") if isinstance(generation, dict) else None
    supplier = supplier if isinstance(supplier, dict) else {}
    check("generation record to the pin, the manifest and the bundles",
          isinstance(generation, dict) and generation.get("pin") == pin and manifest is not None
          and generation.get("manifest_sha256") == digest(manifest)
          and generation.get("compiled_experimental_bundles") == bundles and all(bundles.values()))
    check("generation record to the distribution record's entrypoint",
          bool(entry.get("sha256")) and supplier.get("main_sha256") == entry.get("sha256"))
    check("generation record to the distribution record's tree and archive",
          record is not None and supplier.get("tree_manifest_sha256") == record["inventory"]["manifest_sha256"]
          and supplier.get("archive_sha256") == record["archive"]["sha256"])
    binaries = set()
    for scenario, recording in sorted(records.items()):
        named = recording.get("version_identity")
        named = named if isinstance(named, dict) else {}
        begins = [event.get("pin") for event in recording.get("events") or [] if event.get("event") == "begin"]
        check("recording to the pin and its version label",
              recording_pin(recording) == pin and all(name == pin for name in begins)
              and named.get("version_output") == "codex-cli " + pin, scenario)
        distribution = named.get("distribution")
        distribution = distribution if isinstance(distribution, dict) else {}
        check("recording to the distribution record",
              record is not None and bool(entry.get("sha256")) and named.get("binary_sha256") == entry.get("sha256")
              and distribution.get("archive_sha256") == record["archive"]["sha256"]
              and distribution.get("inventory_manifest_sha256") == record["inventory"]["manifest_sha256"], scenario)
        binaries.add(named.get("binary_sha256") if isinstance(named.get("binary_sha256"), str) else None)
    if records:
        check("recordings to one binary", len(binaries) == 1 and None not in binaries
              and re.fullmatch(r"[0-9a-f]{64}", next(iter(binaries))) is not None)
    return rows, problems


def recordings_folder(pin):
    return RECORDINGS if pin == LEGACY else RECORDINGS / pin


def compare(from_pin, to_pin, scenarios=SCENARIOS):
    known = [LEGACY] + list(intake.PINS)
    for pin in (from_pin, to_pin):
        if not any(pin == name for name in known):
            raise Refused("refused: %r is not a pin of the table (%s)" % (pin, ", ".join(known)))
    if from_pin == to_pin:
        raise Refused("refused: the two pins are the same")
    if to_pin == LEGACY:
        raise Refused("refused: %s is admitted only as the pin advanced from" % LEGACY)
    resources = Path(intake.RESOURCES)
    pins = {"from": from_pin, "to": to_pin}
    for pin in pins.values():
        if not (resources / pin).is_dir():
            raise Refused("refused: unknown pin %s: the repository holds no generated schema for it" % pin)
    inputs = Inputs()
    findings = []
    evidence = {"identity": [], "recording_admission": [], "validation_failures": [], "mechanisms_not_observed": []}

    # generated schema
    bundles, defs, manifests, v2_checks, manifest_bytes = {}, {}, {}, {}, {}
    for side, pin in pins.items():
        folder = resources / pin
        bundles[side] = inputs.json("generated schema bundle at " + pin, folder / BUNDLE)
        v2 = inputs.json("generated v2 schema bundle at " + pin, folder / V2_BUNDLE)
        text = manifest_bytes[side] = inputs.bytes("generator output manifest at " + pin, folder / MANIFEST)
        if bundles[side] is not None:
            problems = bundle_problems(bundles[side])
            for problem in problems:
                inputs.problems.append({"role": "generated schema bundle", "pin": pin, "problem": problem})
            if problems[:1] == ["no definitions object"]:
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
    methods = {side: {union: union_methods(defs[side], union) for union in UNIONS} for side in pins}
    method_sets = {label: {"at_from": sorted(methods["from"][union]), "at_to": sorted(methods["to"][union]),
                           "count_from": len(methods["from"][union]), "count_to": len(methods["to"][union]),
                           "added": sorted(set(methods["to"][union]) - set(methods["from"][union])),
                           "removed": sorted(set(methods["from"][union]) - set(methods["to"][union]))}
                   for union, label in UNIONS.items()}

    # what the App relies on
    names = {method for side in pins for union in UNIONS for method in methods[side][union]}
    source = Path(SOURCE)
    relied, files_read = relied_methods(source, names, inputs) if source.is_dir() else ({}, 0)
    if not source.is_dir():
        inputs.missing.append({"role": "host source", "path": Inputs.label(source), "state": "missing"})
    elif files_read and not relied:
        inputs.problems.append({"role": "host source", "path": Inputs.label(source),
                                "problem": "no protocol method of either pin appears in it as a string literal"})
    roots, unmapped = {"from": set(), "to": set()}, []
    for side in pins:
        for union in UNIONS:
            for method, member in methods[side][union].items():
                if method not in relied:
                    continue
                if params_of(member):
                    roots[side].add(params_of(member))
                if union in ("ClientRequest", "ServerRequest"):
                    response = response_of(method, member, defs[side])
                    if response:
                        roots[side].add(response)
                    else:
                        unmapped.append({"method": method, "pin": pins[side], "params": params_of(member)})
    reached = {}
    for side, pin in pins.items():
        reached[side], dangling = closure(roots[side], defs[side])
        dangling |= {"a relied-on method's params or response names %s" % root for root in roots[side]
                     if root not in defs[side]}
        # A reached definition that refers to nothing, or is not a schema, is unusable input: it is
        # never a finding to dispose.
        for problem in sorted(dangling) + schema_problems(reached[side], defs[side]):
            inputs.problems.append({"role": "generated schema bundle", "pin": pin,
                                    "problem": "reached definition unusable: " + problem})
    relied_defs = reached["from"] | reached["to"]
    root_names = roots["from"] | roots["to"]
    inputs.read.append({"role": "host source (identity of what was derived from it)",
                        "path": Inputs.label(source),
                        "sha256": digest(canonical(relied).encode()),
                        "note": "digest of the relied-on method map; file bytes are not pinned so that the "
                                "result changes only when what the App relies on changes"})

    # definitions: identity and difference
    unchanged, changed = [], {}
    for name in sorted(relied_defs):
        old, new = defs["from"].get(name), defs["to"].get(name)
        if old is not None and new is not None and canonical(old) == canonical(new):
            unchanged.append(name)
            continue
        state = "added" if old is None else "removed" if new is None else "changed"
        changed[name] = {"state": state, "role": "root" if name in root_names else "reached by reference",
                         "before_sha256": content_sha(old), "after_sha256": content_sha(new),
                         "difference": diff_paths(old, new) if state == "changed" else []}
        findings.append(finding("definition " + state, name, old, new))
    members_changed = {}
    for union in UNIONS:
        for method in sorted(relied):
            old, new = methods["from"][union].get(method), methods["to"][union].get(method)
            if old is None and new is None:
                continue
            if new is None:
                findings.append(finding("relied-on method removed", "%s %s" % (union, method), old, None))
            elif old is not None and canonical(old) != canonical(new):
                members_changed["%s %s" % (union, method)] = diff_paths(old, new)
                findings.append(finding("method union member changed", "%s %s" % (union, method), old, new))
    standing_changes = []
    for element in sorted(set(manifests["from"]) & set(manifests["to"])):
        old, new = manifests["from"][element]["standing"], manifests["to"][element]["standing"]
        if old != new:
            standing_changes.append({"element": element, "before": old, "after": new})
            if element_definition(element) in relied_defs:
                findings.append(finding("standing change", element, old, new))

    # supplement
    supplement = {}
    for side, pin in pins.items():
        entries = inputs.json("supplement at " + pin, resources / pin / SUPPLEMENT, required=False)
        if entries is not None and not (isinstance(entries, list) and all(
                isinstance(e, dict) and {"element", "pin", "evidence"} <= set(e)
                and isinstance(e["element"], str) and e["element"].strip() and e["pin"] == pin
                and isinstance(e["evidence"], str) and e["evidence"].strip() for e in entries)):
            inputs.problems.append({"role": "supplement", "pin": pin,
                                    "problem": "not a list of entries each naming its element, this pin and "
                                               "its evidence"})
            entries = None
        supplement[side] = entries or []
    generated_to = set(defs["to"]) | {m for union in UNIONS for m in methods["to"][union]}
    carried = {e["element"] for e in supplement["to"]}
    for entry in supplement["from"]:
        if entry["element"] not in generated_to and entry["element"] not in carried:
            findings.append(finding("supplement element lost", entry["element"], entry, None))

    # recorded exchanges
    validators = Validators(bundles["to"]) if bundles["to"] is not None else None
    limits, recordings, loaded = [EVIDENCE_LIMIT] if scenarios else [], {}, {side: {} for side in pins}
    for scenario in scenarios:
        records = {}
        for side, pin in pins.items():
            record = inputs.json("recording %s at %s" % (scenario, pin),
                                 recordings_folder(pin) / (scenario + ".recording.json"))
            problem = None if record is None else recording_problem(record, scenario, pin)
            if problem:
                inputs.problems.append({"role": "recording " + scenario, "pin": pin, "problem": problem})
                record = None
            records[side] = record
            if record is not None:
                loaded[side][scenario] = record
        if None in records.values():
            continue
        for side, pin in pins.items():
            record = records[side]
            gaps = coverage_gaps(scenario, record)
            if record["format"] == CURRENT:
                gaps += socket_gaps(record)
            elif side == "to":
                gaps.append("the current recording format %s" % CURRENT)
            else:
                limits.append("the %s recording at %s carries no socket observation because its format (%s) did "
                              "not record one; this is a limit of the comparison, not an observation"
                              % (scenario, pin, OLDER))
            evidence["recording_admission"] += [{"scenario": scenario, "pin": pin, "lacks": gap} for gap in gaps]
        rows = {side: frame_rows(records[side]) for side in pins}
        sequences = {side: sequence(rows[side]) for side in pins}
        shape = {side: shapes(rows[side]) for side in pins}
        differences = shape_differences(shape["from"], shape["to"])
        entry = {
            "frames": {pins[side]: len(rows[side]) for side in pins},
            "sequence": {pins[side]: sequences[side] for side in pins},
            "sequence_differences": sequence_differences(sequences["from"], sequences["to"]),
            "shape_groups_only_from": sorted(set(shape["from"]) - set(shape["to"])),
            "shape_groups_only_to": sorted(set(shape["to"]) - set(shape["from"])),
            "shape_differences": differences,
        }
        for group in entry["shape_groups_only_from"]:
            if group.split(" ")[-1] in relied:
                findings.append(finding("recorded group absent at the new pin", "%s %s" % (scenario, group),
                                        shape["from"][group], None))
        for group in differences:
            if group.split(" ")[-1] in relied:
                findings.append(finding("recorded shape changed", "%s %s" % (scenario, group),
                                        shape["from"][group], shape["to"][group]))
        if validators is not None:
            entry["validation_against_to"] = {pins[side]: validate(rows[side], validators) for side in pins}
            for failure in entry["validation_against_to"][from_pin]["failures"]:
                if failure["method"] in relied:
                    findings.append(finding("prior-pin frame fails the new schema", "%s %s g%s/%s" % (
                        scenario, failure["method"], failure["generation"], failure["position"]),
                        failure["errors"], None))
            evidence["validation_failures"] += [dict(failure, scenario=scenario) for failure in
                                                entry["validation_against_to"][to_pin]["failures"]]
        mechanisms = {}
        for side in pins:
            observed, expected, context, involved = mechanism_of(scenario, records[side])
            mechanisms[pins[side]] = {"observed": observed, "context": context}
        entry["mechanism"] = dict(mechanisms, expected=expected, involves=involved)
        evidence["mechanisms_not_observed"] += [
            {"scenario": scenario, "mechanism": key, "expected": value,
             "observed": mechanisms[to_pin]["observed"].get(key)}
            for key, value in sorted(expected.items()) if mechanisms[to_pin]["observed"].get(key) != value]
        recordings[scenario] = entry

    # identity: every input bound to the supplier identity it claims
    bindings = []
    for side, pin in pins.items():
        rows, problems = identity(pin, resources / pin, manifest_bytes[side], loaded[side], inputs)
        bindings += rows
        evidence["identity"] += problems
        limits += ["%s%s at %s: %s" % (row["binding"], " (%s)" % row["scenario"] if "scenario" in row else "",
                                       pin, row["state"]) for row in rows if row["state"].startswith("not checked")]

    # dispositions
    path = RESULTS / ("%s-to-%s.dispositions.json" % (from_pin, to_pin))
    authored = inputs.json("dispositions", path, required=False)
    entries, fields = [], ("decided_by", "decision", "finding", "where_recorded")
    if authored is not None:
        if isinstance(authored, list) and all(
                isinstance(e, dict) and set(fields) <= set(e) <= set(fields) | {"group"}
                and all(isinstance(v, str) and v.strip() for v in e.values()) for e in authored):
            entries = authored
            named = [e["finding"] for e in entries]
            for repeated in sorted({name for name in named if named.count(name) > 1}):
                inputs.problems.append({"role": "dispositions", "path": Inputs.label(path),
                                        "problem": "two dispositions name the finding " + repeated})
        else:
            inputs.problems.append({"role": "dispositions", "path": Inputs.label(path),
                                    "problem": "not a list of {finding, decided_by, decision, where_recorded"
                                               "[, group]} with every field a non-empty string"})
    unique = {item["id"]: item for item in findings}
    findings = [unique[key] for key in sorted(unique)]
    disposed = {entry["finding"] for entry in entries}
    undisposed = [item["id"] for item in findings if item["id"] not in disposed]
    stale = sorted(disposed - set(unique))
    inadmissible = {"missing_inputs": sorted(inputs.missing, key=canonical),
                    "missing_structure": sorted(inputs.problems, key=canonical)}
    inadmissible.update({key: sorted(value, key=canonical) for key, value in evidence.items()})
    reasons = ["%d finding(s) without a disposition" % len(undisposed)] if undisposed else []
    reasons += ["a disposition names no finding of this comparison: " + item for item in stale]
    reasons += ["%s: %s" % (key.replace("_", " "), canonical(item)) for key, items in sorted(inadmissible.items())
                for item in items]
    inadmissible["coverage_required"] = {"%s %s" % (scenario, fmt): [step_label(step) for step in steps]
                                         for (fmt, scenario), steps in sorted(SCRIPTS.items())
                                         if scenario in scenarios}

    def namespace_counts(names):
        return {"root": sum(not n.startswith("v2/") for n in names), "v2": sum(n.startswith("v2/") for n in names)}

    common = set(defs["from"]) & set(defs["to"])
    return {
        "format": FORMAT,
        "from": from_pin,
        "to": to_pin,
        "rules": RULES,
        "scenarios": list(scenarios),
        "limits": limits,
        "identity": {"bindings": bindings,
                     "exceptions": {"%s: %s" % key: reason for key, reason in sorted(EXCEPTIONS.items())
                                    if key[0] in pins.values()}},
        "inputs": {"read": sorted(inputs.read, key=canonical)},
        "inadmissible": inadmissible,
        "schema": {
            "method_sets": method_sets,
            "all_definitions": {
                "count_from": namespace_counts(defs["from"]), "count_to": namespace_counts(defs["to"]),
                "added": sorted(set(defs["to"]) - set(defs["from"])),
                "removed": sorted(set(defs["from"]) - set(defs["to"])),
                "changed_count": namespace_counts([n for n in common
                                                   if canonical(defs["from"][n]) != canonical(defs["to"][n])]),
            },
            "relied_on_and_reached": {"unchanged": unchanged, "changed": changed},
            "relied_on_method_members_changed": members_changed,
            "v2_bundle_differs_from_main_bundle": v2_checks,
            "standing_changed": standing_changes,
        },
        "supplement": {"at_from": supplement["from"], "at_to": supplement["to"]},
        "recorded_exchanges": recordings,
        "relied_on": {"files_read": files_read, "methods": relied, "roots": sorted(root_names),
                      "unmapped_responses": sorted(unmapped, key=canonical)},
        "findings": findings,
        "verdict": {
            "verdict": "returned for decision" if reasons else "passed",
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
    known = [LEGACY] + list(intake.PINS)
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="from_pin", required=True, choices=known)
    parser.add_argument("--to", dest="to_pin", required=True, choices=known)
    args = parser.parse_args(argv)
    try:
        result = compare(args.from_pin, args.to_pin)
    except Refused as refusal:
        sys.stderr.write("%s\n" % refusal)
        return 2
    out = RESULTS / ("%s-to-%s.json" % (args.from_pin, args.to_pin))
    out.write_text(render(result), encoding="utf-8")
    verdict = result["verdict"]
    print("%s: %d findings, %d undisposed, %d reasons" % (verdict["verdict"], len(result["findings"]),
                                                          len(verdict["undisposed_findings"]),
                                                          len(verdict["reasons"])))
    return 0 if verdict["verdict"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
