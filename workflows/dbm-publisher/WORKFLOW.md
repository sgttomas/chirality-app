---
name: dbm-publisher
description: "Develop and publish one engineering Design Basis Memorandum from accepted domain state, with frozen planning, section production, post-authoring review, and human acceptance."
metadata:
  category: Documents and drawings
  applicability: Develop and publish one Design Basis Memorandum from accepted domain state.
---

# Publish a Design Basis Memorandum

WORKING_ITEMS coordinates this undertaking. Engage HELPS_HUMANS when the intended publication, section design, or rules need development. TASK carries bounded section synthesis, review, and package assembly assignments.

## Seven decisions

1. **Admit the basis.** Confirm the accepted DOMAIN root, publication intent, root closure and audit evidence. Freeze the exact inputs in `Publication_Input_Manifest.md`. Use `FULL_ENGINEERING_DBM` unless the human explicitly chooses `DBM_DIGEST` and records its narrower purpose.
2. **Understand the knowledge landscape.** Examine accepted categories, knowledge types, artifacts, objectives, and open matters. Show the human coverage, uncertainty, and the engineering story the publication must convey.
3. **Choose the publication schema and rules.** Develop the section structure and engineering conventions with the human. Keep design values, operating limits, equipment configurations, interfaces, constraints, and explicit uncertainty in the body; detailed traceability belongs in the appendix and QA records.
4. **Approve the section map.** Generate candidate mappings from machine-readable selectors. The human accepts the final `Section_Map.csv`; accepted mapping and rules determine section scope and authority.
5. **Authorize authoring.** Freeze planning artifacts and bounded section briefs. Dispatch TASK with `Workflow: dbm-section-publish` per section, including section-relevant open-item context. Refine oversized sections before dispatch.
6. **Assess the completed package.** Assemble the entire current section set with `dbm-publish`. Prepare structural and claim evidence; dispatch `dbm-postauthor-concordance` for candidate findings and optionally `dbm-concordance-verify` for semantic cross-section review. The human dispositions findings and directs necessary reruns. Reassemble and reassess the full package after section changes.
7. **Accept publication.** Present body adequacy, evidence, unresolved matters, provenance, and actual readiness. Human acceptance authorizes the accepted pointer and subsequent change-workflow handoff.

## Authority and judgment

Publication is derived from the admitted current state. It does not amend decomposition or accepted scope-change truth. The approved schema, rules, and section map govern synthesis from accepted mapped content. Retired or no-factual-use content cannot seed active body prose. Hypergraph evidence is auxiliary structure; blocked graph QA cannot support package QA.

Maintain the distinction between tool-produced evidence, agent-prepared findings, and human dispositions. Schema validity alone does not establish engineering adequacy. Surface human rulings, engineering TBDs, and decomposition gaps throughout planning, authoring, and review. Preserve their identities and owners in `Publication_Open_Items.md`; body prose expresses the corresponding limits honestly.

## Selected resources

- Load [CONTRACT.md](CONTRACT.md) for runtime paths, input classes, manifests, schema/map/rules fields, section artifacts, and package records.
- Load [PROCEDURE.md](PROCEDURE.md) for the current gate's tool recipes, dispatch steps, and rerun handling.
- Load [ACCEPTANCE.md](ACCEPTANCE.md) when validating planning, reviewing outputs, or closing the run.

All commands resolve against the declared tool root. Freeze the selected workflow and resources with the run brief. A rejected or abandoned publication run is recorded as such; a new run regenerates its working planning, dispatch, section, and package artifacts from admitted inputs.
