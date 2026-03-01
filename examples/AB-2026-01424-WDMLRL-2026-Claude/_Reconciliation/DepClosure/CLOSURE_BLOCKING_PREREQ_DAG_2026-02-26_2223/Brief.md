# Brief — BLOCKING_PREREQ_DAG

## Verbatim

Define deliverable DAG for scheduling/blocked-state using only EXECUTION+DELIVERABLE+PREREQUISITE+BLOCKING rows.

## DAG Definition (hard-coded for this run)

- Status = ACTIVE
- DependencyClass = EXECUTION
- TargetType = DELIVERABLE
- DependencyType = PREREQUISITE
- EstimateImpactClass = BLOCKING
- Direction in {UPSTREAM, DOWNSTREAM}

Direction interpretation:
- UPSTREAM rows are treated as `TargetDeliverableID → FromDeliverableID`
- DOWNSTREAM rows are treated as `FromDeliverableID → TargetDeliverableID`
