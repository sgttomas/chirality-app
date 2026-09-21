# D-GOV-26 — Closeout of the four owner-gated items by adopted recommendation (delegated execution)

Status:       RULED
HumanRuling:  "Delegate to `opus-5` subagents the closeout of those four owner-gated issues by following your recommendations in each case." (owner, 2026-07-25; verbatim fence below)
PublicationSHA: ccee1654535375965d92f71e55dd66de0b3eed40 (this record's publication commit; backfilled in the same tranche per precedent)
EffectiveSHA: 31b8dc94acca50dbaf9a518a23dad8583c8c6c62 (merge of PR #351 into `main`; backfilled by the ROOT-INIT-CLOSE-20260725 tranche per precedent)
Date:         2026-07-25
FramedBy:     Agent-drafted (Agent 0, `HELP_HUMAN` posture); the four issues and recommendations were surfaced in the Receipt-49 closeout report, in-session
AcceptedBasis: `main@4aaa66483` (post-PR-#350)
DecisionKey:  `owner_gated_closeout`
RecordConvention: supersede-never-edit; approval vehicle stated below (K-AUTH-2)
Run record:   `execution/_Coordination/AgentRuns/ROOT-OGC-20260725/`

## Recorded ruling

<!-- BEGIN OWNER RULING VERBATIM -->
Delegate to `opus-5` subagents the closeout of those four owner-gated issues by following your recommendations in each case.
<!-- END OWNER RULING VERBATIM -->

**Vehicle (K-AUTH-2).** The ruling adopts the four recommendations below as
dispositions and delegates their exact prose to dispatched `opus-5`
subagents under sealed briefs. No exact candidate SHA was designated;
approval binds at the merge SHA of the human-gated PR carrying this tranche
(the EffectiveSHA above, backfilled on merge). The owner reviews the exact
prose at that gate; any owner correction supersedes.

## The four issues and the adopted recommendations (verbatim from the surfaced report)

1. **`_Archive/` tracking** — "recommend accepting the status quo (dirs
   exist locally, `.gitignore` policy stands) and adding a one-line SPEC
   §1.1 note that `_Archive/` subfolders are local working state, not
   tracked content." → Executed by S1 (`docs/SPEC.md` §1.1).
2. **Instruction-surface enumeration** — "recommend adding
   `.github/workflows/` to SPEC §0.2.2 (the guards already treat it as
   protected) and adding `CLAUDE.md` to the guarded set (it's a live
   instruction pointer file)." → Executed by S1. **Section-label
   correction, recorded at fan-in before publication:** the recommendation
   (quoted verbatim above) said "§0.2.2", but the instruction-surface
   enumeration lives at `docs/SPEC.md` §0.2.1 (line 44); §0.2.2 carries
   only the narrower working-root write-prohibition list. The substance
   was applied where the enumeration actually is (§0.2.1), the guard
   docstrings' citations were corrected likewise, and §0.2.2's
   prohibition list was deliberately not expanded. `CLAUDE.md` joined the
   G2/G3/G4 instruction-surface set with regression tests; the
   `harness-premerge` CI trigger was aligned at fan-in so `CLAUDE.md`
   changes exercise it. From this tranche's effect onward, changes to
   `CLAUDE.md` and `.github/workflows/` are M2 instruction-surface
   tranches by doctrine, not only by guard behavior.
3. **K-WRITE-2 gloss debt** (routed at D-GOV-21 packet §5.1) — the gloss
   "confines a task's effects to its working root" overstates the
   invariant's mechanical reach in a monorepo; recommendation was to stage
   the amendment. → Executed by S2 (`docs/CONTRACT.md`, gloss only; the
   invariant sentence remains byte-identical).
4. **Export-staging regeneration** — "recommend keeping DEFERRED until the
   public export is next actually needed; regeneration is deterministic
   whenever run." → Settled as a **standing disposition** (no longer
   carried as open debt); S3 supplies a read-only export-boundary audit
   evidencing that the deferral is safe
   (`execution/_Coordination/AgentRuns/ROOT-OGC-20260725/evidence/EXPORT_BOUNDARY_AUDIT.md`).
   Regeneration, when eventually needed, is its own act at its own basis.

## Downstream coordination (M6)

`projects/chirality-app-dev` pins `docs/SPEC.md` and `docs/CONTRACT.md` by
sha256 in its authority corpus — a routed change notice ships in this
tranche to its coordination surface. The chirality domain pack pins
neither (survey at the AcceptedBasis). The tranche manifest records the
gate and disposition.
