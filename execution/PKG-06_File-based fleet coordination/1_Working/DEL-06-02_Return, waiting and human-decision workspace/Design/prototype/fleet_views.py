"""DEL-06-02 return-review queue and waiting views (FLEET_VIEWS.md FV-v0.1 §3, §4). Prototype, not product code.

Python 3 standard library. Consumes DEL-06-01's reader (fleet_store.Reader, FR-v0.1 §6; DEP-06-02-008), whose
facts carry connector needs read by RF-5a from DEL-07-02's standing records (CFB-v0.1 §2; DEP-07-02-015);
FV-10 words them. Derives rows and writes nothing (FV-9). Each row carries the source
records it rests on, so a person can open the evidence behind every statement (V4-PM-06).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
DEL_06_01_PROTO = os.path.join(DESIGN, "..", "..", "DEL-06-01_Bounded delegation and current work-graph records",
                               "Design", "prototype")
sys.path.insert(0, os.path.normpath(DEL_06_01_PROTO))
from fleet_store import Reader  # noqa: E402

def owner_label(o):
    who = o.get("identity", "owner not named")
    if o.get("kind") == "person" and not o.get("identityVerified", False):
        who += " (identity not verified)"
    return who


def examiner_owner(f, reader):
    """FV-2: who examines the return: the brief's preparer, as the brief records it. With no brief, no examiner is
    invented: the graph's item owner is usually the executor (FV-2a), so it is not used as a fallback."""
    if f["brief"] and f["brief"]["brief"] in reader.briefs:
        return owner_label(reader.briefs[f["brief"]["brief"]][0]["body"]["preparedBy"]) + " (prepared the brief)"
    return "examiner not established"


def queue(facts, reader):
    """FV-1...FV-3: returned work awaiting examination or integration; nothing enters without a return record."""
    rows = []
    for f in facts["items"]:
        r = f["return"]
        if not r or f["integration"]:
            continue
        if f["review"] is None:
            state = "awaiting review"
        elif f["review"]["verdict"] == "findings to repair":
            state = "reviewed — findings to repair"
        elif f["review"]["verdict"] == "not concluded":
            state = "review not concluded"
        else:
            state = "reviewed — awaiting integration"
        rows.append({"item": f["itemId"], "outcome": f["outcome"], "state": state,
                     "returnedBy": r["by"], "recordedBy": r["recordedBy"],
                     "examiner": f["review"]["by"] if f["review"] else None,
                     "examines": examiner_owner(f, reader),
                     "sources": [x for x in (r["source"], f["review"] and f["review"]["source"]) if x]})
    return rows


