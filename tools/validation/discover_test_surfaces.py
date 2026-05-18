#!/usr/bin/env python3
"""
Discover test surfaces by repository convention.

This tool is read-only. It reports discovered test files, runner families,
suggested commands, and symbol counts as generated output rather than storing
mutable test inventory counts in docs.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


PY_TEST_RE = re.compile(r"^\s*(?:async\s+)?def\s+test_[A-Za-z0-9_]*\s*\(", re.MULTILINE)
PY_CLASS_RE = re.compile(r"^\s*class\s+Test[A-Za-z0-9_]*\b", re.MULTILINE)
VITEST_RE = re.compile(r"\b(?:it|test)(?:\.\w+)?\s*\(")
RUST_TEST_RE = re.compile(r"#\[(?:[A-Za-z0-9_]+::)*test\]")


@dataclass(frozen=True)
class FileFinding:
    path: str
    symbol_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discover repo test surfaces.")
    parser.add_argument(
        "repo_root",
        nargs="?",
        default=".",
        help="Repository root to scan (default: current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON. This is the default; retained for explicit callers.",
    )
    parser.add_argument("--text", action="store_true", help="Emit a human-readable summary.")
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def count_python_tests(path: Path) -> int:
    text = read_text(path)
    return len(PY_TEST_RE.findall(text)) + len(PY_CLASS_RE.findall(text))


def count_vitest_tests(path: Path) -> int:
    return len(VITEST_RE.findall(read_text(path)))


def count_rust_tests(path: Path) -> int:
    return len(RUST_TEST_RE.findall(read_text(path)))


def files_under(root: Path, patterns: Iterable[str]) -> list[Path]:
    if not root.exists():
        return []
    files: set[Path] = set()
    for pattern in patterns:
        files.update(path for path in root.rglob(pattern) if path.is_file())
    return sorted(files)


def file_findings(
    paths: Iterable[Path],
    repo_root: Path,
    counter: Callable[[Path], int],
) -> list[FileFinding]:
    findings: list[FileFinding] = []
    for path in sorted(paths):
        count = counter(path)
        if count > 0:
            findings.append(FileFinding(rel(path, repo_root), count))
    return findings


def surface(
    *,
    surface_id: str,
    label: str,
    runner: str,
    root: Path,
    repo_root: Path,
    command: str,
    findings: list[FileFinding],
) -> dict:
    return {
        "id": surface_id,
        "label": label,
        "runner": runner,
        "root": rel(root, repo_root),
        "suggested_command": command,
        "file_count": len(findings),
        "test_symbol_count": sum(item.symbol_count for item in findings),
        "files": [item.__dict__ for item in findings],
    }


def discover(repo_root: Path) -> dict:
    repo_root = repo_root.resolve()

    tools_root = repo_root / "tools"
    app_tests_root = repo_root / "projects/chirality-app-dev/frontend/src/__tests__"
    piping_tests_root = repo_root / "projects/chirality-piping/tests"
    desktop_root = repo_root / "projects/chirality-piping/apps/desktop"
    piping_root = repo_root / "projects/chirality-piping"

    surfaces = [
        surface(
            surface_id="tools-python",
            label="Root deterministic tool Python tests",
            runner="pytest",
            root=tools_root,
            repo_root=repo_root,
            command="python3 -m pytest -q tools",
            findings=file_findings(
                files_under(tools_root, ["test_*.py", "*_test.py"]),
                repo_root,
                count_python_tests,
            ),
        ),
        surface(
            surface_id="chirality-app-dev-frontend-vitest",
            label="Chirality app frontend Vitest tests",
            runner="vitest",
            root=app_tests_root,
            repo_root=repo_root,
            command="cd projects/chirality-app-dev/frontend && npm test",
            findings=file_findings(
                files_under(app_tests_root, ["*.test.ts", "*.test.tsx", "*.spec.ts", "*.spec.tsx"]),
                repo_root,
                count_vitest_tests,
            ),
        ),
        surface(
            surface_id="openpipestress-pytest",
            label="OpenPipeStress Python tests",
            runner="pytest",
            root=piping_tests_root,
            repo_root=repo_root,
            command="cd projects/chirality-piping && python3 -m pytest -q tests",
            findings=file_findings(
                files_under(piping_tests_root, ["test_*.py", "*_test.py"]),
                repo_root,
                count_python_tests,
            ),
        ),
        surface(
            surface_id="openpipestress-desktop-vitest",
            label="OpenPipeStress desktop Vitest tests",
            runner="vitest",
            root=desktop_root,
            repo_root=repo_root,
            command="cd projects/chirality-piping && npm test --workspace apps/desktop",
            findings=file_findings(
                files_under(desktop_root, ["*.test.ts", "*.test.tsx", "*.spec.ts", "*.spec.tsx"]),
                repo_root,
                count_vitest_tests,
            ),
        ),
        surface(
            surface_id="openpipestress-rust",
            label="OpenPipeStress Rust crate tests",
            runner="cargo",
            root=piping_root,
            repo_root=repo_root,
            command="Run cargo test for each crate with tests: cargo test --manifest-path <crate>/Cargo.toml",
            findings=file_findings(files_under(piping_root, ["*.rs"]), repo_root, count_rust_tests),
        ),
    ]

    return {
        "schema": "chirality-test-surfaces/v1",
        "repo_root": str(repo_root),
        "surfaces": surfaces,
        "totals": {
            "surface_count": len(surfaces),
            "file_count": sum(item["file_count"] for item in surfaces),
            "test_symbol_count": sum(item["test_symbol_count"] for item in surfaces),
        },
    }


def emit_text(report: dict) -> str:
    lines = ["Test surfaces:"]
    for item in report["surfaces"]:
        lines.append(
            f"- {item['id']}: {item['file_count']} files, "
            f"{item['test_symbol_count']} symbols, runner={item['runner']}"
        )
        lines.append(f"  command: {item['suggested_command']}")
    totals = report["totals"]
    lines.append(
        f"Totals: {totals['surface_count']} surfaces, "
        f"{totals['file_count']} files, {totals['test_symbol_count']} symbols"
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    report = discover(Path(args.repo_root))
    if args.text:
        print(emit_text(report))
    else:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
