#!/usr/bin/env python3
"""Mutation tests for the design checker.

Each case copies the worked example (examples/), introduces one defect, and checks
that the expected rule reports it. A checker that passes the unmodified example but
misses a defect fails this test. Run from the data-app-spec package folder:

    python3 -I tools/test_check_design.py

Exit status 0 when every case behaves as expected; 1 otherwise.
"""
import copy
import importlib.util
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples"


def load_module(name):
    module_spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


check_design = load_module("check_design")
Loader = check_design.check_spec.Yaml12Loader


def read(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=Loader)


def find(items, ident):
    return next(item for item in items if item.get("id") == ident)


RECORD_PATH = "checkpoint_snapshots/D-test/DESIGN_DECISION.md"


RULES_PATH = "rules/decision_rules.csv"
RULES_TEXT = "rule_id,worst_status,any_increasing,min_record,action\nR1,below,false,8,reduce\n"


def run_case(design, spec, catalogue, record=None, files=None):
    """Write the documents to a temporary folder and check them.

    `record` is None, or a function given the reloaded design that returns the text of
    a DESIGN_DECISION.md to write at RECORD_PATH, so that digests are computed on the
    bytes the checker reads. `files` maps further relative paths to their text.
    """
    with tempfile.TemporaryDirectory() as tmp:
        paths = {}
        for name, document in (("design", design), ("spec", spec), ("catalogue", catalogue)):
            paths[name] = Path(tmp) / f"{name}.yaml"
            paths[name].write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
        for relative, text in (files or {}).items():
            target = Path(tmp) / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        if record is not None:
            target = Path(tmp) / RECORD_PATH
            target.parent.mkdir(parents=True)
            target.write_text(record(read(paths["design"])), encoding="utf-8")
        report, status = check_design.run(ROOT / "formats", paths["catalogue"], paths["design"], paths["spec"])
    return report, status


def mark_all_made(design, evidence=RECORD_PATH):
    for ruling in design["rulings"]:
        ruling.update(status="made", decided_by="Illustrative owner", evidence=evidence)


def digests(design, returned=()):
    made = [r["id"] for r in design["rulings"] if r["id"] not in returned]
    lines = [f"Digest {r['id']}: {check_design.ruling_digest(design, r)}" for r in design["rulings"]]
    return ("Human response: test fixture, not a real decision\n"
            f"Rulings made: {', '.join(made)}\n"
            f"Rulings returned: {', '.join(returned) or 'none'}\n" + "\n".join(lines) + "\n")


