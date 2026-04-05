from __future__ import annotations

import csv
import os
import stat as statmod
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO = Path("/Users/ryan/ai-env/projects/chirality-app").resolve()
ANALYSIS_DIR = REPO / "analysis"
CSV_PATH = ANALYSIS_DIR / "repo_file_inventory_filtered_core_2026-04-04.csv"
SUMMARY_PATH = ANALYSIS_DIR / "repo_file_inventory_filtered_core_summary_2026-04-04.md"
ALLOWED_ROOT_DIRS = {"docs", "plans", "agents", "skills", "tools"}
EXCLUDED_ROOT_FILES = {"analysis"}
ALLOWED_SCOPES = ["root", "docs", "plans", "agents", "skills", "tools"]


@dataclass(frozen=True)
class SummaryRecord:
    relative_path: str
    byte_size: int
    line_count: int
    mtime_epoch: float
    mtime_local: str


def git_tracked_paths() -> set[str]:
    result = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    output = result.stdout.decode("utf-8", errors="surrogateescape")
    return {path for path in output.split("\0") if path}


def count_lines_and_binary(path: Path, *, is_symlink: bool) -> tuple[int | None, bool | None, str]:
    if is_symlink:
        return None, None, ""

    newline_count = 0
    last_byte = None
    first_chunk = b""

    try:
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                if not first_chunk:
                    first_chunk = chunk[:8192]
                newline_count += chunk.count(b"\n")
                last_byte = chunk[-1]
    except Exception as exc:  # noqa: BLE001
        return None, None, f"{type(exc).__name__}: {exc}"

    size = path.stat().st_size
    if size == 0:
        line_count = 0
    elif last_byte == 0x0A:
        line_count = newline_count
    else:
        line_count = newline_count + 1

    is_probably_binary = b"\x00" in first_chunk
    return line_count, is_probably_binary, ""


