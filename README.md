# Chirality

Chirality is a governed application environment for agent-assisted, deliverable-heavy professional work. It contains a filesystem-native agent operating system together with the governance layer, deterministic tool layer, domain applications under declared domain-engine profiles, governed project records, and human gates that let AI agents act on real work without machine output being confused with professional authority.

This repository is the private canonical source tree for Chirality. It holds the shared instruction architecture, governance documents, deterministic tool layer, public-export source surface, private project workspaces, domain workspaces, and export tooling used to produce the sanitized public `chirality-app` package.

The core insight:

> If the filesystem is the database, architecture is a state-and-authority specification, not a service mesh.

Chirality is not an autonomous swarm. Within the environment sit an instruction architecture, a tool layer, and a desktop harness for directing AI agents under explicit scope, evidence, write-boundary, snapshot, and human-gate rules.

AI can accelerate professional work. It cannot inherit professional responsibility. AI may extend reckoning; it must not inherit judgment.

---

## Private Canonical Repository

This repo is upstream of the public `chirality-app` export. It is maintained as a canonical source tree for several related but distinct surfaces:

| Maintainer surface | Primary roots | Rule of thumb |
| --- | --- | --- |
| Instruction and governance | `AGENTS.md`, `agents/`, `docs/`, root framework docs | Change through live registries and governance docs, not historical inventories |
| Skills and tools | `skills/`, `tools/` | Keep method logic in skills and deterministic operations in tools |
| Public export | `exports/chirality-app/`, export-allowed root files/directories | Treat the export profile as the public boundary contract |
| App development | `projects/chirality-app-dev/` | Develop app/frontend work in the private project workspace; the former root `frontend/` harness snapshot is archived under `.archive/frontend/` |
| Domain/project workspaces | `projects/`, `domains/` | Treat as private applied/development workspaces unless a separate export path is created |
| Archives and planning workspace | `.archive/`, `plans/` | Treat `.archive/` as historical context; treat `plans/` as non-governing planning material unless a file explicitly declares active draft status |

---

## Maintainer Orientation Path

For the shared operating-system surface, start here:

1. `AGENTS.md`
2. `docs/DIRECTIVE.md`
3. `docs/SPEC.md`
4. `docs/TYPES.md`
5. `docs/CONTRACT.md`
6. `docs/PLAN.md`
7. `skills/README.md`
8. `tools/REGISTRY.md`

For the deeper rationale, read `CHIRALITY_FRAMEWORK.md`, `PROFESSIONAL_ENGINEERING.md`, and `docs/thesis/`.

For private project context, read the local README/docs inside the relevant workspace instead of promoting those documents into root docs.

---

## What This Repo Contains

The root operating-system surface is the canonical shared surface:

| Path | Role |
| --- | --- |
| `AGENTS.md` | Agent matrix, live agent index, governance integration rules, and canonical dispatch relationships |
| `agents/` | Individual agent instruction contracts |
| `skills/` | Repo-native method packs loaded by `TASK` |
| `tools/` | Deterministic helpers, validators, build/reporting utilities, and curated tool registry |
| `docs/` | Chirality-wide governance, specifications, roadmap, design basis, and thesis context |
| `init/` | Bootstrap and next-session notes |

Private maintainer and development roots are separate:

| Path | Role |
| --- | --- |
| `exports/` | Private export profiles, manifests, and reports |
| `projects/` | Private project-local development workspaces |
| `domains/` | Private/manual domain packs and local corpus shells |
| `plans/` | Planning workspace for archival imports and active draft plans that are not yet governed roadmap authority |
| `.archive/` | Local archived migration and historical material |

Root-level framing documents provide the theoretical and professional-practice basis for the system:

- `CHIRALITY_FRAMEWORK.md`
- `PROFESSIONAL_ENGINEERING.md`
- `LICENSE.md`

---

## Core Architecture

Chirality separates the **instruction root** from the **working root**.

The instruction root contains release-managed instructions, governance documents, skills, tools, and bootstrap files. The working root is the user-selected project filesystem where agents read and write governed state.

