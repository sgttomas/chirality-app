#!/usr/bin/env python3
"""
extract_pdf_titleblock_text.py
Extract drawing-number candidates, title-block system-name candidates, and title-block text snippets from PDF pages
using the external `pdftotext` utility.

Usage:
    python3 extract_pdf_titleblock_text.py <pdf_path> <output_csv> --pages 7-61
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path


DWG_NO_RE = re.compile(r"\b[A-Z]{2,12}-\d{3,8}-\d{3,8}-\d{3,8}\b")
PROJECT_TITLE_RE = re.compile(r"4-25\s+WEST\s+DOE\s+300\s+MMSCFD\s+DEEPCUT\s+GAS\s+PLANT", re.IGNORECASE)
TITLE_SUFFIX_RE = re.compile(r"PROCESS\s+FLOW\s+DIAGRAM", re.IGNORECASE)


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start = int(start_str)
            end = int(end_str)
            if start > end:
                start, end = end, start
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(p for p in pages if p > 0)


def pdftotext_available() -> bool:
    try:
        subprocess.run(["pdftotext", "-v"], capture_output=True, check=False)
        return True
    except FileNotFoundError:
        return False


def extract_page_text(pdf_path: Path, page_num: int) -> str:
    result = subprocess.run(
        ["pdftotext", "-f", str(page_num), "-l", str(page_num), "-layout", str(pdf_path), "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"pdftotext failed for page {page_num}")
    return result.stdout


def compact_excerpt(text: str, max_lines: int = 8) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    excerpt = lines[-max_lines:]
    return " || ".join(excerpt)


def normalize_spaces(value: str) -> str:
    return " ".join(value.split())


def extract_system_name_candidate(text: str) -> str:
    lines = [normalize_spaces(line) for line in text.splitlines()]
    lines = [line for line in lines if line]

    project_index = next((i for i, line in enumerate(lines) if PROJECT_TITLE_RE.search(line)), None)
    if project_index is None:
        return ""

    for line in lines[project_index + 1: project_index + 6]:
        upper_line = line.upper()
        if "DATE" in upper_line or "SCALE" in upper_line or "CLIENT DWG" in upper_line:
            break
        if TITLE_SUFFIX_RE.search(line):
            return ""
        if line and not line.endswith(":"):
            return line
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract title-block text and drawing-number candidates from PDF pages.")
    parser.add_argument("pdf_path")
    parser.add_argument("output_csv")
    parser.add_argument("--pages", required=True)
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).resolve()
    output_csv = Path(args.output_csv).resolve()

    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 2
    if not pdftotext_available():
        print("ERROR: pdftotext is not installed or not on PATH", file=sys.stderr)
        return 2

    pages = parse_pages(args.pages)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["page", "dwg_no", "system_name_candidate", "status", "titleblock_text"])
        for page_num in pages:
            try:
                text = extract_page_text(pdf_path, page_num)
                match = DWG_NO_RE.search(text)
                dwg_no = match.group(0) if match else ""
                system_name = extract_system_name_candidate(text)
                status = "FOUND" if dwg_no else "NOT_FOUND"
                writer.writerow([page_num, dwg_no, system_name, status, compact_excerpt(text)])
            except Exception as exc:  # noqa: BLE001
                writer.writerow([page_num, "", "", "ERROR", str(exc)])

    print(f"pages={len(pages)}")
    print(f"output={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
