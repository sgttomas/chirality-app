# Child custody synthetic execution review

READY as bounded empirical/model evidence only. Production custody remains NOT READY. No rerun, build, signal or source edit was performed by this reviewer.

Reviewed packet: /private/tmp/child-custody-examination-can9q7. All19 OUTPUT_MANIFEST members independently rehashed successfully. Exact packet anchors:

| File | SHA256 |
|---|---|
| OUTPUT_MANIFEST.json | 2cc79f23b47013220b34d87c8fbfb29072c94bfc4af15f0abbd5ddc63133f191 |
| SOURCE_FREEZE.json | ec5d4793c93eadc4fe3176c84b7f98a4058281f6a27c1a9782930498944cd850 |
| examine | 4c222468006eb23d55baddd14553886fad1ff77cf2cd76e89a3aa1a84257c97a |
| RESULT.json | b3798f9ab16047fcb68bc7d8b8b6ce4f6a96c8b2e5818e0cd2fa38a1d4922f12 |
| native.stdout | 0aa01812b7872a2fd1aac0d418cfcd1d072b07736196bb3f668526a4c5f6803e |
| model.stdout | 07f3e0e430349d3ea5b383d5b9ee4e9994f120c8091d2c45a9f02195f8599819 |
| process-ledger.jsonl | dbfa77a49b97f417877b4a6c0976188a66e3b348f029b1a03a68b7b171803ca6 |

Frozen C/driver bytes remain identical to the independently reviewed instrument. Compiler receipt binds the approved argv, exact freeze and resulting executable, with exit0/no timeout and empty stderr. Driver ledger accounts for compiler94635, native helper94773 and model helper94785 with matching successful wait returns. Source-review note in the packet is the historical pre-execution freeze note, not a current claim that nothing ran.

## Actual observations

Native helper created exactly its one fixture94782 according to the reviewed single-fork source and raw ledger. The ready/release-held observation returned zero with si_pid0. Live getpgid returned94782. Release write succeeded. Two later WNOWAIT observations returned matching PID94782, CLD_EXITED(code1), status37. The deliberate waitpid consumed PID94782/status9472 (exit37); the sole follow-up query returned -1/ECHILD(errno10). No cleanup polling, timer termination or unresolved-disposition path occurred. Helper and driver successful exits are recorded. This accounts for the created fixture; no descendant census was performed or needed for this no-descendant source.

Material result: between the second terminal WNOWAIT observation and consuming wait, getpgid(94782) returned -1/ESRCH(errno3). Thus the optional lookup failed while exact child status remained waitable. Do not interpret this as group extinction, PGID reuse, all descendants ended, or proof that a zombie either does or does not reserve a group identifier. It provides no positive warrant for the proposed group-continuity argument. Repeated nonconsuming status observation and group lookup are separate facts.

Inert guarded schedule recorded reaper-busy, one correct-identity action and zero post-reap actions. Deliberately broken schedule recorded reap/reuse then one detected wrong-identity action. Both model results match the planned discrimination. No real process signal/reused-ID action occurred in reviewed source. The model does not prove Rust/App lock integration or OS custody.

C trace timestamps and Python driver timestamps have different monotonic origins on this platform; ordering is supported within each trace and by explicit spawn/wait/PID joins, not by subtracting the two clocks.

## Limits

Runtime metadata records Darwin25.6.0/xnu-12377.161.14 on arm64 and Python3.13.7. One observed run does not establish current supported API policy, equivalence to older pinned XNU, foreign-waiter exclusion, retained PGID continuity, final-reap policy, App retention or shutdown handling. All production blockers remain. This review covers raw execution/receipts and current manifest; a later authored final report is not yet included in that manifest and must preserve these interpretations. No native supplier/App or qualification follows.
