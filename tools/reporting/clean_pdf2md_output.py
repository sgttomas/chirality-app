#!/usr/bin/env python3
"""
clean_pdf2md_output.py
Remove repeating page headers, separators, and boilerplate from
PDF-to-markdown conversion output.

Handles four common header variants produced by VLM-based PDF converters:
  1. HTML <table> with Project Name / Document Title rows
  2. Markdown pipe table (4-column: Project Name + Document Number)
  3. Markdown pipe table (2-column: stacked Project Name / Number / Title / Rev)
  4. Plain bold text (non-table header block)

Also removes page-break separators (--- and <hr>).

Usage:
    python3 clean_pdf2md_output.py <file.md> [file2.md ...]

Inputs:
    file.md — one or more markdown files to clean in-place

Outputs:
    Each file is overwritten with cleaned content.
    Prints per-file line removal count to stdout.

Example:
    python3 clean_pdf2md_output.py output.md
    python3 clean_pdf2md_output.py docs/DBM_4-25.md docs/DBM_3-25.md
"""

import re
import sys
from pathlib import Path


def clean_pdf2md(text: str) -> str:
    # --- Pattern 1: HTML <table> headers containing Project Name / Document Title ---
    # Handles <table>, <table><tbody>, with varied whitespace and attributes.
    html_header = re.compile(
        r'<table>\s*(?:<tbody>\s*)?'
        r'<tr>.*?Project Name.*?</tr>\s*'
        r'<tr>.*?Document Title.*?</tr>\s*'
        r'(?:</tbody>\s*)?</table>\s*',
        re.DOTALL | re.IGNORECASE,
    )
    text = html_header.sub('', text)

    # --- Pattern 2: Markdown pipe table (4-column with Document Number) ---
    # | ... Project Name ... | ... | Document Number: | ... |
    # | :--- | :--- | :--- | :--- |     (optional alignment row)
    # | ... Document Title ... | ... | Revision No.: | ... |
    md_header_4col = re.compile(
        r'^\|[^\n]*Project Name[^\n]*\|\s*\n'
        r'(?:\|[\s:\-|]+\|\s*\n)?'
        r'\|[^\n]*Document Title[^\n]*\|\s*\n',
        re.MULTILINE | re.IGNORECASE,
    )
    text = md_header_4col.sub('', text)

    # --- Pattern 3: Markdown pipe table (2-column stacked) ---
    # | :--- | :--- |
    # | **Project Name:** | ... |
    # | **Document Number:** | ... |
    # | **Document Title:** | ... |
    # | **Revision No.:** | ... |
    md_header_2col = re.compile(
        r'^\|[\s:\-|]+\|\s*\n'
        r'\|[^\n]*\*\*Project Name:\*\*[^\n]*\|\s*\n'
        r'\|[^\n]*\*\*Document Number:\*\*[^\n]*\|\s*\n'
        r'\|[^\n]*\*\*Document Title:\*\*[^\n]*\|\s*\n'
        r'\|[^\n]*\*\*Revision No\.:\*\*[^\n]*\|\s*\n',
        re.MULTILINE | re.IGNORECASE,
    )
    text = md_header_2col.sub('', text)

    # --- Pattern 4: Plain bold text header (no table) ---
    # **Project Name:** ...
    # **Document Title:** ...
    #
    # **Document Number:** ...
    # **Revision No.:** ...
    plain_header = re.compile(
        r'^\*\*Project Name:\*\*[^\n]*\n'
        r'\*\*Document Title:\*\*[^\n]*\n'
        r'\s*\n?'
        r'\*\*Document Number:\*\*[^\n]*\n'
        r'\*\*Revision No\.:\*\*[^\n]*\n',
        re.MULTILINE | re.IGNORECASE,
    )
    text = plain_header.sub('', text)

    # --- Remove page-break separators ---
    text = re.sub(r'^\s*---\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*<hr>\s*$', '', text, flags=re.MULTILINE)

    # --- Collapse triple+ blank lines ---
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.md> [file2.md ...]", file=sys.stderr)
        sys.exit(1)

    for path_str in sys.argv[1:]:
        path = Path(path_str)
        if not path.is_file():
            print(f"ERROR: Not a file: {path}", file=sys.stderr)
            sys.exit(1)

        original = path.read_text(encoding='utf-8')
        cleaned = clean_pdf2md(original)

        removed = original.count('\n') - cleaned.count('\n')
        path.write_text(cleaned, encoding='utf-8')
        print(f"{path.name}: {removed} lines removed")


if __name__ == '__main__':
    main()
