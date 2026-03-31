#!/usr/bin/env python3
"""
rasterize_pdf.py
Render PDF pages to numbered PNG files via pymupdf.

Idempotent: skips pages where the PNG already exists, enabling
resumable conversions. Writes a manifest.json with page metadata.

Usage:
    python3 rasterize_pdf.py <pdf_path> <output_dir> [--dpi 300] [--pages 1-5,7]

Inputs:
    pdf_path   — path to the input PDF file
    output_dir — directory for PNG output (created if absent)
    --dpi N    — rendering DPI (default: 300)
    --pages S  — page range: all, 5, 3-15, or 1,3,5,7 (default: all)

Outputs:
    page_0001.png, page_0002.png, ... — one PNG per rendered page
    manifest.json — metadata: pdf_path, page_count, dpi, pages_rendered, files

Example:
    python3 rasterize_pdf.py document.pdf ./work --dpi 300
    python3 rasterize_pdf.py document.pdf ./work --dpi 300 --pages 1-5
"""

import json
import os
import sys
import time

try:
    import pymupdf
except ImportError:
    print("ERROR: pymupdf is not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(2)


def parse_pages(spec, total_pages):
    """Parse a page range spec into a sorted list of 1-indexed page numbers."""
    if spec is None or spec.strip().lower() == 'all':
        return list(range(1, total_pages + 1))

    pages = set()
    for part in spec.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            start, end = part.split('-', 1)
            start = int(start) if start.strip() else 1
            end = int(end) if end.strip() else total_pages
            pages.update(range(max(1, start), min(total_pages, end) + 1))
        else:
            p = int(part)
            if 1 <= p <= total_pages:
                pages.add(p)
    return sorted(pages)


def rasterize(pdf_path, output_dir, dpi=300, pages_spec=None):
    """Rasterize PDF pages to PNGs. Returns (manifest_dict, rendered_count, reused_count)."""
    pdf_path = os.path.abspath(pdf_path)
    output_dir = os.path.abspath(output_dir)

    if not os.path.isfile(pdf_path):
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(2)

    os.makedirs(output_dir, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    total_pages = doc.page_count

    pages = parse_pages(pages_spec, total_pages)

    rendered = 0
    reused = 0
    files = {}

    for page_num in pages:
        filename = f"page_{page_num:04d}.png"
        filepath = os.path.join(output_dir, filename)
        files[str(page_num)] = filename

        if os.path.isfile(filepath):
            reused += 1
            continue

        page = doc[page_num - 1]  # pymupdf is 0-indexed
        scale = dpi / 72.0
        mat = pymupdf.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat)
        pix.save(filepath)
        rendered += 1

    doc.close()

    manifest = {
        "pdf_path": pdf_path,
        "page_count": total_pages,
        "dpi": dpi,
        "pages_rendered": pages,
        "files": files,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    return manifest, rendered, reused


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <pdf_path> <output_dir> [--dpi 300] [--pages 1-5,7]",
              file=sys.stderr)
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    dpi = 300
    pages_spec = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--dpi' and i + 1 < len(sys.argv):
            dpi = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--pages' and i + 1 < len(sys.argv):
            pages_spec = sys.argv[i + 1]
            i += 2
        else:
            print(f"ERROR: Unknown argument: {sys.argv[i]}", file=sys.stderr)
            sys.exit(1)

    manifest, rendered, reused = rasterize(pdf_path, output_dir, dpi, pages_spec)

    total = len(manifest["pages_rendered"])
    print(f"{total} pages: {rendered} rendered, {reused} reused (DPI={dpi})")
    print(f"manifest: {os.path.join(output_dir, 'manifest.json')}")


if __name__ == '__main__':
    main()
