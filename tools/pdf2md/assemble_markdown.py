#!/usr/bin/env python3
"""
assemble_markdown.py
Join per-page markdown files into a single assembled document.

Reads manifest.json from the pages directory for canonical page order.
Missing pages get a placeholder marker. Joins with a configurable
separator between pages.

Usage:
    python3 assemble_markdown.py <pages_dir> <output_file> [--separator "---"]

Inputs:
    pages_dir   — directory containing page_NNNN.md files and manifest.json
    output_file — path to write the assembled markdown
    --separator — string between pages (default: "---")

Outputs:
    Assembled markdown file. Prints summary to stdout.

Example:
    python3 assemble_markdown.py ./work output.md
    python3 assemble_markdown.py ./work output.md --separator "---"
"""

import json
import os
import re
import sys
from pathlib import Path


def assemble(pages_dir, output_file, separator='---'):
    """Assemble per-page markdowns into a single document."""
    pages_dir = Path(pages_dir)
    output_file = Path(output_file)

    manifest_path = pages_dir / 'manifest.json'
    if not manifest_path.is_file():
        print(f"ERROR: manifest.json not found in {pages_dir}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    pages_rendered = manifest.get('pages_rendered', [])
    if not pages_rendered:
        print("ERROR: No pages in manifest", file=sys.stderr)
        sys.exit(1)

    parts = []
    missing = []
    assembled = 0

    for page_num in sorted(pages_rendered):
        md_filename = f"page_{page_num:04d}.md"
        md_path = pages_dir / md_filename

        if md_path.is_file():
            content = md_path.read_text(encoding='utf-8').strip()
            if content:
                parts.append(content)
                assembled += 1
            else:
                parts.append(f'*[Page {page_num}: empty]*')
                missing.append(page_num)
        else:
            parts.append(f'*[Page {page_num}: conversion unavailable]*')
            missing.append(page_num)

    # Join with separator
    sep_block = f'\n\n{separator}\n\n' if separator else '\n\n'
    text = sep_block.join(parts)

    # Final blank-line collapse
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Ensure final newline
    text = text.rstrip() + '\n'

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(text, encoding='utf-8')

    byte_count = output_file.stat().st_size
    total = len(pages_rendered)

    print(f"{assembled}/{total} pages assembled → {output_file}")
    if missing:
        print(f"  missing/empty: {missing}")
    print(f"  size: {byte_count:,} bytes")

    return assembled, missing


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <pages_dir> <output_file> [--separator \"---\"]",
              file=sys.stderr)
        sys.exit(1)

    pages_dir = sys.argv[1]
    output_file = sys.argv[2]
    separator = '---'

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--separator' and i + 1 < len(sys.argv):
            separator = sys.argv[i + 1]
            i += 2
        else:
            print(f"ERROR: Unknown argument: {sys.argv[i]}", file=sys.stderr)
            sys.exit(1)

    assemble(pages_dir, output_file, separator)


if __name__ == '__main__':
    main()
