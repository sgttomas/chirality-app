#!/bin/zsh
# check_four_documents.sh
# Verifies that the four-document kit exists in a deliverable folder.
# Only meaningful for deliverables at lifecycle state >= INITIALIZED.
#
# Usage: ./check_four_documents.sh <DELIVERABLE_PATH>
#
# Inputs:
#   DELIVERABLE_PATH — Path to a single deliverable folder
#
# Outputs:
#   PASS (exit 0) if all 4 documents present.
#   FAIL (exit 1) with list of missing documents.
#
# Example:
#   ./check_four_documents.sh ./execution/PKG-001_.../1_Working/DEL-001-01_...

DEL_PATH="${1:?Usage: $0 <DELIVERABLE_PATH>}"

DOC_KIT=(
  "Datasheet.md"
  "Specification.md"
  "Guidance.md"
  "Procedure.md"
)

missing=()
for f in "${DOC_KIT[@]}"; do
  if [ ! -f "$DEL_PATH/$f" ]; then
    missing+=("$f")
  fi
done

del_name=$(basename "$DEL_PATH")
del_id="${del_name%%_*}"

if [ ${#missing[@]} -eq 0 ]; then
  echo "PASS: $del_id — all 4 document kit files present"
  exit 0
else
  echo "FAIL: $del_id — missing ${#missing[@]} document(s): ${missing[*]}"
  exit 1
fi
