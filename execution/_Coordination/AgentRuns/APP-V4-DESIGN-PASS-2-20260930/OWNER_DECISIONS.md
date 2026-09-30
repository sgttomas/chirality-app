# Owner decisions — APP-V4-DESIGN-PASS-2-20260930

Exact owner text, as given in the chat session with HELP_HUMAN. Custody: the
session transcript; recorded here by HELP_HUMAN. A record here is not a claim
that the owner reviewed any file.

## Start direction (2026-09-30)

> Start the next first-increment design pass using DAG-003.

Context: HELP_HUMAN had offered four possible next undertakings after
`APP-V4-SCA002-20260929` closed, and recommended this one: "The next
first-increment design pass, using DAG-003 to plan it. It would also re-point
the 17 design files at the amended requirement texts, which closes one of the
two items you deferred."

**Reading (HELP_HUMAN's interpretation, not owner text):** a second design
pass on the 14 first-increment deliverables, planned through accepted
DAG-003, that (1) re-pins their Design files to the amended basis and the
revised ScopeOfWork contracts, and (2) develops the design toward the 60%
level described in `loop/LOOP_INIT.md`. The exact content of (2) is set by a
scoping survey (node S1) and recorded in the work graph. The coverage-telemetry
rebuild, the SWBPIPE relay and the audit-script fix were offered separately
and are not selected.

## Standing directions that apply

- Git: "You should have the ability to monitor PRs and merge once the CI goes
  green. I want you to do that. Tell me if something is blocking."
  (2026-09-28). Applied as before: auto-merge is enabled only after an
  independent review of the candidate finds nothing blocking.
- DECISION-3 (`APP-V4-SWBPIPE-INTAKE-20260928`): host joins deferred.
- DECISION-4 and DECISION-5 of that run: phased checkpoints; model access by
  OAuth or API key with no default; host-agent network destinations.

## DECISION-K1 (owner, exact, 2026-09-30)

**Custody:** the owner's chat message to HELP_HUMAN, after the package was
presented as [DECISIONS_PENDING.md](DECISIONS_PENDING.md) (sha256 prefix
`f1e968fe9cc0d40a`, committed at `be55f32502`) and as the review page
https://claude.ai/artifact/9JXQB9hfhyrFnLk7CKMtSf (Version 1). The even-handed
draft behind it is [DECISIONS_DRAFT.md](DECISIONS_DRAFT.md) (`4b34c24f52a63d59`).

> accept all six as recommended

**Effects, stated at the scope decided** (each is the option marked
"recommended" in DECISIONS_PENDING.md Part 1):

- **K1-1 Who asks.** The agent carrying out the workflow asks the person for
  the checkpoint's act; the product gives the agent the checkpoint, offers the
  means to act, and records what it observes. Neither the App nor a host's
  loop requests in the agent's place, pauses the run or otherwise reacts to
  an arrival. R9-1's requester reading becomes SETTLED (this decision).
- **K1-2 An earlier act counts, in the current phase,** when it is of the
  required kind and the content it was made on is still current. The record
  cites the earlier act and its time. A workflow that takes up the governance
  phase may require a fresh act. The PROPOSED rule SP-6 ("only acts captured
  at or after arrival") is replaced for the current phase and kept as a
  governance-phase option.
- **K1-3 Partial lapse.** When one act covered several items and only some
  change, a new act on the changed items alone answers the checkpoint,
  together with the earlier act for the unchanged items.
- **K1-4 The App act control and the person's identity.**
  - The act control's obligation is proposed for DEL-01-04's contract at the
    next amendment. No design work on it in this pass; this run's closeout
    collects the wording with its other proposed contract items.
  - The App records the person's identity from what it can observe (the name
    set in the App, the operating-system account, and the Codex account when
    Codex reports one), marked "identity not verified". A verified identity
    is left for the governance phase.
- **K1-5 Allow list.** A named destination is allowed on its own; a category
  switch means "allow everything in this category". With the switch off,
  only the named entries in that category are allowed. LOOP N-OPEN-4 is
  closed by this decision.
- **K1-6 Prototypes and observations.**
  - A read-only fetch of two published specifications is allowed: the Chat
    Completions reference the host-loop cases are written against, and the
    stateless MCP revision (2026-07-28).
  - For one live Codex turn that calls a test tool, a local model in LM
    Studio is tried first. The owner's Codex sign-in is asked for only if the
    local route cannot produce a tool call.
  - Anything sent to a model is invented example material. Each observation
    is a dated record at one version, not qualification.
  - **Recorder's note:** downloading a chat model into LM Studio is a file
    download. HELP_HUMAN will name the model, its source and its size to the
    owner and wait for a yes before downloading it.

Part 2 of the package (matters the integrator takes in this pass) was
presented as "open to being overruled" (DECISIONS_PENDING.md) and on the
review page under the heading "Taken by me in this pass; say if you
disagree"; the owner did not object. Parts 3 and 4
stand as presented.

## Executor-model direction (owner, exact, 2026-09-30)

**Custody:** the owner's chat message to HELP_HUMAN, after DECISION-K1.

> Ensure you are using `opus-5.5` models on `high` reasoning for your Type 1 and Type 2 agent instances.

**Effect:** every executor launched after this direction runs on Claude Opus
5.5 (`claude-opus-5-5`) at high effort. How it is applied, and which earlier
executors ran on Claude Fable 5.1, is recorded in [DISPATCH.md](DISPATCH.md).
