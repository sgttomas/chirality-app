#!/usr/bin/env python3
"""wdproto.py - design prototype for DEL-02-01 WD-v0.8 (declared-part carriage).

NOT PRODUCT CODE. A design aid (R12-3): it renders and parses workflow
packages in the PROPOSED carriage of WD §3.5, validates the declared part
against workflow-declaration.schema.json with a small JSON Schema subset
validator, and reads it in the order of WD §3.7. Python 3 standard library
only; no network; writes only under a temporary directory.

Usage:
  python3 wdproto.py selftest            run every designed check; exit 1 on a mismatch
  python3 wdproto.py read <package-dir>  print the reading of one package as JSON
  python3 wdproto.py render <decl.json> <prose.md> <out-dir>

JSON Schema subset implemented (draft 2020-12 keywords): type, enum, const,
pattern, minLength, maxLength, minItems, uniqueItems, required, properties,
additionalProperties (boolean false only), items, $ref (local "#/$defs/..."),
allOf, anyOf, not, if/then. Annotation keywords ($schema, $id, title,
description) are ignored. Any other keyword makes the validator stop with an
error, so the subset is enforced rather than assumed.
"""
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
SCHEMA_PATH = os.path.join(DESIGN, "workflow-declaration.schema.json")
VALID_EXAMPLE = os.path.join(DESIGN, "workflow-declaration.valid.example.json")
INVALID_EXAMPLE = os.path.join(DESIGN, "workflow-declaration.invalid.example.json")
EXAMPLES_MD = os.path.join(DESIGN, "EXAMPLES.md")
FIX = os.path.join(HERE, "fixtures")
REPO = os.path.abspath(os.path.join(DESIGN, *([".."] * 7)))

KNOWN_CONTRACT_VERSIONS = {"WD-v0.8"}
INFO_STRING = "workflow-declaration"
CATEGORIES = ["expected_inputs", "required_tools", "checkpoints", "returned_outputs", "returned_evidence"]
CAT_DEF = {"expected_inputs": "expected_input", "required_tools": "required_tool", "checkpoints": "checkpoint",
           "returned_outputs": "returned_output", "returned_evidence": "returned_evidence"}
RECOGNIZED_ACT = re.compile(r"^A(1[0-5]|[1-9])$")  # A1..A15 (A15 per R12-5, PROPOSED in ACT)
FORBIDDEN_STANDING = re.compile(r"\b(approved|certified|sealed|code-compliant)\b", re.I)

# ---------------------------------------------------------------- validator
SUPPORTED = {"type", "enum", "const", "pattern", "minLength", "maxLength", "minItems", "uniqueItems", "required",
             "properties", "additionalProperties", "items", "$ref", "allOf", "anyOf", "not", "if", "then",
             "$schema", "$id", "title", "description", "$defs", "default"}
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool}


def _type_ok(v, t):
    if t == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "null":
        return v is None
    if t == "boolean":
        return isinstance(v, bool)
    return isinstance(v, TYPES[t]) and not (t != "boolean" and isinstance(v, bool))


