"""DEL-06-02 decision view, derived from files only (prototype; DECISION_VIEW.md DV-1...DV-9).

Prototype only, not product code. Python 3 standard library. It reads an RS record
log and the package files the records cite; it writes nothing (DV-9). The rules it
implements are DEL-06-02 Design/DECISION_VIEW.md §3; the comments cite them.

Usage: python3 decision_view.py <input-set root> [<records path relative to root> ...]
"""

import hashlib
import json
import os
import sys

PERSON_WORDING = "identity not verified"


def file_identity(root, ref):
    """TEST VALUE identity of an App file (method unselected, RS U-04), or None if absent."""
    path = os.path.join(root, ref)
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as fh:
        return "sha256:" + hashlib.sha256(fh.read()).hexdigest()


def read_log(path):
    """Entries in written order. A line that does not parse is kept as a limit, never used (RS §3 record states)."""
    entries, limits = [], []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                limits.append(f"{os.path.basename(path)} line {n}: partial entry (not read)")
    return entries, limits


def person_label(p):
    names = [p.get(k) for k in ("displayName", "osAccount", "codexAccount", "hostActor") if p.get(k)]
    who = " / ".join(names) if names else "person not named"
    return who if p.get("identityVerified") else f"{who} ({PERSON_WORDING})"


def derive(root, record_paths):
    entries, limits = [], []
    for rp in record_paths:
        e, l = read_log(os.path.join(root, rp))
        entries += e
        limits += l
    by_id = {e.get("recordId"): e for e in entries}
    # DV-1: a row per act_request that carries alternatives (a decision package); other requests are not packages.
    packages = [e for e in entries if e.get("kind") == "act_request" and "alternatives" in e.get("body", {})]
    acts = [e for e in entries if e.get("kind") == "human_act"]
    rows = []
    for p in packages:
        b = p["body"]
        pid = p["recordId"]
        alt_ids = [a["id"] for a in b["alternatives"]]
        row = {
            "package": pid,
            "packageFile": b["evidence"]["ref"],
            "actRequested": b["actKind"],
            "subject": b["subject"],
            "purpose": b["purpose"],
            "scope": b.get("scope"),
            "requestedBy": b["requester"].get("identity", b["requester"]["kind"]),
            "alternatives": [{"id": a["id"], "statement": a["statement"],
                              "consequences": [c["statement"] for c in b["consequences"] if c["alternative"] == a["id"]]}
                             for a in b["alternatives"]],
            "state": "pending — awaiting the person's decision",
            "decision": None,
            "limits": [],
        }
        # DV-2: package-internal checks (reader rules; the schema cannot see them).
        if len(set(alt_ids)) != len(alt_ids):
            row["limits"].append("alternative identities repeat within the package")
        orphans = sorted({c["alternative"] for c in b["consequences"]} - set(alt_ids))
        if orphans:
            row["limits"].append(f"consequences name no alternative of the package: {orphans}")
        missing = [a for a in alt_ids if not any(c["alternative"] == a for c in b["consequences"])]
        if missing:
            row["limits"].append(f"no consequence stated for: {missing}")
        # DV-3: the package file now, against what the request recorded.
        now = file_identity(root, b["evidence"]["ref"])
        recorded = b["evidence"].get("claimedIdentity")
        if now is None:
            row["limits"].append("package file not available: its current content is unknown")
        elif recorded and now != recorded:
            row["limits"].append("package file differs from the content the request recorded")
        # DV-4: a decision is a human_act of the named kind citing this request; nothing else counts.
        citing = [a for a in acts if a["body"].get("relations", {}).get("requestRef") == pid]
        decided = []
        for a in citing:
            ab = a["body"]
            if ab["actKind"] != b["actKind"]:
                row["limits"].append(f"{a['recordId']}: an act of kind {ab['actKind']} cites this package; "
                                     f"it is not the {b['actKind']} the package requests")
                continue
            chosen = ab.get("relations", {}).get("alternativeChosen")
            if b["actKind"] == "A16" and chosen not in alt_ids:
                # DV-5: not counted; shown with its rule.
                row["limits"].append(f"{a['recordId']}: act not counted: chosen alternative {chosen!r} is not one the package names")
                continue
            decided.append(a)
        if decided:
            a = decided[-1]  # DV-6: the latest in written order; earlier ones stay listed.
            ab = a["body"]
            chosen = ab.get("relations", {}).get("alternativeChosen")
            bound = ab["boundContent"][0].get("value")
            # DV-7: lapse against the package file (RS §7 L-1 for an App file; L-3, L-6).
            if now is None:
                lapse = "unknown (unavailable)"
            elif now == bound:
                lapse = "not lapsed"
            else:
                lapse = "lapsed — the package changed after the decision"
            row["state"] = "decided"
            row["decision"] = {
                "act": a["recordId"],
                "actKind": ab["actKind"],
                "alternativeChosen": chosen,
                "statement": next((x["statement"] for x in b["alternatives"] if x["id"] == chosen), None),
                "decidedBy": person_label(ab["decisionActor"]),
                "recordedBy": f"{a['recorder']['role']} {a['recorder']['identity']}",
                "recordingMode": ab["recordingMode"],
                "captureEvidence": [c["ref"] for c in ab["captureEvidence"]],
                "capturedAt": ab["captureTime"],
                "lapse": lapse,
                "earlierActs": [x["recordId"] for x in decided[:-1]],
            }
        rows.append(row)
    # §6: an act citing a request the log does not hold is listed as a view limit, on no row.
    for a in acts:
        ref = a["body"].get("relations", {}).get("requestRef")
        if ref and by_id.get(ref, {}).get("kind") != "act_request":
            limits.append(f"{a['recordId']}: cites request {ref}, which this record set does not hold")
    # DV-8: what the view does not read is not evidence (conversation text, native status).
    return {"view": "decision packages (DEL-06-02; derived, not authority)", "rows": rows, "limits": limits}


def main():
    root = sys.argv[1]
    recs = sys.argv[2:] or ["records/coordination.rs.jsonl"]
    print(json.dumps(derive(root, recs), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
