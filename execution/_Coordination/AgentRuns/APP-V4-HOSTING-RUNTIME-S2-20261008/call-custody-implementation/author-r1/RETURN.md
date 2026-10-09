# Call-custody R1 repair freeze

Seven staged source files on the original f028 base remain uncommitted. Compared with the initial candidate, only hosting.rs and hosting_call_custody_tests.rs change. The reply invocation tracks whether it won the0→1 transition; only that invocation may perform error cleanup1→5. A rejected duplicate cannot cancel another invocation's preparation. No ordinary production behavior or scope expansion.

Manifest SHA25641801c8f97d9dcc37bf2f5f71a0d23eb7d6db207f3088ac42fa2c9e6bd1c03fe.
Patch SHA25660244e182132050ce11e560ae610eb5928a356c57094c9736704fc3d137005be.

Independent isolated red source/log are preserved here. Before the fix, the maintained full Host test reproduced the same cancellation: state5 instead of1, exit101, one failed test in full-host-red.log. The hook invokes the second attempt with the exact original handle before the first final cut; it does not recreate a capability. After the fix, the unchanged test verifies second rejection leaves state1, the outer attempt writes exactly one unavailable response, and canonical local-write settlement completes.

Final same-source filtered default18/18 and distribution-successor,custom-protocol18/18 pass. Logs default-final.log/features-final.log retain raw output. Commands/environment are identical to the initial packet except the additional maintained test. No process/signal fixture was introduced. Shared target released after both test processes exited.

Initial author command used a repository-relative append path from app/src-tauri, so no test was appended; its filter ran zero tests. That output is retained as unmatched-filter-before-test-append.log and is NOT red/green evidence. Correct-path append then produced the actual full-host red before repair. Initial staged index update was sandbox-denied; an authorized escalated git add succeeded, and the final official staged scan passed7files/3terms/0findings. Final diff check is clear.

Initial frozen manifest/source/logs remain at /private/tmp/cce-call-evidence; its limits, accepted brief/addendum, withdrawn source-premise correction, bounds accounting, actual-vs-simulated distinctions and S4 hold remain applicable. R1 contains copied accepted basis and source files and binds the previous manifest. No commit, export, B pin, PR, activation or qualification claim. Await independent exact-candidate backcheck.