def waiting(facts, root=None):
    """FV-4...FV-8, FV-10: every selected, not-done item with the cause its records evidence, or an explicit gap."""
    rows = []
    for f in facts["items"]:
        if not f["selected"]:
            continue
        done = f["integration"] or f["external"]
        causes, sources = [], []
        if done:
            category = "done"
            causes.append("integrated" if f["integration"] else f"external result ({f['external']['owner']})")
            sources.append(f["integration"]["source"] if f["integration"] else "external_result")
        else:
            outstanding = [n for n in f["needs"] if n["state"] == "outstanding"]
            unknown = [n for n in f["needs"] if n["state"] == "unknown"]
            for n in outstanding:
                k = n["need"]["kind"]
                if k == "item":
                    causes.append(f"waits for {n['need']['ref']} ({n['why']})")
                elif k == "decision":
                    causes.append(f"waits for the person's decision: {n['why']}")
                elif n.get("connector"):
                    causes.append(f"waits on {n['why']}")
                    sources.append(n["record"])
                else:
                    causes.append(f"waits for input {n['need']['ref']} ({n['why']})")
            for n in unknown:
                causes.append(f"cause not established: {n['need']['kind']} {n['need']['ref']} ({n['why']})")
                if n.get("connector"):
                    sources.append(n["record"])
            for n in f["needs"]:
                if n["state"] == "satisfied" and n.get("connector"):
                    causes.append(n["why"])
                    sources.append(n["record"])
            for n in f["needs"]:
                if n["state"] == "satisfied" and n["need"]["kind"] == "decision":
                    # FV-6: the decision is shown as recorded; what the chosen alternative implies is not interpreted here.
                    causes.append(f"decision recorded: {n['why']}")
            if f["return"]:
                category = "returned"
                causes.append("in the return queue" if not f["review"] else f"review: {f['review']['verdict']}")
            elif f["dispatch"] and f["dispatch"]["state"] == "dispatch observed":
                last = f["observed"][-1] if f["observed"] else None
                if last and "ended" in last:
                    category = "unknown"
                    causes.append(f"observation ended ({last['ended']}); last observed {last['lastObserved']!r}; outcome unknown")
                elif last and last.get("status") == "completed":
                    category = "unknown"
                    causes.append("Codex reports the child completed; no return recorded")
                elif last:
                    category = "in progress"
                    causes.append(f"Codex reports {last['status']!r} ({last['source']})")
                else:
                    category = "in progress"
                    causes.append("dispatched; no status observed since")
            elif outstanding:
                category = "waiting"
            elif unknown:
                category = "unknown"
            elif f["owner"]["kind"] == "external":
                category = "waiting"
                causes.append(f"waits for the external owner {owner_label(f['owner'])}; no result recorded")
            elif f["brief"] and f["brief"]["state"] != "prepared":
                category = "unknown"
                causes.append(f"brief {f['brief']['brief']} named in the graph but not readable; dispatch cannot be established")
            elif f["brief"] and f["brief"]["state"] == "prepared":
                category = "ready"
                causes.append("ready: inputs satisfied, brief prepared, no dispatch observed")
            else:
                category = "ready"
                causes.append("ready: inputs satisfied")
            if f["related"]:
                causes.append("related conversation: " + ", ".join(f"{r['thread']} ({r['relation']} {r['source']})" for r in f["related"]))
        if f["basisChanged"] and not done:
            causes.append("basis changed since: " + ", ".join(f["basisChanged"]))
        qualified = False
        if not done and facts.get("logIncomplete"):
            # FV-8a (RV E2-R1): an unread log line could be any record of any item; no not-done row keeps a state.
            causes = [f"coordination log incomplete: line(s) {facts['logIncomplete']} unread; this item's state cannot be "
                      f"established"] + [f"readable records show: {c}" for c in causes]
            category = "unknown"
        unassociated = [c["child"] for c in facts.get("childIndex", []) if c["brief"] is None] + list(facts.get("orphanChildren", []))
        if category == "ready" and unassociated:
            # FV-4a (RV E2-R3): a child spawned without a brief reference may be doing this item.
            # FV-4a (RV E2-R4): the qualifier is in the label and is the first cause, so no display shows a bare "ready".
            causes.insert(0, f"{len(unassociated)} child(ren) observed without a brief reference or dispatch record "
                             f"({', '.join(unassociated)}); a dispatch for this item may be unrecorded")
            category = "ready (qualified)"
            qualified = True
        rows.append({"item": f["itemId"], "outcome": f["outcome"], "category": category,
                     "owner": owner_label(f["owner"]), "causes": causes, "sources": sources,
                     "readinessQualified": qualified})
    return rows


def build(root, rs_records=None):
    reader = Reader(root, rs_records)
    facts = reader.item_facts("FX-U1")
    return {"views": "return-review queue and waiting (DEL-06-02; derived, not authority)",
            "graph": facts.get("graph"), "revision": facts.get("revision"),
            "queue": queue(facts, reader),
            # FV-8a: the queue is complete only if every coordination-log line was read and no observation is orphaned.
            "queueComplete": not facts.get("logIncomplete") and not facts.get("orphanChildren") and "items" in facts and bool(facts["items"]),
            "waiting": waiting(facts, root),
            "notes": facts["notes"], "limits": facts["limits"]}
