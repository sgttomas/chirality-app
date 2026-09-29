# Basis amendment — APP-V4-BASIS-ALIGN-20260928, node P1

**Status: PROPOSED (scope-change checkpoint-group-2 preparation, the exact
amendment). Nothing here is applied.** This file gives the exact old → new
text for:

- **Part A, the accepted basis documents:** `projects/chirality-app-v4/docs/`
  PRD.md, ARCHITECTURE.md, HOST_INTEGRATION.md and EXAMINATION.md;
- **Part B, the decomposition package** under
  `projects/chirality-app-v4/execution/_Decomposition/`, with the mirrored
  deliverable `_CONTEXT.md` lines.

Each edit traces to an owner decision. The atomic actions (A01…A47) are in
[IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md). The ScopeOfWork text is in
[SOW_REVISIONS.md](SOW_REVISIONS.md).

- **Basis:** commit `874508f16`. Input sha256: PRD.md `657593ce…4538573`,
  ARCHITECTURE.md `c3ae766e…42687e533`, HOST_INTEGRATION.md `08c8fc7d…d0960da`,
  EXAMINATION.md `1b156553…ef54ee19`, ScopeLedger.csv `36364330…5fd73`,
  Deliverables.csv `bcdf6f2f…915eb`, Packages.csv `b8a9b949…1fbd`,
  Vocabulary_Map.csv `af6c2187…d8ba`, Open_Issues.csv `77ecfea2…aef4`,
  SOFTWARE_DECOMP.md `5b66fefd…4ded`.
- **Checks:** every Part A "old" block was applied, by script, to copies of the
  four documents. Each occurs exactly once, in order. Every Part B field
  value was checked against the parsed CSV row (see IMPACT_ASSESSMENT
  §"Validation").
- **Acceptance-conditional tokens:** `{AMENDMENT_ID}` (recommended `SCA-V4-001`,
  item O-1), `{AMENDMENT_SNAPSHOT}` (the accepted snapshot folder under
  `execution/_ScopeChange/`) and `{ACCEPT_DATE}` (the date of the owner's
  group-3 act). They are filled from the accepted records at application; no
  other byte depends on the acceptance act.

## Decisions this amendment applies

The owner's words are recorded exactly in
`execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`:

- **DECISION-4 D4-1, phased checkpoints.** V4-WF-05's first half ("holds …
  the run waits") is *phased to the governance layer, not withdrawn*. Its
  second half (the act is recorded only when performed) is in force.
  Reserved acts stand. The principle applies to a host's embedded loop.
  (Owner: "Yes reserved acts should stand. Yes the principle should also
  apply to a host's own embedded loop … every workflow that needs such
  governance will have to be served by what we build.")
- **DECISION-4 D4-3, model access.** A cloud model is reached by OAuth sign-in
  or an API key; there is no default between local and cloud. This revises
  V4-HOST-01's "local by default" and "API key" wording, and V4-ARC-11.
- **DECISION-5, revised V4-HOST-02**, with the exact replacement wording, the
  two-level allow list, stateless MCP (revision 2026-07-28) only, person-only
  in-work grants, the always-off list, record and show, the outside-process
  limit and the phasing. The "in local operation" qualifier is dropped.
  DECISION-5 governs a host's embedded agent; the App's Codex keeps the
  person's configuration.

The SWBPIPE-intake receipt lists these under "For the next accepted-basis
update". R8-1, R8-9 and R8-13 give the integrator's framing.

## Edits at a glance

| # | Document · locus | Kind | Decision |
|---|---|---|---|
| A01 | PRD · V4-WF-05 | Requested | DECISION-4 D4-1 |
| A02 | PRD · V4-HOST-01 | Requested | DECISION-4 D4-3 |
| A03 | PRD · V4-HOST-02 | Requested (verbatim) | DECISION-5 |
| A04 | PRD · §2.2 introduction ("local-first agent") | Consequential | DECISION-4 D4-3 |
| A05 | PRD · §9 OQ-03 consequence cell | Consequential | DECISION-5 |
| A06 | PRD · §1.1 purpose ("runs local-first") | **Owner item O-8** | DECISION-4 D4-3 |
| A07 | PRD · status paragraph; §0 source table and link | Acceptance-conditional note | — |
| A08 | ARCHITECTURE · V4-ARC-11 | Requested | DECISION-4 D4-3 |
| A09 | ARCHITECTURE · V4-ARC-12 | Requested (host-agent properties) | DECISION-4 D4-3; DECISION-5 |
| A10 | ARCHITECTURE · "Properties the host agent must hold", first bullet | Requested | DECISION-5 |
| A11 | ARCHITECTURE · §1 priority 3; §2 diagram label | Consequential | DECISION-4 D4-3; DECISION-5 |
| A12 | HOST_INTEGRATION · V4-HI-42 (the checkpoint wait, line 137–138) | Requested | DECISION-4 D4-1 |
| A13 | HOST_INTEGRATION · §8.1 Domains paragraph (V4-HOST-02 reference) | Requested | DECISION-5 |
| A14 | HOST_INTEGRATION · V4-HI-70 run record | Consequential | DECISION-5 ("recorded") |
| A15 | EXAMINATION · V4-EXM-22 (V4-WF-05 verification wording) | Requested | DECISION-4 D4-1 |
| A16 | EXAMINATION · V4-EXM-23 | Requested | DECISION-5 |
| A17 | ARCHITECTURE, HOST_INTEGRATION, EXAMINATION · status paragraphs | Acceptance-conditional note | — |

"Requested" means named in the undertaking's owner direction or its brief.
"Consequential" means the same meaning stated elsewhere in the set, which
would otherwise contradict the requested edit. Consequential edits are listed
for the owner in O-7. Not changed, with reasons: PRD V4-APP-02, V4-ARC-04,
ARCHITECTURE §3 "left to the implementation" (the App's own Codex access;
DECISION-5 excludes it); EXAMINATION V4-EXM-12 (App access); V4-EXM-20 "with a
local model" and §7 replacement evidence (a local model remains an option,
and the replacement criterion is the owner's); PRD §10 "Declared checkpoint"
(no waiting clause); PRD V4-AUT-03/04 and OQ-02 "open detail" (DECISION-1 is
first-increment scoped; see O-26); HOST_INTEGRATION §10 item 7 (already says
"data boundary").

---

## Part A — Accepted basis documents

### PRD.md

#### A01 · §4.1 V4-WF-05
Target: PRD.md
Trace: DECISION-4 D4-1 and its clarification; R8-1; EXEC PH-10; WD U-33; ACT AP-11.
The first half is phased, not withdrawn. The second half and reserved acts
are stated as in force. The governance layer is kept serveable.
```old
- **V4-WF-05** The product holds a workflow's declared checkpoints: when a
  run reaches one, the required human act is requested, and the run does not
  record the act as done until the person performs it.
```
```new
- **V4-WF-05** When a run reaches a workflow's declared checkpoint, the
  required human act is requested, and the run does not record the act as
  done until the person performs it. Holding the checkpoint — the run waits
  until the act is performed — is **phased to the governance layer**, not
  withdrawn (DEC-4): in the current phase, declared checkpoints are plan
  guidance that the person and the agents manage, and neither the App nor a
  host's embedded loop enforces a hold, blocks a run, or reports a workflow
  unsupported because a hold cannot be enforced. Enforced holds are applied
  later to the workflows that need them; the declared checkpoint and the
  definitions that enforcement needs are kept so that every such workflow can
  be served. Reserved human acts (§4.5) are unaffected.
```

#### A02 and A03 · §2.2 V4-HOST-01 and V4-HOST-02
Target: PRD.md
Trace: A02 DECISION-4 D4-3 and R8-9. A03 DECISION-5, whose revised V4-HOST-02 text is used **verbatim**. The words and punctuation are the decision's (checked by script: the whitespace-normalized text equals the decision's quoted sentence). Two presentational differences follow this file's convention: the line wrapping, and the provenance suffix "(D-18; DEC-5)" placed before the closing period, as on every PRD requirement.
```old
- **V4-HOST-01** A host's agent runs against a model server the user controls
  by default; a cloud model is used only if the user chooses one and provides
  an API key (D-18).
- **V4-HOST-02** In local operation, a host's agent sends no data to any
  destination other than the configured model server (D-18).
```
```new
- **V4-HOST-01** A host's agent runs on a model the person chooses: a model
  server the user controls, or a cloud model reached by OAuth sign-in or an
  API key. There is no default between them; they are options the person
  chooses among (D-18; DEC-4).
- **V4-HOST-02** A host's agent sends data only to the model service the
  person selected and to destinations the person has allowed — in advance in
  an allow list (by category, such as web access, MCP servers or other APIs,
  or by named destination) or when the agent asks during its work. Nothing
  else is contacted: no analytics, silent provider switch or background
  download unless the person turns it on. Every destination contacted is
  recorded and shown (D-18; DEC-5).
```

