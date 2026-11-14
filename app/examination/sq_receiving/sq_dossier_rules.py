"""SQ-v0.2 dossier rules a schema cannot express (SQ-R1 to SQ-R13 and SQ-R18; SQ-R14 to SQ-R17 retired into SQ-R18).

Call after schema validation, with the step map the dossier is read against.
These inspect declared facts, not their truth. Steps the step map takes out of the release the dossier
names ("out_of_release", for that release only) stay listed and are never counted (SQ-R3, SQ-R4, SQ-R8).
"""
SCENARIOS = ["V4-EXM-10", "V4-EXM-11", "V4-EXM-12"]
JOURNEYS = ["J1", "J2"]
NATIVE = {"native_development", "native_packaged"}
NOT_CLAIMED = {"joined_host_witness", "replacement", "public_release", "retirement",
               "professional_reliance", "practitioner_validation"}
# Run B's steps for the local model server (DEL-09-02's scope): the local key, its configuration, and
# one conversation with each mode with the switch between them.
LOCAL_STEPS = {"M12-2", "M12-3", "M12-5"}


def out_of_release(step_map, release):
    """The steps the step map takes out of the release named, by scenario, from its "out_of_release" entry.

    The positive evidence is a decision recorded in the step map for exactly that release (its "release"
    equal to the one named, as the dossier names it). With no release named, or no decision for it, no step
    is taken: every step counts. A taken step stays listed in its scenario and is never counted: it is not
    aggregated and need not be recorded.
    """
    taken = {}
    if not isinstance(release, str) or not release:
        return taken
    for scenario, decision in step_map.get("out_of_release", {}).items():
        if not isinstance(decision, dict) or decision.get("release") != release:
            continue
        named = decision.get("steps")
        taken[scenario] = set(named) if named else {s["step"] for s in step_map["scenarios"].get(scenario, [])}
    return taken


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
    taken = out_of_release(step_map, d.get("release"))

    def counted(scenario, step):
        return step.get("counts", True) and step["step"] not in taken.get(scenario["scenario"], ())
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
        # SQ-R3 the declared access modes (not observations), each in the home the scope defines for it,
        # with distinct conversations. With the local model server's steps out of the release, the one
        # mode is the ChatGPT account; with none of them out, the two modes; a map taking only some of
        # them out declares no mode that can be met. An observed difference is a failed M12 step in its
        # result record, not a changed declaration.
        local_out = LOCAL_STEPS & taken.get("V4-EXM-12", set())
        if local_out == LOCAL_STEPS:
            wrong = kinds != ["chatgpt_account"] or homes.get("chatgpt_account") != "H-acct" or len(convs) != 1
        else:
            wrong = (bool(local_out) or kinds != ["chatgpt_account", "local_provider"]
                     or homes.get("chatgpt_account") != "H-acct" or homes.get("local_provider") != "H-omlx"
                     or len(set(convs)) != 2)
        if wrong:
            v.append("SQ-R3")
    # SQ-R4 a scenario outcome only once every counted step is recorded; it is their aggregate
    for s in d["scenarios"]:
        steps = [st for st in s["steps"] if counted(s, st)]
        if "outcome" in s:
            if any(st["state"] != "recorded" for st in steps) or aggregate([st["outcome"] for st in steps]) != s["outcome"]:
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
        all_recorded = all(st["state"] == "recorded" for s in d["scenarios"] for st in s["steps"] if counted(s, st))
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
        # SQ-R18 a journey step is not accepted as passed when its recorded facts forbid it
        # (pass_forbidden; it retired SQ-R14 to SQ-R17)
        for st in s["steps"]:
            if st["state"] == "recorded" and st["outcome"] == "pass" and pass_forbidden(ms.get(st["step"]), st):
                v.append("SQ-R18")
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




def pass_forbidden(definition, step, result=None):
    """SQ-R18: the reasons a recorded J1 or J2 step's facts forbid "pass"; empty when they do not.

    `definition` is the step's step-map entry, `step` the dossier step and `result` its EXP result
    record where the caller has it (the receivers do; the dossier rules alone do not). Every
    requirement is read from the definition, never from what the recorder sets. It prescribes
    nothing among fail, blocked and inconclusive: which of those a record states is DEL-09-01's
    aggregate of its parts, and whether it is right is the independent reviewer's (VER-007).
    """
    if definition is None:
        return ["step not defined in the step map"]
    op = step.get("operation")
    if op is None:
        return ["not attempted"]
    reasons = []
    if op["interface_gaps"]:
        reasons.append("interface gap recorded")
    if op["examination_limits"]:
        reasons.append("examination limit recorded")
    if op["means"] == "not_through_app_controls":
        reasons.append("not performed through the App's controls")
    required = {o["id"]: o for o in definition.get("required_observations", [])}
    recorded = {}
    for o in op.get("observations", []):
        if o["id"] not in required:
            reasons.append("observation not in the definition: " + o["id"])
        elif o["id"] in recorded:
            reasons.append("observation recorded twice: " + o["id"])
        recorded.setdefault(o["id"], o)
    for oid, defined in required.items():
        o = recorded.get(oid)
        if o is None:
            reasons.append("required observation missing: " + oid)
        elif o["status"] != "made":
            reasons.append("required observation not made: " + oid)
        elif o.get("result") != defined["expected"] or not str(o.get("evidence", "")).strip():
            reasons.append("required observation not as expected: " + oid)
    if result is not None:
        planned = {p["part"]: p for p in definition.get("parts", [])}
        parts = result.get("parts", [])
        names = [p["part"] for p in parts]
        set_aside = {p["part"] for p in result.get("parts_not_applicable", [])}
        for name in planned:
            if names.count(name) != 1:
                reasons.append("planned part missing or repeated: " + name)
            if name in set_aside:
                reasons.append("planned part set aside: " + name)
        route = result["configuration"]["route"]["kind"]
        for part in parts:
            defined = planned.get(part["part"])
            if defined is None:
                reasons.append("part not in the definition: " + part["part"])
            elif defined.get("needs_native"):
                if part.get("needs_native") is False:
                    reasons.append("native part marked not native: " + part["part"])
                # EXP-R4's evidence rule, applied because the definition marks the part native
                if part["outcome"] == "pass" and not {e.get("route", route) for e in part.get("evidence", [])} & NATIVE:
                    reasons.append("part passed without native evidence: " + part["part"])
    return reasons
