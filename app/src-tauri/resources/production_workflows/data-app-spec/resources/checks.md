# data-app-spec: checks

## Before checkpoint A

1. Every stated purpose, use, non-use and constraint traces to the human's words or to an identified source.
2. The proposed tier names its consequences, its detectability and the accountable role.
3. The source inventory states, for each source, what it can support and the permitted observation or use.
4. In `derive` mode, the reference app is identified: deployment URL, observation date, and source repository and revision if public.

## Before the design checkpoint (new and revise modes)

1. Every need, decision, obligation and non-use traces to the human's words or an identified source; agent interpretations are marked as such.
2. Every need, decision and activity has at least one option. Each consequential trade-off shows at least two.
3. Every chosen pattern's authoring questions are answered with grounds or recorded as gaps naming who can answer them.
4. The tier proposal cites its error consequences; the non-uses are stated.
5. `check_design.py` reports no errors on the design record and catalogue. Each proposed ruling's digest is in the presented record.
6. Every answer that is a domain or professional judgment names the authority that must rule it (`authority`), and is presented to that person.
7. Obligations that only a human act can meet, such as authentication, are listed as conditions of acceptance.
8. The sketch shows each activity's steps in order and labels each element with its need.

## Before checkpoint B

1. **Validation of the exact frozen bytes.**
   - The canonical `appspec.json` validates against the bound schema release.
   - The semantic validator reports no errors.
   - Its output is in the candidate.
2. **Closure lock.** Every pinned asset, dataset, product manifest, component bundle and pack resolves, and its hash matches.
3. **Buildability.** One of two verdicts is stated with reasons:
   - buildable for the accepted coverage;
   - not buildable, naming the blocking gaps, undecided or unruled fidelity decisions, placeholders and extensions.
4. **Design trace (new and revise modes).**
   - `check_design.py --spec` reports no errors.
   - The trace is complete.
   - Every choice the specification relies on is bound.
5. **Grounds.** Every consequential element has grounds or an explicit standing:
   - criteria and their editions;
   - method choices;
   - parameter values;
   - units;
   - CRS.
6. **No flattening.** No TBD, assumption or conflict has become settled prose.
7. **Domain knowledge.**
   - Every criterion, method and parameter table used comes from an accepted pack or is examined here.
   - Conflicts are open or ruled; none is resolved silently.
8. **Analysis components.**
   - Every component has the known-answer tests its tier requires.
   - Each test names its oracle, source, tolerance rationale and confirmation status.
9. **Examination.**
   - The independent examination ran on the frozen candidate.
   - Its findings are repaired and backchecked, or presented unresolved.
   - The tier's domain and professional reviews are complete, or their absence is stated as blocking.
10. **Acceptance and provenance.** The specification records no acceptance of itself, and the provenance policy reads acceptance status from the decision record.
11. **Decision record.** `DECISION.md` fields stay empty until the human responds.
12. **Canonical form.**
    - `appspec.json` was produced with the validator's own parser.
    - Its equivalence to the authoring form was checked.
    - The validation output in the candidate is for the JSON file, parsed as JSON.
13. **Rulings before freeze.**
    - Every departure the agent recommends has the human's ruling.
    - No recommendation is carried as an `x-` extension.
14. **Layout sizing.** The specified viewport sizes and each area's height behaviour are stated.
15. **Reference evidence (`derive` mode).**
    - Every computed output observed in the reference is reproduced from the specification's rules, or the residual is stated.
    - Every widget's complete rendered state is captured and cited, including chart layout, legends, and empty and error states.
    - The reference's own data download, where offered, is reconciled to the primary source.

## Failure reporting

| Status | Use when |
|---|---|
| `FAILED_INPUTS` | Missing decision-maker, mode, ontology or schema identity, or write permission |
| `BLOCKED` | A required review is unavailable, or the reference cannot be observed enough for the selected mode and no ruling re-scopes it |
| `READY_WITH_GAPS` | Accepted coverage is buildable but stated gaps remain outside it |
| `NOT_BUILDABLE` | Valid and examined, but build-blocking gaps or decisions remain; still presentable for limited acceptance or return |
