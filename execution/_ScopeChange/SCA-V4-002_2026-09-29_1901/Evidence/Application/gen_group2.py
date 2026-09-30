#!/usr/bin/env python3
"""AK1 (APP-V4-SCA002-20260929): render the accepted packet into the group-2 scope-change artifacts.
Amendment_Actions.csv   = IMPACT_ASSESSMENT section 3.2 CSV block, {AMENDMENT_ID} filled (LF, as the packet draft).
Supersession_Delta.csv  = BASIS_AMENDMENT Part D CSV block, {AMENDMENT_ID} and {D_SEQ_DEL0401} filled.
Amendment_Preview.md    = header + BASIS_AMENDMENT from "## Part A" to the end, verbatim.
Usage: gen_group2.py REPO CANDIDATE_DIR
"""
import sys, re, hashlib, csv, io
W, OUT = sys.argv[1], sys.argv[2]
PK = W + '/projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/AMENDMENT_PACKET/'
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = {n: open(PK + n, 'rb').read() for n in ('BASIS_AMENDMENT.md', 'IMPACT_ASSESSMENT.md', 'SOW_REVISIONS.md', 'ARC_EFFECT.md', 'OWNER_ITEMS.md')}
EXP = {'BASIS_AMENDMENT.md': '091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238',
       'IMPACT_ASSESSMENT.md': '46444eab11d7af768484e3996a6be784a9448b5960cc0c7197fd6533fd830456',
       'SOW_REVISIONS.md': '440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d',
       'ARC_EFFECT.md': '4b3aeec0f041266dce0e2fae754c129d4473ff8c3268c0b5c638529c6951ddc0',
       'OWNER_ITEMS.md': '1d46458c966b6cc41be361eb2ddbc75df409bcc43202aff17478b81438ca51a8'}
for n, h in EXP.items():
    assert sha(raw[n]) == h, n
ba, ia = raw['BASIS_AMENDMENT.md'].decode(), raw['IMPACT_ASSESSMENT.md'].decode()

def block(t, draft_prefix, fills, nrows, ncols):
    (b,) = re.findall(r"^```csv\n(.*?)\n```$", t, flags=re.M | re.S)
    assert sha((b + "\n").encode()).startswith(draft_prefix), "draft bytes differ from the packet's stated draft hash"
    assert set(re.findall(r"\{[A-Z0-9_]+\}", b)) == set(fills)
    for k, v in fills.items():
        b = b.replace(k, v)
    out = b + "\n"
    rows = list(csv.reader(io.StringIO(out, newline=""), strict=True))
    assert len(rows) == nrows + 1 and all(len(r) == ncols for r in rows), (len(rows), {len(r) for r in rows})
    return out, rows

reg, rrows = block(ia, 'dafa622e', {'{AMENDMENT_ID}': 'SCA-V4-002'}, 16, 10)
dlt, drows = block(ba, 'a14c4dd1', {'{AMENDMENT_ID}': 'SCA-V4-002', '{D_SEQ_DEL0401}': 'D-014'}, 18, 13)
h = rrows[0]
assert [r[h.index('ActionSeq')] for r in rrows[1:]] == [str(i) for i in range(1, 17)]
assert all(r[h.index('ActionType')] == 'MODIFY' for r in rrows[1:])
assert [r[1] for r in rrows[1:] if r[h.index('ScopeChanging')] == 'YES'] == ['1']
assert [r[1] for r in rrows[1:] if r[h.index('SupersessionBindingPresent')] == 'YES'] == ['14']
assert all(';' not in r[h.index('DownstreamReruns')] for r in rrows[1:])
assert all(c == c.strip() for r in rrows for c in r)
ids = [r[1] for r in drows[1:]]
assert ids[-1] == 'D-014' and sum(i.startswith('DL-SCA-V4-001-A') for i in ids) == 17 and len(set(ids)) == 18
open(OUT + '/Amendment_Actions.csv', 'w', newline='').write(reg)
open(OUT + '/Supersession_Delta.csv', 'w', newline='').write(dlt)

i = ba.index('## Part A — Accepted basis documents')
body = ba[i:]
for p in ('## Part B', '## Part C', '## Part D', '## Record fixes carried'):
    assert body.count('\n' + p) == 1, p
