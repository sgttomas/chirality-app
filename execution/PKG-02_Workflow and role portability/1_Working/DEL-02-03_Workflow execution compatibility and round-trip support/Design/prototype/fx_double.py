"""Test-double catalog and fixture workflows built from C-v0.7 §10 (FX-PIPE-01)
and WD-EX-v0.7 E1, E1c, E1d, E5, E6, E7, E8.

Design prototype for DEL-02-03 (EXEC-v0.6 §3.3-§3.6). Not product code. All
material is invented fixture subject matter; labels are fixture labels, not
operation identities, wire names or SWBPIPE commitments.
"""

import copy

# C §10.2 entries (edition e2). Class values are C §3.1's; exposure per FXA-1.
_E2 = {
    "OP-C1": {"version": "v1", "class": "none"},
    "OP-C2": {"version": "v1", "class": "none",
              "preconditions": [("a current solve exists",
                                 "No current solve for LC-1 at this revision")]},
    "OP-C3": {"version": "v1", "class": "none"},
    "OP-C4": {"version": "v1", "class": "may apply within granted autonomy"},
    "OP-C5": {"version": "v1", "class": "may apply within granted autonomy"},
    "OP-C6": {"version": "v1", "class": "reserved to the person"},
    "OP-C7": {"version": "v1", "class": "reserved to the person"},
    "OP-C8": {"version": "v1", "class": "reserved to the person"},
    "OP-C9": {"version": "v1", "class": "may apply within granted autonomy"},
    "OP-C10": {"version": "v1", "class": "policy of the reversed operation"},
    "OP-C11": {"version": "v1", "class": "no policy basis"},
    "OP-C12": {"version": "v1", "class": "none"},
}
for _e in _E2.values():
    _e["exposure"] = {"H": "exposed", "E": "exposed", "X": "exposed"}  # FXA-1
    _e.setdefault("preconditions", [])


def catalog(edition="e2", variants=(), revision="r12", readable=True):
    """Return a catalog double: {edition, readable, revision, entries}."""
    entries = copy.deepcopy(_E2)
    if edition == "e1":                      # C §10.1: e1 is e2 without OP-C9
        del entries["OP-C9"]
    v = set(variants)
    if "V-X1" in v:                          # C §10.4 V-X1
        entries["OP-C9"]["exposure"]["X"] = "not exposed"
    if "OP-C4-absent" in v:                  # WD-EX E7 L-WDEX-13
        del entries["OP-C4"]
    if "OP-C5-absent" in v:                  # EXEC L-EXEC-26
        del entries["OP-C5"]
    if "OP-C1-v2" in v:                      # C §10.5 hypothetical; EXEC L-EXEC-2
        entries["OP-C1"]["version"] = "v2"
    # T8 (C §10.6): at r13 there is no current solve for LC-1.
    no_solve = revision == "r13"
    return {"edition": edition, "readable": readable, "revision": revision,
            "no_current_solve": no_solve, "entries": entries}


def _req(ref, necessity="required", version="v1", cls="host_operation", purpose=""):
    return {"reference": ref, "class": cls, "necessity": necessity,
            "declared_versions": [version] if version else [], "purpose": purpose}


_ID = lambda name, rev, origin="project", root="fx-proj": {
    "kind": "workflow", "origin": origin, "source_root": root, "name": name,
    "revision": rev}

# WD-EX E1 (checkpoints with held actions, WD §4.3.1; R6-1).
_CP_ACCEPT = {"name": "CP-accept", "required_act": "A5", "reached_when_kind": "c",
              "subject_class": "change items of a named proposal",
              "held_actions": {"form": "absent_derived", "app_side": False},
              "valid": True}
_CP_CHECK_E1 = {"name": "CP-check", "required_act": "A4", "reached_when_kind": "b",
                "subject_class": "objects changed by a named outcome",
                "held_actions": {"form": "listed_steps", "app_side": True},
                "valid": True}
_CP_CHECK_E1C = {"name": "CP-check", "required_act": "A4", "reached_when_kind": "c",
                 "subject_class": "objects changed by a named outcome",
                 "held_actions": {"form": "listed_steps", "app_side": True},
                 "valid": True}
