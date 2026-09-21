#!/usr/bin/env python3
"""G4 — instruction-surface tranche manifest check (D-GOV-21 §5.3, M2/M6).

Deterministic guard shipped by the D-GOV-21 guard-capability tranche (packet
§6 step 6) and wired into governance-harness CI. Each accepted root tranche
that changes protected instruction-surface paths must carry a tranche manifest
declaring those changes; this guard verifies manifest presence, schema
validity, path coverage of an actual diff, and the recorded M2 gate and M6
notice disposition for the tranche.

**It checks recorded provenance; it never infers origin from a diff.** The
authorization, integration owner, merge gate, and notice disposition are read
as recorded fields. A diff is used only to ask whether the changed
instruction-surface paths are covered by a declared manifest — never to
attribute authorship, to infer that a change was authorized, or to synthesize
a manifest. A manifest records that a gate was taken; it grants nothing
(K-AUTH-1).

Design of record (manifest format and location)
-----------------------------------------------
Location: `docs/governance_harness/tranche_manifests/<TRANCHE_ID>.yaml`, one
file per tranche, filename stem equal to `tranche_id`. Schema id:
`instruction-tranche-manifest/v1`. All paths are repo-root-relative POSIX
paths or globs. Shape::

    schema: instruction-tranche-manifest/v1
    tranche_id: ROOT-LANE-B-20260725
    title: Guard capability G1-G4
    date: 2026-07-25
    basis: <commit sha>            # optional: the basis the tranche was cut from
    instruction_surface_paths:     # every protected path the tranche changes
      - tools/validation/validate_root_harness_adapter.py
      - .github/workflows/governance-harness.yml
    m2_gate:
      authorization: <verbatim or cited independent owner authorization>
      authorized_by: <human actor of record>
      authorization_date: 2026-07-25
      integration_owner: <the single serialized integration owner>
      merge_gate: owner-authorized-pr  # standing Git grant; human-gated-pr remains valid for historical/exact-action records
      self_merge: true             # permitted by owner-authorized-pr; legacy
                                   # human-gated-pr requires owner_direction
                                   # for self_merge true (PRD annex 5.3.1)
      owner_direction:             # optional owner direction of record
        directed_by: <owner of record>
        direction_date: 2026-07-29
        approved_source_sha: <full 40-hex pre-merge pin of the approved HEAD>
    m6_notice:
      disposition: pending         # pending | routed | none-required
      routed_to: []                # notice paths; required when routed
      rationale: <why this disposition>

Declared paths are NOT required to exist: a tranche may delete a path. Paths
that do not intersect the instruction surface are recorded as over-declaration
(INFO, non-blocking). `disposition: pending` is lawful and PASSes with an INFO
note — the M6 routing decision is completed by the accepting agent at fan-in,
and this guard records rather than pre-empts that act.

When a repository-separation tranche moves a routed notice to another
repository, it may record an `external_notice_routes` list. Each entry names
the former repo-relative `source`, the destination `repository` and
repo-relative `path`, and the immutable full `commit` that contains it. A
missing local routed notice PASSes only when an exact, well-formed relocation
record exists; the guard reports the external route as INFO. The guard checks
recorded provenance and syntax, not remote availability.

`merge_gate: owner-authorized-pr` records use of the standing Git grant in
PRD annex §5.3.1 (owner direction 2026-09-12). It permits `self_merge: true`
without a per-merge approval SHA. This guard checks declaration shape, not
whether the assignment is authorized or whether the actual PR has passed
required CI and independent review. Those conditions and owner holds must
still be checked before merging.

Historical `human-gated-pr` manifests remain supported. In that mode,
`self_merge: true` requires a complete `owner_direction` block naming the
owner, direction date, and full 40-hex `approved_source_sha`. A supplied
block must be well formed in either mode. Neither mode mechanically proves
human authority (K-AUTH-1).

The instruction surface is `docs/SPEC.md` §0.2.1's enumeration as amended by
D-GOV-26: `AGENTS.md`, `CLAUDE.md`, `agents/`, `.agents/skills/`, legacy
`skills/`, `tools/`, root
`docs/`, `init/`, `.github/workflows/`. `CLAUDE.md` is the session-init
instruction pointer importing `AGENTS.md`; `.github/workflows/` holds the CI
workflow definitions that gate merges, and had previously been guarded on the
Lane B characterization in
`execution/_Coordination/WORKPLAN_2026-07-25_root_product_development.md`.

Modes and behavior (severity semantics per D-GOV-02)
----------------------------------------------------
- *CI mode* (no arguments): the manifest directory must exist and hold at
  least one manifest, and every manifest in it must be schema-valid. An absent
  or empty directory is BLOCK — the discipline must not be silently emptied.
  (This is the G4 discipline applied to itself: this tranche's own manifest
  lives there and is checked by every CI run.)
- *Diff mode* (`--base REF --head REF [--tranche ID]`): computes
  `git diff --name-only <base>..<head>`, filters to instruction-surface paths,
  and BLOCKs on any changed instruction-surface path not covered by a declared
  manifest path (all manifests by default, or one named `--tranche`).
- *Candidate-range diff mode* adds `--added-manifests-only`: schema-validates
  the whole manifest corpus as usual, but accepts path coverage only from
  manifest files added in the named diff. This is the governed CI mode: an old
  manifest, whether unchanged or modified, cannot stand in for the candidate
  tranche's required new manifest.
- Exit 0 PASS, exit 1 BLOCK, exit 2 operational (PyYAML unimportable, git
  unavailable or refs unresolvable, unusable arguments).

Observation boundary
--------------------
Manifest files' recorded fields, the existence of notice paths a manifest
declares as routed, and — in diff mode only — the file-name list of a git
diff between two named refs. No commit content, no authorship, no other
working root.

Registration entry it will assert in `execution/_harness/root_guards.yaml`
(written by root Project Setup, never by this tranche)::

    guards:
      G4:
        registered: true
        status: passing
        validator: tools/validation/validate_instruction_tranche_manifest.py
        tests: tools/validation/test_validate_instruction_tranche_manifest.py
        state_surface: docs/governance_harness/tranche_manifests/
        schema: instruction-tranche-manifest/v1
        diff_mode: "--base REF --head REF [--tranche ID]"
"""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

