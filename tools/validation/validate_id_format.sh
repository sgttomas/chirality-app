#!/bin/zsh
# validate_id_format.sh
# Validates that an ID matches the expected format for its type.
#
# Usage: ./validate_id_format.sh <ID_TYPE> <ID_VALUE>
#
# Inputs:
#   ID_TYPE  — One of: PKG, DEL, DEP, SOW, OBJ, CAT, KTY
#   ID_VALUE — The ID string to validate
#
# Exit codes:
#   0 = valid
#   1 = invalid
#
# Example:
#   ./validate_id_format.sh DEL DEL-001-01

ID_TYPE="${1:?Usage: $0 <ID_TYPE> <ID_VALUE>}"
ID_VALUE="${2:?Usage: $0 <ID_TYPE> <ID_VALUE>}"

case "$ID_TYPE" in
  PKG)  PATTERN='^PKG-[0-9]{3}$' ;;
  DEL)  PATTERN='^DEL-[0-9]{3}-[0-9]{2}$' ;;
  DEP)  PATTERN='^DEP-[0-9]{3}-[0-9]{2}-[0-9]{3}$' ;;
  SOW)  PATTERN='^SOW-[0-9]{4}[a-z]?$' ;;
  OBJ)  PATTERN='^OBJ-[0-9]{3}$' ;;
  CAT)  PATTERN='^CAT-[0-9]{3}$' ;;
  KTY)  PATTERN='^KTY-[0-9]{2}-[0-9]{2}$' ;;
  *)
    echo "ERROR: Unknown ID type '$ID_TYPE'. Valid: PKG, DEL, DEP, SOW, OBJ, CAT, KTY" >&2
    exit 1
    ;;
esac

if echo "$ID_VALUE" | grep -qE "$PATTERN"; then
  echo "VALID: $ID_VALUE matches $ID_TYPE format"
  exit 0
else
  echo "INVALID: $ID_VALUE does not match $ID_TYPE format ($PATTERN)" >&2
  exit 1
fi
