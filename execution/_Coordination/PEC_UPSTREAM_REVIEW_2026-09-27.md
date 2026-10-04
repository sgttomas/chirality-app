# PEC upstream comparison — independent affected review

**PASS — no actionable findings.** Reviewed 2026-09-27 by fresh terminal TASK `/root/renewal_research_strategy/pec_comparison_review`, independent of the author, under WORKING_ITEMS `/root/renewal_research_strategy` and HELP_HUMAN `/root`. This is an agent review, not owner acceptance, PEC qualification or App Group1 confirmation.

## Candidate and source identity

Base/source pin: `acc7d3cc7f5183152752c35995c73ad34673011b`; branch `codex/app-v4-pec-upstream-comparison-20260927`. Reviewed the ordinary four-file working diff plus the untracked comparison account. Final authored candidate SHA-256 identities, relative to `projects/chirality-app-v4/`:

| File | SHA-256 |
|---|---|
| `README.md` | `52ef37d4a5f8e0c609ae1f04ba97805f4ac64aec4bab1d0cfc8ade077c45608d` |
| `execution/_Coordination/PEC_UPSTREAM_COMPARISON_2026-09-27.md` | `a8b8fd9c7d898b53b5de51f61b4bfdef36373c774f345e2f573af147e84d28ea` |
| `execution/_Coordination/WorkGraphs/APP-V4-PROJECT-DEFINITION-20260926/WORK_GRAPH.md` | `30511a2428afeb2ba9e23cb6e9c552077e598e79c29268f2dfc2bb345ce8f620` |
| `execution/_Decomposition/External_Dependencies.csv` | `1a6e3f5de5241d66e99ae8019b480d9ce1f05a5abffb202a76946816b6555187` |
| `execution/_Decomposition/Open_Issues.csv` | `2540ab76b737fd1454bb7aae6ade865e66d57ca073e7997ebd49c5d2a9bc187c` |

## Evidence and result

- Read the POST-SCA005 receipt, D107 owner direction/freeze and follow-on graph, and S1/D1/X1 handoffs at the pin. Local Git confirms PR1014 merge `974bf7da496ca2a8deede7731222f037cca4655a` and App correction PR1011 merge `8bbd022b98140e2128b6132bf661786ee3a8d108`. Completed undertaking and applied acts are correctly separated from writing-time handoff status, artifact review/re-acceptance, qualified release and receiving adoption. D107 leaves TM1/RV1 and residual decisions with PEC; the App comparison does not take them over or impose a blanket PEC hold.
- Checked varied consequential primary claims: DEL-02-01 REQ-002/007 requires declared feed coverage; DEL-03-01 REQ-007/008 and CON-005 preserves the explicit full-rebuild coverage question; DEL-03-03 REQ-015–017 and CON-006/007 distinguishes terminal merge lag, non-terminal drift and unchanged declared history without inferring missing snapshot facts. The comparison accurately preserves these qualifications.
- Checked PEC PRD PEC-K-01/02/03/11, PEC-ORI-007, PEC-API-007 and §12; DEL-04-03 REQ-001/016–023; DEL-04-05 REQ-013/CON-001–004; DEL-08-06 REQ-013–015 and its cited TBD/CON items; and DEL-10-13 CON-004. Optional use, receiver-side total absence/file fallback, separate three-field stamp/reliance declaration, publisher ownership and unresolved exact query/release terms remain intact. No ready interface, shared authentication, network field or live Runtime feed is invented.
- Compared D105 SPEC/ADRs with App `docs/ARCHITECTURE.md` V4-ARC-01/03/10. The final account expressly qualifies PEC/compatibility Runtime premises without restoring App v4's excluded v3 Runtime service; the selected Codex/minimal-host direction stays unchanged. This existing source-basis difference is not converted into a new governance proposal.
- The `c5d852c4a`→pin range contains 34 PEC v2 parser fixture/test files and the `software-workflow.json` check registration, with no change to PEC PRD, v2 production source/contracts/config or tier-0 profile. The test-module introduction expressly limits its evidence to fixture integrity. No product test was run in this review, and local registration is not presented as hosted execution or parser qualification.
- Parsed both CSVs: only DEP-002 and OI-022 change; row counts remain 6 and 26. ScopeLedger is byte-identical to HEAD: 262 IDs, 234 IN / 15 OUT / 13 TBD. The candidate touches no accepted seed/composite, thesis, prior candidate or product document. Workflow comparison and actual Group1 confirmation remain pending. The prospective domain-engine report is kept distinct from D107 consumer-contract consideration and K3 publication; it establishes neither delivery nor a waiting gate.

## Provenance and limits

Native harness delegation executed this review; its one-file write scope and read-only source scope are brief restrictions, not a claimed host sandbox. No delegation, source edit, Git/network mutation, external-session contact or unfinished-worktree inspection occurred. Parent-transcribed owner messages and the parent's read-only PR-list observation retain their stated custody limits; this review did not independently query that listing. The earlier scout's target-by-target postimage matching is credited as separate evidence, not re-claimed as this review's work. This review covers the five bound files; subsequent substantive changes need affected checking.

Instruction origins actually read, rooted at `~/.codex/worktrees/077c/chirality` (SHA-256): `AGENTS.md` `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd`; `agents/AGENT_TASK.md` `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`; selected `.agents/skills/chirality-change/SKILL.md` `1a2b056263ec77e4104efdf99afe3fe76dda792334a243fb2f21c60bc9c81450`; read-only PEC source-context `projects/pec/AGENTS.md` `df9196d152a01afe59b388111ae0a14381b4ad74f280e95f9c44a1eaee925eb8`. No other role or workflow body was selected.
