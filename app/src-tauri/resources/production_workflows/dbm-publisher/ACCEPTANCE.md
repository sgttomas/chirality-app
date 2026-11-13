# dbm-publisher acceptance

A DBM publication run is valid only when all of the following are true:

1. `EXECUTION_ROOT` is one accepted DOMAIN execution root.
2. The active root `Handoff_State.md` and latest audit evidence support publication-phase consumption before any section synthesis runs.
3. `Publication_Input_Manifest.md` exists and freezes exact content inputs, `DBM_OUTPUT_MODE`, and admission / closure evidence before any section synthesis runs.
4. Gate 1 records whether the run is a `CLEAN_RESTART` or `TARGETED_RERUN`; abandoned, rejected, superseded, or quality-limited publication outputs are not reused unless the human explicitly approves a bounded targeted rerun against an accepted baseline package.
5. `DBM_OUTPUT_MODE` defaults to `FULL_ENGINEERING_DBM`; `DBM_DIGEST` is valid only when explicitly selected by the human and recorded in the manifest and publication rules.
6. `Publication_Schema.md`, `Publication_Rules.md`, and `Section_Map.csv` are human-approved before section dispatch.
7. `Section_Map.csv` rows only reference exact artifacts named in the frozen input manifest and mapped KTY-local files.
8. Publication content authority follows the approved stack. The original DBM is never treated as current-state design-basis authority.
9. Detailed traceability appears only in the appendix/QA outputs, not inline in the rewritten DBM body, but material engineering design-basis content remains in the body.
10. Every required section has exactly one current section output bundle when package publication is run, including section body and QA outputs.
11. In `FULL_ENGINEERING_DBM` mode, every required section has section-level `Design Basis Content Coverage` and `Table Treatment` QA records.
12. In `FULL_ENGINEERING_DBM` mode, package publication emits `Publication_Content_Adequacy.md` with the fixed schema in CONTRACT.md.
13. Post-authoring evidence bundle review (`TASK + dbm-postauthor-concordance`) runs after package assembly and produces candidate findings for human disposition. Human dispositions are recorded in `Publication_Review_Disposition.csv` before pointer updates.
14. `Publication_Handoff_State.md` exists in the accepted package snapshot before `_LATEST.md` is updated.
15. `_LATEST.md` is updated only after explicit human acceptance of a package snapshot.

Invalid behaviors include:

- guessed decomposition filenames or directory assumptions when the manifest can freeze explicit paths,
- use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as factual publication authority without human promotion (exception: `_Aggregation/Hypergraph/` may be consumed as auxiliary structure evidence when explicitly admitted in the manifest via `HYPERGRAPH_USE_MODE != NONE`; `_MEMORY.md` may be read as non-authoritative operational context when `_STATUS.md` is read),
- asking `build_section_map.py` to interpret free-text inclusion/exclusion prose,
- letting `dbm-publish` act as a dispatcher,
- treating `_STATUS.md >= INITIALIZED` as sufficient publication admission without frozen root closure evidence in the manifest,
- silently reconciling conflicting mapped inputs without explicit authority,
- publishing `DBM_DIGEST` output as the default governing full DBM without explicit human mode selection,
- allowing QA scaffolds, assertion registers, raw caveat dumps, path inventories, or trace mechanics to stand in for a DBM-native body in `FULL_ENGINEERING_DBM` mode,
- treating provenance appendix relocation as permission to omit material engineering values, constraints, design-basis tables, assumptions, TBDs, or interfaces from the body,
- mutating KTY-local truth during publication,
- publishing pre-SCA or superseded state as if it were current,
- reusing abandoned, rejected, superseded, or quality-limited `_Planning`, `dispatch`, `sections`, or `package` outputs as working authority without an explicit Gate 1 human decision,
- updating the accepted package pointer before human acceptance or before `Publication_Handoff_State.md` exists.
