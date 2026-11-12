# dbm-concordance-verify contract

## Brief

`TASK + dbm-concordance-verify` reviews internal semantic consistency after a
complete DBM has been authored. WORKING_ITEMS may commission it alongside
`dbm-postauthor-concordance` for a package, or directly against a standalone
human draft. A standalone run makes no DOMAIN admission or publication claim.

### Scope and required brief fields

`ScopePath` is `REVIEW_OUTPUT_DIR`. `AllowedWriteTargets` names exactly the two
output files below. Both must be distinct, remain inside the review directory
after path resolution, and must not alias any input. If `PACKAGE_SNAPSHOT_PATH`
is supplied, the review directory must also be inside that package boundary.
Existing accepted outputs are not overwritten; use a new review directory.

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why consistency review is needed | `Review shared utility conditions across the authored DBM.` |
| `ScopePath` | path | Authorized review directory | `/project/reviews/CONCORDANCE-01/` |
| `Workflow` | string | Workflow selection | `dbm-concordance-verify` |
| `AllowedWriteTargets` | list[path] | Exactly the two review outputs | `[/.../Publication_Concordance_Verification.md, /.../Publication_Concordance_Verification_Findings.csv]` |
| `RuntimeOverrides.ASSEMBLED_DBM_PATH` | path | Complete authored Markdown DBM | `/project/draft.md` |
| `RuntimeOverrides.REVIEW_OUTPUT_DIR` | path | Authorized output root | `/project/reviews/CONCORDANCE-01/` |
| `RuntimeOverrides.OUTPUT_VERIFICATION_PATH` | path | Markdown report | `/.../Publication_Concordance_Verification.md` |
| `RuntimeOverrides.OUTPUT_VERIFICATION_FINDINGS_PATH` | path | Candidate findings CSV | `/.../Publication_Concordance_Verification_Findings.csv` |
| `ExpectedOutputs` | list[path] | Same two review outputs | `[/.../Publication_Concordance_Verification.md, /.../Publication_Concordance_Verification_Findings.csv]` |

### Optional runtime overrides

| Field | Meaning |
|---|---|
| `SECTIONS_ROOT` | Current section bodies and QA; they must correspond to the assembled document |
| `REVIEW_EVIDENCE_ROOT` | Same-document evidence bundle: summary, section coverage, draft claims, body thinness, TBD inventory, and candidate findings |
| `SECTION_MAP_PATH` | Approved section identities and contribution scope |
| `PUBLICATION_RULES_PATH` | Approved terminology, uncertainty, and restatement policy |
| `PUBLICATION_INPUT_MANIFEST` | Input provenance and admission context; its presence is not itself admission |
| `SOURCE_SUPERSESSION_FINDINGS_PATH` | Existing source-fidelity findings to interpret, not independent source authority |
| `PACKAGE_SNAPSHOT_PATH` | Additional package boundary for pipeline runs |
| `CONCORDANCE_REGISTER_PATH` | Explicit legacy register; every supplied key must be accounted for |
| `CONCORDANCE_FINDINGS_PATH` | Explicit legacy deterministic findings to interpret |

`CustomInstructions` may focus attention but cannot narrow the complete-document
review without recording the omitted coverage and `ReviewStatus = PARTIAL`.
There is no inferred legacy-register path and no required assertion CSV.

### Example standalone brief

```md
PURPOSE: Review cross-section consistency of the human-prepared DBM.
ScopePath: /project/reviews/CONCORDANCE-01/
Workflow: dbm-concordance-verify
AllowedWriteTargets:
  - /project/reviews/CONCORDANCE-01/Publication_Concordance_Verification.md
  - /project/reviews/CONCORDANCE-01/Publication_Concordance_Verification_Findings.csv
RuntimeOverrides:
  ASSEMBLED_DBM_PATH: /project/draft.md
  REVIEW_OUTPUT_DIR: /project/reviews/CONCORDANCE-01/
  OUTPUT_VERIFICATION_PATH: /project/reviews/CONCORDANCE-01/Publication_Concordance_Verification.md
  OUTPUT_VERIFICATION_FINDINGS_PATH: /project/reviews/CONCORDANCE-01/Publication_Concordance_Verification_Findings.csv
ExpectedOutputs:
  - /project/reviews/CONCORDANCE-01/Publication_Concordance_Verification.md
  - /project/reviews/CONCORDANCE-01/Publication_Concordance_Verification_Findings.csv
```

