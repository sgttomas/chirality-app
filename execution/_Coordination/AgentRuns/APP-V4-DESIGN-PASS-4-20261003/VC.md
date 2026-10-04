# VC — Codex version-advance check 0.158.0 → 0.160.0 (return)

Node VC (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04 03:30–04:05 UTC. Authority: R19-5, HOSTING-v0.9 §9.5, owner direction 4 C and the download approval in `OWNER_DECISIONS.md`. No git writes. The only network use was the one approved download.

## Files written

| File | sha256 |
|---|---|
| `PKG-01_…/DEL-01-01_…/Design/VERSION_ADVANCE_0.160.0.md` (the record; redacted as OBS-2/OBS-3) | `30f4eae2cfbf20a894239a89bd769a0c31acd78c11b6383652a327aa181e6025` |
| `PKG-01_…/DEL-01-01_…/Design/prototype/version_advance/va_harness.py` (run-time wrapper; obs2/obs3 harnesses imported unchanged) | `fbe61c7272ca452cf75ceab930adb01fb2b162a394a808bf7b34b7b4f0fb98e8` |
| `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/VC.md` (this return) | — |
| Scratch: `<session scratchpad>/codex-0.160.0/` (tarball, extracted package, generated output, 0.158.0 regeneration, diffs, observation homes and raw logs, statement-inventory scripts) | not committed |

No existing Design file was edited.

## Summary

1. **Download verified.** `codex-0.160.0-darwin-arm64.tgz` (134,311,083 B) was checked **before extraction**: sha1 `f78898f0…dc9c` and integrity `sha512-aefV6cqZ…gA48vZmDgrQ==` both equal the registry values. Signed by OpenAI OpCo (2DC432GLL2), valid. `bin/codex` sha256 `112fae7a…1b4b`. Nothing was installed.
2. **Generation.** This is the 0.158.0 method: both generators, both variants, twice each, deterministic. There are two stated deviations (vendor binary run directly; home holding `plugins = false`). The same method run with the 0.158.0 binary reproduced the committed `MANIFEST.sha256` body exactly. Results: TS 734/875 files (+2 each), JSON Schema 314/440; new combined manifest `ef47ec4e…3f37`.
3. **Protocol differences: four, all additive or documentation-only.** Every method, notification and server request is the same, and so are the stable/experimental split, the TS-only five, deprecations and the server's 170 accepted methods.
   - Δ1 `thread/items/list` `cursor` may also be an item anchor `{type:"item", itemId}`.
   - Δ2 `mcpServerStatus/list` gains optional `serverName`.
   - Δ3 `Turn.error` doc: "failed or interrupted" (was "only failed").
   - Δ4 `CodexErrorInfo` gains `tooManyDenials`.

   Non-protocol differences: three new under-development feature flags, all off by default (`instant_interrupt`, two `guardian_*`); bundled system skill `plugin-creator` removed. Base instructions, mode texts, request shape and headers are identical. All 0.158.0 and 0.160.0 recorded frames validate against both schemas.
4. **Observation reruns** (LM Studio 0.4.16+2, `qwen/qwen3.5-9b`, parallel 1, 28 predictions, 38 sessions, scratch homes, plugins off, no non-loopback socket, no S-2, every process stopped):
   - **Same:** O-1, O-2 (stdin and kill), O-3, O-5, O-6, O-7 (plugins-off variants), O-8, W-1, W-2, W-2b, W-3, W-4, the W-5 mechanism, O-5b mechanism, W-6b, and the handshake/exit facts.
   - **Changed:** W-6. A fork's first turn **no longer gets a fresh `<environment_context>`**; everything else is the same, including that `developerInstructions` on a fork is ignored. The skills block lacks `plugin-creator`.
   - **Model adherence varied** (not a version fact): W-1 3/4, W-5 3/6, O-5b missed. The inputs are structurally identical to 0.158.0's.
   - **Not run:** the O-7 baseline (plugins on), because it needs network the brief does not allow. O-4 was not in the required list.
5. **Statements affected.** There are 962 statement units in 42 Design files: changed 22, not re-checked 43, partly not re-checked 174, unchanged+ 18, unchanged 523, pin or record only 182. The record's §7 lists every unit by file and line.
   - The changed ones are the identity values: HOSTING L1107, L1108, L1113, L1143, L216, L2199; NPTD L459; COMMITTED_STATE; and the dated value lines in the PIN_SPIKE and OBS records.
   - OBS_3 L191 (the fork's fresh environment context).
   - NIR L396 (`Turn.error` "only when failed").
6. **Design decisions: none change.** Items to carry into the design nodes:
   - NIR L396 wording (Δ3), with a defence for an interrupted turn that carries an error.
   - HOSTING §7.1 identity values if the pin advances.
   - An optional item-anchor read for WR SC-3 and RECOVERY R-4 (Δ1).
   - An optional `serverName` for ADAPTER (Δ2).

   The W-5 variance supports the existing choice not to rely on `thread/settings/update`.

## Deviations needing HELP_HUMAN's judgment

- **S-9:** right after the model load, before any Codex process, three 1-s samples read pressure 4, then 2. The run went ahead as OBS-2 did in its D-1. The level never read 4 inside a scenario.
- **Model inputs and the user name:** the inputs carried scratch paths that contain the user name, because the brief puts the scratch folder under the session scratchpad. They went to the loopback provider only.
- **Non-canonical path rerun:** the canonical-path test needed `capture` rerun through the `/tmp` spelling of the same folder (record D-3).
