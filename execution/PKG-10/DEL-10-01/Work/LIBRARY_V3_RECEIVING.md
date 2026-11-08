# Library 3.0.0 contributor adoption

## Selection and source

The owner directed this post-handoff adoption as one App PR. App pins its
contributor instructions to released `library-v3.0.0`, commit
`5170575f3f4c1fc51386fa5cd38c7ef9ac048b20`, rather than tracking moving main.
The shared checkout `/Users/ryan/dev/chirality-library` was clean and both HEAD
and the release tag resolved to that commit before reliance. Dependent results
record that resolved revision. Source paths and fixture hashes are in
[`reference/library-v3.0.0/`](../../../../reference/library-v3.0.0/README.md).
The released migration notes were read first; the reported archive digest is
recorded there without claiming an archive download or independent verification.

This supersedes c35/v2.1 only for new contributor work. Earlier results,
fixtures, accepted scope and product bindings retain their actual subjects.
It serves DEL-10-01 OUT-001/002/003 and the existing source-selection condition;
no ScopeOfWork commitment, maturity or dependency condition changes. Its new
compatibility harness is declared in `deliverable.yaml`.

## Received practice

- INTERLOCUTOR is one opt-in continuing child for the life of its paired Agent
  0 session, continued by message; replace it only if lost or the owner asks.
  Periodic summaries and pre-merge consultations remain advisory, without
  veto, sign-off, host permission or owner authority. The three-round rule and
  model/effort steering remain. Independent reviews are separate contributions.
- The released coordination method replaces the earlier unselected PR9 notice.
  Staffing follows actual contribution needs. Full dispatch briefs identify
  input/context, integration owner, write and decision boundaries and a return
  route the host actually delivers. Established routes are not re-investigated
  without changed conditions. Completion/recovery is proportionate and respects
  host polling/timer prohibitions. Existing App custody and retained-evidence
  requirements still apply.
- Project entry uses init, standing AGENTS and top-level loop, with a deliberate
  edition/revision. Cross-project messages identify the need, basis and blocking
  status after checking the recipient session; they transfer no authority.
- The active role and selected methods are read with their typed YAML header
  and prose body. Complete-source fingerprints include the header. The five-role
  registry, unchanged eligibility restrictions and separate write authority
  remain; an indexed method is not automatically eligible for INTERLOCUTOR.

## Project-entry check and local treatment

Checked against the release's
`workflows/project-setup/resources/project-entry.md`, "Checking a project":

| Check | App treatment |
| --- | --- |
| Bootstrap resolves identity, AGENTS, selected role and loop, then orient/await | Existing tagged prompt already supplies the route; retained unchanged. README now explicitly says send only the tagged block. |
| CLAUDE contains only the AGENTS pointer | Preserved exactly `@AGENTS.md` plus its existing newline. |
| Standing subjects and deliberate Library selection | Existing authority/holds/roles retained; pin changed explicitly to v3. App-local verification tiers and cross-project wording adapted without importing another repository's grants. |
| Actual grants remain local and loop links to them | Owner quote and App-only Git grant unchanged; loop points to AGENTS verification/grant/holds. |
| No session/gate narrative in AGENTS or loop | Removed the dated resumption/retired-session narrative from those entry surfaces. It already remains in CURRENT_EXECUTION_BASIS; preserve the standing macOS/shared-code rule and handoff safeguards. Legacy vocabulary/source citations are retained where they explain current interpretation. |
| Queries work from the stated directory and links resolve | Use the affected deliverable, with DEL-10-01 as an explicit worked example. The query and local entry links are checked below. Python/PyYAML and repository-root invocation remain prerequisites. |

App's accepted execution layout, retained local workflows/test inputs, protected
Windows/VM boundaries, credential/download rules and release reservations stay
local. The owner's later direction makes typed headers mandatory before handoff;
the coverage and compatibility account below supersedes their earlier optional
standing. The released Library role headers are read as part of the source.

The five-file legacy practice-pointer PR72 remains a separate draft: its Root
citations predate the repository split and need current-source reconciliation.
This receiving does not blindly apply that older text or rewrite frozen manual
inputs. The proposed survey wording is outside scope. The successor steering
prompt and closeout PR161 are held unchanged for the owner's later direction;
their c35-era current statements must not override this newer selection.

## Compatibility findings and product boundary

The retained v2.1 validator explicitly rejects an initial `---` as
`ROLE_PROSE_METADATA`. Running it against the exact v3 fixture must refuse all
five role headers. Do not patch that historical reader or strip the new headers
to manufacture compatibility. The v3 validator and its existing PyYAML
frontmatter parser accept the new roles. The resolver retains the full YAML and
body with their exact hash; it still gives INTERLOCUTOR no unassigned writes or
delegation and refuses a method without explicit compatibility.

The new ten-file test closure is deliberately partial: five roles, registry,
validator/parser, resolver and LICENSE. It is not the release distribution,
renderer, complete method catalog or a live product dependency. App CI exercises
it in an isolated exported folder and never reads a sibling Library checkout.
The exact released document-metadata schema is retained separately beside that
closure, with its source path, Git blob/mode and digest in the same manifest.
The old v2.1 harness continues on its frozen fixture; its active-selection-named
test now reads the historical receiving account to avoid mislabeling c35 as
the current selection.

