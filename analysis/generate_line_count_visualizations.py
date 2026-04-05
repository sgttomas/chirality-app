from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


ANALYSIS_DIR = Path("/Users/ryan/ai-env/projects/chirality-app/analysis")
SOURCE_CSV = ANALYSIS_DIR / "repo_file_inventory_filtered_core_2026-04-04.csv"
BUCKET_CSV = ANALYSIS_DIR / "line_count_bucket_counts_10_core_2026-04-04.csv"
SUMMARY_MD = ANALYSIS_DIR / "line_count_bucket_counts_10_core_summary_2026-04-04.md"
COMBINED_SVG = ANALYSIS_DIR / "line_count_distribution_core_10line_buckets.svg"
PER_SCOPE_DIR = ANALYSIS_DIR / "line_count_distributions_10line"
BUCKET_SIZE = 10
SCOPES = ["root", "docs", "plans", "agents", "skills", "tools"]


@dataclass(frozen=True)
class ScopeStats:
    scope_group: str
    file_count: int
    max_line_count: int
    populated_bucket_count: int
    most_populated_bucket_label: str
    most_populated_bucket_files: int


def read_scope_line_counts() -> dict[str, list[int]]:
    scope_counts: dict[str, list[int]] = defaultdict(list)
    with SOURCE_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scope = row["scope_group"]
            line_count_text = row["line_count"]
            line_count = int(line_count_text) if line_count_text else 0
            scope_counts[scope].append(line_count)
    return {scope: scope_counts.get(scope, []) for scope in SCOPES}


def bucket_start(line_count: int) -> int:
    return (line_count // BUCKET_SIZE) * BUCKET_SIZE


def bucket_label(start: int) -> str:
    end = start + BUCKET_SIZE - 1
    return f"{start}-{end}"


def build_bucket_rows(scope_line_counts: dict[str, list[int]]) -> tuple[list[dict[str, int | str]], list[ScopeStats], int]:
    max_line_count = max((max(counts) for counts in scope_line_counts.values() if counts), default=0)
    max_bucket_start = bucket_start(max_line_count)
    all_bucket_starts = list(range(0, max_bucket_start + BUCKET_SIZE, BUCKET_SIZE))

    rows: list[dict[str, int | str]] = []
    scope_stats: list[ScopeStats] = []

    for scope in SCOPES:
        counts = scope_line_counts.get(scope, [])
        counter = Counter(bucket_start(value) for value in counts)
        most_populated_bucket_start, most_populated_bucket_files = max(
            counter.items(),
            key=lambda item: (item[1], -item[0]),
            default=(0, 0),
        )
        scope_stats.append(
            ScopeStats(
                scope_group=scope,
                file_count=len(counts),
                max_line_count=max(counts, default=0),
                populated_bucket_count=sum(1 for value in counter.values() if value > 0),
                most_populated_bucket_label=bucket_label(most_populated_bucket_start),
                most_populated_bucket_files=most_populated_bucket_files,
            )
        )
        for start in all_bucket_starts:
            rows.append(
                {
                    "scope_group": scope,
                    "bucket_start": start,
                    "bucket_end": start + BUCKET_SIZE - 1,
                    "bucket_label": bucket_label(start),
                    "file_count": counter.get(start, 0),
                }
            )
    return rows, scope_stats, max_bucket_start


def write_bucket_csv(rows: list[dict[str, int | str]]) -> None:
    with BUCKET_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["scope_group", "bucket_start", "bucket_end", "bucket_label", "file_count"],
        )
        writer.writeheader()
        writer.writerows(rows)


