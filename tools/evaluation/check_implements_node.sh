#!/bin/zsh
# check_implements_node.sh
# Verifies every Dependencies.csv has at least one IMPLEMENTS_NODE anchor row.
# Usage: ./check_implements_node.sh <EXECUTION_ROOT>

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"

echo "=== IMPLEMENTS_NODE Anchor Coverage ==="
echo ""

total=0
has_anchor=0
missing_anchor=0

find "$EXROOT" -path "*/1_Working/*/Dependencies.csv" -type f | sort | while read csvfile; do
  total=$((total + 1))
  del_dir=$(dirname "$csvfile")
  del_name=$(basename "$del_dir")
  del_id="${del_name%%_*}"

  count=$(grep -c "IMPLEMENTS_NODE" "$csvfile" 2>/dev/null || echo 0)

  if [ "$count" -gt 0 ]; then
    has_anchor=$((has_anchor + 1))
  else
    echo "MISSING ANCHOR: $del_id"
    missing_anchor=$((missing_anchor + 1))
  fi
done

echo ""
echo "Total files: $total"
echo "With IMPLEMENTS_NODE: $has_anchor"
echo "Missing IMPLEMENTS_NODE: $missing_anchor"