Authoritative project state is file-based. Packages, deliverables, references, dependency registers, review records, snapshots, and publication outputs are readable as plain files by humans, agents, and deterministic tools. Runtime convenience state may exist in the harness, but chat context, model memory, browser storage, local UI preferences, and application caches do not override governed project files.

If a decision is not in a versioned file, it does not exist for purposes of reliance.

---

## Governance And Authority

Chirality is designed around a professional-accountability problem: model output can sound plausible even when it is unsupported. The system response is to make warrant, authority, and uncertainty visible.

The main epistemic mechanisms are:

- mandatory provenance for governed claims
- explicit `TBD` markers for unknowns
- conflict surfacing instead of silent resolution
- epistemic labels such as `FACT`, `ASSUMPTION`, `PROPOSAL`, and `TBD`

Human authority remains non-transferable. Agents can propose, extract, draft, reconcile, validate, and report. Humans decide, approve, adjudicate conflicts, accept residual risk, and issue work for reliance. No agent may certify, approve, sign, seal, or issue professional work product.

The division of labor is constant across the environment: agents propose, deterministic tools and domain engines compute, humans rule, and the versioned record binds what was decided. Domain engines own authoritative domain truth; Chirality governs the work around them without becoming the solver (`docs/CONTRACT.md` K-DOMAIN-1..4).

The invariant system is defined in `docs/CONTRACT.md`. The design basis and professional grounding are developed in `docs/DBM_Agent_Instruction_Architecture.md`, `CHIRALITY_FRAMEWORK.md`, and `PROFESSIONAL_ENGINEERING.md`.

---

## Agents, Skills, Tools, And Tests

Use live registries and discovery tools rather than static counts.

| Surface | Source |
| --- | --- |
| Agents | `AGENTS.md` and `agents/AGENT_*.md` |
| Skills | `skills/README.md` plus immediate `skills/*/SKILL.md` folders |
| Tools | `tools/REGISTRY.md` as the curated contract/index surface |
| Tests | `tools/validation/discover_test_surfaces.py` for this private canonical repo |
| Roadmap | `docs/PLAN.md` |

An agent is an LLM plus instructions, declared files/context, tools, and permissions. Type 0 / Type 1 / Type 2 are runtime delegation positions: Supervising Architect, Manager, and Specialist. Standards constrain every layer but are not agents. `AGENTS.md` is the canonical runtime doctrine and live role index.

Multi-agent workflows may use terminal fan-out/fan-in, supervised
parent-mediated many-to-many coordination, or mixed dependency-valid work
graphs. HELP_HUMAN manages cross-package work; each WORKING_ITEMS instance
manages one activated package and its deliverable-scoped Agent 2 work.

`TASK` is the default recurring-method form of Agent 2. Ephemeral bounded generalists and human-approved dedicated specialists are also valid. Skills are method packs TASK can hydrate; tools are deterministic helpers for repeatable operations such as scaffolding, validation, PDF/drawing processing, dependency analysis, publication assembly, source cataloging, and test-surface discovery.

---

## Maintainer Change Workflow

Prefer changing the smallest authoritative surface that owns the behavior:

- Change agent role, authority, or routing through `AGENTS.md` and `agents/`.
- Change recurring bounded methods through `skills/` and validate skill metadata.
- Change deterministic behavior through `tools/` and update `tools/REGISTRY.md` when the tool contract is part of the curated index.
- Change Chirality-wide governance through root `docs/`, not project-local docs.
- Change app/product development in `projects/chirality-app-dev/`, then promote only reviewed public-export material into root/export surfaces.
- Change OpenPipeStress or domain-pack material in its project/domain workspace; do not backfill it into root docs by default.
- Regenerate the public export manifest after changing any public-exported file.

When live folders, indexes, and narrative documents disagree, treat the live registry/discovery surface as the starting point and surface the discrepancy in the change rather than silently preserving stale prose.

---

## Private Project And Domain Workspaces

`projects/` and `domains/` are private canonical-repo workspaces. They are not part of the public `chirality-app` export.

