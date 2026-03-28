#!/bin/zsh
# count_deliverable_files.sh
# Counts file presence across all deliverable folders for structure audit.
# Usage: ./count_deliverable_files.sh <EXECUTION_ROOT>

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"

echo "=== Deliverable File Inventory ==="
echo ""

total=$(find "$EXROOT" -path "*/1_Working/DEL-*" -maxdepth 4 -type d | wc -l | tr -d ' ')
echo "Total deliverable folders: $total"
echo ""

for file in _STATUS.md _CONTEXT.md _DEPENDENCIES.md _REFERENCES.md \
            Datasheet.md Specification.md Guidance.md Procedure.md \
            Dependencies.csv _MEMORY.md _SEMANTIC.md _SEMANTIC_LENSING.md; do
  count=$(find "$EXROOT" -path "*/1_Working/DEL-*/$file" -type f | wc -l | tr -d ' ')
  echo "$file: $count / $total"
done
