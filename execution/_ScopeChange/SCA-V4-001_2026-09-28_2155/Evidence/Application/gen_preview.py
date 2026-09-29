import sys,os,hashlib
W,OUT=sys.argv[1],sys.argv[2]
PK=W+'/projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/AMENDMENT_PACKET/'
ba=open(PK+'BASIS_AMENDMENT.md',encoding='utf-8').read()
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
i=ba.index('## Part A — Accepted basis documents')
body=ba[i:]
assert body.count('## Part B')==1
head=f'''# SCA-V4-001 — Amendment preview (exact amendment, rendered)

**Standing: accepted at checkpoint group 2 (owner DECISION-7, 2026-09-28), as
transcribed after the act.** The owner reviewed the packet itself; this file
renders its exact text for the scope-change layout. Where this file and the
packet differ, the packet governs:

| Accepted source | sha256 |
|---|---|
| `AMENDMENT_PACKET/BASIS_AMENDMENT.md` (Parts A and B: basis documents, decomposition package, `_CONTEXT.md` mirrors) | `{sha(PK+'BASIS_AMENDMENT.md')}` |
| `AMENDMENT_PACKET/SOW_REVISIONS.md` (the 16 ScopeOfWork contracts, 124 E-blocks) | `{sha(PK+'SOW_REVISIONS.md')}` |

## Token fill

- `{{AMENDMENT_ID}}` = `SCA-V4-001` (owner item O-1, accepted).
- `{{AMENDMENT_SNAPSHOT}}` = the accepted group-3 snapshot folder under
  `execution/_ScopeChange/`. The current candidate is
  `SCA-V4-001_2026-09-28_2155`; the value is fixed only by the group-3 act.
- `{{ACCEPT_DATE}}` = the date of the owner's group-3 act.

## Application classes

| Class | Edits | When |
|---|---|---|
| Candidate edits (no acceptance token) | Part A: A01, A02/A03, A04, A05, A06 (O-8), A11a, A11b, A08/A09, A10, A12, A13, A14, A15, A16. Part B: D-01…D-08 (ScopeItemStatement and DecisionRef), D-09, D-10a/b, D-11a–d, D-12a–c, D-13 (O-8), D-14a/b (O-17), D-16, B7 mirrors, B8 Consolidated_Coverage RECOMPUTE | Written into the candidate poststate after group 2 |
| **Acceptance-conditional** (carry `{{ACCEPT_DATE}}` and/or `{{AMENDMENT_SNAPSHOT}}`) | A07 (three old/new pairs in PRD.md), A17a (ARCHITECTURE.md), A17b (HOST_INTEGRATION.md), A17c (EXAMINATION.md), D-15 (`## Decision Log` section in SOFTWARE_DECOMP.md) | Only after group-3 acceptance, with the tokens filled from the accepted record; then Consolidated_Coverage is recomputed again by the same rule (A07/A17 move document lines and hashes) |
| ScopeOfWork edits (SOW_REVISIONS.md) | A32–A47, 16 contracts | After group-3 acceptance, by `scope-of-work` MODE=REVISE, one brief per deliverable, closing with MODE=VERIFY (O-3) |

Every "old" block below was checked to occur exactly once in its target
before application; every acceptance-conditional "old" block also occurs
exactly once in the candidate, so it still applies at group 3.

---

'''
open(OUT,'w',encoding='utf-8').write(head+body)
