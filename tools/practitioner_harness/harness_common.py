#!/usr/bin/env python3
"""Shared primitives for the practitioner harness.

Severity taxonomy per D-GOV-02 (TYPES.md §11, ratified). Findings and facts
carry per-invariant ratification labels (K-CLAIM-1 posture); the basis is the
owner ratification of docs/CONTRACT.md in full, 2026-07-11 (recorded in the
docs/CONTRACT.md status block; loop Receipt 9), with D-GOV-05 (2026-07-01)
remaining the ruling of record for the earlier partial basis.
Every file write is contained to the declared generated root per D-GOV-01 /
K-WRITE-2 via `ensure_generated_scope`.

Authority note: everything this module helps emit is a generated view — not
authority. The cited source files govern on any disagreement.
"""

from __future__ import annotations

import dataclasses
import datetime as _dt
import enum
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

TOOL_NAME = "practitioner_harness"
REPORT_SCHEMA = "practitioner-harness-report/v1"
CONTRACT_SOURCE = ("governance_harness_plan_v3_2026-07-01 "
                   "+ D-GOV-01..07 @ 82a35c545 + D-GOV-08 @ 5f0f45c2b "
                   "+ docs/CONTRACT.md RATIFIED 2026-07-11")
GENERATED_ROOT_NAME = "_harness_generated"
HUMAN_ACTORS_RELPATH = "docs/governance_harness/human_actors.md"

# Exit codes (D-GOV-02):
EXIT_OK = 0            # ran; no BLOCK (REVIEW/WARN/INFO/NOT_APPLICABLE may exist)
EXIT_BLOCK = 1         # >=1 BLOCK finding (or >=1 REVIEW under --strict)
EXIT_OPERATIONAL = 2   # operational error or refusal


class Severity(enum.Enum):
    BLOCK = "BLOCK"
    REVIEW = "REVIEW"
    WARN = "WARN"
    INFO = "INFO"
    NOT_APPLICABLE = "NOT_APPLICABLE"


# --- Per-invariant ratification labels (K-CLAIM-1) ----------------------------
# RATIFIED basis: owner ratification of docs/CONTRACT.md in full, 2026-07-11
# (recorded in the docs/CONTRACT.md status block; loop Receipt 9). D-GOV-05
# (2026-07-01) remains the ruling of record for the earlier partial basis.
# The full K-* catalog below mirrors the docs/CONTRACT.md "K-* Invariant
# Index" (27 IDs); DRAFT = pending ratification on its own track; findings on
# DRAFT invariants are advisory (never BLOCK) except purely local technical
# checks.
RATIFIED_INVARIANTS: dict[str, str] = {
    "SOURCE_OF_TRUTH": "RATIFIED",       # DIRECTIVE §2.1/§2.3
    "GENERATED_OUTPUT": "RATIFIED",      # D-GOV-01
    "SEVERITY_TAXONOMY": "RATIFIED",     # D-GOV-02 (TYPES §11)
    # docs/CONTRACT.md K-* Invariant Index (owner ratification 2026-07-11):
    "K-HIER-1": "RATIFIED",
    "K-ID-1": "RATIFIED",
    "K-AUTH-1": "RATIFIED",
    "K-AUTH-2": "RATIFIED",
    "K-BIND-1": "RATIFIED",
    "K-SEAL-1": "RATIFIED",
    "K-GHOST-1": "RATIFIED",
    "K-DEP-1": "RATIFIED",
    "K-DEP-2": "RATIFIED",
    "K-STATUS-1": "RATIFIED",
    "K-STALE-1": "RATIFIED",
    "K-STALE-2": "RATIFIED",
    "K-VAL-1": "RATIFIED",
    "K-GATE-1": "RATIFIED",
    "K-MERGE-1": "RATIFIED",
    "K-PROV-1": "RATIFIED",
    "K-INVENT-1": "RATIFIED",
    "K-CONFLICT-1": "RATIFIED",
    "K-CLAIM-1": "RATIFIED",
    "K-WRITE-1": "RATIFIED",
    "K-WRITE-2": "RATIFIED",
    "K-SNAP-1": "RATIFIED",
    "K-AGENTS-1": "RATIFIED",
    "K-DOMAIN-1": "RATIFIED",
    "K-DOMAIN-2": "RATIFIED",
    "K-DOMAIN-3": "RATIFIED",
    "K-DOMAIN-4": "RATIFIED",
}

