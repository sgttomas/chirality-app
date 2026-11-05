# Renderer check of the Run guide's results and run order, 2026-11-04

Standing: automated renderer observations of App-side behaviour. They are not
owner or human acceptance, not native J1/J2 passes, and not model, sign-in,
native window or production qualification.

## Subject

- **Merged result:** PR #125, merged to main as `2ed3d14f`. Its whole tree
  (`8aa23e87…`) is identical to the head integrated from, `2d1edca3`.
- **Render subjects:** `d341f57a`, `9efa17a7`, `ca324f2b`, `addba4ba` and
  `0b9a9068`. All are ancestors of `2d1edca3`, and each keeps its own identity.
- **Not rendered:** the later `runReading` guard (`e6e80559`) was checked only by
  source review and mounted tests. The parent ran 15 tests and probes of stale
  and current requests. This account makes no renderer claim for it.
- **Run order:** the `preparationOrder` producer is #127, merged as main
  `6d43298d`. Its tests were run by the author, not by me.
- **Baseline:** the Run guide facts observed on `9248a36e`.
- **Builds:** each build is an offline `npm run build` of an immutable
  `git archive` export. The lock file and `package.json` were unchanged
  throughout.

## Method

- **Renderer:** cached headless Chromium, driven over CDP from a 127.0.0.1
  server, at desktop (1100×800) and narrow (480×860) widths.
- **Real input:** host status and a run row from the frontend's executed Rust
  producers (packet sha256 `6d292510…`). The synthetic run rows copy that row's
  real `generation` and `workflow.sourceRoot`.
- **Synthetic, and labelled in each report:**
  - **Runs** in each state: completed, ended by the person, open, start not
    confirmed, prepared but unsent. Plus runs in another conversation and another
    home.
  - **Declared `returned_outputs`.**
  - **`reopened.runs`,** in the `record_supply` row shape.
  - **A restart,** either dropping the thread or keeping its ID.
  - **`preparationOrder` values:** these are synthetic. Only their shape follows
    #127 (`53c6853d` `runtime_session.rs`), and the array order is scrambled.

## Observed

| Head | Result |
|---|---|
| `9248a36e` (baseline) | **Results:** the Run guide's Results step listed only the declared outputs. It had no list of runs and no route to their evidence. |
| `d341f57a` | **Runs in this conversation:**<ul><li>Each run shows its plain reading, its declared outputs, and "the App hasn't checked them".</li><li>The prepared run and other conversations' runs are left out.</li><li>"Show the conversation" opens it, and the evidence link lands focused on the run's studio entry.</li></ul>**Recorded runs:** rows of the same name and origin are listed with no navigation.<br>**Defects:**<ul><li>The evidence landing switched the view to Make a workflow without saying so.</li><li>The "isn't loaded" line could never be reached, because the chat choice resets on any change of generation.</li></ul> |
| `9efa17a7` | **Evidence link:** it names "(in the workflow studio, under Make a workflow)".<br>**Unloaded runs:** after a restart that drops the thread, "Runs whose conversation isn't loaded" lists the sent runs with find-it-in-History and no Show. Runs from another home are left out. |
| `ca324f2b` | **Exact generation and home:** a run counts as current only on an exact match. After a restart that keeps the thread ID, runs from the earlier session move to the not-loaded group, with no Show.<br>**Recorded runs:** matched on name, origin and `source_root`/`sourceRoot`. Different or missing roots are left out, and each listed row shows its revision.<br>**Order (synthetic values):**<ul><li>**All known:** sorted highest first, and the unique highest run is current.</li><li>**A prepared run highest:** "Check your inputs, then start".</li><li>**One unknown:** listed under "These runs' order isn't known", with progress "can't tell which one is the latest" and Prepare held while a run is open.</li></ul> |
| `addba4ba` | **Unknown order, unresolved start:** "Next" reads "a start here has an unknown outcome… can't tell which run is latest". |
| `0b9a9068` | **Unknown order, after the checkbox:**<ul><li>**With a run open or sent:** "Next" reads "A run in this conversation is still open… before preparing another", and Prepare stays disabled.</li><li>**With nothing open:** "Describe… then prepare the run", and Prepare is enabled.</li></ul> |

## Not established

- Run order produced by a real host. In these runs the order values were
  synthetic; the merged producer matches the shape used, by source.
- The `e6e80559` `runReading` guard in a renderer.
- Any real Codex run, model, native window, or durable record read.
- Owner or human use, and J1 completion.

Evidence (task scratch `app-p2-trial-u5RbDlpZ`): `out-j2-125` … `out-j2-125g`
(reports and screenshots), plus the synthetic peer `mock-j2.js` and the driver
`j2drive.mjs`.
