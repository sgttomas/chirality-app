#!/bin/zsh
# scan_next_amendment_id.sh
# Scans _ScopeChange/ folder names to determine the next available SCA-{NNN} ID.
#
# Usage: ./scan_next_amendment_id.sh <SCOPE_CHANGE_ROOT>
#
# Inputs:
#   SCOPE_CHANGE_ROOT — Path to _ScopeChange/ directory (or parent containing it)
#
# Outputs:
#   Next available SCA-{NNN} ID (stdout). If no prior amendments, outputs SCA-001.
#
# Example:
#   ./scan_next_amendment_id.sh ./execution/_ScopeChange
#   # Output: SCA-002

SCOPE_ROOT="${1:?Usage: $0 <SCOPE_CHANGE_ROOT>}"

# Find highest existing SCA-NNN number
max_num=0
for dir in "$SCOPE_ROOT"/SCA-*/ "$SCOPE_ROOT"/SCA-* 2>/dev/null; do
  [ -e "$dir" ] || continue
  base=$(basename "$dir")
  num=$(echo "$base" | grep -oE 'SCA-([0-9]+)' | grep -oE '[0-9]+')
  if [ -n "$num" ] && [ "$num" -gt "$max_num" ] 2>/dev/null; then
    max_num=$num
  fi
done

next_num=$((max_num + 1))
printf "SCA-%03d\n" $next_num