head = f'''# SCA-V4-002 — Amendment preview (exact amendment, rendered)

**Standing: accepted at checkpoint group 2 (owner DECISION-2 of run
`APP-V4-SCA002-20260929`, 2026-09-29), as transcribed after the act.** The
owner reviewed the packet itself; this file renders its exact text for the
scope-change layout. Where this file and the packet differ, the packet
governs:

| Accepted source | sha256 |
|---|---|
| `AMENDMENT_PACKET/BASIS_AMENDMENT.md` (Parts A to D: the basis document, the decomposition package, the `_CONTEXT.md` edits, the pointer and effective-state record, the supersession rows) | `{EXP['BASIS_AMENDMENT.md']}` |
| `AMENDMENT_PACKET/SOW_REVISIONS.md` (nine ScopeOfWork contracts, 26 F-blocks) | `{EXP['SOW_REVISIONS.md']}` |
| `AMENDMENT_PACKET/ARC_EFFECT.md` (the four consumption sentences and the SCC computation) | `{EXP['ARC_EFFECT.md']}` |

This file was written before any SCA-V4-002 edit was applied. Everything
below the rule is BASIS_AMENDMENT.md from "## Part A" to its end, byte for
byte. Its phrases "PROPOSED", "conditional", "recommended" and "if the owner
chooses" are the packet's words at presentation; the owner's answers are in
"Owner answers" below.

## Owner answers that fix the conditional edits

| Item | Answer (DECISION-2: "accept the remaining items as recommended") | Effect on the text below |
|---|---|---|
| Q-5 | Option A: OI-001/OI-002 stay OPEN | B-03: no edit. The option-B text is not applied |
| Q-6 | Included | `{{Q6_CLAUSE}}` = `, DEL-04-02 and DEL-01-01`; SOW_REVISIONS F-0402 and F-0101 stand |
| Q-7 | Included | B-02 applies; `{{Q7_CLAUSE}}` = `; the OI-012 pointer in Open_Issues.csv` |
| Q-8 | Line break | A-01 applies in its recommended form; the blank-line alternative is not applied |
| Q-10 | Option (a) | Part D: all 17 `DL-` rows and D-014; `{{Q10_CLAUSE}}` = `; and path-level Supersession_Delta rows for SCA-V4-001 actions 18–25, 36, 42 and 46` |
| Q-11 | Included | B-05a and B-05b apply; `{{Q11_CLAUSE}}` = `; Deliverables DEL-04-01 (checkpoint clause) with its _CONTEXT.md mirror` |
| Q-12 | Option (a) | B-06a, B-06b and B-06c apply, at the times below; `{{Q12_CLAUSE}}` = `; a reading-rule note ("GROUP3 as amended by the active _ScopeChange/_LATEST.md") on _LATEST.md, checkpoint_snapshots/_LATEST_ACCEPTED.md and five _CONTEXT.md basis lines` |
| Q-13 | Accepted | C-02 is written after group 1 |

The clause values are copied from the B-04 "Slot rules" table below.

## Token fill

- `{{AMENDMENT_ID}}` = `SCA-V4-002` (owner item Q-1, accepted).
- `{{D_SEQ_DEL0401}}` = `D-014` (Part D).
- `{{AMENDMENT_SNAPSHOT}}` = the accepted group-3 snapshot folder under
  `execution/_ScopeChange/`. The current candidate is
  `SCA-V4-002_2026-09-29_1901`; the value is fixed only by the group-3 act.
- `{{ACCEPT_DATE}}` = the date of the owner's group-3 act.
- `{{CLOSURE_VERDICT}}`, `{{GROUP12_REFS}}`, `{{SCA001_CLOSURE}}`,
  `{{ARC_LIST}}`, `{{OPEN_LIST}}` and `{{UTC}}` (C-01) are filled at the
  pointer move, by the C-01 slot rules below.

## Application classes

| Class | Edits | When |
|---|---|---|
| After group-1 acceptance | C-02: the SCA-V4-001 effective-state record (new file; no existing byte changes) | Written after the group-1 decision snapshot |
| Candidate edits (no acceptance token) | A-01; B-01 (RECOMPUTE, 31 rows); B-02 (Q-7); B-05a and B-05b (Q-11); B-06b; B-06c (five `_CONTEXT.md` files); Part D (`Supersession_Delta.csv`, then `Supersession_Map.csv` by the accumulator) | Written into the candidate poststate after group 2 |
| No edit | B-03 (Q-5 option A) | — |
| **Acceptance-conditional** (carry `{{ACCEPT_DATE}}` and/or `{{AMENDMENT_SNAPSHOT}}`) | B-04 (the `## Decision Log` entry in SOFTWARE_DECOMP.md); C-01 (`_ScopeChange/_LATEST.md` in SPEC §11.2 form) | Only after group-3 acceptance, with the tokens filled from the accepted record |
| **Timed with the SoW REVISEs** (no token; the file is bound in `_DAG/DAG-002/SOURCE_MANIFEST.sha256`) | B-06a (`_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`) | After group-3 acceptance, with the SoW REVISEs, so that the one DAG-003 currency audit takes it up (B-06 "Timing of B-06a"; IMPACT_ASSESSMENT §7 step 5) |
| ScopeOfWork edits (SOW_REVISIONS.md) | Register rows 1–9, nine contracts, 26 blocks | After group-3 acceptance, by `scope-of-work` MODE=REVISE, one brief per deliverable, closing with MODE=VERIFY, `STATUS_POLICY=NO_STATUS_TOUCH` (Q-3) |

Every candidate "old" block or value was checked, before application, to
occur exactly once in its target at commit `39c97257b`
(`apply_sca002.py`, dry run). The B-04 and B-06a "old" blocks also occur
exactly once there.

---

'''
open(OUT + '/Amendment_Preview.md', 'w', encoding='utf-8').write(head + body)
for n in ('Amendment_Actions.csv', 'Supersession_Delta.csv', 'Amendment_Preview.md'):
    print(sha(open(OUT + '/' + n, 'rb').read()), n)
