# V0-H — independent review of frozen CC-H

Date: 2026-10-04. Reviewer: `/root/group_a_execution/hosting_contract_review`, independent TASK descendant of `/root/group_a_execution`, delegated-harness-native collaboration; no descendants. Root resolved using `git rev-parse --show-toplevel` to `/Users/ryan/.codex/worktrees/077c/chirality`. Write boundary: this review only.

## Candidate and standing

Reviewed original sealed `changes/CC-H.md` SHA-256 `8890040d5121d43ae40d49f5ddf5e228ea20abfff6aedec5681817f05fe3187e` and its 27 candidate output hashes. All 27 matched before source examination and execution. Reviewed bounded diff from `e916ad1789` for both DEL-01-01/05 Design fences, including schemas, prototypes and fixtures; the two newly untracked rejection fixtures were included from the manifest. Other moving CC candidates were not assessed. No stock Codex execution, credential use, live turns, external network, downloads, Git mutations or shared artifact changes.

Disposition: **repair before fan-in of this frozen package**. Three major findings below; no separate critical blocker and no minor finding. The substantive H5 representation, LT-24 readiness exception, three-part normal verification obligation and thread-start disclosure are coherent definition directions. Findings concern an incompatible schema identity and the changed package's own executable consumer/evidence gaps. They do not reject the definition merely because product or other Design consumer propagation remains ahead.

The manager was told the original source snapshot was complete before supplier advancement could begin. A subsequent read observed the server schema already changed to v0.10; that is a repair observation, not an independently reviewed successor. This report deliberately retains findings against the sealed original. Seal successor hashes and recheck changed areas before disposing them.

## Major findings

### H-M1 — incompatible server-request schema reuses its prior identity (blocking)

Location: DEL-01-01 `Design/hosting.server-request-entry.schema.json:3,12` in the original frozen candidate. `$id` remains `urn:chirality:del-01-01:hosting-boundary:v0.9:server-request-entry`, the same as `e916ad1789`, while `generation` changes from integer to a closed object. By contrast lifecycle/client IDs advance from v0.8 to v0.9 and access state/network IDs from v0.2 to v0.3.

Trigger/impact: a validator registry or reader retaining the old v0.9 resource and a consumer loading the new v0.9 resource resolve the same identity to incompatible contracts; valid old integer entries are rejected by the new bytes with no schema-identity discriminator. Candidate-output hashes identify bytes but do not fix ambiguous schema references. This undermines CC-H's propagation instruction to update schema ids/consumers without silent fallback, and historical/read-version treatment.

Repair: give the changed server-request schema a fresh identity (for example v0.10), name old-versus-new read/adoption treatment in CC-H, and propagate that identity through actual registries/consumers/fixtures. Preserve the old schema as historical wherever historical records require it. Check one old integer entry and one new composite entry against their respective identities. The later observed v0.10 edit is a plausible repair but still requires a sealed successor review.

### H-M2 — access consumers export one fixed session for independent App instances (blocking for CC-H model/consumer completion)

Location: DEL-01-05 `Design/prototype/access_model.py:434,609`, with `App.__init__` at 230. Both state and network exports construct `appSession: "prototype-session"`; the network function has no session input and the App model owns no session identity. Home uses a role value as the identity without receiving an actual boundary generation.

Reproduction on sealed bytes: two independent `App()` instances each export exactly `{"appSession":"prototype-session","home":"account","spawnCounter":1}`. `network_view([], plugins_setting({}))` exports that same identity. Schema validation accepts these records because each object has the required fields.

Impact: adding object shape does not exercise H5 uniqueness across launches or show that access/network records identify the hosted child; separate runs collapse to one identity and cannot join correctly to a Boundary whose appSession is a generated UUID. CC-H's direction that all access-state/network consumers carry the full identity is therefore not realized even in its own changed model. This is an executable model defect, not an observation of deployed App behavior.

Repair: bind access exports to the actual supplied hosting generation or an explicit App-owned session/home identity, using the same session across its homes and a fresh session across launches. Network export must receive that identity rather than fabricate another. Add two-session, two-home and repeated-export checks, including equality of hosting and access/network identities for the same child. Fixed fixture values may remain explicitly invented examples.

### H-M3 — hosting answer consumer cannot consume the full identity it exports (blocking for CC-H model/consumer completion)

Location: DEL-01-01 `Design/prototype/boundary_model.py:663–666`, against exported `records()` and delivered envelope conversions at 489/756. `answer(..., generation=...)` still indexes its integer-keyed cache using the argument directly.

Reproduction on sealed bytes: start `new_boundary()`, obtain `b.generation_identity(b.generation)`, pass that object to `b.answer('does-not-exist', {}, {'class':'app-rule','ruleName':'example'}, generation=object)`: `TypeError: unhashable type: 'dict'`. Passing the old integer returns the intended `refused(no-such-request)`. A real receiver returning the generation from a delivered/register export has the same problem before any refusal/settlement logic runs.

Impact: the package's changed boundary export and its answer consumer disagree. The current tests use internal counters and never return the exported composite object, so their stale-answer and refusal passes do not establish composite identity compatibility. Keeping integer caches inside one session/home is permissible; accepting an external object's counter without checking its session/home would not be.

