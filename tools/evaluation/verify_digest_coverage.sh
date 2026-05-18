#!/bin/zsh
# verify_digest_coverage.sh
# Verifies 1:1 mapping between deliverable folders and content digest files.
# Usage: ./verify_digest_coverage.sh <EXECUTION_ROOT>
#
# Exit codes:
#   0 = all deliverables have digests
#   1 = missing digests detected

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"
EVALROOT="$EXROOT/_Evaluation/content-digests"

missing=0
found=0
total=0

for pkg in "$EXROOT"/PKG-*/; do
  for del in "$pkg"1_Working/DEL-*/; do
    [ -d "$del" ] || continue
    delname=$(basename "$del")
    del_id="${delname%%_*}"
    pkg_num=$(echo "$del_id" | sed 's/DEL-\([0-9]*\)-.*/PKG-\1/')
    digest="$EVALROOT/$pkg_num/${del_id}.md"
    total=$((total + 1))
    if [ -f "$digest" ] && [ -s "$digest" ]; then
      found=$((found + 1))
    else
      echo "MISSING: $pkg_num/$del_id"
      missing=$((missing + 1))
    fi
  done
done

echo ""
echo "Total deliverables: $total"
echo "Digests found:      $found"
echo "Digests missing:    $missing"

if [ $missing -eq 0 ]; then
  echo "PASS — All $total deliverables have content digests."
  exit 0
else
  echo "FAIL — $missing deliverables are missing content digests."
  exit 1
fi
