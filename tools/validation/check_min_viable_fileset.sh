#!/bin/zsh
# check_min_viable_fileset.sh
# Verifies that all 5 required metadata files exist in a deliverable folder.
#
# Usage: ./check_min_viable_fileset.sh <DELIVERABLE_PATH>
#
# Inputs:
#   DELIVERABLE_PATH — Path to a single deliverable folder
#
# Outputs:
#   PASS (exit 0) if all 5 files present.
#   FAIL (exit 1) with list of missing files if any are absent.
#
# Example:
#   ./check_min_viable_fileset.sh ./execution/PKG-001_.../1_Working/DEL-001-01_...

DEL_PATH="${1:?Usage: $0 <DELIVERABLE_PATH>}"

REQUIRED_FILES=(
  "_STATUS.md"
  "_CONTEXT.md"
  "_DEPENDENCIES.md"
  "_REFERENCES.md"
  "_SEMANTIC.md"
)

missing=()
for f in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$DEL_PATH/$f" ]; then
    missing+=("$f")
  fi
done

del_name=$(basename "$DEL_PATH")
del_id="${del_name%%_*}"

if [ ${#missing[@]} -eq 0 ]; then
  echo "PASS: $del_id — all 5 minimum viable files present"
  exit 0
else
  echo "FAIL: $del_id — missing ${#missing[@]} file(s): ${missing[*]}"
  exit 1
fi
