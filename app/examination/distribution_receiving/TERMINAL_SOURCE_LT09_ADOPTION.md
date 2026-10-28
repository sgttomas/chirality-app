# B-S4-TERMINAL-SOURCE-LT09-v1

Fixed standalone LT09 source adoption at
`9af67409ed0e625fcd8e0e9a0c59975fccfcae71`, using the unchanged
`group-b-s1-reader-exchange.v1` contract and receiving algorithm. Parent selected
this separate active cohort after the new terminal test-module declaration
changed the pinned hosting_successor.rs bytes and correctly caused the previous
source guard to refuse. Merely adding the terminal consumer did not make the
old standalone CLI current.

Only receive.py's literal active pin selector/digest and predecessor-pin filename
change. pins.terminal-source-lt09-v1.json fixes the new source and fresh actual
LT09 exports, and binds the prior pins.lt23-source-v1.json bytes. All historical
pin files, fixture cohorts and evidence stay unchanged; no caller fallback,
source-guard suppression, test skipping or global pin mutation is introduced.
The full reader receipt and v1 shape/behavior are unchanged. Among previously
selected sources only hosting_successor.rs changed, by a cfg(test) terminal
exporter module declaration. New exports identify the actual source/test binary
separately from invented App candidate identity.

The parent settled this two-cohort route in the active task, through Group B
WORKING_ITEMS, after explicit impact accounting. That later direction supersedes
the initial instruction to preserve receive.py bytes, solely for these selector
changes and the new named cohort. Exact relay wording is preserved in the author
run. Host fresh v1 exports received independent READY before freezing this cohort.

Active fixtures live in group_b_distribution_receiving_terminal_source_fixtures.
Current standalone tests remain meaningful on the fresh actual exports and
explicitly refuse old source and terminal exchange shapes. This path still
receives LT09 only; terminal_evidence_received and terminal authority remain
false. Separate terminal receiver pins freeze the final receive.py bytes after
this adoption. No canonical rollout, native capability, S3, qualification,
package witness, owner gate or release is established.
