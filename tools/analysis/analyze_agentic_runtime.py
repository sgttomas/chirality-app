#!/usr/bin/env python3
"""Analyze governed agent-run runtime and failure evidence.

Contract
========
Inputs:
  --repo-root: Git checkout containing the governed run.
  --run-root: Stage execution run containing package, child, RECON, and CHANGE records.
  --event-catalog: curated CSV of abnormal episodes with exact evidence needles.
  --output-dir: dedicated derivative output directory.

Outputs:
  summary.json, events.csv, report.md, and MANIFEST.tsv under --output-dir.

Scope and posture:
  Read-only outside --output-dir. The tool validates rather than invents event
  classifications: every catalog row must bind an existing evidence file and
  exact text. Statistics are descriptive; Wilson intervals quantify sampling
  uncertainty only and do not make the governed units independent/random.

Exit codes:
  0 success; 1 invalid input/evidence; 2 operational error.

Idempotence:
  Idempotent for identical repository bytes, Git metadata, and catalog input.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


PACKAGE_RE = re.compile(r"^WORKING-(A\d+)-PKG\d+$")
CHILD_RE = re.compile(r"^(AUTHOR|VERIFY)-(DEL-\d{2}-\d{2})(?:-R\d+)?$")
CHANGE_RE = re.compile(r"^CHANGE-(A\d+)-G$")

EVENT_COLUMNS = [
    "event_id",
    "wave",
    "package",
    "deliverable",
    "stage",
    "category",
    "subtype",
    "scope_kind",
    "affected_units",
    "substantive_impact",
    "detected_by",
    "outcome",
    "evidence_path",
    "evidence_needle",
]

EVENT_CATEGORIES = {
    "BRIEF_OR_INPUT",
    "TOOL_INVOCATION",
    "PROJECT_CHECK_SUBSTRATE",
    "NEGATIVE_FIXTURE_SETUP",
    "EVIDENCE_TERMINALIZATION",
    "EVIDENCE_PORTABILITY",
    "SUSPECTED_NOT_REPRODUCED",
}
IMPACT_VALUES = {"NONE", "EVIDENCE_ONLY", "SUBSTANTIVE"}
SCOPE_KINDS = {"child", "package", "wave"}


class AnalysisError(ValueError):
    """Input or evidence is invalid."""


@dataclass(frozen=True)
class EvidenceEvent:
    row: dict[str, str]
    evidence_sha256: str
    evidence_line: int


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AnalysisError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AnalysisError(f"expected JSON object: {path}")
    return value


def require_within(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise AnalysisError(f"{label} escapes {root}: {path}") from exc
    return resolved


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> dict[str, float | int]:
    if trials < 0 or successes < 0 or successes > trials:
        raise AnalysisError(f"invalid binomial values: {successes}/{trials}")
    if trials == 0:
        return {"successes": successes, "trials": trials, "rate": 0.0, "low": 0.0, "high": 1.0}
    p = successes / trials
    denominator = 1.0 + z * z / trials
    center = (p + z * z / (2.0 * trials)) / denominator
    half = z * math.sqrt((p * (1.0 - p) + z * z / (4.0 * trials)) / trials) / denominator
    return {
        "successes": successes,
        "trials": trials,
        "rate": p,
        "low": max(0.0, center - half),
        "high": min(1.0, center + half),
    }


def percentile(values: list[float], proportion: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = proportion * (len(ordered) - 1)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    fraction = rank - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def duration_stats(values: Iterable[float]) -> dict[str, float | int | None]:
    data = [float(value) for value in values]
    return {
        "count": len(data),
        "total_seconds": round(sum(data), 3),
        "mean_seconds": round(statistics.fmean(data), 3) if data else None,
        "median_seconds": round(statistics.median(data), 3) if data else None,
        "p95_seconds": round(percentile(data, 0.95), 3) if data else None,
        "min_seconds": round(min(data), 3) if data else None,
        "max_seconds": round(max(data), 3) if data else None,
    }


def collect_packages(instances_root: Path) -> list[dict[str, Any]]:
    packages: list[dict[str, Any]] = []
    for directory in sorted(path for path in instances_root.iterdir() if path.is_dir() and PACKAGE_RE.match(path.name)):
        status_path = directory / "STATUS.json"
        if not status_path.is_file():
            raise AnalysisError(f"package status missing: {status_path}")
        status = read_json(status_path)
        match = PACKAGE_RE.match(directory.name)
        assert match
        members = int(status.get("members", status.get("member_count", 0)))
        packages.append(
            {
                "instance": directory.name,
                "wave": match.group(1),
                "package": str(status.get("package") or status.get("package_id") or directory.name),
                "status": str(status.get("status", "")),
                "terminal": bool(status.get("terminal", False)),
                "members": members,
                "mappings": int(status.get("mapping_rows", status.get("mappings", status.get("mapping_count", 0)))),
                "source_lines": int(status.get("source_lines", status.get("source_line_count", 0))),
                "replacement_rows": int(status.get("replacement_rows", 0)),
                "rollback_rows": int(status.get("rollback_rows", 0)),
                "project_writes": int(status.get("project_writes", status.get("live_project_writes", 0))),
                "status_path": status_path,
            }
        )
    if not packages:
        raise AnalysisError(f"no App package instances found under {instances_root}")
    return packages


def collect_children(instances_root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for package_dir in sorted(path for path in instances_root.iterdir() if path.is_dir() and PACKAGE_RE.match(path.name)):
        wave = PACKAGE_RE.match(package_dir.name).group(1)  # type: ignore[union-attr]
        children_root = package_dir / "children"
        if not children_root.is_dir():
            continue
        for child in sorted(path for path in children_root.iterdir() if path.is_dir()):
            match = CHILD_RE.match(child.name)
            if not match:
                continue
            status_path = child / "STATUS.json"
            status: dict[str, Any] = read_json(status_path) if status_path.is_file() else {}
            rows.append(
                {
                    "wave": wave,
                    "package_instance": package_dir.name,
                    "child": child.name,
                    "role": match.group(1),
                    "deliverable": match.group(2),
                    "retry_suffix": bool(re.search(r"-R\d+$", child.name)),
                    "has_launch_brief": (child / "LAUNCH_BRIEF.md").is_file(),
                    "has_status": status_path.is_file(),
                    "status": str(status.get("status", "")),
                    "terminal": status.get("terminal"),
                    "verdict": str(status.get("verdict", "")),
                }
            )
    closeouts_by_wave = Counter(row["wave"] for row in rows if "MANAGER_EVIDENCE_CLOSEOUT" in row["status"])
    retries_by_wave = Counter(row["wave"] for row in rows if row["retry_suffix"])
    return {
        "rows": rows,
        "documented_attempts": sum(row["has_launch_brief"] for row in rows),
        "status_records": sum(row["has_status"] for row in rows),
        "retry_named_attempts": sum(row["retry_suffix"] for row in rows),
        "manager_evidence_closeouts": sum("MANAGER_EVIDENCE_CLOSEOUT" in row["status"] for row in rows),
        "manager_evidence_closeouts_by_wave": dict(sorted(closeouts_by_wave.items())),
        "retry_named_attempts_by_wave": dict(sorted(retries_by_wave.items())),
        "failed_status_records": sum(
            row["has_status"] and ("FAIL" in row["status"] or "STALLED" in row["status"])
            for row in rows
        ),
        "status_distribution": dict(sorted(Counter(row["status"] or "MISSING" for row in rows).items())),
    }


def collect_project_checks(instances_root: Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for package_dir in sorted(path for path in instances_root.iterdir() if path.is_dir() and PACKAGE_RE.match(path.name)):
        wave = PACKAGE_RE.match(package_dir.name).group(1)  # type: ignore[union-attr]
        for path in sorted(package_dir.glob("PROJECT_CHECKS*.json")):
            payload = read_json(path)
            results = payload.get("results", payload.get("checks", []))
            if not isinstance(results, list):
                raise AnalysisError(f"results must be a list: {path}")
            for result in results:
                if not isinstance(result, dict):
                    raise AnalysisError(f"non-object result in {path}")
                raw_duration = result.get("duration_seconds", result.get("elapsed_seconds"))
                try:
                    duration = float(raw_duration) if raw_duration is not None else None
                    exit_code = int(result.get("exit_code", 0))
                except (TypeError, ValueError) as exc:
                    raise AnalysisError(f"invalid duration/exit in {path}") from exc
                status = str(result.get("status", ""))
                records.append(
                    {
                        "wave": wave,
                        "package_instance": package_dir.name,
                        "evidence": path.relative_to(instances_root.parent.parent).as_posix(),
                        "check_id": str(result.get("id", result.get("check", result.get("check_id", "")))),
                        "status": status,
                        "exit_code": exit_code,
                        "duration_seconds": duration,
                        "failed": status != "PASS" or exit_code != 0,
                    }
                )
    by_check: dict[str, Any] = {}
    for check_id in sorted({record["check_id"] for record in records}):
        selected = [record for record in records if record["check_id"] == check_id]
        by_check[check_id] = {
            **duration_stats(record["duration_seconds"] for record in selected if record["duration_seconds"] is not None),
            "invocations": len(selected),
            "timed_invocations": sum(record["duration_seconds"] is not None for record in selected),
            "passes": sum(not record["failed"] for record in selected),
            "failures": sum(record["failed"] for record in selected),
        }
    failures = [record for record in records if record["failed"]]
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(record["wave"], record["check_id"])].append(record)
    retained_measured_seconds = 0.0
    all_measured_seconds = sum(
        record["duration_seconds"] for record in records if record["duration_seconds"] is not None
    )
    for selected in grouped.values():
        timed_passes = [
            record["duration_seconds"]
            for record in selected
            if not record["failed"] and record["duration_seconds"] is not None
        ]
        timed_any = [record["duration_seconds"] for record in selected if record["duration_seconds"] is not None]
        if timed_passes:
            retained_measured_seconds += max(timed_passes)
        elif timed_any:
            retained_measured_seconds += max(timed_any)
    per_wave_cache = {
        "assumption": "one successful invocation per wave/check identity; package candidates do not mutate the live project",
        "current_invocations": len(records),
        "retained_invocations": len(grouped),
        "avoidable_invocations": len(records) - len(grouped),
        "avoidable_invocation_fraction": (len(records) - len(grouped)) / len(records) if records else 0.0,
        "measured_seconds_retained_conservative": round(retained_measured_seconds, 3),
        "measured_seconds_avoidable_lower_bound": round(all_measured_seconds - retained_measured_seconds, 3),
    }
    return {
        "records": records,
        "invocations": len(records),
        "passes": len(records) - len(failures),
        "failures": len(failures),
        "timed_invocations": sum(record["duration_seconds"] is not None for record in records),
        "untimed_invocations": sum(record["duration_seconds"] is None for record in records),
        "duration": duration_stats(record["duration_seconds"] for record in records if record["duration_seconds"] is not None),
        "failed_duration": duration_stats(record["duration_seconds"] for record in failures if record["duration_seconds"] is not None),
        "by_check": by_check,
        "per_wave_cache_scenario": per_wave_cache,
        "packages_with_failed_first_premerge": sorted(
            {record["package_instance"] for record in failures if record["check_id"] == "frontend-premerge"}
        ),
    }


def git_timestamp(repo_root: Path, commit: str) -> datetime:
    process = subprocess.run(
        ["git", "show", "-s", "--format=%cI", commit],
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode != 0:
        raise AnalysisError(f"cannot resolve Git timestamp for {commit}: {process.stderr.strip()}")
    try:
        return datetime.fromisoformat(process.stdout.strip())
    except ValueError as exc:
        raise AnalysisError(f"invalid Git timestamp for {commit}: {process.stdout.strip()}") from exc


def collect_wave_windows(repo_root: Path, instances_root: Path, packages: list[dict[str, Any]], include_git: bool) -> list[dict[str, Any]]:
    if not include_git:
        return []
    aggregates: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for package in packages:
        wave = package["wave"]
        for key in ("members", "mappings", "source_lines"):
            aggregates[wave][key] += int(package[key])
    rows: list[dict[str, Any]] = []
    for directory in sorted(path for path in instances_root.iterdir() if path.is_dir() and CHANGE_RE.match(path.name)):
        status = read_json(directory / "STATUS.json")
        wave = CHANGE_RE.match(directory.name).group(1)  # type: ignore[union-attr]
        basis = str(status.get("basis_commit", ""))
        binding = str(status.get("evidence_binding_commit", ""))
        remote = status.get("remote", {})
        merge = str(remote.get("merge_commit", "")) if isinstance(remote, dict) else ""
        if not all((basis, binding, merge)):
            raise AnalysisError(f"incomplete CHANGE timing identities: {directory}")
        basis_time = git_timestamp(repo_root, basis)
        binding_time = git_timestamp(repo_root, binding)
        merge_time = git_timestamp(repo_root, merge)
        prep_seconds = (binding_time - basis_time).total_seconds()
        merge_lag_seconds = (merge_time - binding_time).total_seconds()
        envelope_seconds = (merge_time - basis_time).total_seconds()
        if min(prep_seconds, merge_lag_seconds, envelope_seconds) < 0:
            raise AnalysisError(f"negative Git timing window for {wave}")
        members = aggregates[wave]["members"]
        source_lines = aggregates[wave]["source_lines"]
        rows.append(
            {
                "wave": wave,
                "basis_commit": basis,
                "evidence_binding_commit": binding,
                "merge_commit": merge,
                "basis_time": basis_time.isoformat(),
                "binding_time": binding_time.isoformat(),
                "merge_time": merge_time.isoformat(),
                "preparation_seconds": prep_seconds,
                "merge_lag_seconds": merge_lag_seconds,
                "activation_to_merge_seconds": envelope_seconds,
                "members": members,
                "mappings": aggregates[wave]["mappings"],
                "source_lines": source_lines,
                "members_per_hour": members / (envelope_seconds / 3600.0),
                "source_lines_per_minute_preparation": source_lines / (prep_seconds / 60.0),
            }
        )
    return rows


def collect_reconciliations(instances_root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for status_path in sorted(instances_root.glob("RECON-A[123]-F/STATUS.json")):
        status = read_json(status_path)
        rows.append(
            {
                "instance": status_path.parent.name,
                "status": str(status.get("status", "")),
                "members": int(status.get("members", 0)),
                "mappings": int(status.get("mapping_rows", status.get("mappings", 0))),
                "source_lines": int(status.get("source_lines", 0)),
                "apply_simulations": int(status.get("apply_simulations_passed", status.get("apply_simulations", 0))),
                "rollback_simulations": int(status.get("rollback_simulations_passed", status.get("rollback_simulations", 0))),
                "project_writes": int(status.get("project_writes", 0)),
            }
        )
    return {
        "instances": rows,
        "passes": sum(row["status"] == "PASS" for row in rows),
        "members": sum(row["members"] for row in rows),
        "apply_simulations": sum(row["apply_simulations"] for row in rows),
        "rollback_simulations": sum(row["rollback_simulations"] for row in rows),
        "project_writes": sum(row["project_writes"] for row in rows),
    }


def load_events(repo_root: Path, catalog_path: Path) -> list[EvidenceEvent]:
    try:
        with catalog_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != EVENT_COLUMNS:
                raise AnalysisError(f"event catalog columns must be exactly {EVENT_COLUMNS}; got {reader.fieldnames}")
            rows = list(reader)
    except OSError as exc:
        raise AnalysisError(f"cannot read event catalog {catalog_path}: {exc}") from exc
    seen: set[str] = set()
    events: list[EvidenceEvent] = []
    for number, row in enumerate(rows, start=2):
        event_id = row["event_id"].strip()
        if not event_id or event_id in seen:
            raise AnalysisError(f"missing/duplicate event_id at catalog row {number}: {event_id}")
        seen.add(event_id)
        category = row["category"].strip()
        impact = row["substantive_impact"].strip()
        scope_kind = row["scope_kind"].strip()
        if category not in EVENT_CATEGORIES:
            raise AnalysisError(f"unknown event category {category} at row {number}")
        if impact not in IMPACT_VALUES:
            raise AnalysisError(f"unknown substantive impact {impact} at row {number}")
        if scope_kind not in SCOPE_KINDS:
            raise AnalysisError(f"unknown scope kind {scope_kind} at row {number}")
        try:
            affected = int(row["affected_units"])
        except ValueError as exc:
            raise AnalysisError(f"affected_units is not an integer at row {number}") from exc
        if affected < 1:
            raise AnalysisError(f"affected_units must be positive at row {number}")
        evidence_path = require_within(repo_root / row["evidence_path"], repo_root, "evidence_path")
        if not evidence_path.is_file():
            raise AnalysisError(f"event evidence missing at row {number}: {evidence_path}")
        text = evidence_path.read_text(encoding="utf-8")
        needle = row["evidence_needle"]
        if not needle or needle not in text:
            raise AnalysisError(f"event needle absent at row {number}: {event_id} in {evidence_path}")
        line = text[: text.index(needle)].count("\n") + 1
        normalized = {column: row[column].strip() for column in EVENT_COLUMNS}
        events.append(EvidenceEvent(normalized, sha256_path(evidence_path), line))
    return sorted(events, key=lambda event: event.row["event_id"])


def event_statistics(events: list[EvidenceEvent], packages: int, members: int, baseline_child_roles: int) -> dict[str, Any]:
    by_category: dict[str, Any] = {}
    for category in sorted(EVENT_CATEGORIES):
        selected = [event for event in events if event.row["category"] == category]
        if not selected:
            continue
        by_category[category] = {
            "episodes": len(selected),
            "affected_units": sum(int(event.row["affected_units"]) for event in selected),
            "packages": len({event.row["package"] for event in selected if event.row["package"]}),
            "deliverables": len({event.row["deliverable"] for event in selected if event.row["deliverable"]}),
            "subtypes": dict(sorted(Counter(event.row["subtype"] for event in selected).items())),
        }
    by_wave: dict[str, Any] = {}
    for wave in sorted({event.row["wave"] for event in events}):
        selected = [event for event in events if event.row["wave"] == wave]
        by_wave[wave] = {
            "episodes": len(selected),
            "affected_units": sum(int(event.row["affected_units"]) for event in selected),
            "categories": dict(sorted(Counter(event.row["category"] for event in selected).items())),
        }
    substantive = [event for event in events if event.row["substantive_impact"] == "SUBSTANTIVE"]
    return {
        "episodes": len(events),
        "affected_units": sum(int(event.row["affected_units"]) for event in events),
        "affected_packages": len({event.row["package"] for event in events if event.row["package"]}),
        "affected_deliverables": len({event.row["deliverable"] for event in events if event.row["deliverable"]}),
        "substantive_episodes": len(substantive),
        "by_category": by_category,
        "by_wave": by_wave,
        "by_detection_layer": dict(sorted(Counter(event.row["detected_by"] for event in events).items())),
        "by_outcome": dict(sorted(Counter(event.row["outcome"] for event in events).items())),
        "reference_denominators": {
            "packages": packages,
            "members": members,
            "baseline_child_roles": baseline_child_roles,
        },
    }


def render_report(summary: dict[str, Any]) -> str:
    inventory = summary["inventory"]
    child = summary["children"]
    checks = summary["project_checks"]
    events = summary["events"]
    intervals = summary["intervals"]
    recon = summary["reconciliation"]
    cache = checks["per_wave_cache_scenario"]
    lines = [
        "# App Stage-2 Agentic Runtime and Failure Analysis",
        "",
        "> Deterministic derivative report. The cited run evidence governs. Rates are descriptive;",
        "> Wilson intervals do not make packages, agents, or deliverables independent random samples.",
        "",
        "## Population and outcomes",
        "",
        f"- Packages / waves / members: {inventory['packages']} / {inventory['waves']} / {inventory['members']}.",
        f"- Author/verifier baseline roles: {inventory['baseline_child_roles']}; documented child-attempt directories: {child['documented_attempts']}.",
        f"- Mappings / source lines: {inventory['mappings']:,} / {inventory['source_lines']:,}.",
        f"- Eventual accepted candidates: {inventory['members']}/{inventory['members']}; substantive candidate failures in the catalog: {events['substantive_episodes']}.",
        f"- RECON apply/rollback simulations: {recon['apply_simulations']}/{recon['rollback_simulations']} across {recon['members']} members; project writes: {recon['project_writes']}.",
        f"- Manager-evidence-closeout statuses: {child['manager_evidence_closeouts']}; retry-suffixed attempt directories: {child['retry_named_attempts']}.",
        "",
        "## Command-level project checks",
        "",
        f"- Recorded invocations: {checks['invocations']} ({checks['passes']} PASS, {checks['failures']} FAIL).",
        f"- Recorded command time: {checks['duration']['total_seconds']:.3f} seconds across {checks['timed_invocations']} timed invocations; {checks['untimed_invocations']} invocations lack durations.",
        f"- Timed failed-attempt time: {checks['failed_duration']['total_seconds']:.3f} seconds.",
        f"- Packages with a failed first frontend-premerge attempt: {len(checks['packages_with_failed_first_premerge'])}/{inventory['packages']}.",
        "",
        "| Check | Runs | Failures | Total s | Median s | P95 s |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for check_id, values in checks["by_check"].items():
        lines.append(
            f"| {check_id} | {values['invocations']} | {values['failures']} | {values['total_seconds']:.3f} | "
            f"{values['median_seconds']:.3f} | {values['p95_seconds']:.3f} |"
        )
    lines.extend(
        [
            "",
            "Hypothetical one-successful-run-per-wave/check cache:",
            "",
            f"- Invocations retained/avoided: {cache['retained_invocations']}/{cache['avoidable_invocations']} "
            f"({cache['avoidable_invocation_fraction']:.1%} avoided).",
            f"- Measured time avoidable lower bound: {cache['measured_seconds_avoidable_lower_bound']:.3f} seconds; "
            "untimed records make the true value larger.",
            "- This is a counterfactual estimate, not an executed optimization.",
        ]
    )
    lines.extend(["", "## Curated abnormal episodes", "", "| Category | Episodes | Affected units | Packages | Deliverables |", "|---|---:|---:|---:|---:|"])
    for category, values in events["by_category"].items():
        lines.append(
            f"| {category} | {values['episodes']} | {values['affected_units']} | {values['packages']} | {values['deliverables']} |"
        )
    lines.extend(["", "Detection layers: " + ", ".join(f"{key}={value}" for key, value in events["by_detection_layer"].items()) + ".", ""])
    if summary["wave_windows"]:
        lines.extend(
            [
                "## Git-bounded wall-clock envelopes",
                "",
                "These are activation-commit to merge-commit envelopes, not CPU time or summed agent time.",
                "",
                "| Wave | Members | Preparation h | Merge lag min | Envelope h | Members/h | Source lines/min preparation |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in summary["wave_windows"]:
            lines.append(
                f"| {row['wave']} | {row['members']} | {row['preparation_seconds']/3600:.3f} | "
                f"{row['merge_lag_seconds']/60:.3f} | {row['activation_to_merge_seconds']/3600:.3f} | "
                f"{row['members_per_hour']:.3f} | {row['source_lines_per_minute_preparation']:.3f} |"
            )
    lines.extend(
        [
            "",
            "## Statistical bounds",
            "",
            f"- Eventual-pass rate: {intervals['eventual_pass']['rate']:.1%}; 95% Wilson interval "
            f"{intervals['eventual_pass']['low']:.1%}–{intervals['eventual_pass']['high']:.1%}.",
            f"- Observed substantive-failure rate: {intervals['substantive_failure']['rate']:.1%}; 95% Wilson interval "
            f"{intervals['substantive_failure']['low']:.1%}–{intervals['substantive_failure']['high']:.1%}.",
            f"- Project-check invocation failure rate: {intervals['project_check_failure']['rate']:.1%}; 95% Wilson interval "
            f"{intervals['project_check_failure']['low']:.1%}–{intervals['project_check_failure']['high']:.1%}.",
            "",
            "## Measurement limits",
            "",
            "- No native model-token, context-occupancy, CPU, or per-agent start/stop telemetry is present.",
            "- Event classification is curated and evidence-bound because historical prose/status schemas are heterogeneous.",
            "- Event episodes are not equal-cost or statistically independent; counts must not be read as a defect probability without their denominator.",
            "- Git envelopes include orchestration, evidence work, integration, CI, and queue latency.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(output_dir: Path, summary: dict[str, Any], events: list[EvidenceEvent]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "summary.json"
    events_path = output_dir / "events.csv"
    report_path = output_dir / "report.md"
    manifest_path = output_dir / "MANIFEST.tsv"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with events_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = EVENT_COLUMNS + ["evidence_sha256", "evidence_line"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for event in events:
            writer.writerow({**event.row, "evidence_sha256": event.evidence_sha256, "evidence_line": event.evidence_line})
    report_path.write_text(render_report(summary), encoding="utf-8")
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("path\tsha256\tbytes\n")
        for path in (events_path, report_path, summary_path):
            handle.write(f"{path.name}\t{sha256_path(path)}\t{path.stat().st_size}\n")


def analyze(
    repo_root: Path,
    run_root: Path,
    event_catalog: Path,
    output_dir: Path,
    *,
    include_git_runtime: bool = True,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    run_root = require_within(run_root, repo_root, "run_root")
    event_catalog = require_within(event_catalog, repo_root, "event_catalog")
    output_dir = require_within(output_dir, repo_root, "output_dir")
    if not run_root.is_dir():
        raise AnalysisError(f"run root is not a directory: {run_root}")
    instances_root = run_root / "instances"
    if not instances_root.is_dir():
        raise AnalysisError(f"instances directory missing: {instances_root}")
    packages = collect_packages(instances_root)
    children = collect_children(instances_root)
    checks = collect_project_checks(instances_root)
    reconciliation = collect_reconciliations(instances_root)
    events = load_events(repo_root, event_catalog)
    members = sum(package["members"] for package in packages)
    baseline_child_roles = 2 * members
    inventory = {
        "run_root": run_root.relative_to(repo_root).as_posix(),
        "packages": len(packages),
        "waves": len({package["wave"] for package in packages}),
        "members": members,
        "baseline_child_roles": baseline_child_roles,
        "mappings": sum(package["mappings"] for package in packages),
        "source_lines": sum(package["source_lines"] for package in packages),
        "replacement_rows": sum(package["replacement_rows"] for package in packages),
        "rollback_rows": sum(package["rollback_rows"] for package in packages),
        "package_passes": sum(package["status"] == "PASS" and package["terminal"] for package in packages),
        "project_writes": sum(package["project_writes"] for package in packages),
    }
    children_summary = {key: value for key, value in children.items() if key != "rows"}
    children_summary["baseline_child_roles"] = baseline_child_roles
    children_summary["extra_documented_attempts"] = children_summary["documented_attempts"] - baseline_child_roles
    event_summary = event_statistics(events, len(packages), members, baseline_child_roles)
    wave_windows = collect_wave_windows(repo_root, instances_root, packages, include_git_runtime)
    summary = {
        "schema": "chirality-agentic-runtime-analysis/v1",
        "claim_posture": "DESCRIPTIVE_DERIVATIVE_NOT_CAUSAL",
        "inventory": inventory,
        "packages": [{key: value for key, value in package.items() if key != "status_path"} for package in packages],
        "children": children_summary,
        "project_checks": {key: value for key, value in checks.items() if key != "records"},
        "reconciliation": reconciliation,
        "events": event_summary,
        "wave_windows": wave_windows,
        "intervals": {
            "eventual_pass": wilson_interval(members, members),
            "substantive_failure": wilson_interval(event_summary["substantive_episodes"], members),
            "project_check_failure": wilson_interval(checks["failures"], checks["invocations"]),
            "extra_attempt_overhead": wilson_interval(max(0, children_summary["extra_documented_attempts"]), baseline_child_roles),
            "manager_closeout_status": wilson_interval(children_summary["manager_evidence_closeouts"], baseline_child_roles),
            "package_first_premerge_failure": wilson_interval(
                len(checks["packages_with_failed_first_premerge"]), len(packages)
            ),
        },
        "limits": {
            "native_token_telemetry": False,
            "native_context_occupancy": False,
            "per_agent_complete_timing": False,
            "git_windows_are_wall_clock_envelopes": True,
            "event_catalog_is_curated_and_exact_evidence_bound": True,
        },
    }
    write_outputs(output_dir, summary, events)
    return summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--event-catalog", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--skip-git-runtime", action="store_true", help="Omit CHANGE/Git wall-clock envelopes")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = analyze(
            args.repo_root,
            args.run_root,
            args.event_catalog,
            args.output_dir,
            include_git_runtime=not args.skip_git_runtime,
        )
    except AnalysisError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        "PASS: "
        f"{summary['inventory']['members']} members, "
        f"{summary['project_checks']['invocations']} project-check invocations, "
        f"{summary['events']['episodes']} evidence-bound abnormal episodes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
