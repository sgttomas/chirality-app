#!/usr/bin/env python3
"""
check_concordance.py — Deterministic cross-section assertion concordance checker.

Purpose:
  Compare the frozen concordance register against the current per-section
  assertion CSVs and report blocking mismatches deterministically.

Inputs:
  --register        Frozen Publication_Concordance_Register.csv
  --sections-root   Root containing per-section *_ASSERTIONS.csv files
  --output-report   Publication_Concordance_Report.md
  --output-findings Publication_Concordance_Findings.csv

Writes:
  - Publication_Concordance_Report.md
  - Publication_Concordance_Findings.csv

Scope boundary:
  Reads: register and per-section assertion CSVs under sections-root
  Writes: only Publication_Concordance_Report.md and
  Publication_Concordance_Findings.csv
  Does not mutate section outputs or the publication package snapshot

Exit codes:
  0 = success, no blocking concordance findings
  1 = fatal input / parsing error
  2 = outputs written, but blocking findings remain

Example:
  python3 tools/publication/check_concordance.py \
    --register /repo/.../_Planning/Publication_Concordance_Register.csv \
    --sections-root /repo/.../_Publication/DBM/sections \
    --output-report /repo/.../_Publication/DBM/package/RUN-20260418-120000/Publication_Concordance_Report.md \
    --output-findings /repo/.../_Publication/DBM/package/RUN-20260418-120000/Publication_Concordance_Findings.csv

All assertions listed in the register are treated as concordance-blocking in v1.

Optional hypergraph QA (AUXILIARY_STRUCTURE_EVIDENCE):
  When the manifest declares a hypergraph use mode that includes QA
  (AUXILIARY_QA or AUXILIARY_PLANNING_AND_QA), the tool runs a supplementary
  block of hypergraph-specific checks and reports them SEPARATELY from
  deterministic concordance findings.  Hypergraph QA findings may be
  ADVISORY_ONLY or BLOCK_ON_BINDING_FAILURE depending on the configured
  binding policy.  The core concordance engine is never modified by
  hypergraph inputs.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

FINDING_COLUMNS = [
    "AssertionKey",
    "AssertionLabel",
    "AuthoritySectionID",
    "SectionID",
    "FindingType",
    "ExpectedNormalizedValue",
    "ObservedNormalizedValue",
    "ComparisonRule",
    "Blocking",
    "Notes",
]


ALLOWED_ASSERTION_STATUS = {"ASSERTED", "REFERRED", "NOT_APPLICABLE", "CONFLICT_UNRESOLVED"}

# ---------------------------------------------------------------------------
# Hypergraph use-mode and binding-policy constants.
#
# Hypergraph QA is supplementary — it never replaces deterministic
# concordance checking.  See plan section "Publication Tooling Changes /
# Tool 2".
# ---------------------------------------------------------------------------
HYPERGRAPH_QA_MODES = {
    "AUXILIARY_QA",
    "AUXILIARY_PLANNING_AND_QA",
}
HYPERGRAPH_BINDING_POLICIES = {"ADVISORY_ONLY", "BLOCK_ON_BINDING_FAILURE"}


def fatal(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_within(path: Path, root: Path, label: str) -> None:
    """Fail fast if a requested output path escapes the publication tool root inferred from sections-root."""
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fatal(f"{label} must resolve under publication root {root}: {path}")


def fail_if_output_exists(path: Path, label: str) -> None:
    if path.exists():
        fatal(f"{label} already exists; choose a new immutable package snapshot before rerunning: {path}")


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            normalized_rows: List[Dict[str, str]] = []
            for row in reader:
                normalized: Dict[str, str] = {}
                for key, value in row.items():
                    normalized_key = (key or "").strip()
                    if isinstance(value, list):
                        normalized_value = "; ".join((item or "").strip() for item in value if (item or "").strip())
                    else:
                        normalized_value = (value or "").strip()
                    normalized[normalized_key] = normalized_value
                normalized_rows.append(normalized)
            return normalized_rows
    except FileNotFoundError:
        fatal(f"CSV file not found: {path}")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def parse_list_cell(value: str) -> List[str]:
    if not value:
        return []
    parts = re.split(r"[;,]", value.replace("\n", ";"))
    result: List[str] = []
    seen = set()
    for part in parts:
        token = part.strip()
        if not token or token in seen:
            continue
        result.append(token)
        seen.add(token)
    return result


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).upper()


def tokenize(value: str) -> Tuple[str, ...]:
    return tuple(token for token in re.split(r"[^A-Z0-9]+", normalize_text(value)) if token)


def parse_number(value: str) -> float:
    match = re.search(r"[-+]?\d+(?:\.\d+)?", value.replace(",", ""))
    if not match:
        raise ValueError(value)
    return float(match.group(0))


def parse_range(value: str) -> Tuple[float, float]:
    numbers = re.findall(r"[-+]?\d+(?:\.\d+)?", value.replace(",", ""))
    if len(numbers) >= 2:
        first, second = float(numbers[0]), float(numbers[1])
        return (min(first, second), max(first, second))
    raise ValueError(value)


def compare_values(rule: str, parameter: str, expected: str, observed: str) -> bool:
    rule = rule.strip().upper()
    if rule == "EXACT":
        return normalize_text(expected) == normalize_text(observed)
    if rule == "ROUND_N":
        digits_match = re.search(r"(\d+)", parameter or "")
        digits = int(digits_match.group(1)) if digits_match else 0
        return round(parse_number(expected), digits) == round(parse_number(observed), digits)
    if rule == "TOKEN_MATCH":
        return tokenize(expected) == tokenize(observed)
    if rule == "SET_MATCH":
        return set(tokenize(item)[0] if len(tokenize(item)) == 1 else " ".join(tokenize(item)) for item in parse_list_cell(expected)) == set(
            tokenize(item)[0] if len(tokenize(item)) == 1 else " ".join(tokenize(item)) for item in parse_list_cell(observed)
        )
    if rule == "RANGE_MATCH":
        return parse_range(expected) == parse_range(observed)
    raise ValueError(f"Unsupported comparison rule: {rule}")


def load_section_assertions(sections_root: Path) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    by_section: Dict[str, Dict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for assertion_path in sorted(sections_root.glob("*/*_ASSERTIONS.csv")):
        rows = read_csv_rows(assertion_path)
        for row in rows:
            section_id = row.get("SectionID", "") or assertion_path.parent.name
            assertion_key = row.get("AssertionKey", "")
            if not section_id or not assertion_key:
                continue
            status = row.get("AssertionStatus", "")
            if status and status not in ALLOWED_ASSERTION_STATUS:
                fatal(f"Unsupported AssertionStatus '{status}' in {assertion_path}")
            by_section[section_id][assertion_key].append(row)
    return by_section


def make_finding(
    register_row: Dict[str, str],
    section_id: str,
    finding_type: str,
    expected: str,
    observed: str,
    notes: str,
) -> Dict[str, str]:
    return {
        "AssertionKey": register_row.get("AssertionKey", ""),
        "AssertionLabel": register_row.get("AssertionLabel", ""),
        "AuthoritySectionID": register_row.get("AuthoritySectionID", ""),
        "SectionID": section_id,
        "FindingType": finding_type,
        "ExpectedNormalizedValue": expected,
        "ObservedNormalizedValue": observed,
        "ComparisonRule": register_row.get("ComparisonRule", ""),
        "Blocking": "TRUE",
        "Notes": notes,
    }


def evaluate_register(
    register_rows: List[Dict[str, str]],
    assertions_by_section: Dict[str, Dict[str, List[Dict[str, str]]]],
) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    findings: List[Dict[str, str]] = []
    metrics = {
        "total_assertions": len(register_rows),
        "passed_assertions": 0,
        "blocked_mismatches": 0,
        "missing_required_assertions": 0,
    }

    for register_row in register_rows:
        assertion_key = register_row.get("AssertionKey", "")
        authority_section = register_row.get("AuthoritySectionID", "")
        required_sections = parse_list_cell(register_row.get("RequiredSectionIDs", ""))
        required_sections = [section for section in required_sections if section]
        comparison_rule = register_row.get("ComparisonRule", "")
        comparison_param = register_row.get("ComparisonParameter", "")

        if authority_section and authority_section not in required_sections:
            required_sections = [authority_section] + required_sections

        authority_rows = assertions_by_section.get(authority_section, {}).get(assertion_key, []) if authority_section else []
        if not authority_rows:
            findings.append(
                make_finding(
                    register_row,
                    authority_section,
                    "MISSING_AUTHORITY_ASSERTION",
                    "",
                    "",
                    "Authority section did not emit the required assertion row.",
                )
            )
            metrics["blocked_mismatches"] += 1
            metrics["missing_required_assertions"] += 1
            continue
        if len(authority_rows) > 1:
            findings.append(
                make_finding(
                    register_row,
                    authority_section,
                    "DUPLICATE_AUTHORITY_ASSERTION_ROWS",
                    "",
                    "",
                    "Authority section emitted multiple rows for the same assertion key.",
                )
            )
            metrics["blocked_mismatches"] += 1
            continue
        authority_row = authority_rows[0]
        if authority_row.get("AssertionStatus", "") != "ASSERTED":
            findings.append(
                make_finding(
                    register_row,
                    authority_section,
                    "NON_ASSERTED_AUTHORITY_STATUS",
                    "ASSERTED",
                    authority_row.get("AssertionStatus", ""),
                    "Authority section must emit ASSERTED status.",
                )
            )
            metrics["blocked_mismatches"] += 1
            continue
        expected_value = authority_row.get("NormalizedValue", "")
        if not expected_value:
            findings.append(
                make_finding(
                    register_row,
                    authority_section,
                    "EMPTY_AUTHORITY_VALUE",
                    "non-empty",
                    "",
                    "Authority section ASSERTED row is missing NormalizedValue.",
                )
            )
            metrics["blocked_mismatches"] += 1
            continue

        assertion_failed = False
        for required_section in required_sections:
            section_rows = assertions_by_section.get(required_section, {}).get(assertion_key, [])
            if not section_rows:
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "MISSING_REQUIRED_ASSERTION",
                        expected_value,
                        "",
                        "Required section did not emit an assertion row for this key.",
                    )
                )
                metrics["blocked_mismatches"] += 1
                metrics["missing_required_assertions"] += 1
                assertion_failed = True
                continue
            if len(section_rows) > 1:
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "DUPLICATE_SECTION_ASSERTION_ROWS",
                        expected_value,
                        "",
                        "Section emitted multiple rows for the same assertion key.",
                    )
                )
                metrics["blocked_mismatches"] += 1
                assertion_failed = True
                continue
            section_row = section_rows[0]
            status = section_row.get("AssertionStatus", "")
            observed_value = section_row.get("NormalizedValue", "")
            if required_section == authority_section:
                continue
            if status == "REFERRED":
                continue
            if status == "NOT_APPLICABLE":
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "NOT_APPLICABLE_IN_REQUIRED_SECTION",
                        expected_value,
                        observed_value,
                        "Required section must ASSERT or REFERENCE the value; NOT_APPLICABLE is not allowed.",
                    )
                )
                metrics["blocked_mismatches"] += 1
                assertion_failed = True
                continue
            if status == "CONFLICT_UNRESOLVED":
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "CONFLICT_UNRESOLVED",
                        expected_value,
                        observed_value,
                        "Section declared an unresolved assertion conflict.",
                    )
                )
                metrics["blocked_mismatches"] += 1
                assertion_failed = True
                continue
            if status != "ASSERTED":
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "INVALID_ASSERTION_STATUS",
                        expected_value,
                        status,
                        "Required section must ASSERT or REFERENCE the assertion.",
                    )
                )
                metrics["blocked_mismatches"] += 1
                assertion_failed = True
                continue
            if not observed_value:
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "EMPTY_ASSERTED_VALUE",
                        expected_value,
                        "",
                        "ASSERTED section row is missing NormalizedValue.",
                    )
                )
                metrics["blocked_mismatches"] += 1
                assertion_failed = True
                continue
            try:
                matched = compare_values(comparison_rule, comparison_param, expected_value, observed_value)
            except Exception as exc:  # pragma: no cover - defensive
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "INVALID_COMPARISON_INPUT",
                        expected_value,
                        observed_value,
                        f"Comparison failed: {exc}",
                    )
                )
                metrics["blocked_mismatches"] += 1
                assertion_failed = True
                continue
            if not matched:
                findings.append(
                    make_finding(
                        register_row,
                        required_section,
                        "VALUE_MISMATCH",
                        expected_value,
                        observed_value,
                        "Observed normalized value does not concord with authority section under the configured comparison rule.",
                    )
                )
                metrics["blocked_mismatches"] += 1
                assertion_failed = True
        if not assertion_failed:
            metrics["passed_assertions"] += 1

    return findings, metrics


def _read_hypergraph_manifest_fields(manifest_path: Path) -> Dict[str, str]:
    """Read the frozen manifest and extract hypergraph-related explicit fields.

    This function intentionally re-reads the manifest rather than importing the
    full manifest parser from build_section_map, to keep check_concordance.py
    self-contained.  Only the explicit key-value fields are needed.
    """
    fields: Dict[str, str] = {}
    if not manifest_path.exists():
        return fields
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except Exception:
        return fields

    kv_re = re.compile(r"^\s*(?:-\s*)?(?:\*\*)?([A-Za-z0-9_ /-]+?)(?:\*\*)?\s*:\s*(.+?)\s*$")
    kv_bold_re = re.compile(r"^\s*(?:-\s*)?\*\*([A-Za-z0-9_ /-]+?):\*\*\s*(.+?)\s*$")
    for line in text.splitlines():
        match = kv_bold_re.match(line) or kv_re.match(line)
        if match:
            key = re.sub(r"\s+", " ", match.group(1).strip()).rstrip(":").upper().replace(" ", "_").replace("/", "_")
            value = match.group(2).strip().strip("`")
            fields[key] = value

    return {
        "use_mode": fields.get("HYPERGRAPH_USE_MODE", ""),
        "binding_policy": fields.get("HYPERGRAPH_QA_BINDING_POLICY", "ADVISORY_ONLY"),
        "snapshot_path": fields.get("HYPERGRAPH_SNAPSHOT_PATH", ""),
        "qa_verdict": fields.get("HYPERGRAPH_QA_VERDICT", ""),
        "limitations": fields.get("HYPERGRAPH_LIMITATIONS", ""),
    }


def _hypergraph_qa_allowed(hg_fields: Dict[str, str]) -> bool:
    """Return True only when the manifest admits hypergraph evidence for QA use."""
    return hg_fields.get("use_mode", "").strip().upper() in HYPERGRAPH_QA_MODES


def _hypergraph_qa_is_binding(hg_fields: Dict[str, str]) -> bool:
    """Return True if hypergraph QA findings are configured as blocking."""
    return hg_fields.get("binding_policy", "").strip().upper() == "BLOCK_ON_BINDING_FAILURE"


def evaluate_hypergraph_qa(
    register_rows: List[Dict[str, str]],
    hg_fields: Dict[str, str],
) -> List[Dict[str, str]]:
    """Run supplementary hypergraph QA checks.

    These checks are reported SEPARATELY from deterministic concordance
    findings.  The core concordance engine is untouched.

    Current checks:
      - HYPERGRAPH_QA_BLOCKED_SNAPSHOT: the admitted snapshot has a BLOCKED
        QA verdict but was used for QA anyway.
      - HYPERGRAPH_QA_LIMITATIONS_PRESENT: limitations are disclosed in the
        manifest.

    Returns a list of finding rows using the same FINDING_COLUMNS schema
    but with FindingType prefixed by HYPERGRAPH_QA_.
    """
    findings: List[Dict[str, str]] = []
    is_binding = _hypergraph_qa_is_binding(hg_fields)
    blocking_label = "TRUE" if is_binding else "FALSE"

    qa_verdict = hg_fields.get("qa_verdict", "").strip().upper()
    if qa_verdict == "BLOCKED":
        findings.append({
            "AssertionKey": "HYPERGRAPH_SNAPSHOT_QA",
            "AssertionLabel": "Hypergraph snapshot QA verdict",
            "AuthoritySectionID": "",
            "SectionID": "",
            "FindingType": "HYPERGRAPH_QA_BLOCKED_SNAPSHOT",
            "ExpectedNormalizedValue": "NON_BLOCKING",
            "ObservedNormalizedValue": "BLOCKED",
            "ComparisonRule": "",
            "Blocking": blocking_label,
            "Notes": (
                "The admitted hypergraph snapshot has a BLOCKED QA verdict.  "
                "Hypergraph-derived QA results should be treated with caution."
            ),
        })

    limitations = hg_fields.get("limitations", "").strip()
    if limitations:
        findings.append({
            "AssertionKey": "HYPERGRAPH_LIMITATIONS",
            "AssertionLabel": "Hypergraph limitations",
            "AuthoritySectionID": "",
            "SectionID": "",
            "FindingType": "HYPERGRAPH_QA_LIMITATIONS_PRESENT",
            "ExpectedNormalizedValue": "",
            "ObservedNormalizedValue": limitations[:200],
            "ComparisonRule": "",
            "Blocking": blocking_label,
            "Notes": "The manifest declares known hypergraph limitations.",
        })

    return findings


def build_report(
    findings: List[Dict[str, str]],
    metrics: Dict[str, int],
    hypergraph_findings: Optional[List[Dict[str, str]]] = None,
    hg_fields: Optional[Dict[str, str]] = None,
) -> str:
    implicated_sections = sorted({row.get("SectionID", "") for row in findings if row.get("SectionID", "")})
    lines = [
        "# Publication Concordance Report",
        "",
        "## Summary",
        "",
        f"- Total assertions checked: {metrics['total_assertions']}",
        f"- Passed assertions: {metrics['passed_assertions']}",
        f"- Blocked mismatches: {metrics['blocked_mismatches']}",
        f"- Missing required assertions: {metrics['missing_required_assertions']}",
        f"- Sections implicated by findings: {', '.join(implicated_sections) if implicated_sections else 'None'}",
        "",
        "## Findings",
        "",
    ]
    if findings:
        lines.append("| AssertionKey | AuthoritySectionID | SectionID | FindingType | Expected | Observed | Notes |")
        lines.append("|---|---|---|---|---|---|---|")
        for row in findings:
            lines.append(
                "| {AssertionKey} | {AuthoritySectionID} | {SectionID} | {FindingType} | {ExpectedNormalizedValue} | {ObservedNormalizedValue} | {Notes} |".format(
                    **{key: value.replace("|", "\\|") for key, value in row.items() if isinstance(value, str)}
                )
            )
    else:
        lines.append("- None")
    lines.append("")

    # --- Supplementary hypergraph QA block (reported separately) ----------
    if hypergraph_findings is not None:
        lines.append("## Hypergraph QA (Supplementary)")
        lines.append("")
        binding_policy = (hg_fields or {}).get("binding_policy", "ADVISORY_ONLY")
        use_mode = (hg_fields or {}).get("use_mode", "NONE")
        lines.append(f"- Hypergraph use mode: {use_mode}")
        lines.append(f"- Binding policy: {binding_policy}")
        lines.append(f"- Hypergraph QA findings: {len(hypergraph_findings)}")
        lines.append("")
        if hypergraph_findings:
            lines.append("| FindingType | Expected | Observed | Blocking | Notes |")
            lines.append("|---|---|---|---|---|")
            for row in hypergraph_findings:
                lines.append(
                    "| {FindingType} | {ExpectedNormalizedValue} | {ObservedNormalizedValue} | {Blocking} | {Notes} |".format(
                        **{key: value.replace("|", "\\|") for key, value in row.items() if isinstance(value, str)}
                    )
                )
        else:
            lines.append("- None")
        lines.append("")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check structured cross-section concordance assertions.")
    parser.add_argument("--register", required=True)
    parser.add_argument("--sections-root", required=True)
    parser.add_argument("--output-report", required=True)
    parser.add_argument("--output-findings", required=True)
    # Optional: path to the frozen publication manifest for hypergraph QA.
    # When provided and the manifest admits hypergraph evidence for QA,
    # supplementary hypergraph QA checks are run and reported separately
    # from core concordance findings.
    parser.add_argument("--manifest", default="")
    args = parser.parse_args()

    register_path = Path(args.register).resolve()
    sections_root = Path(args.sections_root).resolve()
    output_report = Path(args.output_report).resolve()
    output_findings = Path(args.output_findings).resolve()

    if not register_path.exists() or not sections_root.exists():
        fatal("Register path and sections root must exist.")

    publication_root = sections_root.parent
    require_within(output_report, publication_root, "--output-report")
    require_within(output_findings, publication_root, "--output-findings")
    fail_if_output_exists(output_report, "--output-report")
    fail_if_output_exists(output_findings, "--output-findings")

    register_rows = read_csv_rows(register_path)
    assertions_by_section = load_section_assertions(sections_root)
    findings, metrics = evaluate_register(register_rows, assertions_by_section)

    # ------------------------------------------------------------------
    # Optional supplementary hypergraph QA
    # (AUXILIARY_STRUCTURE_EVIDENCE — see plan Phase 2, Tool 2).
    #
    # When the manifest admits hypergraph evidence for QA, run a
    # supplementary block of hypergraph-specific checks.  These are
    # reported SEPARATELY from concordance findings and do not modify the
    # core concordance engine.  The binding policy determines whether
    # hypergraph QA findings can block the package.
    # ------------------------------------------------------------------
    hypergraph_findings: Optional[List[Dict[str, str]]] = None
    hg_fields: Optional[Dict[str, str]] = None
    manifest_path = Path(args.manifest).resolve() if args.manifest else None
    if manifest_path and manifest_path.exists():
        hg_fields = _read_hypergraph_manifest_fields(manifest_path)
        if _hypergraph_qa_allowed(hg_fields):
            hypergraph_findings = evaluate_hypergraph_qa(register_rows, hg_fields)

    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_findings.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(
        build_report(findings, metrics, hypergraph_findings=hypergraph_findings, hg_fields=hg_fields),
        encoding="utf-8",
    )

    # Write core concordance findings.  Hypergraph QA findings, if any,
    # are appended with distinct FindingType prefixes so downstream
    # consumers can filter them independently.
    all_findings = list(findings)
    if hypergraph_findings:
        all_findings.extend(hypergraph_findings)
    write_csv(output_findings, FINDING_COLUMNS, all_findings)

    print(f"Wrote concordance report: {output_report}")
    print(f"Wrote concordance findings: {output_findings}")
    print(f"Blocking concordance findings: {len(findings)}")
    if hypergraph_findings is not None:
        binding_hg = [f for f in hypergraph_findings if f.get("Blocking") == "TRUE"]
        print(f"Hypergraph QA findings: {len(hypergraph_findings)} ({len(binding_hg)} binding)")

    if findings:
        return 2
    # Hypergraph binding findings can also trigger exit code 2
    if hypergraph_findings and any(f.get("Blocking") == "TRUE" for f in hypergraph_findings):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
