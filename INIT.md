# INIT — Next Session Orientation

This document is meant to get the following 4_DOCUMENTS agent off to the races without retracing earlier work. Treat the filesystem as authoritative; rely on the lifecycle entries in `test/execution/_Coordination/_COORDINATION.md`.

## Immediate tasks
1. **Confirm context:** Read `/Users/ryan/ai-env/projects/chirality-app/README.md` and `/Users/ryan/ai-env/projects/chirality-app/AGENTS.md` if you are unfamiliar with the framework. Then read `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Coordination/_COORDINATION.md` to see the most recent lifecycle entries and the 4_DOCUMENTS enrichment log. _Do not re-verify or re-open any deliverables completed before this session; the documentation in this package reflects current status._
2. **Focus scope:** Begin your work inside `test/execution/PKG-04_Pavement_and_Surfacing/1_Working/`. Each deliverable folder you touch should only have `_CONTEXT.md`, `_REFERENCES.md`, and the decomposition entry read to understand its scope. **Skip scanning deliverables outside PKG-04** unless explicitly directed.
3. **Produce documents:** Run the 4_DOCUMENTS enrichment cycle (three passes) for each PKG-04 deliverable in order (start with `DEL-04.01`). Overwrite the four documents, label assumptions/TBDs, cite the decomposition or Employer's Requirements PDFs, and keep cross-document consistency in mind.
4. **Don’t invent states:** `_STATUS.md` files already reflect the correct lifecycle state. Do not change them unless the deliverable is still `OPEN` and you’re generating the initial drafts for the first time.

## Orientation rules for the next agent
- **No re-reading past deliverables:** The status entries/traces you read in `_COORDINATION.md` are enough. Do not try to audit PKG-03 content again.
- **Keep relationships local:** You only need to think about how the PKG-04 deliverable ties to the decomposition’s scope, objectives, and referenced documents. Adjacent deliverables only matter where the current `_CONTEXT.md` explicitly references them.
- **Focus on design intent:** The decomposition and `_CONTEXT.md` provide the project context you need for this deliverable. Build your four documents from that info plus the Employer’s Requirements volumes (Paths: `test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf`).

## Lessons for the next iteration
- The cross-document alignment pass performed in PKG-03 (Datasheet ↔ Specification ↔ Guidance ↔ Procedure) is repeatable; keep capturing those explicit link points so future agents can trust the status and move forward without rechecking everything.
- Document references and verification points directly in each file so the next working batch can be confident the draft reflects what came before.