#### A04 · §2.2 introduction
Target: PRD.md
Trace: DECISION-4 D4-3 ("There doesn't need to be a 'default' there should just be options"). "Local-first" names a default.
```old
(OD-04). Each host embeds a simpler, local-first agent (D-18) that acts on the
host's objects through the same operations the professional uses.
```
```new
(OD-04). Each host embeds a simpler agent (D-18), running on a local or cloud
model the person chooses (V4-HOST-01), that acts on the host's objects through
the same operations the professional uses.
```

#### A05 · §9 OQ-03, "Consequence if unresolved" cell
Target: PRD.md
Trace: DECISION-5 (the "in local operation" qualifier dropped; destinations the person allows).
```old
Existing local-operation privacy constraints are not relaxed by the new capability |
```
```new
Existing host-agent data constraints (V4-HOST-02) are not relaxed by the new capability: a Domains service is contacted only as a destination the person has allowed |
```

#### A06 · §1.1 Purpose for decomposition — conditional (owner item O-8)
Target: PRD.md
Trace: DECISION-4 D4-3. This is the owner's accepted purpose statement, so it changes only if the owner accepts O-8. The recommended text is below. The alternative is to leave the quotation as it is and rely on V4-HOST-01.
```old
> and validates it to the degree the situation warrants. In host
> applications the agent runs local-first, on a model server the user
> controls. The Chirality App, for creating workflows, is the exemplar each
> application follows.
```
```new
> and validates it to the degree the situation warrants. In host
> applications the agent runs on a model the person chooses — a model server
> the user controls or a cloud model — with no default. The Chirality App,
> for creating workflows, is the exemplar each application follows.
```

#### A07 · Status paragraph and §0 source table — acceptance-conditional
Target: PRD.md
Trace: scope-change method (the amendment is recorded where the basis is read). The `{ACCEPT_DATE}` and `{AMENDMENT_ID}` values come from the accepted group-3 record.
```old
proceeding with decomposition and project definition, not product implementation,
release, or automatic resolution of unruled details.
```
```new
proceeding with decomposition and project definition, not product implementation,
release, or automatic resolution of unruled details. Amended by scope-change
amendment {AMENDMENT_ID}, accepted {ACCEPT_DATE}: V4-WF-05 (phased
checkpoints), V4-HOST-01 and V4-HOST-02 and the text that states the same
meanings, applying owner decisions DEC-4 and DEC-5 (§0).
```
```old
| X-nn / L-nn | Historical exemplars/lessons in `../conceptual/EXEMPLARS_AND_LESSONS.md`; evidence with limits, not automatic additional requirements. |
```
```new
| X-nn / L-nn | Historical exemplars/lessons in `../conceptual/EXEMPLARS_AND_LESSONS.md`; evidence with limits, not automatic additional requirements. |
| DEC-4 / DEC-5 | [Owner decisions][B-DEC45] `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4`, with its clarification (phased checkpoints; model access by OAuth sign-in or an API key, with no default), and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`, with its confirmation (host-agent network destinations); applied by scope-change amendment {AMENDMENT_ID}. |
```
```old
[B-OWNER]: ../execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/OWNER_DIRECTIONS.md
```
```new
[B-OWNER]: ../execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/OWNER_DIRECTIONS.md
[B-DEC45]: ../execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md
```

### ARCHITECTURE.md

#### A11a · §1 priority 3
Target: ARCHITECTURE.md
Trace: DECISION-4 D4-3 (no default); DECISION-5 ("in local operation" qualifier dropped). The priority itself (local models and data privacy, third) is unchanged; only its description is.
```old
3. **Local models and data privacy** — the host model defaults to the local
   server; model traffic stays within the selected local-operation boundary.
   A cloud model is used only by the user's choice. The later Domains
   connector must preserve the applicable data boundary; its deployment is
   unresolved, not an implicit exception (PRD OQ-03).
