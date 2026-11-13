# Check a local need declaration

Inspect the saved `deliverable.yaml`, not just the proposed text.

1. The write stayed within the selected local file and `needs` boundary; a new
   file uses the established stable identity, agreeing with a containing folder
   that names a DEL identity. Existing non-need fields, scope,
   acceptance, lifecycle, supplier authorship and technical holds remain intact.
2. YAML is parseable without duplicate keys. `id` is the accepted native
   `DEL-nn-nn` identity and `needs` is a list. Every entry has a supported `from`
   string and a nonempty `condition`. Optional `when` is text, `gating` is a
   Boolean and `direction` is `upstream` or `downstream`. Document
   paths are project-relative and contained.
3. Each condition states an actual input/use with its case, maturity and trigger
   where material. Its scope/design/source basis is inspectable or its missing
   basis is explicit. File presence, lifecycle or a supplier declaration is not
   recorded as satisfaction.
4. Native inputs live at the consumer. Actual outward nonlocal obligations live
   at the producer with `direction: downstream` and `gating: false`; they are
   not treated as incoming requirements. No native downstream mirrors or
   supplier-internal work structure were created.
5. Distinct same-endpoint cases remain distinct. A repeated source statement
   does not add a duplicate. Changes/removals have an actual semantic reason;
   absence from a text scan is insufficient. Unknown sources remain unknown.
6. No hierarchy anchors, row IDs, automatic status/maturity transitions,
   satisfaction fields, routine histories or second dependency artifacts were
   introduced. Repeating the refresh against unchanged evidence leaves the
   needs unchanged.

Use the [tool guide](tools.md) for an available structural query. Inspect its
errors and partial coverage before interpreting results. If the tool is not
available or its broader reads are unauthorized, directly inspect the selected
YAML and relevant references and report that validation limit. Never claim a
tool pass from inspection alone.

Return malformed or ambiguous existing entries that cannot be repaired without
changing disputed meaning. A structurally valid file or a successful query does
not establish completeness, input suitability, engineering release or readiness.
