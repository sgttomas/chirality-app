#!/usr/bin/env python3
"""Build EB-1's input-set manifest (DEL-10-01 EB-v0.1 §8; RRM-v0.1 format, schema unchanged).

Design prototype, not product code. Reads files only; writes one JSON file
(default: ../eb1/IS-EB1-1.input-set.json). Paths in the manifest are
repository-relative so the dispatcher can copy them into a scratch folder
keeping their structure.

Usage: python3 make_input_set.py [--out PATH]
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DESIGN = HERE.parent


def repo_root() -> pathlib.Path:
    out = subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True)
    return pathlib.Path(out.stdout.strip())


E = "projects/chirality-app-v4/execution"
RUN = f"{E}/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003"
D1001 = (f"{E}/PKG-10/"
         "DEL-10-01")

# (path, standing, note)
ITEMS = [
    (f"{D1001}/Design/EXECUTION_BASIS.md", "project_file",
     "The account under test (O-E, EB-v0.1). An index: its claims about acts must be confirmed in the records it cites."),
    (f"{E}/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md", "record", None),
    (f"{E}/_Coordination/Acceptances/APP-V4-BASIS-20260926/OWNER_DIRECTIONS.md", "record", None),
    (f"{E}/_Coordination/Changes/APP-V4-CLARIFICATION-20260927/DIRECTION.md", "record", None),
    (f"{E}/_Decomposition/checkpoint_snapshots/GROUP1-20260927T222641Z/DECISION.md", "record", None),
    (f"{E}/_Decomposition/checkpoint_snapshots/GROUP2-20260927T233018Z/DECISION.md", "record", None),
    (f"{E}/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/DECISION.md", "record", None),
    (f"{E}/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md", "record", None),
    (f"{E}/_Coordination/_COORDINATION.md", "record", None),
    (f"{E}/_Coordination/CURRENT_EXECUTION_BASIS.md", "record", None),
    (f"{E}/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/DECISION.md", "record", None),
    (f"{E}/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/DECISION.md", "record", None),
    (f"{E}/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/DECISION.md", "record", None),
    (f"{E}/_ScopeChange/_LATEST.md", "record", None),
    (f"{E}/_DAG/_LATEST.md", "record", None),
    (f"{E}/_DAG/DAG-001/ACCEPTANCE_RECORD.md", "record", None),
    (f"{E}/_DAG/DAG-004/ACCEPTANCE_RECORD.md", "record", None),
    (f"{E}/_DAG/DAG-004/HANDOFF_STATE.md", "record", None),
    (f"{E}/_Evaluation/DAGCurrency/_LATEST.md", "record", None),
    (f"{E}/_Coordination/HANDOFF_30_PERCENT.md", "record", None),
    (f"{E}/_Decomposition/Open_Issues.csv", "record", None),
    (f"{E}/_Decomposition/External_Dependencies.csv", "record", None),
    (f"{RUN}/OWNER_DECISIONS.md", "record", None),
    (f"{RUN}/OWNER_DECISIONS_2.md", "record", None),
    (f"{RUN}/R23_RESOLUTIONS.md", "record", "HELP_HUMAN's rulings, not owner acts."),
    (f"{E}/_Coordination/WorkGraphs/APP-V4-DESIGN-PASS-4-20261003/WORK_GRAPH.md", "record", None),
    ("docs/governance_harness/tranche_manifests/ROOT-DGOV52-APPLICATION-20261004.yaml", "record", None),
    (f"{E}/_Coordination/NOTICE_2026-10-04_ROOT_D-GOV-52_AGENTS_MD_APP_V4_ALIGNMENT.md", "record", None),
    ("projects/chirality-app-v4/loop/LOOP_INIT.md", "project_file", "The project's loop instruction."),
    ("projects/chirality-app-v4/docs/OPERATING_METHOD.md", "project_file", "Accepted-basis consolidation (post-act; see its status line)."),
]
PIN_NOTE = "Pinned subject bytes, supplied so the reader can recompute the hash; reading the body is not required."
PINNED = [
    "docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Consolidated_v7.md",
    "docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md",
    "docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md",
    "workflows/project-setup/WORKFLOW.md",
    ".agents/skills/preparation/SKILL.md",
    "workflows/scope-of-work/WORKFLOW.md",
    "workflows/dependency-extract/WORKFLOW.md",
    "workflows/audit-dep-closure/WORKFLOW.md",
    "workflows/project-dag/WORKFLOW.md",
    "workflows/construct-local-work-graph/WORKFLOW.md",
    "workflows/scope-change/WORKFLOW.md",
    "workflows/scc-resolution-case/WORKFLOW.md",
    "workflows/bounded-reconciliation/WORKFLOW.md",
    "workflows/coordinated-knowledge-work/WORKFLOW.md",
]

WITHHELD = [
    {"identity": "HELP_HUMAN Claude Code session of run APP-V4-DESIGN-PASS-4-20261003 (and the earlier runs' coordinating sessions)", "kind": "harness_session"},
    {"identity": "The owner's chat with HELP_HUMAN (the channel every owner act was transcribed from)", "kind": "harness_session"},
    {"identity": "O-E's session (author of EXECUTION_BASIS.md and of the question key)", "kind": "harness_session"},
    {"identity": "O-E's working context", "kind": "author_memory"},
    {"identity": f"{RUN}/SURVEY/S2-E.md (O-E's survey)", "kind": "derived_view"},
    {"identity": f"{D1001}/Design/eb1/EB1_QUESTION_KEY.md (the examiner's key)", "kind": "derived_view"},
    {"identity": "The repository working tree and Git history beyond the supplied files", "kind": "derived_view"},
]


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build(root: pathlib.Path) -> dict:
    items = []
    for path, standing, note in ITEMS + [(p, "project_file", PIN_NOTE) for p in PINNED]:
        f = root / path
        if not f.is_file():
            sys.exit(f"missing: {path}")
        item = {"path": path, "sha256": sha256(f), "standing": standing}
        if note:
            item["note"] = note
        items.append(item)
    return {
        "record_kind": "rrm_input_set",
        "format": "RRM-v0.1",
        "input_set_id": "IS-EB1-1",
        "source_journey": {
            "identity": "App v4 project execution basis as recorded in project files, read cold (DEL-10-01 EB-1)",
            "run_authors": [
                {"identity": "The owner (Ryan)", "role": "decision actor in every owner act"},
                {"identity": "HELP_HUMAN sessions", "role": "relay, recorder, ruling author (R23)"},
                {"identity": "WORKING_ITEMS instances of the definition and setup runs", "role": "recorders and record writers"},
                {"identity": "Type 2 nodes AK2 (SCA runs), D2 (SCA-V4-003) and /root (30% closeout)", "role": "record writers from transcriptions"},
                {"identity": "O-E (Type 2, Claude Opus 5.5)", "role": "author of EXECUTION_BASIS.md"},
            ],
            "journey_dates": [
                {"value": "2026-09-26", "source": "record_timestamp"},
                {"value": "2026-10-04", "source": "observed_clock"},
            ],
        },
        "items": items,
        "withheld": WITHHELD,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DESIGN / "eb1" / "IS-EB1-1.input-set.json"))
    a = ap.parse_args()
    m = build(repo_root())
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out} with {len(m['items'])} items")


if __name__ == "__main__":
    main()
