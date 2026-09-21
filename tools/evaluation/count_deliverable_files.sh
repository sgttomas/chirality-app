#!/bin/zsh
# Compatibility entrypoint: SOFTWARE inventory; use audit_structure for another variant.
# The historical isolated-migration and migration-authority options are passed through.
SCRIPT_DIR="${0:A:h}"
EXROOT="${1:?Execution root required}"
shift
exec python3 "$SCRIPT_DIR/audit_structure.py" --root "$EXROOT" --variant SOFTWARE --output - "$@"