The product remains basis `89acac6a3983c605820496d0d121c73bb2297706`, four
roles, all default flags false. DEL-02-04 Work sources, generator derivation,
eight shipped instruction files, historical bindings, role-supply runtime and
prototype remain unchanged. This is **operational v3 adoption, not product v3
adoption**.

For a future product migration: the closed role-set parser, enum/path allowlists
and three direct conversation entries do not admit a fifth role today. The
current guidance readers accept nonempty UTF-8 bytes and do not require a first
`#`, so a YAML prefix is not itself a mechanical read failure; the full bytes
would reach developer instructions and change all relevant content fingerprints.
The deterministic Work-to-resource generator also copies bytes unchanged. A
later update must deliberately author/select guidance, version/reconcile the
role set and source binding, regenerate derivatives and check actual supplier
uptake. Metadata must not be silently stripped or imported as runtime authority.
The earlier [v2.1 product-boundary recommendation](LIBRARY_V2_1_RECEIVING.md#product-boundary-recommendation-for-a-future-additive-migration)
remains a recommendation, not a selected product migration. No native/model
proof follows from this source inspection.

## Verification

Focused checks use prepared offline Python/PyYAML/pytest under the ordinary
slot wrapper with fresh scratch OS/Codex/temp homes. The receiving harness,
historical fixture checks, existing deliverable/CI/prototype consumers,
instruction-resource freshness and the documented neighborhood query are the
relevant checks. Results: 130 focused pytest cases passed; deliverables reported
41 deliverables and zero errors; the DEL-10-01 neighborhood query succeeded;
instruction-resource freshness passed for all eight files; ten generator tests
passed; and examination pins agreed. The ten retained Library blobs and modes
were independently compared with the selected Git objects. Receiving/init local
links resolved, and the protected product sources, generated instructions,
derivation, historical fixture, init prompt and CLAUDE pointer were unchanged.

Evidence is retained in
`/Users/ryan/dev/chirality-t3/scratch/app-library-v3-receiving-_xtqy8q6/CHECK_SUMMARY.json`;
the final receipt binds contribution and log hashes to the PR head. The initial
harness invocation failed because Python `-I` removed the released validator's
adjacent-module import path. The harness now uses `-E -s` in its relocated
export; the released source was not patched. The corrected focused batch passed.
No App build, native/supplier/auth/model action, asset acquisition or Library
write was performed.

## Mandatory maintained-document headers

The owner extended the adoption: "I want all the typed headers in place
consistently across the projects before we handoff." Nineteen maintained
documents now carry the released schema's name, description, kind and surface:
AGENTS, the init prompt and its usage README, the loop, all fourteen Markdown
documents under docs (including the eight user-manual pages), and the one
tool-use README. The header sits above the unchanged init tagged block; only
that block is sent. CLAUDE remains exactly its existing AGENTS pointer.

All are instructions by principal use. The five accepted PRD/companion
documents use the requirements surface, including architecture and operating
method: their rationale remains in the body, but they establish the accepted
product basis. The manual pages and CI guide use reference; the deliverable
query README uses tool. No classification remains unresolved. No date, revision
or status field was added to metadata; the existing body standing is preserved.
Bodies and anchors are unchanged except for explicitly labelling the loop's
query as an example, following the interlocutor's minor clarity suggestion.

The retained local coordinated-knowledge-work WORKFLOW and REVIEW-NOTES are
migration test inputs, not maintained App method authoring; their exact hashes
remain those in reference/migration/shared-inputs.json. They therefore take the
owner's retained-historical-byte exclusion. There are no local skill entrypoints
or maintained local workflow entrypoints to migrate. Execution documents,
foundation/thesis, reference/migration, frozen/reference editions, all packaged
resources and their Work sources, generated derivatives and CLAUDE are excluded.
Root README, license, conceptual history and app-local documentation are outside
the named maintained surfaces. No generated workflow index exists for the
retained local input, and none was invented or refreshed.

`tools/validation/test_document_metadata.py` discovers the maintained surfaces,
validates every header against the exact local Draft 2020-12 schema, rejects
invalid/history metadata, preserves package extensions, verifies the schema's
source identity and the frozen workflow bytes, and checks the tagged bootstrap
and CLAUDE pointer. Governance CI runs it with existing App-compatible
jsonschema 4.26.0; no sibling checkout or network schema resolution is required.
Source inspection found no documentation renderer/build or application reader
for these guide bodies. Existing role/entry readers use full text and anchored
section searches, which tolerate the prefix. The compatibility suite and
examination freshness check exercise the existing readers; no current pin or
derivative requires regeneration for these documents. Historical hash-bound
documentary selections retain their frozen subjects rather than being renewed.

The extended focused suite passed 167 pytest cases, including all nineteen live
headers and schema/entry/preservation regressions, plus ten instruction-generator
tests. Deliverables again reported 41/zero errors; the neighborhood query,
eight-file instruction freshness and examination-pin check passed. Header/body
comparison preserved all nineteen pre-header bodies apart from the stated loop
clarification. Extended evidence and the final exact-head receipt are in
`/Users/ryan/dev/chirality-t3/scratch/app-library-v3-headers-3ual3kma/CHECK_SUMMARY.json`.