`projects/chirality-app-dev/` is the current private development pathway for the next version of the Chirality App. It contains project-local docs, execution material, examples, plans, provenance, and frontend source. Its current state should be treated as draft/pre-release development material.

`projects/chirality-piping/` is the OpenPipeStress project-local workspace. OpenPipeStress is a code-neutral piping flexibility and stress-analysis platform with project-local governance, docs, schemas, code, apps, tests, validation assets, execution material, plans, and provenance. Its project tree is private to this canonical repo and is not exported through `chirality-app`.

`domains/piping-design/` is a private/manual domain pack for piping-design knowledge, decomposition state, vocabulary roots, local source corpora, and local indexes. Large corpora and generated local indexes are intentionally excluded from git and from public export.

---

## Frontend Development Path

Chirality App product and frontend development is oriented around `projects/chirality-app-dev/`, the private development workspace for the app pathway. The earlier root `frontend/` runtime-harness snapshot has been archived under `.archive/frontend/` and is no longer an active root surface.

The durable source of truth is the instruction, governance, skill, tool, export, and project-development surface described here — not any single harness snapshot.

---

## Public Export Boundary

The public `chirality-app` export is controlled by `exports/chirality-app/`. The current public export profile includes the shared operating-system surface needed by the app package:

- root governance/bootstrap/framing files
- `.github/`
- `AGENTS.md`
- `agents/`
- `skills/`
- `tools/`
- `docs/`
- `init/`

The current public export profile excludes private or local-only workspace content:

- `.archive/`
- `projects/`
- `domains/`
- `plans/`
- `exports/`
- migration records
- source corpora and local indexes
- dependency/build/cache folders
- local runtime state
- environment files and secrets

Do not infer the public package contents from the root directory listing. The export profile is the boundary for copied content. Some exported tools and docs may still mention canonical private workspace paths because they are maintained from this source tree; those references do not mean the private workspace content is exported.

---

## Publishing Pipeline

Build the public staging package:

```sh
python3 exports/chirality-app/export_public.py
```

The export profile copies allowlisted files, sanitizes private absolute paths in text files, writes the export manifest/report, and fails if boundary checks find forbidden public paths or private absolute path leaks.

To replace a local public checkout after reviewing the staging report:

```sh
python3 exports/chirality-app/export_public.py --apply-target /path/to/chirality-app
```

---

## Historical And Archived Material

`.archive/` is local archived material. The moved migration records under `.archive/migration/` are useful for understanding how this canonical repo was assembled, but they are not live inventory, not current topology, and not part of the public export.

`plans/` is a planning workspace. Most material there is archival or draft context, but the directory may also hold active planning seeds before they are promoted into governed roadmap authority. The governed roadmap surface remains `docs/PLAN.md`.

---

## Validation

Use these checks based on the change:

```sh
python3 tools/validation/validate_skill_metadata.py skills
python3 tools/validation/discover_test_surfaces.py . --text
python3 exports/chirality-app/export_public.py
```

Run skill metadata validation after skill changes. Run test discovery when changing test surfaces or reporting available checks. Run the export tool before publishing or after changing any public-exported surface.

---

## Shared Agent Runtime

The root `runtime/` workspace is Chirality’s reusable execution substrate. A
single opt-in per-user daemon owns engines, credentials, sessions, delegation,
tools, interruption, and local-model residency. Desktop, the bundled
`chirality` CLI, and registered projects communicate with it over an
authenticated Unix-domain socket; there is no TCP control listener.

Tracked `chirality.project.json` files declare portable project identity and
relative authority references. Machine paths, client tokens, encrypted
credentials, central runtime sessions, logs, and residency state remain in
application user data and do not replace checkout-contained governance truth.

The initial local-agent pilot is deliberately narrow: one real Agent 1 may
delegate one governed read-only task to one Pi Agent 2 using an exact oMLX
model that the user explicitly made resident. Models are not permanently
assigned to Agent 0/1/2 roles.

---

## License

MIT License + Professional Engineering Clause. See `LICENSE.md`.

Copyright (c) 2026 Ryan Tufts
