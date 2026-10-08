# C3 CI-29 source treatment

Author: harness-native TASK `/root/group_c_successor/cfb_design_owner`, under
WORKING_ITEMS `/root/group_c_successor`. Basis: main `236cbc3c69`.
Named change: CI-29 / CFB-v0.3 / route-account format 0.2. Proposed definition,
subject to independent review; no source recovery or persistent App behavior.

## Treatment and authority

CFB §7 and DEL-07-02 REQ-002/VER-002 already require unavailable-source gaps
and unsupported affected parts. Historical format 0.1 requires a source read.
The additive successor permits no successful reads only with no facts or
supported conclusions, nonempty gaps (effect and responsible party required),
and nonempty unsupported conclusions. Existing duties/prohibitions remain.
The source owner prepares this named repair within the delegated scope;
independent review is required. This is definition completion, not a change to
product obligations, DAG, group order or owner decisions. CI-29 is implemented
only at successor definition. Persistent writing remains held.

Historical CONNECTOR_FALLBACK.md, both original schemas, fixtures, pins and
run evidence are unchanged. The successor amendment identifies its exact
basis; its new schema ID and formatVersion are 0.2. No old 0.1 reference may
resolve to new bytes. There is no automatic consumer adoption. No source,
provider or human act is established by constructed schema tests.

## Consequences and receiving owners

| Consumer | Exact consequence and next treatment |
|---|---|
| DEL-07-01 PEC, PEC_RECEIVING header/§8 | Pins CFB 69c1f10e…; standing and PR-1–7 unchanged. At deliberate adoption, distinguish a gap/unsupported account from an answer marked from files. No fabricated file answer; external PEC remains owner of provider terms. |
| DEL-08-01 Domains, DOMAINS_RECEIVING header/§4 | Same CFB pin and unchanged standing/admission derivation. Deliberate route-format adoption and missing-source presentation review required; external query/admission/allocation remains its actual owners. |
| DEL-06-01 FLEET_RECORDS FR-D3/RF-5a | Location remains with user project, no selected path. Connector needs use standing and route reference; an empty-source account cannot satisfy a need or create readiness. Standing schema and vendored pins unchanged. |
| DEL-06-02 FLEET_VIEWS FV-10 | Waiting cause may link route gaps after adoption. Existing reference consumption requires no successful-read count and is not automatically changed. |
| DEL-09-10 CONNECTOR_WITNESS §3(5), §4 | Historical requirement to answer from route cannot turn an unanswered question into a pass. Future unavailable-source case must examine explicit unsupported/gap behavior against DEL-07-02 VER-002, with examiner review of affected claims. Historical witness evidence is neither rerun nor reclassified. |
| DEL-08-02 RESEARCH_TO_DESIGN §1 | Pins CFB and explicitly refuses changed source hashes. Old bytes stay usable; later activation/adoption must assess successor separately. |

Manager carries these notices to affected receiving work; this contribution
edits no sibling contract or pin. No provider receiving or research activation
is implied. Fleet software is not a C prerequisite: CFB §6 H-6 reads files.

## O-D placement alternatives (proposal only)

CFB §9 assigns route placement to O-D with DEL-06-01; FR-D3 says no path is
selected. A caller-selected target inside the user's project could implement
that location constraint without a global canonical directory, but choosing
that policy still resolves the expressly open design matter. Passing an
arbitrary path to a writer does not itself satisfy the before-implementation
wording or establish custody. The source owner must explicitly select and
review a placement treatment before persistent writing; any consequential
cross-group choice goes through HELP_HUMAN to the owner.

Recommended concrete treatment for O-D consideration: caller identifies the
user-project root and an explicit project-relative account target; validate
containment, refuse unintended replacement, preserve account identity and
prior accounts, return a durable reference for consumers. Do not create a
common service, canonical fleet directory or requirement for fleet software.
Containment, collision behavior and reference resolution need design/review
before implementation. This is a proposal, not selected policy.

Alternative: O-D and DEL-06-01 agree a shared project-relative directory and
reference policy. This couples the designs more closely; if it requires D
production before C, reverses order, forms a cross-group cycle or invalidates
finished work, escalate immediately under GC-7 rather than proceeding.

