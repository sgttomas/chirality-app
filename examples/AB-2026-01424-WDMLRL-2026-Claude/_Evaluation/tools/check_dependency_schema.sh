#!/bin/zsh
# check_dependency_schema.sh
# Validates Dependencies.csv v3.1 schema across all deliverables.
# Usage: ./check_dependency_schema.sh <EXECUTION_ROOT>

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"

REQUIRED_COLS="RegisterSchemaVersion,DependencyID,FromPackageID,FromDeliverableID,FromDeliverableName,DependencyClass,AnchorType,Direction,DependencyType,TargetType,TargetPackageID,TargetDeliverableID,TargetRefID,TargetName,TargetLocation,Statement,EvidenceFile,SourceRef,EvidenceQuote,Explicitness,RequiredMaturity,ProposedMaturity,SatisfactionStatus,Confidence,Origin,FirstSeen,LastSeen,Status,Notes"

echo "=== Dependencies.csv Schema Audit ==="
echo ""

total=0
valid=0
invalid=0

find "$EXROOT" -path "*/1_Working/*/Dependencies.csv" -type f | while read csvfile; do
  total=$((total + 1))
  header=$(head -1 "$csvfile" | tr -d '\r')

  # Check each required column exists in header
  missing=""
  IFS=',' read -rA required <<< "$REQUIRED_COLS"
  for col in "${required[@]}"; do
    if ! echo "$header" | grep -q "$col"; then
      missing="$missing $col"
    fi
  done

  colcount=$(echo "$header" | awk -F',' '{print NF}')
  rowcount=$(wc -l < "$csvfile" | tr -d ' ')
  rows=$((rowcount - 1))

  del_dir=$(dirname "$csvfile")
  del_name=$(basename "$del_dir")
  del_id="${del_name%%_*}"

  if [ -z "$missing" ]; then
    echo "VALID: $del_id ($colcount cols, $rows rows)"
  else
    echo "INVALID: $del_id — missing:$missing"
  fi
done

echo ""
echo "Audit complete."
