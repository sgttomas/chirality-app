#!/usr/bin/env python3
"""practitioner harness — governed read-mostly project observation CLI.

Subcommands: status, drift, self-check, bridge-status, brief, next,
run-validations, scope-check, evidence-check, closeout-digest, coord-check.
Markdown report always to stdout; optional JSON report, brief files,
evidence records, and closeout digests are contained to the declared
generated root `{REPO_ROOT}/_harness_generated/` (D-GOV-01 / K-WRITE-2).
`brief` generates a CANDIDATE projection or, with `--verify-adoption <path>`,
verifies a brief's committed adoption (detect, never adopt — no harness
command flips a brief's state; D-GOV-04). `next` is a sourced pick-list of
active work: the practitioner selects; the tool never selects.
`run-validations` executes the adapter manifest's declared validation
commands under the plan v3 mutation-control contract and captures evidence
records — facts, never approval; a completed exit-0 run is structural
evidence only (K-DOMAIN-4 analogue). `scope-check` compares the changed
paths of a git diff range to the brief's fence (BLOCK only against a
verified active fence; path judgment is never lifecycle judgment, K-GATE-1).
`evidence-check` verifies evidence completeness per the provenance ladder
(D-GOV-08 Option B; completeness never sufficiency; nothing there BLOCKs).
`closeout-digest` composes both checks in-process into a digest for the
human CHANGE closeout — never a lifecycle transition.
`coord-check` is the report-only coordination/control analogue over a git
diff range: citation resolution, decision-register coverage, named
precedent presence where packet-shaped records call for it, and
machine-absolute paths on diff-added lines (HB-10; SPEC §0.2.4).

Exit codes (D-GOV-02): 0 = ran, no BLOCK; 1 = >=1 BLOCK (or >=1 REVIEW under
--strict); 2 = operational error or refusal.

Everything emitted is a generated view — not authority; the cited source
files govern on any disagreement (K-AUTH-1).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cmd_brief
import cmd_bridge_status
import cmd_closeout
import cmd_coord_check
import cmd_drift
import cmd_evidence_check
import cmd_next
import cmd_run_validations
import cmd_scope_check
import cmd_self_check
import cmd_status
from harness_common import (
    EXIT_OPERATIONAL,
    GENERATED_ROOT_NAME,
    HarnessOperationalError,
    Report,
    compute_exit_code,
    resolve_repo_root,
)

PROJECT_ALIASES: dict[str, str] = {
    "app-dev": "projects/chirality-app-dev",
    "chirality-app-dev": "projects/chirality-app-dev",
    "piping": "projects/chirality-piping",
    "chirality-piping": "projects/chirality-piping",
    "pec": "projects/pec",
    "chirality-pec": "projects/pec",
}

FULL_CITIZENSHIP_PROJECTS = (
    "app-dev",
    "chirality-app-dev",
    "piping",
    "chirality-piping",
)


def _project_root(repo_root: Path, name: str) -> Path:
    rel = PROJECT_ALIASES.get(name)
    if rel is None:
        raise HarnessOperationalError(
            f"Unknown --project {name!r}; known: {sorted(set(PROJECT_ALIASES))}")
    root = repo_root / rel
    if not root.is_dir():
        raise HarnessOperationalError(f"Project root absent: {root}")
    return root


def _alias_by_root(repo_root: Path) -> dict[Path, str]:
    """Reverse of PROJECT_ALIASES for `next`: resolved project root -> the
    CLI `--project` alias (where two aliases share a root, the shorter wins).
    A root missing from this mapping gets no ready-made `brief` command —
    `next` labels it instead of fabricating one (K-INVENT-1)."""
    by_root: dict[Path, str] = {}
    for alias, rel in PROJECT_ALIASES.items():
        root = (repo_root / rel).resolve()
        if root not in by_root or len(alias) < len(by_root[root]):
            by_root[root] = alias
    return by_root


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-root", default=argparse.SUPPRESS,
                        help="Repo root (default: git rev-parse --show-toplevel, "
                             "else walk up for .git)")
    common.add_argument("--strict", action="store_true", default=argparse.SUPPRESS,
                        help="Treat REVIEW findings as exit-1")
    common.add_argument("--json-report", default=argparse.SUPPRESS,
                        help=f"Write the JSON report at this path (must be inside "
                             f"{GENERATED_ROOT_NAME}/)")
    common.add_argument("--out-dir", default=argparse.SUPPRESS,
                        help=f"Generated-output directory (default: "
                             f"{{REPO_ROOT}}/{GENERATED_ROOT_NAME}; all file writes "
                             "contained to the generated root)")

    parser = argparse.ArgumentParser(
        prog="harness.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", parents=[common],
                              help="One-page sourced posture view")
    g = p_status.add_mutually_exclusive_group(required=True)
    g.add_argument("--project", choices=FULL_CITIZENSHIP_PROJECTS)
    g.add_argument("--domain-engines", action="store_true")

    p_drift = sub.add_parser("drift", parents=[common],
                             help="Current State vs history-assertion drift audit")
    p_drift.add_argument("--project", choices=FULL_CITIZENSHIP_PROJECTS)
    p_drift.add_argument("--all", action="store_true",
                         help="Audit both pilot projects (default)")
    p_drift.add_argument("--include-domain-engines", action="store_true",
                         help="Fold in the domain-engine control-area surface audit")

    p_check = sub.add_parser("self-check", parents=[common],
                             help="Consistency audit over the pilot scope")
    p_check.add_argument("--root", help="Audit only this root (default: pilot scope)")

    sub.add_parser("bridge-status", parents=[common],
                   help="Generated bridge owner-shaped act pick-list; the "
                        "tool never selects")

    p_brief = sub.add_parser("brief", parents=[common],
                             help="Emit a CANDIDATE tranche brief (never adopts), "
                                  "or verify committed adoption of an existing "
                                  "brief (--verify-adoption; detect, never adopt)")
    # Generate mode requires --project/--deliverable; verify mode takes ONLY
    # the path. Both are optional at parse level and enforced manually so the
    # two modes can share the subcommand without argparse contortions.
    p_brief.add_argument("--project", choices=FULL_CITIZENSHIP_PROJECTS)
    p_brief.add_argument("--deliverable", metavar="DEL-NN-MM")
    p_brief.add_argument("--objective", default=None)
    p_brief.add_argument("--tranche-id", default=None)
    p_brief.add_argument("--verify-adoption", metavar="BRIEF_PATH", default=None,
                         help="Verify committed adoption of the brief file at "
                              "BRIEF_PATH (D-GOV-04 / K-AUTH-2); takes only "
                              "the path — never a lifecycle transition")

    p_next = sub.add_parser("next", parents=[common],
                            help="Sourced pick-list of active work — the "
                                 "practitioner selects; the tool never selects")
    p_next.add_argument("--project", choices=FULL_CITIZENSHIP_PROJECTS,
                        help="One project only (default: both pilot projects)")

    p_runval = sub.add_parser(
        "run-validations", parents=[common],
        help="Execute the adapter manifest's declared validation commands "
             "for the project the brief fences, under the mutation-control "
             "contract; capture evidence records (facts, never approval)")
    p_runval.add_argument("--brief", required=True, metavar="BRIEF_PATH",
                          help="The brief whose first write_scope entry "
                               "resolves the project; committed-adoption "
                               "posture is verified first (D-GOV-04)")
    p_runval.add_argument("--list", action="store_true",
                          help="Print the resolved command list and stop — "
                               "nothing executed, nothing written")
    p_runval.add_argument("--timeout-seconds", type=int, default=1800,
                          help="Per-command timeout (default 1800); a "
                               "timed-out command is recorded TIMED_OUT, "
                               "never an inferred outcome")

    p_scope = sub.add_parser(
        "scope-check", parents=[common],
        help="Compare the changed paths of a git diff range to the brief's "
             "fence — findings report only; BLOCK only against a verified "
             "active fence (D-GOV-04); path judgment is never lifecycle "
             "judgment (K-GATE-1)")
    p_scope.add_argument("--brief", required=True, metavar="BRIEF_PATH",
                         help="The brief whose fence judges the paths; "
                              "committed-adoption posture is verified first "
                              "(D-GOV-04)")
    p_scope.add_argument("--diff", required=True, metavar="RANGE",
                         help="Git rev or A..B range for git diff "
                              "--name-status; validated with git rev-parse "
                              "first — an unresolvable range is an "
                              "operational error (exit 2)")

    p_evidence = sub.add_parser(
        "evidence-check", parents=[common],
        help="Verify evidence completeness for the brief's declared "
             "validations per the provenance ladder (D-GOV-08 Option B) — "
             "completeness, never sufficiency; nothing here BLOCKs")
    p_evidence.add_argument("--brief", required=True, metavar="BRIEF_PATH",
                            help="The brief whose declared validations and "
                                 "evidence targets are checked; committed-"
                                 "adoption posture is verified first "
                                 "(D-GOV-04)")

    p_closeout = sub.add_parser(
        "closeout-digest", parents=[common],
        help="Compose scope-check + evidence-check in-process into one "
             "digest for the human CHANGE closeout — never a lifecycle "
             "transition")
    p_closeout.add_argument("--brief", required=True, metavar="BRIEF_PATH",
                            help="The brief the digest summarizes against")
    p_closeout.add_argument("--diff", required=True, metavar="RANGE",
                            help="Git rev or A..B range passed to the "
                                 "composed scope-check")
    p_closeout.add_argument("--write-digest", action="store_true",
                            help="Also write the digest markdown to "
                                 "_harness_generated/closeout/"
                                 "<tranche_id>.md (contained to the "
                                 "generated root)")

    p_coord = sub.add_parser(
        "coord-check", parents=[common],
        help="Report-only checks for changed coordination/control artifacts "
             "in a git diff range: citation resolution, decision-register "
             "coverage, named-precedent presence, and machine-absolute "
             "paths on diff-added lines")
    p_coord.add_argument("--diff", required=True, metavar="RANGE",
                         help="Git rev or A..B range for git diff "
                              "--name-status; validated with git rev-parse "
                              "first")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    strict = bool(getattr(args, "strict", False))
    json_report: str | None = getattr(args, "json_report", None)
    try:
        repo_root = resolve_repo_root(getattr(args, "repo_root", None))
        out_dir = Path(getattr(args, "out_dir", repo_root / GENERATED_ROOT_NAME))

        report: Report
        if args.command == "status":
            if getattr(args, "domain_engines", False):
                report = cmd_status.run_status_domain_engines(repo_root)
            else:
                report = cmd_status.run_status_project(
                    repo_root, _project_root(repo_root, args.project))
        elif args.command == "drift":
            if args.project and not args.all:
                roots = [_project_root(repo_root, args.project)]
            else:
                roots = [_project_root(repo_root, "app-dev"),
                         _project_root(repo_root, "piping")]
            report = cmd_drift.run_drift(
                repo_root, roots,
                include_domain_engines=getattr(args, "include_domain_engines", False))
        elif args.command == "self-check":
            root_filter = Path(args.root) if getattr(args, "root", None) else None
            if root_filter is not None and not root_filter.is_absolute():
                root_filter = repo_root / root_filter
            report, refusal = cmd_self_check.run_self_check(repo_root, root_filter)
            if refusal is not None:
                sys.stdout.write(report.render_markdown())
                if json_report:
                    report.write_json(json_report, repo_root)
                print(refusal, file=sys.stderr)
                return EXIT_OPERATIONAL
        elif args.command == "bridge-status":
            report = cmd_bridge_status.run_bridge_status(repo_root)
        elif args.command == "brief":
            if args.verify_adoption:
                rejected = [flag for flag, value in (
                    ("--project", args.project),
                    ("--deliverable", args.deliverable),
                    ("--objective", args.objective),
                    ("--tranche-id", getattr(args, "tranche_id", None)),
                ) if value]
                if rejected:
                    raise HarnessOperationalError(
                        "brief --verify-adoption takes only the brief path; "
                        f"rejected: {', '.join(rejected)}.")
                brief_path = Path(args.verify_adoption)
                if not brief_path.is_absolute():
                    brief_path = repo_root / brief_path
                report = cmd_brief.run_verify_adoption(repo_root, brief_path)
            else:
                if not args.project or not args.deliverable:
                    raise HarnessOperationalError(
                        "brief (generate mode) requires --project and "
                        "--deliverable; verify mode requires "
                        "--verify-adoption <path>.")
                project_root = _project_root(repo_root, args.project)
                others = sorted(
                    {repo_root / rel for rel in PROJECT_ALIASES.values()} - {project_root})
                report = cmd_brief.run_brief(
                    repo_root, project_root, [p for p in others if p.is_dir()],
                    deliverable=args.deliverable, objective=args.objective,
                    tranche_id=getattr(args, "tranche_id", None), out_dir=out_dir)
        elif args.command == "next":
            if getattr(args, "project", None):
                roots = [_project_root(repo_root, args.project)]
            else:
                roots = [_project_root(repo_root, "app-dev"),
                         _project_root(repo_root, "piping")]
            report = cmd_next.run_next(repo_root, roots, _alias_by_root(repo_root))
        elif args.command == "run-validations":
            brief_path = Path(args.brief)
            if not brief_path.is_absolute():
                brief_path = repo_root / brief_path
            report = cmd_run_validations.run_run_validations(
                repo_root, brief_path, out_dir,
                timeout_seconds=args.timeout_seconds,
                list_only=getattr(args, "list", False),
                alias_by_root=_alias_by_root(repo_root))
        elif args.command == "scope-check":
            brief_path = Path(args.brief)
            if not brief_path.is_absolute():
                brief_path = repo_root / brief_path
            report = cmd_scope_check.run_scope_check(
                repo_root, brief_path, args.diff)
        elif args.command == "evidence-check":
            brief_path = Path(args.brief)
            if not brief_path.is_absolute():
                brief_path = repo_root / brief_path
            report = cmd_evidence_check.run_evidence_check(
                repo_root, brief_path, out_dir, _alias_by_root(repo_root))
        elif args.command == "closeout-digest":
            brief_path = Path(args.brief)
            if not brief_path.is_absolute():
                brief_path = repo_root / brief_path
            report = cmd_closeout.run_closeout_digest(
                repo_root, brief_path, args.diff, out_dir,
                _alias_by_root(repo_root),
                write_digest=getattr(args, "write_digest", False))
        elif args.command == "coord-check":
            report = cmd_coord_check.run_coord_check(repo_root, args.diff)
        else:  # pragma: no cover - argparse enforces the choices.
            raise HarnessOperationalError(f"Unknown command {args.command!r}")

        sys.stdout.write(report.render_markdown())
        if json_report:
            report.write_json(json_report, repo_root)
        if report.summary.get("identity_refusal"):
            print(str(report.summary["identity_refusal"]), file=sys.stderr)
            return EXIT_OPERATIONAL
        return compute_exit_code(report.findings, strict=strict)
    except HarnessOperationalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_OPERATIONAL


if __name__ == "__main__":
    sys.exit(main())
