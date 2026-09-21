#!/usr/bin/env python3
"""`drift` — status-truth drift audit per project adapter.

Compares each `_STATUS.md` `**Current State:**` field with the last
state-bearing history assertion (prose-bullet-v1 dialect). A mismatch is a
REVIEW finding — which surface is right is a human call (K-CONFLICT-1
surfaces it; the harness never resolves it). Unparseable histories are never
guessed and never counted as mismatches.

Baseline comparison is a trend statement only: the manifest-recorded
`drift_baseline_mismatch` / `drift_baseline_files` are quoted next to the
measured values; drift of the measurement itself is INFO, not a violation.
"""

from __future__ import annotations

from pathlib import Path

import adapter_project
import cmd_self_check
from adapter_loader import load_adapter
from harness_common import (
    Report,
    Severity,
    SourcedFact,
    make_finding,
)

import prose_bullet_v1


def observe_for_drift(repo_root: Path, project_root: Path) -> adapter_project.ProjectObservation:
    manifest = load_adapter(project_root)
    return adapter_project.observe_project(manifest, repo_root)


def run_drift(
    repo_root: Path,
    project_roots: list[Path],
    include_domain_engines: bool = False,
) -> Report:
    report = Report(command="drift")
    report.md("# Drift — Current State vs last history assertion")
    report.md("")
    total_files = 0
    total_mismatches = 0
    per_project_rows: list[str] = []

    for project_root in project_roots:
        obs = observe_for_drift(repo_root, project_root)
        manifest = obs.manifest
        files = obs.files
        total_files += len(files)

        mism_parsed = 0
        mism_assumed = 0
        matches = 0
        unparseable_docs = 0
        no_assertion = 0
        for f in files:
            if f.unparseable_doc:
                unparseable_docs += 1
                report.add_finding(make_finding(
                    Severity.WARN, "UNPARSEABLE_HISTORY", "staleness/drift",
                    "Status document is UNPARSEABLE at doc level ("
                    + "; ".join(f.doc.doc_caveats) + "); not guessed, not counted "
                    "as a mismatch — human review required.",
                    f.rel_path, None, invariant="K-STATUS-1"))
                continue
            if f.assertion is None:
                no_assertion += 1
                if f.empty_history:
                    report.add_finding(make_finding(
                        Severity.WARN, "EMPTY_HISTORY", "staleness/drift",
                        "No history bullets present; zero state-bearing assertions — "
                        "not counted as a mismatch.",
                        f.rel_path, None, invariant="K-STATUS-1"))
                else:
                    report.add_finding(make_finding(
                        Severity.WARN, "UNPARSEABLE_HISTORY", "staleness/drift",
                        f"History has {len(f.doc.history)} bullet(s) but zero "
                        "state-bearing assertions within the manifest lifecycle "
                        "states; not guessed, not counted as a mismatch.",
                        f.rel_path, None, invariant="K-STATUS-1"))
                continue
            if f.mismatch:
                total_mismatches += 1
                if f.assertion.caveat_class == prose_bullet_v1.PARSED:
                    mism_parsed += 1
                else:
                    mism_assumed += 1
                trailing = (
                    f" ({f.trailing_unparseable} trailing unparseable bullet(s) "
                    "after the assertion)" if f.trailing_unparseable else "")
                report.add_finding(make_finding(
                    Severity.REVIEW, "STATUS_HISTORY_MISMATCH", "staleness/drift",
                    f"Current State is {f.current_state!r} (line "
                    f"{f.current_state_line}) but the last state-bearing history "
                    f"assertion is {f.assertion.state!r} (rule "
                    f"{f.assertion.rule!r}, caveat class "
                    f"{f.assertion.caveat_class}){trailing}. Sources conflict; "
                    "which surface is right is a human call (K-CONFLICT-1).",
                    f.rel_path, f.current_state_line, invariant="K-CONFLICT-1"))
            else:
                matches += 1

        # Approval-SHA reachability (only where the manifest declares the field).
        for sha, reachable in sorted(obs.sha_reachability.items()):
            example = next((f.rel_path for f in files if f.approval_sha == sha), "")
            if reachable is True:
                report.add_finding(make_finding(
                    Severity.INFO, "APPROVAL_SHA_REACHABLE", "provenance",
                    f"Declared approval SHA {sha} is reachable in this repository "
                    f"(git cat-file -e {sha}^{{commit}}); example surface cited.",
                    example, None, invariant="K-PROV-1"))
            elif reachable is False:
                report.add_finding(make_finding(
                    Severity.REVIEW, "APPROVAL_SHA_UNREACHABLE", "provenance",
                    f"Declared approval SHA {sha} is unreachable in this repository; "
                    "human review required.",
                    example, None, invariant="K-PROV-1"))
            else:
                report.add_finding(make_finding(
                    Severity.NOT_APPLICABLE, "APPROVAL_SHA_UNVERIFIABLE", "provenance",
                    f"Declared approval SHA {sha}: git state unavailable here; "
                    "reachability not verifiable in this context.",
                    example, None, invariant="K-PROV-1"))

        measured_mism = mism_parsed + mism_assumed
        # Cite the manifest the loader actually read: project adapters live at
        # `<root>/_harness/adapter.yaml`, the root adapter at
        # `execution/_harness/adapter.yaml`.
        report.add_finding(make_finding(
            Severity.INFO, "DRIFT_BASELINE_COMPARISON", "staleness/drift",
            f"{manifest.project}: measured {measured_mism} mismatch(es) over "
            f"{len(files)} file(s) vs recorded baseline "
            f"{manifest.drift_baseline_mismatch}/{manifest.drift_baseline_files} "
            "(trend statement only).",
            manifest.manifest_relpath(repo_root),
            None, invariant="K-STATUS-1"))
        report.add_fact(SourcedFact(
            fact_id=f"drift.{manifest.project}",
            value=(f"files={len(files)}, matches={matches}, "
                   f"mismatches={measured_mism} (strict-parsed={mism_parsed}, "
                   f"assumption-parsed={mism_assumed}), "
                   f"unparseable_docs={unparseable_docs}, "
                   f"no_state_assertion={no_assertion}"),
            source_path=str(project_root.relative_to(repo_root)),
            authority_status="observed", parse_status="PARSED"))
        per_project_rows.append(
            f"| {manifest.project} | {len(files)} | {matches} | {measured_mism} "
            f"| {mism_parsed} | {mism_assumed} | {unparseable_docs} "
            f"| {manifest.drift_baseline_mismatch}/{manifest.drift_baseline_files} |")

    report.md("| Project | Files | Matches | Mismatches | via strict rule | via assumption rules | Unparseable docs | Recorded baseline |")
    report.md("|---|---|---|---|---|---|---|---|")
    for row in per_project_rows:
        report.md(row)
    report.md("")
    report.md(f"Denominator: {total_files} status file(s) audited; "
              f"{total_mismatches} mismatch(es) measured.")

    if include_domain_engines:
        de_report, refusal = cmd_self_check.run_self_check(
            repo_root, root_filter=repo_root / "_DomainEngines")
        for finding in de_report.findings:
            report.add_finding(finding)
        for fact in de_report.facts:
            report.add_fact(fact)
        if refusal:
            report.summary["identity_refusal"] = refusal

    report.summary["files_total"] = total_files
    report.summary["mismatches_total"] = total_mismatches
    return report
