#!/usr/bin/env python3
"""Shared parsers and production-format contracts for Scope-of-Work tools."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SCHEMA = "chirality-deliverable-sow/v1"
LEGACY_FILES = ("Datasheet.md", "Specification.md", "Procedure.md", "Guidance.md")
REQUIRED_HEADINGS = (
    "Purpose and Objective Traceability",
    "Deliverable Definition — Ontology",
    "Completion and Reliance Basis — Epistemology",
    "Production and Verification Method — Praxeology",
    "Governing Values and Decisions — Axiology",
    "Output and Evaluation Matrix",
)
REQUIRED_FRONTMATTER = (
    "schema",
    "deliverable_id",
    "package_id",
    "decomposition_basis",
    "project_scope_refs",
    "package_objective_refs",
)
MATRIX_COLUMNS = (
    "Output",
    "Objective refs",
    "Requirement/claim refs",
    "Acceptance refs",
    "Verification refs",
    "Evidence expectation",
)
BEGIN_RE = re.compile(r"^<!-- sow-source-begin (\{.*\}) -->$")
END_MARKER = "<!-- sow-source-end -->"
MIGRATION_AUTHORITY = "D-GOV-16@7584718aa32b112e415331736d1a8e68c12ac176"
# Retain the imported name for callers while narrowing it to the exact ruled
# authority. A syntactically valid but unruled D-GOV-16 token is unauthorized.
MIGRATION_AUTHORITY_RE = re.compile(re.escape(MIGRATION_AUTHORITY))
MIGRATION_MARKER_PREFIX = "<!-- migration-authority: "
ACCEPTED_FORMATS = ("SOW_V1", "LEGACY_FOUR_DOC")
PRODUCTION_FORMATS = (*ACCEPTED_FORMATS, "MIGRATION_DUAL", "AMBIGUOUS", "INVALID")


class SowError(ValueError):
    """Raised for deterministic contract failures."""


@dataclass(frozen=True)
class Catalog:
    width: int
    definitions: dict[str, str]
    dispositions: tuple[str, ...]

    @property
    def local_re(self) -> re.Pattern[str]:
        prefixes = "|".join(re.escape(key) for key in self.definitions)
        return re.compile(rf"\b(?:{prefixes})-\d{{{self.width}}}\b")

    @property
    def definition_re(self) -> re.Pattern[str]:
        prefixes = "|".join(re.escape(key) for key in self.definitions)
        return re.compile(
            rf"^(?:[-*]\s+\*\*|#{{3,6}}\s+)(?P<id>(?:{prefixes})-\d{{{self.width}}})(?:\*\*)?\s+[—-]\s+",
            re.MULTILINE,
        )


@dataclass(frozen=True)
class SowDocument:
    path: Path
    raw: str
    frontmatter: dict[str, object]
    body: str
    definitions: tuple[str, ...]
    references: tuple[str, ...]

    @property
    def sha256(self) -> str:
        return sha256_bytes(self.raw.encode("utf-8"))


@dataclass(frozen=True)
class FormatResolution:
    """Fail-closed resolution of one PROJECT/SOFTWARE production contract."""

    state: str
    issues: tuple[str, ...]
    legacy_files: tuple[str, ...]
    has_scope_of_work: bool

    @property
    def valid(self) -> bool:
        return self.state in (*ACCEPTED_FORMATS, "MIGRATION_DUAL") and not self.issues

    @property
    def selected_files(self) -> tuple[str, ...]:
        if self.state == "LEGACY_FOUR_DOC":
            return LEGACY_FILES
        if self.state in {"SOW_V1", "MIGRATION_DUAL"}:
            return ("ScopeOfWork.md",)
        return ()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_catalog(path: Path | None = None) -> Catalog:
    target = path or Path(__file__).with_name("id_catalog.json")
    try:
        raw = json.loads(target.read_text(encoding="utf-8"))
        width = int(raw["width"])
        definitions = dict(raw["definitions"])
        dispositions = tuple(raw["migration_dispositions"])
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SowError(f"invalid ID catalog {target}: {exc}") from exc
    if width < 1 or not definitions or any(not re.fullmatch(r"[A-Z]+", key) for key in definitions):
        raise SowError(f"invalid ID catalog membership or width: {target}")
    return Catalog(width, definitions, dispositions)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        raise SowError(f"expected inline list, got: {value}")
    inner = value[1:-1].strip()
    if not inner:
        return []
    items = []
    for item in inner.split(","):
        clean = item.strip().strip("\"'")
        if not clean:
            raise SowError(f"empty inline-list member: {value}")
        items.append(clean)
    return items


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise SowError("ScopeOfWork.md must begin with --- frontmatter")
    end = next((index for index, line in enumerate(lines[1:], 1) if line.rstrip("\r\n") == "---"), None)
    if end is None:
        raise SowError("frontmatter is missing closing ---")
    values: dict[str, object] = {}
    for number, line in enumerate(lines[1:end], 2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise SowError(f"unsupported frontmatter syntax at line {number}")
        key, value = stripped.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in values:
            raise SowError(f"duplicate frontmatter key: {key}")
        values[key] = parse_inline_list(value) if value.startswith("[") else value.strip("\"'")
    return values, "".join(lines[end + 1 :])


def parse_sow_text(path: Path, raw: str, catalog: Catalog | None = None) -> SowDocument:
    catalog = catalog or load_catalog()
    frontmatter, body = parse_frontmatter(raw)
    contract_body = re.sub(
        r"^<!-- sow-source-begin \{[^\n]*\} -->$.*?^<!-- sow-source-end -->$",
        "",
        body,
        flags=re.MULTILINE | re.DOTALL,
    )
    # Blockquotes in a finalized converted contract preserve literal legacy
    # source. They are readable contract context, not SOW_V1 local-ID syntax.
    contract_body = "\n".join(
        "" if re.match(r"^ {0,3}>", line) else line for line in contract_body.splitlines()
    )
    definitions = tuple(match.group("id") for match in catalog.definition_re.finditer(contract_body))
    references = tuple(catalog.local_re.findall(contract_body))
    return SowDocument(path, raw, frontmatter, body, definitions, references)


def parse_sow(path: Path, catalog: Catalog | None = None) -> SowDocument:
    return parse_sow_text(path, path.read_text(encoding="utf-8"), catalog)


def heading_positions(body: str) -> list[tuple[str, int]]:
    return [(match.group(1).strip(), match.start()) for match in re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE)]


def section_text(body: str, heading: str) -> str:
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE))
    for index, match in enumerate(matches):
        if match.group(1).strip() == heading:
            end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
            return body[match.end() : end]
    return ""


def validate_document(doc: SowDocument, catalog: Catalog | None = None) -> list[str]:
    catalog = catalog or load_catalog()
    issues: list[str] = []
    for key in REQUIRED_FRONTMATTER:
        if key not in doc.frontmatter or doc.frontmatter[key] in ("", []):
            issues.append(f"missing or empty frontmatter field: {key}")
    if doc.frontmatter.get("schema") != SCHEMA:
        issues.append(f"schema must equal {SCHEMA}")
    deliverable_id = str(doc.frontmatter.get("deliverable_id", ""))
    package_id = str(doc.frontmatter.get("package_id", ""))
    if not re.fullmatch(r"DEL-\d{2,3}-\d{2,3}", deliverable_id):
        issues.append("deliverable_id must match DEL-<2-or-3 digits>-<2-or-3 digits>")
    if not re.fullmatch(r"PKG-\d{2,3}", package_id):
        issues.append("package_id must match PKG-<2-or-3 digits>")
    if "@" not in str(doc.frontmatter.get("decomposition_basis", "")):
        issues.append("decomposition_basis must bind a path and revision with @")

    headings = [name for name, _ in heading_positions(doc.body)]
    found = [heading for heading in headings if heading in REQUIRED_HEADINGS]
    if found != list(REQUIRED_HEADINGS):
        issues.append("required level-two headings are missing, duplicated, or out of order")

    duplicates = sorted({item for item in doc.definitions if doc.definitions.count(item) > 1})
    if duplicates:
        issues.append("duplicate local definitions: " + ", ".join(duplicates))
    defined = set(doc.definitions)
    if any(item.startswith("REM-") for item in defined):
        issues.append("REM-* definitions belong in _STATUS.md, not ScopeOfWork.md")
    unresolved = sorted(set(doc.references) - defined)
    if unresolved:
        issues.append("unresolved local references: " + ", ".join(unresolved))
    for prefix in ("OUT", "AC"):
        if not any(item.startswith(prefix + "-") for item in defined):
            issues.append(f"at least one {prefix}-* definition is required")

    matrix = section_text(doc.body, "Output and Evaluation Matrix")
    header = next((line for line in matrix.splitlines() if line.strip().startswith("|")), "")
    columns = tuple(cell.strip() for cell in header.strip().strip("|").split("|")) if header else ()
    if columns != MATRIX_COLUMNS:
        issues.append("output/evaluation matrix has missing or noncanonical columns")

    objective_refs = set(doc.frontmatter.get("project_scope_refs", [])) | set(
        doc.frontmatter.get("package_objective_refs", [])
    )
    mapped_outputs: set[str] = set()
    mapped_acceptance: set[str] = set()
    mapped_verification: set[str] = set()
    local_pattern = lambda prefix: rf"{re.escape(prefix)}-\d{{{catalog.width}}}"
    for line in matrix.splitlines():
        if not line.strip().startswith("|") or re.match(r"^\s*\|?\s*:?-", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(local_pattern("OUT"), cells[0]):
            mapped_outputs.add(cells[0])
            if cells[0] not in defined:
                issues.append(f"matrix output is not defined: {cells[0]}")
            if len(cells) < 5 or not objective_refs.intersection(cells[1].replace(",", " ").split()):
                issues.append(f"matrix output lacks declared objective reference: {cells[0]}")
            ac_refs = set(re.findall(local_pattern("AC"), cells[3] if len(cells) > 3 else ""))
            ver_refs = set(re.findall(local_pattern("VER"), cells[4] if len(cells) > 4 else ""))
            mapped_acceptance.update(ac_refs)
            mapped_verification.update(ver_refs)
            human_review = bool(re.fullmatch(r"HUMAN_REVIEW:\s*\S(?:.*\S)?", cells[4] if len(cells) > 4 else ""))
            if not ac_refs or (not ver_refs and not human_review):
                issues.append(f"matrix output lacks acceptance or verification reference: {cells[0]}")
    missing_outputs = sorted(item for item in defined if item.startswith("OUT-") and item not in mapped_outputs)
    missing_acceptance = sorted(item for item in defined if item.startswith("AC-") and item not in mapped_acceptance)
    missing_verification = sorted(item for item in defined if item.startswith("VER-") and item not in mapped_verification)
    if missing_outputs:
        issues.append("defined outputs missing from matrix: " + ", ".join(missing_outputs))
    if missing_acceptance:
        issues.append("defined acceptance criteria missing from matrix: " + ", ".join(missing_acceptance))
    if missing_verification:
        issues.append("defined verification methods missing from matrix: " + ", ".join(missing_verification))
    return issues


def read_lifecycle_state(deliverable: Path) -> str | None:
    status = deliverable / "_STATUS.md"
    if not status.is_file():
        return None
    text = status.read_text(encoding="utf-8", errors="replace")
    patterns = (
        r"(?im)^\s*\*\*Current State:\*\*\s*`?([A-Z_]+)`?\s*$",
        r"(?im)^\s*(?:Lifecycle\s+)?State\s*:\s*`?([A-Z_]+)`?\s*$",
        r"(?im)^\s*-\s*(?:Lifecycle\s+)?State\s*:\s*`?([A-Z_]+)`?\s*$",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def migration_marker(authority: str) -> str:
    return f"{MIGRATION_MARKER_PREFIX}{authority} -->"


def resolve_production_format(
    deliverable: Path,
    *,
    isolated_migration: bool = False,
    migration_authority: str = "",
) -> FormatResolution:
    """Resolve and validate the production format for one deliverable.

    Dual format is authorized only when both an isolated-workspace assertion
    and an exact D-GOV-16 authority reference are supplied, and the validated
    ScopeOfWork.md binds that same authority. Accepted baselines therefore
    resolve dual content to AMBIGUOUS by default.
    """

    deliverable = Path(deliverable)
    legacy = tuple(name for name in LEGACY_FILES if (deliverable / name).is_file())
    sow_path = deliverable / "ScopeOfWork.md"
    has_sow = sow_path.is_file()
    complete_legacy = len(legacy) == len(LEGACY_FILES)
    partial_legacy = bool(legacy) and not complete_legacy
    issues: list[str] = []
    sow_doc: SowDocument | None = None

    if has_sow:
        try:
            sow_doc = parse_sow(sow_path)
            issues.extend(validate_document(sow_doc))
        except (OSError, UnicodeError, SowError) as exc:
            issues.append(f"invalid ScopeOfWork.md: {exc}")

    if partial_legacy:
        missing = [name for name in LEGACY_FILES if name not in legacy]
        issues.insert(0, "partial legacy production kit; missing: " + ", ".join(missing))
        return FormatResolution("INVALID", tuple(issues), legacy, has_sow)

    if complete_legacy and has_sow:
        if issues:
            return FormatResolution("INVALID", tuple(issues), legacy, has_sow)
        authority = migration_authority
        authority_valid = authority == MIGRATION_AUTHORITY
        marker_valid = sow_doc is not None and migration_marker(authority) in sow_doc.body
        if isolated_migration and authority_valid and marker_valid:
            return FormatResolution("MIGRATION_DUAL", (), legacy, has_sow)
        dual_issues = ["dual production formats require an isolated conversion workspace and exact migration authority"]
        if migration_authority and not authority_valid:
            dual_issues.append(f"migration authority must equal {MIGRATION_AUTHORITY}")
        if isolated_migration and authority_valid and not marker_valid:
            dual_issues.append("ScopeOfWork.md does not bind the supplied migration authority")
        return FormatResolution("AMBIGUOUS", tuple(dual_issues), legacy, has_sow)

    if complete_legacy:
        return FormatResolution("LEGACY_FOUR_DOC", (), legacy, has_sow)
    if has_sow:
        if issues:
            return FormatResolution("INVALID", tuple(issues), legacy, has_sow)
        return FormatResolution("SOW_V1", (), legacy, has_sow)
    return FormatResolution("INVALID", ("missing production contract",), legacy, has_sow)


def require_requested_format(resolution: FormatResolution, requested: str) -> FormatResolution:
    """Fail closed when a caller's declared format disagrees with resolution."""

    if requested != "AUTO" and requested != resolution.state:
        raise SowError(f"requested production format {requested} resolves as {resolution.state}")
    return resolution


