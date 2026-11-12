"""SQ-v0.2 dossier rules a schema cannot express (SQ-R1 to SQ-R17).

Call after schema validation, with the step map the dossier is read against.
These inspect declared facts, not their truth.
"""
SCENARIOS = ["V4-EXM-10", "V4-EXM-11", "V4-EXM-12"]
JOURNEYS = ["J1", "J2"]
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
    if sorted(n for n in names if n not in JOURNEYS) != SCENARIOS:
        v.append("SQ-R1")
    # SQ-R11 the two journeys, each once, beside the three scenarios (DEL-09-02 AC-007)
    if sorted(n for n in names if n in JOURNEYS) != JOURNEYS:
        v.append("SQ-R11")
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
    for s in d["scenarios"]:
        journey = s["scenario"] in JOURNEYS
        # SQ-R12 a journey step states who operated it and by what means exactly when it was attempted;
        # a not-run or unrecorded step, and a step of another scenario, states no operation
        if any(("operation" in st) != (journey and attempted(st)) for st in s["steps"]):
            v.append("SQ-R12")
        if not journey:
            continue
        tried = [st for st in s["steps"] if attempted(st)]
        # SQ-R13 the journey's basis is the one its attempted steps give (journey_basis)
        if s.get("basis") != journey_basis(tried):
            v.append("SQ-R13")
        for st in tried:
            op = st.get("operation", {})
            # SQ-R14 a journey action not done through the App's controls is never a passed step
            if op.get("means") == "not_through_app_controls" and st["outcome"] == "pass":
                v.append("SQ-R14")
            # SQ-R15 what the App's window did not give a user fails the step; it cannot pass
            if op.get("interface_gaps") and st["outcome"] == "pass":
                v.append("SQ-R15")
            # SQ-R16 what the examination could not perceive or operate leaves the step unpassed
            if op.get("examination_limits") and st["outcome"] == "pass":
                v.append("SQ-R16")
            # SQ-R17 a passed step lists each outside-the-controls kind its map requires (the
            # preparation or independent observation the step's observation rests on)
            need = set(ms.get(st["step"], {}).get("outside_controls_required", []))
            if st["outcome"] == "pass" and need - {x["kind"] for x in op.get("outside_controls", [])}:
                v.append("SQ-R17")
    return sorted(set(v))


ATTEMPTED = ("pass", "fail", "blocked", "inconclusive")


def attempted(st):
    """A recorded step whose outcome shows an attempt (DEL-09-01: blocked was attempted; not-run was not)."""
    return st["state"] == "recorded" and st.get("outcome") in ATTEMPTED


def journey_basis(tried):
    """The basis a journey's attempted steps give (SQ-R13)."""
    ops = [st.get("operation") for st in tried]
    def by_agent(op):
        return (op["operator"]["kind"] == "agent" or op["means"] == "app_controls_by_computer_use"
                or any(i["kind"] == "operated_control" and i["actor"]["kind"] == "agent" for i in op["interventions"]))
    if any(op and by_agent(op) for op in ops):
        return "agent_operated"
    def by_person_alone(op):
        return (op["operator"]["kind"] == "person" and op["means"] == "app_controls_by_hand"
                and not any(i["kind"] in ("operated_control", "explained_control") for i in op["interventions"]))
    if ops and all(op and by_person_alone(op) for op in ops):
        return "person_observed"
    return "not_established"
