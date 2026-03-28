#!/bin/zsh
# create_snapshot_folder.sh
# Creates a timestamped immutable snapshot folder under a tool root.
# Universal primitive used by all snapshot-producing agents.
#
# Usage: ./create_snapshot_folder.sh <TOOL_ROOT> <PREFIX> <LABEL>
#
# Inputs:
#   TOOL_ROOT — Path to the tool root (e.g., _Estimates/, _Aggregation/)
#   PREFIX    — Snapshot prefix (e.g., EST, AGG, COV, CLOSURE, EPREP, SCA)
#   LABEL     — Run label (e.g., DEL-001-01, Estimate_Collation, POST_SCA001)
#
# Outputs:
#   Created folder path (printed to stdout for capture by caller).
#   Format: {TOOL_ROOT}/{PREFIX}_{LABEL}_{YYYY-MM-DD}_{HHMM}/
#
# Example:
#   SNAP=$(./create_snapshot_folder.sh ./_Estimates EST DEL-001-01)

TOOL_ROOT="${1:?Usage: $0 <TOOL_ROOT> <PREFIX> <LABEL>}"
PREFIX="${2:?Usage: $0 <TOOL_ROOT> <PREFIX> <LABEL>}"
LABEL="${3:?Usage: $0 <TOOL_ROOT> <PREFIX> <LABEL>}"

TIMESTAMP=$(date +%Y-%m-%d_%H%M)
SNAP_DIR="$TOOL_ROOT/${PREFIX}_${LABEL}_${TIMESTAMP}"

mkdir -p "$SNAP_DIR"
echo "$SNAP_DIR"
