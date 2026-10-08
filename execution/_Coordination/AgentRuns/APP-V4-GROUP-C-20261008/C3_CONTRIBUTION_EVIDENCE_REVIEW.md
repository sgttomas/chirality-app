# CCE source proposal independent review

Verdict: READY AS A REVIEWABLE PROPOSAL; IMPLEMENTATION HELD.

Exact candidate: `fcfdfee7eb5b4b3d4b0d024611062d44047f98fe`; basis `cd79d9b477f7f33aa4d7a3683e26e6337039d412`. Independent TASK under Group C WORKING_ITEMS, existing harness-native child; no descendants. Six additive files only. Existing App code, formats 0.1–0.4, CAM and CRP are unchanged. This verdict does not select lifecycle A, release implementation, authorize a target write, qualify native execution, or establish actor truth/performance.

## Retained preliminary findings and repairs

The preliminary draft was NOT READY on the following points. These findings remain historical, rather than being replaced by the final passing result.

1. Parsed Host Value serialization was described as original RPC bytes. The proposal now distinguishes exact decoded input/message UTF-8 from `sha256:host_parsed_frame_json_utf8`, with its pinned serialization method. Original wire spelling is not reconstructed or claimed. The retained wrong-wire-method negative rejects it.
2. Requiring a live source at final freeze could strand an already observed graph outcome. Previously minted, same-process observations may now be archived as historical after source closure. Closure permits no new mint, turn, write, retry, or cold capability restoration. Closure before operation mint retains the original uncertain attempt and gap, with null integration even if later file bytes happen to match.
3. A shape-valid but semantically invalid base 0.4 account was accepted after coherent digest rebinding. Reproduction: replace `facts[0].statement` with `INVENTED invalid CRR fact`, serialize the base, update its length/hash, update the answer account hash, and recompute answer artifact length/hash and receipt content hash; use answer-only state. The draft accepted it. The frozen checker invokes the unchanged owning CRR semantic validator and rejects the same fully rebound mutation.
4. Same-generation contribution stages reused positions 2/3 with different hashes, and conflicting event locators were accepted. Reproduction: give the review item source the answer item source identity while retaining its different digest; separately copy all four answer dispatch/item/terminal/response positions into the review receipt. Both now reject. Sequential fixture stages and per-generation source/position consistency plus causal floors repair the original ambiguity. Numeric positions are not compared across unrelated generations.
5. Source closure before integration was conflated with explicit cancellation. Historical answer-only and review-only records are now permitted on closure; explicit pre-dispatch cancellation discards the active set. After dispatch, outcome retention applies. Both historical partial states pass the frozen consistency checker without acquiring integration standing.

## Exact checks and basis

Independently executed the frozen checker: 51 definition consistency cases passed. Separately reconstructed eight probes: fully rebound invalid base; conflicting event identity; reused stage chronology; three leading-zero position variants; historical answer-only; historical review-only. All eight produced the expected rejection or acceptance. These are constructed cold consistency checks, not native mint, authority, lifecycle, or writer qualification.

Independently retrieved and SHA-256 checked all 19 consulted source blobs at the recorded basis revision and all five candidate artifact blobs against `C3_CONTRIBUTION_EVIDENCE_BASIS.json`; all matched. The six-file additive diff establishes unchanged previous formats and App inputs. Scoped RS concurrence was retrieved from manager commit `7465b7def1` and matched `b9041b59c2b84e63ec14c681b346283b33ab5b896c67c56fb04117be9c1e40c3`.

Exact artifact SHA-256 values:

- CCE-v0.1: `71bdbfa0538ed335bef97e0ab11f3180b2b49628174f285dc9f9dbd32e329bc4`.
- Contribution-message schema: `3c11053965d864b78d274993629564d77ee90baf8da63049692f8744627c8b87`.
- Account 0.5 schema: `327ca15977a73a6b6d2f72ed27fde07259f4ba6c4ea9781d4ca17ad72b860108`.
- Fixture: `08b5fa515b35a92c889a1b69ed71e9d9c1a613598bf9c4933e5e8e807ad434cc`.
- Checker: `f7895b1778141235c0d71c407254c1aa26a590413557ce00cbdf9234b5c67ba9`.

Review instruction basis: Root/TASK/App loop/chirality-change hashes are retained and verified in the candidate basis; selected software-code-review skill SHA-256 `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`. Review used the existing isolated reviewer branch. No code edits, build, download, native action, supplier session, or target write occurred.

## Meaning and implementation holds

The proposed chain distinguishes an immutable recorded 0.4 subject, actual request-bound agent emission, separate manager review, and an observed destination update. Valid JSON, invented origin locators, history pages, injected messages, fork-carried history, role labels, and cold records cannot mint authorship. The checker deliberately demonstrates that internally consistent fabricated locators can pass cold checks; private live custody must supply the missing warrant. Claim citations and manager disposition do not establish source truth, personal identity, human acceptance, duty performance, or exclusive causality.

The review binds exact answer bytes and the insertion plan. Dedicated review-hash placeholder substitution avoids a self-reference cycle. Independent preimage and two agreeing post-write reads, expected prefix/block/suffix, literal target and actual completed fileChange evidence remain required. Native writer instructions and observed reads are not descriptor-bound write containment or proof of no other writes. Unexpected outcomes preserve uncertainty without automatic rollback or retry.

Lifecycle A remains PROPOSED OPEN. Its one active set/one payload/final existing slot accounting is a proposal, not an implemented capacity change. PM05 prefreeze process loss remains explicit: final cold readability does not make the whole workflow recoverable. Alternative B is compared, not selected.

Target authorization requires the project owner's accepted task scope plus exact manager target selection. No accepted machine-readable grant or scope-owner-to-App custody bridge currently exists. Role selection, renderer paths, free text, filesystem access and method selection cannot replace that bridge. This is a separate implementation hold. The new private Host/RoleBinding/SourceRequest/live-frame capability join also needs actual implementation and independent interface review; current primitives alone do not supply the combined capability. RS concurrence is bounded and conditional, not a release or qualification of that future seam. Supplier version labels and these synthetic checks do not qualify actual native behavior.

No remaining source-proposal blocker was identified after the recorded repairs. Parent technical selection and resolution of the explicit implementation holds remain necessary before implementation release.