def with_rules(design, text=RULES_TEXT):
    """Give k_decision_rules identified content, as an elicited rule table would."""
    import hashlib
    find(design["knowledge_needs"], "k_decision_rules")["adopted_content"] = {
        "path": RULES_PATH, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def all_made_with_rules(design, spec, catalogue):
    with_rules(design)
    mark_all_made(design)


def drop_min_record_gap(design, spec, catalogue):
    """Remove the gap that records k_min_record, and answer the question it covered."""
    design["gaps"].remove(find(design["gaps"], "g_min_record"))
    for settled in find(design["choices"], "ch_trend")["settled"]:
        if settled["key"] == "minimum_record":
            settled.pop("gap")
            settled["answer"] = "8 results"


def add_question(spec, text):
    spec["purpose"]["questions"] = [{"id": "n_exceedances", "text": text}]


# (name, mutation, record, expected text in report, expected exit status)
CASES = [
    ("unmodified example passes", lambda d, s, c: None, None, "RULES: 0 errors, 0 warnings", 0),
    ("need without an answering element", lambda d, s, c: find(d["needs"], "n_where").pop("answered_by"), None, "ERROR D-Q1 need `n_where`", 1),
    ("trace to a missing element", lambda d, s, c: find(d["needs"], "n_where").update(answered_by=["no_such_view"]), None, "ERROR D-T1", 1),
    ("choice without ruling or delegation", lambda d, s, c: find(d["choices"], "ch_export").pop("ruling"), None, "ERROR D-CH2 choice `ch_export` names neither", 1),
    ("consequential choice under a delegation", lambda d, s, c: find(d["choices"], "ch_well_detail").update(category="consequential"), None, "ERROR D-CH2 choice `ch_well_detail` is consequential", 1),
    ("delegation covering consequential choices", lambda d, s, c: find(d["delegations"], "del_presentation")["covers"].append("consequential"), None, "ERROR D-DEL", 1),
    ("choice outside its ruling's scope", lambda d, s, c: find(d["rulings"], "r_design")["scope"].remove("ch_export"), None, "ERROR D-CH4 `ch_export` cites ruling `r_design`", 1),
    ("unknown pattern", lambda d, s, c: find(d["options"], "opt_site_map").update(pattern="no_such_pattern"), None, "ERROR D-P0", 1),
    ("authoring question not in the pattern", lambda d, s, c: find(d["choices"], "ch_site_map")["settled"].append({"key": "invented_key", "answer": "x"}), None, "ERROR D-CH3", 1),
    ("authoring question left unaddressed", lambda d, s, c: find(d["choices"], "ch_site_map")["settled"].pop(0), None, "unaddressed in `ch_site_map`: crs", 0),
    ("non-use not disclosed", lambda d, s, c: find(d["non_uses"], "nu_not_qaqc").pop("disclosed_by"), None, "ERROR D-NU1 non-use `nu_not_qaqc`", 1),
    ("knowledge need neither satisfied nor a gap", drop_min_record_gap, None, "ERROR D-K1 knowledge need `k_min_record`", 1),
    ("alternative not realised", lambda d, s, c: find(d["alternatives"], "alt_stop").pop("realized_by"), None, "ERROR D-AL1 alternative `alt_stop`", 1),
    ("decision without consequence display", lambda d, s, c: find(d["decisions"], "d_sampling_plan").pop("consequences_shown_by"), None, "ERROR D-DC1", 1),
    ("decision without its disclosure", lambda d, s, c: find(d["decisions"], "d_sampling_plan").pop("decision_disclosure"), None, "ERROR D-D4 decision `d_sampling_plan`", 1),
    ("per-subject candidates labelled screen", lambda d, s, c: find(d["decisions"], "d_sampling_plan").update(app_role="screen"), None, "ERROR D-D3 decision `d_sampling_plan`", 1),
    ("recommending without adopted logic", lambda d, s, c: find(d["decisions"], "d_sampling_plan").pop("adopted_by"), None, "ERROR D-D2 decision `d_sampling_plan`: the app recommends", 1),
    ("ranking without adopted weights", lambda d, s, c: (find(d["decisions"], "d_sampling_plan").update(app_role="rank"), find(d["decisions"], "d_sampling_plan").pop("adopted_by")), None, "ERROR D-D2 decision `d_sampling_plan`: the app ranks", 1),
    ("tier differs from the specification", lambda d, s, c: s["consequence"].update(tier="T1_exploratory"), None, "ERROR D-SYNC1", 1),
    ("specification question reworded", lambda d, s, c: add_question(s, "Which wells are above the guideline?"), None, "ERROR D-SYNC2", 1),
    ("different app", lambda d, s, c: s["app"].update(id="other_app"), None, "ERROR D-SYNC3", 1),
    ("orphan view", lambda d, s, c: d["supporting"].pop(0), None, "WARN D-V1 view `txt_home_view`", 0),
    ("obligation not addressed", lambda d, s, c: find(d["obligations"], "o_confidential").pop("addressed_by"), None, "WARN D-OB1 obligation `o_confidential`", 0),
    ("obligation addressed only by a placeholder", lambda d, s, c: d["gaps"].remove(find(d["gaps"], "g_guideline_edition")), None, "WARN D-OB1 obligation `o_guideline_edition` is addressed only by placeholders", 0),
    ("need without grounds", lambda d, s, c: find(d["needs"], "n_where").pop("basis"), None, "WARN D-GR1 needs without a basis", 0),
    ("compare with a single target", lambda d, s, c: find(d["needs"], "n_where")["task"].update(query="compare", cardinality="single"), None, "ERROR D-TK1 need `n_where`", 1),
    ("evaluative need without an interpretation", lambda d, s, c: find(d["needs"], "n_exceedances").pop("interpretation"), None, "WARN D-IM1 need `n_exceedances`", 0),
    ("pattern that does not address the task", lambda d, s, c: find(d["needs"], "n_where")["task"].update(target="correlation"), None, "WARN D-P1 option `opt_site_map`", 0),
    ("made ruling without evidence", lambda d, s, c: find(d["rulings"], "r_tier").update(status="made"), None, "ERROR D-RUL ruling `r_tier`", 1),
    ("rulings recorded as made without a decision record", lambda d, s, c: mark_all_made(d, "Test fixture, not a real decision"), None, "ERROR D-RUL2 ruling `r_design`", 1),
    ("decision rules adopted without identified content", lambda d, s, c: mark_all_made(d), digests, "ERROR D-RUL5 ruling `r_decision_rules`", 1),
    ("ruling returned but marked made", all_made_with_rules, lambda d: digests(d, returned=("r_design",)), "ERROR D-RUL4 ruling `r_design`", 1),
    ("consequential choices under a delegated ruling", lambda d, s, c: (all_made_with_rules(d, s, c), find(d["rulings"], "r_design").update(authority="delegated")), digests, "ERROR D-CH7 `ch_upload` is reserved to the owner", 1),
    ("per-subject candidates traced by node id, labelled screen", lambda d, s, c: (find(d["decisions"], "d_sampling_plan").update(app_role="screen"), [a.update(realized_by=["well_screen"]) for a in d["alternatives"]]), None, "ERROR D-D3 decision `d_sampling_plan`", 1),
    ("disclosure that does not say who decides", lambda d, s, c: find(d["decisions"], "d_sampling_plan").update(decision_disclosure="nu_not_drinking_water"), None, "WARN D-D4 decision `d_sampling_plan`", 0),
    ("specialist authority label dropped", lambda d, s, c: [x.pop("authority") for x in find(d["choices"], "ch_exceedance")["settled"] if x["key"] == "comparison_rule"], None, "WARN D-CH8 `ch_exceedance.comparison_rule`", 0),
    # Resolving the gaps without answers also leaves their knowledge needs unrecorded, so D-K1 errors follow.
    ("gaps marked resolved with no answer", lambda d, s, c: [g.update(status="resolved") for g in d["gaps"]], None, "WARN D-GAP2", 1),
    ("all rulings made, with a decision record", all_made_with_rules, digests, "VERDICT: design RULED WITH OPEN GAPS", 0),
    ("specialist answers ruled by the owner", lambda d, s, c: (all_made_with_rules(d, s, c), find(d["rulings"], "r_professional_method").update(authority="owner")), digests, "awaiting a ruling by accountable_professional", 0),
]

def edit_answer(design):
    for settled in find(design["choices"], "ch_export")["settled"]:
        if settled["key"] == "format":
            settled["answer"] = "csv instead of xlsx"


def flip_gaps(design):
    """The backcheck's attack: close every gap after the rulings, and point the knowledge needs somewhere."""
    for gap in design["gaps"]:
        gap["status"] = "resolved"
    for knowledge in design["knowledge_needs"]:
        knowledge.setdefault("satisfied_by", ["tier1_groundwater"])


def change_rules_file(design):
    return {RULES_PATH: RULES_TEXT + "R2,exceeds,true,8,stop\n"}


# Cases whose decision record is computed before the edit they then make: (name, edit, expected, status).
AFTER_RULING = [
    ("answer edited after its ruling", edit_answer, "ERROR D-RUL3 ruling `r_design`", 1),
    ("gaps flipped to resolved after the rulings", flip_gaps, "ERROR D-RUL3", 1),
]


def run_after_ruling(base_design, base_spec, base_catalogue, edit):
    design, spec, catalogue = (copy.deepcopy(x) for x in (base_design, base_spec, base_catalogue))
    with_rules(design)
    mark_all_made(design)
    record_text = digests(read_roundtrip(design))
    edit(design)
    return run_case(design, spec, catalogue, record=lambda _reloaded: record_text, files={RULES_PATH: RULES_TEXT})


def run_rules_changed(base_design, base_spec, base_catalogue):
    """The rule table's bytes change after the ruling that adopted them."""
    design, spec, catalogue = (copy.deepcopy(x) for x in (base_design, base_spec, base_catalogue))
    with_rules(design)
    mark_all_made(design)
    return run_case(design, spec, catalogue, record=digests, files=change_rules_file(design))


def read_roundtrip(document):
    """The document as the checker will read it after writing."""
    return yaml.load(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), Loader=Loader)