Available now: in-memory source-account definition/checks. Held: persistent
writing and placement implementation. No placement choice, new DAG arc,
provider deployment, native act, person act or SEAL-2 work occurs here.

## O-D comparison using the bounded Group A precedent

Source custody: `AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md`,
“Bounded App-local storage allocation”, records the exact human answer
**“Approve App-local storage (recommended)”**, relayed from the human's active
chat by parent `/root`. The prepared question points to the manager amendment
in that run's `PLACEMENT_DECISION_PREPARATION.md`, “Current reviewed
recommendation — manager amendment”. That amendment specifies project run
logs under `.chirality/records/runs/`, outside-run standing acts under
`.chirality/records/acts/`, and project captures under `.chirality/captures/`;
unwritable targets refuse visibly with no silent relocation. The decision
expressly is not global OI-013/014 closure or SWBPIPE construction/resumption.
This is existing recorded custody, not a newly witnessed owner act here.

That Group A allocation is a useful project-local recovery precedent; it
neither assigns connector/fleet paths nor selects the CFB §9 treatment.
No connector account is an act log or capture merely because it shares a
parent directory. Group A readers must not be assumed to discover it.

| O-D alternative | Benefit | Required treatment and risk |
|---|---|---|
| Canonical connector descendant, for example `.chirality/records/connectors/route-accounts/<safe-storage-key>.json` | Predictable discovery/recovery alongside other project records; portable project-relative references; avoids requiring callers to maintain a target registry | Proposed path only. O-D must select/version naming, account-to-storage identity mapping, immutable prior-account handling, containment/symlink checks, collision rules and reader discovery. A shared parent is no common service or inherited act-log/capture semantics. Visible failure on unwritable targets/no silent relocation should be selected explicitly. |
| Explicit caller-selected project-contained target | Fits differing project structures without global canonical path; caller retains destination choice | Still needs O-D selection. Caller must supply root/target and durable discovery/reference custody; moved targets and missing registrations can make recovery incomplete. Same containment, collision and visible-failure policy require review. |

With this precedent available, the preferred proposal for the placement
owner to consider is the canonical connector descendant: predictable recovery
reduces the additional discovery contract. The earlier caller-selected
recommendation remains a viable alternative, not an adopted policy. This
comparison changes no selected path: neither option is authorized here for
persistent implementation. The concrete example above is deliberately
identified as proposed, not a current repository or user-project convention.

DEL-06-01 could later adopt a separate fleet descendant under the same
`.chirality/records/` parent and consume stable project-relative route-account
references. C can define its own connector target/reference contract without
waiting for D fleet software, while notifying D of the proposed interface.
Sharing the parent does not require merging formats, readers, writers or
custody; D decides its own adoption. This preserves the C→D direction and H-6
file access. If agreement instead requires D's placement implementation first,
or a common service/reader prerequisite, return that consequential choice
through HELP_HUMAN under GC-7; do not label the resulting reversal resolved.

## Verification

Maintained `Design/check_route_account_v02.py` checks Draft 2020-12 schemas,
valid empty-source and mixed-read cases; rejects missing gap/responsibility,
unsupported/prohibited omissions, fabricated facts/support and performed duty
without evidence; checks required read identity and 0.1/0.2 separation.
An initial constructed fixture used wrong existing field spellings; corrected
to the unchanged standing schema before final validation. Checks establish
schema behavior, not source truth or product completion. Independent review
and final validation are recorded by their actual performers.

## C3-PLACE-01 definition preparation follow-up

HELP_HUMAN's relayed clarification treats O-D placement as a named technical
design selection within DEL-07-02/DEL-06-01 ownership, not a new human gate.
The source owner has prepared `Design/CONNECTOR_ROUTE_PLACEMENT_v0.1.md` as
an additive definition; it does not revise the independently reviewed CI-29
source amendment or schema. The earlier alternatives remain the proposal
history, not extra approval requirements. Proposed canonical location is
`.chirality/records/connectors/route-accounts/`, with separate storage identity,
anchored no-follow containment, write-once atomic publication, uncertain-commit
recovery, durable references and cold discovery. Fleet concurrence and exact
independent review are pending; persistence and consumer adoption remain held.
No new owner act or group-order change is recorded by this definition.