# Empty since the 2026-07-11 full ratification of docs/CONTRACT.md; the name
# and its use are retained so imports and `ratification_labels_map()` survive,
# and so any future not-yet-ratified invariant can be listed here explicitly.
DRAFT_INVARIANTS_EXPLICIT: tuple[str, ...] = ()


def ratification_for(invariant: str) -> str:
    """Label an invariant RATIFIED | DRAFT | N_A.

    Basis: owner ratification of docs/CONTRACT.md in full, 2026-07-11
    (docs/CONTRACT.md status block; loop Receipt 9); D-GOV-05 (2026-07-01)
    remains the ruling of record for the earlier partial basis.
    """
    if invariant in RATIFIED_INVARIANTS:
        return "RATIFIED"
    # Fail-closed default: any K-* ID not in the catalog above (e.g. a future
    # invariant added to a CONTRACT before this map is updated) labels DRAFT,
    # keeping its findings advisory until consciously cataloged as RATIFIED.
    if invariant in DRAFT_INVARIANTS_EXPLICIT or invariant.startswith("K-"):
        return "DRAFT"
    return "N_A"


def ratification_labels_map() -> dict[str, str]:
    labels = dict(RATIFIED_INVARIANTS)
    for inv in DRAFT_INVARIANTS_EXPLICIT:
        labels[inv] = "DRAFT"
    return labels


class HarnessOperationalError(Exception):
    """Operational error or refusal -> exit 2."""


class GeneratedScopeError(HarnessOperationalError):
    """Attempted write outside the declared generated root -> exit 2."""


class IdentityRefusalError(HarnessOperationalError):
    """D-GOV-04 refusal: identity-dependent check cannot attribute an actor."""


@dataclass
class Finding:
    severity: Severity
    code: str
    dimension: str
    message: str
    source_path: str
    source_line: int | None = None
    invariant: str = ""
    invariant_ratification: str = ""
    caveat: str = ""

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        d["severity"] = self.severity.value
        return d


@dataclass
class SourcedFact:
    fact_id: str
    value: str
    source_path: str
    source_hint: str = ""
    authority_status: str = ""
    parse_status: str = "PARSED"
    caveat: str = ""

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)


def make_finding(
    severity: Severity,
    code: str,
    dimension: str,
    message: str,
    source_path: str,
    source_line: int | None = None,
    invariant: str = "",
    caveat: str = "",
    local_technical: bool = False,
) -> Finding:
    """Build a Finding, enforcing the D-GOV-05 advisory rule.

    Findings on DRAFT invariants are advisory (never BLOCK) except purely
    local technical checks (path containment, source-file existence,
    generated-output labeling), which may BLOCK regardless.
    """
    ratification = ratification_for(invariant) if invariant else "N_A"
    if severity is Severity.BLOCK and ratification == "DRAFT" and not local_technical:
        severity = Severity.REVIEW
        caveat = (caveat + " " if caveat else "") + (
            "Severity capped at REVIEW: invariant is DRAFT (advisory per D-GOV-05)."
        )
    return Finding(
        severity=severity,
        code=code,
        dimension=dimension,
        message=message,
        source_path=source_path,
        source_line=source_line,
        invariant=invariant,
        invariant_ratification=ratification,
        caveat=caveat,
    )


