#!/usr/bin/env python3
"""Apply only the owner-approved 53 Root retirement postimages.

This is a migration transaction, not a lifecycle transition. Gate 4 publication
authorizes execution; future Gate 5 confirmation is deliberately not an input.
All evidence is append-only in a new invocation directory. No pointer or Git
mutation is available. Interrupted journals require guarded recovery, never
automatic completion of a mixed state.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import yaml
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/validation"))
GUARDS = (
    "validate_root_materialization_fence", "validate_root_harness_adapter",
    "validate_root_surface_ownership", "validate_root_work_graph_dispatch",
    "validate_instruction_tranche_manifest",
)
CONFIGS = tuple("execution/_harness/" + name + ".yaml" for name in (
    "adapter", "root_guards", "surface_ownership", "work_graph"))
EVIDENCE_ROOTS = (
    "execution/_ScopeChange/SCA-005_2026-09-06_APPLICATION/",
    "execution/_Coordination/AgentRuns/ROOT_RUNTIME_AUTHORITY_APPLICATION_20260906/",
    "execution/_Coordination/AgentRuns/ROOT_RUNTIME_MIGRATION_GATE5_2026-09-06/",
)
SELF = "tools/scaffolding/apply_root_retirement.py"
TEST = "tools/validation/test_apply_root_retirement.py"
REQUIRED_SUITES = {TEST, "tools/validation/test_root_governance_state.py",
                   *("tools/validation/test_" + name + ".py" for name in GUARDS)}
STATUS = re.compile(r"execution/PKG-0[1-6]_[^/]+/1_Working/DEL-\d{2}-\d{2}_[^/]+/_STATUS\.md\Z")


class Refusal(RuntimeError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    """Durably publish journal updates; evidence paths are never source targets."""
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    descriptor, temporary_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def durable_bytes(path: Path, data: bytes):
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def replace_bytes(path: Path, data: bytes, temporary: Path):
    durable_bytes(temporary, data)
    mode = path.stat().st_mode & 0o777
    os.chmod(temporary, mode)
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def verified(root: Path, ref: dict) -> Path:
    from root_governance_state import safe_path
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise Refusal("Reference must contain only path and sha256")
    path = safe_path(root, ref["path"])
    if not path.is_file() or sha(path.read_bytes()) != ref["sha256"]:
        raise Refusal(f"Hash mismatch: {ref['path']}")
    return path


def load_subject(root: Path, subject_path: Path, effect_path: Path):
    from root_governance_state import load_governance_state, verify_owner_act
    subject = read_json(subject_path)
    effect = read_json(effect_path)
    digest = sha(subject_path.read_bytes())
    if not isinstance(subject, dict) or set(subject) != {"schema", "governance_state", "tested_files", "fixture_suites"}:
        raise Refusal("Unknown or missing subject fields")
    if not isinstance(effect, dict) or set(effect) != {"schema", "subject_sha256", "owner_act"}:
        raise Refusal("Unknown or missing execution record fields")
    if subject.get("schema") != "root-retirement-application/v1":
        raise Refusal("Unknown application subject schema")
    if effect.get("schema") != "root-retirement-execution/v1" or effect.get("subject_sha256") != digest:
        raise Refusal("Execution record does not bind this exact subject")
    from root_governance_state import GovernanceError
    config = {"mode": "governance-only", "governance_state": subject["governance_state"]}
    try:
        state = load_governance_state(root, config, require_effective=False, verify_statuses="preimage")
    except GovernanceError:
        state = load_governance_state(root, config, require_effective=False, verify_statuses="postimage")
    if effect["owner_act"] != state["gate4"]:
        raise Refusal("Execution authority must be the selected published Gate 4 record")
    verify_owner_act(root, effect["owner_act"], state["propagation_plan"]["sha256"])
    rows = state["source_statuses"]
    paths = [row["path"] for row in rows]
    if len(rows) != 53 or len(set(paths)) != 53 or any(not STATUS.fullmatch(p) for p in paths):
        raise Refusal("Subject must contain exactly 53 unique Root status targets")
    if len({row["source_package"] for row in rows}) != 6 or len({row["source_id"] for row in rows}) != 53:
        raise Refusal("Source identity or six-parent census mismatch")
    statuses = []
    for row in rows:
        from root_governance_state import safe_path
        target = safe_path(root, row["path"])
        post = verified(root, {"path": row["postimage_path"], "sha256": row["postimage_sha256"]}).read_bytes()
        before = target.read_bytes()
        if sha(before) not in (row["preimage_sha256"], row["postimage_sha256"]):
            raise Refusal(f"Changed preimage: {row['path']}")
        # The approved postimage is an immutable full file, never generated text.
        if b"RETIRED" not in post or row["preimage_sha256"] == row["postimage_sha256"]:
            raise Refusal(f"Invalid retirement postimage: {row['path']}")
        for memory in (target.with_name("_MEMORY.md"), target.with_name("MEMORY.md")):
            if memory.exists():
                safe_path(root, memory.relative_to(root).as_posix()).read_bytes()  # Paired memory read.
        statuses.append((row, before, post))
    observed = {"post" if sha(before) == row["postimage_sha256"] else "pre" for row, before, _ in statuses}
    if len(observed) != 1:
        raise Refusal("Mixed source state; use recorded guarded recovery, not completion")
    pins = subject.get("tested_files", [])
    pinned_paths = [p["path"] for p in pins]
    required = {SELF, TEST, "tools/validation/root_governance_state.py", *CONFIGS,
                *("tools/validation/" + name + ".py" for name in GUARDS), subject["governance_state"]["path"]}
    if len(set(pinned_paths)) != len(pins) or not required.issubset(pinned_paths):
        raise Refusal("Missing or duplicate implementation/configuration pins")
    for pin in pins:
        if set(pin) != {"path", "sha256"}:
            raise Refusal("Malformed implementation pin")
        if pin["path"] not in required and not re.fullmatch(
                r"tools/(validation|practitioner_harness|scaffolding)/[A-Za-z0-9_]+\.(py|sh)", pin["path"]):
            raise Refusal("Pin outside guard implementation/configuration allowlist")
        verified(root, pin)
    suites = subject.get("fixture_suites", [])
    if not REQUIRED_SUITES.issubset({suite["path"] for suite in suites}):
        raise Refusal("All G0-G4, shared-state and applicator positive/negative suites are required")
    for suite in suites:
        if not re.fullmatch(r"tools/validation/test_[A-Za-z0-9_]+\.py", suite["path"]):
            raise Refusal("Fixture suite must be a pinned validation test file")
        verified(root, suite)
        if suite not in pins:
            raise Refusal("Fixture suite missing from tested implementation pins")
    return subject, digest, statuses, observed == {"post"}


def run_fixtures(root: Path, subject: dict, evidence: Path):
    results = []
    for number, suite in enumerate(subject["fixture_suites"]):
        command = [sys.executable, "-m", "pytest", "-q", suite["path"]]
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        (evidence / f"fixture-{number}.log").write_text(result.stdout + result.stderr)
        results.append({"command": command, "exit_code": result.returncode,
                        "suite": suite, "tested_files": subject["tested_files"]})
        write_json(evidence / f"fixture-{number}.json", results[-1])
        if result.returncode:
            raise Refusal(f"Positive/negative fixture suite failed: {suite['path']}")


def run_guards(root: Path, evidence: Path, phase: str):
    results = []
    for module_name in GUARDS:
        module = importlib.import_module(module_name)
        code, lines = module.check(root)
        results.append({"guard": module_name, "exit_code": code, "output": lines})
        if code:
            write_json(evidence / f"{phase}-guards.json", results)
            raise Refusal(f"{phase} guard failed: {module_name}: {lines}")
    write_json(evidence / f"{phase}-guards.json", results)


def prospective(root: Path, statuses, evidence: Path, subject=None):
    # Only tracked files and explicit accepted pending targets/references are
    # copied. Ignored local runtime/account state is never snapshot material.
    from root_governance_state import safe_path, PLAN
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=root,
                             capture_output=True, check=True).stdout.decode().split("\0")
    tracked_paths = {path for path in tracked if path}
    paths = set(tracked_paths)
    for filename, column in (("WRITE_TARGETS.csv", "Target"), ("GUARDS/WRITE_PATH_INVENTORY.csv", "Path")):
        with safe_path(root, PLAN + "/" + filename).open(newline="") as stream:
            paths.update(row[column] for row in csv.DictReader(stream) if "*" not in row[column])
    def reference(ref):
        if ref is not None:
            relative = ref["path"]
            if relative not in paths and not relative.startswith(EVIDENCE_ROOTS):
                raise Refusal("Undeclared prospective reference: " + relative)
            paths.add(relative)
    if subject:
        for pin in subject["tested_files"]: reference(pin)
        reference(subject["governance_state"])
        state = read_json(verified(root, subject["governance_state"]))
        for key in ("selected_subject", "propagation_plan", "gate3", "gate4", "gate5", "transaction"):
            reference(state.get(key))
        for binding in state.get("successor_bindings", []):
            reference({"path": binding["path"]})
            reference(binding["authority"])
    # Live reviewed YAMLs may point to the distinct prospective/applied state;
    # the execution subject itself still binds the prepared state.
    for config_path in CONFIGS:
        config = yaml.safe_load(safe_path(root, config_path).read_text())
        if isinstance(config, dict) and config.get("governance_state"):
            reference(config["governance_state"])
            verified(root, config["governance_state"])
    with tempfile.TemporaryDirectory(prefix="prospective-", dir=evidence) as temporary:
        scratch = Path(temporary)
        excluded_symlinks = []
        for relative in sorted(paths):
            if (root / relative).is_symlink():
                excluded_symlinks.append(relative)
                continue  # Historical tracked link: never dereference in prospective state.
            if relative in tracked_paths:
                # Git paths are literal filenames: Next.js [id] is not a glob.
                source = root / relative
                try:
                    source.resolve().relative_to(root.resolve())
                except ValueError as error:
                    raise Refusal("Tracked snapshot path escapes checkout: " + relative) from error
                if any(parent.is_symlink() for parent in source.parents if parent != root and parent.is_relative_to(root)):
                    excluded_symlinks.append(relative)
                    continue
            else:
                source = safe_path(root, relative, allow_missing=True)
            if not source.exists(): continue
            if not source.is_file(): raise Refusal("Snapshot input is not a regular file: " + relative)
            if source.is_relative_to(evidence): continue
            destination = scratch / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination, follow_symlinks=False)
        write_json(evidence / "prospective-excluded-symlinks.json", excluded_symlinks)
        gitdir = subprocess.run(["git", "rev-parse", "--absolute-git-dir"], cwd=root,
                                text=True, capture_output=True, check=True).stdout.strip()
        (scratch / ".git").write_text("gitdir: " + gitdir + "\n")
        for row, _, post in statuses:
            (scratch / row["path"]).write_bytes(post)
        if subject is not None:
            run_fixtures(scratch, subject, evidence)
        run_guards(scratch, evidence, "prospective")


def transact(root: Path, statuses, evidence: Path, digest: str, guard_runner=run_guards, after_write=None):
    """Recover only files that still equal our exact postimage, including interrupts."""
    from root_governance_state import safe_path
    journal = {"schema": "root-retirement-journal/v1", "subject_sha256": digest,
               "state": "PREPARED", "entries": [], "blocked": []}
    for index, (row, before, _) in enumerate(statuses):
        backup = f"preimage-{index}.bin"
        durable_bytes(evidence / backup, before)
        journal["entries"].append({**row, "backup": backup})
    write_json(evidence / "journal.json", journal)
    try:
        journal["state"] = "APPLYING"
        write_json(evidence / "journal.json", journal)
        for index, (row, before, post) in enumerate(statuses):
            path = safe_path(root, row["path"])
            if path.read_bytes() != before:
                raise Refusal(f"Concurrent source edit: {row['path']}")
            replace_bytes(path, post, evidence / f"replacement-{index}.bin")
            if after_write is not None:
                after_write(index, path)
        guard_runner(root, evidence, "live")
        journal["state"] = "APPLIED"
        write_json(evidence / "journal.json", journal)
    except BaseException:
        journal["state"] = "ROLLING_BACK"
        try:
            write_json(evidence / "journal.json", journal)
        except OSError as error:
            # A failed evidence device must not prevent restoration of source bytes.
            journal["journal_error"] = str(error)
        for index, (row, before, post) in enumerate(statuses):
            try:
                path = safe_path(root, row["path"])
                current = path.read_bytes()
                if current == post:
                    replace_bytes(path, before, evidence / f"rollback-{index}.bin")
                elif current != before:
                    journal["blocked"].append(row["path"])
            except (OSError, ValueError, RuntimeError):
                journal["blocked"].append(row["path"])
        journal["state"] = "BLOCKED_PARTIAL" if journal["blocked"] else "ROLLED_BACK"
        try:
            write_json(evidence / "journal.json", journal)
        except OSError as error:
            print(f"RETIREMENT RECOVERY JOURNAL BLOCK: {error}; {journal}", file=sys.stderr)
        raise


def execute(root: Path, subject_path: Path, effect_path: Path, evidence: Path, apply: bool):
    from root_governance_state import safe_path
    try:
        relative = evidence.absolute().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise Refusal("Evidence directory must remain in the declared migration run") from error
    if not relative.startswith(EVIDENCE_ROOTS):
        raise Refusal("Evidence directory outside approved migration evidence scopes")
    evidence = safe_path(root, relative, allow_missing=True)
    subject, digest, statuses, already = load_subject(root, subject_path, effect_path)
    state = read_json(verified(root, subject["governance_state"]))
    transaction = state.get("transaction")
    if apply or already:
        from root_governance_state import safe_path
        if not transaction:
            raise Refusal("Application requires a declared transaction journal")
        journal_path = safe_path(root, transaction["path"], allow_missing=True)
        if already:
            previous = read_json(journal_path)
            if previous.get("state") != "APPLIED" or previous.get("subject_sha256") != digest:
                raise Refusal("Postimages lack a completed journal for this exact subject")
        elif transaction.get("sha256") is not None or journal_path != evidence.resolve() / "journal.json":
            raise Refusal("Evidence directory must match the serialized pending transaction path")
    # Existing evidence may never be overwritten or used as a fresh execution claim.
    evidence.mkdir(parents=True, exist_ok=False)
    write_json(evidence / "invocation.json", {"subject_sha256": digest,
               "effect_sha256": sha(effect_path.read_bytes()), "apply": apply,
               "at": datetime.now(timezone.utc).isoformat(), "fixture_authority": False})
    prospective(root, statuses, evidence, subject)
    # Re-read authority, code, config and all sources after expensive checks.
    _, repeated, _, repeated_already = load_subject(root, subject_path, effect_path)
    if repeated != digest or repeated_already != already:
        raise Refusal("Subject or source state changed during preflight")
    if already:
        run_guards(root, evidence, "idempotent")
        write_json(evidence / "result.json", {"state": "ALREADY_APPLIED", "subject_sha256": digest})
    elif apply:
        transact(root, statuses, evidence, digest)
    else:
        write_json(evidence / "result.json", {"state": "DRY_RUN_PASS", "subject_sha256": digest})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject-manifest", required=True, type=Path)
    parser.add_argument("--effect-record", required=True, type=Path)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        execute(ROOT, args.subject_manifest.resolve(), args.effect_record.resolve(), args.evidence_dir.absolute(), args.apply)
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"RETIREMENT BLOCK: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
