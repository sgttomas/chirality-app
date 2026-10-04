#!/usr/bin/env python3
"""EU-D1 fixture FX-EUD1: one question, five conditions, two connectors.

Bounded prototype (owner O-D, run APP-V4-DESIGN-PASS-4-20261003; R23-34). Not
product code. Python 3 standard library and read-only `git show`; no network.

Writes, deterministically (rerunning gives the same bytes):

- sources/: the real work graph of this run at two committed revisions,
  read with `git show` (authoritative input; never edited);
- pec/: five constructed PEC responses P1...P5 and one no-response
  observation P6, built only from elements PEC's own contract names
  (PEC-ORI-003, -004, -007; DEL-04-03 CLM-003, CLM-019). Every one is
  `constructed` (HOSTING §9.2). No PEC response, release or adoption exists
  (DEP-002 unestablished at ffb2b6289; D108);
- pec/ADOPTION_ACCOUNT.json: a constructed DEL-07-01 OUT-004 account;
- domains/: invented research sources, a constructed admission basis, one
  constructed result set DM-1 built from an older source revision, and one
  no-response observation DM-2;
- MANIFEST.sha256.

Usage: python3 make_fixture.py [OUTDIR]   (default: fixtures/FX-EUD1 here)
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
WG = "projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-DESIGN-PASS-4-20261003/WORK_GRAPH.md"
S = "e4a0c2c4c369c9f85c3be4417e5815a4b4cb0abc"   # since-revision
R = "e086dfff32c0ddc5f3236dadf2dcb5795a518734"   # at-revision (the file's last change before HEAD d2929fd62b)
CONSTRUCTED = "constructed (EU-D1); not a PEC response; element names are Chirality labels, not PEC wire fields"


def git_show(rev, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout


def dump(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False) + "\n").encode("utf-8")


def write(out, rel, data):
    p = os.path.join(out, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def stamp(pin, freshness):
    return {"examined_through": pin, "generated_at": "2026-10-04T08:00:00Z",
            "feed_freshness": [{"feed": "work_graphs", "freshness": freshness}]}


COVERAGE = ("orientation: work-graph nodes in READY, ACTIVE or BLOCKED for the loop (PEC-ORI-001); "
            "deltas: node state changes since the caller's SHA (PEC-ORI-002)")


def claim(cid, text, sha_, tier, anchor="#nodes", **extra):
    c = {"claim_id": cid, "statement": text,
         "citation": {"path": WG, "anchor": anchor, "sha": sha_}, "tier": tier}
    c.update(extra)
    return c


DELTAS = [
    ("VC", "ACTIVE", "COMPLETE (R23-22)"),
    ("E", "ACTIVE", "COMPLETE (RR-E, RR-F)"),
    ("O-B1", "READY", "COMPLETE"),
    ("O-C1", "READY", "COMPLETE"),
    ("D", "PLANNED", "COMPLETE (PR)"),
    ("T2", None, "PLANNED"),
]


def delta_claims(only=None):
    out = []
    for i, (node, old, new) in enumerate(DELTAS, start=2):
        if only is not None and node not in only:
            continue
        if old is None:
            text = f"Node {node} was added since {S[:10]}, with state {new}"
        else:
            text = f"Node {node} changed from {old} to {new} since {S[:10]}"
        out.append(claim(f"c{i}", text, R, "record"))
    return out


def presence_claim():
    """A presence fact cites PEC's presence record, never a file: the presence tier is not
    reconstructible from files (PEC-K-02). Repair OD-F1 (was a work-graph citation with an
    anchor that does not exist); renumbered c9 -> c8 (T-4)."""
    return {"claim_id": "c8", "statement": "A session for owner O-A was active",
            "citation": {"path": "pec-presence:session/O-A"}, "tier": "presence", "heartbeat_age_s": 120}


def pec_response(rid, release, qualification, pin, feeds, fallback, claims, note):
    return {"fixture": rid, "standing": CONSTRUCTED, "note": note,
            "question": "Q1", "release": {"identity": release, "stated_qualification": qualification},
            "stamp": stamp(pin, f"examined through {pin[:10]}" if pin else None),
            "envelope": {"pin": pin, "feeds": feeds, "fallback_signal": fallback},
            "claims": claims}


def feed(coverage=COVERAGE, freshness=None, limitation=None, pin=R):
    return {"feed": "work_graphs", "coverage": coverage,
            "freshness": freshness if freshness is not None else f"examined through {pin[:10]}",
            "limitation": limitation}


def build(out):
    files = {}
    srcS, srcR = git_show(S, WG), git_show(R, WG)
    files["sources/WORK_GRAPH@e4a0c2c4c3.md"] = srcS
    files["sources/WORK_GRAPH@e086dfff32.md"] = srcR
    files["sources/SOURCES.json"] = dump({
        "note": "Bytes read with `git show <commit>:<path>`; committed revisions only. The working tree may hold later, uncommitted bytes of the same path; Q1 is asked at the committed revision R.",
        "sources": [
            {"source_id": "WG@S", "path": WG, "revision": S, "sha256": sha(srcS), "file": "sources/WORK_GRAPH@e4a0c2c4c3.md"},
            {"source_id": "WG@R", "path": WG, "revision": R, "sha256": sha(srcR), "file": "sources/WORK_GRAPH@e086dfff32.md"}]})

    c1R = claim("c1", f"No work-graph node of APP-V4-DESIGN-PASS-4-20261003 is READY, ACTIVE or BLOCKED at {R[:10]}", R, "record")
    full = [c1R] + delta_claims() + [presence_claim()]
    files["pec/P1.json"] = dump(pec_response("P1", "pec-release-EX-1", "qualified", R, [feed()], "clear", full,
                                             "adopted release, pin at R, no limitation, fallback clear"))
    files["pec/P2.json"] = dump(pec_response("P2", "pec-release-EX-2", "unqualified", R, [feed()], "clear", full,
                                             "same claims as P1 from a release the App has not adopted"))
    c1S = claim("c1", f"Work-graph nodes READY or ACTIVE at {S[:10]}: VC ACTIVE, E ACTIVE, O-B1 READY, O-C1 READY", S, "record")
    files["pec/P3.json"] = dump(pec_response("P3", "pec-release-EX-1", "qualified", S, [feed(pin=S)], "clear",
                                             [c1S, presence_claim()],
                                             "adopted release, pin at S (before the cited file changed)"))
    c1P = claim("c1", f"No READY, ACTIVE or BLOCKED node among the parsed rows at {R[:10]}", R, "record")
    files["pec/P4.json"] = dump(pec_response("P4", "pec-release-EX-1", "qualified", R,
                                             [feed(coverage="partial: node-table rows after node K not parsed",
                                                   limitation="work-graph table rows 6-10 unparsed (PEC-ORI-006 measurement limitation)")],
                                             "clear", [c1P] + delta_claims(only={"VC"}),
                                             "adopted release, pin at R, the work-graph feed only partly parsed"))
    files["pec/P5.json"] = dump(pec_response("P5", "pec-release-EX-1", "qualified", R,
                                             [feed(limitation="service failing its own checks: reconcile check failed")],
                                             "set", full, "adopted release, pin at R, file-fallback signal set"))
    # P7 (RV2 EUD1-R1; R23-40): the same response as P3's first claim, but the question is asked AT S
    # (question Q1-S), so the pin equals the asked revision: adopted, current, relied. It reports what
    # the work graph records at S (O-B1 and O-C1 READY); it does not make anything ready to start.
    files["pec/P7.json"] = dump(dict(pec_response("P7", "pec-release-EX-1", "qualified", S, [feed(pin=S)], "clear",
                                                  [c1S], "adopted release, pin at S, the question asked at S (Q1-S)"),
                                     question="Q1-S"))
    # P8 (OD-F1): as P1, but record-tier claim c3 cites an anchor that is not in the cited file.
    bad = [dict(c) for c in full]
    bad = [dict(c, citation=dict(c["citation"], anchor="#no-such-section")) if c["claim_id"] == "c3" else c for c in bad]
    files["pec/P8.json"] = dump(pec_response("P8", "pec-release-EX-1", "qualified", R, [feed()], "clear", bad,
                                             "as P1, but claim c3's citation does not resolve in the cited file"))
    files["pec/P6.json"] = dump({"fixture": "P6", "standing": CONSTRUCTED, "question": "Q1",
                                 "observation": "no_response",
                                 "detail": "connector stopped: no service answered the request; no response carries any signal",
                                 "note": "receiver-side observation of total absence (DEL-07-01 REQ-005)"})
    files["pec/ADOPTION_ACCOUNT.json"] = dump({
        "account": "acct:pec-adoption-EX", "form": "DEL-07-01 OUT-004 evidence account (PRC-v0.1 §6)",
        "standing": "constructed (EU-D1): no PEC release exists; DEP-002 is OPTIONAL_RECEIVING_QUALIFICATION_UNESTABLISHED_AT_ffb2b6289",
        "adopted": [{"release": "pec-release-EX-1", "feeds": ["work_graphs"],
                     "recorded_by": "App receiving owner (constructed)", "evidence": ["constructed"]}],
        "not_adopted": [{"release": "pec-release-EX-2", "why": "stated unqualified; no qualification or release evidence"}],
        "d108": "D-PEC-108 accepted the D1 bytes as-is: RF-001 MAJOR retained, PEC DEL-00-01/AC-002 partly met. No repair, readiness, release or adoption is inferred from it."})

    # ---- Domains (invented research material)
    src1a = b"# SRC-1 Support spacing note (invented)\nrevision: rev-A\n\nLine EX-L1 support spacing: 3.0 m.\n"
    src1b = b"# SRC-1 Support spacing note (invented)\nrevision: rev-B\n\nLine EX-L1 support spacing: 2.4 m (revised after the rev-A check).\n"
    src2 = b"# SRC-2 Forum post (invented)\nrevision: rev-1\n\nSomeone says line EX-L1 spacing is 3.0 m.\n"
    files["domains/sources/SRC-1@rev-A.md"] = src1a
    files["domains/sources/SRC-1.md"] = src1b
    files["domains/sources/SRC-2.md"] = src2
    files["domains/ADMISSION.json"] = dump({
        "standing": "constructed (EU-D1): no Domains provider, contract or admission exists (OI-023, OI-026 open)",
        "contract": {"identity": "DQC-EX-1", "established": True},
        "admitted": [{"source_ref": "domains/sources/SRC-1.md", "admitted_revision": "rev-A", "basis_ref": "ADM-1",
                      "use": "support-spacing research context"}]})
    files["domains/DM-1.json"] = dump({
        "fixture": "DM-1", "standing": "constructed (EU-D1); not a Domains response", "question": "QD",
        "contract": "DQC-EX-1", "index_basis": "built from SRC-1 rev-A and SRC-2 rev-1",
        "results": [
            {"result_id": "r1", "source_ref": "domains/sources/SRC-1.md", "indexed_revision": "rev-A",
             "snippet": "Line EX-L1 support spacing: 3.0 m.", "admission": {"state": "admitted", "basis_ref": "ADM-1", "admitted_revision": "rev-A"}},
            {"result_id": "r2", "source_ref": "domains/sources/SRC-2.md", "indexed_revision": "rev-1",
             "snippet": "Someone says line EX-L1 spacing is 3.0 m.", "admission": {"state": "not_admitted"}}]})
    files["domains/DM-2.json"] = dump({"fixture": "DM-2", "standing": "constructed (EU-D1)", "question": "QD",
                                       "observation": "no_response", "detail": "query tool unavailable"})

    for rel, data in sorted(files.items()):
        write(out, rel, data)
    manifest = "".join(f"{sha(files[k])}  {k}\n" for k in sorted(files))
    write(out, "MANIFEST.sha256", manifest.encode())
    return files


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "fixtures", "FX-EUD1")
    build(out)
    print("FX-EUD1 written to", out)
