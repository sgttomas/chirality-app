#!/usr/bin/env python3
"""Validate the D-48 / DEC-081 chirality-piping claims-language taxonomy.

The tool is read-only. Exit 0 means the scanned surfaces conform to the
governed claims registry (`projects/chirality-piping/docs/claims_registry.md`),
exit 1 means one or more findings, and exit 2 means an operational/input
failure. Conformance is deterministic lint evidence only; it creates no
lifecycle, release-readiness, professional-approval, certification, sealing,
authentication, or code-compliance claim.

Checks:
  1. AD_HOC_CLAIMS_LITANY — a scanned line carries three or more distinct
     litany-vocabulary terms (or "not authoritative"-family phrasing) without
     matching a registered boundary-statement text.
  2. Anchor presence — the PRD section 19.3 notice fragment, the BS-MATURITY
     app-shell banner, and the report-renderer notice fragment exist on their
     named surfaces (MISSING_PRD_NOTICE / MISSING_MATURITY_BANNER /
     MISSING_RENDERER_NOTICE).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_RELPATH = Path("projects/chirality-piping")

# Litany vocabulary (matched case-insensitively as substrings). A line with
# >= LITANY_THRESHOLD distinct terms is an ad-hoc prohibition litany unless it
# carries a registered text.
LITANY_TERMS = (
    "certif",
    "seal",
    "authenticat",
    "code-compliance",
    "code compliance",
    "professional",
    "approval",
    "approve",
    "endorse",
    "release-readiness",
    "production-readiness",
)
LITANY_THRESHOLD = 3

RETIRED_PHRASE = "not authoritative"

# Registered boundary-statement texts, copied verbatim (whitespace unwrapped)
# from docs/claims_registry.md section 1, plus the PRD section 19.3 notice
# fragment. Lines carrying one of these — or whose own content is a wrapped
# contiguous chunk (>= SUPPRESSION_WINDOW characters) of one, for multi-line
# statements — are registry usage, not ad-hoc litany.
REGISTERED_TEXTS = (
    # BS-IP canonical + short variants
    "OpenPipeStress ships no protected standards content. All code-specific "
    "values, tables, allowables, and factors are supplied by the user or "
    "user-controlled private sources, with provenance recorded.",
    "no protected standards content; code-specific data is user-supplied",
    "user-supplied data with recorded provenance; no protected standards "
    "content",
    # BS-ACCEPT canonical + short variants
    "Results are engineering decision-support information. Acceptance, "
    "professional judgment, and any certification, sealing, or "
    "code-compliance determination remain with the responsible engineer and "
    "project authority.",
    "Acceptance, professional judgment, and any certification, sealing, or "
    "code-compliance determination remain with the responsible engineer and "
    "project authority.",
    "acceptance and professional judgment remain with the responsible "
    "engineer",
    "human review remains required; acceptance stays with the responsible "
    "engineer",
    "decision-support information for review by the responsible engineer",
    # BS-VALID canonical + short variants
    "Candidate designs are validated in the user's accepted professional "
    "tools (external-prover correlation, PRD §22.5). Internal benchmarks "
    "and rule checks are development verification and screening evidence.",
    "validation occurs in the user's accepted professional tools; this "
    "package is screening and handoff evidence",
    "handoff evidence for external validation, not a validation outcome",
    # BS-MATURITY canonical
    "Technical preview — not a released product.",
    # GF-TOKEN canonical
    "Standard claim fence applies (F-PIP-2; claims taxonomy per DEC-081).",
    # PRD section 19.3 report-notice fragment
    "does not certify, seal, approve, authenticate, or determine code "
    "compliance",
)
SUPPRESSION_WINDOW = 15

# Anchor surfaces: (finding code, project-relative path, required fragment).
ANCHORS = (
    (
        "MISSING_PRD_NOTICE",
        "docs/PRD.md",
        "does not certify, seal, approve, authenticate, or determine code "
        "compliance for professional reliance",
    ),
    (
        "MISSING_MATURITY_BANNER",
        "apps/desktop/src/App.tsx",
        "Technical preview — not a released product.",
    ),
    (
        "MISSING_RENDERER_NOTICE",
        "core/reporting/report_renderer/src/lib.rs",
        "decision-support software",
    ),
)

# Top-level docs/ entries excluded from the litany scan (registry authorities
# and ruled/history surfaces per claims_registry.md section 5).
DOC_EXCLUDED_FILES = frozenset({
    "PRD.md",
    "claims_registry.md",
    "PROFESSIONAL_BOUNDARY.md",
    "IP_AND_DATA_BOUNDARY.md",
    "CONTRACT.md",
    "report_notice_template.md",
    "PLAN.md",
})
DOC_EXCLUDED_DIRS = frozenset({"_history", "_ScopeChange"})
DOC_EXCLUDED_RELPATHS = frozenset({"security/threat_model.md"})
DOC_EXCLUDED_PREFIX = "governance"

# DEC-081 two-wave activation. Wave 1 aligns product surfaces (desktop UI,
# the named user-facing docs). Wave 2 extends the scan to the live
# ScopeOfWork.md surfaces and the remaining docs (spec/governance-adjacent
# pages) after their alignment lands. Flipped to True with the D-48 Wave-2
# tranche (2026-07-16): the full live doc tree and all live ScopeOfWork.md
# files are now in scope.
WAVE2_SURFACES_ACTIVE = True

# Docs scanned during Wave 1 (relative to projects/chirality-piping/docs/).
# Retained for the gate's False mode (exercised in tests only).
WAVE1_DOC_RELPATHS = frozenset({
    "README.md",
    "BUILD_AND_RELEASE.md",
    "RELEASE_NOTES_TEMPLATE.md",
    "user_guide/index.md",
    "validation_manual/index.md",
    "validation_manual/headless_runner_reproduction.md",
})

# A litany-shaped line that explicitly cites the PRD prohibited-claims
# authority is a rule statement, not an ad-hoc hedge (registry section 3).
AUTHORITY_CITATION_MARKERS = ("§21.2", "section 21.2")

# Detection-vocabulary definitions inside lint/enforcement code are quoted
# patterns, not boundary prose.
ENFORCEMENT_VOCAB_MARKERS = ("software certifies",)


@dataclass(frozen=True)
class Finding:
    code: str
    path: str  # repo-root-relative, posix
    line: int | None
    message: str


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


_NORMALIZED_REGISTERED = tuple(_normalize(t) for t in REGISTERED_TEXTS)


def _strip_decoration(normalized_line: str) -> str:
    """Drop quoting/markup decoration so a wrapped chunk of a registered
    statement compares against the registered text itself."""
    return re.sub(r"^[^a-z0-9]+|[^a-z0-9]+$", "", normalized_line)


def _carries_registered_text(normalized_line: str) -> bool:
    for text in _NORMALIZED_REGISTERED:
        if text in normalized_line:
            return True
    # Wrapped multi-line statement: the line's own content (decoration
    # stripped) is >= SUPPRESSION_WINDOW consecutive characters of a
    # registered text.
    core = _strip_decoration(normalized_line)
    if len(core) < SUPPRESSION_WINDOW:
        return False
    return any(core in text for text in _NORMALIZED_REGISTERED)


def _litany_terms_on(normalized_line: str) -> list[str]:
    return [term for term in LITANY_TERMS if term in normalized_line]


def _iter_desktop_sources(project_root: Path) -> list[Path]:
    src = project_root / "apps" / "desktop" / "src"
    if not src.is_dir():
        return []
    return [
        p
        for p in src.rglob("*")
        if p.is_file()
        and p.suffix in {".ts", ".tsx"}
        and ".test." not in p.name
    ]


def _doc_excluded(rel_to_docs: Path) -> bool:
    posix = rel_to_docs.as_posix()
    if posix in DOC_EXCLUDED_RELPATHS:
        return True
    parts = rel_to_docs.parts
    if len(parts) == 1 and parts[0] in DOC_EXCLUDED_FILES:
        return True
    if parts[0] in DOC_EXCLUDED_DIRS:
        return True
    if parts[0].startswith(DOC_EXCLUDED_PREFIX):
        return True
    return False


def _iter_docs(project_root: Path) -> list[Path]:
    docs = project_root / "docs"
    if not docs.is_dir():
        return []
    candidates = [
        p
        for p in docs.rglob("*.md")
        if p.is_file() and not _doc_excluded(p.relative_to(docs))
    ]
    if WAVE2_SURFACES_ACTIVE:
        return candidates
    return [
        p
        for p in candidates
        if p.relative_to(docs).as_posix() in WAVE1_DOC_RELPATHS
    ]


def _iter_scopes_of_work(project_root: Path) -> list[Path]:
    if not WAVE2_SURFACES_ACTIVE:
        return []
    return [
        p
        for p in project_root.glob(
            "execution/PKG-*/1_Working/DEL-*/ScopeOfWork.md"
        )
        if p.is_file()
    ]


def iter_scanned_files(repo_root: Path) -> list[Path]:
    project_root = repo_root / PROJECT_RELPATH
    files = (
        _iter_desktop_sources(project_root)
        + _iter_docs(project_root)
        + _iter_scopes_of_work(project_root)
    )
    return sorted(set(files))


def _scan_file(path: Path, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line_no, line in enumerate(text.splitlines(), start=1):
        normalized = _normalize(line)
        if not normalized:
            continue
        terms = _litany_terms_on(normalized)
        if (
            len(terms) >= LITANY_THRESHOLD
            and not _carries_registered_text(normalized)
            and not any(m in normalized for m in AUTHORITY_CITATION_MARKERS)
            and not any(m in normalized for m in ENFORCEMENT_VOCAB_MARKERS)
        ):
            findings.append(Finding(
                "AD_HOC_CLAIMS_LITANY", rel, line_no,
                "ad-hoc prohibition litany ("
                + ", ".join(terms)
                + ") without a registered boundary statement; use the "
                "applicable docs/claims_registry.md text (DEC-081)",
            ))
        if RETIRED_PHRASE in normalized:
            findings.append(Finding(
                "AD_HOC_CLAIMS_LITANY", rel, line_no,
                '"not authoritative"-family phrasing is retired on this '
                "surface; use BS-ACCEPT from docs/claims_registry.md "
                "(DEC-081)",
            ))
    return findings


def _check_anchors(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    project_root = repo_root / PROJECT_RELPATH
    for code, rel_path, fragment in ANCHORS:
        path = project_root / rel_path
        rel = (PROJECT_RELPATH / rel_path).as_posix()
        if not path.is_file():
            findings.append(Finding(
                code, rel, None,
                f"anchor surface is absent; it must carry \"{fragment}\" "
                "(DEC-081)",
            ))
            continue
        text = _normalize(
            path.read_text(encoding="utf-8", errors="replace")
        )
        if _normalize(fragment) not in text:
            findings.append(Finding(
                code, rel, None,
                f"required statement \"{fragment}\" not found on this "
                "anchor surface (DEC-081)",
            ))
    return findings


def validate_claims_language(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_scanned_files(repo_root):
        rel = path.relative_to(repo_root).as_posix()
        findings.extend(_scan_file(path, rel))
    findings.extend(_check_anchors(repo_root))
    return sorted(
        findings, key=lambda f: (f.path, f.line if f.line is not None else 0,
                                 f.code, f.message)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    try:
        repo_root = args.repo_root.resolve()
        project_root = repo_root / PROJECT_RELPATH
        if not project_root.is_dir():
            raise ValueError(
                f"project root does not exist: {project_root}"
            )
        scanned = iter_scanned_files(repo_root)
        findings = validate_claims_language(repo_root)
    except (OSError, ValueError) as exc:
        print(f"OPERATIONAL_ERROR: {exc}", file=sys.stderr)
        return 2

    if findings:
        for finding in findings:
            location = f":{finding.line}" if finding.line is not None else ""
            print(
                f"INVALID {finding.code} {finding.path}{location}: "
                f"{finding.message}"
            )
        return 1

    print(
        f"VALID claims-language surfaces: {len(scanned)} files scanned; "
        "DEC-081 registry taxonomy satisfied"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
