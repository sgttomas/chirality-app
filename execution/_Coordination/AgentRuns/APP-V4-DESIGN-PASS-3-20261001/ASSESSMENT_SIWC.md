# Assessment — "Sign in with ChatGPT" (2026-10-01)

Requested by the owner before answering DECISIONS_PENDING_2 (L-1…L-7):
"This is a brand new development and is relevant here. Assess and report
back with recommendations before I attend to your seven follow-up choices:
https://help.openai.com/en/articles/20001410-sign-in-with-chatgpt"

Prepared by HELP_HUMAN. Sources read on 2026-10-01 in the built-in browser
(public pages; no sign-in): the help article above; help article 20001542
"Using your ChatGPT plan in other apps and sites"; learn.chatgpt.com
"Sign in with ChatGPT" (partner list); developers.openai.com `/siwc`,
`/siwc/quickstart`, `/siwc/request-client-id`, and the open-source pages
`/siwc/token-sharing-open-source` (overview, sign-in, profiles-and-sessions,
codex-app-server, token-reference, errors-and-recovery, preview-limitations).
Codex 0.158.0 facts are from the scratch binary (`strings`) and its
generated types. Nothing was registered, submitted or signed in.

## What it is (as published)

- **Identity sign-in** (OIDC, scopes `openid profile email`): the app gets
  name, email, picture and a stable `sub`. Commercial use is a limited trial
  with selected partners (client IDs by waitlist).
- **ChatGPT plan usage** (scopes `offline_access resource.invoke
  chatgpt.tokens.use.direct`, resource `https://api.openai.com/v1`): the
  app sends **Responses API** requests with the user's OAuth access token;
  usage counts toward the plan's "ChatGPT Work and Codex usage". Plus and
  Pro only. The user sets a weekly per-app cap and can disconnect in ChatGPT
  Settings. Usage errors stop inference; no silent switch to another billing
  path.
- **Open-source route:** "ChatGPT plan usage is available to all open-source
  partners and selected private clients"; "These docs explain ChatGPT plan
  usage for open-source and locally hosted apps. If you're interested in
  offering it in a paid or remotely hosted app, complete the interest form."
  Dynamic client registration (`client_id=dynamic_agent_client`,
  `agent_name_hint`, a persisted opaque `ext_agent_host_id`), loopback
  redirect on 127.0.0.1, PKCE, no client secret. **The app stores the
  tokens** (access 1 h, rotating refresh 30 d) in protected local storage.
- **Codex app-server, documented route:** the app puts the access token in
  the child's environment (`ACCESS_TOKEN`) and starts app-server with a
  custom Responses provider (`env_key`, `requires_openai_auth=false`,
  `supports_websockets=false`). "No separate Codex sign-in is required."
  Token renewal: "restart app-server with the renewed ACCESS_TOKEN, then
  resume the saved thread." `model/list` is "a catalog, not an entitlement
  check".
- **Preview limits:** `store:false`, `stream:true`; hosted tools unsupported
  (image generation, file search, Code Interpreter, hosted MCP/connectors,
  `tool_search`); "Configurations that emit Responses tool_search will
  fail"; Codex's local shell/MCP tools and child agents work through
  function/custom tools (namespaces are supported).

Codex 0.158.0: the provider keys the route needs (`env_key`,
`requires_openai_auth`, `supports_websockets`) are present in the binary.
App-server also has a stable `chatgptAuthTokens` login (client-supplied
access token plus `chatgptAccountId`) and a `account/chatgptAuthTokens/refresh`
server request; nothing published says it accepts these tokens, so it is an
unverified alternative to the restart route.

## What it changes here

