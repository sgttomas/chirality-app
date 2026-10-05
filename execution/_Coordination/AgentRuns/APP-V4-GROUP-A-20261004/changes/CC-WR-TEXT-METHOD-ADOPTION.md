# CC-WR-TEXT-METHOD-ADOPTION

2026-10-05. Bounded source adoption prepared by TASK `/root/group_a_execution/runtime_integration` under WORKING_ITEMS `/root/group_a_execution`; no descendants. **Frozen candidate for independent review, not yet an I2 receiving warrant.** This executor recovered the current accepted source/CC promises; it makes no claim of historical design authorship. No App/parser/resource-mirror, shared lib/UI, Cargo/dependency, Root instruction, other Design, authentication, credential, native/model, network or Git mutation.

## Point of need and source basis

WR `workspace-registration.schema.json` `$defs/text_identity.method` constrained all input to the historical `sha256 over UTF-8 text`. TX-4 and `wrproto.tsha`/`compose_start` emitted that label, while reviewed CC-CONTENT-IDENTITY and current ROLE/EXEC select `chirality.app.exact-bytes.sha256/v1` for fresh App source/composed bytes. The prototype body fallback also compared digest values without a method guard. I2's new-method composition could therefore fail WR's receiving schema, or a naive label-only change could infer body equality across methods.

CC-CONTENT-IDENTITY's selected exact-byte method, historical opacity and WR propagation govern this bounded change. WD §6.1 RV-1…5 preserves complete source/package scope and no normalization; ROLE §6.1 separates source bytes from CO-1…5 composition; EXEC §6.3 TR-4's receiving adoption expressly designates exact-byte run-start/end text and says same method/subject/scope permits comparison, missing/different methods unknown/incomparable. WR TX-4/SC-4 are the point of consumption. WR ID-2/RB-1…4's package equality, source revalidation and A15 registration remain independent, unchanged. No algorithm, host identity, canonical package method, human gate or qualification is newly selected here.

## Applied bounded adoption and current receiver API

- Fresh App run-start/end text and `workflow_file.content` use `chirality.app.exact-bytes.sha256/v1`, lowercase 64-hex SHA-256 of exact bytes. Composed text is encoded UTF-8 after framing; WORKFLOW.md is hashed as read stored bytes. No normalization/exclusions; no substitution for the whole package revision.
- `$defs/text_identity` retains `{method,value}`, required fields, no extra properties, and the existing lowercase 64-hex value gate. Only its method gate changes from historical const to nonempty opaque string. Historical and unknown method/value input is accepted as carriage, not as verified source/supply. Other identity schema definitions and package registration algorithms are untouched.
- Existing `run_text.text_identity`, `run_text.workflow_file.content`, and `supply_check.expected_text/expected_workflow/observed_text` fields stay unchanged. `supply_check.state` gains `incomparable`, with native-read observation fields required for that state. The prototype's real `RunDesk.check` calls `text_standing`, retains expected identity exactly, computes observed identity separately and appends a visible method-incomparability limit.
- Different text methods immediately produce `incomparable`, even if digest characters match. If same-method full text differs and body extraction succeeds, body comparison also requires the exact-byte method; a historical body identity cannot provide a value-only fallback. Same-method full-text equality establishes only composed-text supply; it does not compare a separate source scope or prove model adoption.
- Original valid/invalid fixtures remain byte-for-byte unchanged. Their P-63 historical recomputation explicitly uses the originally recorded legacy algorithm solely as a fixture control, never remints/relabels the identity or bridges methods. New synthetic controls are separate `prototype/fixtures/text-method-controls.json`.

These are WR Design/prototype APIs, not an implemented product-reader guarantee. I2 must deliberately adopt this reviewed schema and incomparable semantics before consumption. The product resource mirror remains untouched. Full CM parser repair, actual native history receiving, registration/act/auth evidence and provider/model adoption are independent.

## Meaningful verification

Offline standard-library source checks, `PYTHONDONTWRITEBYTECODE=1`, no Cargo/supplier/model/auth invocation:

1. `python3 Design/prototype/text_method_controls.py`: **6 tests passed**, exit 0. Known abc vector; CRLF/LF, Unicode spelling and trailing-space sensitivity; new/legacy/unknown method carriage preserving inputs; empty/missing method and invalid value refusal; actual compose_start exact stored body and separate source/composed identities; actual RunDesk.check retained legacy/unknown expected identities and explicit incomparable state despite equal digest values; same-method body fallback versus historical-body refusal; historical fixture schema validity and unchanged bytes.
2. `python3 Design/prototype/wrproto.py`: **99/99 passed**, exit 0, including all 137 emitted WR records conforming and existing registration/selection/run checks. This remains a design double: A15/native supplier claims are not upgraded by these controls.
3. Captured historical valid/invalid SHA-256 compared with preimages: exact match. Owned diff whitespace check passed. No other Design or App source changed by this task.

Initial control-harness runs exposed missing synthetic selection fields and an unregistered sibling schema; these harness setup errors were corrected before the recorded final six-test pass. Existing prototype ResourceWarnings for read-only unclosed file handles remain visible in captured stderr; no unrelated prototype cleanup performed.

## Custody, review and limits

`probes/WR-TEXT-METHOD-ADOPTION/` preserves pre-edit owned-source bytes and PREIMAGES.json, read-source hashes, final source seals, and both actual stdout/stderr outputs. Frozen source input hashes are current observations, not historical authorship/custody claims. Independent review is required before I2/App mirror adoption; ordinary method adoption creates no extra human checkpoint. No supply/registration/A15 authenticity, native window/process, actual model following, physical crash or global/host method comparability is claimed.

## Frozen source SHA-256

- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md` — `bd61f48ca97eba9c7665b31ff7506672f18152d57a20b0ffd361a168750af989`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/workspace-registration.schema.json` — `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/prototype/wrproto.py` — `303474582a5192909b7f60e0108009d47efe77fd0477f1ec3c88f00b80fd9c62`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/prototype/text_method_controls.py` — `c5853f53421fc82cc07728b49b1d406eb3e860c15290367d2797542c57229b24`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/prototype/fixtures/text-method-controls.json` — `1b791948fbae6c68fe7b5f6273a310ccf8723294e5e46df025a44341034a6c2e`

Read-only origins are recorded in `probes/WR-TEXT-METHOD-ADOPTION/READ_ORIGINS.json`; historical fixture/source preimages and hashes are in `PREIMAGES.json`. Original CC and earlier evidence remain unchanged.
