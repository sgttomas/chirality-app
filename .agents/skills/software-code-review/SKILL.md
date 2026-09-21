---
name: software-code-review
description: Review a bounded software diff for correctness, regressions, scope compliance, contracts, security, maintainability, and verification evidence before implementation fan-in.
---

# Software Code Review

Review the sealed brief, accepted basis, diff, and verification evidence. Validate changed paths before judging implementation details, using `tools/software_workflow/validate_change_scope.py` when the repository profile supports it.

Trace changed behavior through relevant callers, interfaces, persistence, error paths, concurrency, and tests. Check public contracts, structured data, migrations, and generated artifacts when touched. The helpers in `tools/software_workflow/` can select affected checks, compare structured outputs, and detect generated-file drift.

Report only actionable findings. Each finding should identify a precise location, the triggering condition, concrete impact, supporting evidence, and remediation direction. Order findings by severity. Separate confirmed defects from residual risk and missing verification.

Conclude whether the implementation return is suitable for manager fan-in and state the remaining risk. Review is read-only unless the request separately authorizes edits; it does not perform lifecycle acceptance.