def validate(schema, inst, root=None, path=""):
    """Return a list of (path, keyword, detail). Empty list: valid."""
    root = root if root is not None else schema
    errs = []
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise ValueError("unsupported schema keyword(s) %s at %s" % (sorted(unknown), path or "/"))
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise ValueError("non-local $ref " + ref)
        target = root
        for part in ref[2:].split("/"):
            target = target[part]
        errs += validate(target, inst, root, path)
    if "type" in schema:
        ts = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(inst, t) for t in ts):
            return errs + [(path, "type", "expected %s" % "/".join(ts))]
    if "enum" in schema and inst not in schema["enum"]:
        errs.append((path, "enum", "value %r not in %s" % (inst, schema["enum"])))
    if "const" in schema and inst != schema["const"]:
        errs.append((path, "const", "value %r is not %r" % (inst, schema["const"])))
    if isinstance(inst, str):
        if "minLength" in schema and len(inst) < schema["minLength"]:
            errs.append((path, "minLength", "shorter than %d" % schema["minLength"]))
        if "maxLength" in schema and len(inst) > schema["maxLength"]:
            errs.append((path, "maxLength", "longer than %d" % schema["maxLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], inst):
            errs.append((path, "pattern", "%r does not match %s" % (inst, schema["pattern"])))
    if isinstance(inst, list):
        if "minItems" in schema and len(inst) < schema["minItems"]:
            errs.append((path, "minItems", "fewer than %d items" % schema["minItems"]))
        if schema.get("uniqueItems"):
            seen = [json.dumps(x, sort_keys=True) for x in inst]
            if len(seen) != len(set(seen)):
                errs.append((path, "uniqueItems", "duplicate items"))
        if "items" in schema:
            for i, x in enumerate(inst):
                errs += validate(schema["items"], x, root, "%s/%d" % (path, i))
    if isinstance(inst, dict):
        for r in schema.get("required", []):
            if r not in inst:
                errs.append((path, "required", r))
        props = schema.get("properties", {})
        for k, v in inst.items():
            if k in props:
                errs += validate(props[k], v, root, "%s/%s" % (path, k))
            elif schema.get("additionalProperties") is False:
                errs.append(("%s/%s" % (path, k), "additionalProperties", "unrecognized element %r" % k))
    for sub in schema.get("allOf", []):
        errs += validate(sub, inst, root, path)
    if "anyOf" in schema:
        if not any(not validate(s, inst, root, path) for s in schema["anyOf"]):
            errs.append((path, "anyOf", "no alternative matches"))
    if "not" in schema and not validate(schema["not"], inst, root, path):
        errs.append((path, "not", "matches a forbidden form"))
    if "if" in schema and not validate(schema["if"], inst, root, path):
        errs += validate(schema.get("then", {}), inst, root, path)
    return errs


# ---------------------------------------------------------------- carriage
FENCE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")


def split_front_matter(text):
    """Return (front_matter_dict or None, body_start_line_index, lines)."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if not lines or lines[0] != "---":
        return None, 0, lines
    fm, key = {}, None
    for i in range(1, len(lines)):
        ln = lines[i]
        if ln == "---":
            return fm, i + 1, lines
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", ln)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip()
        elif key and ln.startswith((" ", "\t")):
            fm[key] = (fm[key] + " " + ln.strip()).strip()
    return None, 0, lines  # unterminated front matter: treated as none


def extract(text):
    """WD §3.5 CR-1..CR-6. Returns dict(status, blocks, block_text, front_matter)."""
    fm, start, lines = split_front_matter(text)
    blocks, i, n = [], start, len(lines)
    while i < n:
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        fence, info = m.group(2), m.group(3).strip()
        if fence[0] == "`" and "`" in info:
            i += 1
            continue  # not a fence opener (CommonMark)
        j = i + 1
        close = re.compile(r"^ {0,3}" + re.escape(fence[0]) + "{%d,}\\s*$" % len(fence))
        while j < n and not close.match(lines[j]):
            j += 1
        if info == INFO_STRING:
            blocks.append("\n".join(lines[i + 1:j]))
        i = j + 1
    if not blocks:
        return {"status": "absent", "blocks": 0, "block_text": None, "front_matter": fm}
    if len(blocks) > 1:
        return {"status": "more_than_one_block", "blocks": len(blocks), "block_text": None, "front_matter": fm}
    return {"status": "found", "blocks": 1, "block_text": blocks[0], "front_matter": fm}


def pretty(v, ind=0, width=100):
    """Readable JSON layout: scalars and short flat values inline, the rest one member per line.
    Layout is free under WD §3.5 (any JSON text is read the same); this is the prototype's choice."""
    flat = json.dumps(v, ensure_ascii=False, separators=(", ", ": "))
    nested = isinstance(v, (dict, list)) and any(isinstance(x, (dict, list)) and x for x in (v.values() if isinstance(v, dict) else v))
    if not isinstance(v, (dict, list)) or (len(flat) + ind <= width and not (isinstance(v, dict) and nested and len(v) > 2)):
        return flat
    pad, sub = " " * ind, " " * (ind + 2)
    if isinstance(v, list):
        return "[\n" + ",\n".join(sub + pretty(x, ind + 2, width) for x in v) + "\n" + pad + "]"
    return "{\n" + ",\n".join(sub + json.dumps(k, ensure_ascii=False) + ": " + pretty(x, ind + 2, width - len(k) - 4)
                              for k, x in v.items()) + "\n" + pad + "}"


def render(declaration, prose):
    """Render WORKFLOW.md: the prose (front matter included) followed by the fenced declared part."""
    body = pretty(declaration)
    if not prose.endswith("\n"):
        prose += "\n"
    return prose + "```" + INFO_STRING + "\n" + body + "\n```\n"


def headings(text):
    _, start, lines = split_front_matter(text)
    out, infence, fence = set(), False, None
    for ln in lines[start:]:
        m = FENCE.match(ln)
        if m and not infence:
            infence, fence = True, m.group(2)
            continue
        if infence:
            if re.match(r"^ {0,3}" + re.escape(fence[0]) + "{%d,}\\s*$" % len(fence), ln):
                infence = False
            continue
        h = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", ln)
        if h:
            out.add(h.group(1))
    return out


# ---------------------------------------------------------------- parse
class DuplicateKey(Exception):
    pass


def _no_dupes(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise DuplicateKey(k)
        d[k] = v
    return d


def parse_block(block_text):
    try:
        return json.loads(block_text, object_pairs_hook=_no_dupes), None
    except DuplicateKey as e:
        return None, "duplicate JSON key %r" % str(e)
    except ValueError as e:
        return None, "not JSON: %s" % e


# ---------------------------------------------------------------- reading (WD §3.7)
def _classify_checkpoint_errors(errs, el):
    """VO-5 for one checkpoint. Returns (reading, fb, findings, governed_status, fresh_status, held_note)."""
    findings, reading, fb = [], "recognized", None
    governed_bad = any(p.endswith("/governed") for p, k, d in errs)
    fresh_bad = any(p.endswith("/fresh_act_required") for p, k, d in errs)
    held = [e for e in errs if "/held_actions" in e[0]]
    rest = [e for e in errs if not (e[0].endswith("/governed") or e[0].endswith("/fresh_act_required") or "/held_actions" in e[0])]

    def first(r, f, why):
        nonlocal reading, fb
        findings.append("%s: %s" % (f or r, why))
        if reading == "recognized":
            reading, fb = r, f
    for p, k, d in rest:
        if p.endswith("/name") or (k == "required" and d == "name"):
            first("not_established", "FB-02", "checkpoint name missing or ill-formed")
    for p, k, d in rest:
        if p.endswith("/required_act") or (k == "required" and d == "required_act"):
            val = el.get("required_act") if isinstance(el, dict) else None
            recognized = k == "required" or (isinstance(val, str) and RECOGNIZED_ACT.match(val))
            first("invalid" if recognized else "not_established", "FB-03" if recognized else "FB-04", "required act: " + d)
    for p, k, d in rest:
        if k == "required" and d == "reached_when":
            first("invalid", "FB-13", "reached-when absent")
    for p, k, d in rest:
        if p.endswith("/required_act") or (k == "required" and d in ("name", "required_act", "reached_when")):
            continue
        if k in ("enum", "additionalProperties", "const"):
            first("not_established", "§3.4", "unrecognized element or value at %s: %s" % (p, d))
        else:
            first("not_established", "FB-02", "malformed at %s: %s %s" % (p, k, d))
    gov = "not_established (FB-19)" if governed_bad else None
    fresh = "not_established (FB-19)" if fresh_bad else None
    if governed_bad:
        findings.append("FB-19: governed value unrecognized; preserved; governance not established")
    if fresh_bad:
        findings.append("FB-19: fresh act required value unrecognized; preserved; not established")
    held_note = None
    if held:
        held_note = "malformed; governance phase: conservative default (R10-10)"
        findings.append("held actions malformed: governance-phase conservative default (R10-10); no failure row")
    return reading, fb, findings, gov, fresh, held_note


def read_declaration(decl_text, schema, prose_text="", execution_json=None):
    """Read one declared part (WD §3.7 VO-1..VO-10). Returns a reading dict."""
    R = {"declared_part": None, "findings": [], "categories": {}, "elements": {}, "compatible_roles": None,
         "tool_restriction": None, "unrecognized_top_level": []}
    if execution_json is not None:
        R["root_execution_json"] = {"compatible_roles": execution_json.get("compatible_roles"),
                                    "restriction": (execution_json.get("tools") or {}).get("capabilities")}
        R["tool_restriction"] = R["root_execution_json"]["restriction"]
    if decl_text is None:
        R["declared_part"] = "undeclared"
        for c in CATEGORIES:
            R["categories"][c] = "undeclared"
        if execution_json is not None:
            R["compatible_roles"] = execution_json.get("compatible_roles")
            R["findings"].append("FB-05: required tools undeclared; Root restriction retained as a ceiling, never read as requirements")
        return R
    doc, err = parse_block(decl_text)                                        # VO-2
    if err:
        R["declared_part"] = "not_established (FB-02)"
        R["findings"].append("FB-02: " + err)
        return R
    if not isinstance(doc, dict) or not isinstance(doc.get("declaration_contract_version"), str):
        R["declared_part"] = "not_established (FB-02)"
        R["findings"].append("FB-02: envelope is not an object with a contract version")
        return R
    ver = doc["declaration_contract_version"]                               # VO-3
    if ver not in KNOWN_CONTRACT_VERSIONS:
        R["declared_part"] = "not_established (§3.4 contract version %s not known; preserved)" % ver
        R["findings"].append("§3.4: contract version %s preserved and reported" % ver)
        return R
    R["declared_part"] = "declared"
    top = schema["properties"]
    for k in doc:                                                            # VO-4
        if k not in top:
            R["unrecognized_top_level"].append(k)
            R["findings"].append("§3.4: unrecognized top-level element %r preserved and reported" % k)
    idx = {}
    for c in CATEGORIES:                                                     # VO-4, VO-5
        if c not in doc:
            R["categories"][c] = "undeclared"
            continue
        v = doc[c]
        if not isinstance(v, list):
            R["categories"][c] = "not_established (FB-02)"
            R["findings"].append("FB-02: category %s is not a list" % c)
            continue
        R["categories"][c] = "declared_empty" if not v else "declared"
        els = []
        for i, el in enumerate(v):
            errs = validate({"$ref": "#/$defs/" + CAT_DEF[c]}, el, schema, "/%s/%d" % (c, i))
            name = el.get("name") if isinstance(el, dict) and isinstance(el.get("name"), str) else None
            e = {"name": name, "reading": "recognized", "fb": None, "findings": []}
            if c == "checkpoints":
                r, fb, f, gov, fresh, held = _classify_checkpoint_errors(errs, el)
                e.update(reading=r, fb=fb, findings=f)
                e["governed"] = gov or ("yes" if isinstance(el, dict) and el.get("governed") == "yes" else "absent")
                e["fresh_act_required"] = fresh or ("yes" if isinstance(el, dict) and el.get("fresh_act_required") == "yes" else "absent")
                if held:
                    e["held_actions"] = held
            elif errs:
                unrec = [x for x in errs if x[1] in ("enum", "additionalProperties", "const")]
                e["reading"], e["fb"] = "not_established", ("§3.4" if unrec and len(unrec) == len(errs) else "FB-02")
                e["findings"] = ["%s %s %s" % x for x in errs]
            e["_el"] = el
            els.append(e)
        # VO-6 duplicate names (DN-1..DN-3)
        counts = {}
        for e in els:
            if e["name"]:
                counts[e["name"]] = counts.get(e["name"], 0) + 1
        for e in els:
            if e["name"] and counts[e["name"]] > 1:
                e["findings"].append("FB-20: duplicate name %r in %s" % (e["name"], c))
                if e["reading"] == "recognized":
                    e["reading"], e["fb"] = ("invalid" if c == "checkpoints" else "not_established"), "FB-20"
        if c == "returned_outputs":  # DN-4: designating lines unique among message outputs
            lines = {}
            for e in els:
                ln = e["_el"].get("designating_line") if isinstance(e["_el"], dict) else None
                if isinstance(ln, str):
                    lines.setdefault(ln.strip(), []).append(e)
            for ln, es in lines.items():
                if len(es) > 1:
                    for e in es:
                        e["findings"].append("FB-20: designating line %r shared by %d outputs" % (ln, len(es)))
                        if e["reading"] == "recognized":
                            e["reading"], e["fb"] = "not_established", "FB-20"
                            counts[e["name"]] = counts.get(e["name"], 1) + 1  # treat as unusable for references
        R["elements"][c] = els
        idx[c] = {e["name"]: e for e in els if e["name"] and counts.get(e["name"]) == 1}
        idx.setdefault("_dup_" + c, {n for n, k in counts.items() if k > 1})

    def ref(cat, name):
        """VO-7: 'ok' | 'undeclared' | 'not_established' (declared but unusable)."""
        if name in idx.get("_dup_" + cat, set()):
            return "not_established"
        e = idx.get(cat, {}).get(name)
        if e is None:
            return "undeclared"
        return "ok" if e["reading"] == "recognized" else "not_established"

    def tool_class(name):
        e = idx.get("required_tools", {}).get(name)
        return e["_el"].get("class") if e else None

    def output_el(name):
        e = idx.get("returned_outputs", {}).get(name)
        return e["_el"] if e else None

    def mark(e, r, fb, why):
        e["findings"].append("%s: %s" % (fb, why))
        if e["reading"] == "recognized":
            e["reading"], e["fb"] = r, fb

    # VO-7 references, VO-8 combinations, VO-9 labels, for non-checkpoint categories
    for e in R["elements"].get("expected_inputs", []):
        el = e["_el"]
        if e["reading"] != "recognized":
            continue
        if el.get("kind") == "host_read":
            s = ref("required_tools", el.get("read_through"))
            if s != "ok":
                mark(e, "not_established", "FB-21", "read_through %r is %s" % (el.get("read_through"), s))
            elif tool_class(el.get("read_through")) != "host_operation":
                mark(e, "not_established", "FB-21", "read_through names a harness capability")
    for e in R["elements"].get("returned_outputs", []):
        el = e["_el"]
        if e["reading"] != "recognized":
            continue
        for s in el.get("promised_standing", []):
            if FORBIDDEN_STANDING.search(s) or s.strip().lower() == "checked":
                mark(e, "invalid", "FB-10", "promised standing %r" % s)
        g = el.get("gating_checkpoint")
        if g and ref("checkpoints", g) != "ok":
            mark(e, "not_established", "FB-21", "gating checkpoint %r is %s" % (g, ref("checkpoints", g)))
        for t in el.get("relies_on", []) + (el.get("produced_by") or {}).get("tools", []):
            if ref("required_tools", t) != "ok":
                mark(e, "not_established", "FB-21", "tool %r is %s" % (t, ref("required_tools", t)))
    for e in R["elements"].get("returned_evidence", []):
        el = e["_el"]
        if e["reading"] != "recognized":
            continue
        for s in el.get("supports", []):
            a, b = ref("returned_outputs", s), ref("checkpoints", s)
            if a == "ok" and b == "ok":
                mark(e, "not_established", "FB-21", "supports %r is ambiguous (output and checkpoint)" % s)
            elif a != "ok" and b != "ok":
                mark(e, "not_established", "FB-21", "supports %r names no usable output or checkpoint" % s)

    # checkpoints: VO-7 references (FB-13), VO-8 combinations (FB-16, FB-17), VO-10 flags
    for e in R["elements"].get("checkpoints", []):
        el = e["_el"]
        if e["reading"] != "recognized":
            continue
        rw, sb = el.get("reached_when", {}), el.get("subject", {})
        act, kind, cls = el.get("required_act"), rw.get("kind"), sb.get("class")

        def need_tool(t, host_only, what):
            s = ref("required_tools", t)
            if s == "undeclared":
                mark(e, "invalid", "FB-13", "%s names undeclared tool %r" % (what, t))
            elif s == "not_established":
                mark(e, "not_established", "§3.4", "%s names tool %r that is not established" % (what, t))
            elif host_only and tool_class(t) != "host_operation":
                mark(e, "invalid", "FB-13", "%s names %r, which is not a host operation" % (what, t))

        def need_output(o, what):
            s = ref("returned_outputs", o)
            if s == "undeclared":
                mark(e, "invalid", "FB-13", "%s names undeclared output %r" % (what, o))
            elif s == "not_established":
                mark(e, "not_established", "§3.4", "%s names output %r that is not established" % (what, o))
        if kind == "before_dispatch":
            need_tool(rw.get("tool"), False, "reached-when")
        elif kind == "output_produced":
            need_output(rw.get("output"), "reached-when")
            o = output_el(rw.get("output"))
            if o is not None and o.get("form") == "host_change" and "produced_by" not in o:
                mark(e, "invalid", "FB-13", "kind (b) on a host-change output without its production element")
            if o is not None and o.get("form") in ("workflow_input", "human_act_standing"):
                mark(e, "invalid", "FB-13", "kind (b) on a %s output, whose production is not observable" % o.get("form"))
        elif kind == "host_outcome":
            for t in rw.get("tools", []):
                need_tool(t, True, "reached-when")
        if cls in ("named_output", "objects_named_output_concerns"):
            need_output(sb.get("output"), "subject")
            o = output_el(sb.get("output"))
            if cls == "objects_named_output_concerns" and o is not None and not o.get("relies_on"):
                mark(e, "invalid", "FB-13", "objects a named output concerns: output %r names no read or examination it relies on" % sb.get("output"))
        if cls == "objects_changed_by_named_outcome":
            for t in sb.get("tools", []):
                need_tool(t, True, "subject")
        # VO-8 combinations
        if act == "A5" and not (kind == "host_outcome" and rw.get("outcome") == "queued" and cls == "change_items_of_named_proposal"):
            mark(e, "invalid", "FB-16", "A5 needs reached-when (c) queued and subject change items of the named proposal")
        if cls == "targets_of_held_call" and kind != "before_dispatch":
            mark(e, "invalid", "FB-16", "targets of the held call needs reached-when (a) (R3-2)")
        if act == "A12" and not (cls == "grant_setting" and sb.get("setting")):
            mark(e, "invalid", "FB-17", "A12 checkpoint names no setting content")
        if cls == "grant_setting" and act != "A12":
            mark(e, "invalid", "FB-17", "grant setting subject is for A12 only")
        if act == "A7" and el.get("actor") != "the_accountable_professional":
            e["findings"].append("note: A7 actor requirement is the accountable professional (V4-AUT-05)")
        # held actions: host_operations_only must name host operations
        ha = el.get("held_actions")
        if isinstance(ha, dict) and ha.get("form") == "host_operations_only" and "held_actions" not in e:
            if any(ref("required_tools", t) != "ok" or tool_class(t) != "host_operation" for t in ha.get("tools", [])):
                e["held_actions"] = "does not show host operations only; governance phase: conservative default (R10-10)"
        # VO-10 flags
        if el.get("fresh_act_required") == "yes" and el.get("governed") != "yes":
            e["findings"].append("note: fresh act required without governed: shown, no effect in any phase (FA-3)")
        # stage anchoring (information only)
    heads = headings(prose_text) if prose_text else set()
    if heads:
        for c in CATEGORIES:
            for e in R["elements"].get(c, []):
                el = e["_el"]
                if not isinstance(el, dict):
                    continue
                anchors = [x for x in (el.get("stages") or []) if isinstance(x, str)] + (
                    [el["position"]] if isinstance(el.get("position"), str) else [])
                for s in anchors:
                    if s not in heads:
                        e["findings"].append("note: stage %r is not a prose heading" % s)
    # compatible roles, restriction (VO-10; FB-22)
    if "compatible_roles" in doc:
        cr = doc["compatible_roles"]
        errs = validate(top["compatible_roles"], cr, schema, "/compatible_roles")
        R["compatible_roles"] = cr if not errs else "not_established"
        if errs:
            R["findings"].append("compatible roles not established: %s" % "; ".join(d for p, k, d in errs))
    if "tool_restriction" in doc:
        tr = doc["tool_restriction"]
        R["tool_restriction"] = tr.get("capabilities") if isinstance(tr, dict) else "not_established"
    if execution_json is not None:
        jr = execution_json.get("compatible_roles")
        if jr is not None and isinstance(R["compatible_roles"], list) and sorted(jr) != sorted(R["compatible_roles"]):
            R["compatible_roles"] = "not_established (FB-22)"
            R["findings"].append("FB-22: declared compatible roles and execution.json compatible_roles differ")
        if R["compatible_roles"] is None and jr is not None:
            R["compatible_roles"] = jr
    if R["categories"].get("required_tools") == "undeclared" and R["tool_restriction"]:
        R["findings"].append("FB-05: required tools undeclared; restriction retained as a ceiling, never read as requirements")
    for c in list(R["elements"]):
        for e in R["elements"][c]:
            e.pop("_el", None)
    return R


def read_package(pkg_dir, schema):
    wf = os.path.join(pkg_dir, "WORKFLOW.md")
    text = open(wf, encoding="utf-8").read()
    ex = extract(text)
    xj = None
    xp = os.path.join(pkg_dir, "execution.json")
    if os.path.exists(xp):
        xj = json.load(open(xp, encoding="utf-8"))
    if ex["status"] == "more_than_one_block":
        R = {"declared_part": "not_established (FB-02)", "findings": ["FB-02: more than one workflow-declaration block"],
             "categories": {}, "elements": {}}
    else:
        R = read_declaration(ex["block_text"], schema, text, xj)
    R["front_matter"] = ex["front_matter"]
    R["carriage"] = ex["status"]
    if ex["front_matter"] and ex["front_matter"].get("name") != os.path.basename(os.path.normpath(pkg_dir)):
        R.setdefault("findings", []).append("note: front-matter name differs from the package folder name")
    R["revision_prototype"] = revision(pkg_dir)
    return R


# ---------------------------------------------------------------- revision (U-03 illustration only)
def revision(pkg_dir):
    """File set and canonicalization of WD §6.1 RV-1..RV-5. The digest method 'proto-sha256-list-0' is an
    illustration for this prototype, NOT a selection (U-03)."""
    entries = []
    for dp, dns, fns in os.walk(pkg_dir, followlinks=False):
        for d in list(dns):
            if os.path.islink(os.path.join(dp, d)):
                return {"status": "not_established", "reason": "non-regular entry (symbolic link) " + d}
        for f in fns:
            p = os.path.join(dp, f)
            if os.path.islink(p) or not os.path.isfile(p):
                return {"status": "not_established", "reason": "non-regular entry " + os.path.relpath(p, pkg_dir)}
            rel = os.path.relpath(p, pkg_dir).replace(os.sep, "/")
            entries.append((rel.encode("utf-8"), hashlib.sha256(open(p, "rb").read()).hexdigest()))
    entries.sort()
    listing = "".join("%s  %s\n" % (h, r.decode("utf-8")) for r, h in entries).encode("utf-8")
    return {"status": "computed", "method": "proto-sha256-list-0 (illustration; U-03 open)", "files": len(entries),
            "value": hashlib.sha256(listing).hexdigest()}


# ---------------------------------------------------------------- helpers for the self-test
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def examples_blocks():
    """Blocks in EXAMPLES.md that follow a '<!-- wd-proto:ID -->' marker line: {ID: block text}."""
    text = open(EXAMPLES_MD, encoding="utf-8").read().split("\n")
    out, i = {}, 0
    while i < len(text):
        m = re.match(r"^<!-- wd-proto:([A-Za-z0-9._-]+) -->$", text[i])
        if m:
            j = i + 1
            while j < len(text) and not FENCE.match(text[j]):
                j += 1
            fm = FENCE.match(text[j])
            fence = fm.group(2)
            k = j + 1
            close = re.compile(r"^ {0,3}" + re.escape(fence[0]) + "{%d,}\\s*$" % len(fence))
            while k < len(text) and not close.match(text[k]):
                k += 1
            out[m.group(1)] = "\n".join(text[j + 1:k])
            i = k
        i += 1
    return out


def write_pkg(root, name, prose, decl, extra=None):
    d = os.path.join(root, name)
    os.makedirs(d, exist_ok=True)
    text = render(decl, prose) if decl is not None else prose
    open(os.path.join(d, "WORKFLOW.md"), "w", encoding="utf-8").write(text)
    for fn, content in (extra or {}).items():
        open(os.path.join(d, fn), "w", encoding="utf-8").write(content)
    return d, text


def load(p):
    return json.load(open(p, encoding="utf-8"))


def hosting_groups():
    """HOSTING §8.4 capability account: {group id: set of supplier names}, Parts A and B."""
    import glob
    execution = os.path.abspath(os.path.join(DESIGN, "..", "..", "..", ".."))
    paths = glob.glob(os.path.join(execution, "PKG-01_*", "1_Working", "DEL-01-01_*", "Design", "HOSTING_BOUNDARY.md"))
    if len(paths) != 1:
        raise RuntimeError("HOSTING_BOUNDARY.md not found once under %s" % execution)
    text = open(paths[0], encoding="utf-8").read()
    sec = text.split("### 8.4 ", 1)[1].split("\n## 9. ", 1)[0]
    groups = {}
    for line in sec.splitlines():
        m = re.match(r"\| \*\*(HCG-[AB]\d\d)\*\*", line)
        if m:
            cells = line.strip("|").split("|")[1:]
            groups[m.group(1)] = set(re.findall(r"`([^`]+)`", "|".join(cells)))
    return paths[0], groups


def check_group_mapping(check):
    """R14-5: each §4.2.5 name names one Part A group; every supplier name its row cites that HOSTING
    places in some group is a member of that group (names HOSTING does not list are skipped)."""
    text = open(os.path.join(DESIGN, "WORKFLOW_DECLARATION.md"), encoding="utf-8").read()
    sec = text.split("#### 4.2.5 ", 1)[1].split("- **HC-1 ", 1)[0]
    path, groups = hosting_groups()
    where = {}
    for g, names in groups.items():
        for n in names:
            where.setdefault(n, set()).add(g)
    rows = [l for l in sec.splitlines() if l.startswith("| `")]
    problems, mapped = [], {}
    for l in rows:
        cells = [c.strip() for c in l.strip("|").split("|")]
        name = cells[0].strip("`")
        gids = re.findall(r"HCG-[AB]\d\d", cells[4])
        if len(set(gids)) != 1 or not gids[0].startswith("HCG-A"):
            problems.append((name, "groups", gids))
            continue
        g = gids[0]
        mapped[name] = g
        for cited in re.findall(r"`([^`]+)`", cells[2] + "|" + cells[4]):
            if cited in where and g not in where[cited]:
                problems.append((name, cited, sorted(where[cited])))
    ok = len(rows) == 10 and not problems and len(groups) == 27
    check("S-11 §4.2.5 names resolve to HOSTING §8.4 groups (R14-5)", ok,
          "%d names -> %s; %d groups read from HOSTING%s" % (len(mapped), ", ".join(
              "%s %s" % (k, v) for k, v in mapped.items()), len(groups), "" if ok else "; problems %s" % problems[:4]))


def selftest():
    schema = load(SCHEMA_PATH)
    results = []

    def check(case, cond, got):
        results.append((case, "PASS" if cond else "FAIL", got))

    tmp = tempfile.mkdtemp(prefix="wdproto-")
    try:
        # S-1 schema and its example instances (R12-1, R12-2)
        v_errs = validate(schema, load(VALID_EXAMPLE))
        check("S-1a valid example (E1) validates", v_errs == [], "%d errors" % len(v_errs))
        inv = load(INVALID_EXAMPLE)
        i_errs = validate(schema, inv)
        want = {("/required_tools/0", "required", "class"), ("/required_tools/0", "required", "purpose"),
                ("/required_tools/1/capability", "enum"), ("/required_tools/1", "required", "fallback"),
                ("/checkpoints/0/required_act", "enum"), ("/checkpoints/0/reached_when/kind", "enum"),
                ("/checkpoints/0/governed", "const"), ("/returned_outputs/0", "required", "designating_line"),
                ("/compatible_roles/0", "enum")}
        got = {(p, k, d) if k == "required" else (p, k) for p, k, d in i_errs}
        check("S-1b invalid example is rejected with the nine expected errors", want <= got and len(i_errs) == 9,
              "%d errors: %s" % (len(i_errs), sorted(got)))
        for fx in ["E1b", "E1d", "E1e"]:
            e = validate(schema, load(os.path.join(FIX, fx + ".declaration.json")))
            check("S-1c %s declaration validates" % fx, e == [], "%d errors %s" % (len(e), e[:3]))

        # S-2 E1: render, parse, read; EXAMPLES.md normative rendering equals the render
        e1 = load(VALID_EXAMPLE)
        prose = open(os.path.join(FIX, "E1.prose.md"), encoding="utf-8").read()
        d, text = write_pkg(tmp, "supports-adjust", prose, e1)
        ex = extract(text)
        check("S-2a E1 renders and extracts one block", ex["status"] == "found", ex["status"])
        doc, err = parse_block(ex["block_text"])
        check("S-2b E1 round trip equals the declaration", err is None and canonical(doc) == canonical(e1), err or "equal")
        R = read_package(d, schema)
        cats = R["categories"]
        allrec = all(e["reading"] == "recognized" for c in R["elements"] for e in R["elements"][c])
        counts = {c: len(R["elements"].get(c, [])) for c in CATEGORIES}
        check("S-2c E1 reading: five categories declared, every element recognized (VC-03)",
              all(cats[c] == "declared" for c in CATEGORIES) and allrec and counts == {
                  "expected_inputs": 3, "required_tools": 5, "checkpoints": 2, "returned_outputs": 5,
                  "returned_evidence": 6}, "%s; %s" % (counts, [f for c in R["elements"] for e in R["elements"][c] for f in e["findings"]]))
        eb = examples_blocks()
        check("S-2d EXAMPLES.md E1 rendering is byte-identical to the render", eb.get("E1.WORKFLOW.md") == text.rstrip("\n"),
              "marker present" if "E1.WORKFLOW.md" in eb else "marker missing")
        r1 = revision(d)
        r2 = revision(d)
        open(os.path.join(d, "WORKFLOW.md"), "a", encoding="utf-8").write(" ")
        r3 = revision(d)
        open(os.path.join(d, "WORKFLOW.md"), "w", encoding="utf-8").write(text)
        os.symlink("WORKFLOW.md", os.path.join(d, "alias.md"))
        r4 = revision(d)
        os.remove(os.path.join(d, "alias.md"))
        check("S-2e revision file set (RV-1..RV-5): stable, byte-sensitive, link not established",
              r1["value"] == r2["value"] and r3["value"] != r1["value"] and r4["status"] == "not_established",
              "%s…; changed %s…; link: %s" % (r1["value"][:12], r3["value"][:12], r4["status"]))

        # S-3 E1d
        e1d = load(os.path.join(FIX, "E1d.declaration.json"))
        prose_d = open(os.path.join(FIX, "E1d.prose.md"), encoding="utf-8").read()
        d, text = write_pkg(tmp, "label-with-grant", prose_d, e1d)
        R = read_package(d, schema)
        cps = {e["name"]: e for e in R["elements"]["checkpoints"]}
        check("S-3a E1d reading: tools and checkpoints declared; inputs, outputs, evidence undeclared; CP-grant and CP-check recognized",
              R["categories"] == {"expected_inputs": "undeclared", "required_tools": "declared", "checkpoints": "declared",
                                  "returned_outputs": "undeclared", "returned_evidence": "undeclared"}
              and cps["CP-grant"]["reading"] == "recognized" and cps["CP-check"]["reading"] == "recognized",
              "%s; CP-grant %s" % (R["categories"], cps["CP-grant"]["reading"]))
        check("S-3b EXAMPLES.md E1d rendering is byte-identical to the render", eb.get("E1d.WORKFLOW.md") == text.rstrip("\n"),
              "marker present" if "E1d.WORKFLOW.md" in eb else "marker missing")
        for fx in ["E1b", "E1e"]:
            blk = eb.get(fx + ".declaration")
            ok = blk is not None and canonical(json.loads(blk)) == canonical(load(os.path.join(FIX, fx + ".declaration.json")))
            check("S-3c EXAMPLES.md %s declared part equals the fixture" % fx, ok, "equal" if ok else "differs or missing")

        # S-4 E1e: A6, A7, input kinds, harness capability
        e1e = load(os.path.join(FIX, "E1e.declaration.json"))
        d, text = write_pkg(tmp, "supports-approve", open(os.path.join(FIX, "E1e.prose.md"), encoding="utf-8").read(), e1e)
        R = read_package(d, schema)
        rec = {e["name"]: e["reading"] for c in R["elements"] for e in R["elements"][c]}
        check("S-4 E1e reading: A6 and A7 checkpoints, both new input kinds and the file-change capability recognized",
              all(v == "recognized" for v in rec.values()) and len(rec) == 13, "%d elements, %s" % (len(rec), sorted(set(rec.values()))))

        # S-5 E5: Root create-workflow (real bytes) and its declared-empty variant
        e5 = os.path.join(REPO, "workflows", "create-workflow")
        R = read_package(e5, schema)
        check("S-5a E5 (real bytes): no block; every category undeclared; no checkpoint synthesized (VC-04)",
              R["carriage"] == "absent" and set(R["categories"].values()) == {"undeclared"} and not R["elements"],
              "carriage %s; name %s" % (R["carriage"], R["front_matter"].get("name")))
        src = open(os.path.join(e5, "WORKFLOW.md"), encoding="utf-8").read()
        d, _ = write_pkg(tmp, "create-workflow", src, {"declaration_contract_version": "WD-v0.8", "checkpoints": []})
        R = read_package(d, schema)
        check("S-5b E5 variant declaring no checkpoints: checkpoints declared empty, the rest undeclared",
              R["categories"]["checkpoints"] == "declared_empty" and R["categories"]["required_tools"] == "undeclared",
              str(R["categories"]))

        # S-6 E6: Root project-dag (real bytes) and its v4 rendering
        e6 = os.path.join(REPO, "workflows", "project-dag")
        R = read_package(e6, schema)
        check("S-6a E6 (real bytes): required tools undeclared; restriction retained (7); role WORKING_ITEMS; FB-05 (VC-06)",
              R["categories"]["required_tools"] == "undeclared" and len(R["tool_restriction"] or []) == 7
              and R["compatible_roles"] == ["WORKING_ITEMS"] and any(f.startswith("FB-05") for f in R["findings"]),
              "restriction %s" % R["tool_restriction"])
        xj = load(os.path.join(e6, "execution.json"))
        v4 = {"declaration_contract_version": "WD-v0.8", "compatible_roles": xj["compatible_roles"],
              "tool_restriction": {"capabilities": xj["tools"]["capabilities"]}}
        src = open(os.path.join(e6, "WORKFLOW.md"), encoding="utf-8").read()
        d, _ = write_pkg(tmp, "project-dag", src, v4)
        R = read_package(d, schema)
        check("S-6b E6 in the carriage: restriction stays a restriction; required tools undeclared; no requirement derived",
              R["categories"]["required_tools"] == "undeclared" and R["tool_restriction"] == xj["tools"]["capabilities"]
              and "required_tools" not in R["elements"] and any(f.startswith("FB-05") for f in R["findings"]),
              str(R["categories"]["required_tools"]))
        bad = dict(v4, compatible_roles=["TASK"])
        d, _ = write_pkg(tmp, "project-dag-x", src, bad, {"execution.json": json.dumps(xj)})
        R = read_package(d, schema)
        check("S-6c declared roles differ from execution.json: FB-22, roles not established",
              R["compatible_roles"] == "not_established (FB-22)", str(R["compatible_roles"]))

        # S-7 variants (VC-12, VC-29, VC-41, VC-45 and the new rules)
        def variant(base, mutate):
            doc = copy.deepcopy(base)
            mutate(doc)
            return read_declaration(json.dumps(doc, ensure_ascii=False), schema)

        def cp(R, name):
            return [e for e in R["elements"]["checkpoints"] if e["name"] == name]

        def setp(path, value):
            def f(doc):
                o = doc
                for k in path[:-1]:
                    o = o[k]
                o[path[-1]] = value
            return f
        V = [
            ("L-WDEX-18a VC-12 A2 apply", e1, setp(["checkpoints", 1, "required_act"], "A2"), "CP-check", ("invalid", "FB-03")),
            ("L-WDEX-18e VC-12 A3 examine", e1, setp(["checkpoints", 1, "required_act"], "A3"), "CP-check", ("invalid", "FB-03")),
            ("L-WDEX-18b VC-12 A14 tool permission", e1, setp(["checkpoints", 1, "required_act"], "A14"), "CP-check", ("invalid", "FB-03")),
            ("L-WDEX-18c VC-12 A15 register (R12-5)", e1, setp(["checkpoints", 1, "required_act"], "A15"), "CP-check", ("invalid", "FB-03")),
            ("L-WDEX-18d VC-12 unknown name", e1, setp(["checkpoints", 1, "required_act"], "approve-design"), "CP-check", ("not_established", "FB-04")),
            ("L-WDEX-19a VC-29 A5 kind (a)", e1, setp(["checkpoints", 0, "reached_when"], {"kind": "before_dispatch", "tool": "add-support"}), "CP-accept", ("invalid", "FB-16")),
            ("L-WDEX-19b VC-29 A5 kind (b)", e1, setp(["checkpoints", 0, "reached_when"], {"kind": "output_produced", "output": "summary"}), "CP-accept", ("invalid", "FB-16")),
            ("L-WDEX-19c VC-29 A5 other subject", e1, setp(["checkpoints", 0, "subject"], {"class": "objects_changed_by_named_outcome", "tools": ["add-support"], "outcome": "applied"}), "CP-accept", ("invalid", "FB-16")),
            ("L-WDEX-19d VC-29 held-call targets with kind (b)", e1, setp(["checkpoints", 1, "subject"], {"class": "targets_of_held_call"}), "CP-check", ("invalid", "FB-16")),
            ("L-WDEX-20 VC-41 A12 without setting", e1d, setp(["checkpoints", 0, "subject"], {"class": "grant_setting"}), "CP-grant", ("invalid", "FB-17")),
            ("L-WDEX-21a VC-45 governed yes", e1d, setp(["checkpoints", 0, "governed"], "yes"), "CP-grant", ("recognized", None, "yes")),
            ("L-WDEX-21b VC-45 governed absent", e1d, lambda d: None, "CP-grant", ("recognized", None, "absent")),
            ("L-WDEX-21c VC-45 governed unrecognized", e1d, setp(["checkpoints", 0, "governed"], "maybe"), "CP-grant", ("recognized", None, "not_established (FB-19)")),
            ("L-WDEX-22 duplicate checkpoint name", e1, lambda d: d["checkpoints"].append(copy.deepcopy(d["checkpoints"][1])), "CP-check", ("invalid", "FB-20")),
            ("L-WDEX-23 reached-when names undeclared output", e1, setp(["checkpoints", 1, "reached_when", "output"], "final-report"), "CP-check", ("invalid", "FB-13")),
            ("L-WDEX-24 message output without designating line", e1, lambda d: d["returned_outputs"][1].pop("designating_line"), "CP-check", ("not_established", "§3.4")),
            ("L-WDEX-25 unknown element in a checkpoint", e1, setp(["checkpoints", 1, "priority"], "high"), "CP-check", ("not_established", "§3.4")),
            ("L-WDEX-26 malformed held actions", e1, setp(["checkpoints", 1, "held_actions"], {"form": "some"}), "CP-check", ("recognized", None)),
            ("L-WDEX-27a fresh act on a governed checkpoint", e1d, lambda d: d["checkpoints"][0].update(governed="yes", fresh_act_required="yes"), "CP-grant", ("recognized", None)),
            ("L-WDEX-27b fresh act without governed", e1d, setp(["checkpoints", 0, "fresh_act_required"], "yes"), "CP-grant", ("recognized", None)),
            ("L-WDEX-28 on subject absent declared", e1, setp(["checkpoints", 1, "on_subject_absent"], {"path": "return_to_stage", "stage": "Re-examine"}), "CP-check", ("recognized", None)),
        ]
        for label, base, mut, name, exp in V:
            R = variant(base, mut)
            es = cp(R, name)
            got = [(e["reading"], e["fb"]) + ((e.get("governed"),) if len(exp) == 3 else ()) for e in es]
            ok = bool(es) and all(g == exp for g in got)
            extra = ""
            if label.startswith("L-WDEX-26"):
                ok = ok and "R10-10" in (es[0].get("held_actions") or "")
                extra = "; held actions: " + str(es[0].get("held_actions"))
            if label.startswith("L-WDEX-27b"):
                ok = ok and any("FA-3" in f for f in es[0]["findings"])
            check("S-7 " + label, ok, "%s%s" % (got, extra))
        R = variant(e1, lambda d: d["returned_outputs"][4].update(designating_line=d["returned_outputs"][1]["designating_line"]))
        got = [(e["name"], e["reading"], e["fb"]) for e in R["elements"]["returned_outputs"] if e["fb"]]
        ck = cp(R, "CP-check")[0]
        check("S-7 L-WDEX-37 two message outputs share a designating line: both FB-20; CP-check on one not established",
              got == [("examination-report", "not_established", "FB-20"), ("summary", "not_established", "FB-20")]
              and ck["reading"] == "not_established", "%s; CP-check %s" % (got, ck["reading"]))
        def wf_input(d):
            d["returned_outputs"][4]["form"] = "workflow_input"
            del d["returned_outputs"][4]["designating_line"]
            d["checkpoints"][1]["reached_when"]["output"] = "summary"
        R = variant(e1, wf_input)
        check("S-7 L-WDEX-38 kind (b) on a workflow-input output is invalid (FB-13)",
              [(e["reading"], e["fb"]) for e in cp(R, "CP-check")] == [("invalid", "FB-13")], str([(e["reading"], e["fb"]) for e in cp(R, "CP-check")]))
        R = variant(e1, lambda d: d["returned_outputs"][0]["promised_standing"].append("approved"))
        check("S-7 L-WDEX-29 output promising 'approved' is invalid (FB-10)",
              [(e["reading"], e["fb"]) for e in R["elements"]["returned_outputs"] if e["name"] == "adjustment"] == [("invalid", "FB-10")], "")
        R = variant(e1, setp(["returned_evidence", 0, "supports"], ["nothing-here"]))
        check("S-7 L-WDEX-30 evidence supporting an undeclared name (FB-21)",
              R["elements"]["returned_evidence"][0]["fb"] == "FB-21", R["elements"]["returned_evidence"][0]["fb"])
        R = variant(e1, lambda d: d["required_tools"].append({"name": "gpu", "class": "harness_capability", "capability": "gpu-compute", "purpose": "x", "necessity": "required", "stages": ["Inspect"]}))
        check("S-7 L-WDEX-31 unrecognized harness capability name: that reference not established",
              [e["reading"] for e in R["elements"]["required_tools"] if e["name"] == "gpu"] == ["not_established"], "")
        R = variant(e1, lambda d: d.update(x_note="kept"))
        check("S-7 L-WDEX-32 unrecognized top-level element preserved; categories unaffected",
              R["unrecognized_top_level"] == ["x_note"] and R["categories"]["checkpoints"] == "declared", str(R["unrecognized_top_level"]))
        for lbl, ver in [("L-WDEX-33a newer contract version", "WD-v0.9"), ("L-WDEX-33b pre-representation version", "WD-v0.7")]:
            R = variant(e1, setp(["declaration_contract_version"], ver))
            check("S-7 %s: declared part not established" % lbl, R["declared_part"].startswith("not_established"), R["declared_part"])
        blk = json.dumps(e1, indent=2, ensure_ascii=False)
        R = read_declaration(blk.replace('"declaration_contract_version": "WD-v0.8",', '"declaration_contract_version": "WD-v0.8",\n  "checkpoints": [],', 1), schema)
        check("S-7 L-WDEX-34 duplicate JSON key: FB-02", R["declared_part"] == "not_established (FB-02)", R["findings"][:1])
        d, text = write_pkg(tmp, "two-blocks", prose + "```workflow-declaration\n{}\n```\n", e1)
        R = read_package(d, schema)
        check("S-7 L-WDEX-35 two declaration blocks: FB-02, nothing read", R["declared_part"] == "not_established (FB-02)", R["findings"][:1])
        nested = "---\nname: nested\ndescription: x\n---\n# Nested\n\n````markdown\n```workflow-declaration\n{}\n```\n````\n"
        check("S-7 L-WDEX-36 a declaration block quoted inside another fence is not read", extract(nested)["status"] == "absent", extract(nested)["status"])

        # L-WDEX-42 (RP-3; V18-2 m-2): a file output without its path is not established, and the
        # kind (b) checkpoint on it is not established, never recognized
        R = variant(e1e, lambda d: [o.pop("path") for o in d["returned_outputs"] if o["name"] == "approval-package"])
        outp = [(e["reading"], e["fb"]) for e in R["elements"]["returned_outputs"] if e["name"] == "approval-package"]
        ck = [(e["reading"], e["fb"]) for e in cp(R, "CP-approve")]
        check("S-7 L-WDEX-42 file output without path: output not established (FB-02); CP-approve not established",
              outp == [("not_established", "FB-02")] and ck == [("not_established", "§3.4")], "%s; CP-approve %s" % (outp, ck))

        # S-8 the invalid example read element by element (a reader does not reject the whole document)
        R = read_declaration(json.dumps(inv), schema)
        got = {c: [(e["name"], e["reading"], e["fb"]) for e in R["elements"].get(c, [])] for c in R["elements"]}
        check("S-8 invalid example read: tools not established; CP-check invalid FB-03 (FB-19 reported); output not established; roles not established",
              got["required_tools"] == [("read-supports", "not_established", "FB-02"), ("write-report", "not_established", "FB-02")]
              and got["checkpoints"] == [("CP-check", "invalid", "FB-03")]
              and got["returned_outputs"] == [("summary", "not_established", "FB-02")]
              and R["compatible_roles"] == "not_established", str(got))

        # S-9 cross-language parse: node (if present) extracts and parses the same E1 block
        node = shutil.which("node")
        if node:
            d = os.path.join(tmp, "supports-adjust", "WORKFLOW.md")
            out = subprocess.run([node, os.path.join(HERE, "extract.mjs"), d], capture_output=True, text=True, timeout=30)
            ok = out.returncode == 0 and out.stdout.strip() == canonical(e1)
            check("S-9 node extract.mjs gives the same canonical JSON for E1", ok, "node %s" % subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip())
        else:
            check("S-9 node extract.mjs gives the same canonical JSON for E1", True, "SKIPPED: node not found")

        # S-10 the workflow identity definition (WD §6.1, §3.6; RP-3, V18-2 m-9) and its conformance instances
        ids = load(os.path.join(FIX, "workflow-identity.examples.json"))
        idef = schema["$defs"]["workflow_identity"]
        for v in ids["valid"]:
            e = validate(idef, v["instance"], schema)
            check("S-10 identity valid: %s" % v["label"], e == [], "%d errors %s" % (len(e), e[:2]))
        for v in ids["invalid"]:
            e = validate(idef, v["instance"], schema)
            check("S-10 identity invalid: %s" % v["label"], len(e) == 1 and [e[0][0], e[0][1]] == v["error"], str(e))

        # S-11 the name-to-group mapping of WD §4.2.5 against HOSTING §8.4 (R14-5)
        check_group_mapping(check)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    w = max(len(r[0]) for r in results)
    for case, st, got in results:
        print("%-4s %-*s  %s" % (st, w, case, got))
    fails = sum(1 for r in results if r[1] == "FAIL")
    print("\n%d checks, %d passed, %d failed" % (len(results), len(results) - fails, fails))
    return 1 if fails else 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "selftest":
        return selftest()
    if len(argv) == 3 and argv[1] == "read":
        print(json.dumps(read_package(argv[2], load(SCHEMA_PATH)), indent=2, ensure_ascii=False))
        return 0
    if len(argv) == 5 and argv[1] == "render":
        decl, prose = load(argv[2]), open(argv[3], encoding="utf-8").read()
        name = (split_front_matter(prose)[0] or {}).get("name", "workflow")
        d, _ = write_pkg(argv[4], name, prose, decl)
        print(os.path.join(d, "WORKFLOW.md"))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