def resolve_format(
    deliverable: Path,
    isolated_migration: bool = False,
    migration_authority: str = "",
) -> str:
    """Compatibility wrapper returning only the fail-closed state string."""

    return resolve_production_format(
        deliverable,
        isolated_migration=isolated_migration,
        migration_authority=migration_authority,
    ).state


def split_source_sections(text: str) -> list[tuple[int, int, str, str]]:
    """Return inclusive line ranges, heading, and content, preserving all source lines."""
    lines = text.splitlines()
    heading_indexes = [i for i, line in enumerate(lines) if re.match(r"^#{1,6}\s+", line)]
    if not heading_indexes:
        return [(1, len(lines), "Unsectioned source", text)]
    sections: list[tuple[int, int, str, str]] = []
    if heading_indexes[0] > 0:
        sections.append((1, heading_indexes[0], "Source preamble", "\n".join(lines[: heading_indexes[0]])))
    for position, start in enumerate(heading_indexes):
        end = heading_indexes[position + 1] if position + 1 < len(heading_indexes) else len(lines)
        heading = re.sub(r"^#{1,6}\s+", "", lines[start]).strip()
        sections.append((start + 1, end, heading, "\n".join(lines[start:end])))
    return sections


def demote_headings(text: str, minimum_level: int = 4) -> str:
    def replace(match: re.Match[str]) -> str:
        level = max(minimum_level, min(6, len(match.group(1)) + 3))
        return "#" * level + " "
    return re.sub(r"^(#{1,6})\s+", replace, text, flags=re.MULTILINE)


def iter_source_blocks(body: str) -> Iterable[tuple[dict[str, object], str]]:
    lines = body.splitlines()
    index = 0
    while index < len(lines):
        match = BEGIN_RE.match(lines[index])
        if not match:
            index += 1
            continue
        try:
            metadata = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise SowError(f"invalid source marker JSON at body line {index + 1}") from exc
        end = index + 1
        while end < len(lines) and lines[end] != END_MARKER:
            end += 1
        if end == len(lines):
            raise SowError(f"unterminated source marker at body line {index + 1}")
        yield metadata, "\n".join(lines[index + 1 : end])
        index = end + 1
