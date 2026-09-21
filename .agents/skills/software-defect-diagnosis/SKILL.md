---
name: software-defect-diagnosis
description: Reproduce, isolate, and explain a bounded software defect before repair. Use for failing tests, regressions, runtime errors, performance anomalies, or conflicting symptom reports.
---

# Software Defect Diagnosis

Freeze the observed symptom, environment, expected behavior, and reproduction boundary. Reproduce it with the narrowest registered check or deterministic probe available; use the repository discovery and registered-check helpers under `tools/software_workflow/` when applicable.

Reduce competing hypotheses with evidence. Trace inputs and state transitions to the earliest divergence, and distinguish the root cause from contributing conditions and downstream consequences. Record failed reproduction attempts when they materially narrow the diagnosis.

Return:

- the reproduction result and exact evidence;
- a causal chain with confidence and viable alternatives;
- affected surfaces and likely dependants;
- bounded repair options and the regression check needed to prove the fix;
- remaining unknowns or environmental limits.

Diagnosis does not imply repair authority. Do not edit code unless the request separately authorizes implementation.