def cap_severity_for_unadopted_brief(finding: Finding, reason: str = "") -> Finding:
    """D-GOV-04: findings referencing a brief that is not HUMAN_ADOPTED+committed
    are capped at REVIEW."""
    if finding.severity is Severity.BLOCK:
        finding.severity = Severity.REVIEW
        extra = reason or (
            "Severity capped at REVIEW: referenced brief is not HUMAN_ADOPTED"
            "+committed (D-GOV-04)."
        )
        finding.caveat = (finding.caveat + " " if finding.caveat else "") + extra
    return finding


def compute_exit_code(findings: list[Finding], strict: bool = False) -> int:
    sevs = {f.severity for f in findings}
    if Severity.BLOCK in sevs:
        return EXIT_BLOCK
    if strict and Severity.REVIEW in sevs:
        return EXIT_BLOCK
    return EXIT_OK


# --- Repo root and generated-scope containment --------------------------------

def resolve_repo_root(explicit: str | None = None, start: Path | None = None) -> Path:
    """Resolve the repo root: explicit flag, else `git rev-parse --show-toplevel`,
    else walk up looking for `.git`."""
    if explicit:
        root = Path(explicit).resolve()
        if not root.is_dir():
            raise HarnessOperationalError(f"--repo-root is not a directory: {explicit}")
        return root
    cwd = (start or Path.cwd()).resolve()
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return Path(proc.stdout.strip()).resolve()
    except OSError:
        pass
    node = cwd
    while True:
        if (node / ".git").exists():
            return node
        if node.parent == node:
            break
        node = node.parent
    raise HarnessOperationalError(
        "Cannot resolve repo root (no git, no .git ancestor); pass --repo-root."
    )


def generated_root(repo_root: Path) -> Path:
    """The containment boundary for all harness writes.

    The boundary is the LEXICAL `{repo_root}/_harness_generated` under the
    resolved repo root. If that path exists as a symlink, refuse outright:
    resolving it would silently relocate the boundary (outside the repo, or
    onto a governed tree), defeating the containment this function anchors.
    """
    lexical = repo_root.resolve() / GENERATED_ROOT_NAME
    if lexical.is_symlink():
        raise GeneratedScopeError(
            f"Refusing to use {GENERATED_ROOT_NAME}/ as the generated root: it is a "
            f"symlink ({lexical} -> {os.readlink(lexical)}). The declared generated "
            "root must be a real directory under the repo root (D-GOV-01 / K-WRITE-2)."
        )
    return lexical


def ensure_generated_scope(path: Path | str, repo_root: Path) -> Path:
    """Resolve `path` (symlinks, `..`, absolutes) and REFUSE anything outside
    `{REPO_ROOT}/_harness_generated/` (D-GOV-01 / K-WRITE-2). Returns the
    resolved path on success; raises GeneratedScopeError otherwise.

    Comparison is by exact resolved path components (case-sensitive) so a
    case-variant sibling prefix cannot spoof containment.
    """
    gen_root = generated_root(repo_root)
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = gen_root / candidate
    # Resolve the deepest existing ancestor (this resolves symlinks in parents),
    # then re-append the non-existent tail without allowing `..` escapes.
    resolved = candidate.resolve()
    gen_parts = gen_root.parts
    res_parts = resolved.parts
    if len(res_parts) < len(gen_parts) or res_parts[: len(gen_parts)] != gen_parts:
        raise GeneratedScopeError(
            f"Refusing write outside the declared generated root "
            f"{GENERATED_ROOT_NAME}/ : {path} (resolved: {resolved}). "
            "All harness file writes are contained per D-GOV-01 / K-WRITE-2."
        )
    return resolved


def write_generated_file(path: Path | str, text: str, repo_root: Path) -> Path:
    resolved = ensure_generated_scope(path, repo_root)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    # Re-check after mkdir in case a parent component was a symlink created race-side.
    resolved = ensure_generated_scope(resolved, repo_root)
    resolved.write_text(text, encoding="utf-8")
    return resolved


