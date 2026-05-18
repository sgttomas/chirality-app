#!/usr/bin/env python3
"""
Apply user-submitted equation corrections from an audit `flagged.json`.

Each flagged entry's `description` field MUST already be the corrected LaTeX
expression (not a natural-language note). The EQUATION_AUDIT persona's
Phase 3a converts any prose notes to LaTeX via the `equation-flag-interpret`
skill before this tool runs; the persona's Phase 3b runs
`validate_flagged_schema.py` to confirm before reaching Phase 3c. This tool
also runs the validator itself as a fail-fast gate.

This tool then finds each equation in the per-page Markdown by hash, replaces
the LaTeX in both `page_NNNN.md` and `page_NNNN.anchored.md`, reassembles +
cleans the source document, and writes `backcheck.json` so the regenerated
audit displays the post-fix equations under the Backcheck status.

The existing `flagged.json` is archived to `flagged.json.<timestamp>.bak`
and replaced with `{}` (no flags pending). `verified.json` is untouched.

This tool is deterministic: it does NOT shell out to any LLM. LLM reasoning
belongs in the `equation-flag-interpret` skill (see AGENT_HELPS_HUMANS R12).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)


def eqhash(latex: str) -> str:
    return hashlib.sha1(latex.strip().encode("utf-8")).hexdigest()[:12]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--audit-dir", required=True, help="directory holding flagged.json (and where backcheck.json will be written) — usually <book>/audit/equations/working/")
    p.add_argument("--work-dir", required=True, help="per-page _pdf2md_work directory")
    p.add_argument("--source-md", required=True, help="assembled <stem>.md path to regenerate")
    p.add_argument("--title", required=True, help="title used by audit_equations.py")
    p.add_argument("--flagged-json", default=None, help="override path to flagged.json (defaults to <audit-dir>/flagged.json)")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def apply_to_file(path: Path, target_hash: str, new_latex: str) -> tuple[bool, str | None]:
    """Replace the equation matching target_hash in `path`. Returns (changed, prev_latex_seen)."""
    if not path.exists():
        return (False, None)
    text = path.read_text(encoding="utf-8")
    for m in DISPLAY_RE.finditer(text):
        if eqhash(m.group(1)) == target_hash:
            prev = m.group(1).strip()
            new_text = text[: m.start(1)] + new_latex + text[m.end(1) :]
            path.write_text(new_text, encoding="utf-8")
            return (True, prev)
    return (False, None)


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> int:
    args = parse_args()
    audit_dir = Path(args.audit_dir).resolve()
    work_dir = Path(args.work_dir).resolve()
    source_md = Path(args.source_md).resolve()
    if args.flagged_json:
        flagged_path = Path(args.flagged_json).resolve()
    else:
        canonical = audit_dir / "flagged.json"
        if canonical.exists() and json.loads(canonical.read_text(encoding="utf-8") or "{}"):
            flagged_path = canonical
        else:
            # Pick the most recent <slug>_flagged_<ts>.json in audit_dir
            candidates = sorted(audit_dir.glob("*_flagged_*.json"))
            if candidates:
                flagged_path = candidates[-1]
                print(f"using latest exported flagged file: {flagged_path.name}")
            else:
                flagged_path = canonical
    backcheck_path = audit_dir / "backcheck.json"

    if not flagged_path.exists():
        print(f"flagged file not found: {flagged_path}", file=sys.stderr)
        return 1
    flagged = json.loads(flagged_path.read_text(encoding="utf-8"))
    if not flagged:
        print("flagged.json is empty — nothing to do")
        return 0

    # Fail-fast schema gate: refuse to apply if any description is prose-shaped
    # or any required field is missing. The EQUATION_AUDIT persona's Phase 3a
    # is responsible for converting prose to LaTeX via equation-flag-interpret.
    # The gate is unconditional — R12 says LLM reasoning belongs in the skill,
    # not in this tool, and this gate is what enforces it.
    validator = Path(__file__).parent / "validate_flagged_schema.py"
    result = subprocess.run(
        [sys.executable, str(validator), "--flagged-json", str(flagged_path)],
        capture_output=True, text=True,
    )
    sys.stdout.write(result.stdout)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        print(
            "\nERROR: flagged.json failed schema validation. Run "
            "equation-flag-interpret via TASK first, or supply LaTeX-shaped "
            "descriptions directly. See the per-entry errors above.",
            file=sys.stderr,
        )
        return 4

    existing_backcheck = {}
    if backcheck_path.exists():
        try:
            existing_backcheck = json.loads(backcheck_path.read_text(encoding="utf-8"))
        except Exception:
            existing_backcheck = {}

    new_backcheck_entries: dict[str, dict] = {}
    today = dt.date.today().isoformat()
    failures: list[dict] = []

    for key, entry in flagged.items():
        page = int(entry["page"])
        target_hash = entry["hash"]
        raw_note = entry.get("description", "").strip()
        if not raw_note:
            failures.append({"key": key, "reason": "empty description"})
            continue
        new_latex = raw_note

        plain = work_dir / f"page_{page:04d}.md"
        anchored = work_dir / f"page_{page:04d}.anchored.md"

        if args.dry_run:
            print(f"[dry-run] page={page} hash={target_hash} -> new_hash={eqhash(new_latex)}")
            continue

        changed_plain, prev_plain = apply_to_file(plain, target_hash, new_latex)
        changed_anch, prev_anch = apply_to_file(anchored, target_hash, new_latex)

        if not changed_plain and not changed_anch:
            failures.append({"key": key, "reason": f"equation hash {target_hash} not found on page {page}"})
            continue
        if changed_plain != changed_anch:
            print(f"WARN: page {page} hash {target_hash} present in only one of page_{page:04d}.md / .anchored.md", file=sys.stderr)

        prev_latex = entry.get("current_latex") or prev_plain or prev_anch or ""
        new_hash = eqhash(new_latex)
        new_key = f"{page}:{new_hash}"
        new_backcheck_entries[new_key] = {
            "page": page,
            "hash": new_hash,
            "prev_hash": target_hash,
            "prev_latex": prev_latex,
            "new_latex": new_latex,
            "description": entry.get("description", ""),
            "flagged_at": entry.get("flagged_at", ""),
            "applied_at": today,
        }
        print(f"applied: page={page} {target_hash} -> {new_hash}")

    if failures:
        print("FAILURES:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        if not new_backcheck_entries:
            print("no successful applications — aborting before reassembly", file=sys.stderr)
            return 2

    if args.dry_run:
        print("dry-run: skipping reassembly + sidecar writes")
        return 0

    # Reassemble + clean
    repo_root = Path(__file__).resolve().parents[2]
    run([
        sys.executable, str(repo_root / "tools/pdf2md/assemble_markdown.py"),
        str(work_dir), str(source_md),
        "--separator", "---",
        "--page-template", "page_{page:04d}.anchored.md",
    ])
    run([
        sys.executable, str(repo_root / "tools/reporting/clean_pdf2md_output.py"),
        str(source_md),
    ])

    # Merge backcheck.json: existing + new, prune any keys that are in verified.json
    verified_path = audit_dir / "verified.json"
    verified = {}
    if verified_path.exists():
        try:
            verified = json.loads(verified_path.read_text(encoding="utf-8"))
        except Exception:
            verified = {}
    merged = {**existing_backcheck, **new_backcheck_entries}
    pruned = {k: v for k, v in merged.items() if k not in verified}
    backcheck_path.write_text(json.dumps(pruned, indent=2), encoding="utf-8")
    print(f"backcheck.json: {len(pruned)} entries (new={len(new_backcheck_entries)}, pruned={len(merged) - len(pruned)})")

    # Archive flagged.json and reset to {}
    stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    backup = flagged_path.with_suffix(f".json.{stamp}.bak")
    shutil.copy2(flagged_path, backup)
    flagged_path.write_text("{}\n", encoding="utf-8")
    print(f"flagged.json archived to {backup.name} and reset to empty")

    # Re-run audit (same-dir tool reference; survives subsystem relocation)
    run([
        sys.executable, str(Path(__file__).parent / "audit_equations.py"),
        "--work-dir", str(work_dir),
        "--out-html", str(audit_dir / "equations.html"),
        "--out-jsonl", str(audit_dir / "equations.jsonl"),
        "--title", args.title,
    ])

    print(f"done. applied={len(new_backcheck_entries)} failures={len(failures)}")
    return 0 if not failures else 3


if __name__ == "__main__":
    raise SystemExit(main())
