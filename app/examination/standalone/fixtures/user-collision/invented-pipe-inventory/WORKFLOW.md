---
name: invented-pipe-inventory
description: Count an invented pipe inventory for a standalone App test; never use for engineering reliance.
---
# Invented pipe inventory

Fixture variant: user-collision. This package is unregistered test material.

## Count

Read the input CSV supplied by the person in a scratch project. Validate the
header and nonnegative integer quantities. Report only the number of inventory rows; do not report piece totals.
Use the included [tally.py](tally.py) with an available Python 3: `python3 <package>/tally.py <input.csv>`. Redirect successful JSON output to inventory-summary.json. Read and report failure before writing any result. Use an available local tool to compute the result and retain the input digest,
command and observed result. Do not download a tool; missing tools or unreadable
inputs stop this attempt with the cause. Never guess omitted quantities.

## Return

Write inventory-summary.json in the scratch project and return its path plus
the retained basis. Re-read the input before resuming interrupted work; if it
changed, recompute and identify the new basis. Report tool failure without
claiming a completed count. The agent performs counting; the person alone
reviews or registers a workflow outside this counting method. No human-act
checkpoint is declared here; routine tool permissions are not registration.

```workflow-declaration
{
  "declaration_contract_version": "WD-v0.8",
  "expected_inputs": [
    {
      "name": "inventory",
      "meaning": "Invented inventory CSV with item, material and nonnegative integer pieces. No real project data.",
      "kind": "file_supplied",
      "necessity": "required",
      "stages": [
        "Count"
      ]
    }
  ],
  "required_tools": [
    {
      "name": "count-tool",
      "class": "harness_capability",
      "capability": "shell-command",
      "purpose": "Read the supplied CSV and compute the declared count with an available local tool.",
      "necessity": "required",
      "stages": [
        "Count"
      ]
    }
  ],
  "checkpoints": [],
  "returned_outputs": [
    {
      "name": "summary",
      "meaning": "Report only the number of inventory rows; do not report piece totals.",
      "form": "file",
      "destination": "scratch project",
      "path": "inventory-summary.json",
      "promised_standing": [
        "computed invented-material count"
      ]
    }
  ],
  "returned_evidence": [
    {
      "name": "basis",
      "meaning": "Input identity, command used and observed tool result; missing observations stay explicit.",
      "kind": "evaluated_basis",
      "supports": [
        "summary"
      ]
    }
  ],
  "compatible_roles": [
    "TASK",
    "WORKING_ITEMS",
    "HELP_HUMAN",
    "HELPS_HUMANS"
  ]
}
```
