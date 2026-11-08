# Current production subject and focused v4 testing

## Owner message custody, 2026-11-02

Parent relayed the owner: “1. keep the app ID. Figure out a feasible testing
strategy.” The selected production identifier is **com.chirality.app**, using
the already recovered Developer ID team as the basis for the closed private
publisher input. This supersedes the separate-v4 route/proposed identifier.
Minimum macOS15 and planned package version4.0.0 remain selected. No credential,
signing, entitlement or runtime activation action follows from identifier choice.

The owner then corrected scope: “Actually I don't want to do a lot of testing
compared to v3. It was an ephemeral version, setting us up for v4. I will just
test v4.” This selects v4 functional testing, not a v3 equivalence, regression,
migration or rollback qualification campaign. No such campaign is a new gate.
Historical pending drafts, release artifacts and the12d26 unsigned candidate
retain their original subjects. Existing v3 stays preserved as fallback and
visual reference; no overwrite or launch was performed for this examination.

## Narrow source/config collision findings

At source0d43475e, lib.rs startup obtains Tauri app_data_dir and installs
capture_seal/installation consumers from it. records_store::for_app places
release records at AppData/records unless the person chose another location;
release ignores the development CHIRALITY_RECORDS_STORE override. capture_seal
uses AppData/capture-seal; the keychain continuity provider uses the sibling
capture-seal-keychain directory. Therefore a different productName or an
alternate .app filesystem path does not isolate same-ID AppData/keychain use.
Changing HOME alone is not an established isolation boundary for macOS APIs.

Read-only installed bundle Info.plist confirms v3.0.1/com.chirality.app and no
SUFeedURL field. That is not proof of its complete storage or updater behavior.
The v3.0.1 Git tag has no frontend tree or authoritative installed desktop
storage layout; do not invent a v3 data mapping from it. Current v4 base
identifier is development skeleton; no updater dependency/config was found in
Cargo.toml/tauri.conf.json. No owner data, preferences, keyring or credentials
were opened. Same-ID collision is conservatively possible; no absence claim.

## Practical execution sequence

1. Iterative UI/native work uses separately named builds and explicit distinct
   development/package-test IDs through the existing helper. Use fresh scratch
   Codex homes and disposable test projects/records. The helper's default-None
   route permits source/UI/startup work but does not qualify production publisher,
   signing, enrollment or installed custody. Do not duplicate retained builds
   merely for branch movement.
2. For the eventual selected, signed com.chirality.app candidate, use an explicitly
   chosen clean local macOS test account with its own OS home and keychain and
   synthetic projects. This is a proposed practical isolation route, not account
   provisioning authorization or a VM/cloud request. Keep the candidate outside
   /Applications/Chirality.app; invoke its exact absolute bundle/executable path,
   not a bundle-ID lookup that could select v3. The separate account is needed
   for per-user namespaces, not a v3 compatibility study. A second path alone
   is insufficient. Before execution, verify the selected account/root and
   non-overlap without inspecting owner private data. No immediate owner act is
   requested while source/notice/signing preparation continues.
3. The 2026-11-05 owner correction assigns development testing to agents; Agent 0
   carries the App to a publication-ready recommendation before owner testing.
   Both standalone journeys remain open: J1 first use, an existing workflow,
   useful real-model work and finding results; J2 create, trial, register and
   reuse a workflow and return to unfinished work. Collect actual package/S4/
   functional witnesses against the applicable exact candidate through the
   existing consumer path; mocked/source passes do not replace them. Signing,
   enrollment and any necessary account operation remain separately authorized
   stages. Existing owner data is not a fixture: no implicit migration, key
   import, reset, resealing or cleanup.

The identifier choice does not select service/account/access-group values.
Runtime owns SEAL_C_KEYCHAIN_SIGNING_JOIN.md; it has been notified of the new
subject and narrowed test scope. AppIdentifierPrefix comes from actual
signing authorization, never a guessed team prefix. Existing namespaces do not
supply authority to enroll, import or regenerate keys. No capability narrowing
is inferred; the owner's question about human functions remains for Agent0.

The next candidate must account for the frontend lane's exact ten IBM Plex
WOFF2 assets and OFL license from its WORKSPACE_SETUP_PRESENTATION.md table.
They are a separate font notice/resource subject, not covered by the eleven
supplier-source receipts. No historical inventory is relabelled.

Reconciled in [`app/packaging/font_notice/`](../../../../app/packaging/font_notice/README.md).
All eleven files are Git-blob identical to v3 at Root `485051ea`. The index records
each font's own name-table copyright (Mono 2017, Sans 2019, Serif 2020 IBM Corp.)
and OFL licence URL. That supplies the Mono and Serif notices the retained OFL
header omits. Production input preparation now refuses a stale font index and maps
the index and OFL text to `third-party-notices/fonts/`. The declared
`@fontsource` 5.3.0 upstream remains unverified offline. Plans prepared before
this change, including `AcP2w3vq`, do not carry the font notice.