def fmt_bytes(num: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(num)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{num} B"


def local_folder(parent: Path) -> str:
    if parent == Path("."):
        return "."
    return "/".join(parent.parts[-2:])


def update_top(
    items: list[SummaryRecord],
    record: SummaryRecord,
    *,
    key,
    reverse: bool = True,
    limit: int = 20,
) -> None:
    items.append(record)
    items.sort(key=key, reverse=reverse)
    del items[limit:]


def walk_subset() -> list[Path]:
    found: list[Path] = []

    with os.scandir(REPO) as iterator:
        top_entries = sorted(iterator, key=lambda entry: entry.name)

    for entry in top_entries:
        full_path = Path(entry.path)
        rel_path = full_path.relative_to(REPO)
        rel_path_str = rel_path.as_posix()

        if entry.is_dir(follow_symlinks=False):
            if rel_path_str in ALLOWED_ROOT_DIRS:
                stack = [full_path]
                while stack:
                    current = stack.pop()
                    with os.scandir(current) as child_iterator:
                        children = sorted(child_iterator, key=lambda child: child.name)
                    for child in children:
                        child_path = Path(child.path)
                        if child.is_dir(follow_symlinks=False):
                            stack.append(child_path)
                            continue
                        found.append(child_path)
            continue

        if rel_path_str in EXCLUDED_ROOT_FILES:
            continue
        found.append(full_path)

    found.sort(key=lambda path: path.relative_to(REPO).as_posix())
    return found


def table_lines(title: str, items: list[dict[str, object]], columns: list[str]) -> list[str]:
    lines = [
        f"## {title}",
        "",
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for item in items:
        lines.append("| " + " | ".join(str(item[column]) for column in columns) + " |")
    lines.append("")
    return lines


def scope_group(relative_path: str) -> str:
    if "/" not in relative_path:
        return "root"
    return relative_path.split("/", 1)[0]


def main() -> None:
    ANALYSIS_DIR.mkdir(exist_ok=True)
    tracked = git_tracked_paths()
    files = walk_subset()

    rows: list[dict[str, object]] = []
    errors: list[tuple[str, str]] = []

    scope_counts: Counter[str] = Counter()
    scope_bytes: Counter[str] = Counter()
    scope_lines: Counter[str] = Counter()
    scope_latest: dict[str, str] = {}
    ext_counter: Counter[str] = Counter()
    path_depth_counter: Counter[int] = Counter()
    binary_counter: Counter[str] = Counter()

    zero_byte_count = 0
    executable_count = 0
    tracked_count = 0
    symlink_count = 0
    total_bytes = 0
    total_lines = 0

    largest_by_size: list[SummaryRecord] = []
    largest_by_lines: list[SummaryRecord] = []
    newest_files: list[SummaryRecord] = []

    for full_path in files:
        rel_path = full_path.relative_to(REPO)
        rel_path_str = rel_path.as_posix()
        parent_rel = rel_path.parent
        parent_parts = () if parent_rel == Path(".") else parent_rel.parts

        try:
            st = full_path.lstat()
        except Exception as exc:  # noqa: BLE001
            errors.append((rel_path_str, f"{type(exc).__name__}: {exc}"))
            continue

        entry_type = "symlink" if statmod.S_ISLNK(st.st_mode) else "file"
        is_symlink = entry_type == "symlink"
        line_count, is_probably_binary, read_error = count_lines_and_binary(full_path, is_symlink=is_symlink)
        if read_error:
            errors.append((rel_path_str, read_error))

        extension = full_path.suffix.lower()
        modified = datetime.fromtimestamp(st.st_mtime).astimezone()
        modified_iso = modified.isoformat()
        tracked_in_git = rel_path_str in tracked
        current_scope = scope_group(rel_path_str)
        is_executable = bool(st.st_mode & 0o111) and not is_symlink

        if st.st_size == 0:
            zero_byte_count += 1
        if is_executable:
            executable_count += 1
        if tracked_in_git:
            tracked_count += 1
        if is_symlink:
            symlink_count += 1

        total_bytes += st.st_size
        if line_count is not None:
            total_lines += line_count

        scope_counts[current_scope] += 1
        scope_bytes[current_scope] += st.st_size
        scope_lines[current_scope] += 0 if line_count is None else line_count
        scope_latest[current_scope] = max(scope_latest.get(current_scope, ""), modified_iso)
        ext_counter[extension or "[no extension]"] += 1
        path_depth_counter[len(parent_parts)] += 1
        if is_probably_binary is None:
            binary_counter["not_scanned"] += 1
        elif is_probably_binary:
            binary_counter["binary"] += 1
        else:
            binary_counter["non_binary"] += 1

        rows.append(
            {
                "relative_path": rel_path_str,
                "file_name": full_path.name,
                "parent_dir_1": parent_parts[-1] if len(parent_parts) >= 1 else ".",
                "parent_dir_2": parent_parts[-2] if len(parent_parts) >= 2 else ".",
                "local_folder_max_2_parents": local_folder(parent_rel),
                "path_depth": len(parent_parts),
                "file_extension": extension,
                "byte_size": st.st_size,
                "line_count": "" if line_count is None else line_count,
                "entry_type": entry_type,
                "is_probably_binary": "" if is_probably_binary is None else str(is_probably_binary).lower(),
                "is_executable": str(is_executable).lower(),
                "mode_octal": oct(st.st_mode & 0o777),
                "mtime_local": modified_iso,
                "mtime_epoch": f"{st.st_mtime:.6f}",
                "tracked_in_git": str(tracked_in_git).lower(),
                "scope_group": current_scope,
                "read_error": read_error,
            }
        )

        summary_record = SummaryRecord(
            relative_path=rel_path_str,
            byte_size=st.st_size,
            line_count=-1 if line_count is None else line_count,
            mtime_epoch=st.st_mtime,
            mtime_local=modified_iso,
        )
        update_top(largest_by_size, summary_record, key=lambda item: (item.byte_size, item.relative_path))
        update_top(largest_by_lines, summary_record, key=lambda item: (item.line_count, item.relative_path))
        update_top(newest_files, summary_record, key=lambda item: (item.mtime_epoch, item.relative_path))

    fieldnames = [
        "relative_path",
        "file_name",
        "parent_dir_1",
        "parent_dir_2",
        "local_folder_max_2_parents",
        "path_depth",
        "file_extension",
        "byte_size",
        "line_count",
        "entry_type",
        "is_probably_binary",
        "is_executable",
        "mode_octal",
        "mtime_local",
        "mtime_epoch",
        "tracked_in_git",
        "scope_group",
        "read_error",
    ]

    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary_lines = [
        "# Filtered Repo File Inventory Summary",
        "",
        f"- Generated at: {datetime.now().astimezone().isoformat()}",
        f"- Repo root: `{REPO}`",
        "- Included scope: root-level files plus recursive contents of `docs/`, `plans/`, `agents/`, `skills/`, and `tools/`",
        f"- Output CSV: `analysis/{CSV_PATH.name}`",
        "",
        "## Totals",
        "",
        f"- Total entries: {len(rows)}",
        f"- Total bytes: {total_bytes} ({fmt_bytes(total_bytes)})",
        f"- Total counted lines: {total_lines}",
        f"- Zero-byte files: {zero_byte_count}",
        f"- Executable files: {executable_count}",
        f"- Symlinks: {symlink_count}",
        f"- Probable binary files: {binary_counter.get('binary', 0)}",
        f"- Probable non-binary files: {binary_counter.get('non_binary', 0)}",
        f"- Git-tracked files: {tracked_count}",
        f"- Read errors: {len(errors)}",
        "",
    ]

    summary_lines.extend(
        table_lines(
            "Scope Breakdown",
            [
                {
                    "scope_group": scope,
                    "file_count": scope_counts[scope],
                    "total_bytes": scope_bytes[scope],
                    "human_size": fmt_bytes(scope_bytes[scope]),
                    "total_lines": scope_lines[scope],
                    "latest_mtime_local": scope_latest.get(scope, ""),
                }
                for scope in ALLOWED_SCOPES
            ],
            ["scope_group", "file_count", "total_bytes", "human_size", "total_lines", "latest_mtime_local"],
        )
    )
    summary_lines.extend(
        table_lines(
            "Extensions By File Count",
            [
                {"file_extension": extension, "file_count": count}
                for extension, count in ext_counter.most_common(30)
            ],
            ["file_extension", "file_count"],
        )
    )
    summary_lines.extend(
        table_lines(
            "Path Depth Distribution",
            [
                {"path_depth": depth, "file_count": count}
                for depth, count in sorted(path_depth_counter.items())
            ],
            ["path_depth", "file_count"],
        )
    )
    summary_lines.extend(
        table_lines(
            "Largest Files By Size",
            [
                {
                    "relative_path": item.relative_path,
                    "byte_size": item.byte_size,
                    "human_size": fmt_bytes(item.byte_size),
                }
                for item in largest_by_size
            ],
            ["relative_path", "byte_size", "human_size"],
        )
    )
    summary_lines.extend(
        table_lines(
            "Largest Files By Line Count",
            [
                {
                    "relative_path": item.relative_path,
                    "line_count": item.line_count,
                }
                for item in largest_by_lines
            ],
            ["relative_path", "line_count"],
        )
    )
    summary_lines.extend(
        table_lines(
            "Newest Files By Filesystem Modified Time",
            [
                {
                    "relative_path": item.relative_path,
                    "mtime_local": item.mtime_local,
                }
                for item in newest_files
            ],
            ["relative_path", "mtime_local"],
        )
    )
    if errors:
        summary_lines.extend(
            table_lines(
                "Read Errors",
                [
                    {"relative_path": relative_path, "error": error}
                    for relative_path, error in errors[:100]
                ],
                ["relative_path", "error"],
            )
        )

    SUMMARY_PATH.write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"Wrote {len(rows)} rows to {CSV_PATH}")
    print(f"Wrote summary to {SUMMARY_PATH}")
    print(f"Total bytes: {total_bytes}")
    print(f"Total counted lines: {total_lines}")
    print(f"Read errors: {len(errors)}")


if __name__ == "__main__":
    main()
