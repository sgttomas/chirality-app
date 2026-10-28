# I3-POLICY R1 — review repairs

TASK `/root/group_a_execution/policy_standing_production`, parent `/root/group_a_execution`; same gpt-6.1-sol medium, delegated-harness-native descendant, no descendants. Actual repair turn under manager's bounded authorization. Read saved `reviews/V2-I3-POLICY.md` after its initial save was unavailable. No instructions, ScopeOfWork, Design, graph, lib, Cargo, shared validator, Git, credential, network or native-control writes.

I3P-1 repaired: `phase_one_overlay` excludes A12 from ordinary content-lapse transitions (ACT §2.5, §4.3, RS L-0/L-12). Its admitted performed arrival stays performed before/after resume and after run end. An inconsistent incoming generic content-lapse flag is retained visibly as `evidence_limit`: “content lapse reported for A12; not applicable — setting standing requires control evidence”. This annotation establishes no current control state or actual supersession. Setting/current-control observation and performed checkpoint disposition remain distinct.

I3P-2 repaired: fallback labels exhaustively preserve all eight admitted dispositions. Lapsed reads “act lapsed”, Invalid “invalid checkpoint”, NotEstablished “not established”, NotReached “not reached”; Waiting/Performed/ResolvedNegatively/Unknown retain their precise labels. Declaration findings and unknowns create no hold.

Exact reviewer reproductions use the unchanged inputs with the required contract oracle, including governed=false, alleged generic lapse=true, A12 before resume and after run end, and A4 ended projection of Lapsed/Invalid/NotEstablished. Tests also repeat that projection, exercise every label, retain ordinary A4 lapse controls, and contrast an admitted established A12 successor (prior direct becomes propose) with pending/refused/requested changes preserving the prior effective direct setting. The original review defect evidence and initial tests were not weakened.

Original candidate source/test/log/candidate bytes remain under `review_history/r0/`; original `candidate.json` and `test-output.txt` remain unchanged. Successor module/test/output hashes are `candidate-r1.json`. Canonical combined output is `test-output-r1.txt`.

Final command from repository root:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test policy_standing
```

Exit 0; **14 passed, 0 failed** (13 own tests plus shared validator module test), 0.39 seconds test execution. Manager granted exclusive Cargo slot and received release. An earlier R1 run after initial correction passed before adding exact-input/repeated-projection/evidence-limit coverage; the final successor result supersedes it. No actual capture, native admission, control enforcement, host operation, cold replay or whole-deliverable completion is claimed. Same independent reviewer backcheck remains required.

Source changes: only standing.rs and tests/policy_standing.rs. act_policy.rs is byte-identical to the reviewed original. All initial integration prerequisites in changes/I3-POLICY.md remain. Consumer wiring must display the added optional evidence_limit alongside the checkpoint observation.
