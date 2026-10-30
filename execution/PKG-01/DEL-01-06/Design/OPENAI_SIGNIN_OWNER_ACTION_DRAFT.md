# OpenAI distributed sign-in: current source finding and owner draft

Read-only supplier-documentation check, 2026-10-29. Draft for the owner; not
sent, not a registration, legal conclusion, changed commitment or supplier
approval of this product. `Evidence/PKG/terms/OpenAI.json` remains `unresolved`
and `distribution_decision: not_made`; OI-007/DEP-004/SOW-117 remain unchanged.
This finding is separate from PR15 and its immutable candidate evidence.

## What the current official sources establish

1. [Codex app-server, Auth endpoints](https://learn.chatgpt.com/docs/app-server#auth-endpoints)
   expressly says local or open-source applications using app-server
   authentication can continue using it, recommends SIWC migration, and says
   app-server authentication has never been permitted for commercial or hosted
   services. This is a published written supplier position with a stated scope,
   not a product-specific response or permission for every distribution model.
2. [SIWC open-source/local overview](https://developers.openai.com/siwc/token-sharing-open-source)
   documents plan usage for open-source and locally hosted apps; paid or remotely
   hosted apps are directed to the interest form. The
   [OSS registration flow](https://developers.openai.com/siwc/token-sharing-open-source/sign-in)
   uses initial `dynamic_agent_client`, a persistent host ID and the app's real
   name; the user authorizes registration and receives an account/workspace-bound
   issued client ID. This direct flow needs neither a client secret nor partner
   API key. It is not developer-wide advance client-ID registration.
3. [Request a client ID](https://developers.openai.com/siwc/request-client-id)
   describes select commercial partners and links an interest form. Do not
   turn that route into an unsupported universal OSS registration prerequisite.
4. [SIWC with Codex app-server](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server)
   documents an app-managed OAuth token passed to a Responses provider, app
   attribution matching its registration name, and app-owned token renewal with
   process restart/resume. This is a different account/custody flow from the
   App's current stock-Codex-managed login. Its
   [preview limits](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations)
   and [UI/UX guidance](https://developers.openai.com/siwc/ui-ux-guidelines)
   apply to that route; they do not prove the pinned supplier implements it or
   authorize silently replacing the current flow.

The official developers Codex auth/app-server links redirect to the fetched
ChatGPT Learn pages. Both those pages and the SIWC pages above were actually
retrieved. Published pages do not authenticate a project-specific approval,
classify an unselected business model, resolve binary/component redistribution
notices, or supply the owner's public distribution decision. No supplier legal
terms outside these allowed documentation sources were examined.

## Actual product flow and exact remaining question

Repository source is MIT-licensed (`LICENSE.md`). The retained macOS Tauri App
bundles the complete unmodified official stock Codex `0.160.0` platform tree
and starts app-server locally over private stdio. `hosting.rs`
`account_oauth_start` sends `account/login/start` with `type: chatgpt` or
`chatgptDeviceCode`; Codex owns the managed OAuth flow and credential refresh
in the selected App-owned local account home. The App supplies native sign-in
controls/presentation; it does not currently implement SIWC dynamic registration
or its own token exchange. API-key and local-provider modes are separate.
These are source facts, not live authentication qualification.

## First-release disposition, not a new inquiry gate

Agent0/owner first confirms the actual first offering and unchanged existing
managed-login flow. If it is free/local/OSS within the published continuation,
the proposed route is to accept that identified official statement as the
written-position evidence, retain its exact source/date/scope and separately
assess actual bundled-component notices. A possible official contact is not a
reason to demand a project-specific reply. Commercial/hosted or changed-auth
scope uses its applicable documented route only when actually selected.

The previous external inquiry is optional, **only for a real unanswered issue**:
“Chirality App uses the existing local stock-Codex managed sign-in flow.
Our selected offering is [actual offering]. The published local/OSS continuation
states [exact applicable scope]. Please clarify [one specific unresolved
condition], and identify the authoritative written basis.” Nothing is sent,
registered or signed in by preparing this draft.

## Proposed OLD → NEW clauses — PENDING OWNER DISPOSITION

Basis: current DEL-01-06 ScopeOfWork, SHA-256
`08e30b97baeb06ae57b6166d6358f5c68ad1d934102df7ea094ce6cc57abd795`.
The OLD blocks are exact current text; NEW is a proposed replacement, not applied
or accepted. Citation suffixes are preserved. No present terms/distribution
resolution, change to historical evidence, or public release is claimed.

### OUT-004

OLD:

- **OUT-004** — DOC: written supplier distribution-terms response obtained by the owner before public release beyond owner use, together with its source, actual custody and applicability to the distributed sign-in in question. Carry an unresolved response explicitly before it is obtained; any future Claude sign-in retains its own conditional terms question. Scope SOW-117; objective OBJ-002. [B1; B3: OI-007; B4: DEP-004; B5: OQ-08; B6: §§6, 8]

NEW — proposed:

- **OUT-004** — DOC: the supplier's written distribution-terms position, evidenced by either an applicable identified official supplier publication or a direct supplier response, obtained and retained by the owner before public release beyond owner use. Retain the exact source and supplier identity, publication/response date when supplied and retrieval/receipt date, evidence reference and actual custody, the first-release offering and sign-in flow to which it applies, applicable conditions/exclusions and the owner's applicability disposition. Keep missing or unestablished applicability unresolved. Record the owner's public distribution decision separately, or as not made; neither evidence route supplies that decision. Any future Claude sign-in retains its own conditional terms question only if that need arises. Scope SOW-117; objective OBJ-002. [B1; B3: OI-007; B4: DEP-004; B5: OQ-08; B6: §§6, 8]

### REQ-004

OLD:

- **REQ-004** — The conditional written-response obligation shall be satisfied before public release beyond owner use, with the actual supplier position and owner custody recorded as described in CLM-003. Missing or unconfirmed terms shall remain visibly unresolved at that point of need. They shall not be represented as settled by a package launch, source inspection, an earlier sign-in assumption or this contract; they do not create a blanket prerequisite to owner use or independent development. [B1; B3: OI-007; B4: DEP-004; B5: OQ-08; B6: §§6, 8]

NEW — proposed:

- **REQ-004** — The conditional written-position obligation shall be satisfied before public release beyond owner use by retaining either an applicable identified official supplier publication or a direct supplier response, with source, dates, custody, actual release/sign-in scope and owner applicability disposition as described in CLM-003 and OUT-004. A further product-specific response is not required solely because one could be requested when an applicable official publication is accepted as the evidence. Missing evidence or unestablished applicability remains visibly unresolved. Package execution, an agent's assertion or an earlier sign-in assumption cannot substitute for that evidence; speculative future offerings do not add conditions to the selected first release. Owner use and independent development remain ungated by this conditional public-release obligation, and the owner's public distribution decision remains separate. [B1; B3: OI-007; B4: DEP-004; B5: OQ-08; B6: §§6, 8]

### AC-004

OLD:

- **AC-004** — OUT-004 contains the actual written supplier response obtained by the owner before public release beyond owner use. Before that response exists, the record reports the conditional obligation as unresolved rather than claiming this criterion satisfied. Any future Claude sign-in has its own response only if that need arises. Verify with VER-004. [REQ-004]

NEW — proposed:

- **AC-004** — OUT-004 retains the exact applicable official supplier publication or direct response obtained by the owner before public release beyond owner use, with source and supplier identity, publication/response date when supplied, retrieval/receipt date, custody and the owner-confirmed scope/conditions for the selected first-release offering and sign-in flow. An applicable identified official publication may satisfy this criterion without an additional product-specific reply. Before applicable evidence is retained and its applicability established, the record remains unresolved. Any future Claude sign-in has its own applicable position only if that need arises. Verify with VER-004. [REQ-004]

### VER-004

OLD:

- **VER-004** — Compare the terms record with the actual written response and its available custody evidence, supplier identity, distributed-sign-in applicability and owner's obtaining act. At the public-release point of need, an absent response leaves AC-004 unsatisfied. Verify faithful recording of a genuinely evidenced supplier response/owner act with actor distinct from recorder; also check that a draft request, unconfirmed assumption, package pass or recorder assertion cannot fabricate a supplier answer or owner distribution decision. A missing public distribution decision stays unclaimed; terms receipt itself does not establish it. [AC-004, AC-005; B3: OI-007; B4: DEP-004]

NEW — proposed:

- **VER-004** — Compare the terms evidence with the exact official supplier publication or direct response and its source identity, dates and custody; compare its conditions and exclusions with the owner's stated first-release offering and actual sign-in flow. Verify the owner's obtaining/retention and applicability disposition separately from the recorder's act. An accepted applicable publication must not fail solely for lack of a direct reply. Missing evidence, unsupported applicability, a draft inquiry, package pass or recorder assertion cannot establish the supplier position. Check that source publication, evidence capture and applicability do not fabricate product-specific supplier approval or the owner's public distribution decision; retain that separate decision reference or not_made. Bundled-component licensing/notices remain a separate packaging assessment, not presumed satisfied by authentication guidance. [AC-004, AC-005; B3: OI-007; B4: DEP-004]

### CLM-003

OLD:

- **CLM-003** — Distributed-sign-in terms remain OI-007, owned by **Owner and relevant supplier**, needed **Before public release beyond owner use**. DEP-004 names OpenAI and conditional future Anthropic as suppliers of a written position, and the **Owner public distribution decision** as consumer. The owner obtains the response; the relevant supplier supplies its position. A future Claude sign-in question applies only if that need arises. The accepted conditional obligation is IN; its answer is unconfirmed. The accepted project boundary does not block owner use or independent development on this unresolved answer and supplies no legal conclusion. [B1: DEL-01-06; B3: OI-007; B4: DEP-004; B5: OQ-08; B6: §6]

NEW — proposed:

- **CLM-003** — Distributed-sign-in terms remain OI-007, owned by Owner and relevant supplier, needed before public release beyond owner use. DEP-004 names OpenAI and conditional future Anthropic as suppliers of a written position and the owner's public distribution decision as consumer. The supplier authors the official publication or direct response; the owner obtains and retains the applicable position, establishes its applicability to the selected release/sign-in scope, and separately decides public distribution. Either applicable identified official publication or direct response may evidence the position; a product-specific reply is not a blanket prerequisite. A future Claude sign-in question applies only if that need arises. The conditional obligation remains IN; its current satisfaction is unconfirmed. Owner use and independent development are not blocked by the unresolved public-release position, and no legal conclusion is supplied. [B1: DEL-01-06; B3: OI-007; B4: DEP-004; B5: OQ-08; B6: §6]

## Necessary correspondence only — also proposed

**ScopeOfWork Purpose**

OLD:

the written distributed-sign-in response at its accepted public-release point of need

NEW — proposed:

the applicable written distributed-sign-in position, evidenced by an identified official supplier publication or direct response, at its accepted public-release point of need

**ScopeOfWork SOW-117 local-contribution cell**

OLD:

Preserve the conditional obligation, its actual supplier response and unresolved standing

NEW — proposed:

Preserve the conditional obligation, applicable official publication or direct response, and unresolved standing until applicability is established

**ScopeOfWork Interfaces sentence**

OLD:

Obtain and retain the written terms response through the owner before public distribution beyond owner use.

NEW — proposed:

Obtain and retain the applicable written terms position through the owner before public distribution beyond owner use, using either an identified official supplier publication or a direct response.

**ScopeOfWork OUT-004 traceability cell**

OLD:

Written supplier response obtained by the owner before public release beyond owner use, or explicit unsatisfied obligation before receipt

NEW — proposed:

Applicable official supplier publication or direct response obtained and retained by the owner before public release beyond owner use, or explicit unresolved evidence/applicability

**Design PK-R4**

OLD:

- **PK-R4** (terms) The recorder is neither the obtainer of a response nor
  the decider of distribution.

NEW — proposed:

- **PK-R4** (terms) The recorder does not acquire the owner's applicability or distribution authority by capturing a publication or response.
  Attribute supplier authorship, owner obtaining/retention and applicability,
  and the separate owner distribution decision to their actual actors.

**Design §9**

OLD:

One record per supplier: OpenAI now; Anthropic only if a Claude sign-in is
ever offered. State `unresolved` until a written response exists; then
`response_received` with the response by reference, its custody, who
obtained it (the owner), what it applies to in its own words, and the date.
The owner's distribution decision is a separate reference or `not_made`; a
response never stands for it (PK-R4; AC-005). Owner use and development are
not gated by an `unresolved` record (TBD-002).

NEW — proposed:

One terms account per supplier whose sign-in is actually offered. Retain either
an applicable identified official supplier publication or direct response,
including exact source/supplier, publication/response date if supplied,
retrieval/receipt date, preserved content reference and custody, actual selected
release/authentication scope, conditions/exclusions and the owner's applicability
disposition. Until applicable evidence is retained and applicability established,
keep the position unresolved. A direct reply is not additionally required merely
because an official contact could answer. The owner's separate public distribution
decision remains its own reference or not_made; evidence/currentness observations
and applicability do not decide release. Owner use/development remain ungated.

Preserve every historical PKG-v0.2 record and its closed schema/state meaning.
Its response_received/response representation cannot truthfully label an official
publication as a direct reply. On approval, supply a small versioned terms-record
successor that distinguishes official_publication from direct_response and carries
the evidence/applicability fields above; do not silently reinterpret old records.
The historical unresolved OpenAI.json remains unchanged until a separately
recorded owner disposition and applicable new evidence record exist.

Additional exact editorial correspondence — all proposed, not applied:

| Locus | OLD | NEW |
|---|---|---|
| Design introduction | how the written distribution-terms response is kept. | how the applicable written distribution-terms position (identified official publication or direct response) is kept. |
| Design §1 written-position row | The supplier supplies; the owner obtains | The supplier publishes or responds; the owner obtains/retains and establishes applicability |
| Design §11 PKG-VC-04 expected cell | `unresolved` before a response; actors kept apart | `unresolved` before applicable evidence and applicability are established; actors kept apart |
| deliverable.yaml incoming DEP-004 condition | Obtain and retain the actual written supplier position through the owner before public release beyond owner use; future Anthropic/Claude terms apply only if that sign-in need arises. | Obtain and retain through the owner either an applicable identified official supplier publication or direct response before public release beyond owner use, with source/date/custody, selected release/sign-in scope and owner applicability disposition; future Anthropic/Claude terms apply only if that sign-in need arises. |
| deliverable.yaml downstream DEP-004 condition | The owner public distribution decision consumes the written supplier position retained with source, actual custody and applicability. | The owner public distribution decision consumes the applicable written supplier position, evidenced by an identified official publication or direct response retained with source/date/custody, selected release/sign-in scope and owner applicability disposition; the distribution decision remains separate. |

Keep metadata arcs, historical source locators/provenance and current unresolved
labels unchanged; these condition edits change no topology or present satisfaction.

REQ-005, AC-005/006, VER-005, AX-002, TBD-002 and historical source tables remain
unchanged: they already preserve actual actors, separate distribution authority,
open status and independent development. No speculative future commercial,
embedded or migration question becomes a first-release blocker. This proposal
needs the owner's disposition before any governing clause/schema/record changes.
