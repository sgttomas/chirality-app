#!/bin/zsh
# count_deliverable_files.sh
# Counts file presence across all deliverable folders for structure audit.
# Usage: ./count_deliverable_files.sh <EXECUTION_ROOT> [--isolated-migration --migration-authority D-GOV-16@<sha>]

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"
shift
FORMAT_ARGS=()
while (( $# > 0 )); do
  case "$1" in
    --isolated-migration)
      FORMAT_ARGS+=("$1")
      shift
      ;;
    --migration-authority)
      if (( $# < 2 )); then
        echo "ERROR: --migration-authority requires a value" >&2
        exit 2
      fi
      FORMAT_ARGS+=("$1" "$2")
      shift 2
      ;;
    *)
      echo "ERROR: unknown argument: $1" >&2
      exit 2
      ;;
  esac
done
SCRIPT_DIR="${0:A:h}"
FORMAT_VALIDATOR="$SCRIPT_DIR/../scope_of_work/validate_scope_of_work.py"

echo "=== Deliverable File Inventory ==="
echo ""

total=$(find "$EXROOT" -path "*/1_Working/DEL-*" -maxdepth 4 -type d | wc -l | tr -d ' ')
echo "Total deliverable folders: $total"
echo ""

for file in _STATUS.md _CONTEXT.md _DEPENDENCIES.md _REFERENCES.md \
            Datasheet.md Specification.md Guidance.md Procedure.md ScopeOfWork.md \
            Dependencies.csv _MEMORY.md _SEMANTIC.md _SEMANTIC_LENSING.md; do
  count=$(find "$EXROOT" -path "*/1_Working/DEL-*/$file" -type f | wc -l | tr -d ' ')
  echo "$file: $count / $total"
done

sow_count=0
legacy_count=0
migration_count=0
ambiguous_count=0
invalid_count=0
while IFS= read -r -d $'\0' deliverable; do
  report=$(PYTHONDONTWRITEBYTECODE=1 python3 "$FORMAT_VALIDATOR" "$deliverable" --json "${FORMAT_ARGS[@]}" 2>/dev/null)
  state=$(print -r -- "$report" | sed -n 's/^  "format": "\([^"]*\)",$/\1/p')
  case "$state" in
    SOW_V1) (( sow_count++ )) ;;
    LEGACY_FOUR_DOC) (( legacy_count++ )) ;;
    MIGRATION_DUAL) (( migration_count++ )) ;;
    AMBIGUOUS) (( ambiguous_count++ )) ;;
    *) (( invalid_count++ )) ;;
  esac
done < <(find "$EXROOT" -path "*/1_Working/DEL-*" -maxdepth 4 -type d -print0)

echo ""
echo "Production format SOW_V1: $sow_count / $total"
echo "Production format LEGACY_FOUR_DOC: $legacy_count / $total"
echo "Production format MIGRATION_DUAL: $migration_count / $total"
echo "Production format AMBIGUOUS: $ambiguous_count / $total"
echo "Production format INVALID: $invalid_count / $total"
