#!/usr/bin/env python3
"""Render a validated ScopeOfWork.md to deterministic, script-free HTML."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

from common import SCHEMA, SowError, parse_sow, resolve_production_format, validate_document

RENDERER_VERSION = "chirality-sow-renderer/v1"


def inline(text: str) -> str:
    escaped = html.escape(text, quote=True)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_markdown(body: str) -> str:
    out: list[str] = []
    in_list = False
    in_table = False
    lines = body.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("<!--"):
            index += 1
            continue
        if re.match(r"^ {0,3}>", line):
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_table:
                out.append("</tbody></table>")
                in_table = False
            quoted: list[str] = []
            while index < len(lines) and re.match(r"^ {0,3}>", lines[index]):
                quoted.append(re.sub(r"^ {0,3}> ?", "", lines[index]))
                index += 1
            out.append("<blockquote>" + render_markdown("\n".join(quoted)) + "</blockquote>")
            continue
        if in_list and not re.match(r"^[-*]\s+", stripped):
            out.append("</ul>")
            in_list = False
        if in_table and not stripped.startswith("|"):
            out.append("</tbody></table>")
            in_table = False
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            out.append(f'<h{level} id="{anchor}">{inline(title)}</h{level}>')
        elif re.match(r"^[-*]\s+", stripped):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(re.sub(r'^[-*]\\s+', '', stripped))}</li>")
        elif stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                index += 1
                continue
            if not in_table:
                out.append("<table><tbody>")
                in_table = True
            out.append("<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in cells) + "</tr>")
        elif stripped:
            out.append(f"<p>{inline(stripped)}</p>")
        index += 1
    if in_list:
        out.append("</ul>")
    if in_table:
        out.append("</tbody></table>")
    return "\n".join(out)


def render(source: Path) -> str:
    doc = parse_sow(source)
    issues = validate_document(doc)
    if issues:
        raise SowError("source validation failed: " + "; ".join(issues))
    title_match = re.search(r"^#\s+(.+)$", doc.body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else str(doc.frontmatter["deliverable_id"])
    body = render_markdown(doc.body)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="chirality-canonical-schema" content="{SCHEMA}">
<meta name="chirality-canonical-sha256" content="{doc.sha256}">
<meta name="chirality-renderer-version" content="{RENDERER_VERSION}">
<title>{html.escape(title)}</title>
<style>body{{font:16px/1.55 system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem}}table{{border-collapse:collapse;width:100%}}td{{border:1px solid #bbb;padding:.4rem;vertical-align:top}}code{{background:#eee;padding:.1rem .2rem}}blockquote{{border-left:.25rem solid #bbb;margin:1rem 0;padding:.25rem 1rem;color:#333}}</style>
</head>
<body>
<p><strong>Derivative view.</strong> Canonical source: <code>ScopeOfWork.md</code>; SHA-256: <code>{doc.sha256}</code>.</p>
{body}
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    args = parser.parse_args()
    try:
        resolution = resolve_production_format(
            args.source.parent,
            isolated_migration=args.isolated_migration,
            migration_authority=args.migration_authority,
        )
        if resolution.state not in {"SOW_V1", "MIGRATION_DUAL"} or not resolution.valid:
            raise SowError(f"format state is {resolution.state}: {'; '.join(resolution.issues)}")
        output = render(args.source)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8", newline="\n")
        else:
            sys.stdout.write(output)
        return 0
    except (OSError, UnicodeError, SowError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
