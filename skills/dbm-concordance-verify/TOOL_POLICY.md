# TOOL POLICY - dbm-concordance-verify

## Preferred tool order

No deterministic tools are required. The verifier reads already-produced package and section artifacts and performs semantic reasoning.

## Allowed deterministic tools

### TASK-enforced

None. The skill omits `allowed-tools`.

### Operationally invoked

None.

## Expected use of reasoning

Use strong-model semantic reasoning to compare section prose, assertion rows, deterministic findings, and source-supersession findings across the full package context.

## Disallowed use

- Do not invoke publication tools.
- Do not dispatch other agents or skills.
- Do not read raw KTY-local source files.
- Do not rewrite section bodies, section QA, planning artifacts, or the concordance register.

## Write boundary

Writes are limited to:
- `Publication_Concordance_Verification.md`
- `Publication_Concordance_Verification_Findings.csv`

Both outputs must resolve under the current immutable package snapshot directory named in the brief.
