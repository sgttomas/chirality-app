# C3-S3 exact Git observation proposal

Candidate CGP-v0.1 / C3-S3-GIT-01 supplies one exact selected-path blob at a
full commit ID, optionally the same path at since/at commits. Only transient
observations/excerpts are produced. Local snapshot, caller assertion and Git
object evidence stay separate; no source/account materialization is selected.

Concrete scope: repository-root projects, ordinary or backlink-validated linked
worktrees; full object IDs only; raw bounded commit/tree/blob traversal and
regular modes; explicit linked metadata outside project rather than false
containment; alternates/separate layouts outside initial support. Existing
CSP private selection must retain path identity for this host-only join.
Preferred mechanism is restricted raw Git subprocess against sanitized helper
metadata and validated object-store association, with actual no-helper/no-fetch
qualification before release. No Git dependency download or claimed sandbox.

Available machinery: CSP host-private sessions, native callback pattern,
project Root verification, byte snapshot and excerpt implementation; SHA-256
and subprocess standard library. Git 2.54.0 (Apple Git-157) observed on the
development host only; Cargo.toml has no object library. Missing: reviewed
adapter, supported invocation/config isolation proof, object-integrity and
association parsing, offline hostile-configuration tests and actual native
witness. No implementation or probe qualification is claimed here.

Consumers: new transient preview only; no changes to saved-account reader,
CFB-v0.3/CRP-v0.3 schemas or PEC/Domains/fleet receiving. External metadata read
is specifically derived from selected worktree; broader path permissions are
not inferred. No D prerequisite or person/manager/agent act is supplied.
Review must assess whether the restricted helper mechanism meets the bounded
no-network/no-helper contract before code release; unsupported hosts refuse.

Technical choices are proposed for manager selection, not a new owner gate.
Broader authority, policy, network/dependency or persisted-meaning changes would
return through HELP_HUMAN. Source origins and exact repository hashes are in
C3_S3_SOURCE_BASIS.json. No MEMORY/native/download/credential work occurred.
