---
name: software-code-review
description: Review a bounded software diff for correctness, regressions, scope compliance, contracts, security, maintainability, and verification
  evidence. Use at staged or terminal fan-in before a manager accepts an implementation return.
---

# Software code review

## Method

1. Read the sealed brief, accepted basis, diff, and verification evidence.
2. Validate changed paths before judging implementation details.
3. Trace changed behavior through callers, interfaces, persistence, errors, concurrency, and tests as applicable.
4. Check public contracts, generated artifacts, schemas, and migrations when touched.
5. Report only actionable findings with location, impact, evidence, and remediation direction.
6. State residual risk and whether the return is valid for manager fan-in; do not perform lifecycle acceptance.

Read-only and safe for generic TASK. Review independence does not grant authority to rewrite the implementation.