# --- human_actors allowlist (D-GOV-04) ----------------------------------------

@dataclass
class HumanActorsAllowlist:
    source_path: str
    canonical_names: list[str] = field(default_factory=list)
    aliases: dict[str, str] = field(default_factory=dict)  # alias -> canonical

    def match(self, actor: str) -> str | None:
        """Return the canonical name if `actor` matches, else None."""
        raw = actor.strip().strip("*").strip()
        candidates = [raw]
        # Leading token before parenthetical/qualifier, e.g. "owner (in-session)".
        if "(" in raw:
            candidates.append(raw.split("(", 1)[0].strip())
        first = raw.split()[0].strip(",;") if raw.split() else ""
        if first:
            candidates.append(first)
        for cand in candidates:
            if cand in self.canonical_names:
                return cand
            if cand in self.aliases:
                return self.aliases[cand]
        return None


def load_human_actors(repo_root: Path) -> HumanActorsAllowlist | None:
    """Load the owner-curated identity allowlist. Returns None when absent
    (callers of identity-dependent checks must then REFUSE per D-GOV-04)."""
    path = repo_root / HUMAN_ACTORS_RELPATH
    if not path.is_file():
        return None
    allow = HumanActorsAllowlist(source_path=str(path.relative_to(repo_root)))
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        if cells[0].lower().startswith("canonical"):
            in_table = True
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if not in_table:
            # Tolerate tables without a recognized header: skip.
            continue
        canonical = cells[0].strip("`").strip()
        if not canonical:
            continue
        allow.canonical_names.append(canonical)
        allow.aliases[canonical] = canonical
        if len(cells) >= 3:
            for alias in re.findall(r"`([^`]+)`", cells[2]):
                allow.aliases[alias.strip()] = canonical
        if len(cells) >= 4:
            for alias in re.findall(r"`([^`]+)`", cells[3]):
                allow.aliases[alias.strip()] = canonical
    if not allow.canonical_names:
        return None
    return allow


def identity_refusal_message(detail: str) -> str:
    return (
        "REFUSAL (exit 2, D-GOV-04): an identity-dependent check could not "
        "attribute a human actor against the owner-curated allowlist "
        f"({HUMAN_ACTORS_RELPATH}). {detail} Refusing rather than guessing: "
        "misclassifying a human as an agent would false-block (D-GOV-04)."
    )


# --- Claim-language guard ------------------------------------------------------

# Forbidden claim vocabulary (constraint: no harness output may CLAIM these
# statuses except when quoting a labeled human-authored source).
FORBIDDEN_CLAIM_WORDS: list[str] = [
    "approved",
    "issued",
    "professionally accepted",
    "certified",
    "sealed",
    "safe",
    "ready for construction",
    "closed",
]

# Allowlisted quoting/technical contexts inside harness templates.
_CLAIM_ALLOWED_PHRASES = (
    "safe to delete",   # pinned generated-view header wording (D-GOV-01)
)


def find_claim_language(text: str) -> list[str]:
    """Return forbidden claim words present in `text` as lowercase-claim usage.

    All-uppercase tokens (state-vocabulary data values such as ISSUED/CLOSED)
    and allowlisted phrases are permitted; this lints templates, not data.
    """
    scrubbed = text
    for phrase in _CLAIM_ALLOWED_PHRASES:
        scrubbed = re.sub(re.escape(phrase), " ", scrubbed, flags=re.IGNORECASE)
    hits: list[str] = []
    for word in FORBIDDEN_CLAIM_WORDS:
        for m in re.finditer(r"(?<![A-Za-z_])" + re.escape(word) + r"(?![A-Za-z_])",
                             scrubbed, flags=re.IGNORECASE):
            token = m.group(0)
            if token.isupper():
                continue  # state token as data value
            hits.append(word)
            break
    return hits


# --- Report assembly -----------------------------------------------------------

