"""Write fixture FX-DP1 (one decision package decided by the person; one still pending).

Prototype only (LOOP_INIT: bounded connected test). Python 3 standard library.
Invented content: no act was performed by anyone. Deterministic: running it again
writes the same bytes, so the frozen MANIFEST.sha256 can be re-checked.

Layout written under fixtures/FX-DP1/ (the input set a reader is given):
  project/decisions/PKG-1.json, PKG-2.json   decision package files an agent wrote (App files)
  records/coordination.rs.jsonl              RS format 0.1 log: two act_request entries, one A16 human_act
  aac/offer-PKG-1.json                       the App act control's offer (DEL-01-04 AAC §5.1 shape + PR-6..PR-9)
  aac/cap-decide-PKG-1.json                  its capture evidence (AAC §5.2 shape + PR-10..PR-12)
  conversation/agent-message.txt             an agent's message claiming a decision: NOT a record (CAP-7, HA-1)
"""

import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "fixtures", "FX-DP1")
METHOD = "file content identity (method unselected; TEST VALUE: sha-256 of the file bytes)"


def dump(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write(rel, data):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return "sha256:" + hashlib.sha256(data).hexdigest()


def package(pid, subject, purpose, alts, cons):
    # The elements the agent names, exactly those of the act_request it becomes (RS §13.6; PR-3, PR-4).
    return {
        "packageId": pid,
        "actKind": "A16",
        "subject": subject,
        "purpose": purpose,
        "scope": "undertaking FX-U1 (invented)",
        "alternatives": [{"id": a, "statement": s} for a, s in alts],
        "consequences": [{"alternative": a, "statement": s} for a, s in cons],
    }


def main():
    pkg1 = package(
        "PKG-1",
        ["route for stage 2 of undertaking FX-U1"],
        "choose how stage 2 of FX-U1 proceeds (reserved to the person by the FX-U1 brief, item 4; invented)",
        [("ALT-1", "Start stage 2 now on the current supplier facts"),
         ("ALT-2", "Hold stage 2 until the version check returns, then start")],
        [("ALT-1", "Stage 2 starts today; any changed supplier fact reopens the affected parts"),
         ("ALT-2", "Stage 2 starts after the check; no rework from a changed fact; about one day later")],
    )
    pkg2 = package(
        "PKG-2",
        ["reviewer for stage 2 of undertaking FX-U1"],
        "choose who reviews stage 2 (reserved to the person by the FX-U1 brief, item 5; invented)",
        [("ALT-1", "The standing reviewer"), ("ALT-2", "A fresh reviewer of another model family")],
        [("ALT-1", "Continuity with stage 1 findings"), ("ALT-2", "More independence; slower start")],
    )
    c1 = write("project/decisions/PKG-1.json", dump(pkg1))
    c2 = write("project/decisions/PKG-2.json", dump(pkg2))

    writer = {"role": "App writer", "identity": "app-writer:local"}
    iface = {"role": "App interface (capturing surface)", "identity": "app-interface:local"}
    ctx = {"surface": "App"}

    def request(seq, rid, pkg, ref, cid, t):
        return {"format": "chirality.rs.record", "formatVersion": "0.1", "recordId": rid, "kind": "act_request",
                "recorder": writer, "context": ctx, "seq": seq, "writtenAt": "w%03d" % seq,
                "body": {"requester": {"kind": "agent", "identity": "thread:fx-u1-manager"},
                         "form": "decision package file",
                         "actKind": pkg["actKind"], "subject": pkg["subject"], "purpose": pkg["purpose"],
                         "scope": pkg["scope"], "association": "not at a checkpoint",
                         "evidence": {"kind": "content identity", "ref": ref, "claimedIdentity": cid,
                                      "method": METHOD, "resolutionAtWrite": "resolved"},
                         "time": t,
                         "alternatives": pkg["alternatives"], "consequences": pkg["consequences"]}}

    person = {"displayName": "Engineer A", "osAccount": "enga", "identityVerified": False}
    alts_shown = [{"id": a["id"], "statement": a["statement"],
                   "consequences": [c["statement"] for c in pkg1["consequences"] if c["alternative"] == a["id"]]}
                  for a in pkg1["alternatives"]]
    offer = {"format": "chirality.aac.offer", "formatVersion": "0.3", "offerId": "offer:pkg-1",
             "actKind": "A16", "wording": "decide",
             "subject": {"class": "App file", "ref": "project/decisions/PKG-1.json",
                         "contentIdentity": {"method": METHOD, "value": c1}},
             "scope": pkg1["scope"], "purpose": pkg1["purpose"], "actorRequirement": "the person",
             "declineAvailable": False, "answers": {"standing": "no arrival: a standing act (RC-6)"},
             "requestRef": "rec:app:coord:0001", "composedAt": "t3",
             "offerDigest": {"method": "TEST VALUE: sha-256 over the offer without offerDigest", "value": "pending"},
             "alternatives": alts_shown}
    od = dict(offer)
    del od["offerDigest"]
    offer["offerDigest"]["value"] = "sha256:" + hashlib.sha256(json.dumps(od, sort_keys=True).encode()).hexdigest()
    write("aac/offer-PKG-1.json", dump(offer))

    cap = {"format": "chirality.aac.capture-evidence", "formatVersion": "0.3", "captureId": "cap:decide-pkg-1",
           "offerId": offer["offerId"], "offerDigest": offer["offerDigest"], "choice": "act", "actKind": "A16",
           "actor": person, "boundSubject": ["decision package rec:app:coord:0001"],
           "boundContent": [{"method": METHOD, "value": c1}], "scope": pkg1["scope"], "purpose": pkg1["purpose"],
           "capturedAt": "t4", "surface": "App interface", "inputSource": "host-native-confirmation",
           "answers": {"standing": "no arrival: a standing act (RC-6)"}, "requestRef": "rec:app:coord:0001",
           "alternativeChosen": "ALT-2", "recordId": "rec:app:coord:0003",
           "evidenceLimits": ["identity not verified"]}
    write("aac/cap-decide-PKG-1.json", dump(cap))

    act = {"format": "chirality.rs.record", "formatVersion": "0.1", "recordId": "rec:app:coord:0003", "kind": "human_act",
           "recorder": iface, "context": ctx, "seq": 3, "writtenAt": "w003",
           "body": {"actKind": "A16", "actClass": {"value": "person's act (V4-PM-04)"}, "decisionActor": person,
                    "recordingMode": "direct capture", "boundSubject": ["decision package rec:app:coord:0001"],
                    "boundContent": [{"method": METHOD, "value": c1}], "scope": pkg1["scope"], "purpose": pkg1["purpose"],
                    "captureEvidence": [{"kind": "capture evidence", "ref": "cap:decide-pkg-1", "resolutionAtWrite": "resolved"}],
                    "captureTime": "t4", "evidenceLimits": ["identity not verified"],
                    "relations": {"requestRef": "rec:app:coord:0001", "alternativeChosen": "ALT-2"}}}
    lines = [request(1, "rec:app:coord:0001", pkg1, "project/decisions/PKG-1.json", c1, "t1"),
             request(2, "rec:app:coord:0002", pkg2, "project/decisions/PKG-2.json", c2, "t2"),
             act]
    write("records/coordination.rs.jsonl",
          "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in lines).encode("utf-8"))
    write("conversation/agent-message.txt",
          b"(Invented agent message, not a record.) The owner chose ALT-1 for PKG-2, so I will proceed.\n")

    # Input-set manifest, in shasum -a 256 format, sorted, paths relative to fixtures/FX-DP1/.
    rows = []
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            if f == "MANIFEST.sha256":
                continue
            p = os.path.join(d, f)
            with open(p, "rb") as fh:
                rows.append((os.path.relpath(p, ROOT), hashlib.sha256(fh.read()).hexdigest()))
    with open(os.path.join(ROOT, "MANIFEST.sha256"), "w", encoding="utf-8") as fh:
        for rel, h in sorted(rows):
            fh.write(f"{h}  {rel}\n")
    print("wrote", ROOT)


if __name__ == "__main__":
    main()
