#!/bin/zsh
# count_workspace_state.sh
# Counts deliverables per lifecycle state and reports project-wide summary.
#
# Usage: ./count_workspace_state.sh <EXECUTION_ROOT>
#
# Inputs:
#   EXECUTION_ROOT — Path to project execution root
#
# Outputs:
#   State distribution table, total counts.
#
# Example:
#   ./count_workspace_state.sh ./execution

EXROOT="${1:?Usage: $0 <EXECUTION_ROOT>}"

echo "=== Project State Summary ==="
echo "Execution Root: $EXROOT"
echo "Date: $(date +%Y-%m-%d)"
echo ""

# Count packages
pkg_count=$(find "$EXROOT" -maxdepth 1 -type d -name "PKG-*" | wc -l | tr -d ' ')
echo "Packages: $pkg_count"

# Count deliverables (the DEL-* directory itself, not its subdirectories)
del_count=$(find "$EXROOT" -mindepth 3 -maxdepth 3 -type d -path "*/1_Working/DEL-*" | wc -l | tr -d ' ')
echo "Deliverables: $del_count"
echo ""

# State distribution
echo "| State | Count |"
echo "|-------|-------|"

# Match the single current-state declaration line only. A whole-file match
# also hits the append-only History section, which names every prior state.
for state in OPEN INITIALIZED SEMANTIC_READY IN_PROGRESS CHECKING ISSUED; do
  count=$(find "$EXROOT" -path "*/1_Working/DEL-*/_STATUS.md" -type f \
    -exec grep -l "^\*\*Current State:\*\* ${state}[[:space:]]*$" {} \; 2>/dev/null | wc -l | tr -d ' ')
  echo "| $state | $count |"
done

echo ""

# Tool roots
echo "Tool Roots:"
for root in _Aggregation _Coordination _Decomposition _Estimates _EstimatePrep _Reconciliation _Schedule _Sources _Change; do
  if [ -d "$EXROOT/$root" ]; then
    echo "  [x] $root"
  else
    echo "  [ ] $root"
  fi
done
