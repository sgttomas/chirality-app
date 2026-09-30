# Owner decisions — APP-V4-DESIGN-PASS-2-20260930

Exact owner text, as given in the chat session with HELP_HUMAN. Custody: the
session transcript; recorded here by HELP_HUMAN. A record here is not a claim
that the owner reviewed any file.

## Start direction (2026-09-30)

> Start the next first-increment design pass using DAG-003.

Context: HELP_HUMAN had offered four possible next undertakings after
`APP-V4-SCA002-20260929` closed, and recommended this one: "The next
first-increment design pass, using DAG-003 to plan it. It would also re-point
the 17 design files at the amended requirement texts, which closes one of the
two items you deferred."

**Reading (HELP_HUMAN's interpretation, not owner text):** a second design
pass on the 14 first-increment deliverables, planned through accepted
DAG-003, that (1) re-pins their Design files to the amended basis and the
revised ScopeOfWork contracts, and (2) develops the design toward the 60%
level described in `loop/LOOP_INIT.md`. The exact content of (2) is set by a
scoping survey (node S1) and recorded in the work graph. The coverage-telemetry
rebuild, the SWBPIPE relay and the audit-script fix were offered separately
and are not selected.

## Standing directions that apply

- Git: "You should have the ability to monitor PRs and merge once the CI goes
  green. I want you to do that. Tell me if something is blocking."
  (2026-09-28). Applied as before: auto-merge is enabled only after an
  independent review of the candidate finds nothing blocking.
- DECISION-3 (`APP-V4-SWBPIPE-INTAKE-20260928`): host joins deferred.
- DECISION-4 and DECISION-5 of that run: phased checkpoints; model access by
  OAuth or API key with no default; host-agent network destinations.