def render_scope_chart(
    *,
    title: str,
    bucket_rows: list[dict[str, int | str]],
    max_bucket_count: int,
    width: int = 980,
    height: int = 360,
    show_all_x_labels: bool = False,
) -> str:
    margin_left = 70
    margin_right = 20
    margin_top = 40
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    bar_gap = 1
    num_bars = len(bucket_rows)
    bar_width = max(1.0, (plot_width / max(num_bars, 1)) - bar_gap)

    x_label_step = 1 if show_all_x_labels else max(1, num_bars // 12)
    y_ticks = 5

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
        '<rect width="100%" height="100%" fill="#f8fafc" />',
        f'<text x="{margin_left}" y="24" font-family="Menlo, Consolas, monospace" font-size="16" fill="#0f172a">{escape(title)}</text>',
        f'<text x="{margin_left}" y="42" font-family="Menlo, Consolas, monospace" font-size="11" fill="#475569">Bucket size: {BUCKET_SIZE} lines</text>',
    ]

    plot_x1 = margin_left
    plot_y1 = margin_top
    plot_x2 = margin_left + plot_width
    plot_y2 = margin_top + plot_height

    for tick_index in range(y_ticks + 1):
        tick_value = round((max_bucket_count / y_ticks) * tick_index) if max_bucket_count else 0
        y = plot_y2 - (plot_height * tick_index / y_ticks)
        parts.append(
            f'<line x1="{plot_x1}" y1="{y:.2f}" x2="{plot_x2}" y2="{y:.2f}" stroke="#cbd5e1" stroke-width="1" />'
        )
        parts.append(
            f'<text x="{margin_left - 8}" y="{y + 4:.2f}" text-anchor="end" font-family="Menlo, Consolas, monospace" font-size="10" fill="#334155">{tick_value}</text>'
        )

    parts.append(
        f'<line x1="{plot_x1}" y1="{plot_y2}" x2="{plot_x2}" y2="{plot_y2}" stroke="#0f172a" stroke-width="1.5" />'
    )
    parts.append(
        f'<line x1="{plot_x1}" y1="{plot_y1}" x2="{plot_x1}" y2="{plot_y2}" stroke="#0f172a" stroke-width="1.5" />'
    )

    for index, row in enumerate(bucket_rows):
        count = int(row["file_count"])
        bar_height = 0 if max_bucket_count == 0 else (count / max_bucket_count) * plot_height
        x = margin_left + index * (bar_width + bar_gap)
        y = plot_y2 - bar_height
        label = str(row["bucket_label"])
        parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" fill="#2563eb">'
            f'<title>{escape(label)}: {count} files</title></rect>'
        )
        if index % x_label_step == 0 or index == num_bars - 1:
            parts.append(
                f'<text x="{x + (bar_width / 2):.2f}" y="{plot_y2 + 18:.2f}" text-anchor="middle" '
                f'font-family="Menlo, Consolas, monospace" font-size="9" fill="#475569" '
                f'transform="rotate(45 {x + (bar_width / 2):.2f} {plot_y2 + 18:.2f})">{escape(label)}</text>'
            )

    parts.append(
        f'<text x="{margin_left + (plot_width / 2):.2f}" y="{height - 12}" text-anchor="middle" font-family="Menlo, Consolas, monospace" font-size="11" fill="#334155">Line-count bucket</text>'
    )
    parts.append(
        f'<text x="18" y="{margin_top + (plot_height / 2):.2f}" text-anchor="middle" font-family="Menlo, Consolas, monospace" font-size="11" fill="#334155" transform="rotate(-90 18 {margin_top + (plot_height / 2):.2f})">Files in bucket</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def write_scope_svgs(rows: list[dict[str, int | str]]) -> list[Path]:
    PER_SCOPE_DIR.mkdir(exist_ok=True)
    rows_by_scope: dict[str, list[dict[str, int | str]]] = defaultdict(list)
    for row in rows:
        rows_by_scope[str(row["scope_group"])].append(row)

    max_bucket_count = max((int(row["file_count"]) for row in rows), default=0)
    output_paths: list[Path] = []

    for scope in SCOPES:
        svg_text = render_scope_chart(
            title=f"{scope}/ line-count distribution",
            bucket_rows=rows_by_scope[scope],
            max_bucket_count=max_bucket_count,
        )
        output_path = PER_SCOPE_DIR / f"{scope}_line_count_distribution_10line_buckets.svg"
        output_path.write_text(svg_text, encoding="utf-8")
        output_paths.append(output_path)
    return output_paths


def render_combined_svg(rows: list[dict[str, int | str]]) -> None:
    rows_by_scope: dict[str, list[dict[str, int | str]]] = defaultdict(list)
    for row in rows:
        rows_by_scope[str(row["scope_group"])].append(row)

    panel_width = 600
    panel_height = 280
    columns = 2
    rows_count = 3
    width = panel_width * columns
    height = panel_height * rows_count + 50
    max_bucket_count = max((int(row["file_count"]) for row in rows), default=0)

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Line-count distributions by scope">',
        '<rect width="100%" height="100%" fill="#e2e8f0" />',
        '<text x="24" y="28" font-family="Menlo, Consolas, monospace" font-size="20" fill="#0f172a">Line-count distributions by scope</text>',
        f'<text x="24" y="46" font-family="Menlo, Consolas, monospace" font-size="11" fill="#334155">Source: {escape(SOURCE_CSV.name)} | Bucket size: {BUCKET_SIZE} lines</text>',
    ]

    for index, scope in enumerate(SCOPES):
        panel_x = (index % columns) * panel_width
        panel_y = 60 + (index // columns) * panel_height
        inner = render_scope_chart(
            title=f"{scope}/",
            bucket_rows=rows_by_scope[scope],
            max_bucket_count=max_bucket_count,
            width=panel_width,
            height=panel_height,
        )
        inner_lines = inner.splitlines()
        inner_content = "\n".join(inner_lines[1:-1])
        parts.append(
            f'<svg x="{panel_x}" y="{panel_y}" width="{panel_width}" height="{panel_height}" viewBox="0 0 {panel_width} {panel_height}">'
        )
        parts.append(inner_content)
        parts.append("</svg>")

    parts.append("</svg>")
    COMBINED_SVG.write_text("\n".join(parts), encoding="utf-8")


def write_summary(scope_stats: list[ScopeStats]) -> None:
    lines = [
        "# Line-Count Bucket Summary",
        "",
        f"- Generated at: {datetime.now().astimezone().isoformat()}",
        f"- Source CSV: `analysis/{SOURCE_CSV.name}`",
        f"- Bucket CSV: `analysis/{BUCKET_CSV.name}`",
        f"- Combined SVG: `analysis/{COMBINED_SVG.name}`",
        f"- Per-scope SVG directory: `analysis/{PER_SCOPE_DIR.name}/`",
        f"- Bucket size: {BUCKET_SIZE} lines",
        "",
        "## Scope Summary",
        "",
        "| scope_group | file_count | max_line_count | populated_bucket_count | most_populated_bucket | files_in_most_populated_bucket |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in scope_stats:
        lines.append(
            f"| {item.scope_group} | {item.file_count} | {item.max_line_count} | {item.populated_bucket_count} | {item.most_populated_bucket_label} | {item.most_populated_bucket_files} |"
        )
    lines.append("")
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    scope_line_counts = read_scope_line_counts()
    bucket_rows, scope_stats, _max_bucket_start = build_bucket_rows(scope_line_counts)
    write_bucket_csv(bucket_rows)
    write_scope_svgs(bucket_rows)
    render_combined_svg(bucket_rows)
    write_summary(scope_stats)
    print(f"Wrote bucket CSV to {BUCKET_CSV}")
    print(f"Wrote summary to {SUMMARY_MD}")
    print(f"Wrote combined SVG to {COMBINED_SVG}")
    print(f"Wrote per-scope SVGs to {PER_SCOPE_DIR}")


if __name__ == "__main__":
    main()