```
```new
3. **Local models and data privacy** — a host's agent runs on a local model
   server the user controls or on a cloud model the person chooses (OAuth
   sign-in or API key), with no default between them. It sends data only to
   the selected model service and to destinations the person has allowed, and
   every destination contacted is recorded and shown (V4-HOST-01/02; DEC-4,
   DEC-5). The later Domains connector must preserve the applicable data
   boundary; its deployment is unresolved, not an implicit exception (PRD
   OQ-03).
```

#### A11b · §2 diagram, model label
Target: ARCHITECTURE.md
Trace: DECISION-4 D4-3; DECISION-5. The label lines sit outside the drawn boxes, so the box geometry is unchanged.
```old
                                        Local model server (oMLX, LM Studio,
                                        Ollama) — or a cloud API if chosen
```
```new
                                        Local model server (oMLX, LM Studio,
                                        Ollama) or a cloud model (OAuth
                                        sign-in or API key), as the person
                                        chooses; other destinations only if
                                        the person allows them
```

#### A08 and A09 · §4 V4-ARC-11 and V4-ARC-12
Target: ARCHITECTURE.md
Trace: A08 DECISION-4 D4-3; R8-9. A09 DECISION-5 (the host enforces the selected service and allowed destinations and records them) and DECISION-4 D4-3 (a sign-in credential, like a key, stays outside the script; LOOP NW-3…NW-6 as extended by R8-9).
```old
| V4-ARC-11 | **Model: the local model server by default**; a cloud model only if the user chooses one and supplies an API key | D-18 |
| V4-ARC-12 | **Network through the host.** The loop's requests pass through the host's own native layer, which enforces the configured endpoint and holds any key outside the interface's script | D-18; T10 risk 3 |
```
```new
| V4-ARC-11 | **Model: local or cloud, as the person chooses, with no default** — a local model server the user controls, or a cloud model reached by OAuth sign-in or an API key | D-18; DEC-4 |
| V4-ARC-12 | **Network through the host.** The loop's requests pass through the host's own native layer, which allows only the selected model service and the destinations the person has allowed, records every destination contacted, and holds any key or sign-in credential outside the interface's script | D-18; DEC-4; DEC-5; T10 risk 3 |
```

#### A10 · §4 "Properties the host agent must hold", first bullet
Target: ARCHITECTURE.md
Trace: DECISION-5 "Effects, stated at the scope decided", taken point by point: allow list; MCP; in-work permission; always off; record and show; limit; phasing; scope.
```old
- In local operation it makes no network request other than to the
  configured model server (V4-HOST-02).
```
```new
- It sends data only to the model service the person selected and to
  destinations the person has allowed (V4-HOST-02; DEC-5):
  - the allow list works at two levels, a category switch (web access, MCP
    servers, other APIs, …) and named destinations within each category;
    the selected model service, and its sign-in service for a chosen cloud
    model, are always allowed by the person's model choice;
  - an MCP server is allowed only if it follows the stateless MCP revision
    2026-07-28; a server that does not is not offered and cannot be allowed;
  - the agent may ask for a destination during its work, and only the person
    grants it — once, for this run or always, for the destination or its
    category; only the requesting call waits, and a decline is reported to
    the agent as "destination not allowed by the person";
  - analytics or usage reporting, a silent switch to another model or
    provider, and background downloads or updates stay off unless the
    person turns them on;
  - every destination contacted is recorded and shown, in any model mode.

  An MCP server or other outside process can make its own network calls;
  unless it is sandboxed, the host can only decide whether to start it and
  record what it declares. Allow lists locked by an organization and
  enforced sandboxing of outside processes belong to a later governance
  phase. This property governs a host's embedded agent; the App's own Codex
  keeps the person's Codex configuration, approval and sandbox choices.
