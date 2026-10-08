# C3-S4-R1 independent implementation review

## Initial exact candidate: NOT READY

Candidate `30f214d63c5fa4e539664caf9e7604d018a0ca54`, receiving `3d73db745edd3378e0bb254a1b263215ef0861e9`, author `ce1bc1948c8a1f3daa555f734915846dd94694bf`. Author and manager App trees match exactly: `74865e436796a686f1455bdcc6a9f53bb8344d18`. One confirmed blocking P2 remains below. Passing maintained tests do not repair it.

Independent TASK `/root/group_c_successor/cfb_design_review`, parent `/root/group_c_successor`, harness-native descendant, no delegation. Existing isolated reviewer worktree/branch `codex/group-c-reconstruction-code-review` and private serial offline target reused; no clone, new worktree, download, supplier/native act, credentials or MEMORY activity. Only this report is committed. Root/TASK/loop/software-code-review context and source review origins remain in the prior retained review records.

### P2: remount reuses pair/claim keys and makes retained citations ambiguous

Location: `app/src/ConnectorReconstruction.tsx` lines 5–8 (`useRef(0)` and local serial-derived keys), combined with `app/src/ConnectorSourcePanel.tsx`'s conditional format0.4 editor mount and retained parent reconstruction state.

Reproduction: choose format0.4 and add an explicit excerpt pair; it receives key `pairs-1`. Switch to0.3, then back to0.4. Parent keeps the pair but the child is remounted with serial zero. Add another pair: it also receives `pairs-1`. The same sequence for claims reuses `claims-1`; citation checkbox values and React keys no longer uniquely identify entries. Host composition refuses duplicate keys, so the normal format-switch/edit path cannot freeze the intended account, and duplicate claim/pair citations are ambiguous.

Executed actual component handlers through the maintained-style TypeScript transpiler and a minimal hook harness, resetting child refs at remount while retaining its value prop. Observed `{"first":"pairs-1","afterRemount":["pairs-1","pairs-1"],"unique":1}`; assertion that key count equals distinct-key count failed (exit1). The parent conditional mount and retained useState were independently traced. This is a concrete UI lifecycle failure, not native execution.

Repair direction: make newly allocated entry identities collision-free against retained state across editor remounts, without silently renumbering existing referenced entries. Retain an actual toggle/remount handler regression covering pairs and claims/citations, and recheck frozen/cold accounting after repair. Reviewer made no code repair. Manager and original author received the exact sequence before repair.

### Other independent checks on the initial candidate

- Full29-path diff inspected; selected CRR source/schema remain exact. Four source-artifact and fourteen implementation-file hashes match the code basis. The basis's consulted graph hash matches receiving main, not the subsequently updated manager graph; the other three reconsulted context hashes match current bytes. Existing 0.1/0.2/0.3 schema/source bytes are unchanged. Host's receiving-base Exit closing hook remains intact; additive preparation uses the existing project guard and shared registry.
- Default connector Rust checks: **77 passed**. Distribution-successor checks: **78 passed**, comprising all77 maintained checks plus one independent disposable matrix test. No production code changes were included in that test export.
- The independent matrix captured all **58 cold cases** from the exact selected source checker, excluding its hot-buffer-only calls, and sent every account through the production Rust schema/semantic validator. Every expected positive/negative outcome matched. This includes the five repaired source-review regressions and cold-forgery versus provenance limits; it does not stand in for private hot-buffer verification.
- Maintained full npm: **25 passed, one supplier handshake skipped**; nested decision-flow Rust checks **4 passed**. Actual component/handler tests are included. Frontend production build passed; range whitespace check passed. Existing compiler warnings remain distinct from this finding.

Source pins: CRR `40de3420103f9109b611615d10a3335213742a95ca973fd26a5bac94393b9179`; schema0.4 `7fa9002696c62bd1300763f88e0381d120907ee1de8f4fbe15b1e4aba489246c`; constructed fixture `1201571a1eb69cea27bfc5818710adbde84be7e142d962155f07c803b7d5b2bf`; definition checker `a55cb0edfae2c82f69cd261b88b72946d13e40d876d651931dc6175efb8005dd`. Source selection remains the explicit C3_S4_R1_TECHNICAL_SELECTION.md, not the historical source-only integration return.

### Contract assessment and limits retained

The inspected producer generates exact fact statements, checked selected-excerpt pairs and the full mechanical supported list; claims, contradictions and unverified contribution reports are separate. Hot anchors bind original buffers; ordinary citations are not typed RS consumption or actor authentication. Equal excerpts do not prove whole-file equality or substantive stability. Partial/zero-read shapes, generated contradiction consequences, original-byte cold cap, exact1MiB/escaping and unknown-version refusal have meaningful maintained checks.

Existing shared registry code carries0.3 and0.4 through the same final-current freeze, one-payload/64-lifetime capacity, root identity, once-only publication and actual uncertainty custody. Maintained tests exercise cross-version64/65, root/duplicate/incomplete/reread/cancel refusal, final-freeze refusal, real postpublication error and original outcome after session replacement/reconciliation/repeat. No registry reset or performance/authority promotion is introduced. These backend results do not waive the UI defect.

Constructed Git/file operations and mocked handler transport are not native IPC/picker/person witnessing. Same-engine Git, mutable-path/process, CRP uncertainty, generic cold pre-read allocation, capacity sufficiency, full reconstruction/actual duties and external consumer adoption limits remain. No new native witness or release approval follows from this review. Exact repaired candidate and affected independent checks are required before READY.

## Repaired exact candidate: READY for bounded fan-in

Backchecked manager `cfbd16b30a7d814fa9119f8a487f6f00c32807b3`, author repair `3597f32bba534368522c938bdc9a9a91e0093647`. Their complete App trees match: `165fa9eae21184a4c22541ac14c1189ab18a2826`. Only the reconstruction component, its maintained source-presentation test, implementation evidence and basis changed from the initial candidate. All fourteen repaired implementation hashes match. Rust/backend/schema/source/registry/cold-reader bytes are unchanged, so the prior default77/distribution78 results and58-case production semantic matrix remain applicable; no redundant Rust suite is claimed.

The generator now reserves retained row keys and pair/claim citations, including dangling citations, before allocating another key. It does not renumber existing rows or rebind existing references. Independent replay of the original actual-component remount sequence produced `pairs-1`, then `pairs-2`; the distinct-key assertion passed. Additional independent deletion/remount sequence retained a claim citation to removed `pairs-1`, then allocated a different new pair key, leaving the old citation unresolved rather than silently pointing it at new evidence. The new maintained regression exercises the actual parent format-toggle handlers, child remount, both pair and claim identities, existing citations and deletion with retained dangling refs; it passed.

Full maintained npm on the repaired export: **26 passed, one supplier handshake skipped**, including **20 source/route renderer and handler checks** and nested decision-flow Rust **4 passed**. Production frontend build and repair whitespace check passed. The author's earlier failing uniqueness regression is retained in implementation evidence; this independent report preserves its own original failing sequence above. A passing broad run alone was not used to close the finding.

P2 is repaired; no unresolved blocker found for this exact candidate. The fix affects caller-side reference keys before composition, not host-minted account/fact/claim identities, frozen bytes, semantic validation, shared lifetime capacity, actual publication or cold evidence meaning. Existing dangling-reference refusal therefore continues to protect preparation, and recorded/cold account semantics are unchanged. READY is bounded implementation fan-in only: required CI/final metadata review, native witness, actual duties, full reconstruction, capacity assessment and external adoption remain separate. No launch or frozen witness-artifact modification occurred.
