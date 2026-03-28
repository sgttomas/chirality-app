#!/bin/zsh
# scaffold_tool_root.sh
# Creates a tool root directory with standard subfolders and _LATEST.md stub.
#
# Usage: ./scaffold_tool_root.sh <EXECUTION_ROOT> <ROOT_NAME>
#
# Inputs:
#   EXECUTION_ROOT — Path to project execution root
#   ROOT_NAME      — Tool root name (e.g., _Aggregation, _Estimates, _Reconciliation)
#
# Outputs:
#   Tool root folder with _Archive/ subfolder and _LATEST.md stub.
#
# Example:
#   ./scaffold_tool_root.sh ./execution _Aggregation

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT> <ROOT_NAME>}"
ROOT_NAME="${2:?Usage: $0 <EXECUTION_ROOT> <ROOT_NAME>}"

ROOT_DIR="$EXROOT/$ROOT_NAME"

mkdir -p "$ROOT_DIR/_Archive"

if [ ! -f "$ROOT_DIR/_LATEST.md" ]; then
  echo "Latest: (none)" > "$ROOT_DIR/_LATEST.md"
  echo "Created $ROOT_DIR/_LATEST.md"
else
  echo "Exists: $ROOT_DIR/_LATEST.md"
fi

echo "Tool root ready: $ROOT_DIR"
