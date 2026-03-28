#!/bin/zsh
# write_status.sh
# Writes or updates _STATUS.md with a lifecycle state transition.
# Appends to History section; updates Current State.
#
# Usage: ./write_status.sh <DEL_PATH> <STATE> <ACTOR>
#
# Inputs:
#   DEL_PATH — Path to deliverable folder
#   STATE    — Lifecycle state (OPEN|INITIALIZED|SEMANTIC_READY|IN_PROGRESS|CHECKING|ISSUED)
#   ACTOR    — Who triggered the transition (e.g., PREPARATION, 4_DOCUMENTS, human)
#
# Outputs:
#   Written/updated _STATUS.md in the deliverable folder.
#
# Example:
#   ./write_status.sh ./execution/PKG-001_.../1_Working/DEL-001-01_... INITIALIZED 4_DOCUMENTS

DEL_PATH="${1:?Usage: $0 <DEL_PATH> <STATE> <ACTOR>}"
STATE="${2:?Usage: $0 <DEL_PATH> <STATE> <ACTOR>}"
ACTOR="${3:?Usage: $0 <DEL_PATH> <STATE> <ACTOR>}"

VALID_STATES="OPEN INITIALIZED SEMANTIC_READY IN_PROGRESS CHECKING ISSUED"
if ! echo "$VALID_STATES" | grep -qw "$STATE"; then
  echo "ERROR: Invalid state '$STATE'. Valid: $VALID_STATES" >&2
  exit 1
fi

STATUS_FILE="$DEL_PATH/_STATUS.md"
DEL_NAME=$(basename "$DEL_PATH")
DEL_ID="${DEL_NAME%%_*}"
TODAY=$(date +%Y-%m-%d)

if [ -f "$STATUS_FILE" ]; then
  # Update existing: replace Current State line, append to History
  sed -i '' "s/^\*\*Current State:\*\*.*/\*\*Current State:\*\* $STATE/" "$STATUS_FILE"
  sed -i '' "s/^\*\*Last Updated:\*\*.*/\*\*Last Updated:\*\* $TODAY/" "$STATUS_FILE"
  echo "- $TODAY — State set to $STATE ($ACTOR)" >> "$STATUS_FILE"
else
  # Create new
  cat > "$STATUS_FILE" << EOF
# Status: $DEL_ID

**Current State:** $STATE
**Last Updated:** $TODAY

## History
- $TODAY — State set to $STATE ($ACTOR)
EOF
fi

echo "Status: $DEL_ID → $STATE (by $ACTOR)"
