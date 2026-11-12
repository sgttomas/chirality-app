---
name: dbm-concordance-verify
description: Review semantic consistency across an authored DBM's sections, using current text and available review evidence; supports publication packages and standalone drafts.
metadata:
  kind: instruction
  surface: workflow
---

# dbm-concordance-verify

Load [CONTRACT.md](CONTRACT.md) when preparing the brief or validating the result.
This is a reasoning-only review; its execution configuration permits no shell
commands. The caller prepares readable Markdown and any mechanical evidence.

## Purpose

Review the complete authored DBM for semantic agreement across sections. Compare
repeated values, equipment configurations, scope assignments, interfaces,
operating cases, protective functions, terminology, and uncertainty in context.
Use available post-authoring review evidence to guide attention, while reading
the entire document rather than treating extracted claims as exhaustive.

The workflow accepts a pipeline-produced `Rewritten_DBM.md` or a human-prepared
Markdown draft. A DOMAIN structure, publication planning artifacts, frozen
concordance register, and per-section assertion CSVs are not prerequisites.
Internal agreement does not establish correctness against external sources,
regulatory compliance, completeness of the design basis, or publication acceptance.
Those assessments belong to their separately commissioned reviews and the human.

## Inputs

Required:
- `ASSEMBLED_DBM_PATH` — complete authored DBM in Markdown, including body tables.
- `REVIEW_OUTPUT_DIR` — caller-authorized review directory.
- `OUTPUT_VERIFICATION_PATH` — markdown report under that directory.
- `OUTPUT_VERIFICATION_FINDINGS_PATH` — findings CSV under that directory.

Optional:
- `SECTIONS_ROOT` — current section bodies and QA records from the same assembly.
- `REVIEW_EVIDENCE_ROOT` — post-authoring evidence bundle from the same document.
- `SECTION_MAP_PATH` — approved section identities and contribution scope.
- `PUBLICATION_RULES_PATH` — approved terminology, uncertainty, and restatement rules.
- `PUBLICATION_INPUT_MANIFEST` — admitted input/provenance context.
- `SOURCE_SUPERSESSION_FINDINGS_PATH` — existing source-fidelity review findings.
- `PACKAGE_SNAPSHOT_PATH` — additional package containment boundary when applicable.
- `CONCORDANCE_REGISTER_PATH`, `CONCORDANCE_FINDINGS_PATH` — explicitly supplied
  legacy evidence for a historical/resume comparison; never required or inferred.

The contract defines path handling, evidence limitations, outputs, and an example
standalone brief. Optional evidence can extend the comparison but cannot replace
reading the authored document or silently acquire content authority.

## Method

1. **Validate scope and inputs.** Confirm the authored document is readable and
   both distinct output paths resolve within `REVIEW_OUTPUT_DIR`. If a package
   boundary is supplied, confirm the review directory is also within it. Refuse
   an output path that aliases any input. Identify the complete heading/section
   inventory from the document; use approved section IDs when available and
   heading plus line anchors otherwise.
2. **Check evidence provenance.** Read supplied planning and review evidence.
   Check that section bodies and bundle provenance correspond to the authored
   document being reviewed. Missing, stale, malformed, or contradictory supplied
   evidence is a limitation, not permission to substitute another document.
   Continue the unaffected authored-text review and report `PARTIAL` where a
   requested comparison cannot be completed. Absent optional inputs that were
   never supplied do not make a standalone consistency review partial.
3. **Discover shared assertions after authoring.** Read every section and table.
   Group claims by engineering meaning, facility/system, design or operating
   case, conditions, and uncertainty status. Assign descriptive `AssertionKey`s
   to these groups. Distinguish design limits from operating targets, per-unit
   from total capacity, gauge from absolute pressure, existing from proposed
   equipment, and different facilities or modes. Claims extraction and legacy
   keys are aids; discover relationships absent from those inputs as well.
4. **Compare sections in context.** Review each shared assertion across its
   occurrences, including prose-to-table relationships and implied interfaces.
   Explain any normalization; call a difference a normalization artifact only
   when units, datum, conditions, precision, and engineering meaning justify
   equivalence. Do not invent tolerances or infer a common datum. Preserve
   differences between assumptions, TBDs, and confirmed statements.
5. **Assess implicit conflicts and coverage.** Inspect configurations,
   responsibilities, interfaces, control/protection narratives, and uncertainty
   for contradictions beyond repeated numbers. Report `COVERAGE_GAP` only when a
   stated interface, approved section purpose, or explicit cross-reference
   establishes the missing relationship. A fact need not recur in every section.
   Unestablished external completeness remains a limitation.
6. **Interpret supplementary evidence.** Explain relevant tool findings in the
   current prose context. If a legacy register was explicitly supplied, account
   for every key, including keys absent from current text. Per-section assertion
   and discovery CSVs are optional corroboration, not required worker outputs.
   Do not resolve a contradiction by choosing an unsupported authoritative value.
7. **Emit and return.** Write the two fixed outputs. Report sections examined,
   assertion groups compared, evidence limitations, and all candidate findings.
   The caller presents observations for human disposition and records decisions
   in the undertaking's review record, citing observation IDs. This workflow
   never records a human ruling, rewrites inputs, or updates acceptance pointers.

## Observations and status

Allowed `Verdict` values are shared with the contract:
- `CONFIRMED` — the compared authored statements agree in their stated context.
- `NORMALIZATION_ARTIFACT` — an apparent mismatch has a justified equivalent meaning.
- `SEMANTIC_MISMATCH` — explicit statements disagree about the same engineering fact.
- `IMPLICIT_CONFLICT` — prose or configuration implies a contradictory state.
- `COVERAGE_GAP` — an established cross-section relationship is unrepresented.
- `NEEDS_HUMAN_RULING` — supplied evidence cannot resolve a material ambiguity.

All non-`CONFIRMED` observations appear in the findings CSV with an observation
ID, severity, locations, evidence, explanation, and recommended action. Observations
are candidates for disposition; they do not automatically block readiness.

`ReviewStatus` is `COMPLETE` when the full authored document and requested
comparisons were reviewed, or `PARTIAL` when some remain unassessed. Neither
status is a quality verdict. A complete review may contain serious findings;
zero findings in a partial review must not be represented as verified agreement.

## Boundaries

Write only the two named outputs. Do not modify the draft, section QA, planning
artifacts, knowledge base, optional registers, or governed pointers. Do not
invoke publication tools, dispatch agents, or read raw KA/KTY or reference source
files. Source-grounded accuracy review remains a separate assignment.