For a pipeline run, supply the package's `Rewritten_DBM.md`, current section
root, approved section map/rules/manifest, and its `review/` evidence bundle.
Place the verification outputs in an authorized directory within that package.
Run after assembly and bundle preparation; rendering a dispatch brief does not
establish that those future inputs exist or match.

## Acceptance

A valid review has both outputs and stays inside the exact write boundary. Its
report accounts for every authored section, documents comparison scope and
limitations, and accounts for each explicitly supplied legacy register key.
All non-`CONFIRMED` observations have matching findings rows. Empty findings
still emit the CSV header. No input or accepted pointer is changed.

### Required findings schema

Columns, in order:

`ObservationID, AssertionKey, Verdict, Severity, ImpactedSections, EvidenceRefs, EvidenceSource, Explanation, RecommendedAction`

- `ObservationID`: run-local identity `CV-001`, `CV-002`, ...; shared with report.
- `AssertionKey`: descriptive identity for the engineering fact/state and its
  applicable scope/case; reuse a supplied legacy key only when its meaning matches.
- `Verdict`: `CONFIRMED`, `NORMALIZATION_ARTIFACT`, `SEMANTIC_MISMATCH`,
  `IMPLICIT_CONFLICT`, `COVERAGE_GAP`, or `NEEDS_HUMAN_RULING`.
- `Severity`: `HIGH`, `MEDIUM`, `LOW`, or `ADVISORY`, based on consequence.
- `ImpactedSections`: section IDs, or document heading/line references when no
  approved IDs exist.
- `EvidenceRefs`: exact document/table/line references supporting the observation;
  disagreements cite both positions. Missing relationships cite the expectation
  and examined section. Avoid unsupported references to external truth.
- `EvidenceSource`: `AUTHORED_TEXT` plus any supplied artifact/row references
  actually used. Tool signals alone are not a semantic finding.
- `Explanation`: engineering reasoning, including applicable context, uncertainty,
  and any unit/datum/precision normalization. No invented tolerances.
- `RecommendedAction`: concrete review or repair, including needed human ruling.

`CONFIRMED` observations may remain in the report only. The findings CSV has no
automatic `Blocking` field. Human dispositions are recorded separately by the
caller, referencing these observation IDs; this workflow does not author them.
Legacy `OMITTED_REQUIRED_ASSERTION` and `REGISTER_GAP` output labels are replaced
by `COVERAGE_GAP` where an actual expectation is evidenced, otherwise by
`NEEDS_HUMAN_RULING`. A missing legacy emission row alone is not a body omission.

### Required report structure

H2 headings, in order:

1. `## Verification Summary` — `ReviewStatus: COMPLETE|PARTIAL`, document identity,
   evidence basis, candidate counts, and a clear limit to internal consistency.
2. `## Inputs and Limitations` — consumed paths, provenance checks, unavailable or
   stale supplied evidence, and dimensions not assessed. State that external
   correctness/completeness is not established by this review.
3. `## Section Coverage` — every section examined, with IDs or heading/line anchors;
   identify any unread/unreviewed section and its effect on status.
4. `## Cross-Section Observations` — comparison groups, context, locations, verdicts,
   and observation IDs; include explicitly supplied legacy keys.
5. `## Review Evidence Interpretation` — interpreted substrate/legacy findings, or
   `Not supplied; review based on authored content`.
6. `## Human Rulings Required` — unresolved candidate observations and proposed next
   steps. No prefilled human decisions or publication-readiness verdict.

`ReviewStatus = COMPLETE` means the full authored text and commissioned
comparisons were assessed; it is compatible with material candidate findings.
`PARTIAL` means an assessment remains incomplete. Missing optional inputs never
supplied are not a failure. Missing/stale supplied evidence requires an explicit
limitation and `PARTIAL` for affected requested comparisons; review unaffected text.

### Failure and recovery

Use `FAILED_INPUTS` for unreadable/missing authored Markdown, missing required
overrides, escaping/aliasing output paths, or attempted overwrite of accepted
review outputs. Do not fabricate empty successful reports. Continue unaffected
work when optional evidence is unavailable and emit a candid partial review.
Use `FAILED` if internal failure prevents producing the two outputs; identify
what was reviewed and what remains. After document edits, commission a new
full-document review against the new version and its corresponding evidence.

## Tools and authority

No deterministic tool execution or delegation. Read only the authored document,
its supplied section outputs, and named planning/review evidence. No raw KA/KTY
or reference-source reads; no source-grounded accuracy claim. No changes to
inputs, human dispositions, or pointers. Tools supply observations; agents
interpret them; the human decides their disposition and acceptance consequence.