Repair: validate/resolve the full supplied generation at the public answer boundary, compare all three elements before looking up an internal counter, and refuse an identity from another session/home or a closed spawn. Keep any integer-only helper explicitly internal. Add an exported identity round-trip for a valid outstanding request plus stale/cross-session/cross-home requests with reused supplier request ids; assert refusal and no written reply or settlement mutation.

## Checks and supported conclusions

- Original manifest: 27/27 output hashes match; change-record hash matches supplied seal.
- Hosting original suite: 36/37 passed under sandbox. The only failure was unchanged `obs1_doubles`, `PermissionError(1, 'Operation not permitted')` at local Unix socket bind. Authorized identical fixture rerun outside sandbox passed: MCP initialize/list/call/errors/receipt and CLI exit/result/local socket all asserted. No test was changed or dropped. This is 37 exercised model results with the local fixture rerun separately, not a single all-pass suite invocation.
- Hosting table coverage: 24/24 lifecycle rows and 13/13 register rows; 268 emitted records validated; 79 constructed/mutated frames valid against committed 0.158.0 bundle. This is model assurance only.
- Access suite: 10/10, including thread-start classified `purpose: model`, and 16 emitted records validated. The suite does not catch H-M2.
- New counter-only and missing-session fixture purposes were read; final separate validation rejected them for object type and missing appSession. That validation occurred after source snapshot completion, so it is supplementary rather than a new seal of all candidate outputs.
- `git diff --check` across the Design fences passed. It does not establish semantics.
- Independent targeted reproductions above used Python standard library and existing prototypes only. One attempted helper call used nonexistent `validate`, then was corrected to the validator's actual `errors` API; no conclusion relies on the failed attempt. The corrected schema comparison observed a successor v0.10 edit and is not attributed to the frozen v0.9 bytes.

CI-7 definition preserves HOSTING §7.2's declared/observed label + expected distribution identity + generated-output pin rule. LT-04 remains verified-only; LT-24 requires explicit development choice, observed label, unverifiable standing and no known mismatch. The model refused unverifiable without opt-in, then used LT-24 with opt-in, and refused a mismatched label even with opt-in. Ready announcement and lifecycle through closure retain unverified-development standing. Hash-only product verification remains an explicitly named propagation defect, not discharged by this review. Product tests must cover each missing/mismatched component, restart, contradictory handshake and complete match.

CI-8 definition correctly adds thread-start phase without inventing a turn, narrows plugin-off language, keeps reported historical N-1 observation distinct from expected-at-pin and actual sampled sources, and preserves lower-bound limits. Prior N-1 in `app/EVIDENCE.md` describes the 0.158.0 default-provider websocket 401 and later loopback sampling; no fresh supplier observation was made here. No veto, provider substitution, new default, approval/sandbox mandate, credential custody change or obligation narrowing appears in the reviewed diff. The access prototype's static expected list still contains only plugin/remote-control rows; model prewarm classification is tested using a scripted observation. When product prediction is implemented, test provider-dependent expected rows separately from actual contact, without claiming a universal destination or internet absence.

## Adoption and reserved work

CC-H's located consumer inventory is a useful bounded adoption starting point. DEL-01-02 needs composite durable/correlation keys and supplier standing; DEL-01-04/NIR needs request actions and display; DEL-04-03 needs hosting-record ingestion; DEL-03-03 needs thread/channel destination information. CC-A owns its moving NIR consumer and must adopt the reviewed definition; this review neither assesses that moving candidate nor treats its remaining work as failure of CC-H definition readiness. GUIDE hash pins should be reconciled last; packaging and qualification readers must receive exact reviewed schema identities.

`app/src-tauri/src/hosting.rs`, `App.tsx`, offline schema tests and documentation remain manager-owned propagation. No integer fallback, session/home truncation, hash-only verified status, missing development standing or invented turn/model observation should survive that work. Consumers outside Group A require owning-loop adoption and GC-8 graph notices, not silent edits by this reviewer. Supplier advancement to 0.160.0 requires its own source identity and affected checks; this 0.158.0 review confers no qualification, implementation readiness, product default decision, owner acceptance, stage gate or release.

## Actual reading origins

Root instruction content was supplied in this session; actual Root path/hash is recorded below. TASK, software-code-review skill, LOOP_INIT, current-edition index, manual headings through level 3, full Field Book, selected Group A graph, acceptance, GC rulings, owner decisions, both SoW requirements/criteria, R18/R19 generation/home and user-choice passages, full bounded changed source/fixtures, CC-H and V0-BASIS targeted obligations, and N-1 were consulted. No other role body was activated. Full-file fingerprints identify observed source bytes, not a claim that every unchanged line was read. Candidate identity is the original sealed manifest above, distinct from subsequently changed sources.

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `.agents/skills/software-code-review/SKILL.md` — `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28`
- `docs/alignment-manual/README.md` — `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md` — `0d8e5b2774c26cde277fbb98b394fdc74a4bf6c171f1fea89904d7a6062565e8`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GC_RULINGS.md` — `22187acaffb9a0e2c5ef6ed415cce0c62c6e6db06361405cf8caf642b5a59a92`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-BASIS.md` — `3d9644efdd2086630b6c319871c54d3eb0239d80d131f43083d0927b2270b906`
