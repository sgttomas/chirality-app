# deliverable-consistency — Tool Policy

## Preferred execution style

This skill is tool-first for the initial sweep, then reasoning-first for adjudication.

Preferred method order:
1. run `tools/validation/scan_deliverable_consistency.py` against the deliverable
2. read the flagged production docs and nearby context through `DELIVERABLE_TASK`
3. compare files directly where the scan surfaces a plausible inconsistency
4. emit evidence-backed proposals
5. apply minimal edits only if authorized

## Repo tool usage

Primary tool:
- `tools/validation/scan_deliverable_consistency.py`

Normal invocation shape:

```sh
python3 tools/validation/scan_deliverable_consistency.py "$DeliverablePath"
```

Use the optional flags only when the brief calls for them:
- `--focus-doc`
- `--strictness`
- `--max-findings`
- `--check-identity`
- `--check-unsourced-numerics`

The tool is a first-pass detector, not a final judge:
- unresolved markers are deterministic findings
- identity mismatches are candidate inconsistencies until checked in context
- unsourced numeric lines are review prompts, not automatic defects

## Disallowed behavior

- no project-wide scanning
- no writes outside the deliverable
- no dependency register edits unless separately authorized through the profile brief