| Point | Effect |
|---|---|
| Custody (V4-ARC-04; D-GOV-43 "authentication separated for Chirality and custodied by Codex") | The open-source route requires the **App** to hold the tokens. Adopting it changes the custody rule, as L-1 option B does. It does match the other half of D-GOV-43: a grant to Chirality, separate from the person's Codex CLI sign-in, which the person sees, caps and can revoke in ChatGPT Settings |
| L-1 (sign-in and API key side by side) | With App custody, one Codex process could carry the plan provider, an API-key provider and local providers, chosen per conversation, so the second App-owned home is no longer the only answer. But see the next row |
| Recovery (D1, K-4; OBS-2 O-2) | The documented route restarts Codex at every token renewal (hourly). A restart interrupts live turns and drops pending requests (observed). Renewal must happen at idle points, a turn longer than the token's remaining life may fail, and plan conversations are best in their own Codex process so restarts touch nothing else |
| K-2 / DEL-01-05 | A fourth access mode: "ChatGPT plan, connected to Chirality". Codex's own ChatGPT sign-in stays available (it serves more plans: Plus/Pro only here) |
| K1-4 identity, L-5 | The App would hold an OpenAI-verified account identity (validated ID token, `sub`, email) from sign-in time. A record could say "account verified at sign-in", while the person's presence at an act stays unverified |
| L-3 plugins | Plugin or connector configurations that make Codex emit `tool_search` fail on this route |
| Delegation | Works on this route (namespace tools supported), unlike LM Studio |
| Host loop (V4-ARC-10, R12-11) | Plan usage is Responses-only; the host loop is Chat Completions. A host could use plan billing only if the model-interface boundary admits a Responses provider. Next relay item; host joins stay deferred (DECISION-3) |
| Eligibility | Chirality is MIT-licensed and the App runs locally, which reads as the open-source route. "Open-source partners" and "supported open source tools" (four listed) leave open whether any open-source app may self-register or must be accepted. Not established |
| Status | Preview; published within the last hours; subject to change |

## Recommendations

*Superseded in part (2026-10-02):* recommendations 1–3 were scaled back after
the owner asked whether there was any pressing need; see "Addendum" and
"The four triggers" below. L-1 and L-6 were answered as originally framed.

1. **Answer L-2, L-3, L-4 and L-7 as you would have; hold L-1 and L-6.** L-5
   stands, with the note above.
2. **Add the plan connection to the design as a PROPOSED fourth access mode**
   (DEL-01-05 round 2): App-held tokens in the macOS keychain, its own Codex
   process, renewal only at idle points, per-app cap and disconnect shown,
   all limits above stated. Keep Codex's own ChatGPT sign-in as the
   designed default until the route is verified.
3. **Propose the custody amendment** for the basis with SCA-V4-003: "custodied
   by Codex, or, for a ChatGPT plan grant made to Chirality, by the App in
   protected OS storage". The same amendment then settles L-1 as option B
   (App-held API key) if you prefer one Codex process for cloud modes.
4. **Settle eligibility before relying on it.** You decide whether to ask
   OpenAI (the interest form is for paid or remotely hosted apps; the
   open-source pages need no form). Nothing is submitted by an agent.
5. **One observation when the design needs it,** with your own Plus or Pro
   sign-in (a new L-6 option): the dynamic registration, the env_key route on
   0.158.0, and whether `chatgptAuthTokens` accepts the token (which would
   remove the hourly restart).
6. **Record the host-loop consequence** on the next-relay list: plan billing
   for a host needs a Responses provider behind the R12-11 boundary.

## Addendum — dependency comparison (owner question, 2026-10-01)

> what about the dependencies management.  How does this "sign-in with ChatGPT" approach compare to what we were currently doing with the Codex instance.

**Runtime suppliers.** Current design: one supplier, Codex, pinned at
0.158.0 (DEL-01-01), owns sign-in, token storage, refresh, logout, account
reads and the model route. SIWC: two suppliers, Codex for the engine and
OpenAI's SIWC authorization service for the grant, which is a preview, not
versioned or pinned, and has no supplier contract in this project. The App
takes over the OAuth client (loopback listener, PKCE, dynamic registration,
ID-token validation against JWKS, keychain storage, serialized refresh,
revocation, error handling).

