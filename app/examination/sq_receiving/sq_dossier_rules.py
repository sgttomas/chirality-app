"""SQ-v0.2 dossier rules a schema cannot express (SQ-R1 to SQ-R10).

Call after schema validation, with the step map the dossier is read against.
These inspect declared facts, not their truth.
"""
SCENARIOS = ["V4-EXM-10", "V4-EXM-11", "V4-EXM-12"]
NOT_CLAIMED = {"joined_host_witness", "replacement", "public_release", "retirement",
               "professional_reliance", "practitioner_validation"}


def known_cases(step_map):
    """The supplier cases the step map declares, as (deliverable, file, case_id)."""
    return {(c["deliverable"], c["file"], c["case_id"])
            for steps in step_map["scenarios"].values() for s in steps for c in s["supplier_cases"]}


def aggregate(outs):
    if "fail" in outs:
        return "fail"
    if "blocked" in outs:
        return "blocked"
    if outs and all(o == "pass" for o in outs):
        return "pass"
    if all(o == "not-run" for o in outs):
        return "not-run"
    return "inconclusive"


def map_steps(step_map):
    return {s["step"]: s for v in step_map["scenarios"].values() for s in v}


def violations(d, step_map):
    v = []
    ms = map_steps(step_map)
    names = [s["scenario"] for s in d["scenarios"]]
    if sorted(names) != SCENARIOS:
        v.append("SQ-R1")
    by = {s["scenario"]: s for s in d["scenarios"]}
    if "V4-EXM-10" in by and "V4-EXM-11" in by and by["V4-EXM-10"]["run_ref"] != by["V4-EXM-11"]["run_ref"]:
        v.append("SQ-R2")
    m12 = by.get("V4-EXM-12")
    if m12:
        modes = m12.get("access_modes", [])
        kinds = sorted(m["kind"] for m in modes)
        homes = {m["kind"]: m["home"] for m in modes}
        convs = [m["conversation_ref"] for m in modes]
        # SQ-R3 the declared access modes (not observations): exactly the two modes, each in the
        # home the scope defines for it, with distinct conversations. An observed difference is a
        # failed M12 step in its result record, not a changed declaration.
        if (kinds != ["chatgpt_account", "local_provider"] or homes.get("chatgpt_account") != "H-acct"
                or homes.get("local_provider") != "H-omlx" or len(set(convs)) != 2):
            v.append("SQ-R3")
    # SQ-R4 a scenario outcome only once every counted step is recorded; it is their aggregate
    for s in d["scenarios"]:
        counted = [st for st in s["steps"] if st.get("counts", True)]
        if "outcome" in s:
            if any(st["state"] != "recorded" for st in counted) or aggregate([st["outcome"] for st in counted]) != s["outcome"]:
                v.append("SQ-R4")
                break
    if not NOT_CLAIMED <= set(d["handoff"]["not_claimed"]):
        v.append("SQ-R5")
    # SQ-R6 every supplier case a step cites is one the step map declares
    known = known_cases(step_map)
    for s in d["scenarios"]:
        for st in s["steps"]:
            if any((c["deliverable"], c["file"], c["case_id"]) not in known for c in st["supplier_cases"]):
                v.append("SQ-R6")
                break
    for s in d["scenarios"]:
        want = [x["step"] for x in step_map["scenarios"].get(s["scenario"], [])]
        if [st["step"] for st in s["steps"]] != want:
            v.append("SQ-R7")
            break
    # SQ-R8 handover as qualification, and independence
    h = d["handoff"]
    if h["handed_over"]:
        all_recorded = all(st["state"] == "recorded" for s in d["scenarios"] for st in s["steps"] if st.get("counts", True))
        if not all_recorded or any("outcome" not in s for s in d["scenarios"]) or not d["examiner"].get("review_record"):
            v.append("SQ-R8")
    if h["reported_as_independent"] and (d["examiner"]["separation"] == "not_separate" or not d["examiner"].get("review_record")):
        v.append("SQ-R8")
    # SQ-R9 stimuli: a recorded counted step lists every stimulus its map declares; one not produced cannot pass
    for s in d["scenarios"]:
        for st in s["steps"]:
            if st["state"] != "recorded" or not st.get("counts", True):
                continue
            declared = set(ms.get(st["step"], {}).get("stimuli", []))
            given = {x["id"]: x for x in st.get("stimuli", [])}
            no_replay = {x["id"] for x in step_map["stimuli"] if not x.get("replay_counterpart")}
            if (declared - set(given)
                    or any(x["produced"] == "replay" and i in no_replay for i, x in given.items())
                    or (any(x["produced"] == "not_produced" for x in given.values())
                        and st["outcome"] not in ("blocked", "fail"))):
                v.append("SQ-R9")
                break
    # SQ-R10 a counted step's map entry carries counts consistently
    for s in d["scenarios"]:
        for st in s["steps"]:
            if st["step"] in ms and st.get("counts", True) != ms[st["step"]]["counts"]:
                v.append("SQ-R10")
                break
    return sorted(set(v))
