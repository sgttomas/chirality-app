#!/usr/bin/env python3
"""Validate decomposition companion registers for a project execution root.

Closes OI-013: there was no durable, deterministic validator for the
decomposition companion register family. `validate_dependencies_schema.py`
owns single-file v3.1 schema/enum conformance; `analyze_dep_closure.py` owns
graph topology and reports an *EvidenceFile-presence* metric only. Neither
tests evidence-cell quality, and neither tests the registers against each
other.

This tool is additive and report-only. It never mutates an input. It reuses
`validate_dependencies_schema.validate()` for schema conformance rather than
restating that contract.

Check families
--------------
SCH  Per-file v3.1 schema conformance (delegated).
EVQ  Evidence-cell quality: locus/quote confusion and empty-evidence rows,
     reported as distinct named sub-classes, row-class aware.
XRG  Cross-register consistency: Deliverables.csv <-> ScopeLedger.csv <->
     ContextBudgetQA.csv.
DRB  Dependency-register binding: Dependencies.csv <-> Deliverables.csv and
     the owning deliverable folder.

Metric naming (deliberate, per the analyze_dep_closure.py lesson)
-----------------------------------------------------------------
"Evidence-file coverage"    = EvidenceFile cell is populated.
"Evidence-file resolution"  = that path exists on disk.
"Evidence-locus quality"    = SourceRef is a locus, not a pasted quote.
"Evidence-quote coverage"   = EvidenceQuote carries verbatim source text.
These are four different measurements. Do not collapse them into one number.

Scan boundary
-------------
Deliverable-local registers are discovered under
`<EXECUTION_ROOT>/PKG-*/{1_Working,2_Checking,3_Issued}/DEL-*/Dependencies.csv`.
`0_References` is excluded (reference material, not deliverables), as is any
register held outside a package lifecycle folder. `EvidenceFile` is resolved as
a path relative to `--evidence-root` (default: the parent of EXECUTION_ROOT) and
must name a regular file; absolute paths are rejected rather than followed.

Honest-empty waivers
--------------------
A dependency can be real and still have no quotable source text. To keep exit 0
from becoming an incentive to invent a quote, a register may sit beside an
optional `Dependencies_EvidenceWaivers.csv` with columns
`DependencyID, WaivedCheck, Rationale, DeclaredBy, DeclaredOn`. Only `EVQ-003`
and `EVQ-004` are waivable. A valid waiver downgrades that row's finding to
WARNING and counts it under `waived`; it never hides the row. Waivers are
themselves checked: a stale one (`EVQ-007`), a thin or placeholder rationale
(`EVQ-008`), or a malformed/unknown entry (`EVQ-009`) is an ERROR. So exit 0
means every row either carries real evidence or carries a declared, attributed,
substantively-reasoned exception — never that the defects were papered over.

Usage
-----
    python3 tools/validation/validate_decomposition_registers.py <EXECUTION_ROOT> \
        [--json OUT.json] [--strict] [--max-per-code N] [--families SCH,EVQ,XRG,DRB]
    python3 tools/validation/validate_decomposition_registers.py --list-checks

Exit codes
----------
    0  clean (no ERROR findings; no WARNING findings under --strict)
    1  findings
    2  operational error (unreadable/absent required input, bad arguments)
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parent
if str(VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATION_DIR))

from validate_dependencies_schema import validate as validate_dep_schema  # noqa: E402

ERROR = "ERROR"
WARNING = "WARNING"

FAMILIES = ("SCH", "EVQ", "XRG", "DRB")

CHECKS: dict[str, tuple[str, str, str]] = {
    # code: (family, default severity, description)
    "SCH-001": ("SCH", ERROR, "Dependencies.csv fails the v3.1 schema/enum contract"),
    "EVQ-001": ("EVQ", ERROR, "Locus/quote duplication: SourceRef and EvidenceQuote hold identical non-empty text"),
    "EVQ-002": ("EVQ", WARNING, "Quote-shaped locus: SourceRef embeds a quoted span (locus column carrying quote text)"),
    "EVQ-003": ("EVQ", ERROR, "Empty-evidence row: EvidenceQuote is blank"),
    "EVQ-004": ("EVQ", ERROR, "Placeholder locus: SourceRef is blank or a placeholder token (e.g. 'location TBD')"),
    "EVQ-005": ("EVQ", ERROR, "EvidenceFile cell is blank"),
    "EVQ-006": ("EVQ", ERROR, "EvidenceFile path does not resolve on disk"),
    "EVQ-007": ("EVQ", ERROR, "Evidence waiver is stale: the row it waives now carries real evidence"),
    "EVQ-008": ("EVQ", ERROR, "Evidence waiver has a missing or placeholder Rationale"),
    "EVQ-009": ("EVQ", ERROR, "Evidence waiver is malformed, names an unknown DependencyID, or waives an unwaivable check"),
    "XRG-001": ("XRG", ERROR, "ScopeLedger DeliverableIDs names a deliverable absent from Deliverables.csv"),
    "XRG-002": ("XRG", ERROR, "Deliverables CoversScopeItems names a scope item absent from ScopeLedger.csv"),
    "XRG-003": ("XRG", ERROR, "Scope-coverage link is non-reciprocal between ScopeLedger.csv and Deliverables.csv"),
    "XRG-004": ("XRG", ERROR, "PackageID disagrees between ScopeLedger.csv and Deliverables.csv for a linked deliverable"),
    "XRG-005": ("XRG", ERROR, "Scope item's ObjectiveIDs are not propagated to the covering deliverable's SupportsObjectives"),
    "XRG-006": ("XRG", WARNING, "IN-scope ledger item has no DeliverableIDs"),
    "XRG-007": ("XRG", ERROR, "Non-IN ledger item carries DeliverableIDs"),
    "XRG-008": ("XRG", WARNING, "Deliverables.csv row has a blank PhaseHint"),
    "XRG-009": ("XRG", ERROR, "ContextBudgetQA.csv and Deliverables.csv cover different deliverable sets"),
    "XRG-010": ("XRG", ERROR, "ContextEnvelope disagrees between ContextBudgetQA.csv and Deliverables.csv"),
    "DRB-001": ("DRB", ERROR, "FromDeliverableID disagrees with the owning deliverable folder"),
    "DRB-002": ("DRB", ERROR, "FromDeliverableID is absent from Deliverables.csv"),
    "DRB-003": ("DRB", ERROR, "FromPackageID disagrees with Deliverables.csv"),
    "DRB-004": ("DRB", WARNING, "FromDeliverableName disagrees with Deliverables.csv Name"),
    "DRB-005": ("DRB", ERROR, "TargetDeliverableID is absent from Deliverables.csv"),
    "DRB-006": ("DRB", ERROR, "DependencyID prefix disagrees with FromDeliverableID"),
    "DRB-007": ("DRB", ERROR, "DependencyID is duplicated across the corpus"),
    "DRB-008": ("DRB", WARNING, "Deliverables.csv row has no deliverable-local Dependencies.csv in any scanned lifecycle folder"),
}

# A locus that is a placeholder rather than a citable location.
PLACEHOLDER_LOCUS = re.compile(
    r"^\s*(?:"
    r"location\s+tbd|tbd|to\s+be\s+determined|n/?a|none|unknown|pending|\?+|-+|\.+"
    r")\s*$",
    re.IGNORECASE,
)

# A quoted span inside the locus column: paired straight or curly double quotes
# with at least four characters between them (avoids matching stray inch marks).
QUOTE_SPAN = re.compile(r'"[^"]{4,}"|“[^”]{4,}”')

DEL_DIR = re.compile(r"^(DEL-\d{2}-\d{2})(?:[_-].*)?$")

# Honest-empty declaration. Some dependencies are genuinely real but have no
# quotable source text — the relation was reasoned from register truth rather
# than stated anywhere. Without a declared route for that case, a clean exit
# could only be reached by inventing a quote, which would make the gate an
# incentive to fabricate evidence. A waiver keeps such a row visible (it stays
# a WARNING and is counted separately), but lets a fully-dispositioned corpus
# reach exit 0 honestly.
WAIVER_FILENAME = "Dependencies_EvidenceWaivers.csv"
WAIVER_COLUMNS = ("DependencyID", "WaivedCheck", "Rationale", "DeclaredBy", "DeclaredOn")
WAIVABLE_CHECKS = ("EVQ-003", "EVQ-004")
MIN_RATIONALE_CHARS = 30

# Lifecycle folders that can hold a deliverable. A deliverable moves between
# these as it matures, so a scan limited to 1_Working silently stops seeing a
# register the moment the deliverable is promoted. 0_References holds reference
# material, not deliverables, and is deliberately excluded.
LIFECYCLE_DIRS = ("1_Working", "2_Checking", "3_Issued")


class OperationalError(Exception):
    """Input could not be read or the invocation is unusable."""


def split_list(value: str | None) -> list[str]:
    """Split a semicolon- or comma-delimited register cell into tokens."""
    return [token.strip() for token in re.split(r"[;,]", value or "") if token.strip()]


def read_register(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return [
                {(k or "").strip().lstrip("﻿"): (v or "") for k, v in row.items()}
                for row in csv.DictReader(handle)
            ]
    except FileNotFoundError as exc:
        raise OperationalError(f"register not found: {path}") from exc
    except (csv.Error, UnicodeDecodeError) as exc:
        raise OperationalError(f"register unreadable: {path}: {exc}") from exc
    except OSError as exc:
        # PermissionError, IsADirectoryError, and every other OS-level failure
        # are operational (exit 2), not register findings (exit 1).
        raise OperationalError(f"register unreadable: {path}: {exc}") from exc


class Finding:
    __slots__ = ("code", "family", "severity", "path", "line", "row_id", "row_class", "detail")

    def __init__(self, code, path, detail, line=None, row_id=None, row_class=None,
                 severity=None):
        family, default_severity, _ = CHECKS[code]
        self.code = code
        self.family = family
        self.severity = severity or default_severity
        self.path = path
        self.line = line
        self.row_id = row_id
        self.row_class = row_class
        self.detail = detail

    def as_dict(self) -> dict:
        return {
            "code": self.code,
            "family": self.family,
            "severity": self.severity,
            "path": self.path,
            "line": self.line,
            "row_id": self.row_id,
            "row_class": self.row_class,
            "detail": self.detail,
        }


def discover_dependency_files(execution_root: Path) -> list[tuple[Path, str | None]]:
    """Return (path, owning DEL id from folder name) for each deliverable-local register.

    Scans every lifecycle folder in LIFECYCLE_DIRS, not just 1_Working, so that a
    promoted deliverable's register does not silently drop out of the corpus.
    """
    found: list[tuple[Path, str | None]] = []
    for package_dir in sorted(execution_root.glob("PKG-*")):
        if not package_dir.is_dir():
            continue
        for lifecycle_name in LIFECYCLE_DIRS:
            lifecycle_dir = package_dir / lifecycle_name
            if not lifecycle_dir.is_dir():
                continue
            for deliverable_dir in sorted(lifecycle_dir.glob("DEL-*")):
                register = deliverable_dir / "Dependencies.csv"
                if register.is_file():
                    match = DEL_DIR.match(deliverable_dir.name)
                    found.append((register, match.group(1) if match else None))
    return found


def read_waivers(
    register_path: Path,
    known_ids: set[str],
    rel_path: str,
    findings: list[Finding],
) -> dict[tuple[str, str], dict[str, str]]:
    """Load and validate the optional honest-empty waiver sidecar.

    Returns {(DependencyID, WaivedCheck): row} for waivers that are themselves
    well-formed. A malformed waiver is a finding in its own right and never
    softens the row it claims to cover.
    """
    waiver_path = register_path.parent / WAIVER_FILENAME
    if not waiver_path.is_file():
        return {}

    waiver_rel = os.path.join(os.path.dirname(rel_path), WAIVER_FILENAME)
    rows = read_register(waiver_path)
    accepted: dict[tuple[str, str], dict[str, str]] = {}

    for offset, row in enumerate(rows, start=2):
        missing = [column for column in WAIVER_COLUMNS if column not in row]
        if missing:
            findings.append(
                Finding("EVQ-009", waiver_rel,
                        f"waiver sidecar is missing required column(s): {', '.join(missing)}",
                        line=offset)
            )
            continue

        dep_id = (row.get("DependencyID") or "").strip()
        check = (row.get("WaivedCheck") or "").strip().upper()
        rationale = (row.get("Rationale") or "").strip()
        declared_by = (row.get("DeclaredBy") or "").strip()
        declared_on = (row.get("DeclaredOn") or "").strip()

        if not dep_id or dep_id not in known_ids:
            findings.append(
                Finding("EVQ-009", waiver_rel,
                        f"waiver names DependencyID {dep_id!r}, which is not a row of "
                        f"{os.path.basename(rel_path)}", line=offset, row_id=dep_id or None)
            )
            continue
        if check not in WAIVABLE_CHECKS:
            findings.append(
                Finding("EVQ-009", waiver_rel,
                        f"WaivedCheck {check!r} is not waivable; only "
                        f"{', '.join(WAIVABLE_CHECKS)} may be waived",
                        line=offset, row_id=dep_id)
            )
            continue
        if not declared_by or not declared_on:
            findings.append(
                Finding("EVQ-009", waiver_rel,
                        "waiver must record both DeclaredBy and DeclaredOn",
                        line=offset, row_id=dep_id)
            )
            continue
        if (
            len(rationale) < MIN_RATIONALE_CHARS
            or PLACEHOLDER_LOCUS.match(rationale)
        ):
            findings.append(
                Finding("EVQ-008", waiver_rel,
                        f"Rationale must be a substantive statement of why no source text "
                        f"is quotable (at least {MIN_RATIONALE_CHARS} characters); "
                        f"found {rationale!r}", line=offset, row_id=dep_id)
            )
            continue

        accepted[(dep_id, check)] = row

    return accepted


def check_evidence_quality(
    rows: list[dict[str, str]],
    rel_path: str,
    evidence_root: Path,
    findings: list[Finding],
    counters: dict,
    waivers: dict[tuple[str, str], dict[str, str]] | None = None,
) -> None:
    """EVQ family — the two OI-013 sub-classes plus the file-cell metrics."""
    waivers = waivers or {}
    waivers_used: set[tuple[str, str]] = set()

    for offset, row in enumerate(rows, start=2):
        row_id = (row.get("DependencyID") or "").strip() or "<missing DependencyID>"
        row_class = (row.get("DependencyClass") or "").strip() or "<unclassed>"
        source_ref = (row.get("SourceRef") or "").strip()
        quote = (row.get("EvidenceQuote") or "").strip()
        evidence_file = (row.get("EvidenceFile") or "").strip()

        bucket = counters["by_class"].setdefault(
            row_class,
            {
                "rows": 0,
                "locus_quote_duplication": 0,
                "quote_shaped_locus": 0,
                "empty_evidence_quote": 0,
                "placeholder_locus": 0,
                "evidence_file_populated": 0,
                "evidence_file_resolved": 0,
                "well_formed_evidence": 0,
                "waived_rows": 0,
            },
        )
        bucket["rows"] += 1

        clean = True
        row_waived = False

        # (a) locus/quote confusion.
        if source_ref and quote and source_ref == quote:
            bucket["locus_quote_duplication"] += 1
            clean = False
            findings.append(
                Finding(
                    "EVQ-001",
                    rel_path,
                    "SourceRef and EvidenceQuote are byte-identical, so one column is "
                    "carrying the other's content; a locus names where evidence sits "
                    "and a quote reproduces it, and the two are never the same text "
                    f"({len(source_ref)} chars): {source_ref[:120]!r}",
                    line=offset,
                    row_id=row_id,
                    row_class=row_class,
                )
            )
        elif source_ref and QUOTE_SPAN.search(source_ref):
            bucket["quote_shaped_locus"] += 1
            clean = False
            findings.append(
                Finding(
                    "EVQ-002",
                    rel_path,
                    "SourceRef embeds a quoted span; a locus should name where the "
                    f"evidence sits, not restate it: {source_ref[:120]!r}",
                    line=offset,
                    row_id=row_id,
                    row_class=row_class,
                )
            )

        # (b) empty-evidence rows, reported distinctly from (a).
        if not quote:
            bucket["empty_evidence_quote"] += 1
            clean = False
            waiver = waivers.get((row_id, "EVQ-003"))
            if waiver:
                waivers_used.add((row_id, "EVQ-003"))
                row_waived = True
            findings.append(
                Finding(
                    "EVQ-003",
                    rel_path,
                    "EvidenceQuote is blank; the row asserts a dependency with no "
                    "quoted source text"
                    + (f" — WAIVED: {(waiver.get('Rationale') or '').strip()}" if waiver else ""),
                    line=offset,
                    row_id=row_id,
                    row_class=row_class,
                    severity=WARNING if waiver else None,
                )
            )
        if not source_ref or PLACEHOLDER_LOCUS.match(source_ref):
            bucket["placeholder_locus"] += 1
            clean = False
            waiver = waivers.get((row_id, "EVQ-004"))
            if waiver:
                waivers_used.add((row_id, "EVQ-004"))
                row_waived = True
            findings.append(
                Finding(
                    "EVQ-004",
                    rel_path,
                    f"SourceRef is a placeholder, not a citable locus: {source_ref!r}"
                    + (f" — WAIVED: {(waiver.get('Rationale') or '').strip()}" if waiver else ""),
                    line=offset,
                    row_id=row_id,
                    row_class=row_class,
                    severity=WARNING if waiver else None,
                )
            )

        # Evidence-file coverage and resolution — distinct metrics.
        if not evidence_file:
            clean = False
            findings.append(
                Finding("EVQ-005", rel_path, "EvidenceFile is blank", line=offset,
                        row_id=row_id, row_class=row_class)
            )
        else:
            bucket["evidence_file_populated"] += 1
            # An EvidenceFile must name a regular file reached from the declared
            # evidence root. A directory is not evidence, and an absolute path
            # would silently escape --evidence-root, so both are findings.
            candidate = Path(evidence_file)
            if candidate.is_absolute():
                clean = False
                findings.append(
                    Finding(
                        "EVQ-006",
                        rel_path,
                        "EvidenceFile is an absolute path; it must be relative to the "
                        f"evidence root ({evidence_root}): {evidence_file!r}",
                        line=offset,
                        row_id=row_id,
                        row_class=row_class,
                    )
                )
            elif (evidence_root / candidate).is_file():
                bucket["evidence_file_resolved"] += 1
            else:
                clean = False
                target = evidence_root / candidate
                reason = "is a directory, not a file" if target.is_dir() else "does not resolve"
                findings.append(
                    Finding(
                        "EVQ-006",
                        rel_path,
                        f"EvidenceFile {reason} under {evidence_root}: {evidence_file!r}",
                        line=offset,
                        row_id=row_id,
                        row_class=row_class,
                    )
                )

        if clean:
            bucket["well_formed_evidence"] += 1
        if row_waived:
            bucket["waived_rows"] += 1

    # A waiver that no longer covers a live defect is stale: the row was
    # repaired but the declaration was left behind, which would silently soften
    # a future regression.
    waiver_rel = os.path.join(os.path.dirname(rel_path), WAIVER_FILENAME)
    for (dep_id, check) in sorted(set(waivers) - waivers_used):
        findings.append(
            Finding("EVQ-007", waiver_rel,
                    f"waiver of {check} for {dep_id} is stale — that row now carries "
                    f"real evidence; remove the waiver", row_id=dep_id)
        )


def check_dependency_binding(
    rows: list[dict[str, str]],
    rel_path: str,
    folder_del_id: str | None,
    deliverables: dict[str, dict[str, str]],
    seen_ids: dict[str, str],
    findings: list[Finding],
) -> None:
    """DRB family — Dependencies.csv against Deliverables.csv and its own folder."""
    have_deliverables = bool(deliverables)
    for offset, row in enumerate(rows, start=2):
        row_id = (row.get("DependencyID") or "").strip() or "<missing DependencyID>"
        row_class = (row.get("DependencyClass") or "").strip() or None
        from_del = (row.get("FromDeliverableID") or "").strip()
        from_pkg = (row.get("FromPackageID") or "").strip()
        from_name = (row.get("FromDeliverableName") or "").strip()
        target_del = (row.get("TargetDeliverableID") or "").strip()

        if row_id != "<missing DependencyID>":
            prior = seen_ids.get(row_id)
            if prior:
                findings.append(
                    Finding("DRB-007", rel_path,
                            f"DependencyID also appears in {prior}",
                            line=offset, row_id=row_id, row_class=row_class)
                )
            else:
                seen_ids[row_id] = rel_path

        if folder_del_id and from_del and from_del != folder_del_id:
            findings.append(
                Finding("DRB-001", rel_path,
                        f"FromDeliverableID {from_del!r} but the register sits in {folder_del_id}",
                        line=offset, row_id=row_id, row_class=row_class)
            )

        if from_del and from_del.startswith("DEL-"):
            expected_prefix = "DEP-" + from_del[len("DEL-"):]
            if row_id != "<missing DependencyID>" and not row_id.startswith(expected_prefix):
                findings.append(
                    Finding("DRB-006", rel_path,
                            f"DependencyID does not start with {expected_prefix!r}",
                            line=offset, row_id=row_id, row_class=row_class)
                )

        if not have_deliverables:
            continue

        if from_del and from_del not in deliverables:
            findings.append(
                Finding("DRB-002", rel_path,
                        f"FromDeliverableID {from_del!r} is not a Deliverables.csv row",
                        line=offset, row_id=row_id, row_class=row_class)
            )
        elif from_del:
            record = deliverables[from_del]
            if from_pkg and from_pkg != record.get("PackageID", "").strip():
                findings.append(
                    Finding("DRB-003", rel_path,
                            f"FromPackageID {from_pkg!r} but Deliverables.csv says "
                            f"{record.get('PackageID', '').strip()!r}",
                            line=offset, row_id=row_id, row_class=row_class)
                )
            if from_name and from_name != record.get("Name", "").strip():
                findings.append(
                    Finding("DRB-004", rel_path,
                            f"FromDeliverableName {from_name!r} but Deliverables.csv says "
                            f"{record.get('Name', '').strip()!r}",
                            line=offset, row_id=row_id, row_class=row_class)
                )

        if target_del and target_del not in deliverables:
            findings.append(
                Finding("DRB-005", rel_path,
                        f"TargetDeliverableID {target_del!r} is not a Deliverables.csv row",
                        line=offset, row_id=row_id, row_class=row_class)
            )


def check_cross_register(
    deliverables: dict[str, dict[str, str]],
    ledger: list[dict[str, str]],
    context_qa: list[dict[str, str]] | None,
    paths: dict[str, str],
    findings: list[Finding],
) -> None:
    """XRG family — the companion registers against each other."""
    for item in ledger:
        item_id = (item.get("ScopeItemID") or "").strip()
        status = (item.get("InOutStatus") or "").strip().upper()
        linked = split_list(item.get("DeliverableIDs"))
        objectives = split_list(item.get("ObjectiveIDs"))
        ledger_pkg = (item.get("PackageID") or "").strip()

        if status == "IN" and not linked:
            findings.append(
                Finding("XRG-006", paths["ledger"],
                        f"IN-scope item {item_id} has no covering deliverable", row_id=item_id)
            )
        if status and status != "IN" and linked:
            findings.append(
                Finding("XRG-007", paths["ledger"],
                        f"{status} item {item_id} names deliverables {', '.join(linked)}",
                        row_id=item_id)
            )

        for deliverable_id in linked:
            record = deliverables.get(deliverable_id)
            if record is None:
                findings.append(
                    Finding("XRG-001", paths["ledger"],
                            f"{item_id} names deliverable {deliverable_id!r}, absent from "
                            f"{paths['deliverables']}", row_id=item_id)
                )
                continue
            covers = split_list(record.get("CoversScopeItems"))
            if item_id not in covers:
                findings.append(
                    Finding("XRG-003", paths["ledger"],
                            f"{item_id} names {deliverable_id}, but that deliverable's "
                            f"CoversScopeItems does not name {item_id}", row_id=item_id)
                )
            record_pkg = (record.get("PackageID") or "").strip()
            if ledger_pkg and record_pkg and ledger_pkg != record_pkg:
                findings.append(
                    Finding("XRG-004", paths["ledger"],
                            f"{item_id} declares PackageID {ledger_pkg!r} but {deliverable_id} "
                            f"is in {record_pkg!r}", row_id=item_id)
                )
            supports = split_list(record.get("SupportsObjectives"))
            for objective in objectives:
                if objective not in supports:
                    findings.append(
                        Finding("XRG-005", paths["ledger"],
                                f"{item_id} maps to {objective}, but covering deliverable "
                                f"{deliverable_id} does not support it", row_id=item_id)
                    )

    ledger_index = {(row.get("ScopeItemID") or "").strip(): row for row in ledger}
    for deliverable_id, record in deliverables.items():
        if not (record.get("PhaseHint") or "").strip():
            findings.append(
                Finding("XRG-008", paths["deliverables"],
                        f"{deliverable_id} has a blank PhaseHint", row_id=deliverable_id)
            )
        for item_id in split_list(record.get("CoversScopeItems")):
            item = ledger_index.get(item_id)
            if item is None:
                findings.append(
                    Finding("XRG-002", paths["deliverables"],
                            f"{deliverable_id} covers {item_id!r}, absent from {paths['ledger']}",
                            row_id=deliverable_id)
                )
            elif deliverable_id not in split_list(item.get("DeliverableIDs")):
                findings.append(
                    Finding("XRG-003", paths["deliverables"],
                            f"{deliverable_id} covers {item_id}, but that ledger row's "
                            f"DeliverableIDs does not name {deliverable_id}", row_id=deliverable_id)
                )

    if context_qa is None:
        return
    qa_index = {(row.get("DeliverableID") or "").strip(): row for row in context_qa}
    for missing in sorted(set(deliverables) - set(qa_index)):
        findings.append(
            Finding("XRG-009", paths["context_qa"],
                    f"{missing} is in {paths['deliverables']} but has no ContextBudgetQA row",
                    row_id=missing)
        )
    for extra in sorted(set(qa_index) - set(deliverables)):
        findings.append(
            Finding("XRG-009", paths["context_qa"],
                    f"{extra} has a ContextBudgetQA row but is not in {paths['deliverables']}",
                    row_id=extra)
        )
    for deliverable_id in sorted(set(deliverables) & set(qa_index)):
        declared = (deliverables[deliverable_id].get("ContextEnvelope") or "").strip()
        measured = (qa_index[deliverable_id].get("ContextEnvelope") or "").strip()
        if declared != measured:
            findings.append(
                Finding("XRG-010", paths["context_qa"],
                        f"{deliverable_id} ContextEnvelope {measured!r} vs "
                        f"{paths['deliverables']} {declared!r}", row_id=deliverable_id)
            )


def run(
    execution_root: Path,
    families: tuple[str, ...] = FAMILIES,
    evidence_root: Path | None = None,
) -> dict:
    """Execute the selected check families. Returns a machine-readable report."""
    execution_root = Path(execution_root)
    if not execution_root.is_dir():
        raise OperationalError(f"EXECUTION_ROOT is not a directory: {execution_root}")
    evidence_root = Path(evidence_root) if evidence_root else execution_root.parent

    findings: list[Finding] = []
    skipped: list[str] = []
    counters: dict = {"by_class": {}}

    decomposition = execution_root / "_Decomposition"
    deliverables_path = decomposition / "Deliverables.csv"
    ledger_path = decomposition / "ScopeLedger.csv"
    context_qa_path = decomposition / "ContextBudgetQA.csv"

    deliverables: dict[str, dict[str, str]] = {}
    if deliverables_path.is_file():
        deliverables = {
            (row.get("DeliverableID") or "").strip(): row
            for row in read_register(deliverables_path)
            if (row.get("DeliverableID") or "").strip()
        }

    if "XRG" in families:
        if deliverables_path.is_file() and ledger_path.is_file():
            context_qa = read_register(context_qa_path) if context_qa_path.is_file() else None
            if context_qa is None:
                skipped.append("XRG ContextBudgetQA checks (ContextBudgetQA.csv absent)")
            check_cross_register(
                deliverables,
                read_register(ledger_path),
                context_qa,
                {
                    "deliverables": os.path.relpath(deliverables_path, execution_root),
                    "ledger": os.path.relpath(ledger_path, execution_root),
                    "context_qa": os.path.relpath(context_qa_path, execution_root),
                },
                findings,
            )
        else:
            skipped.append("XRG family (Deliverables.csv and/or ScopeLedger.csv absent)")

    registers = discover_dependency_files(execution_root)
    seen_ids: dict[str, str] = {}
    per_file: list[dict] = []

    for register_path, folder_del_id in registers:
        rel_path = os.path.relpath(register_path, execution_root)
        before = len(findings)

        if "SCH" in families:
            ok, schema_findings, _ext, _count, _header = validate_dep_schema(str(register_path))
            if not ok:
                for detail in schema_findings:
                    findings.append(Finding("SCH-001", rel_path, detail))

        rows = read_register(register_path)
        if "EVQ" in families:
            known_ids = {
                (row.get("DependencyID") or "").strip()
                for row in rows
                if (row.get("DependencyID") or "").strip()
            }
            waivers = read_waivers(register_path, known_ids, rel_path, findings)
            check_evidence_quality(
                rows, rel_path, evidence_root, findings, counters, waivers=waivers
            )
        if "DRB" in families:
            check_dependency_binding(
                rows, rel_path, folder_del_id, deliverables, seen_ids, findings
            )

        per_file.append(
            {
                "path": rel_path,
                "rows": len(rows),
                "findings": len(findings) - before,
            }
        )

    if "DRB" in families and deliverables:
        covered = {folder_del_id for _p, folder_del_id in registers if folder_del_id}
        for missing in sorted(set(deliverables) - covered):
            findings.append(
                Finding("DRB-008", os.path.relpath(deliverables_path, execution_root),
                        f"{missing} has no deliverable-local Dependencies.csv in any of "
                        f"{'/'.join(LIFECYCLE_DIRS)}; a register outside these folders "
                        f"is not scanned", row_id=missing)
            )

    by_code: dict[str, int] = {}
    for finding in findings:
        by_code[finding.code] = by_code.get(finding.code, 0) + 1

    total_rows = sum(entry["rows"] for entry in per_file)
    return {
        "tool": "validate_decomposition_registers.py",
        "execution_root": str(execution_root),
        "evidence_root": str(evidence_root),
        "families": list(families),
        "registers_scanned": len(registers),
        "dependency_rows": total_rows,
        "deliverables_declared": len(deliverables),
        "row_class_metrics": counters["by_class"],
        "findings_by_code": dict(sorted(by_code.items())),
        "error_count": sum(1 for f in findings if f.severity == ERROR),
        "warning_count": sum(1 for f in findings if f.severity == WARNING),
        "skipped": skipped,
        "per_file": per_file,
        "findings": [f.as_dict() for f in findings],
    }


def print_report(report: dict, max_per_code: int) -> None:
    print(f"Register validation — {report['execution_root']}")
    print(f"  Families: {', '.join(report['families'])}")
    print(f"  Registers scanned: {report['registers_scanned']}  "
          f"Dependency rows: {report['dependency_rows']}  "
          f"Deliverables declared: {report['deliverables_declared']}")
    for note in report["skipped"]:
        print(f"  SKIPPED: {note}")

    metrics = report["row_class_metrics"]
    if metrics:
        print("\nEvidence-cell metrics by row class")
        header = (f"  {'class':<12}{'rows':>6}{'well-formed':>13}{'locus=quote':>13}"
                  f"{'quoted-locus':>14}{'empty-quote':>13}{'ph-locus':>10}"
                  f"{'waived':>8}{'file-pop':>10}{'file-res':>10}")
        print(header)
        for row_class in sorted(metrics):
            m = metrics[row_class]
            print(f"  {row_class:<12}{m['rows']:>6}{m['well_formed_evidence']:>13}"
                  f"{m['locus_quote_duplication']:>13}{m['quote_shaped_locus']:>14}"
                  f"{m['empty_evidence_quote']:>13}{m['placeholder_locus']:>10}"
                  f"{m.get('waived_rows', 0):>8}"
                  f"{m['evidence_file_populated']:>10}{m['evidence_file_resolved']:>10}")

    if report["findings"]:
        print("\nFindings")
        shown: dict[str, int] = {}
        for finding in report["findings"]:
            code = finding["code"]
            shown[code] = shown.get(code, 0) + 1
            if shown[code] > max_per_code:
                continue
            locator = finding["path"]
            if finding["line"] is not None:
                locator += f":{finding['line']}"
            ident = f" [{finding['row_id']}]" if finding["row_id"] else ""
            print(f"  {finding['severity']} {code} {locator}{ident} — {finding['detail']}")
        for code, count in sorted(report["findings_by_code"].items()):
            if count > max_per_code:
                print(f"  ... {code}: {count - max_per_code} further occurrence(s) suppressed "
                      f"(--max-per-code {max_per_code}; full list in --json)")

    print("\nSummary by check code")
    if report["findings_by_code"]:
        for code, count in sorted(report["findings_by_code"].items()):
            severity = CHECKS[code][1]
            print(f"  {severity:<7} {code}  {count:>5}  {CHECKS[code][2]}")
    else:
        print("  (none)")
    print(f"\n  ERROR findings:   {report['error_count']}")
    print(f"  WARNING findings: {report['warning_count']}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("execution_root", nargs="?", help="Project execution root")
    parser.add_argument("--json", dest="json_out", help="Write the full report as JSON")
    parser.add_argument("--families", default=",".join(FAMILIES),
                        help=f"Comma-separated subset of {','.join(FAMILIES)}")
    parser.add_argument("--evidence-root", help="Base for resolving EvidenceFile "
                                                "(default: parent of EXECUTION_ROOT)")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on WARNING findings as well as ERROR")
    parser.add_argument("--max-per-code", type=int, default=20,
                        help="Human-readable output cap per check code (default 20)")
    parser.add_argument("--list-checks", action="store_true",
                        help="Print the check catalogue and exit")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if args.list_checks:
        print(f"{'code':<10}{'family':<8}{'severity':<9}description")
        for code, (family, severity, description) in CHECKS.items():
            print(f"{code:<10}{family:<8}{severity:<9}{description}")
        return 0

    if not args.execution_root:
        print("ERROR: EXECUTION_ROOT is required (or use --list-checks)", file=sys.stderr)
        return 2

    families = tuple(f.strip().upper() for f in args.families.split(",") if f.strip())
    unknown = [f for f in families if f not in FAMILIES]
    if unknown:
        print(f"ERROR: unknown family/families: {', '.join(unknown)}", file=sys.stderr)
        return 2

    try:
        report = run(
            Path(args.execution_root),
            families=families,
            evidence_root=Path(args.evidence_root) if args.evidence_root else None,
        )
    except OperationalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print_report(report, args.max_per_code)

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
        print(f"\n  JSON report: {out_path}")

    if report["error_count"]:
        return 1
    if args.strict and report["warning_count"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