_CP_GRANT = {"name": "CP-grant", "required_act": "A12", "reached_when_kind": "a",
             "subject_class": "grant setting",
             "held_actions": {"form": "host_operations_only", "app_side": False},
             "valid": True}

_E1_REQS = [
    _req("OP-C1", purpose="read supports on the run"),
    _req("OP-C3", purpose="examine spacing against the limit (A3 findings)"),
    _req("OP-C12", necessity="optional",
         purpose="run the host's named support-spacing check (fallback: report host check not run)"),
    _req("OP-C4", purpose="propose added supports"),
    _req("OP-C5", necessity="optional",
         purpose="propose stiffness changes (fallback: propose added supports only)"),
]


def workflow(name):
    """Fixture declared parts keyed by the EXEC case that uses them."""
    wf = {"declared_part_status": "declared", "required_tools_category": "declared",
          "requirements": [], "checkpoints": [], "delegation_needed": False,
          "compatible_roles": ["TASK", "WORKING_ITEMS"]}
    if name in ("E1-rev-3", "E1-rev-A2", "E1-rev-A2g"):
        rev = {"E1-rev-3": "rev-3", "E1-rev-A2": "rev-A2", "E1-rev-A2g": "rev-A2g"}[name]
        origin, root = ("host", "fx-root") if rev == "rev-3" else ("project", "fx-proj")
        wf.update(identity=_ID("supports-adjust", rev, origin, root),
                  requirements=copy.deepcopy(_E1_REQS),
                  checkpoints=[copy.deepcopy(_CP_ACCEPT), copy.deepcopy(_CP_CHECK_E1)])
        if name == "E1-rev-A2g":               # L-EXEC-33: CP-accept declared governed
            wf["checkpoints"][0]["governed"] = True
    elif name == "E1c":
        wf.update(identity=_ID("supports-label", "rev-C1"),
                  requirements=[_req("OP-C9", purpose="label a support")],
                  checkpoints=[copy.deepcopy(_CP_CHECK_E1C)])
    elif name == "E1d":
        wf.update(identity=_ID("label-with-grant", "rev-D1"),
                  requirements=[_req("OP-C9", purpose="label a support")],
                  checkpoints=[copy.deepcopy(_CP_GRANT), copy.deepcopy(_CP_CHECK_E1C)])
    elif name == "E1d-harness-grant":          # L-EXEC-6 (MT-15)
        wf.update(identity=_ID("label-with-grant", "rev-D1h"),
                  requirements=[_req("OP-C9", purpose="label a support"),
                                _req("shell command", cls="harness_capability", version=None,
                                     purpose="run a shell command")],
                  checkpoints=[dict(copy.deepcopy(_CP_GRANT), held_on_harness=True,
                                    held_actions={"form": "host_operations_only", "app_side": True}),
                               copy.deepcopy(_CP_CHECK_E1C)])
    elif name == "E1-OP-C1-v1":                # L-EXEC-2 (MT-7)
        wf = workflow("E1-rev-3")
    elif name == "E1-harness-file-writing":    # L-EXEC-3 (MT-8)
        wf = workflow("E1-rev-3")
        wf["requirements"].append(_req("file writing", cls="harness_capability", version=None,
                                       purpose="write the summary file"))
    elif name == "requires-OP-C2":             # MT-6 (C §10.6 T8)
        wf.update(identity=_ID("results-review", "rev-R1"),
                  requirements=[_req("OP-C2", purpose="read sustained-load results")])
    elif name == "requires-OP-C11":            # MT-13 (C V-NP1)
        wf.update(identity=_ID("renumber", "rev-N1"),
                  requirements=[_req("OP-C11", purpose="renumber nodes")])
    elif name == "E5":                         # WD-EX E5: prose only
        wf.update(identity=_ID("create-workflow", "rev-root", "bundled", "chirality-root"),
                  declared_part_status="undeclared", required_tools_category="undeclared")
    elif name == "E6":                         # WD-EX E6: restriction, delegation need
        wf.update(identity=_ID("project-dag", "rev-root", "bundled", "chirality-root"),
                  required_tools_category="undeclared", delegation_needed=True,
                  compatible_roles=["WORKING_ITEMS"])
    else:
        raise KeyError(name)
    return wf
