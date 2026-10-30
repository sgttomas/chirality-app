# Distribution identity value prototype

CC-HOSTING-DISTRIBUTION-01 Design candidate. Run `python3 test_inventory.py`
from this directory with an already installed JSON Schema 2020-12 validator
(`jsonschema`; author check used 4.26.0). No install or download is performed.

Synthetic data only; no supplier execution, filesystem inventory, signatures,
qualification provenance or native witness. The model checks inventory schema,
semantic path/parent/uniqueness rules, deterministic file manifest, exact record
comparison and PATH-prefix encoding. Permission values are integers, not octal
strings. Manifest equality alone is deliberately insufficient.

The runtime implementation must independently obtain trustworthy filesystem facts
and enforce link counts, no-follow/stable traversal, target-filesystem path
representability, reference provenance and generation-bound standing. Tests here
cannot establish those properties. Lifecycle and package schema successors remain
explicit propagation work in DISTRIBUTION_IDENTITY.md. Historical prototypes and
v0.2 records are unchanged.