MANIFEST_DIR_RELPATH = Path("docs/governance_harness/tranche_manifests")
MANIFEST_SCHEMA = "instruction-tranche-manifest/v1"

VALID_DISPOSITIONS = ("pending", "routed", "none-required")
REQUIRED_KEYS = (
    "schema",
    "tranche_id",
    "title",
    "date",
    "instruction_surface_paths",
    "m2_gate",
    "m6_notice",
)
REQUIRED_M2_KEYS = (
    "authorization",
    "authorized_by",
    "authorization_date",
    "integration_owner",
    "merge_gate",
    "self_merge",
)
REQUIRED_M6_KEYS = ("disposition", "routed_to", "rationale")
# Optional m2_gate.owner_direction block (PRD annex 5.3.1, D-GOV-31 as
# simplified by owner direction 2026-07-29): when present it must be
# complete. The legacy human-gated-pr mode requires this block for
# self_merge true; owner-authorized-pr does not.
REQUIRED_OWNER_DIRECTION_KEYS = (
    "directed_by",
    "direction_date",
    "approved_source_sha",
)

INSTRUCTION_SURFACE_FILES = ("AGENTS.md", "CLAUDE.md")
INSTRUCTION_SURFACE_DIRS = (
    "agents/",
    ".agents/skills/",  # Canonical portable skill packages.
    "skills/",  # Historical packages remain instruction surfaces.
    "workflows/",
    "tools/",
    "docs/",
    "init/",
    ".github/workflows/",
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TRANCHE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def is_repo_relative(value: str) -> bool:
    if not value or value.startswith("/") or value.startswith("~"):
        return False
    if re.match(r"^[A-Za-z]:[\\/]", value):
        return False
    return ".." not in PurePosixPath(value).parts


def normalize_target(target: str) -> str:
    """Strip leading `./` segments only — never a leading dot of `.github/`."""
    normalized = target.strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def intersects_instruction_surface(target: str) -> bool:
    normalized = normalize_target(target)
    if normalized in ("*", "**", "**/*"):
        return True
    if normalized in INSTRUCTION_SURFACE_FILES:
        return True
    return any(normalized.startswith(prefix) for prefix in INSTRUCTION_SURFACE_DIRS)


def literal_prefix(target: str) -> str:
    normalized = normalize_target(target)
    return normalized.split("*", 1)[0].rstrip("/")


def normalize_date(value: object) -> object:
    """YAML parses an unquoted `2026-07-25` into a `date`; accept either form."""
    if isinstance(value, datetime.datetime):
        return value.date().isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    return value


def covered_by(changed: str, declared: list[str]) -> bool:
    for candidate in declared:
        base = literal_prefix(candidate)
        if not base:
            return True
        if changed == base or changed.startswith(base + "/"):
            return True
    return False


def manifest_paths(root: Path) -> list[Path]:
    directory = root / MANIFEST_DIR_RELPATH
    if not directory.is_dir():
        return []
    return sorted(
        p for p in directory.iterdir() if p.is_file() and p.suffix in (".yaml", ".yml")
    )


def validate_manifest(
    root: Path,
    path: Path,
    external_notice_routes: dict[str, dict[str, str]] | None = None,
) -> tuple[list[str], list[str], dict | None]:
    """Returns (failures, notes, data). `data` is None when unreadable/unparseable."""
    failures: list[str] = []
    notes: list[str] = []
    rel = path.name

    import yaml  # type: ignore  # caller guarantees importability (see check()).

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - parse/read failure is a malformed surface.
        return [f"manifest {rel} is unparseable or unreadable: {exc}"], notes, None
    if not isinstance(data, dict):
        return [f"manifest {rel}: top level is not a mapping"], notes, None

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        failures.append(f"manifest {rel}: missing required keys: {sorted(missing)}")

    if data.get("schema") != MANIFEST_SCHEMA:
        failures.append(
            f"manifest {rel}: schema is {data.get('schema')!r}; this guard understands "
            f"{MANIFEST_SCHEMA!r}"
        )

    tranche_id = data.get("tranche_id")
    if not isinstance(tranche_id, str) or not TRANCHE_ID_RE.match(tranche_id or ""):
        failures.append(f"manifest {rel}: tranche_id {tranche_id!r} is not a plain identifier")
    elif tranche_id != path.stem:
        failures.append(
            f"manifest {rel}: tranche_id {tranche_id!r} does not match the filename "
            f"stem {path.stem!r}"
        )

    for key in ("title",):
        if key in data and (not isinstance(data.get(key), str) or not str(data[key]).strip()):
            failures.append(f"manifest {rel}: {key} must be a non-empty string")

    date = normalize_date(data.get("date"))
    if "date" in data and (not isinstance(date, str) or not DATE_RE.match(date)):
        failures.append(f"manifest {rel}: date {data.get('date')!r} is not YYYY-MM-DD")

    basis = data.get("basis")
    if basis is not None and (
        not isinstance(basis, str) or not re.match(r"^[0-9a-f]{7,40}$", basis)
    ):
        failures.append(f"manifest {rel}: basis {basis!r} is not a 7-40 character hex SHA")

    paths = data.get("instruction_surface_paths")
    if (
        not isinstance(paths, list)
        or not paths
        or not all(isinstance(p, str) and p for p in paths)
    ):
        failures.append(
            f"manifest {rel}: instruction_surface_paths must be a non-empty list of strings"
        )
        paths = []
    for declared in paths:
        if not is_repo_relative(declared):
            failures.append(
                f"manifest {rel}: declared path {declared!r} is not a repo-relative "
                "POSIX path"
            )
        elif not intersects_instruction_surface(declared):
            notes.append(
                f"manifest {rel}: declared path {declared!r} does not intersect the "
                "instruction surface (over-declaration; non-blocking)"
            )

    m2 = data.get("m2_gate")
    if not isinstance(m2, dict):
        if "m2_gate" in data:
            failures.append(f"manifest {rel}: m2_gate must be a mapping")
    else:
        missing_m2 = [k for k in REQUIRED_M2_KEYS if k not in m2]
        if missing_m2:
            failures.append(f"manifest {rel}: m2_gate missing keys: {sorted(missing_m2)}")
        for key in ("authorization", "authorized_by", "integration_owner"):
            value = m2.get(key)
            if key in m2 and (not isinstance(value, str) or not value.strip()):
                failures.append(f"manifest {rel}: m2_gate.{key} must be a non-empty string")
        auth_date = normalize_date(m2.get("authorization_date"))
        if "authorization_date" in m2 and (
            not isinstance(auth_date, str) or not DATE_RE.match(auth_date)
        ):
            failures.append(
                f"manifest {rel}: m2_gate.authorization_date "
                f"{m2.get('authorization_date')!r} is not YYYY-MM-DD"
            )
        if "merge_gate" in m2 and m2.get("merge_gate") not in ("human-gated-pr", "owner-authorized-pr"):
            failures.append(
                f"manifest {rel}: m2_gate.merge_gate is {m2.get('merge_gate')!r}; M2 "
                "requires 'human-gated-pr' or 'owner-authorized-pr'"
            )
        direction = m2.get("owner_direction")
        direction_complete = False
        if direction is not None:
            direction_failures, direction_complete = validate_owner_direction(
                rel, direction
            )
            failures.extend(direction_failures)
        if "self_merge" in m2 and m2.get("self_merge") is not False:
            if m2.get("self_merge") is True and m2.get("merge_gate") == "owner-authorized-pr":
                notes.append(
                    f"manifest {rel}: self-merge declared under the standing owner "
                    "Git grant (PRD annex 5.3.1); actual candidate review, required "
                    "CI and owner holds must still be checked at the PR"
                )
            elif m2.get("self_merge") is True and direction_complete:
                notes.append(
                    f"manifest {rel}: m2_gate.self_merge is true under recorded "
                    f"owner direction by {direction.get('directed_by')!r} on "
                    f"{normalize_date(direction.get('direction_date'))} "
                    "(PRD annex 5.3.1); the schema default remains self_merge false"
                )
            else:
                failures.append(
                    f"manifest {rel}: m2_gate.self_merge is {m2.get('self_merge')!r} "
                    "without a complete m2_gate.owner_direction block; M2 "
                    "forbids self-merge (must be false) absent a recorded owner "
                    "direction (PRD annex 5.3.1)"
                )

    m6 = data.get("m6_notice")
    if not isinstance(m6, dict):
        if "m6_notice" in data:
            failures.append(f"manifest {rel}: m6_notice must be a mapping")
    else:
        missing_m6 = [k for k in REQUIRED_M6_KEYS if k not in m6]
        if missing_m6:
            failures.append(f"manifest {rel}: m6_notice missing keys: {sorted(missing_m6)}")
        disposition = m6.get("disposition")
        if "disposition" in m6 and disposition not in VALID_DISPOSITIONS:
            failures.append(
                f"manifest {rel}: m6_notice.disposition {disposition!r} not in "
                f"{list(VALID_DISPOSITIONS)}"
            )
        rationale = m6.get("rationale")
        if "rationale" in m6 and (not isinstance(rationale, str) or not rationale.strip()):
            failures.append(f"manifest {rel}: m6_notice.rationale must be a non-empty string")
        routed_to = m6.get("routed_to")
        if routed_to is None:
            routed_to = []
        if not isinstance(routed_to, list) or not all(isinstance(p, str) for p in routed_to):
            failures.append(f"manifest {rel}: m6_notice.routed_to must be a list of paths")
            routed_to = []
        if disposition == "routed":
            if not routed_to:
                failures.append(
                    f"manifest {rel}: m6_notice.disposition is 'routed' but routed_to "
                    "names no notice"
                )
            for notice in routed_to:
                if not is_repo_relative(notice):
                    failures.append(
                        f"manifest {rel}: routed notice {notice!r} is not a "
                        "repo-relative POSIX path"
                    )
                elif not (root / notice).exists() and notice in (external_notice_routes or {}):
                    route = (external_notice_routes or {})[notice]
                    notes.append(
                        f"manifest {rel}: routed notice {notice!r} is externalized to "
                        f"{route['repository']}:{route['path']} at commit {route['commit']}"
                    )
                elif not (root / notice).exists():
                    failures.append(
                        f"manifest {rel}: routed notice {notice!r} does not exist"
                    )
        elif disposition == "pending":
            notes.append(
                f"manifest {rel}: m6_notice.disposition is 'pending' — routing is "
                "completed by the accepting agent at fan-in; recorded, not pre-empted"
            )

    return failures, notes, data


def collect_external_notice_routes(
    manifests: list[Path],
) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Collect exact, commit-pinned notice relocations from the manifest corpus."""
    import yaml  # type: ignore

    routes: dict[str, dict[str, str]] = {}
    failures: list[str] = []
    required = {"source", "repository", "path", "commit"}
    for manifest in manifests:
        try:
            data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        except Exception:  # validate_manifest reports the parse failure.
            continue
        if not isinstance(data, dict) or "external_notice_routes" not in data:
            continue
        entries = data.get("external_notice_routes")
        if not isinstance(entries, list):
            failures.append(
                f"manifest {manifest.name}: external_notice_routes must be a list"
            )
            continue
        for index, entry in enumerate(entries):
            prefix = f"manifest {manifest.name}: external_notice_routes[{index}]"
            if not isinstance(entry, dict):
                failures.append(f"{prefix} must be a mapping")
                continue
            missing = required - set(entry)
            if missing:
                failures.append(f"{prefix} missing keys: {sorted(missing)}")
                continue
            source = entry.get("source")
            repository = entry.get("repository")
            destination = entry.get("path")
            commit = entry.get("commit")
            valid = True
            if not isinstance(source, str) or not is_repo_relative(source):
                failures.append(f"{prefix}.source must be a repo-relative POSIX path")
                valid = False
            if (
                not isinstance(repository, str)
                or not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repository)
            ):
                failures.append(f"{prefix}.repository must be an owner/repository slug")
                valid = False
            if not isinstance(destination, str) or not is_repo_relative(destination):
                failures.append(f"{prefix}.path must be a repo-relative POSIX path")
                valid = False
            if not isinstance(commit, str) or not re.match(r"^[0-9a-f]{40}$", commit):
                failures.append(f"{prefix}.commit must be a full 40-hex SHA")
                valid = False
            if not valid:
                continue
            route = {
                "repository": repository,
                "path": destination,
                "commit": commit,
            }
            if source in routes and routes[source] != route:
                failures.append(f"{prefix}.source {source!r} has a conflicting route")
                continue
            routes[source] = route
    return routes, failures


def validate_owner_direction(rel: str, direction: object) -> tuple[list[str], bool]:
    """Validate an m2_gate.owner_direction block (PRD annex 5.3.1).

    Returns (failures, complete). `complete` is True only when every required
    key is present and well-formed — the only state in which
    `self_merge: true` is lawful for the legacy human-gated-pr mode.
    Standing owner-authorized-pr uses ordinary PR evidence instead of this pin.
    """
    failures: list[str] = []
    prefix = f"manifest {rel}: m2_gate.owner_direction"
    if not isinstance(direction, dict):
        return [f"{prefix} must be a mapping"], False

    complete = True
    missing = [k for k in REQUIRED_OWNER_DIRECTION_KEYS if k not in direction]
    if missing:
        failures.append(f"{prefix} missing keys: {sorted(missing)}")
        complete = False

    directed_by = direction.get("directed_by")
    if "directed_by" in direction and (
        not isinstance(directed_by, str) or not directed_by.strip()
    ):
        failures.append(f"{prefix}.directed_by must be a non-empty string")
        complete = False

    direction_date = normalize_date(direction.get("direction_date"))
    if "direction_date" in direction and (
        not isinstance(direction_date, str) or not DATE_RE.match(direction_date)
    ):
        failures.append(
            f"{prefix}.direction_date {direction.get('direction_date')!r} is not "
            "YYYY-MM-DD"
        )
        complete = False

    sha = direction.get("approved_source_sha")
    if "approved_source_sha" in direction and (
        not isinstance(sha, str) or not re.match(r"^[0-9a-f]{40}$", sha)
    ):
        failures.append(
            f"{prefix}.approved_source_sha {sha!r} is not a full 40-hex SHA "
            "(the mandatory pre-merge pin)"
        )
        complete = False

    return failures, complete


def changed_paths(root: Path, base: str, head: str) -> tuple[list[str] | None, str | None]:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "diff", "--name-only", f"{base}..{head}"],
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return None, f"git is unavailable: {exc}"
    if out.returncode != 0:
        return None, f"git diff {base}..{head} failed: {out.stderr.strip()}"
    return [line.strip() for line in out.stdout.splitlines() if line.strip()], None


def added_paths(root: Path, base: str, head: str) -> tuple[list[str] | None, str | None]:
    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "diff",
                "--name-only",
                "--diff-filter=A",
                f"{base}..{head}",
            ],
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return None, f"git is unavailable: {exc}"
    if out.returncode != 0:
        return None, f"git diff {base}..{head} failed: {out.stderr.strip()}"
    return [line.strip() for line in out.stdout.splitlines() if line.strip()], None


def check(
    root: Path,
    base: str | None = None,
    head: str | None = None,
    tranche: str | None = None,
    added_manifests_only: bool = False,
) -> tuple[int, list[str]]:
    """Returns (exit_code, report_lines). 0 PASS, 1 BLOCK, 2 operational."""
    lines: list[str] = []
    diff_mode = base is not None and head is not None

    try:
        import yaml  # type: ignore  # noqa: F401
    except ImportError:
        lines.append(
            "G4 OPERATIONAL (exit 2): PyYAML is not importable, so tranche manifests "
            "cannot be observed; this guard asserts nothing."
        )
        return 2, lines

    directory = root / MANIFEST_DIR_RELPATH
    manifests = manifest_paths(root)
    if not directory.is_dir():
        lines.append(
            f"G4 BLOCK: tranche manifest directory {MANIFEST_DIR_RELPATH.as_posix()} "
            "does not exist; every instruction-surface tranche must carry a manifest "
            "(D-GOV-21 M2/G4)."
        )
        return 1, lines
    if not manifests:
        lines.append(
            f"G4 BLOCK: tranche manifest directory {MANIFEST_DIR_RELPATH.as_posix()} "
            "holds no manifest; the G4 discipline must not be silently emptied."
        )
        return 1, lines

    failures: list[str] = []
    notes: list[str] = []
    by_id: dict[str, dict] = {}
    by_path: dict[str, dict] = {}
    external_notice_routes, route_failures = collect_external_notice_routes(manifests)
    failures.extend(route_failures)
    for path in manifests:
        manifest_failures, manifest_notes, data = validate_manifest(
            root, path, external_notice_routes
        )
        failures.extend(manifest_failures)
        notes.extend(manifest_notes)
        if data is not None and isinstance(data.get("tranche_id"), str):
            by_id[str(data["tranche_id"])] = data
            by_path[path.relative_to(root).as_posix()] = data

    if diff_mode:
        if tranche is not None and tranche not in by_id:
            lines.append(
                f"G4 OPERATIONAL (exit 2): no manifest declares tranche_id {tranche!r} "
                f"under {MANIFEST_DIR_RELPATH.as_posix()}."
            )
            return 2, lines
        changed, error = changed_paths(root, str(base), str(head))
        if changed is None:
            lines.append(f"G4 OPERATIONAL (exit 2): {error}")
            return 2, lines
        touched = [p for p in changed if intersects_instruction_surface(p)]
        if tranche is not None:
            sources = [by_id[tranche]]
        elif added_manifests_only:
            added, added_error = added_paths(root, str(base), str(head))
            if added is None:
                lines.append(f"G4 OPERATIONAL (exit 2): {added_error}")
                return 2, lines
            sources = [by_path[p] for p in added if p in by_path]
            if touched and not sources:
                failures.append(
                    f"diff {base}..{head} changes instruction-surface paths but adds no "
                    "schema-readable tranche manifest"
                )
        else:
            sources = list(by_id.values())
        declared: list[str] = []
        for data in sources:
            values = data.get("instruction_surface_paths")
            if isinstance(values, list):
                declared.extend(str(v) for v in values)
        uncovered = [p for p in touched if not covered_by(p, declared)]
        for path_str in uncovered:
            failures.append(
                f"instruction-surface path {path_str!r} changed in {base}..{head} but "
                "is not covered by any declared tranche manifest path"
            )
        notes.append(
            f"diff {base}..{head}: {len(changed)} changed path(s), {len(touched)} on the "
            f"instruction surface, checked against {len(sources)} manifest(s)"
        )

    mode = "diff" if diff_mode else "CI"
    if failures:
        lines.append(f"G4 BLOCK ({mode} mode):")
        lines.extend(f"  - {failure}" for failure in failures)
        lines.extend(f"  INFO: {note}" for note in notes)
        return 1, lines

    lines.append(
        f"G4 PASS ({mode} mode): {len(manifests)} tranche manifest(s) under "
        f"{MANIFEST_DIR_RELPATH.as_posix()} are schema-valid ({MANIFEST_SCHEMA}); "
        f"declared tranches: {sorted(by_id)}."
    )
    lines.extend(f"  INFO: {note}" for note in notes)
    return 0, lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "G4 instruction-surface tranche manifest check (D-GOV-21 §5.3). No "
            "arguments: CI mode. With --base and --head: diff mode."
        )
    )
    parser.add_argument("--base", help="Base ref for diff mode (base..head).")
    parser.add_argument("--head", help="Head ref for diff mode (base..head).")
    parser.add_argument(
        "--tranche",
        help="Restrict diff-mode coverage to the manifest with this tranche_id.",
    )
    parser.add_argument(
        "--added-manifests-only",
        action="store_true",
        help=(
            "Accept diff coverage only from manifest files added in "
            "the diff; the whole manifest corpus is still schema-validated."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if bool(args.base) != bool(args.head):
        print("G4 OPERATIONAL (exit 2): diff mode requires both --base and --head.")
        return 2
    if args.tranche and not args.base:
        print("G4 OPERATIONAL (exit 2): --tranche applies to diff mode only.")
        return 2
    if args.added_manifests_only and not args.base:
        print(
            "G4 OPERATIONAL (exit 2): --added-manifests-only applies to diff mode only."
        )
        return 2
    if args.tranche and args.added_manifests_only:
        print(
            "G4 OPERATIONAL (exit 2): --tranche and --added-manifests-only are "
            "mutually exclusive."
        )
        return 2
    root = repo_root()
    code, lines = check(
        root,
        args.base,
        args.head,
        args.tranche,
        added_manifests_only=args.added_manifests_only,
    )
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
