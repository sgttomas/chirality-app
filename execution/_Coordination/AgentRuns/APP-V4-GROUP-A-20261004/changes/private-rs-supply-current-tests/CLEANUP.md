# Historical-control retirement from permanent RS tests

2026-10-05. TASK `/root/group_a_execution_astra/rs_supply_design`, under parent
`/root/group_a_execution_astra`; no descendants. Parent explicitly authorized
only retirement of the historical original-receiver plumbing from permanent
tests while preserving its evidence and every current correctness assertion.
Selected `.agents/skills/chirality-change/SKILL.md`: “Separate maintained source
and test fixtures from run evidence” and preserve useful regressions while
keeping one-time history out of the permanent test dependency graph.

The predecessor remains untouched at `/private/tmp/rs-supply-endnotice-repair/app`
and in `../private-rs-supply-endnotice-repair/`. Its frozen executable, original
failure and complete logs remain valid historical evidence for that candidate.
The exact original receiver bytes now also have a durable evidence home at
`../../evidence/WR-RS-PUBLICATION/original_receiver.rs`, SHA-256
`086e9f29677ffba27073a54bf3a27880dbc1de97f0fce33dd0dcc61ef00b4aae`.
`ORIGINAL_FAILURE_BINDING.json` beside it links the original source derivation,
exact failure, predecessor patch, executable and canonical existing logs. Logs
were referenced, not duplicated or edited. No historical evidence was deleted.

Successor private App: `/private/tmp/rs-supply-current-tests/app`.
The exact predecessor-to-successor comparison has only two paths:

- `src-tauri/src/record_supply_original_control.rs` is excluded from product/test
  source, retained in evidence instead.
- `src-tauri/src/record_supply_tests.rs` removes the original module inclusion,
  the two original-failure assertions and their historical comment, and renames
  the publisher regression to `actual_end_publisher_resolves_source_and_cold_reads`.

`current-tests-only.diff` is the narrow test delta. Every actual producer,
publisher, unchanged-body, end-content, original-source, complete RS validation,
cold-reader and negative current-correspondence assertion remains unchanged.
Both actual end-body field-absence assertions remain. No production source,
WR source/schema, policy pin, fixture or acceptance requirement changed. The
permanent suite has no include or path dependency on a dated run directory.

`implementation.patch` is the complete nine-path RS patch from exact b44;
`manifest.json` names the excluded path and source hashes. The joined manifest
binds the same frozen WR successor plus this RS test-only cleanup. Original
receiver code cannot enter maintained fan-in through this patch.

Rustfmt `--edition 2021 --check` on the successor test file returned exit 0.
The exact two-path predecessor comparison passed. No Cargo or execution rerun
was made: another owner holds the shared lane. The original independent
reviewer's narrow assertion-preservation backcheck and the two affected current
end-notice regressions remain pending lane release and manager grant. Prior
70-test results refer to the predecessor and are not relabelled as a successor
execution result. Live native completed-check construction remains absent.

## Granted affected execution

After the compatibility owner released the lane, Parent granted this TASK the
sole lane for no-run compilation and only the two affected tests.
`cargo test --offline --locked --lib --no-run` passed. A frozen copy of that
executable ran exactly:

- `records::supply::tests::actual_end_notice_resolves_original_source_and_preserves_end_content`: 1 passed.
- `records::supply::tests::actual_end_publisher_resolves_source_and_cold_reads`: 1 passed.

Both used the same explicit isolated Cargo home/shared target/offline/skip-
supplier environment as compilation. RS's nine files and WR's five files had
identical hashes before and after; the historical module remained absent.
`validation.json` binds exact commands, environment, source hashes, executable
and canonical `logs/` outputs. Frozen executable SHA-256:
`b89608d92752c44f55808d0c172b5fac3895372e67d86645cc437de2c3298bd6`.
No broader test suite ran. Previous 70-test results remain predecessor evidence
for unchanged production, rather than a falsely relabelled successor run.

The shared lane was released to Parent after these checks; the original
reviewer received the exact result and log hashes for the final preservation
backcheck. No production source changed during this assignment.
