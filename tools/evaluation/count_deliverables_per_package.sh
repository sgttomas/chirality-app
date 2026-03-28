#!/bin/zsh
# count_deliverables_per_package.sh
# Counts deliverable folders per package.
# Usage: ./count_deliverables_per_package.sh <EXECUTION_ROOT>

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"

echo "=== Deliverables Per Package ==="
echo ""

total=0
for pkg in "$EXROOT"/PKG-*/; do
  pkgname=$(basename "$pkg")
  count=$(find "$pkg/1_Working" -maxdepth 1 -type d -name "DEL-*" 2>/dev/null | wc -l | tr -d ' ')
  total=$((total + count))
  printf "%-50s %s\n" "$pkgname" "$count"
done
echo ""
echo "Total: $total"
