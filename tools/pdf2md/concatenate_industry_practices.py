#!/usr/bin/env python3
"""
Concatenate the industry-practices per-PDF Markdown files into one root document.

The input corpus is arranged as:
    ROOT/NN-chapter/chapter-stem-XX.pdf
    ROOT/NN-chapter/chapter-stem-XX.md

Per-PDF Markdown links point at asset paths relative to that PDF's chapter
folder. This tool rewrites those links so they resolve from ROOT.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


INLINE_DEST_RE = re.compile(r"(?<!\\)\]\(([^)]+)\)")
REFERENCE_DEF_RE = re.compile(r"(^\s*\[[^\]]+\]:\s*)(\S+)", re.MULTILINE)
HTML_IMG_SRC_RE = re.compile(r"(<img\b[^>]*\bsrc=[\"'])([^\"']+)([\"'])", re.IGNORECASE)
ASSET_DIRS = ("figures", "tables", "images")


@dataclass(frozen=True)
class SourceDoc:
    chapter_dir: Path
    pdf_path: Path
    md_path: Path
    stem: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Concatenate industry-practices per-PDF Markdown.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def is_asset_path(path: str) -> bool:
    return any(part in ASSET_DIRS for part in Path(path).parts)


def split_suffix(target: str) -> tuple[str, str]:
    suffix = ""
    for sep in ("#", "?"):
        if sep in target:
            target, tail = target.split(sep, 1)
            suffix = sep + tail
            break
    return target, suffix


def asset_prefix(root: Path, source: SourceDoc, asset_rel: str) -> str:
    chapter_rel = source.chapter_dir.relative_to(root).as_posix()
    new_root = source.chapter_dir / "_assets" / source.stem
    legacy_root = source.chapter_dir / f"{source.stem}_assets"
    if (new_root / asset_rel).exists():
        return f"{chapter_rel}/_assets/{source.stem}/{asset_rel}"
    if (legacy_root / asset_rel).exists():
        return f"{chapter_rel}/{source.stem}_assets/{asset_rel}"
    if new_root.exists():
        return f"{chapter_rel}/_assets/{source.stem}/{asset_rel}"
    return f"{chapter_rel}/{source.stem}_assets/{asset_rel}"


def rewrite_target(root: Path, source: SourceDoc, raw_target: str) -> tuple[str, bool]:
    target = raw_target.strip().strip("<>")
    if target.startswith(("./", "../")):
        target = target[2:] if target.startswith("./") else target
    path_part, suffix = split_suffix(target)
    if not is_asset_path(path_part):
        return raw_target, False

    parts = Path(path_part).parts
    first_asset_idx = next((i for i, part in enumerate(parts) if part in ASSET_DIRS), None)
    if first_asset_idx is None:
        return raw_target, False
    asset_rel = Path(*parts[first_asset_idx:]).as_posix()
    return asset_prefix(root, source, asset_rel) + suffix, True


def rewrite_asset_links(text: str, root: Path, source: SourceDoc) -> tuple[str, int]:
    rewritten_count = 0

    def inline_repl(match: re.Match[str]) -> str:
        nonlocal rewritten_count
        new_target, changed = rewrite_target(root, source, match.group(1))
        if changed:
            rewritten_count += 1
        return match.group(0).replace(match.group(1), new_target, 1)

    text = INLINE_DEST_RE.sub(inline_repl, text)

    def reference_repl(match: re.Match[str]) -> str:
        nonlocal rewritten_count
        new_target, changed = rewrite_target(root, source, match.group(2))
        if changed:
            rewritten_count += 1
        return f"{match.group(1)}{new_target}"

    text = REFERENCE_DEF_RE.sub(reference_repl, text)

    def html_repl(match: re.Match[str]) -> str:
        nonlocal rewritten_count
        new_target, changed = rewrite_target(root, source, match.group(2))
        if changed:
            rewritten_count += 1
        return f"{match.group(1)}{new_target}{match.group(3)}"

    text = HTML_IMG_SRC_RE.sub(html_repl, text)
    return text, rewritten_count


def prettify_chapter(folder_name: str) -> str:
    name = re.sub(r"^\d{2}-", "", folder_name)
    return name.replace("-", " ").title()


def collect_sources(root: Path) -> list[SourceDoc]:
    sources: list[SourceDoc] = []
    for pdf_path in sorted(root.glob("[0-9][0-9]-*/*.pdf")):
        md_path = pdf_path.with_suffix(".md")
        if md_path.is_file():
            sources.append(
                SourceDoc(
                    chapter_dir=pdf_path.parent,
                    pdf_path=pdf_path,
                    md_path=md_path,
                    stem=pdf_path.stem,
                )
            )
    return sources


def concatenate(root: Path, output: Path) -> tuple[int, int, int, list[str]]:
    sources = collect_sources(root)
    chunks: list[str] = []
    seen_chapters: set[Path] = set()
    rewritten_links = 0
    empty_inputs: list[str] = []

    for source in sources:
        raw = source.md_path.read_text(encoding="utf-8").strip()
        if not raw:
            empty_inputs.append(str(source.md_path.relative_to(root)))
        text, count = rewrite_asset_links(raw, root, source)
        rewritten_links += count

        headings: list[str] = []
        if source.chapter_dir not in seen_chapters:
            headings.append(f"## {prettify_chapter(source.chapter_dir.name)}")
            seen_chapters.add(source.chapter_dir)
        headings.append(f"### {source.stem}")
        chunks.append("\n\n".join(headings + [text]).strip())

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(("\n\n---\n\n".join(chunks)).rstrip() + "\n", encoding="utf-8")
    return len(sources), len(seen_chapters), rewritten_links, empty_inputs


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    if not root.is_dir():
        raise SystemExit(f"ERROR: root is not a directory: {root}")
    source_count, chapter_count, rewritten_links, empty_inputs = concatenate(root, output)
    print(f"sources={source_count}")
    print(f"chapters={chapter_count}")
    print(f"rewritten_links={rewritten_links}")
    print(f"bytes={output.stat().st_size}")
    if empty_inputs:
        print(f"empty_inputs={len(empty_inputs)}")
        for item in empty_inputs[:50]:
            print(f"  - {item}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
