# PR69 target-specific macOS notice reconciliation

Exact implementation basis: 7fdb470b9bedf3bea9f4369672dd24524a6c799d. Five already
locked packages are now direct runtime dependencies only under macOS. The old
index's manifest hashes and top-level-only enumeration could not truthfully
represent them. Versioned v2 notice selection now includes those declarations,
records their target scope, excludes known other-platform/build/dev declarations,
and refuses unknown target conditions rather than omit them.

All 18 selected direct Cargo archives were checked offline against exact lock
hashes, package manifest identities/licenses and available root notice members.
The five new archives have no root license text. Their recorded .cargo_vcs_info
and README evidence identifies madsmtm/objc2 upstream LICENSE.md associations:
objc2/dispatch2 revision 8852b424193ca41602281b3d7540d7c8ed51e49a;
objc2-app-kit/objc2-foundation revision 7b1abfd750a2cacaea71d6a56ecfb83cb7de560b;
block2 revision b4167b582b2f75f9a1be75495c41b765344fd03c.
The exact crate-level source subpaths and archive/member digests are in index.json.
Those pointers do not supply the missing texts; no downloads were made. Current
report remains notice_text_coverage incomplete with all five names, despite
passing exact index/asset correspondence. Total22components,30existingtexts;
no new asset or overlay text is fabricated. Existing npm/App input bytes unchanged.

Regression checks reject an omitted macOS dependency, wrong declaration targets,
wrong platform, unrepresented missing text and unknown cfg expressions, while
retaining existing byte/link/overlay refusal checks. This implements OUT-001
bounded content preparation and preserves all original scope/dependency conditions.
No transitive completeness, licensing election, new candidate build, supplier
qualification or release is claimed. Existing built candidates remain their
actual historical subjects. Native owner retains PR69/runtime/EXP-SQ generation;
this contribution changes notice inputs/checking only.