```

### HOST_INTEGRATION.md

#### A12 · §6 V4-HI-42 (the checkpoint wait)
Target: HOST_INTEGRATION.md
Trace: DECISION-4 D4-1 and its clarification (reserved acts stand; the principle applies to a host's own loop); R8-11 item 2 (V4-HI-42 is guidance in Phase 1). The requirement keeps its identity and its point: autonomy never stands in for the checkpoint's act.
```old
- **V4-HI-42** A workflow's declared checkpoints override autonomy: at a
  checkpoint the run waits for the person's act (V4-WF-05).
```
```new
- **V4-HI-42** Autonomy does not override a workflow's declared checkpoints:
  whatever the autonomy setting, a checkpoint's required act is requested and
  recorded as done only when the person performs it. Holding the run at the
  checkpoint until then is phased to the governance layer (V4-WF-05): in the
  current phase a checkpoint is plan guidance that the person and the agents
  manage, and the reserved acts (V4-HI-30) still bind.
```

#### A13 · §8.1 Domains paragraph (V4-HOST-02 reference)
Target: HOST_INTEGRATION.md
Trace: DECISION-5 (destinations are those the person has allowed).
```old
does not relax V4-HOST-02 or authorize an unselected network destination.
```
```new
does not relax V4-HOST-02: a Domains query service is contacted only as a
destination the person has allowed.
```

#### A14 · §9 V4-HI-70
Target: HOST_INTEGRATION.md
Trace: DECISION-5 ("Every destination contacted is recorded and shown"); R8-13 (RS R15). The run record is where "recorded" lands.
```old
  human acts performed, and the model used (D-07).
```
```new
  human acts performed, the model used and, for a host's agent, each network
  destination contacted (D-07; V4-HOST-02).
