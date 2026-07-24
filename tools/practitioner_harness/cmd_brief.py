#!/usr/bin/env python3
"""`brief` — emit a CANDIDATE tranche brief for one deliverable, or verify a
brief's committed adoption (`--verify-adoption`).

The brief is a generated projection assembled ONLY from cited sources; nothing
is invented (K-INVENT-1: an unstated objective stays "TBD — practitioner to
state"). Its state is CANDIDATE. Brief lifecycle (metadata on harness
artifacts only, never the deliverable lifecycle):

    CANDIDATE → HUMAN_ADOPTED → EXECUTED → CHECKED → HUMAN_REVIEWED
    → CLOSED/SUPERSEDED

Adoption is NOT implemented here — no harness command flips a brief's state.
Adoption = a human edits `state:` to HUMAN_ADOPTED, attributes themselves
(docs/governance_harness/human_actors.md), and commits the brief into the
governed record (D-GOV-04). Until then, findings referencing this brief are
capped at REVIEW and it fences nothing. `run_verify_adoption` detects that
posture (brief_adoption.verify_adoption); it never adopts.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path

import adapter_domain_engines
import adapter_project
import brief_adoption
from adapter_loader import load_adapter
from harness_common import (
    HarnessOperationalError,
    Report,
    SourcedFact,
    write_generated_file,
)

BRIEF_STATE = "CANDIDATE"
BRIEF_LIFECYCLE = (
    "CANDIDATE → HUMAN_ADOPTED → EXECUTED → CHECKED → HUMAN_REVIEWED → CLOSED/SUPERSEDED"
)

FOOTER_TEMPLATE = (
    "CANDIDATE brief — a generated projection, not authority (D-GOV-04). It "
    "becomes an enforceable fence only when human-adopted and committed to the "
    "governed record; the cited sources govern on any disagreement."
)

OBJECTIVE_TBD = "TBD — practitioner to state"

# Adoption placeholders (parse_brief_markdown treats a value that IS the TBD
# token — "TBD" at a word boundary — as absent) and the mechanical adoption
# steps — all HUMAN acts; no harness command performs any of them (D-GOV-04).
ADOPTED_BY_TBD = (
    "TBD — on adoption, replace with an actor matching "
    "docs/governance_harness/human_actors.md (D-GOV-04)")
ADOPTED_ON_TBD = "TBD"
ADOPTION_INTRO = (
    "Adoption is a human act (D-GOV-04); the harness never performs any of "
    "these steps and never flips this brief's state:")
ADOPTION_STEPS = [
    "a human edits `state:` above to HUMAN_ADOPTED",
    "the same human fills `adopted_by:` (must match "
    "`docs/governance_harness/human_actors.md`) and `adopted_on:`",
    "the file is moved to a governed path OUTSIDE `_harness_generated/` — the "
    "generated root is gitignored scratch; an adoption there does not exist "
    "for reliance (D-GOV-04)",
    "the file is committed — adoption binds to committed content at the "
    "publication commit (K-AUTH-2); check with `brief --verify-adoption <path>`",
]

VERIFY_SCOPE_NOTE = (
    "This verification examines adoption metadata and git committed-ness "
    "only: it is not a judgment on the work the brief fences, not a review of "
    "the brief's content, and never a lifecycle transition — the harness "
    "never flips a brief's state (detect, never rewrite; D-GOV-04).")

TEMPLATES: list[str] = [
    FOOTER_TEMPLATE, OBJECTIVE_TBD, BRIEF_LIFECYCLE, ADOPTED_BY_TBD,
    ADOPTED_ON_TBD, ADOPTION_INTRO, VERIFY_SCOPE_NOTE, *ADOPTION_STEPS,
]

DEL_ID_RE = re.compile(r"^DEL-\d{2}-\d{2}$")

INSTRUCTION_SURFACE_PROHIBITED = (
    "tools/**",
    "agents/**",
    "skills/**",
    "docs/**",
)


def run_brief(
    repo_root: Path,
    project_root: Path,
    other_project_roots: list[Path],
    deliverable: str,
    objective: str | None,
    tranche_id: str | None,
    out_dir: Path,
) -> Report:
    if not DEL_ID_RE.match(deliverable):
        raise HarnessOperationalError(
            f"--deliverable must look like DEL-NN-MM (got {deliverable!r}).")
    manifest = load_adapter(project_root)

    # Locate the deliverable directory via the manifest status glob.
    status_files = adapter_project.collect_status_files(manifest)
    target = None
    for path in status_files:
        dirname = path.parent.name
        if dirname == deliverable or dirname.startswith(deliverable + "_"):
            target = path
            break
    if target is None:
        raise HarnessOperationalError(
            f"No deliverable directory matching {deliverable!r} found under "
            f"`{manifest.status_glob}` in {project_root}.")

    result = adapter_project.analyze_status_file(target, manifest, repo_root)
    del_dir_rel = str(target.parent.relative_to(repo_root))
    status_rel = result.rel_path

    date = _dt.date.today().isoformat()
    tid = tranche_id or f"TRB-{manifest.project}-{deliverable}-{date}"
    report = Report(command="brief")

    # --- source_basis -----------------------------------------------------
    source_basis: list[tuple[str, str]] = []
    source_basis.append((
        f"status: Current State {result.current_state!r} (line "
        f"{result.current_state_line})", status_rel))
    plan_path = project_root / manifest.plan
    plan_status = adapter_project._first_status_line(plan_path)
    if plan_status:
        source_basis.append((
            f"plan posture: {plan_status[0]}",
            f"{(project_root / manifest.plan).relative_to(repo_root)}:{plan_status[1]}"))
    else:
        source_basis.append((
            "plan posture: artifact "
            + ("present; no self-declared Status line found" if plan_path.is_file() else "absent"),
            str((project_root / manifest.plan).relative_to(repo_root))))
    if manifest.coordination_pointer:
        cp = project_root / manifest.coordination_pointer
        source_basis.append((
            "coordination pointer: artifact " + ("present" if cp.is_file() else "absent"),
            str(cp.relative_to(repo_root))))
    register_path = project_root / manifest.decision_register
    register_rows: list[tuple[int, str]] = []
    if register_path.is_file():
        for idx, line in enumerate(register_path.read_text(encoding="utf-8").splitlines(), start=1):
            if deliverable in line:
                register_rows.append((idx, line.strip()))
    if register_rows:
        for idx, row in register_rows[:5]:
            snippet = row if len(row) <= 160 else row[:160] + " …[truncated]"
            source_basis.append((
                f"decision register row mentioning {deliverable}: {snippet}",
                f"{register_path.relative_to(repo_root)}:{idx}"))
    else:
        source_basis.append((
            f"decision register: no rows mentioning {deliverable}",
            str(register_path.relative_to(repo_root)) if register_path.is_file()
            else manifest.decision_register))
    dag_facts = adapter_project.dag_pointer_facts(manifest, repo_root)
    for fact in dag_facts[:3]:
        source_basis.append((f"DAG pointer: {fact.fact_id} = {fact.value}",
                             fact.source_path + (f" ({fact.source_hint})" if fact.source_hint else "")))

    # --- scopes -----------------------------------------------------------
    read_scope = [del_dir_rel + "/**"]
    refs = target.parent / "_REFERENCES.md"
    if refs.is_file():
        read_scope.append(str(refs.relative_to(repo_root)) + " (declared references surface)")
    write_scope = [del_dir_rel + "/**"]

    prohibited: list[str] = ["_DomainEngines/**"]
    de_obs = adapter_domain_engines.observe_domain_engines(repo_root)
    for p in de_obs.protected_write_paths:
        if "<" in p:
            continue  # schema placeholder, not a concrete path
        if p not in prohibited:
            prohibited.append(p)
    for other in other_project_roots:
        try:
            rel_other = str(other.relative_to(repo_root))
        except ValueError:
            rel_other = str(other)
        prohibited.append(rel_other + "/**")
    prohibited.extend(INSTRUCTION_SURFACE_PROHIBITED)

    validations = [
        f"{vc.get('command', '?')} (cwd: {vc.get('cwd', '.')}) — declared in the "
        "adapter manifest; NOT run by this command"
        for vc in manifest.validation_commands
    ]
    evidence_targets = [
        f"_harness_generated/briefs/{tid}.md",
        f"_harness_generated/briefs/{tid}.json",
        f"_harness_generated/evidence/{tid}/",
    ]
    stop_conditions = [
        "an out-of-scope write attempt (outside write_scope or into prohibited_paths)",
        "conflicting current-truth discovered — stop and surface it per K-CONFLICT-1; never resolve silently",
        "a human decision point reached (see human_decision_points)",
    ]
    human_decision_points = [
        "adoption of this brief itself (human edits state to HUMAN_ADOPTED and commits; D-GOV-04)",
        "any CHECKING or ISSUED lifecycle advance — human-only (SPEC §3.3)",
    ]

    # --- Markdown ----------------------------------------------------------
    report.md(f"# Tranche brief {tid} — {BRIEF_STATE}")
    report.md("")
    report.md(f"- tranche_id: `{tid}`")
    report.md(f"- state: {BRIEF_STATE}")
    report.md(f"  - lifecycle: {BRIEF_LIFECYCLE}")
    report.md("  - (brief lifecycle is metadata on harness artifacts only — never the deliverable lifecycle)")
    report.md(f"- objective: {objective or OBJECTIVE_TBD}")
    if objective:
        report.md("  - source: practitioner-stated via --objective (recorded verbatim)")
    else:
        report.md("  - source: none — never invented (K-INVENT-1)")
    report.md(f"- adopted_by: {ADOPTED_BY_TBD}")
    report.md(f"- adopted_on: {ADOPTED_ON_TBD}")
    report.md("")
    report.md("## source_basis")
    report.md("")
    for value, src in source_basis:
        report.md(f"- {value}")
        report.md(f"  - source: `{src}`")
    report.md("")
    report.md("## read_scope")
    report.md("")
    for p in read_scope:
        report.md(f"- `{p}`")
    report.md(f"  - source: deliverable directory located via manifest `status_glob` (`{manifest.status_glob}`)")
    report.md("")
    report.md("## write_scope")
    report.md("")
    for p in write_scope:
        report.md(f"- `{p}`")
    report.md("  - source: plan v3 tranche-brief schema — deliverable directory only")
    report.md("")
    report.md("## prohibited_paths")
    report.md("")
    for p in prohibited:
        report.md(f"- `{p}`")
    report.md("  - source: profile `protected_write_paths` "
              f"(`{de_obs.profile_path.relative_to(repo_root) if de_obs.profile_path else '_DomainEngines/profiles/'}`), "
              "the other project root, and the instruction surface (SPEC §0.2.2)")
    report.md("")
    report.md("## validations (declared, not run)")
    report.md("")
    if validations:
        for v in validations:
            report.md(f"- {v}")
    else:
        report.md("- none declared")
    report.md(f"  - source: `{(project_root / '_harness' / 'adapter.yaml').relative_to(repo_root)}`")
    report.md("")
    report.md("## evidence_targets")
    report.md("")
    for p in evidence_targets:
        report.md(f"- `{p}` (under the declared generated root; D-GOV-01)")
    report.md("")
    report.md("## stop_conditions")
    report.md("")
    for s in stop_conditions:
        report.md(f"- {s}")
    report.md("")
    report.md("## human_decision_points")
    report.md("")
    for h in human_decision_points:
        report.md(f"- {h}")
    report.md("")
    report.md("## adoption")
    report.md("")
    report.md(ADOPTION_INTRO)
    report.md("")
    for step in ADOPTION_STEPS:
        report.md(f"- {step}")
    report.md("")
    report.md("---")
    report.md("")
    report.md(FOOTER_TEMPLATE)

    # --- JSON payload + files ------------------------------------------------
    report.extras["brief"] = {
        "tranche_id": tid,
        "state": BRIEF_STATE,
        "lifecycle": BRIEF_LIFECYCLE,
        "objective": objective or OBJECTIVE_TBD,
        "adopted_by": ADOPTED_BY_TBD,
        "adopted_on": ADOPTED_ON_TBD,
        "adoption_steps": ADOPTION_STEPS,
        "source_basis": [{"value": v, "source": s} for v, s in source_basis],
        "read_scope": read_scope,
        "write_scope": write_scope,
        "prohibited_paths": prohibited,
        "validations": validations,
        "evidence_targets": evidence_targets,
        "stop_conditions": stop_conditions,
        "human_decision_points": human_decision_points,
        "footer": FOOTER_TEMPLATE,
        "adoption_note": (
            "Adoption is not implemented by any harness command: a human edits "
            "state to HUMAN_ADOPTED and commits this brief to the governed "
            "record (D-GOV-04)."),
    }
    report.add_fact(SourcedFact(
        fact_id="brief.deliverable_state",
        value=str(result.current_state),
        source_path=status_rel,
        source_hint=f"line {result.current_state_line}",
        authority_status="governed_committed", parse_status="PARSED"))
    report.summary["tranche_id"] = tid
    report.summary["deliverable"] = deliverable
    report.summary["state"] = BRIEF_STATE

    md_path = write_generated_file(
        Path(out_dir) / "briefs" / f"{tid}.md", report.render_markdown(), repo_root)
    json_text = json.dumps(report.to_json_dict(), indent=2) + "\n"
    json_path = write_generated_file(
        Path(out_dir) / "briefs" / f"{tid}.json", json_text, repo_root)
    report.summary["written"] = [
        str(md_path.relative_to(repo_root)), str(json_path.relative_to(repo_root))]
    return report


def run_verify_adoption(repo_root: Path, brief_path: Path) -> Report:
    """`brief --verify-adoption <path>` — committed-adoption verification of
    one brief file (D-GOV-04 / K-AUTH-2). Renders the fence posture and the
    findings from brief_adoption.verify_adoption; a refusal is wired through
    report.summary["identity_refusal"] (harness.py maps it to stderr + exit 2).
    """
    fence, findings, refusal = brief_adoption.verify_adoption(brief_path, repo_root)
    report = Report(command="brief")

    report.md(f"# Brief committed-adoption verification — {fence.tranche_id}")
    report.md("")
    report.md(VERIFY_SCOPE_NOTE)
    report.md("")
    report.md(f"- brief: `{fence.source_path}`")
    report.md(f"- tranche_id: `{fence.tranche_id}`")
    report.md(f"- state: {fence.state}")
    report.md(f"  - lifecycle: {BRIEF_LIFECYCLE}")
    if fence.adopted_by:
        matched = (f" — allowlist match: {fence.adopted_by_canonical}"
                   if fence.adopted_by_canonical else " — no allowlist match")
        report.md(f"- adopted_by: {fence.adopted_by}{matched}")
    else:
        report.md("- adopted_by: (absent)")
    report.md(f"- adopted_on: {fence.adopted_on or '(absent)'}")
    report.md(f"- committed-ness: {fence.committedness or 'not_checked'}")
    if fence.bound_sha:
        report.md(f"- bound SHA (publication commit; K-AUTH-2): `{fence.bound_sha}`")
        if fence.state in brief_adoption.TERMINAL_STATES:
            report.md(f"  - {brief_adoption.CAVEAT_TERMINAL_BOUND_SHA}")
    report.md(f"- fence_active: {fence.fence_active}")
    if fence.cap_reason:
        report.md(f"  - cap_reason: {fence.cap_reason}")
    report.md("")
    report.md("## Fence summary (entry counts)")
    report.md("")
    for name, entries in (
        ("write_scope", fence.write_scope),
        ("prohibited_paths", fence.prohibited_paths),
        ("validations", fence.validations),
        ("evidence_targets", fence.evidence_targets),
    ):
        report.md(f"- {name}: {len(entries)} entr(y/ies)")
    report.md("")

    for finding in findings:
        report.add_finding(finding)
    for fact in fence.facts:
        report.add_fact(fact)
    report.summary["tranche_id"] = fence.tranche_id
    report.summary["state"] = fence.state
    report.summary["fence_active"] = fence.fence_active
    if fence.bound_sha:
        report.summary["bound_sha"] = fence.bound_sha
    if fence.cap_reason:
        report.summary["cap_reason"] = fence.cap_reason
    if refusal is not None:
        report.summary["identity_refusal"] = refusal
    return report
