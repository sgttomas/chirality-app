# D-GOV-16 Ruled Exact-Bytes Package

Status: `RULED — EXACT BYTES APPROVED; STAGE-2 IMPLEMENTATION PENDING`

The owner approved D-GOV-16 items 1–10 exactly as proposed on 2026-07-12. The
exact successor-standard bytes are therefore ratified under their conditional
status line. The TYPES and SPEC patch bytes are approved but remain unapplied;
they are queued for a later governed implementation tranche. The evidence
index remains derivative evidence rather than authority.

| File | Role | SHA-256 |
|---|---|---|
| `DELIVERABLE_SCOPE_OF_WORK_STANDARD.proposed.md` | Exact proposed successor standard | `7f74290167e3f410242bafe8bca153828a2a93e82099b8498ea6fd90eec85a6f` |
| `TYPES.proposed.patch` | Exact inactive zero-context patch to current `docs/TYPES.md` | `9614166c7db8340532d838768be2de52567862757fe0d5add3d3a90edea9d4b4` |
| `SPEC.proposed.patch` | Exact inactive zero-context patch to current `docs/SPEC.md` | `543200af8a617e2f5673db110eef2b0a5cf742c54e70ccda8bce0cad870d4b2e` |
| `STAGE2_EVIDENCE_PACKAGE_INDEX.md` | Commit/hash-bound Stage-1 evidence and reservation coverage | `8a6e48ac8247fe5147afb4208d3e7c0b4f48cb1071b1e086b4f24a2ceeded806` |

The ruled decision is
`docs/governance_harness/_DECISIONS/D-GOV-16_deliverable_scope_of_work_stage2.md`.
A later controlled implementation may apply only the ruled patch bytes and
must regenerate applicable derivatives. The historical `.proposed` filenames
preserve the exact ruled package identity; they do not mean that the owner's
ruling is provisional.

No Stage-2 implementation is performed by ruling publication. A fresh
governed orchestration plan must be presented from synchronized `main`
containing the published ruling before conversion, consumer migration, pilot
replacement, lifecycle handling, or patch application begins.

The two patch files intentionally use zero context so their artifact bytes do
not contain whitespace-only unified-diff context markers. Validate or apply
them with `git apply --unidiff-zero --check` (or the equivalent controlled
application command).
