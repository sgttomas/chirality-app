# Group B first production slice

Implementation candidate: `fc027ae116` (`codex/app-v4-group-b-support`).
Authoring instance: delegated TASK `/root/group_b_manager/support_production`;
parent WORKING_ITEMS `/root/group_b_manager`. No further delegation.

The new maintained `app/examination/` file CLI checks canonical EXP result and
PKG identity schemas, their applicable semantic rules, and an explicit
candidate/package association. Input files and implementation bytes are hashed
in reports. Canonical source drift, duplicate JSON keys, malformed records,
contradictory aggregate outcomes, native substitution, mismatched candidate
revision/build/pin/support, and historical result reuse are refused at their
respective check boundaries. A consistent record with unrun work remains valid
with its prerequisite gaps; no command exit status establishes qualification.

`SUPPORT_CHECK.json` binds the actual implementation commit/tree/file bytes,
command arguments, environment, observed date, origins/hashes and limitations.
`tests.txt` is raw output: ten test methods passed. They include the unchanged
canonical valid/invalid/rule-violation vectors, plus maintained negative checks
of connected candidate identity, source drift and native substitution. The
sample `invented-package-link.json` reports a consistent invented file pair,
all three Option B prerequisites missing, and the native witness not run.

No native App, supplier binary, sign-in, credential, network service or human
act was used. No schemas, Design contracts, ScopeOfWork, dependency registers,
work graphs, shared README or contract-issue log were changed. Partial M1
support is produced; no M2 package, M3 smoke or SQ qualification is claimed.
Independent review remains for the parent to commission before integration.

## Suggested parent closeout updates

- Add the new explicit offline command/test route to the shared App README.
  The normal `npm test` script is unchanged; it does not run this Python suite.
- Reference this production return and `SUPPORT_CHECK.json` in Group B's work
  graph and the three deliverable MEMORY entries. Keep M1 partial and M2/M3/SQ
  obligations open rather than closing a deliverable on this file tool.
- Contract observation: EXP §4.4 defines support identity using the three schema
  IDs and prototype digest; result schema requires only its own schema ID and
  makes the prototype digest optional, while PKG stores only the EXP version.
  No contract is rewritten here. Package-link requires the digest under §4.4;
  standalone schema validation preserves the canonical optional field. Tool/rule
  identity appears separately in the CLI report. A future full M1 identity
  package should resolve the documentation/schema completeness treatment under
  named review; this does not block this explicitly partial checker.
- Keep SIGN-1 Option B; FP-1(a/b) and FP-3 need actual passing evidence before
  reliance. OI-011's SWB co-owner part remains open.

The implementation commit used the host's existing Git identity. Git reported
its automatically inferred committer (`Ryan Tufts <ryan@<host>.local>`);
this task did not change account configuration or claim owner review.
