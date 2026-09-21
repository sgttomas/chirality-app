#!/bin/zsh
# Compatibility entrypoint: reads explicit Current State fields, including RETIRED.
# Usage: extract_lifecycle_states.sh <EXECUTION_ROOT>
SCRIPT_DIR="${0:A:h}"
exec python3 "$SCRIPT_DIR/audit_structure.py" --root "${1:?Execution root required}" --variant SOFTWARE --output -
