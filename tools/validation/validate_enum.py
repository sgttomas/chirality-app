#!/usr/bin/env python3
"""
validate_enum.py
Validates a value against a named enum set from the Chirality type system.

Usage:
    python3 validate_enum.py <enum_name> <value>

Exit codes:
    0 = valid
    1 = invalid (prints valid options to stderr)

Example:
    python3 validate_enum.py BASIS_OF_ESTIMATE PARAMETRIC
    python3 validate_enum.py LIFECYCLE_STATE SEMANTIC_READY
"""

import sys

ENUMS = {
    "LIFECYCLE_STATE": ["OPEN", "INITIALIZED", "SEMANTIC_READY", "IN_PROGRESS", "CHECKING", "ISSUED"],
    "DEPENDENCY_CLASS": ["ANCHOR", "EXECUTION"],
    "ANCHOR_TYPE": ["IMPLEMENTS_NODE", "TRACES_TO_REQUIREMENT", "NOT_APPLICABLE"],
    "DIRECTION": ["UPSTREAM", "DOWNSTREAM"],
    "DEPENDENCY_TYPE": ["PREREQUISITE", "INTERFACE", "HANDOVER", "CONSTRAINT", "ENABLES", "OTHER"],
    "TARGET_TYPE": ["DELIVERABLE", "PACKAGE", "WBS_NODE", "REQUIREMENT", "DOCUMENT", "EQUIPMENT", "EXTERNAL", "UNKNOWN"],
    "EXPLICITNESS": ["EXPLICIT", "IMPLICIT"],
    "CONFIDENCE": ["HIGH", "MEDIUM", "LOW"],
    "ORIGIN": ["DECLARED", "EXTRACTED"],
    "STATUS": ["ACTIVE", "RETIRED"],
    "SATISFACTION_STATUS": ["TBD", "PENDING", "IN_PROGRESS", "SATISFIED", "WAIVED", "NOT_APPLICABLE"],
    "BASIS_OF_ESTIMATE": ["QUOTE", "RATE_TABLE", "HISTORICAL", "PARAMETRIC", "ALLOWANCE"],
    "BASIS_OF_SCHEDULE": ["PRECEDENCE", "CONSTRAINT", "HYBRID"],
    "COORDINATION_REPR": ["SCHEDULE_FIRST", "DEPENDENCY_TRACKED", "HYBRID"],
    "TRACKING_MODE": ["NOT_TRACKED", "DECLARED", "TRACKED"],
    "DECOMP_VARIANT": ["PROJECT", "SOFTWARE", "DOMAIN"],
    "RUN_PASSES": ["FULL", "P1_P2", "P3_ONLY"],
    "AGENT_TYPE": ["TYPE 0", "TYPE 1", "TYPE 2"],
    "AGENT_CLASS": ["PERSONA", "TASK"],
    "BLOCKING": ["never", "allowed"],
    "ESTIMATE_IMPACT_CLASS": ["BLOCKING", "ADVISORY", "INFO", "TBD"],
    "EPISTEMIC_LABEL": ["FACT", "ASSUMPTION", "PROPOSAL", "TBD"],
    "FINDING_SEVERITY": ["CRITICAL", "MAJOR", "MINOR", "OBSERVATION"],
    "ESTIMATE_PREP_PHASE": ["SCAFFOLD", "BOE"],
}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <enum_name> <value>", file=sys.stderr)
        print(f"Available enums: {', '.join(sorted(ENUMS.keys()))}", file=sys.stderr)
        sys.exit(1)

    enum_name = sys.argv[1].upper()
    value = sys.argv[2]

    if enum_name not in ENUMS:
        print(f"Unknown enum: {enum_name}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(ENUMS.keys()))}", file=sys.stderr)
        sys.exit(1)

    valid_values = ENUMS[enum_name]
    if value in valid_values:
        print(f"VALID: {value} is a valid {enum_name}")
        sys.exit(0)
    else:
        print(f"INVALID: {value} is not a valid {enum_name}", file=sys.stderr)
        print(f"Valid values: {', '.join(valid_values)}", file=sys.stderr)
        sys.exit(1)
