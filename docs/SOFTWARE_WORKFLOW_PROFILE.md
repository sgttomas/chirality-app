# Software Workflow Activation Profile

> **Status: RATIFIED — D-GOV-14 item 3, owner ruling 2026-07-12.** The exact
> text at commit `ee35409f5cf3a81ecb29a271527156b991df97b9` is the activation
> profile contract for WORKING_ITEMS software packages.
>
> **Backward-compatible extension, 2026-07-13:** owner-directed runtime
> hardening permits a registered check to declare one bounded managed service
> as specified below. Existing profiles and commands are unchanged.

## Purpose

Software development is a specialization of package work, not a separate
manager role in this tranche. Use:

```text
WORKING_ITEMS Agent 1
+ one project-local software-workflow.json
+ software-* TASK skills
+ deterministic tools/software_workflow helpers
```

The profile freezes project-specific check commands and path-to-check mappings.
It does not authorize work, expand a brief, or replace accepted project and
decomposition state.

## Activation

A WORKING_ITEMS package activation identifies:

- the package and selected deliverables;
- the accepted project/decomposition basis;
- the project-local `software-workflow.json`;
- changed or expected paths;
- applicable software TASK skills;
- write ownership and fan-in gates;
- human decision points.

Novel stacks may use a sealed ephemeral generalist Agent 2. Repeated methods
graduate into a skill. HELPS_HUMANS may propose a dedicated SOFTWARE_DEV Agent
1 only after project trials demonstrate stable manager semantics that
WORKING_ITEMS cannot safely carry.

## Profile schema

Profiles use `chirality-software-workflow/v1` JSON:

```json
{
  "schema": "chirality-software-workflow/v1",
  "project_root": ".",
  "workspace_root": ".",
  "checks": {
    "unit": {"cwd": ".", "command": ["python3", "-m", "pytest", "-q"]}
  },
  "always_checks": [],
  "path_rules": [
    {"paths": ["src/**"], "checks": ["unit"]}
  ]
}
```

`project_root` defines project-relative path rules. `workspace_root` is the
outer containment boundary for registered check working directories and may
include repository-level governance checks. Commands are argument arrays
executed without a shell. A profile is a
registered tool surface, not permission to run unlisted commands. Agent briefs
still declare the checks and write targets allowed for the run.

### Optional managed service

A check that requires a local execution substrate may declare one `service`
object. `run_registered_checks.py` allocates an isolated loopback port when
`port` is `auto`, starts the registered service without a shell, waits for the
registered readiness URL, injects only the declared `check_env`, executes the
check, and terminates the service in all outcomes. Service and check working
directories remain inside `workspace_root`.

```json
{
  "checks": {
    "premerge": {
      "cwd": "frontend",
      "command": ["npm", "run", "validate:premerge"],
      "service": {
        "cwd": "frontend",
        "command": ["node", "server.js", "--port", "{port}"],
        "port": "auto",
        "ready_url": "http://127.0.0.1:{port}",
        "env": {"PROVIDER": "stub"},
        "check_env": {"BASE_URL": "http://127.0.0.1:{port}"},
        "startup_timeout_seconds": 60,
        "shutdown_timeout_seconds": 10
      }
    }
  }
}
```

`{port}` substitution is supported only in registered service command values,
service environment values, check environment values, and `ready_url`.
Service setup failure is reported separately with exit code `125`; check
timeout remains exit code `124`. Normalized evidence records readiness,
startup duration, bounded log tails, exit state, and confirmed shutdown.

## Canonical tool responsibilities

- `discover_repository.py`: manifests and test surfaces.
- `select_affected_checks.py`: deterministic path-rule selection.
- `run_registered_checks.py`: registered checks and normalized JSON evidence.
- `validate_change_scope.py`: changed-path containment.
- `compare_structured.py`: JSON API/schema/migration comparison.
- `verify_generated_manifest.py`: generated-file digest drift.

Tool output is generated evidence. It becomes accepted workflow state only
through the owning manager's validation and applicable human gates.
