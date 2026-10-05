# Independent shared App custody mechanical review — 2026-10-05

**NOT READY for mechanical fan-in: ARC-1 is one major blocking captured-queue retirement defect.** Physical REC namespace guard remains separately unfinished/admitted work and is not counted as a repaired mechanical warrant or new finding here. No broad factory/native/home qualification follows.

TASK `/root/group_a_execution/hosting_contract_review`, parent `/root/group_a_execution`; no delegation. Software-code-review applied. Only this report written. Read immutable mechanical code/record against prior phase1 and REC source. Parent granted one bounded original-source retirement repro lane; it was released immediately after actual result, before report. No repository product/Design/Git/auth/native credential/model/network operation or66-suite rerun. Own-code cat processes and private scratch metadata only; owned roots and scratch removed.

| Exact immutable mechanical source | SHA-256 |
| --- | --- |
| hosting.rs | `7f2bda33aa129567084354c22e0cb9bef9f89a3890e4f6cede17002a6d0ec0e3` |
| recovery.rs | `bd67449037ca0dc0763fd731e90e8bdac8b8f85c4baf6f539655d93c51fba3e5` |
| auth_rpc.rs unchanged phase1 | `566b52ab2d2eedbc2f98835c07cd3369a2f9046f33d7cead063bbe9ddc45734f` |
| changes/I1-SHARED-APP-CUSTODY.md | `585f4bedf9e1df26a30e51897dd4cfb53818949bfdd9682ef6d2ea33d61d076c` |

All independently hashed from `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-i1-app-custody-mechanical-l_9pu1yi` and original record. Moving namespace/control implementation is excluded. Root/TASK/project/skill/REC/phase1 source origins retained; no other role activated.

## ARC-1 — Weak source registry loses unflushed pointer facts on retirement

**Major, blocking.** AppRuntimeCustody.sources is Vec<Weak<Inner>> (hosting.rs:224); pending_recovery exists only inside each Inner. `record_app_session_end` filters Weak::upgrade and drains surviving sources, without preserving/reporting disappeared queues. A busy shared writer causes actual listed/closed observations to remain pending as designed. After stopped old Host/reader release their last Inner Arc, its weak registry entry no longer upgrades and all unflushed captured rows disappear. Recreating the same home keeps the counter but cannot recover those rows. App-session end can append confirmed while silently skipping them. The original paused-writer positive keeps old Host alive, so it misses this lifetime boundary.

Actual independent original-source reproduction:

1. Configure real original ledger/Host, start owned env-cleared cat pipe via actual post-spawn counter allocator with synthetic ready/generation fields, adopt actual private AppRuntimeCustody.
2. Hold its actual shared writer. on_line receives synthetic fileChange/requestApproval RPC1; actual scoped Stop/EOF closes source. Capture two pending pointer observations (listed and closed) while flush is busy.
3. Positive keeps old Host alive; negative drops it and waits until weak.strong_count==0. Release writer, create another actual Host from same custody, allocate same home (counter2), flush, Stop and record App-session end.
4. Compare exact captured rows with actual sole-ledger snapshot, after all owned cat groups stopped/reaped and data roots removed.

Actual compile0/program **exit101**:

```text
retired=false captured=2 missing=0 end_write="confirmed" old_inner_alive=true
retired=true  captured=2 missing=2 end_write="confirmed" old_inner_alive=false
```

The independent program copies immutable7f Host/bd67 Recovery/auth566 into owned scratch and appends a private fixture, exercising their actual adoption/allocator/on_line/Stop/drain/end functions rather than a fake JSON capability/queue predicate. Contextual compile accommodations: absolute unchanged resource includes/package-version value, existing compiled support modules, and an unused attachment-dispatch lock call adapted for cross-crate private visibility. No exercised ARC/queue/ledger/end function changed. Initial harness setup failed to locate unhashed app rlib; next compile needed package-version/private-lock context; corrected harness retained identical retirement oracle. Those are setup failures, not candidate fixes or whole-suite results. Final scratch/owned data cleanup completed before the expected failing assertion; no stock/native auth process ran.

Repair: put immutable captured pointer queue ownership in genuine App lifetime or explicitly transfer/retain it on source retirement, without keeping native transcript/payload merely to protect these metadata rows. Stopped/recreated/dropped source cannot silently discard pending listed/closed/ack facts; drain/session-end must expose actual unavailable/undrained facts if persistence fails. No caller-side invisible “keep every Host forever” assumption or skipped Weak upgrade can prove completion. Add actual busy-writer old-source drop/reader-release/same-home recreation negative plus kept-source and persistence-failure controls. Preserve original source/full namespace/order/dedup/ack/one append/no retry semantics and no new ledger/store/kind/cache. Same-reviewer frozen successor backcheck required.

## Other mechanical assessment and original history

Actual App adoption caches one private Rust capability and checks existing protected session/home/counter against generation instead of reconstructing from JSON. new_with_app_custody shares the same ledger/writer/counters/hot contexts, opens no second ledger/session and refuses reconfiguration after adoption including writer wait. Per-home allocation occurs after actual spawn, retains same-home counter across recreated Hosts and distinguishes equal RPC/thread labels in distinct full generations. Context lookup refreshes actual shared ledger outside Inner; durable/hot conflicts and historical P/currentQ remain separated. No global capture chronology follows from serialized interleaving.

Writer/drain lock pattern snapshots immutable pending facts, performs ledger IO outside Inner, then removes actually appended prefix and retains failed remainder. No inspected inverse state/ledger mutex order identified. App end is metadata only, one attempted existing session_ended record, idempotent returned observation; it does not stop native children/turns or prove approval. ARC-1 limits its ability to retain source queues across retirement. Initialization-error versus append/projection-error observations are separate; ledger unavailable remains visible and native/reply/Stop paths independent, not memory-only durable fallback.

Source-bound transport/Stop/privacy/credential transient release/CR7 named env removal remain retained phase1 predicates. CODEX_ACCESS_TOKEN removal uses literal name and synthetic env utility fixture, no actual env credential value read. Raw params original Value drop after serialization is a lifetime correction, not erasure proof.

Author5 mechanics/66 Host/10 recovery/6 startup passes remain distinct from this new negative. Original new paused test expected incorrect RQ05 for unwritten closure; source was correctly RQ04, corrected new oracle plus actual written decline/noack RQ05 control preserved semantics. Separate real initialization-versus-append error-field regression101 was fixed with distinct field and unchanged startup oracle. Neither old pass nor these repairs establish retirement preservation. Source record truthfully remains not physical-namespace ready pending actual8f guard.

Return ARC-1 only to original owner, retain successful mechanical predicates/old test histories and physical namespace separation. The admitted REC namespace input/preflight/use guard must receive its own frozen code review; this original source is not full factory READY. Real home/bootstrap/credential/UI/provider/native access and actor/product qualification remain open; no reserved human gate or schema/store expansion is introduced by retaining actual pointer facts.
