# software-defect-diagnosis — Tool Policy

Prefer the narrowest registered check. Discovery and affected-check selection are read-only. Do not install dependencies, mutate persistent data, call networks, or run broad suites when a bounded reproducer exists. Diagnostic instrumentation must be temporary unless explicitly authorized as an output.