MD_HEADER_TEMPLATE = (
    "> **Generated view — not authority.** Produced by tools/practitioner_harness "
    "(command: {cmd}).\n"
    "> Sources cited per finding; on any disagreement the cited source files govern.\n"
    "> Regenerate from project files; safe to delete. Structural checks are not approval,\n"
    "> issue, authentication, or acceptance of residual risk (K-AUTH-1; D-GOV-01).\n"
)

DISCLAIMER_TEMPLATE = (
    "Generated view — not authority. Produced by tools/practitioner_harness "
    "(command: {cmd}). Sources cited per finding; on any disagreement the cited "
    "source files govern. Regenerate from project files; safe to delete. "
    "Structural checks are not approval, issue, authentication, or acceptance "
    "of residual risk (K-AUTH-1; D-GOV-01)."
)

TEMPLATES: list[str] = [MD_HEADER_TEMPLATE, DISCLAIMER_TEMPLATE]


@dataclass
class Report:
    command: str
    findings: list[Finding] = field(default_factory=list)
    facts: list[SourcedFact] = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    extras: dict = field(default_factory=dict)
    markdown_body: list[str] = field(default_factory=list)

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)

    def add_fact(self, fact: SourcedFact) -> None:
        self.facts.append(fact)

    def md(self, line: str = "") -> None:
        self.markdown_body.append(line)

    def severity_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in self.findings:
            counts[f.severity.value] = counts.get(f.severity.value, 0) + 1
        return counts

    def render_markdown(self) -> str:
        out: list[str] = [MD_HEADER_TEMPLATE.format(cmd=self.command)]
        out.extend(self.markdown_body)
        if self.findings:
            out.append("")
            out.append("## Findings")
            out.append("")
            out.append("| Severity | Code | Dimension | Source | Invariant (ratification) | Message |")
            out.append("|---|---|---|---|---|---|")
            for f in self.findings:
                loc = f.source_path + (f":{f.source_line}" if f.source_line else "")
                inv = f"{f.invariant} ({f.invariant_ratification})" if f.invariant else "-"
                msg = f.message.replace("|", "\\|")
                if f.caveat:
                    msg += " [caveat: " + f.caveat.replace("|", "\\|") + "]"
                out.append(f"| {f.severity.value} | {f.code} | {f.dimension} | `{loc}` | {inv} | {msg} |")
        counts = self.severity_counts()
        out.append("")
        out.append("## Summary")
        out.append("")
        if counts:
            out.append("Finding severities: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        else:
            out.append("Finding severities: none")
        for key, val in self.summary.items():
            out.append(f"- {key}: {val}")
        out.append("")
        return "\n".join(out)

    def to_json_dict(self) -> dict:
        return {
            "schema": REPORT_SCHEMA,
            "tool": TOOL_NAME,
            "command": self.command,
            "authority_class": "generated_view",
            "contract_source": CONTRACT_SOURCE,
            "generated_at": _dt.date.today().isoformat(),
            "disclaimer": DISCLAIMER_TEMPLATE.format(cmd=self.command),
            "ratification_labels": ratification_labels_map(),
            "findings": [f.to_dict() for f in self.findings],
            "facts": [f.to_dict() for f in self.facts],
            "summary": {**self.summary, "severity_counts": self.severity_counts()},
            **self.extras,
        }

    def write_json(self, path: Path | str, repo_root: Path) -> Path:
        text = json.dumps(self.to_json_dict(), indent=2, sort_keys=False) + "\n"
        return write_generated_file(path, text, repo_root)


def emit(report: Report, repo_root: Path, json_report: str | None, strict: bool) -> int:
    """Print the Markdown report to stdout, optionally write the JSON report
    (contained to the generated root), and return the exit code."""
    sys.stdout.write(report.render_markdown())
    if json_report:
        report.write_json(json_report, repo_root)
    return compute_exit_code(report.findings, strict=strict)
