#!/usr/bin/env python3
"""Inventory, difference and evidence check for a Codex pin advance (DEL-01-01 REQ-006, VER-006).

It establishes what the App relies on, reports each relied-on definition (and every
definition reached from one by reference) as unchanged or changed with its exact
difference, and checks the recorded exchanges of both pins as evidence. It classifies no
change: every change to what the App relies on is a finding that needs an explicit
disposition naming exactly that change (CLM-003). It passes only when every finding is
disposed, no disposition names a finding that does not exist, and every evidence
requirement is met; a disposition never stands in for evidence. It executes no supplier and
no model and reads only the files named by its arguments.

Usage, from `app/`:
  python3 supplier_checks/version_advance.py compare --from 0.160.0 --to 0.167.0 \\
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
FORMAT = "chirality.app-v4.version-advance.v2"
SCENARIOS = ("nv04", "st5", "st5-race")
RECORDING_FORMATS = ("chirality.app-v4.hosting-capture.st5.v1", "chirality.app-v4.supplier-capture.v2")
BUNDLE = "codex_app_server_protocol.schemas.json"
V2_BUNDLE = "codex_app_server_protocol.v2.schemas.json"
MANIFEST = "MANIFEST.sha256"
SUPPLEMENT = "SUPPLEMENT.json"
UNIONS = {"ClientRequest": "client_requests", "ClientNotification": "client_notifications",
          "ServerRequest": "server_requests", "ServerNotification": "server_notifications"}
PIN = re.compile(r"^\d+\.\d+\.\d+$")
ID_KEY = re.compile(r"^(?:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|\d+)$")
LONG = 1000  # a differing value whose canonical text is longer is given by digest and length
LOOPBACK = ("127.0.0.1", "::1")

RULES = {
    "identity": "a definition is unchanged exactly when its parsed JSON value written canonically (object keys "
                "sorted, no insignificant whitespace, strings and numbers as Python's json writes them, so 1 and "
                "1.0 differ) is the same text at both pins; nothing is stripped or normalised beyond that; "
                "otherwise it is changed, and its difference is listed path by path (object keys, list indexes; "
                "a list of different length is one difference), each value in full or, when its canonical text "
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
    "finding_id": "VA- and the first 12 hex digits of the SHA-256 of the canonical JSON of the finding's kind, "
                  "subject and the SHA-256 of its exact old and new content (null where absent), so a "
                  "disposition stops applying when the change is other than the one decided",
    "inadmissible": "never disposable and each prevents passing: a missing or unusable input or one lacking a "
                    "required structure; a recording lacking a step of its scenario's script in any generation "
                    "(coverage_required); a new-pin recording not of the current format; a current-format "
                    "recording whose socket_watch is absent or does not have samples an integer greater than "
                    "zero, failed_samples exactly zero, samples_by_generation with at least one for every "
                    "generation that has frames, non_loopback_peers empty and loopback_peers only 127.0.0.1 or "
                    "::1; a new-pin supplier notification or server request that fails validation against the "
                    "new pin's schema; an expected mechanism not observed at the new pin",
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


# Every step of each scenario's script (capture.py for the current format; the 0.160.0 harness's
# shorter nv04 script for the older one) that the comparison reads.
SCRIPTS = {
    (CURRENT, "st5"): ST5_SCRIPT + ST5_EVENTS, (CURRENT, "st5-race"): ST5_SCRIPT,
    (CURRENT, "nv04"): NV04_FIRST + history(1) + [(2, "reply", "initialize"), (2, "sent", "initialized")]
    + history(2),
    (OLDER, "st5"): ST5_SCRIPT + ST5_EVENTS, (OLDER, "st5-race"): ST5_SCRIPT, (OLDER, "nv04"): NV04_FIRST,
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
    return st5_mechanism(record, scenario == "st5") + (ST5_METHODS,)


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
        old_texts, new_texts = [canonical(v) for v in before], [canonical(v) for v in after]
        out = [{"path": "%s/%d" % (path, i), "before": shown(v), "after": "<absent>"}
               for i, v in enumerate(before) if old_texts[i] not in new_texts]
        out += [{"path": "%s/%d" % (path, i), "before": "<absent>", "after": shown(v)}
                for i, v in enumerate(after) if new_texts[i] not in old_texts]
        if out:  # items only at one pin, by index at that pin
            return out
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
    if watch.get("non_loopback_peers") != []:
        gaps.append("socket_watch non_loopback_peers present and empty")
    peers = watch.get("loopback_peers")
    if not (isinstance(peers, list) and all(peer in LOOPBACK for peer in peers)):
        gaps.append("socket_watch loopback_peers only 127.0.0.1 or ::1")
    return gaps


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
    findings, evidence = [], {"recording_admission": [], "validation_failures": [], "mechanisms_not_observed": []}

    # generated schema
    bundles, defs, manifests, v2_checks = {}, {}, {}, {}
    for side, pin in pins.items():
        folder = folders[side] / pin
        bundles[side] = inputs.json("generated schema bundle at " + pin, folder / BUNDLE, argument[side], folders[side])
        v2 = inputs.json("generated v2 schema bundle at " + pin, folder / V2_BUNDLE, argument[side], folders[side])
        text = inputs.bytes("generator output manifest at " + pin, folder / MANIFEST, argument[side], folders[side])
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
    reached = {side: closure(roots[side], defs[side]) for side in pins}
    relied_defs = reached["from"] | reached["to"]
    root_names = roots["from"] | roots["to"]
    inputs.read.append({"role": "host source (identity of what was derived from it)",
                        "path": Inputs.label(source, "source", source),
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
        given = from_supplement if side == "from" else to_supplement
        path = Path(given or folders[side] / pin / SUPPLEMENT)
        entries = inputs.json("supplement at " + pin, path, side + "-supplement" if given else argument[side],
                              path.parent if given else folders[side], required=bool(given))
        if entries is not None and not (isinstance(entries, list) and all(
                isinstance(e, dict) and {"element", "pin", "evidence"} <= set(e) for e in entries)):
            inputs.problems.append({"role": "supplement", "pin": pin,
                                    "problem": "not a list of entries naming element, pin and evidence"})
            entries = None
        supplement[side] = entries or []
    generated_to = set(defs["to"]) | {m for union in UNIONS for m in methods["to"][union]}
    carried = {e["element"] for e in supplement["to"]}
    for entry in supplement["from"]:
        if entry["element"] not in generated_to and entry["element"] not in carried:
            findings.append(finding("supplement element lost", entry["element"], entry, None))

    # recorded exchanges
    validators = Validators(bundles["to"]) if bundles["to"] is not None else None
    limits, recordings = [], {}
    folders_rec = {"from": Path(from_recordings or default_recordings(from_pin)),
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

    # dispositions
    path = Path(dispositions or HERE / "version_advance" / ("%s-to-%s.dispositions.json" % (from_pin, to_pin)))
    authored = inputs.json("dispositions", path, "dispositions", path.parent, required=bool(dispositions))
    entries, fields = [], ("decided_by", "decision", "finding", "where_recorded")
    if authored is not None:
        if isinstance(authored, list) and all(
                isinstance(e, dict) and set(fields) <= set(e) <= set(fields) | {"group"}
                and all(isinstance(v, str) and v.strip() for v in e.values()) for e in authored):
            entries = authored
        else:
            inputs.problems.append({"role": "dispositions", "path": Inputs.label(path, "dispositions", path.parent),
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
    print("%s: %d findings, %d undisposed, %d reasons" % (verdict["verdict"], len(result["findings"]),
                                                          len(verdict["undisposed_findings"]),
                                                          len(verdict["reasons"])))
    return 0 if verdict["verdict"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
