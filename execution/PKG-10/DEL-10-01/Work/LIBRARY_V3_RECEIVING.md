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
| Queries work from the stated directory and links resolve | Replaced the placeholder neighborhood argument with DEL-10-01. Check the query and local entry links with the focused verification below. Python/PyYAML and repository-root invocation remain prerequisites. |

App's accepted execution layout, retained local workflows/test inputs, protected
Windows/VM boundaries, credential/download rules and release reservations stay
local. Optional typed headers on App's own init/AGENTS/loop are deferred; those
files have no new metadata consumer to migrate in this adoption. This does not
defer reading the released Library role headers.

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