def main():
    base_design = read(EXAMPLE / "gw-review.design.yaml")
    base_spec = read(EXAMPLE / "gw-review.appspec.yaml")
    base_catalogue = read(ROOT / "formats" / "patterns.yaml")
    failures, total = 0, 0
    results = []
    for name, mutation, record, expected, expected_status in CASES:
        design, spec, catalogue = (copy.deepcopy(x) for x in (base_design, base_spec, base_catalogue))
        mutation(design, spec, catalogue)
        files = {RULES_PATH: RULES_TEXT} if find(design["knowledge_needs"], "k_decision_rules").get("adopted_content") else None
        results.append((name, expected, expected_status) + run_case(design, spec, catalogue, record, files))
    for name, edit, expected, expected_status in AFTER_RULING:
        results.append((name, expected, expected_status) + run_after_ruling(base_design, base_spec, base_catalogue, edit))
    results.append(("decision rule file changed after adoption", "ERROR D-RUL5 ruling `r_decision_rules`", 1)
                   + run_rules_changed(base_design, base_spec, base_catalogue))
    for name, expected, expected_status, report, status in results:
        total += 1
        ok = expected in report and status == expected_status
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} {name}")
        if not ok:
            print(f"     expected {expected!r} with exit {expected_status}; got exit {status}")
            print("     " + "\n     ".join(line for line in report.splitlines() if line.startswith(("- ERROR", "- WARN", "VERDICT", "RULES", "  - "))))
    print(f"\n{total - failures} of {total} cases behaved as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
