#!/usr/bin/env python3
"""`status` — one-page sourced posture view of a project or the domain-engine
control area. Every fact carries its source; the cited files govern.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import adapter_domain_engines
import adapter_project
import cmd_self_check
from adapter_loader import load_adapter
from harness_common import (
    Report,
    SourcedFact,
    ratification_labels_map,
)

ROOT_GOVERNANCE_DOCS = ("DIRECTIVE.md", "CONTRACT.md", "SPEC.md", "TYPES.md")


def _root_governance_lines(repo_root: Path, report: Report) -> None:
    report.md("## Root governance status (self-declared)")
    report.md("")
    for name in ROOT_GOVERNANCE_DOCS:
        path = repo_root / "docs" / name
        if not path.is_file():
            report.md(f"- `docs/{name}`: artifact absent")
            continue
        quoted = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            if "**Status:" in line or line.strip().startswith("Status:"):
                quoted = line.strip()
                break
        if len(quoted) > 160:
            quoted = quoted[:160] + " …[truncated]"
        report.md(f"- `docs/{name}`: {quoted or 'no self-declared Status line found'}")
    report.md("")
    report.md("Per-invariant ratification (docs/CONTRACT.md, owner ratification "
              "2026-07-11; partial basis D-GOV-05): "
              + "; ".join(f"{k}={v}" for k, v in sorted(ratification_labels_map().items())))
    report.md("")


def run_status_project(repo_root: Path, project_root: Path) -> Report:
    manifest = load_adapter(project_root)
    obs = adapter_project.observe_project(manifest, repo_root)
    report = Report(command="status")
    report.md(f"# Status — {manifest.project}")
    report.md("")

    # Plan posture.
    report.md("## Plan posture")
    report.md("")
    for fact in obs.facts:
        if fact.fact_id.endswith(".status_line") or fact.fact_id.endswith(".exists"):
            report.md(f"- `{fact.source_path}`"
                      + (f" ({fact.source_hint})" if fact.source_hint else "")
                      + f": {fact.value}")
    report.md("")

    # Status distribution.
    dist = Counter((f.current_state or "«missing»").upper() for f in obs.files)
    report.md("## Deliverable status distribution (Current State fields)")
    report.md("")
    report.md("| State | Count |")
    report.md("|---|---|")
    for state, count in sorted(dist.items()):
        report.md(f"| {state} | {count} |")
    report.md("")
    report.md(f"Source: {len(obs.files)} file(s) matching `{manifest.status_glob}` "
              f"under `{project_root.relative_to(repo_root)}` (parser: "
              f"{manifest.parser_dialect}). Drift audit: run `drift`.")
    report.md("")

    # Decision register counts.
    report.md("## Decision register (counts by state)")
    report.md("")
    if obs.register_counts:
        report.md(", ".join(f"{k}={v}" for k, v in sorted(obs.register_counts.items()))
                  + f" — source: `{manifest.decision_register}`")
    else:
        report.md(f"No rows parsed — source: `{manifest.decision_register}`")
    report.md("")

    # DAG pointer facts.
    report.md("## DAG pointer")
    report.md("")
    for fact in obs.facts:
        if fact.fact_id.startswith("dag."):
            report.md(f"- {fact.fact_id}: {fact.value} — `{fact.source_path}`"
                      + (f" ({fact.source_hint})" if fact.source_hint else ""))
    report.md("")

    # Validation surfaces.
    report.md("## Validation surfaces (declared, not executed by this command)")
    report.md("")
    if manifest.validation_commands:
        for vc in manifest.validation_commands:
            report.md(f"- `{vc.get('command', '?')}` (cwd: `{vc.get('cwd', '.')}`)")
    else:
        report.md("- none declared")
    report.md("")

    # Git state.
    report.md("## Git state")
    report.md("")
    for fact in obs.facts:
        if fact.fact_id.startswith("git."):
            report.md(f"- {fact.fact_id}: {fact.value}")
    report.md("")

    _root_governance_lines(repo_root, report)

    for fact in obs.facts:
        report.add_fact(fact)
    report.summary["project"] = manifest.project
    report.summary["status_files"] = len(obs.files)
    return report


def run_status_domain_engines(repo_root: Path) -> Report:
    report = Report(command="status")
    obs = adapter_domain_engines.observe_domain_engines(repo_root)
    report.md("# Status — _DomainEngines control area")
    report.md("")
    report.md("## Sourced facts")
    report.md("")
    for fact in obs.facts:
        report.md(f"- {fact.fact_id}: {fact.value} — `{fact.source_path}`"
                  + (f" ({fact.source_hint})" if fact.source_hint else ""))
        report.add_fact(fact)
    report.md("")
    report.md("## Write-fence declarations (from the profile)")
    report.md("")
    for p in obs.protected_write_paths:
        report.md(f"- protected: `{p}`")
    for p in obs.agent_writable_paths:
        report.md(f"- proposal-writable: `{p}`")
    report.md("")

    # Contradiction count from the self-check engine (INFO pointer).
    de_report, refusal = cmd_self_check.run_self_check(
        repo_root, root_filter=repo_root / adapter_domain_engines.DE_DIRNAME)
    contradiction_count = sum(
        1 for f in de_report.findings if f.dimension == "staleness")
    report.md("## Consistency")
    report.md("")
    report.md(f"- Contradiction findings currently measured by the self-check "
              f"engine over this area: {contradiction_count} (INFO pointer — run "
              f"`self-check` for the sourced findings)")
    if refusal:
        report.md(f"- Identity refusal encountered: {refusal}")
        report.summary["identity_refusal"] = refusal
    report.md("")

    _root_governance_lines(repo_root, report)
    report.summary["contradiction_count"] = contradiction_count
    return report
