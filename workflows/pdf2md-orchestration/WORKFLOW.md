---
name: pdf2md-orchestration
description: "Coordinate recoverable PDF conversion through page-bounded vision, deterministic cleanup and asset materialization, assembly, and explicit degraded-output review."
metadata:
  category: Documents and drawings
  applicability: Convert a PDF into recoverable Markdown and referenced assets through page-bounded work.
---

# Convert a PDF through bounded page work

WORKING_ITEMS coordinates conversion. TASK performs visual interpretation on bounded pages. Tools handle rasterization, cleanup, materialization, linking, and assembly. For a small single-run assignment, select the separate `pdf2md` workflow.

## Method

1. **Freeze source and output expectations.** Identify PDF bytes by SHA256, selected pages, DPI, output target, transcription and asset schema, review depth, degraded-output policy, and recovery posture. Reuse work only when source identity and relevant parameters match the producing manifest.
2. **Rasterize and optionally read folios.** Rasterize the selected pages and read the canonical page map. When printed page labels are needed, dispatch `pdf2md-folio-extract` per page and aggregate its results. Physical page indices remain identity; uncertain or absent folios remain null and receive the downstream review required by the domain-decomposition workflow.
3. **Convert pages in batches.** Dispatch TASK with `Workflow: pdf2md-page-full`. Each worker reads the page image once and returns both raw Markdown and `pdf2md-page-assets/v1` JSON. Resume only complete, valid output pairs tied to the current source; incomplete pairs are requeued together.
4. **Clean and materialize.** Run page cleanup and header/footer removal. With `ASSET_MODE=prose`, validate materialization resume state, crop or render assets, rewrite inline placeholders into working links, aggregate the asset manifest, and preserve unmatched assets explicitly. The canonical `page_NNNN.anchored.md` is regenerated from page Markdown and its materialization manifest; it is a mutable working product.
5. **Assemble and assess.** Assemble the scoped page set, run final cleanup, and validate asset references when enabled. Report failed or empty pages, placeholder coverage, missing assets, orphan links, and manifest discrepancies. A degraded assembly requires explicit human acknowledgment before downstream use.
6. **Hand off.** Record source identity, page coverage, output paths, degradation, and recovery requirements. For substantive mathematical content, continue with WORKING_ITEMS using `equation-audit`. Accepted source Markdown can then enter `domain-decomp`.

## Worker compatibility

New page-conversion runs use `pdf2md-page-full`. `pdf2md-page` and `pdf2md-page-assets` remain LEGACY for explicitly selected historical resume contracts; their asset schema remains compatible with materialization. `pdf2md-folio-extract` is a separate, optional active workflow because printed folio metadata has its own acceptance and null-result semantics.

## Selected resources

Load [CONTRACT.md](CONTRACT.md) for runtime parameters, output layouts, and tool interfaces. Load [PROCEDURE.md](PROCEDURE.md) for the current phase's commands, briefs, and resume handling. Check [ACCEPTANCE.md](ACCEPTANCE.md) before assembly handoff. Tool paths resolve against the declared tool root, independently of the working directory.
