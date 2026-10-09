# EXP-IN5-CLARIFICATION-v1

Named technical change: **CC-EXP-IN5-01**. Source owner: DEL-09-01.
This is the additive clarification selected by the Group B technical owner for
independent source review. It neither rewrites EXP-v0.2 nor changes a rule,
schema, outcome, native criterion or actor responsibility. Reviewed source
publication and each affected consumer's receiving disposition are separately
recorded by the manager. This file's presence alone does not establish either
act, repair closure, owner review, route admission or qualification.

## Exact source and controlling reading

This clarification applies to `../EXAMINATION_PROTOCOL.md`, EXP-v0.2,
SHA-256 `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93`, specifically §2.1 IN-5's
“If absent” cell. Its original bytes remain unchanged. The existing
`../exam.result-record.schema.json` SHA-256 is
`f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081`. Those source bytes match publication merge
`09106477e351c6e5bde85259c55a00cc8fc5f7f5` (PR1077). This separately versioned
clarification is not part of that historical publication or the old fixed
EXP-SUPPORT-BINDING-v1 declaration.

R23-20 distinguishes an unattempted planned case (`not-run`) from an attempted
case stopped at its start or later (`blocked`, with cause). The general attempted
case rule remains. The more specific published EXP-R2 and §9 NB-3 require a
package and its record for native_packaged outcomes other than not-run. The
independent RV-EXP-U1 repair confirmation, EXP-R-C, explicitly confirms that
conditional and the missing-package not-run example EXP-EX-04. IN-5's old blanket
blocked phrase does not authorize an exception to those rules.

The R23-20 ruling and RV-EXP-U1 confirmation remain at their recorded origins in
`projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/`
(`R23_RESOLUTIONS.md`, `reviews/RV-EXP-U1.md`). These are historical source
citations, not runtime dependencies or independently authenticated owner acts.

## Clarified IN-5 If-absent text

> Before a candidate is named, list the missing input without a result; once planned for a named candidate, missing package means `not-run` with that input. With the package present, an attempted case stopped by another stated prerequisite may be `blocked`; never substitute a browser pass (§6.1; §9 NB-2/NB-3; EXP-R2)

This is the exact replacement wording selected from the reviewed proposal;
only IN-5's If-absent reading is clarified. The input, DEL-01-06 supplier,
DEP-09-01-016 held relationship and point of need are unchanged. No held arc is
converted into a gate or readiness claim. The old row stays intact in its frozen
source; a future consolidated revision would require its own named source
publication and receiving plan.

| Actual condition | Preserved treatment |
|---|---|
| No named candidate yet | List missing input; do not invent a subject-bound result |
| Planned native_packaged case, package missing | Record not-run with the package as missing input; claiming an attempt cannot waive EXP-R2 |
| Package present, another stated prerequisite stops an attempted case | Blocked remains available with its cause, subject to every other rule |
| Package present, case not attempted | Not-run; package presence does not prove an attempt |
| Browser evidence or development build offered as packaged witness | No substitution; native_development remains a separate route |

Schema-valid declarations do not establish package existence, an actual attempt,
M1 admission, M2/package completeness, M3 witness, S3/reference qualification,
independent review or an owner act. This clarification supplies none of them.

## Finite receiving impact

- Legacy EXP `check.py` and `admission/admission_check.py`: preserve source locks
  and already-correct schema behavior; receive the clarified source reading.
- Proposed and canonical support-identity readers: preserve all old declarations,
  full support tuples and six-role obligations. Do not relabel these new bytes
  as the frozen original publication or claim automatic canonical adoption.
- SQ receiver: retain the existing missing-package exception and its pins. A
  claim to consume this clarification needs an explicit receiving disposition.
- B7 preparation/native forms: keep exact historical plan/form/helper bytes and
  guards; no blank form becomes an execution or result record.
- S4 receiving: retain historical cohorts and the separate current Host-source
  hold. This document is not a new export, pin renewal or qualified reference.
- DEL-01-06 and EXP OUT-1…6 journey/examiner recipients: assess the exact
  clarification at their point of use. If an actual record relied on the wrong
  wording, apply EXP §6.2 impact assessment and retain its original evidence.
  Such a record's existence is not inferred from the textual inconsistency.

The manager carries exact source identity, notices and received dispositions.
No consumer is silently repinned here. F-VC09-01 remains open until the named
source and affected-consumer evidence support its actual disposition; this
supplement alone does not pronounce the finding repaired.
