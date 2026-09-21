#!/usr/bin/env python3
"""Check that owners excluded by a boundary requirement resolve in the cited claim.

This is the deterministic half of the B8 rule nominated in
`BATCH_B8_FANIN.md` §3.1 and dispositioned in P7 §4: *every act enumerated in a
boundary-exclusion requirement resolves to a named owner in the cited claim.*

The enumeration half — deciding what counts as an "act" in a sentence — is
semantic and belongs to the `scope-of-work` skill's QA method, not here. What is
deterministic, and all this tool asserts, is the resolution half: **every owner
ID named by a whole-requirement boundary exclusion is also named by a claim that
the same requirement cites.**

Scope, measured against the live corpus rather than assumed:

* **CHECKED** — whole-requirement boundary exclusions ("shall perform no act
  owned by another deliverable …; each is cited to its owner in `CLM-NNN`").
  These bind owner and claim syntactically, so resolution is decidable.
* **NOT_CHECKABLE** — per-act exclusion clauses inside an otherwise-positive
  requirement. In the live corpus the owner and its claim reference are not
  syntactically bound: some clauses cite no claim at all, and requirement-level
  claim harvesting mis-attributes across clauses. Reporting these as failures
  would be reporting detector limits as contract defects, so they are surfaced
  for the skill's QA method instead.
* **NO_CITED_CLAIM** — a whole-requirement boundary exclusion that cites no
  `CLM-NNN` at all. Its owners cannot be resolved against anything, so this is
  reported separately rather than counted as a pass or as a failure. No live
  contract is in this state today; the category exists because the shape is
  expressible and would otherwise pass silently.
* **NOT_APPLICABLE** — contracts with no `REQ-NNN` definitions at all (for
  example legacy four-document conversions, whose requirements survive only as
  blockquoted source under a different ID grammar). These are reported as
  out-of-grammar, never as passing.

Exit codes: 0 = no unresolved owners; 1 = unresolved owners found; 2 = operational
error (unreadable or unparseable input).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from common import (  # noqa: E402
    SowError,
    load_catalog,
    parse_frontmatter,
    section_text,
)

REQUIREMENT_SECTION = "Completion and Reliance Basis — Epistemology"

# A whole-requirement boundary exclusion. The corpus writes this two ways:
# "shall perform no act owned by another deliverable" and "shall parse no feed
# owned by a sibling deliverable"; both continue "and shall perform no act
# owned by another package".
TEMPLATE_A_RE = re.compile(
    r"shall\s+(?:perform|parse)\s+no\s+\w+(?:\s+\w+)?\s+owned\s+by\s+(?:another|a\s+sibling)",
    re.IGNORECASE,
)

# Owner tokens are backticked deliverable IDs, usually possessive. Both ASCII
# and typographic apostrophes appear in the corpus.
DELIVERABLE_RE = re.compile(r"`(DEL-\d{2,3}-\d{2,3})`")
POSSESSIVE_OWNER_RE = re.compile(r"`DEL-\d{2,3}-\d{2,3}`(?:'s|’s)")
BOUNDARY_LANGUAGE_RE = re.compile(r"owned by|owner|discharg|boundary|exclusion|belongs to", re.IGNORECASE)
CLAIM_REF_RE = re.compile(r"\bCLM-\d{3}\b")
DEFINITION_RE = re.compile(r"^-\s+\*\*(?P<id>[A-Z]{2,3}-\d{3})\*\*\s+—\s+", re.MULTILINE)

# `DEL-02-01` through `DEL-02-07` names every deliverable in the span, not just
# the two endpoints.
RANGE_RE = re.compile(r"`(DEL-(\d{2,3})-(\d{2,3}))`\s+through\s+`(DEL-(\d{2,3})-(\d{2,3}))`")


@dataclass
class Finding:
    category: str
    requirement_id: str
    detail: str
    owners: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "category": self.category,
            "requirement_id": self.requirement_id,
            "detail": self.detail,
            "owners": list(self.owners),
        }


@dataclass
class Report:
    path: str
    status: str = "OK"
    checked: int = 0
    not_checkable: int = 0
    no_cited_claim: int = 0
    findings: list[Finding] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "status": self.status,
            "requirements_checked": self.checked,
            "requirements_not_checkable": self.not_checkable,
            "requirements_without_cited_claim": self.no_cited_claim,
            "findings": [f.as_dict() for f in self.findings],
        }


def strip_blockquotes(text: str) -> str:
    """Blank blockquote lines exactly as `parse_sow_text` does before ID extraction.

    Blockquoted legacy source is readable context, not local ID syntax. Without
    this, IDs that `validate_document` considers non-existent would be scanned.
    """
    return "\n".join("" if re.match(r"^ {0,3}>", line) else line for line in text.splitlines())


def definition_bodies(section: str) -> list[tuple[str, str]]:
    """Split a section into (id, body) pairs, body running to the next definition."""
    matches = list(DEFINITION_RE.finditer(section))
    bodies: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        bodies.append((match.group("id"), section[match.start() : end]))
    return bodies


def expand_owner_tokens(text: str) -> set[str]:
    """Every deliverable ID named by `text`, expanding `X through Y` spans."""
    owners = set(DELIVERABLE_RE.findall(text))
    for start_id, start_pkg, start_num, end_id, end_pkg, end_num in RANGE_RE.findall(text):
        if start_pkg != end_pkg:
            # A cross-package span is not a deliverable enumeration; keep the
            # endpoints only rather than inventing IDs.
            continue
        width = len(start_num)
        for value in range(int(start_num), int(end_num) + 1):
            owners.add(f"DEL-{start_pkg}-{str(value).zfill(width)}")
    return owners


def check_document(path: Path, raw: str) -> Report:
    report = Report(path=str(path))
    _, body = parse_frontmatter(raw)
    body = strip_blockquotes(body)

    requirement_section = section_text(body, REQUIREMENT_SECTION)
    requirements = [
        (rid, rbody) for rid, rbody in definition_bodies(requirement_section) if rid.startswith("REQ-")
    ]
    if not requirements:
        report.status = "NOT_APPLICABLE"
        report.findings.append(
            Finding(
                "NOT_APPLICABLE",
                "-",
                "no REQ-NNN definitions; contract is outside the SOW_V1 requirement grammar",
            )
        )
        return report

    # Claims are defined across every prose section, so index the whole body.
    claims = {cid: cbody for cid, cbody in definition_bodies(body) if cid.startswith("CLM-")}

    for rid, rbody in requirements:
        owners = expand_owner_tokens(rbody)
        if not TEMPLATE_A_RE.search(rbody):
            # A per-act exclusion is signalled either by boundary language or by
            # the possessive owner form ("the act … is `DEL-04-03`'s"), which
            # carries no keyword at all.
            if owners and (BOUNDARY_LANGUAGE_RE.search(rbody) or POSSESSIVE_OWNER_RE.search(rbody)):
                report.not_checkable += 1
                report.findings.append(
                    Finding(
                        "NOT_CHECKABLE",
                        rid,
                        "per-act exclusion clause: owner and claim are not syntactically bound; "
                        "route to the scope-of-work QA method",
                        tuple(sorted(owners)),
                    )
                )
            continue

        cited = CLAIM_REF_RE.findall(rbody)
        if not cited:
            report.no_cited_claim += 1
            report.findings.append(
                Finding(
                    "NO_CITED_CLAIM",
                    rid,
                    "boundary requirement cites no CLM-NNN; resolution cannot be checked",
                    tuple(sorted(owners)),
                )
            )
            continue

        resolvable: set[str] = set()
        missing_claims: list[str] = []
        for claim_id in dict.fromkeys(cited):
            claim_body = claims.get(claim_id)
            if claim_body is None:
                missing_claims.append(claim_id)
                continue
            resolvable |= expand_owner_tokens(claim_body)

        report.checked += 1
        if missing_claims:
            report.findings.append(
                Finding(
                    "UNDEFINED_CLAIM",
                    rid,
                    f"cites undefined claim(s): {', '.join(sorted(missing_claims))}",
                )
            )
        unresolved = sorted(owners - resolvable)
        if unresolved:
            report.findings.append(
                Finding(
                    "UNRESOLVED_OWNER",
                    rid,
                    "owner(s) excluded by this requirement are not named by any claim it cites "
                    f"({', '.join(dict.fromkeys(cited))})",
                    tuple(unresolved),
                )
            )

    if any(f.category in {"UNRESOLVED_OWNER", "UNDEFINED_CLAIM"} for f in report.findings):
        report.status = "FAIL"
    return report


def iter_targets(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if (target / "ScopeOfWork.md").is_file():
        return [target / "ScopeOfWork.md"]
    return sorted(target.rglob("ScopeOfWork.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", type=Path, help="ScopeOfWork.md, a deliverable folder, or a tree to scan")
    parser.add_argument("--json", type=Path, help="Write the full report here")
    parser.add_argument(
        "--show-not-checkable",
        action="store_true",
        help="List per-act exclusions that require the skill QA method",
    )
    args = parser.parse_args()

    load_catalog()  # fail fast if the ID catalog is unreadable
    targets = iter_targets(args.target)
    if not targets:
        print(f"ERROR: no ScopeOfWork.md under {args.target}", file=sys.stderr)
        return 2

    reports: list[Report] = []
    for path in targets:
        try:
            reports.append(check_document(path, path.read_text(encoding="utf-8")))
        except (OSError, SowError, ValueError) as exc:
            print(f"ERROR: {path}: {exc}", file=sys.stderr)
            return 2

    failures = [r for r in reports if r.status == "FAIL"]
    checked = sum(r.checked for r in reports)
    not_checkable = sum(r.not_checkable for r in reports)
    no_cited_claim = sum(r.no_cited_claim for r in reports)
    not_applicable = sum(1 for r in reports if r.status == "NOT_APPLICABLE")

    for report in reports:
        for finding in report.findings:
            if finding.category in {"UNRESOLVED_OWNER", "UNDEFINED_CLAIM"}:
                owners = f" [{', '.join(finding.owners)}]" if finding.owners else ""
                print(f"{finding.category}: {report.path} {finding.requirement_id}: {finding.detail}{owners}")
            elif args.show_not_checkable and finding.category in {"NOT_CHECKABLE", "NO_CITED_CLAIM"}:
                print(f"{finding.category}: {report.path} {finding.requirement_id}: {finding.detail}")

    print(
        f"\nContracts: {len(reports)} ({not_applicable} out-of-grammar) | "
        f"boundary requirements checked: {checked} | "
        f"per-act exclusions for skill QA: {not_checkable} | "
        f"boundary requirements citing no claim: {no_cited_claim} | "
        f"contracts failing: {len(failures)}"
    )

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps([r.as_dict() for r in reports], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
