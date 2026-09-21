#!/bin/zsh
# Compatibility entrypoint: exhaustive JSON report replaces the historical text scan.
# Usage: this-command <EXECUTION_ROOT>
SCRIPT_DIR="${0:A:h}"
exec python3 "$SCRIPT_DIR/audit_dependencies.py" --root "${1:?Execution root required}" --output -
