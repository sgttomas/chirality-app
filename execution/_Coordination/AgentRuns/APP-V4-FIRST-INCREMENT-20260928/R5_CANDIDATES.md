# R5 candidates — residuals from the R4 sweep and W9/W10 (for V3)

Collected by HELP_HUMAN at commit `9fc77baa3`. The V3 reviewers assess each
item (agree / amend / reject). HELP_HUMAN then issues final micro-rulings.

| # | Item | Source | Proposed treatment |
|---|---|---|---|
| Y-1 | Does a host loop evaluating its own resolved copy of the declaration count as **host-held** carriage? | LOOP-v0.4 G-1; CA F-12 | Yes. *Host-held* means the constraint is held on the host side, whether received or derived from the host's own resolved declaration. DEL-03-02 states this. |
| Y-2 | Precedence when an A8-named setting differs from the declared setting content | WD-v0.4 finding | The **declared** setting content binds. An A8 naming different content is a separate request and never changes the subject. |
| Y-3 | Model destination per run vs per turn; mid-run model switch | EXEC F-21; CA F-13; XT F-12; HOSTING §8.3 (per turn) | Record **per turn** where the supplier reports it (HOSTING §8.3). The run-level value is the set of destinations observed. No new run is implied. DEL-04-03 aligns. |
| Y-4 | A person's own host-side undo after resume: does it re-hold? | RS/AS F4-2 | Yes, per RH-2 (a lapse is a lapse whatever caused it). DEL-02-03 states it explicitly. |
| Y-5 | A person's own A1/A2 are run-record operations, not human-act records | RS F4-1 | Confirm. Nothing downstream expects a person-A2 act record. |
| Y-6 | Grant-setting checkpoint arrival before T15 in the shared fixture | LOOP-v0.4 G-2 | C adds an arrival step before T15 (for example T14b), or consumers keep local labels. V3 recommends which. |
| Y-7 | Citations to sibling v0.3 or v0.1 texts that are now v0.4 or v0.2 | ADAPTER VC; W9 CA F-14 / XT F-14; GUIDE F-11 | Re-point to current versions and section numbers in a mechanical pass. |
| Y-8 | App-assured carriage is unreachable while HP-1 is not adopted | EXEC F-18 | P §3.3 and ACT §4.4 state "App-assured: not available in this increment (D6)". |
| Y-9 | Relay: the external route is blocked on SQ-02, and V4-EXM-25 is blocked on SQ-28 | CA F-10/F-11; XT F-9/F-10 | Surface to the owner with the relay. No text change. |