```

### EXAMINATION.md

#### A15 · §4 V4-EXM-22 (V4-WF-05 verification wording)
Target: EXAMINATION.md
Trace: DECISION-4 D4-1. The scenario still verifies V4-WF-05, now as phased.
```old
proposes the second. A workflow checkpoint stops the run for a human act.
```
```new
proposes the second. A workflow checkpoint requests a human act, and the act
is recorded only when the person performs it, whatever the autonomy;
stopping the run at the checkpoint is examined only for a workflow that takes
up the governance phase (V4-WF-05).
```

#### A16 · §4 V4-EXM-23
Target: EXAMINATION.md
Trace: DECISION-5. The identifier is kept. The title drops "in local operation", as DECISION-5 drops that qualifier.
```old
**V4-EXM-23 Privacy in local operation.** During V4-EXM-20, all network
traffic from the host is observed. *Verifies* V4-HOST-02: no request goes
anywhere but the configured model server.
```
```new
**V4-EXM-23 Host-agent network destinations.** During V4-EXM-20, all network
traffic from the host is observed. *Verifies* V4-HOST-02: requests go only to
the selected model service and to destinations the person allowed, in
advance or when the agent asked during its work; a declined request reaches
no destination and is reported to the agent as "destination not allowed by
the person"; nothing else is contacted unless the person turned it on; and
every destination contacted is recorded and shown. An outside process that
is not sandboxed is examined within that stated limit.
```

### A17 · Status paragraphs of ARCHITECTURE, HOST_INTEGRATION and EXAMINATION — acceptance-conditional

#### A17a
Target: ARCHITECTURE.md
```old
post-act text is claimed. Identifiers `V4-ARC-<nn>` are retained.
```
```new
post-act text is claimed. Identifiers `V4-ARC-<nn>` are retained. Amended by
scope-change amendment {AMENDMENT_ID}, accepted {ACCEPT_DATE}, for owner
decisions DEC-4 and DEC-5 (PRD §0).
```

#### A17b
Target: HOST_INTEGRATION.md
```old
hash-review these newly consolidated bytes. Existing `V4-HI-<nn>` identities
are retained.
```
```new
hash-review these newly consolidated bytes. Existing `V4-HI-<nn>` identities
are retained. Amended by scope-change amendment {AMENDMENT_ID}, accepted
{ACCEPT_DATE}, for owner decisions DEC-4 and DEC-5 (PRD §0).
```

#### A17c
Target: EXAMINATION.md
```old
these consolidated bytes is claimed. Existing `V4-EXM-<nn>` identities are
retained.
```
```new
these consolidated bytes is claimed. Existing `V4-EXM-<nn>` identities are
retained. Amended by scope-change amendment {AMENDMENT_ID}, accepted
{ACCEPT_DATE}, for owner decisions DEC-4 and DEC-5 (PRD §0).
```

---

## Part B — Decomposition package (`execution/_Decomposition/`)

The decomposition is **SOFTWARE** (`SOFTWARE_DECOMP.md` plus its authoritative
companion registers; `Companion_Inventory.csv`). Its working CSVs equal the
accepted GROUP3 snapshot copies, except for Open_Issues.csv,
External_Dependencies.csv and SOFTWARE_DECOMP.md, which carry later standing
updates. The scope rows below carry, word for word, the meanings the basis
edits change. If they were left alone, the ledger would contradict the
amended PRD and the revised SoWs that cite it (item O-2).

CSV edits are given **per field**: row key, column, exact old value, exact new
value. The applier writes them with a CSV writer, so a new value containing a
comma is quoted. No row is added, removed, renumbered or moved. No
Package/Deliverable mapping, objective mapping, InOutStatus or count changes.

### B1 · ScopeLedger.csv (Unit Ledger) — ScopeItemStatement and DecisionRef

`DecisionRef` for each row below changes from `APP-V4-BASIS-20260926` to
`APP-V4-BASIS-20260926;{DECISION};{AMENDMENT_ID}`, where `{DECISION}` is the
decision named in the row. `SourceRef` (the original seed clause) is kept; the
original is superseded, not erased (Supersession_Delta, IMPACT_ASSESSMENT §7).

| # | Row | Old ScopeItemStatement | New ScopeItemStatement | Decision |
|---|---|---|---|---|
| D-01 | SOW-015 | The shared host integration contract defaults embedded agents to a user-controlled local model server. | The shared host integration contract offers embedded agents a user-controlled local model server as one of the model options the person chooses among, with no default. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 |
| D-02 | SOW-016 | The shared host integration contract permits cloud models only when the person chooses one and supplies an API key. | The shared host integration contract permits a cloud model when the person chooses one, reached by OAuth sign-in or an API key. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 |
| D-03 | SOW-017 | In local operation the host contract permits agent data transmission only to the configured model server. | The host contract permits agent data transmission only to the model service the person selected and to destinations the person has allowed, in advance or when the agent asks during its work; every destination contacted is recorded and shown. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5 |
| D-04 | SOW-052 | At declared workflow checkpoints request the required human act and wait even when operation autonomy otherwise permits direct application. | At declared workflow checkpoints request the required human act even when operation autonomy otherwise permits direct application; in the current phase the checkpoint is plan guidance and the run does not wait; waiting until the act is performed is phased to the governance layer for workflows that need it. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 |
| D-05 | SOW-137 | The embedded-loop integration contract routes network requests through the host native layer enforcing the configured endpoint. | The embedded-loop integration contract routes network requests through the host native layer, which allows only the selected model service and the destinations the person has allowed and records every destination contacted. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5 |
| D-06 | SOW-138 | Keep host API keys outside interface scripts. | Keep host API keys and sign-in credentials outside interface scripts. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 |
| D-07 | SOW-201 | Examine direct low-consequence application with origin/undo, geometry proposals and a human checkpoint overriding autonomy. | Examine direct low-consequence application with origin/undo, geometry proposals and a human checkpoint whose act autonomy never substitutes, holding the run only in the governance phase. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 |
| D-08 | SOW-202 | Coordinate observation of all host network traffic during the local-model journey to check endpoint-only transmission. | Coordinate observation of all host network traffic during the local-model journey to check transmission only to the selected model service and person-allowed destinations, each recorded and shown. | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5 |

SOW-053 ("Do not record a checkpoint's human act as performed until the person
performs it.") is V4-WF-05's second half, in force. It is unchanged.

### B2 · Vocabulary_Map.csv — term "Declared checkpoint", column Notes

| # | Old Notes | New Notes | Decision |
|---|---|---|---|
| D-09 | Run waits for an identified human act even when direct operation autonomy exists. | Requires an identified human act, recorded only when the person performs it, even when direct operation autonomy exists; holding the run there is phased to the governance layer (APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4). | DECISION-4 D4-1 |

### B3 · Deliverables.csv (Secondary Entities) — Description / AnticipatedArtifacts

Each change is a substring within the field; the rest of the field is
unchanged.

| # | Row · column | Old substring | New substring | Decision |
|---|---|---|---|---|
| D-10a | DEL-02-03 · Description | `checkpoint requests wait regardless of direct autonomy;` | `checkpoint acts are requested and recorded only when performed, regardless of direct autonomy (holds are governance phase);` | DECISION-4 D4-1 |
| D-10b | DEL-02-03 · AnticipatedArtifacts | `TEST: missing-tool, checkpoint hold and source-preserving round-trip fixtures` | `TEST: missing-tool, checkpoint recording (governance-phase hold retained) and source-preserving round-trip fixtures` | DECISION-4 D4-1 |
| D-11a | DEL-05-01 · Description | `the minimal local-first Chat Completions loop` | `the minimal Chat Completions loop on a local or cloud model the person chooses` | DECISION-4 D4-3 |
| D-11b | DEL-05-01 · Description | `host owner selects internals and enforces endpoint/key boundaries;` | `host owner selects internals and enforces destination and key/credential boundaries;` | DECISION-4 D4-3; DECISION-5 |
| D-11c | DEL-05-01 · Description | `constrain local traffic` | `limit traffic to the selected model service and allowed destinations` | DECISION-5 |
| D-11d | DEL-05-01 · AnticipatedArtifacts | `TEST: malformed-call, endpoint and responsiveness conformance cases` | `TEST: malformed-call, destination and responsiveness conformance cases` | DECISION-5 |
| D-12a | DEL-09-07 · Description | `actual human acts and endpoint-only operation.` | `actual human acts and host-agent traffic only to the selected model service and allowed destinations.` | DECISION-5 |
| D-12b | DEL-09-07 · Description | `human checkpoints override autonomy;` | `human checkpoint acts are never substituted by autonomy (holds only in the governance phase);` | DECISION-4 D4-1 |
| D-12c | DEL-09-07 · Description | `all local traffic stays on the configured endpoint.` | `all host traffic goes only to the selected model service and person-allowed destinations, each recorded.` | DECISION-5 |

Names, Type, ResponsibleParty, CoversScopeItems, SupportsObjectives and
ContextEnvelope are unchanged. The deliverable kind and granularity do not
change, so there is no decomposition-contract risk.

### B4 · Packages.csv — PKG-05 description — conditional (owner item O-8)

| # | Row · column | Old substring | New substring | Decision |
|---|---|---|---|---|
| D-13 | PKG-05 · third column (description) | `for the minimal local-first host loop and panel.` | `for the minimal host loop, on a local or cloud model the person chooses, and panel.` | DECISION-4 D4-3 |

### B5 · Open_Issues.csv — OI-001, OI-002 — conditional (owner item O-17)

C1-A open item F-8 (the rows still read OPEN with no pointer to DECISION-1).
`Status` stays **OPEN**: operation-specific additions and host adoption
remain.

| # | Row · column | Old value | New value | Decision |
|---|---|---|---|---|
| D-14a | OI-001 · Consequence | Global list not fixed; false attribution is already prohibited. | Ruled for the first increment's App/shared contracts by APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2 (five reserved acts; carried by DEL-04-01); operation-specific additions remain under OI-021 and host adoption under DEP-001. False attribution is already prohibited. | DECISION-1 D2 |
| D-14b | OI-002 · Consequence | No classifier behavior selected by normalization. | Ruled by APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D3: in the App, routine tool-permission and sandbox modes are the user's own Codex setting; hosts have no classifier mode in the first increment; host adoption remains under DEP-001. | DECISION-1 D3 |

### B6 · SOFTWARE_DECOMP.md — Change Register — acceptance-conditional

The semantic section "Change Register" binds to the heading
`## Artifact coverage and decision/change log` (the only decision/change-log
heading in the document). The entry is appended after the section's last
bullet.

