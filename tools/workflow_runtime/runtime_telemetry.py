#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "chirality-runtime-event/v1"
SUMMARY_SCHEMA = "chirality-runtime-summary/v1"
EVENT_TYPES = {"START", "FINISH", "CHECK", "REMEDIATION", "RETRY", "NOTICE", "MILESTONE"}
OUTCOMES = {"STARTED", "PASS", "FAIL", "BLOCKED", "RETRY", "INFO", "UNKNOWN"}


def contained(root: Path, value: str) -> Path:
    path = Path(value)
    candidate = path.resolve() if path.is_absolute() else (root / path).resolve()
    candidate.relative_to(root)
    return candidate


def parse_timestamp(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    normalized = value.replace("Z", "+00:00")
    result = datetime.fromisoformat(normalized)
    if result.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return result.astimezone(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("schema") != SCHEMA:
            raise ValueError(f"line {line_number}: unsupported schema")
        events.append(event)
    return events


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        existing_ids = set()
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            existing = json.loads(line)
            if existing.get("schema") != SCHEMA or not isinstance(existing.get("event_id"), str):
                raise ValueError(f"invalid existing telemetry event at line {line_number}")
            existing_ids.add(existing["event_id"])
        if event["event_id"] in existing_ids:
            raise ValueError(f"duplicate event_id: {event['event_id']}")
        handle.seek(0, os.SEEK_END)
        handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def positive_optional(value: int | None, label: str) -> int | None:
    if value is not None and value < 0:
        raise ValueError(f"{label} must be non-negative")
    return value


def record(args: argparse.Namespace) -> int:
    run_root = Path(args.run_root).resolve()
    if not run_root.is_dir():
        raise ValueError(f"run root does not exist: {run_root}")
    output = contained(run_root, args.output)
    event_type = args.event_type.upper()
    outcome = args.outcome.upper()
    if event_type not in EVENT_TYPES:
        raise ValueError(f"unsupported event type: {event_type}")
    if outcome not in OUTCOMES:
        raise ValueError(f"unsupported outcome: {outcome}")
    timestamp = parse_timestamp(args.timestamp)
    event = {
        "schema": SCHEMA,
        "event_id": args.event_id,
        "timestamp": iso_utc(timestamp),
        "run_id": args.run_id,
        "instance_id": args.instance_id,
        "session_id": args.session_id,
        "role": args.role,
        "package_id": args.package_id,
        "deliverable_id": args.deliverable_id,
        "attempt": args.attempt,
        "event_type": event_type,
        "outcome": outcome,
        "category": args.category,
        "reason_code": args.reason_code,
        "detail": args.detail,
        "telemetry": {
            "input_tokens": positive_optional(args.input_tokens, "input_tokens"),
            "output_tokens": positive_optional(args.output_tokens, "output_tokens"),
            "context_tokens": positive_optional(args.context_tokens, "context_tokens"),
            "context_limit": positive_optional(args.context_limit, "context_limit"),
        },
    }
    append_event(output, event)
    print(json.dumps({"status": "RECORDED", "event_id": args.event_id, "output": output.relative_to(run_root).as_posix()}))
    return 0


def summarize(args: argparse.Namespace) -> int:
    run_root = Path(args.run_root).resolve()
    if not run_root.is_dir():
        raise ValueError(f"run root does not exist: {run_root}")
    input_path = contained(run_root, args.input)
    output_path = contained(run_root, args.output)
    events = read_events(input_path)
    ids = [event["event_id"] for event in events]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate event IDs in telemetry ledger")

    sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        sessions[event["session_id"]].append(event)
    session_rows = []
    unmatched_sessions = []
    for session_id, rows in sorted(sessions.items()):
        ordered = sorted(rows, key=lambda row: row["timestamp"])
        starts = [row for row in ordered if row["event_type"] == "START"]
        finishes = [row for row in ordered if row["event_type"] == "FINISH"]
        duration = None
        if len(starts) == 1 and len(finishes) == 1:
            duration = round(
                (parse_timestamp(finishes[0]["timestamp"]) - parse_timestamp(starts[0]["timestamp"])).total_seconds(),
                3,
            )
            if duration < 0:
                raise ValueError(f"session {session_id} finishes before it starts")
        else:
            unmatched_sessions.append(session_id)
        session_rows.append({
            "session_id": session_id,
            "instance_id": ordered[0]["instance_id"],
            "role": ordered[0]["role"],
            "package_id": ordered[0]["package_id"],
            "events": len(ordered),
            "duration_seconds": duration,
            "final_outcome": finishes[-1]["outcome"] if finishes else None,
            "retries": sum(row["event_type"] == "RETRY" for row in ordered),
            "remediations": sum(row["event_type"] == "REMEDIATION" for row in ordered),
        })

    starts = [event for event in events if event["event_type"] == "START"]
    context_measured = sum(event["telemetry"]["context_tokens"] is not None for event in starts)
    report = {
        "schema": SUMMARY_SCHEMA,
        "status": "PASS" if events and not unmatched_sessions else "INCOMPLETE",
        "events": len(events),
        "sessions": len(sessions),
        "counts": {
            "event_type": dict(sorted(Counter(event["event_type"] for event in events).items())),
            "outcome": dict(sorted(Counter(event["outcome"] for event in events).items())),
            "category": dict(sorted(Counter(event["category"] for event in events if event["category"]).items())),
            "reason_code": dict(sorted(Counter(event["reason_code"] for event in events if event["reason_code"]).items())),
        },
        "context_telemetry": {
            "starts_with_context_occupancy": context_measured,
            "starts_without_context_occupancy": len(starts) - context_measured,
            "measurement_limitation": None if context_measured == len(starts) else "native context occupancy unavailable for one or more sessions",
        },
        "unmatched_sessions": unmatched_sessions,
        "session_results": session_rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "events": len(events), "sessions": len(sessions), "output": output_path.relative_to(run_root).as_posix()}))
    return 0 if report["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record and summarize bounded workflow runtime telemetry.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--run-root", required=True)
    record_parser.add_argument("--output", default="RUNTIME_EVENTS.jsonl")
    record_parser.add_argument("--event-id", required=True)
    record_parser.add_argument("--run-id", required=True)
    record_parser.add_argument("--instance-id", required=True)
    record_parser.add_argument("--session-id", required=True)
    record_parser.add_argument("--role", required=True)
    record_parser.add_argument("--package-id")
    record_parser.add_argument("--deliverable-id")
    record_parser.add_argument("--attempt", type=int, default=1)
    record_parser.add_argument("--event-type", required=True)
    record_parser.add_argument("--outcome", required=True)
    record_parser.add_argument("--category")
    record_parser.add_argument("--reason-code")
    record_parser.add_argument("--detail")
    record_parser.add_argument("--timestamp")
    record_parser.add_argument("--input-tokens", type=int)
    record_parser.add_argument("--output-tokens", type=int)
    record_parser.add_argument("--context-tokens", type=int)
    record_parser.add_argument("--context-limit", type=int)
    record_parser.set_defaults(handler=record)

    summary_parser = subparsers.add_parser("summarize")
    summary_parser.add_argument("--run-root", required=True)
    summary_parser.add_argument("--input", default="RUNTIME_EVENTS.jsonl")
    summary_parser.add_argument("--output", default="RUNTIME_SUMMARY.json")
    summary_parser.set_defaults(handler=summarize)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "attempt", 1) < 1:
        parser.error("--attempt must be positive")
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(2, f"runtime telemetry error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
