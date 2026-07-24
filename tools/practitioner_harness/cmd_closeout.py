#!/usr/bin/env python3
"""`closeout-digest` — compose scope-check + evidence-check into one digest
for the human CHANGE closeout. Generated digest only: NEVER a lifecycle
transition, never a lifecycle judgment (K-GATE-1), never acceptance of
residual risk (K-AUTH-1).

Composition is IN-PROCESS: the scope-check and evidence-check run functions
are imported and called (never shelled out); the digest carries their path
classifications, captured-evidence facts, summaries, skipped checks
(NOT_APPLICABLE), caveats, the brief's open human decision points, the fixed
blind-spot statement, and the fixed closing statement. Findings are the
union of the sub-checks' findings, deduplicated by (code, source, line) —
this command adds no checks of its own.

NEVER A GATE: the digest's charter is a composition for the human CHANGE
closeout; the sub-checks are the gates. Any sub-check BLOCK is carried here
DOWNGRADED to REVIEW with a caveat naming the gating command — run that
command (e.g. scope-check) for the gating exit code. That keeps the D-GOV-02
exit contract intact: exit 1 iff a BLOCK finding is in THIS report, and the
digest composes none at BLOCK, while the information stays visible.

`--write-digest` additionally writes the digest markdown to
`_harness_generated/closeout/<tranche_id>.md` through `write_generated_file`
(contained to the generated root; D-GOV-01 / K-WRITE-2). Without the flag,
nothing is written. Identity refusals (D-GOV-04) run no sub-check and write
nothing (exit 2).
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import brief_adoption
import cmd_evidence_check
import cmd_scope_check
from cmd_scope_check import BLIND_SPOT_STATEMENT
from harness_common import (
    Report,
    Severity,
    write_generated_file,
)

COMPOSED_NOTE = (
    "closeout-digest composes the scope-check and evidence-check run "
    "functions in-process and unions their findings (deduplicated by "
    "code/source/line); it adds no checks of its own. The digest is a "
    "composition for the human CHANGE closeout, never a gate: any sub-check "
    "BLOCK is carried here downgraded to REVIEW with a caveat naming the "
    "gating command — the gating exit code lives with that sub-check "
    "(D-GOV-02: exit 1 iff a BLOCK finding is in THIS report, and the "
    "digest composes none at BLOCK). The digest file is written only with "
    "--write-digest, and only under the generated root.")

DOWNGRADED_BLOCK_CAVEAT = (
    "Reported at BLOCK by {check} — this digest is a composition and never "
    "a gate; run {check} for the gating exit code (D-GOV-02).")

CLOSING_STATEMENT = (
    "This digest is an INPUT to the human CHANGE closeout: it is never a "
    "lifecycle transition, never a lifecycle judgment, never acceptance of "
    "residual risk, and never a gate — a sub-check BLOCK appears here "
    "downgraded to REVIEW with the gating command named; the human decides; "
    "the digest only collects (K-GATE-1; K-AUTH-1; D-GOV-02).")

REFUSAL_NOTE = (
    "Identity refusal (D-GOV-04): no sub-check ran and no digest was "
    "written.")

TEMPLATES: list[str] = [
    COMPOSED_NOTE, DOWNGRADED_BLOCK_CAVEAT, CLOSING_STATEMENT, REFUSAL_NOTE,
    BLIND_SPOT_STATEMENT,
]


def _severity_counts_line(report: Report) -> str:
    counts = report.severity_counts()
    if not counts:
        return "none"
    return ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))


def run_closeout_digest(
    repo_root: Path,
    brief_path: Path,
    diff_range: str,
    out_dir: Path,
    alias_by_root: dict[Path, str],
    write_digest: bool = False,
) -> Report:
    """See the module docstring for the contract. `alias_by_root` is built by
    the caller from harness.py PROJECT_ALIASES (passed through to
    evidence-check; the run-validations idiom, no circular import)."""
    repo_root = repo_root.resolve()
    fence, _adoption_findings, refusal = brief_adoption.verify_adoption(
        brief_path, repo_root)
    report = Report(command="closeout-digest")
    report.md(f"# closeout-digest — {fence.tranche_id}")
    report.md("")
    report.md(COMPOSED_NOTE)
    report.md("")
    report.md(f"- brief: `{fence.source_path}`")
    report.md(f"- brief state: {fence.state}")
    report.md(f"- fence_active: {fence.fence_active}")
    if fence.cap_reason:
        report.md(f"  - cap_reason: {fence.cap_reason}")
    if fence.bound_sha:
        report.md(f"- bound SHA (K-AUTH-2): `{fence.bound_sha}`")
    report.md(f"- diff range: `{diff_range}`")
    report.summary["tranche_id"] = fence.tranche_id
    report.summary["brief_state"] = fence.state
    report.summary["fence_active"] = fence.fence_active
    report.summary["diff_range"] = diff_range

    if refusal is not None:
        report.md("")
        report.md(REFUSAL_NOTE)
        report.md("")
        report.md(BLIND_SPOT_STATEMENT)
        report.md("")
        report.md(CLOSING_STATEMENT)
        report.summary["identity_refusal"] = refusal
        report.summary["blind_spots"] = BLIND_SPOT_STATEMENT
        report.summary["closing_note"] = CLOSING_STATEMENT
        return report

    scope_report = cmd_scope_check.run_scope_check(
        repo_root, brief_path, diff_range)
    evidence_report = cmd_evidence_check.run_evidence_check(
        repo_root, brief_path, out_dir, alias_by_root)

    seen_findings: set[tuple] = set()
    for check_name, sub_report in (("scope-check", scope_report),
                                   ("evidence-check", evidence_report)):
        for finding in sub_report.findings:
            key = (finding.code, finding.source_path, finding.source_line)
            if key in seen_findings:
                continue
            seen_findings.add(key)
            if finding.severity is Severity.BLOCK:
                # The digest is a composition, never a gate — the sub-check
                # is the gate. Carrying a sub-check BLOCK verbatim would make
                # the digest exit 1 through composition; downgrading to
                # REVIEW with the gating command named keeps D-GOV-02 intact
                # (exit 1 iff a BLOCK finding is in THIS report) while the
                # information stays visible.
                caveat = DOWNGRADED_BLOCK_CAVEAT.format(check=check_name)
                finding = dataclasses.replace(
                    finding, severity=Severity.REVIEW,
                    caveat=(finding.caveat + " " if finding.caveat else "")
                    + caveat)
            report.add_finding(finding)
    seen_facts: set[tuple] = set()
    for fact in scope_report.facts + evidence_report.facts:
        key = (fact.fact_id, fact.value, fact.source_path)
        if key in seen_facts:
            continue
        seen_facts.add(key)
        report.add_fact(fact)

    # --- changed files by fence classification (from scope-check) ---------
    scope_extras = scope_report.extras.get("scope_check", {})
    changed_rows = scope_extras.get("changed", [])
    untracked_rows = scope_extras.get("untracked", [])
    report.md("")
    report.md(f"## Changed files by fence classification ({len(changed_rows)})")
    report.md("")
    if changed_rows:
        report.md("| path | git status | fence judgment | matched fence entry |")
        report.md("|---|---|---|---|")
        for row in changed_rows:
            pattern = f"`{row['matched_pattern']}`" if row["matched_pattern"] else "-"
            report.md(f"| `{row['path']}` | {row['git_status']} "
                      f"| {row['judgment']} | {pattern} |")
    else:
        report.md("- none — the diff range contains no changed paths")
    report.md("")
    report.md(f"## Observed untracked non-ignored files ({len(untracked_rows)})")
    report.md("")
    if untracked_rows:
        report.md("| path | fence judgment | matched fence entry |")
        report.md("|---|---|---|")
        for row in untracked_rows:
            pattern = f"`{row['matched_pattern']}`" if row["matched_pattern"] else "-"
            report.md(f"| `{row['path']}` | {row['judgment']} | {pattern} |")
    else:
        report.md("- none observed")

    # --- evidence records captured (from evidence-check) ------------------
    evidence_extras = evidence_report.extras.get("evidence_check", {})
    per_command = evidence_extras.get("per_command", [])
    report.md("")
    report.md(f"## Evidence records captured ({len(per_command)} declared "
              "validation(s))")
    report.md("")
    if per_command:
        report.md("| command | records | exits (facts) | newest captured_at |")
        report.md("|---|---|---|---|")
        for entry in per_command:
            recs = entry["records"]
            exits = ", ".join(r["exit"] for r in recs) if recs else "-"
            newest = max((r["captured_at"] for r in recs), default="-")
            report.md(f"| `{entry['command']}` | {len(recs)} | {exits} "
                      f"| {newest} |")
    else:
        report.md("- no validation commands declared (see the NOT_APPLICABLE "
                  "finding)")

    # --- the two check summaries ------------------------------------------
    report.md("")
    report.md("## Sub-check summaries")
    report.md("")
    report.md(f"- scope-check severities: {_severity_counts_line(scope_report)} "
              f"(changed paths judged: {len(changed_rows)}; untracked "
              f"observed: {len(untracked_rows)})")
    report.md(f"- evidence-check severities: "
              f"{_severity_counts_line(evidence_report)} "
              f"({evidence_report.summary.get('coverage', 'coverage n/a')})")

    # --- skipped checks (NOT_APPLICABLE) -----------------------------------
    skipped = [f for f in report.findings
               if f.severity is Severity.NOT_APPLICABLE]
    report.md("")
    report.md(f"## Skipped checks — NOT_APPLICABLE ({len(skipped)})")
    report.md("")
    if skipped:
        for finding in skipped:
            report.md(f"- {finding.code}: {finding.message}")
    else:
        report.md("- none")

    # --- caveats ------------------------------------------------------------
    caveats: list[str] = []
    for finding in report.findings:
        if finding.caveat and finding.caveat not in caveats:
            caveats.append(finding.caveat)
    if fence.cap_reason and fence.cap_reason not in caveats:
        caveats.append(fence.cap_reason)
    report.md("")
    report.md(f"## Caveats ({len(caveats)})")
    report.md("")
    if caveats:
        for caveat in caveats:
            report.md(f"- {caveat}")
    else:
        report.md("- none recorded")

    # --- open human decision points (copied from the brief) -----------------
    report.md("")
    report.md("## Open human decision points (copied from the brief)")
    report.md("")
    if fence.human_decision_points:
        for point in fence.human_decision_points:
            report.md(f"- {point}")
    else:
        report.md("- none declared")

    report.md("")
    report.md(BLIND_SPOT_STATEMENT)
    report.md("")
    report.md(CLOSING_STATEMENT)

    report.extras["closeout_digest"] = {
        "changed": changed_rows,
        "untracked": untracked_rows,
        "per_command": per_command,
        "skipped_not_applicable": [f.code for f in skipped],
        "caveats": caveats,
        "human_decision_points": list(fence.human_decision_points),
    }
    report.summary["coverage"] = evidence_report.summary.get("coverage", "")
    report.summary["changed_paths"] = len(changed_rows)
    report.summary["untracked_observed"] = len(untracked_rows)
    report.summary["skipped_not_applicable"] = len(skipped)
    report.summary["blind_spots"] = BLIND_SPOT_STATEMENT
    report.summary["closing_note"] = CLOSING_STATEMENT

    if write_digest:
        digest_path = write_generated_file(
            Path(out_dir) / "closeout" / f"{fence.tranche_id}.md",
            report.render_markdown(), repo_root)
        # Recorded on stdout/JSON only, after the file content is fixed.
        report.summary["digest_written"] = str(
            digest_path.relative_to(repo_root))
    return report
