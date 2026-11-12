---
name: domain-knowledge-intake
description: Turn domain sources and expert input into an identified, warranted domain knowledge pack (criteria, methods and their applicability, parameter tables, assumptions, definitions and caveats), reconciled, examined by a competent domain reviewer and accepted for a stated scope of use by data-application specifications.
metadata:
  kind: instruction
  surface: workflow
---
# Take in domain knowledge for data applications

Use this method when an application specification, or several, needs domain knowledge
that must be right for its intended use. Examples:
- an ambient air-quality objective and its averaging period;
- a remediation guideline table keyed by land use, soil texture and depth;
- the assumptions under which a statistical or physical method applies;
- demographic rates for a population model, each with its source;
- definitions and caveats the application must show.

The normal result is a **domain knowledge pack**: a versioned, content-identified
set of typed items in the application-family ontology's domain classes. Each item
has its grounds and any conflicts. A competent domain reviewer accepts the pack
for a stated scope and use, and specifications reference it by identity.

A pack is reusable. One Alberta ambient-objective pack can serve every air
application that cites it; one remediation-guideline pack can serve every
screening tool. When the issuing body publishes a new edition, a new pack version
is made and the consuming specifications are examined for its effect.

This method does not serve DOMAIN-project corpora or knowledge-type documents; the
`domain-*` workflows remain separate. It does not decide what an application should
do with the knowledge; `data-app-spec` and `analysis-binding` do.

## Why domain knowledge has its own method

Four reasons.

**Rules break silently.** A remediation app can compute depth-specific guidelines and
then apply the shallow value at all depths, or document colour breaks its code does not
use. Explicit rule tables with tests prevent this.

**Values drift between documents and code.** A model's paper, supplement and code can
disagree on parameters and formulas. A conflict must be visible and ruled, not settled by whichever text an agent read last.

**Expert judgment is attributable.** Experts' estimates enter parameter defaults.
The thesis allocates judgment to persons: an agent can record an expert's
judgment but cannot supply it (`docs/thesis/03_philosophical_framework.md` §3.6.4).

**Reliance needs its own subject.** Domain acceptance needs an identified subject
and a competent examiner, separately from acceptance of an application (thesis
Chapter 5 §5.5).

## Roles

- **Lead.** HELPS_HUMANS or WORKING_ITEMS leads, according to whether design or
  production dominates. The domain reviewer is a person, or a role the owner
  appoints, whose competence covers the pack. Where professional obligations apply,
  an accountable professional accepts reliance.
- **Bounded contributions.** TASK carries extraction from a source, verification of
  another TASK's extraction, and rule-table test construction. TASK does not
  delegate.
- **Independent verification.** Extracted numerical values used in computation are
  verified by a separate agent or person, not the extractor (AGENTS.md: numerical
  meaning warrants independent scrutiny).

## Sequence

```text
1. Frame the knowledge needs and their intended use.
2. Acquire and identify sources.
3. Extract typed items with exact locators.
4. Normalise units, keys and resolution rules.
5. Reconcile conflicts and editions.
6. Elicit expert judgment where sources are silent.
7. Verify extraction independently; test rule tables.
8. Freeze the pack; domain review and acceptance.
9. Hand off the pack identity; maintain editions.
```

Use [the contract](resources/contract.md) for the pack format and decision record,
[the method](resources/method.md) for each stage, [checks](resources/checks.md) before
acceptance, and [the brief guide](resources/brief.md) for extraction and
verification assignments.
