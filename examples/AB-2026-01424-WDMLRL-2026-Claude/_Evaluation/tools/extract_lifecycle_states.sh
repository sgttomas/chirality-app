#!/bin/zsh
# extract_lifecycle_states.sh
# Extracts lifecycle state from every _STATUS.md and produces a distribution summary.
# Usage: ./extract_lifecycle_states.sh <EXECUTION_ROOT>

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"

echo "=== Lifecycle State Distribution ==="
echo ""

find "$EXROOT" -path "*/1_Working/DEL-*/_STATUS.md" -type f | while read statusfile; do
  del_dir=$(dirname "$statusfile")
  del_name=$(basename "$del_dir")
  del_id="${del_name%%_*}"
  state=$(grep -oE '(OPEN|INITIALIZED|SEMANTIC_READY|IN_PROGRESS|CHECKING|ISSUED)' "$statusfile" | head -1)
  echo "$del_id $state"
done | sort | awk '{print $2}' | sort | uniq -c | sort -rn
