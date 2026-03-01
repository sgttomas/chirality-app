# Decision Log

- Used `EXECUTION_ROOT=/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude` (from INIT.md execution root; script arg default is `.`).
- Used default edge filter: `DependencyClass=EXECUTION` and `TargetType=DELIVERABLE`.
- Orphan detection is based on `TargetDeliverableID` after normalization (analysis-only).
- Graph metrics (isolates/hubs/SCCs) are computed on in-scope deliverables only; edges to orphans are excluded from SCC/degree calculations but recorded in `Evidence/orphans.csv`.
- SCC detection treats rows with unknown/missing `Direction` as undirected for SCC membership only (adds A↔B in SCC graph) and records the ambiguity via metrics.
