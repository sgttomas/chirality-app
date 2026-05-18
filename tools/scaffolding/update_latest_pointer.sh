#!/bin/zsh
# update_latest_pointer.sh
# Overwrites _LATEST.md to point to the specified snapshot folder.
# Universal primitive used by all snapshot-producing agents.
#
# Usage: ./update_latest_pointer.sh <TOOL_ROOT> <SNAPSHOT_NAME>
#
# Inputs:
#   TOOL_ROOT     — Path to the tool root containing _LATEST.md
#   SNAPSHOT_NAME — Name of the snapshot folder (not full path)
#
# Outputs:
#   Updated _LATEST.md file in TOOL_ROOT.
#
# Example:
#   ./update_latest_pointer.sh ./_Estimates EST_DEL-001-01_2026-03-26_1400

TOOL_ROOT="${1:?Usage: $0 <TOOL_ROOT> <SNAPSHOT_NAME>}"
SNAP_NAME="${2:?Usage: $0 <TOOL_ROOT> <SNAPSHOT_NAME>}"

cat > "$TOOL_ROOT/_LATEST.md" << EOF
Latest: ${SNAP_NAME}
Updated: $(date +%Y-%m-%d)
EOF

echo "Updated $TOOL_ROOT/_LATEST.md → $SNAP_NAME"
