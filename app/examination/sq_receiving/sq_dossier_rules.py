"""SQ-v0.2 dossier rules a schema cannot express (SQ-R1 to SQ-R13 and SQ-R18; SQ-R14 to SQ-R17 retired into SQ-R18).

Call after schema validation, with the step map the dossier is read against.
These inspect declared facts, not their truth.
"""
SCENARIOS = ["V4-EXM-10", "V4-EXM-11", "V4-EXM-12"]
JOURNEYS = ["J1", "J2"]
NATIVE = {"native_development", "native_packaged"}
# The closed results of a required observation, by its kind; the first is the one a definition expects.
OBSERVATION_RESULTS = {"preparation": ("arranged", "not_arranged"),
                       "independent_observation": ("equal", "differs")}
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
        # SQ-R18 a recorded journey step states only an outcome its structured facts permit
        # (permitted_outcomes; it retired SQ-R14 to SQ-R17)
        for st in s["steps"]:
            if st["state"] == "recorded" and st["outcome"] not in permitted_outcomes(ms.get(st["step"]), st):
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



def permitted_outcomes(definition, step, result=None):
    """SQ-R18: the outcomes a recorded J1 or J2 step may state, from its structured facts.

    `definition` is the step's step-map entry, `step` the dossier step and `result` its EXP result
    record where the caller has it (the receivers do; the dossier rules alone do not, and then the
    planned parts are judged by the receivers). Everything that could waive a requirement is read
    from the definition, never from what the recorder sets. Malformed facts permit nothing.

    The checks guarantee that no stated outcome is accepted that the structured facts do not
    permit, and no more. They do not judge prose.
    """
    attempted_outcomes = frozenset(ATTEMPTED)
    if definition is None:
        return frozenset()
    planned = {p["part"]: p for p in definition.get("parts", [])}
    if result is not None:
        # Every planned part is carried with its own outcome, none set aside or marked not native.
        parts = {p["part"]: p for p in result.get("parts", [])}
        set_aside = {p["part"] for p in result.get("parts_not_applicable", [])}
        if (set(parts) != set(planned) or len(parts) != len(result.get("parts", [])) or set_aside & set(planned)
                or any(planned[n].get("needs_native") and parts[n].get("needs_native") is False for n in parts)):
            return frozenset()
    op = step.get("operation")
    # 1. Not attempted: no one operated it.
    if op is None:
        return frozenset({"not-run"})
    required = {o["id"]: o for o in definition.get("required_observations", [])}
    recorded = {}
    for o in op.get("observations", []):
        defined = required.get(o["id"])
        if defined is None or o["id"] in recorded:
            return frozenset()
        if o["status"] == "made" and o.get("result") not in OBSERVATION_RESULTS[defined["kind"]]:
            return frozenset()
        recorded[o["id"]] = o
    contradicted = unresolved = False
    for oid, defined in required.items():
        o = recorded.get(oid)
        if o is None or o["status"] != "made":
            unresolved = True                       # not made: the step could not be evaluated
        elif o["result"] != defined["expected"]:
            if defined["kind"] == "independent_observation":
                contradicted = True                 # made, and what the App did differs: not met
            else:
                unresolved = True                   # a preparation not arranged stops the step
    if result is not None:
        route = result["configuration"]["route"]["kind"]
        for name, part in parts.items():
            # EXP-R4's evidence rule, applied because the definition marks the part native
            native = {e.get("route", route) for e in part.get("evidence", [])} & NATIVE
            if part["outcome"] == "fail":
                contradicted = True
            elif part["outcome"] != "pass" or (planned[name].get("needs_native") and not native):
                unresolved = True
    # 2. An interface gap is an interface failure.
    if op["interface_gaps"]:
        return frozenset({"fail"})
    # A contradicted observation or a failed part: evaluated and not met.
    if contradicted:
        return frozenset({"fail"})
    # 3. An examination limit, or anything unresolved: stopped (blocked) or insufficient (inconclusive).
    if op["examination_limits"] or unresolved:
        return frozenset({"blocked", "inconclusive"})
    # 4. Everything the definition requires holds; pass needs the App's own controls as well.
    if op["means"] == "not_through_app_controls":
        return attempted_outcomes - {"pass"}
    return attempted_outcomes