#### D-15 · Change Register entry
Target: _Decomposition/SOFTWARE_DECOMP.md
```old
- The separate final audit passed; the actual Group3 act is recorded in the accepted snapshot. A later material change reopens only its affected warrant rather than silently changing accepted scope.
```
```new
- The separate final audit passed; the actual Group3 act is recorded in the accepted snapshot. A later material change reopens only its affected warrant rather than silently changing accepted scope.
- {AMENDMENT_ID} ({ACCEPT_DATE}), requested by the owner (run APP-V4-BASIS-ALIGN-20260928, applying APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 and DECISION-5, and APP-V4-FIRST-INCREMENT-20260928-DECISION-1): MODIFY only. ScopeLedger SOW-015, SOW-016, SOW-017, SOW-052, SOW-137, SOW-138, SOW-201 and SOW-202; Vocabulary_Map "Declared checkpoint"; Deliverables DEL-02-03, DEL-05-01 and DEL-09-07; and, where accepted, PKG-05 and OI-001/OI-002. No ID was added, retired, renumbered or moved; 11 Packages, 41 Deliverables and 262 scope IDs are unchanged. Snapshot: `../_ScopeChange/{AMENDMENT_SNAPSHOT}`.
```

### B7 · Mirrored `_CONTEXT.md` lines (PROJECT/SOFTWARE default propagation writes)

