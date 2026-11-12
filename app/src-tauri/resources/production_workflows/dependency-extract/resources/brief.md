# Brief a local need declaration

Supply the following in ordinary prose or structured fields:

- The project root and selected Deliverable's stable identity and locality.
- The purpose of the declaration or refresh and the relevant accepted change,
  intended use or setup scope.
- The exact `deliverable.yaml` write target and authorized read scope, including
  any relevant ScopeOfWork, source references and identity basis.
- Known technical holds, scope/acceptance limits and unresolved source bindings
  that must survive the refresh.

One writer owns the locality. A broader assignment may cover several localities
only when the coordinator makes the write ownership explicit. No additional
write target is implied by a source reference or derived downstream link.

```yaml
Workflow: dependency-extract
PROJECT: /abs/path/to/project
DELIVERABLE: DEL-01-02
PURPOSE: Refresh the inputs needed for the affected interface review.
READ_SCOPE:
  - execution/PKG-01/DEL-01-02/
  - execution/PKG-01/DEL-01-01/ScopeOfWork.md
  - execution/_Decomposition/accepted-basis.md
WRITE_TARGET: execution/PKG-01/DEL-01-02/deliverable.yaml
PRESERVE: Existing issue conditions and the unresolved equipment-rating source.
```

Resolve illustrative paths against the actual project. If a needed reference is
outside the authorized read scope, report that limit and continue unaffected
work. Do not use a package or `ALL` selector as permission to change every
locality without establishing the actual targets.

The output is the current local YAML and a concise return to the coordinator.
No extraction modes, secondary register, mirrored declarations, automatic
retirement, timestamps or run-record bundle are part of this method. A request
to migrate older project artifacts is a separate undertaking.
