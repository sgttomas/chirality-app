# Owner decisions requested (2) — APP-V4-FIRST-INCREMENT-20260928

Prepared by HELP_HUMAN, 2026-09-28, from Wave-2 findings. **Answered:** see
[OWNER_DECISIONS.md](OWNER_DECISIONS.md) DECISION-2 (D5 user flexibility; D6
deferred to the SWBPIPE answer). The text below is the package as presented. W9 and
the Wave-1 residual sweep continue meanwhile. Until these are answered, both
subjects stay `UNRESOLVED`, with an owner and a point of need, in the affected
drafts.

## D5 — Data boundary when the App's Codex reads host content (DEL-03-03 U-X2 / F-12)

**Finding.** With external access enabled (A13), host model content read over
the MCP/CLI channel goes into the App conversation. It therefore reaches that
conversation's model, which may be a cloud model (ChatGPT sign-in or an API
key). V4-HOST-02 ("no destination other than the configured model server")
governs the host's own embedded agent. It does not address App conversations.
Enabling the channel authorizes no data destination, and no deliverable or open
issue owns this boundary. The priority is Architecture §1.3: local models and
data privacy, with cloud used only by the user's choice.

| Option | Effect |
|---|---|
| **A (recommended) — the person's per-conversation choice, disclosed at enablement** | Host content may flow to the App conversation's selected model. The person makes the choice (D-06 / V4-APP-02 provider per conversation). The A13 enablement act and the channel status must show the conversation's model destination, and an App run records it. A host may still restrict its channel, for example to local-provider conversations only; that is the host's policy. The App's local-provider path (DEL-01-05) keeps a fully local option available. |
| B — local-only external access | External access is permitted only when the App conversation uses a local model provider. This is the strongest privacy default, but it makes App↔host control unusable with ChatGPT sign-in, which is the App's primary harness experience. |
| C — defer | Keep open until OI-021 selects the first operation. The adapter contract cannot fix its enablement disclosure until then. |

## D6 — How the App holds its own runs at workflow checkpoints (DEL-02-03 F-10 / U-E1)

**Finding.** The App runs stock Codex (V4-ARC-01, M-2). Codex dispatches tool
calls, including MCP calls to a host, itself. Under D3 the App does not control
routine tool permission. The App therefore has no guaranteed hold point before
dispatch. It has three candidates:

- **HP-1:** App code interposed on the dispatch path, either dynamic tools
  (experimental API) or an App MCP proxy;
- **HP-2:** interrupting the turn after observation (`turn/interrupt`, seen only
  in the 0.158.0 generated types);
- **HP-3:** declining a tool-permission request under a named rule.

The acceptance checkpoint remains host-enforceable through the governing
checkpoint constraint (R2-12), if the host adopts it.

| Option | Effect |
|---|---|
| **A (recommended) — host-enforced plus truthful App best effort** | For host operations, checkpoints are enforced on the host route through the governing checkpoint constraint, which is a relay question. For App-side steps, the App uses HP-2 and HP-3 as best effort, never claims a hold it cannot enforce, and records "action during hold". Each checkpoint reports its *hold support*; one the surface cannot enforce makes the workflow *unsupported* there. A bounded spike observes `turn/interrupt` at 0.158.0 before any reliance. No App code is interposed on dispatch in the first increment, which keeps stock Codex and native presentation. |
| B — interpose App code | The App registers host operations as dynamic tools, or runs an App MCP proxy. This gives a real pre-dispatch hold (HP-1). It adds dependence on Codex's experimental API and a translation layer (tension with M-2 and V4-ARC-05), and it conflicts with the adapter SoW's "no new server". |
| C — defer | Wait for the SWBPIPE seam answer. The App checkpoint semantics stay partly unenforceable in the definitions. |
