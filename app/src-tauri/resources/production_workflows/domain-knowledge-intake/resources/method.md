# domain-knowledge-intake: method

## 1. Frame the needs

Start from the application's questions. List the knowledge items needed and the use of
each:
- a label;
- an input to a computation;
- a classification boundary;
- a value a person relies on for a determination.

Higher-consequence uses need primary sources, exact editions and independent
verification. Display-only items may rest on a documented secondary source if it is
marked as such.

Identify who can accept the pack. If no competent reviewer is available, the pack can
still be prepared, but it remains review-pending.

## 2. Acquire and identify sources

For each item family, prefer the issuing authority's current document. Record for
each source:
- issuer, title and edition;
- effective date and URL or location;
- page, table or section locators;
- retrieval date;
- access terms and licence;
- a content hash where a copy may be kept.

Note superseded editions rather than discarding them. An application may need the
edition in force at a past date. Record what could not be obtained, such as a
paywalled standard or a dead link, and what that limits.

## 3. Extract

Assign extraction per source or per item family to TASK with a bounded brief. Each
item is written in ontology form with:
- its locator;
- the source's own units and wording;
- the normalised form.

**Tables.** Extract tables completely and keep key columns explicit (land use,
depth interval, analyte). **Methods.** Record assumptions, applicability conditions
and known limitations, as well as the formula. **Parameter tables.** Keep row-level
grounds, because different rows often come from different studies.

## 4. Normalise

**Units.** Convert units to UCUM codes and keep the original unit. A conversion
between representations, such as ppb and µg/m³, records its basis: temperature,
pressure and molar mass.

**Keys.** Make applicability keys explicit and enumerate their values.

**Resolution rules.** Express them as explicit rules with cases. Examples:
- "undefined means most conservative";
- "match depth interval by sample midpoint";
- "pH is a range criterion".

**Rule tests.** Write the cases into `tests/` so the rule can be checked mechanically.

## 5. Reconcile

Compare items across sources and against any implementation that claims to use them.
Record each disagreement as a `Conflict` with both claims and their sources. Examples:
- paper versus supplement versus code;
- two editions;
- a value versus its documented derivation.

For each conflict:
- state what changes in an application if one claim or the other is used;
- prepare a proposed ruling;
- name the authority that must make it (owner, domain expert or accountable
  professional).

Do not reconcile by majority, recency or convenience.

## 6. Elicit expert judgment

Where sources are silent or inapplicable, ask the domain expert a structured question:
- the quantity;
- its context;
- the needed precision;
- the reason it matters.

Record the answer as an `expert_judgment` warrant with the expert's identity, date,
scope and stated rationale or range. Keep disagreement between experts visible. Do not
present an elicited value as a published one.

## 7. Verify

A separate agent or person, not the extractor, checks each extracted numerical value
used in computation against its locator. Values used only for display are checked by
sample, with the sample stated. Run the rule-table tests.

Record mismatches and repair them, then backcheck. The check establishes fidelity to
the source. It does not establish that the source is applicable to the application:
the domain review judges that.

## 8. Freeze, review and accept

1. Freeze the pack with its manifest.
2. Present it to the domain reviewer with:
   - the needs and intended uses;
   - the sources and their limits;
   - verification results;
   - open conflicts and proposed rulings;
   - TBD items and their consequence.
3. Record the reviewer's actual response in the decision record.

The reviewer can accept the pack, accept it for a limited scope, exclude items, rule
conflicts, or return it.

## 9. Hand off and maintain

Return:
- the pack identity and the decision record location;
- the scope of use;
- open items.

When an issuer publishes a new edition:
1. Make a new pack version.
2. List the changed items, with old and new values and sources.
3. Identify the consuming specifications, via their `knowledge_packs` references.
4. Hand each owner the effect on that specification.

Do not update a specification's knowledge silently.

## Interruption and recovery

Keep extraction evidence as it is produced. On resumption, compare saved items with
their evidence and current sources. Re-verify only items whose source changed.