| Concern | Codex-custodied sign-in (current) | SIWC plan grant |
|---|---|---|
| Sign-in flow | Codex `account/login/start` (browser or device code) | App's own OAuth client |
| Token custody | Codex home (per App home under K-1) | App (keychain) |
| Renewal | Inside Codex, no interruption | App, hourly; documented route restarts Codex |
| Model route | Codex's ChatGPT route, all Codex features | `api.openai.com/v1` Responses, preview limits (no hosted tools; `tool_search` fails) |
| Model list | From Codex | Bundled catalog, "not an entitlement check" |
| Plans | Codex's supported ChatGPT plans | Plus and Pro only |
| Usage seen by the person | Codex usage | A "Chirality" line with cap and disconnect |
| Account home | Each home holds one account (hence L-1's second home) | No credential in any home; one Codex home can serve every mode |
| Pinning and qualification | Covered by the Codex pin | Needs its own record and observation |
| Doctrine | Matches D-GOV-43 and V4-ARC-04 | Needs the custody amendment |

**Project dependency graph (DAG-003).** DEL-01-05's register traces SOW-009
and SOW-010 ("credentials held by Codex") and OBJ-002 ("three
user-selectable Codex access modes"); both change. Its only production
supplier is DEL-01-01. SIWC would add:

- an external supplier row (OpenAI's authorization service), with
  satisfaction pending eligibility and observation;
- renewal at idle points, which needs DEL-01-02's live-work state. A row
  DEL-01-05 → DEL-01-02 closes a cycle (D4, F0 §3), so it stays a runtime
  value (C-23's "assess live work"), as now;
- restarts through HOSTING's existing stop and start operations, written as
  use of DEL-01-01, not as a new requirement on it (a requirement the other
  way would also close a cycle);
- a verified-identity source for DEL-04-03's person record (runtime value);
- packaging items for DEL-01-06 (keychain access, loopback port, OpenAI's
  branding rules, open-source eligibility alongside OI-007);
- a next-relay note for DEL-05-01 (plan billing needs a Responses provider).

These go through SCA-V4-003 with `dependency-extract` and a `project-dag`
currency check, like the other proposals.

**Recommendation, unchanged.** Keep Codex-custodied sign-in as the designed
default: one pinned supplier, no restart coupling, no doctrine change. Design
the SIWC grant as a PROPOSED optional mode behind eligibility and one
observation, and record its external dependency with that status.

## Correction — what the pin buys (owner remark, 2026-10-01)

> btw Codex frequently updates its version in significant ways.  Pinning can only last so long.

The rows "Pinning and qualification: covered by the Codex pin" overstate it.
The 0.158.0 pin is a fixed reference for design and tests, not lasting
stability: npm lists 0.154.0 (2026-09-09), 0.158.0 (2026-09-28) and, as of
this note, 0.160.0 (2026-10-01T20:26Z), five releases after 0.158.0 in three
days. Both routes face supplier churn; the SIWC route touches fewer Codex
internals (a provider entry instead of Codex's account methods) but is itself
a preview. The conclusion (no pressing need) is unchanged.

## The four triggers (as given to the owner, 2026-10-02; recorded here late)

HELP_HUMAN's answer to "there's no pressing need … or do you see any?" named
four developments that would make the plan grant pressing. R19-4 cites them;
they were stated in the chat and are recorded here:

1. OpenAI restricts third-party apps from using Codex's own ChatGPT sign-in
   and points them to Sign in with ChatGPT.
2. The owner wants a per-app usage cap and a "Chirality" entry in ChatGPT
   settings as product features.
3. A host needs plan billing when host joins resume.
4. The owner decides records should carry an account identity OpenAI has
   verified.

Conditions before adoption (separate from the triggers): eligibility for the
open-source route settled; the custody amendment accepted; one observation
with the owner's own Plus or Pro sign-in.
