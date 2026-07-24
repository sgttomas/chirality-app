#!/usr/bin/env python3
"""Domain-engine control-area adapter (read-only).

Reads `_DomainEngines/` surfaces — index, published rulings, latest pointer,
the profile YAML (parsed + raw header comments), the decision register and
D-T0-* records, and validation reports — and emits SourcedFacts for every
status-restating surface. Contradiction detection itself lives in
cmd_self_check; this module only observes.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in missing dependency environments.
    yaml = None  # type: ignore[assignment]

from harness_common import HarnessOperationalError, SourcedFact

DE_DIRNAME = "_DomainEngines"


@dataclass
class DomainEngineProfileObservation:
    profile_id: str
    profile_data: dict = field(default_factory=dict)
    profile_raw: str = ""
    profile_path: Path | None = None
    protected_write_paths: list[str] = field(default_factory=list)
    agent_writable_paths: list[str] = field(default_factory=list)


@dataclass
class DomainEnginesObservation:
    root: Path
    facts: list[SourcedFact] = field(default_factory=list)
    profile_data: dict = field(default_factory=dict)
    profile_raw: str = ""
    profile_path: Path | None = None
    profile_observations: dict[str, DomainEngineProfileObservation] = field(default_factory=dict)
    register_counts: dict[str, int] = field(default_factory=dict)
    decision_records: list[Path] = field(default_factory=list)
    protected_write_paths: list[str] = field(default_factory=list)
    agent_writable_paths: list[str] = field(default_factory=list)


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _grep_line(path: Path, pattern: str) -> tuple[str, int] | None:
    rx = re.compile(pattern)
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if rx.search(line):
            return line.strip(), idx
    return None


def observe_domain_engines(repo_root: Path, de_root: Path | None = None) -> DomainEnginesObservation:
    root = de_root if de_root is not None else repo_root / DE_DIRNAME
    obs = DomainEnginesObservation(root=root)
    if not root.is_dir():
        obs.facts.append(SourcedFact(
            fact_id="domain_engines.root", value="artifact absent",
            source_path=_rel(root, repo_root), authority_status="observed",
            parse_status="NOT_APPLICABLE"))
        return obs

    # Index banner / title.
    index = root / "DOMAIN_ENGINE_INDEX.md"
    if index.is_file():
        hit = _grep_line(index, r"^#\s")
        if hit:
            obs.facts.append(SourcedFact(
                fact_id="index.title", value=hit[0], source_path=_rel(index, repo_root),
                source_hint=f"line {hit[1]}", authority_status="self-declared",
                parse_status="PARSED"))

    # Published rulings surface.
    rulings = root / "RULINGS_PUBLISHED.md"
    if rulings.is_file():
        hit = _grep_line(rulings, r"^#\s")
        if hit:
            obs.facts.append(SourcedFact(
                fact_id="rulings_published.title", value=hit[0],
                source_path=_rel(rulings, repo_root), source_hint=f"line {hit[1]}",
                authority_status="self-declared", parse_status="PARSED"))

    # Latest pointer fields.
    latest = root / "_LATEST.md"
    if latest.is_file():
        for field_name in ("ProfileStatus", "Integration level", "Closure verdict"):
            for idx, line in enumerate(latest.read_text(encoding="utf-8").splitlines(), start=1):
                stripped = line.strip()
                if stripped.startswith("|"):
                    cells = [c.strip() for c in stripped.strip("|").split("|")]
                    if len(cells) >= 2 and cells[0] == field_name:
                        obs.facts.append(SourcedFact(
                            fact_id=f"latest.{field_name.lower().replace(' ', '_')}",
                            value=cells[1], source_path=_rel(latest, repo_root),
                            source_hint=f"line {idx}", authority_status="self-declared",
                            parse_status="PARSED",
                            caveat="Pointer restatement; per-decision records govern."))
                        break

    # Profile YAML: parsed fields + raw text (header comments).
    profiles_dir = root / "profiles"
    if profiles_dir.is_dir():
        for profile_path in sorted(profiles_dir.glob("*.yaml")):
            profile_raw = profile_path.read_text(encoding="utf-8")
            if yaml is None:
                raise HarnessOperationalError(
                    "PyYAML is required to read domain-engine profiles but is not "
                    "importable in this interpreter (operational error, exit 2).")
            try:
                data = yaml.safe_load(profile_raw) or {}
            except Exception as exc:  # noqa: BLE001
                raise HarnessOperationalError(
                    f"Unparseable profile YAML {profile_path}: {exc}") from exc
            profile_data = data if isinstance(data, dict) else {}
            dp = profile_data.get("domain_profile", {}) if isinstance(
                profile_data.get("domain_profile", {}), dict) else {}
            profile_id = str(dp.get("id") or profile_path.stem)
            rel = _rel(profile_path, repo_root)
            profile_obs = DomainEngineProfileObservation(
                profile_id=profile_id,
                profile_data=profile_data,
                profile_raw=profile_raw,
                profile_path=profile_path,
                protected_write_paths=[
                    str(p) for p in (dp.get("protected_write_paths") or [])],
                agent_writable_paths=[
                    str(p) for p in (dp.get("agent_writable_paths") or [])],
            )
            obs.profile_observations[profile_id] = profile_obs
            # Backward-compatible primary profile fields keep the original
            # OpenPipeStress observation stable while profile-keyed fields
            # carry any additional domain engines.
            if profile_id == "open_pipe_stress" or obs.profile_path is None:
                obs.profile_path = profile_path
                obs.profile_raw = profile_raw
                obs.profile_data = profile_data
                obs.protected_write_paths = list(profile_obs.protected_write_paths)
                obs.agent_writable_paths = list(profile_obs.agent_writable_paths)
            for key in ("profile_status", "profile_version", "integration_level", "id"):
                if key in dp:
                    obs.facts.append(SourcedFact(
                        fact_id=f"profile.{profile_id}.{key}", value=str(dp[key]), source_path=rel,
                        authority_status="governed_committed", parse_status="PARSED"))
                    if profile_id == "open_pipe_stress" or len(obs.profile_observations) == 1:
                        obs.facts.append(SourcedFact(
                            fact_id=f"profile.{key}", value=str(dp[key]), source_path=rel,
                            authority_status="governed_committed", parse_status="PARSED"))

        # Validation reports.
        for report_path in sorted((profiles_dir / "_validation").glob("*.json")):
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                obs.facts.append(SourcedFact(
                    fact_id="profile.validation_report", value="unparseable JSON",
                    source_path=_rel(report_path, repo_root),
                    authority_status="generated_evidence", parse_status="UNPARSEABLE"))
                continue
            profile_id = str(report.get("profile_id") or report_path.stem.removesuffix(".validation"))
            obs.facts.append(SourcedFact(
                fact_id=f"profile.{profile_id}.validation_report",
                value=(f"result={report.get('result')}, "
                       f"profile_status={report.get('profile_status')}, "
                       f"errors={report.get('summary', {}).get('error_count')}"),
                source_path=_rel(report_path, repo_root),
                authority_status="generated_evidence", parse_status="PARSED",
                caveat=("Evidence artifact quoted; validator output is a structural "
                        "check, not acceptance of residual risk (K-GATE-1).")))
            if profile_id == "open_pipe_stress":
                obs.facts.append(SourcedFact(
                    fact_id="profile.validation_report",
                    value=(f"result={report.get('result')}, "
                           f"profile_status={report.get('profile_status')}, "
                           f"errors={report.get('summary', {}).get('error_count')}"),
                    source_path=_rel(report_path, repo_root),
                    authority_status="generated_evidence", parse_status="PARSED",
                    caveat=("Evidence artifact quoted; validator output is a structural "
                            "check, not acceptance of residual risk (K-GATE-1).")))

    # Decision register + records.
    register = root / "_DECISIONS" / "_REGISTER.md"
    if register.is_file():
        hit = _grep_line(register, r"^#\s")
        if hit:
            obs.facts.append(SourcedFact(
                fact_id="decisions.register_title", value=hit[0],
                source_path=_rel(register, repo_root), source_hint=f"line {hit[1]}",
                authority_status="self-declared", parse_status="PARSED"))
        # Table rows only (^|...): the register title also carries a bolded
        # RULED annotation and must not inflate the row count.
        ruled = len(re.findall(r"^\|.*\*\*RULED",
                               register.read_text(encoding="utf-8"), re.MULTILINE))
        obs.register_counts["RULED"] = ruled
        obs.facts.append(SourcedFact(
            fact_id="decisions.ruled_row_count", value=str(ruled),
            source_path=_rel(register, repo_root),
            authority_status="governed_committed", parse_status="PARSED_WITH_ASSUMPTIONS",
            caveat="Counted bolded RULED markers in register rows."))
    obs.decision_records = sorted((root / "_DECISIONS").glob("D-T0-*.md")) if (
        root / "_DECISIONS").is_dir() else []
    return obs
