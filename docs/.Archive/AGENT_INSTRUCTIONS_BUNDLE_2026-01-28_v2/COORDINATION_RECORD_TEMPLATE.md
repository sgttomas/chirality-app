# Coordination Record Template

Use this as a durable, human-owned record of how the project is being coordinated.

> Note: This is *not* a deliverable lifecycle state machine. Deliverables still progress locally through:
> `OPEN → INITIALIZED → IN_PROGRESS → CHECKING → ISSUED`.

---

## Coordination Representation

- **Representation:** [Schedule-first (Gantt) | Declared deps | Full graph]
- **Dependency tracking mode:** [NOT_TRACKED | DECLARED | FULL_GRAPH]
- **External schedule / coordination artifact:** [path/link or N/A]
- **Last updated:** [YYYY-MM-DD]
- **Maintained by:** [name/role]

---

## Coordination Notes (human-owned)

- [Stage gates definitions, if you want them written down]
- [Freeze points and what “done enough” means at each freeze]
- [What dependency data is tracked vs left to human judgment]
- [Any conventions for IDs, tags, naming, interface documents]

---

## Optional: Critical Interface Dependencies (if using DECLARED)

Record only the dependencies that represent real cross-discipline interface commitments.

| Upstream (DEL-ID) | Downstream (DEL-ID) | Reason | Minimum maturity |
|---|---|---|---|
| | | | INITIALIZED |

