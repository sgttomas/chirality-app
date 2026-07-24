#!/usr/bin/env python3
"""`next` — sourced pick-list of active work per pilot project.

The tool NEVER selects; the practitioner selects (plan v3 §Tranche Model:
"practitioner-selected active work"). Per project (via the adapter manifest):
per-state deliverable counts (UNPARSEABLE documents labeled, never guessed)
and a listing of ACTIVE deliverables with the exact ready-made `brief`
command line for each — emitted only when the caller registered a CLI alias
for the project root; an unmapped root gets a labeled note, never a
fabricated command (K-INVENT-1). This is a view, like `status` — no findings
in the normal path, and nothing here is authority; the cited status files
govern.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import adapter_project
from adapter_loader import load_adapter
from harness_common import Report, SourcedFact

# Active = a Current State in this listing precedence order. OPEN is not
# started and ISSUED is terminal — neither is active work.
ACTIVE_STATES = ("CHECKING", "IN_PROGRESS", "SEMANTIC_READY", "INITIALIZED")
MAX_ROWS_PER_PROJECT = 10

PICKLIST_NOTE = (
    "Sourced pick-list only: the tool never selects — the practitioner "
    "selects the active work (plan v3, tranche model).")
ACTIVE_DEFINITION = (
    "Active = Current State in CHECKING > IN_PROGRESS > SEMANTIC_READY > "
    "INITIALIZED (listing precedence); OPEN = not started; ISSUED = terminal. "
    "Any other parsed Current State (e.g. BLOCKED, PREPARATION) is counted "
    "in the per-state facts but not listed as pick-up-next work. "
    "UNPARSEABLE = document-level parse failure — labeled, never guessed "
    "(K-INVENT-1); such files are counted but never listed as active.")
BLOCKED_ON_NOTE = (
    "`blocked-on` quotes optional `blocked-on: D-XX[, D-YY]` tokens from "
    "_STATUS.md; tokens are links to owner-side decisions, not lifecycle state.")
NO_DEL_ID_NOTE = (
    "(directory name carries no DEL-NN-MM id prefix — `brief` requires a DEL "
    "id; not invented per K-INVENT-1)")
NO_ALIAS_NOTE = (
    "(no CLI alias is registered for this project root in harness.py "
    "PROJECT_ALIASES — `brief` command not fabricated per K-INVENT-1)")
TRUNCATION_NOTE = (
    "Truncated: showing {shown} of {total} active row(s); {omitted} row(s) "
    "omitted (no silent caps — rerun with a narrower --project or open the "
    "cited status files).")

TEMPLATES: list[str] = [
    PICKLIST_NOTE, ACTIVE_DEFINITION, NO_DEL_ID_NOTE, NO_ALIAS_NOTE,
    TRUNCATION_NOTE, BLOCKED_ON_NOTE,
]

DEL_ID_PREFIX_RE = re.compile(r"^(DEL-\d{2}-\d{2})(?=[_.\s]|$)")


def run_next(repo_root: Path, project_roots: list[Path],
             cli_aliases: dict[Path, str]) -> Report:
    """`cli_aliases` maps resolved project root -> the `--project` CLI alias,
    built by the caller from its alias table (harness.py PROJECT_ALIASES).
    A root with no entry gets NO_ALIAS_NOTE in place of a command — a
    copy-paste command line is never fabricated (K-INVENT-1)."""
    report = Report(command="next")
    report.md("# Next — active work pick-list (practitioner-selected)")
    report.md("")
    report.md(PICKLIST_NOTE)
    report.md("")
    report.md(ACTIVE_DEFINITION)
    report.md("")
    report.md(BLOCKED_ON_NOTE)
    report.md("")

    precedence = {state: idx for idx, state in enumerate(ACTIVE_STATES)}

    for project_root in project_roots:
        manifest = load_adapter(project_root)
        alias = cli_aliases.get(project_root.resolve())
        rel_root = str(project_root.relative_to(repo_root))
        results = [
            adapter_project.analyze_status_file(path, manifest, repo_root)
            for path in adapter_project.collect_status_files(manifest)
        ]

        # Per-state counts. A document-level parse failure is counted as
        # UNPARSEABLE — labeled, never guessed (K-INVENT-1).
        counts = Counter(
            "UNPARSEABLE" if r.unparseable_doc or not r.current_state
            else r.current_state.strip().upper()
            for r in results)
        counts_value = (", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
                        or "no status files matched")
        report.add_fact(SourcedFact(
            fact_id=f"next.{manifest.project}.state_counts",
            value=counts_value,
            source_path=f"{rel_root}/{manifest.status_glob}",
            source_hint=f"{len(results)} file(s); parser {manifest.parser_dialect}",
            authority_status="observed", parse_status="PARSED"))

        report.md(f"## {manifest.project}")
        report.md("")
        report.md(f"Per-state counts: {counts_value} — source: {len(results)} "
                  f"file(s) matching `{rel_root}/{manifest.status_glob}`")
        report.md("")

        active = [
            r for r in results
            if not r.unparseable_doc
            and (r.current_state or "").strip().upper() in precedence
        ]
        active.sort(key=lambda r: (
            precedence[(r.current_state or "").strip().upper()],
            r.path.parent.name))

        if not active:
            report.md("No active deliverables (per the definition above).")
            report.md("")
            continue

        shown = active[:MAX_ROWS_PER_PROJECT]
        report.md("| Deliverable directory | Current State | Blocked-On | Source | Brief command |")
        report.md("|---|---|---|---|---|")
        for r in shown:
            dirname = r.path.parent.name
            loc = r.rel_path + (f":{r.current_state_line}"
                                if r.current_state_line else "")
            m = DEL_ID_PREFIX_RE.match(dirname)
            if m and alias is not None:
                command = ("`python3 tools/practitioner_harness/harness.py "
                           f"brief --project {alias} --deliverable {m.group(1)}`")
            elif m:
                command = NO_ALIAS_NOTE
            else:
                command = NO_DEL_ID_NOTE
            state = (r.current_state or "").strip().upper()
            blocked_on = ", ".join(f"`{token}`" for token in r.blocked_on) or "-"
            report.md(
                f"| `{dirname}` | {state} | {blocked_on} | `{loc}` | {command} |"
            )
        report.md("")
        if len(active) > len(shown):
            report.md(TRUNCATION_NOTE.format(
                shown=len(shown), total=len(active),
                omitted=len(active) - len(shown)))
            report.md("")
        report.summary[f"active.{manifest.project}"] = len(active)

    return report
