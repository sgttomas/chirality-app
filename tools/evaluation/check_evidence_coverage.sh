#!/bin/zsh
# check_evidence_coverage.sh
# Checks EvidenceFile column population rate across all Dependencies.csv files.
# Usage: ./check_evidence_coverage.sh <EXECUTION_ROOT>

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"

echo "=== EvidenceFile Population Audit ==="
echo ""

total_rows=0
populated_rows=0

find "$EXROOT" -path "*/1_Working/*/Dependencies.csv" -type f | while read csvfile; do
  del_dir=$(dirname "$csvfile")
  del_name=$(basename "$del_dir")
  del_id="${del_name%%_*}"

  # Find EvidenceFile column index from header
  header=$(head -1 "$csvfile" | tr -d '\r')
  col_idx=$(echo "$header" | tr ',' '\n' | grep -n "EvidenceFile" | cut -d: -f1)

  if [ -z "$col_idx" ]; then
    echo "NO COLUMN: $del_id — EvidenceFile column not found"
    continue
  fi

  rows=$(tail -n +2 "$csvfile" | wc -l | tr -d ' ')
  populated=$(tail -n +2 "$csvfile" | awk -F',' -v col="$col_idx" '{if ($col != "" && $col != " ") count++} END {print count+0}')
  empty=$((rows - populated))

  total_rows=$((total_rows + rows))
  populated_rows=$((populated_rows + populated))

  if [ "$empty" -gt 0 ]; then
    echo "GAP: $del_id — $empty/$rows rows missing EvidenceFile"
  fi
done

echo ""
echo "Total rows: $total_rows"
echo "EvidenceFile populated: $populated_rows"
if [ "$total_rows" -gt 0 ]; then
  pct=$((populated_rows * 100 / total_rows))
  echo "Coverage: ${pct}%"
fi