These files mirror the Deliverables.csv and Packages.csv fields above.
`_CONTEXT.md` is not bound by DAG-001's source manifest. The same substrings
change, each once:

| File | Line (field) | Edits |
|---|---|---|
| DEL-02-03 `_CONTEXT.md` (sha256 `b3e0f69e…91ee`) | Description; AnticipatedArtifacts | D-10a; D-10b |
| DEL-05-01 `_CONTEXT.md` (`ddb2ea52…28d1`) | Description; AnticipatedArtifacts; ScopeDescription | D-11a…D-11d; D-13 (if O-8 accepted) |
| DEL-05-02 `_CONTEXT.md` (`265c6631…42e7`) | ScopeDescription | D-13 (if O-8 accepted) |
| DEL-09-07 `_CONTEXT.md` (`bc84dceb…8caf`) | Description | D-12a…D-12c |

### B8 · Surfaces recomputed, not hand-edited

- **Consolidated_Coverage.csv (RECOMPUTE).** Every row binds its document's
  SHA256, a git blob and a line number. 126 rows (PRD 60, HOST_INTEGRATION 31,
  EXAMINATION 22, ARCHITECTURE 13) take the post-amendment hashes and lines.
  The rows for V4-WF-05, V4-HOST-01, V4-HOST-02, V4-ARC-11, V4-ARC-12,
  V4-HI-42, V4-HI-70, V4-EXM-22 and V4-EXM-23 append "amended by
  {AMENDMENT_ID}" to `Standing`. The rule is deterministic: recompute after
  the Part A edits.
- **Coverage_Telemetry.json (RECOMPUTE by the post-change baseline).** Its
  `inputs` bind the ScopeLedger, Deliverables and Packages hashes. The counts
  do not change.
- **NO_CHANGE:** Allocation_Rationale.csv (historical allocation rationale;
  quotes the source meaning at allocation time; homes unchanged),
  Source_Coverage.csv (points to the original seed), Scope_Classification.csv,
  Source_Sections.csv, Objectives.csv, ContextBudgetQA.csv, Companion_Inventory.csv,
  External_Dependencies.csv.
