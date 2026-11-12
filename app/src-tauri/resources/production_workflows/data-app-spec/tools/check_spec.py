#!/usr/bin/env python3
"""App-spec checker: JSON Schema validation plus semantic rules (data-app-spec workflow).

The rules are listed in formats/ONTOLOGY.md §5 and formats/PROJECTION.md. Expression
handling is lexical. A `.json` file is parsed as JSON; any other file as YAML 1.2.
Requires PyYAML and jsonschema.

Usage:
    python3 -I check_spec.py SCHEMA.json SPEC.yaml [SPEC.yaml ...]

Exit status: 0 when every spec parses, passes schema validation and has no semantic
errors; 1 otherwise; 2 on bad invocation. Warnings and the buildability verdict are
reported but do not change the exit status.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import jsonschema
import yaml


class Yaml12Loader(yaml.SafeLoader):
    """SafeLoader without YAML 1.1 surprises: only true/false are booleans; no timestamps."""


for _ch, _resolvers in list(Yaml12Loader.yaml_implicit_resolvers.items()):
    Yaml12Loader.yaml_implicit_resolvers[_ch] = [
        (tag, rx) for tag, rx in _resolvers
        if tag not in ("tag:yaml.org,2002:bool", "tag:yaml.org,2002:timestamp")
    ]
Yaml12Loader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), list("tTfF"))

STATE_TOKEN = re.compile(r"\$([a-z][a-z0-9_]*)")


class Walker:
    def __init__(self, schema):
        self.defs = schema["$defs"]
        self.ids = {}            # id -> (class, path)
        self.dupes = []
        self.refs = []           # (path, expected_class, value, owner_class, slot)
        self.paths = []          # (path, value)  ElementPath values
        self.exprs = []          # (path, value)
        self.extensions = []     # (path, value)
        self.objects = defaultdict(list)  # class -> [(path, obj)]

    def parents(self, cls):
        out = [cls]
        while True:
            parent = self.defs.get(out[-1], {}).get("x-appspec-is-a")
            if not parent:
                return out
            out.append(parent)

    def concrete(self, defname, node):
        d = self.defs[defname]
        if d.get("x-appspec-abstract"):
            kind = node.get("kind") if isinstance(node, dict) else None
            return kind if kind in self.defs else None
        return defname

    def walk_value(self, value, schema, path, owner, slot):
        if not schema:
            return
        if "x-appspec-ref" in schema:
            if isinstance(value, str):
                self.refs.append((path, schema["x-appspec-ref"], value, owner, slot))
            return
        if schema.get("x-appspec-type") == "ElementPath" and isinstance(value, str):
            self.paths.append((path, value))
            return
        if schema.get("x-appspec-type") == "Expression" and isinstance(value, str):
            self.exprs.append((path, value))
            return
        if schema.get("type") == "array" and isinstance(value, list):
            for i, item in enumerate(value):
                self.walk_value(item, schema.get("items", {}), f"{path}[{i}]", owner, slot)
            return
        if "$ref" in schema and isinstance(value, dict):
            self.walk_object(value, schema["$ref"].split("/")[-1], path)
            return
        if "anyOf" in schema:
            for alt in schema["anyOf"]:
                if "$ref" in alt and isinstance(value, dict):
                    self.walk_object(value, alt["$ref"].split("/")[-1], path)
                    return

    def walk_object(self, node, defname, path):
        cls = self.concrete(defname, node)
        if cls is None:
            return
        d = self.defs[cls]
        self.objects[cls].append((path, node))
        if "id" in node and "id" in d.get("properties", {}):
            if node["id"] in self.ids:
                self.dupes.append((node["id"], self.ids[node["id"]][1], path))
            else:
                self.ids[node["id"]] = (cls, path)
        for key, value in node.items():
            if key.startswith("x-"):
                self.extensions.append((f"{path}.{key}", value))
                continue
            prop = d.get("properties", {}).get(key)
            if prop is not None:
                self.walk_value(value, prop, f"{path}.{key}", cls, key)


def summarize(value, limit=110):
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def check(schema, spec_path):
    report, errors, warnings = [], 0, 0
    report.append(f"## {spec_path}")
    try:
        text = Path(spec_path).read_text(encoding="utf-8")
        # Canonical JSON is parsed as JSON: the YAML loader's 1.1 float rule reads exponent forms
        # without a decimal point (e.g. 1e-12) as strings.
        spec = json.loads(text) if str(spec_path).endswith(".json") else yaml.load(text, Loader=Yaml12Loader)
    except (OSError, UnicodeDecodeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        report.append(f"\nPARSE: FAIL - {type(exc).__name__}: {' '.join(str(exc).split())[:400]}")
        return "\n".join(report), 1, 0
    if not isinstance(spec, dict):
        report.append("\nPARSE: FAIL - the document is not a mapping")
        return "\n".join(report), 1, 0
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    schema_errors = sorted(validator.iter_errors(spec), key=lambda e: list(e.absolute_path))
    if schema_errors:
        report.append(f"\nSCHEMA: FAIL ({len(schema_errors)} errors)")
        for err in schema_errors[:60]:
            loc = "/".join(str(p) for p in err.absolute_path)
            report.append(f"- `{loc}`: {err.message[:300]}")
        errors += len(schema_errors)
    else:
        report.append("\nSCHEMA: PASS (JSON Schema 2020-12)")

    w = Walker(schema)
    w.walk_object(spec, "AppSpec", "$")
    sem = []
    for ident, first, second in w.dupes:
        sem.append(f"ERROR duplicate id `{ident}` at {first} and {second}")
    for path, expected, value, owner, slot in w.refs:
        if value not in w.ids:
            sem.append(f"ERROR unresolved reference {path} -> `{value}` (expected {expected})")
            continue
        actual = w.ids[value][0]
        if expected not in w.parents(actual):
            sem.append(f"ERROR reference {path} -> `{value}` is {actual}, expected {expected}")
    for path, value in w.paths:
        head = value.split(".")[0]
        if head not in w.ids:
            sem.append(f"ERROR element path {path} -> `{value}`: `{head}` is not an element id")
    state_ids = {i for i, (c, _) in w.ids.items() if c == "StateVariable"}
    for path, value in w.exprs:
        for token in STATE_TOKEN.findall(value):
            if token not in state_ids:
                sem.append(f"ERROR expression {path} uses `${token}`, which is not a state variable")
    for path, pb in w.objects.get("ParameterBinding", []):
        given = [k for k in ("value", "expression", "from_state", "tbd") if k in pb]
        if len(given) != 1:
            sem.append(f"ERROR R-PB1 {path} must give exactly one of value/expression/from_state/tbd (has {given})")
    for path, pl in w.objects.get("Placement", []):
        has_ref, has_items = "ref" in pl, "items" in pl
        if has_ref == has_items:
            sem.append(f"ERROR R-PL1 {path} must have exactly one of ref/items")
        if has_ref and pl["ref"] not in w.ids:
            sem.append(f"ERROR placement {path} -> `{pl['ref']}` is not an element id")

    # control effect coverage: a state set by a control must be read elsewhere
    read = set()
    for path, expected, value, owner, slot in w.refs:
        if expected == "StateVariable" and not (slot == "sets" and owner.endswith("Control")):
            read.add(value)
    for path, value in w.exprs:
        read.update(STATE_TOKEN.findall(value))
    for cls, items in w.objects.items():
        if not cls.endswith("Control"):
            continue
        for path, ctl in items:
            target = ctl.get("sets")
            if target and target not in read:
                sem.append(f"WARN control `{ctl.get('id')}` sets `{target}`, which nothing reads")
    # verification coverage
    tested = {k.get("subject") for _, k in w.objects.get("KnownAnswerTest", [])}
    for path, comp in w.objects.get("AnalysisComponent", []):
        used_by = [a.get("id") for _, a in w.objects.get("Analysis", []) if a.get("component") == comp.get("id")]
        if comp.get("id") not in tested and not tested.intersection(used_by):
            sem.append(f"WARN component `{comp.get('id')}` has no known-answer test")
    rulings = w.objects.get("Ruling", [])
    for path, r in rulings:
        if r.get("status") == "made" and not (r.get("evidence") and r.get("decided_by")):
            sem.append(f"ERROR ruling `{r.get('id')}` is marked made without decided_by and evidence")
    # a fidelity choice binds only under a ruling a person made; an author cannot originate one (rule R-FD2)
    ruling_status = {r.get("id"): r.get("status") for _, r in rulings}
    fidelity = [f for _, f in w.objects.get("FidelityDecision", [])]
    undecided = [f for f in fidelity if f.get("selected") in ("undecided", "defer")]
    chosen = [f for f in fidelity if f.get("selected") not in ("undecided", "defer")]
    for f in chosen:
        if not f.get("ruling"):
            sem.append(f"ERROR R-FD2 fidelity decision `{f.get('id')}` selects `{f.get('selected')}` without naming a ruling")
    unruled = [f for f in chosen if ruling_status.get(f.get("ruling")) != "made"]

    # interface conformance: bindings must name declared parameters and ports (rule R-IF1)
    comps = {}
    for _, c in w.objects.get("AnalysisComponent", []):
        comps[c.get("id")] = {
            "params": {p.get("name") for p in c.get("parameters", []) or []},
            "required": {p.get("name") for p in c.get("parameters", []) or [] if p.get("required") and "default" not in p},
            "inputs": {p.get("name") for p in c.get("inputs", []) or []},
            "outputs": {p.get("name") for p in c.get("outputs", []) or []},
        }
    analysis_comp = {a.get("id"): a.get("component") for _, a in w.objects.get("Analysis", [])}

    def head(output_path):
        return re.split(r"[.\[]", output_path, maxsplit=1)[0]

    for path, a in w.objects.get("Analysis", []):
        c = comps.get(a.get("component"))
        if c is None:
            continue
        bound = set()
        for pb in a.get("parameters", []) or []:
            bound.add(pb.get("name"))
            if pb.get("name") not in c["params"]:
                sem.append(f"ERROR R-IF1 analysis `{a.get('id')}` binds `{pb.get('name')}`, which component `{a.get('component')}` does not declare")
        for missing in sorted(c["required"] - bound):
            sem.append(f"WARN analysis `{a.get('id')}` leaves required parameter `{missing}` unbound")
        for ib in a.get("inputs", []) or []:
            if ib.get("port") not in c["inputs"]:
                sem.append(f"ERROR R-IF1 analysis `{a.get('id')}` binds input port `{ib.get('port')}`, which the component does not declare")
        for out in a.get("outputs", []) or []:
            if out.get("port") not in c["outputs"]:
                sem.append(f"ERROR R-IF1 analysis `{a.get('id')}` maps output port `{out.get('port')}`, which the component does not declare")
    for path, sc in w.objects.get("Scenario", []):
        targets = [comps.get(analysis_comp.get(x)) for x in sc.get("applies_to", []) or []]
        names = set().union(*[t["params"] for t in targets if t]) if targets else set()
        for pb in sc.get("overrides", []) or []:
            if names and pb.get("name") not in names:
                sem.append(f"ERROR R-IF1 scenario `{sc.get('id')}` overrides `{pb.get('name')}`, which no applies_to component declares")
    for path, k in w.objects.get("KnownAnswerTest", []):
        subj = k.get("subject")
        c = comps.get(subj) or comps.get(analysis_comp.get(subj))
        if c is None:
            continue
        for pb in k.get("parameters", []) or []:
            if pb.get("name") not in c["params"]:
                sem.append(f"ERROR R-IF1 test `{k.get('id')}` sets `{pb.get('name')}`, which the subject's component does not declare")
        for ev in k.get("expected", []) or []:
            if head(ev.get("output", "")) not in c["outputs"]:
                sem.append(f"ERROR R-IF1 test `{k.get('id')}` expects output `{ev.get('output')}`, whose port the component does not declare")

    # placeholders: elements whose content is not established may not be built from (rule R-TBD1)
    placeholders = []
    for cls, items in w.objects.items():
        for path, obj in items:
            if isinstance(obj, dict) and obj.get("standing") == "TBD":
                placeholders.append(f"{cls} `{obj.get('id', obj.get('name', path))}`")
    warnings += sum(1 for s in sem if s.startswith("WARN"))
    errors += sum(1 for s in sem if s.startswith("ERROR"))

    report.append(f"\nSEMANTIC: {sum(1 for s in sem if s.startswith('ERROR'))} errors, {sum(1 for s in sem if s.startswith('WARN'))} warnings")
    report.extend(f"- {s}" for s in sem)

    gaps = w.objects.get("Gap", [])
    open_gaps = [g for _, g in gaps if g.get("status") == "open"]
    blocking = [g for g in open_gaps if "build" in (g.get("blocking") or [])]
    proposed = [r for _, r in rulings if r.get("status") == "proposed"]
    tier = (spec.get("consequence") or {}).get("tier", "unstated")
    report.append("\nSTANDING")
    report.append(f"- elements with ids: {len(w.ids)}; consequence tier: {tier}")
    report.append(f"- gaps: {len(gaps)} total, {len(open_gaps)} open, {len(blocking)} blocking a faithful build")
    report.append(f"- rulings: {len(rulings)} ({len(proposed)} proposed, awaiting a human decision)")
    report.append(f"- fidelity decisions: {len(fidelity)} ({len(undecided)} undecided or deferred; "
                  f"{len(unruled)} selected but awaiting a made ruling)")
    report.append(f"- placeholder elements (standing TBD): {len(placeholders)}" + (f" - {', '.join(placeholders[:12])}" + (" ..." if len(placeholders) > 12 else "") if placeholders else ""))
    verdict = "NOT BUILDABLE" if (blocking or undecided or unruled or placeholders or schema_errors) else "BUILDABLE (structurally)"
    report.append(f"- buildability verdict: {verdict}. Structural buildability is not acceptance or adequacy.")
    if w.extensions:
        report.append(f"\nEXTENSIONS (needs the schema did not meet): {len(w.extensions)}")
        for path, value in w.extensions:
            report.append(f"- `{path}`: {summarize(value)}")
    else:
        report.append("\nEXTENSIONS: none")
    return "\n".join(report), errors, warnings


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    schema = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    total_errors = 0
    out = ["# check_spec report", ""]
    for spec_path in argv[2:]:
        text, errs, _ = check(schema, spec_path)
        out.append(text)
        out.append("")
        total_errors += errs
    print("\n".join(out))
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
