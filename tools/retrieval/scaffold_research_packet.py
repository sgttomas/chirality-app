#!/usr/bin/env python3
"""Scaffold an immutable research packet (RCH_<UTC>_<slug>/) with canonical files.

Creates RESEARCH_NOTE.md, Query_Log.csv, Evidence_Map.csv, Amendment_Candidates.csv,
Open_Questions.csv, Conflicts.csv, and HANDOFF_STATE.md with canonical headers (per
agents/AGENT_RESEARCH.md, via research_packet.py) and refreshes {RESEARCH_ROOT}/_LATEST.md.
Refuses to overwrite an existing packet (packets are immutable run snapshots), so the packet
shape is never re-derived by reasoning.

Usage:
  python3 tools/retrieval/scaffold_research_packet.py \
      --research-root domains/chirality-app-dev/_Research \
      --slug runtime_stabilization --topic "Evidence basis for X"

Inputs:
  --research-root PATH   Where packets live ({domain}/_Research). Required.
  --slug STR             Human slug, lowercased into RCH_<UTC>_<slug>. Required.
  --topic STR            Topic line for RESEARCH_NOTE.md / _LATEST.md. Optional.
  --utc STR              UTC override (default now, format %Y%m%dT%H%M%SZ). Pin for reproducible runs/tests.
  --no-update-latest     Do not refresh _LATEST.md.
  --json                 Print created packet path + files as JSON.

Outputs:
  New immutable packet dir + 7 files + (optionally) refreshed _LATEST.md.
  Exit 0 created, 1 packet already exists (writes nothing), 2 invalid invocation.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "source_catalog"))
from source_database import write_csv  # noqa: E402
from research_packet import (  # noqa: E402
    HANDOFF_STATE_TEMPLATE,
    LATEST_TEMPLATE,
    PACKET_CSV_FILES,
    RESEARCH_NOTE_TEMPLATE,
    packet_slug,
)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--research-root", type=Path, required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--topic", default="")
    ap.add_argument("--utc")
    ap.add_argument("--no-update-latest", action="store_true")
    ap.add_argument("--json", action="store_true", dest="emit_json")
    args = ap.parse_args()

    utc = args.utc or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = packet_slug(args.slug)
    packet_name = f"RCH_{utc}_{slug}"
    research_root = args.research_root
    packet_dir = research_root / packet_name

    if packet_dir.exists():
        print(
            f"ERROR: packet already exists (immutable, refusing to overwrite): {packet_dir}",
            file=sys.stderr,
        )
        return 1

    topic = args.topic or slug.replace("_", " ")
    packet_dir.mkdir(parents=True, exist_ok=False)

    written: list[str] = []
    for filename, columns in PACKET_CSV_FILES.items():
        write_csv(packet_dir / filename, columns, [])
        written.append(filename)
    (packet_dir / "RESEARCH_NOTE.md").write_text(
        RESEARCH_NOTE_TEMPLATE.format(topic=topic), encoding="utf-8"
    )
    written.append("RESEARCH_NOTE.md")
    (packet_dir / "HANDOFF_STATE.md").write_text(
        HANDOFF_STATE_TEMPLATE.format(packet=packet_name), encoding="utf-8"
    )
    written.append("HANDOFF_STATE.md")

    latest_updated = False
    if not args.no_update_latest:
        latest_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        (research_root / "_LATEST.md").write_text(
            LATEST_TEMPLATE.format(packet=packet_name, utc=latest_utc, topic=topic),
            encoding="utf-8",
        )
        latest_updated = True

    payload = {
        "packet_dir": str(packet_dir),
        "packet_name": packet_name,
        "files": sorted(written),
        "latest_updated": latest_updated,
    }
    if args.emit_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"created {packet_dir} ({len(written)} files)")
        if latest_updated:
            print(f"updated {research_root / '_LATEST.md'} -> {packet_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
