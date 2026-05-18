#!/bin/zsh
# scaffold_deliverable.sh
# Creates a deliverable folder with minimum viable fileset (5 stub files) per SPEC.md Section 2.1.
#
# Usage: ./scaffold_deliverable.sh <WORKING_DIR> <DEL_ID> <DelLabel>
#
# Inputs:
#   WORKING_DIR — Path to package's 1_Working/ directory
#   DEL_ID      — Deliverable identifier (e.g., DEL-001-01)
#   DelLabel    — Human-readable label (e.g., "Preliminary-Design")
#
# Outputs:
#   Deliverable folder with 5 stub files. Reports created vs skipped.
#
# Example:
#   ./scaffold_deliverable.sh ./execution/PKG-001_Architectural\ Design/1_Working DEL-001-01 "Preliminary-Design"

WORKING_DIR="${1:?Usage: $0 <WORKING_DIR> <DEL_ID> <DelLabel>}"
DEL_ID="${2:?Usage: $0 <WORKING_DIR> <DEL_ID> <DelLabel>}"
DEL_LABEL="${3:?Usage: $0 <WORKING_DIR> <DEL_ID> <DelLabel>}"

DEL_DIR="$WORKING_DIR/${DEL_ID}_${DEL_LABEL}"
mkdir -p "$DEL_DIR"

STUBS=(
  "_STATUS.md"
  "_CONTEXT.md"
  "_DEPENDENCIES.md"
  "_REFERENCES.md"
  "_SEMANTIC.md"
)

created=0
skipped=0

for stub in "${STUBS[@]}"; do
  target="$DEL_DIR/$stub"
  if [ -f "$target" ]; then
    skipped=$((skipped + 1))
  else
    touch "$target"
    created=$((created + 1))
  fi
done

echo "Deliverable: $DEL_DIR"
echo "Created: $created files"
echo "Skipped (exist): $skipped files"
