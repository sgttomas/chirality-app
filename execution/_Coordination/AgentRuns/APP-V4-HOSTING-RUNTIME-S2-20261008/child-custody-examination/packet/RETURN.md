# Released synthetic examination return

Completed once at source basis `bf795b99d1f7093178b41ca93e638450eca2d8e0`. The exact frozen instrument compiled successfully on the first attempt and both released modes passed. No source repair, rerun, group signal, supplier/App execution, descendant fixture, process enumeration or product change occurred. Shared Cargo target was never used and remains released.

Review basis: plan SHA256 `2d6c6bf3eaee7f6e05a9b893e0afaa41f27859a3b3d1db8dac4af4c436f3ef7f`; instrument review `/private/tmp/CHILD_CUSTODY_INSTRUMENT_REVIEW.md` SHA256 `5b2b740d83b628b3059f74e6607b6948b1aeff90bac40f43f97459c340ad4dfc`. Source freeze unchanged: `ec5d4793c93eadc4fe3176c84b7f98a4058281f6a27c1a9782930498944cd850`.

| Check | Raw result |
|---|---|
| Live child held at release pipe | waitid returned0, zero si_pid |
| First terminal observation | waitid WNOWAIT returned0, child94782, CLD_EXITED(1), status37 |
| Repeated terminal observation | Same child/code/status, still nonconsuming |
| Owned child group lookup before exit | getpgid(94782) returned94782 |
| Owned child lookup after exit observation, before reap | getpgid(94782) returned-1, errno3 (ESRCH) |
| Deliberate consuming wait | waitpid returned94782; raw status9472, exit37 |
| Deliberate postconsume query | waitpid returned-1, errno10 (ECHILD) |
| Guarded inert signal-first schedule | Competing reaper busy; one action to identity1; zero wrong-identity actions |
| Inert reap-first with same invented number | Old owner refused; zero additional actions |
| Deliberately broken check-unlock-act control | One wrong-identity inert action detected after identity changed to2; discriminatory control passed |

The ESRCH observation is **not** evidence that the process group became extinct, that its ID was reused, or that a retained zombie cannot reserve an identifier. It shows only that this getpgid lookup did not return a group after the observed exit. It supplies no affirmative zombie→PGID custody proof. Passing WNOWAIT observations likewise do not establish current Apple support policy, foreign-waiter exclusion, descendant census, production lock correctness or successful Host cleanup. Older pinned Apple source remains xnu-12377.121.6, while this run recorded Darwin25.6.0 / xnu-12377.161.14. Production design remains conditional/held.

## Invocation and process accounting

Both driver invocations used `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`, first `driver.py compile --freeze-sha256 ec5d4793c93eadc4fe3176c84b7f98a4058281f6a27c1a9782930498944cd850`, then `driver.py run --freeze-sha256 ec5d4793c93eadc4fe3176c84b7f98a4058281f6a27c1a9782930498944cd850`, from this directory. Actual compiler/helper argv are preserved in `compile-receipt.json` and `process-ledger.jsonl`; driver argv/interpreter hash and kernel metadata are in the phase-start records. No shell timeout wrapper was used.

| Owned process | Observed disposition |
|---|---|
| Compiler94635 | Direct driver wait returned0; no timeout, stderr empty |
| Native helper94773 | Direct driver wait returned0; no timeout |
| Fixture94782, direct child of94773 | Released through private pipe; actual exact-child wait reaped exit37; no cleanup polling needed |
| Inert model helper94785 | Direct driver wait returned0; no timeout; its threads completed |

There are no unresolved fixture/helper children in the recorded experiment. The two short-lived driver processes returned0 to the command tool; their own PIDs were not recorded, so no invented PID is supplied. Compiler-internal process activity was not enumerated. This is the instrument's owned-process accounting, not a system census. All three stderr files are empty. Self alarms were armed but no timer termination was observed. No real signal syscall exists in the instrument; configured SIGALRM/SIGCHLD behavior and local SIGPIPE handling remain as reviewed.

Python and C monotonic timestamps have different displayed origins in these logs; do not subtract across those clock domains. Within each domain the order and elapsed values are preserved. Native helper log spans approximately12.9ms; model log approximately0.16ms. These are one-run observations, not bounds or product timing requirements.

## Exact hashes and preservation

* Executable: `4c222468006eb23d55baddd14553886fad1ff77cf2cd76e89a3aa1a84257c97a`.
* Native raw stdout: `0aa01812b7872a2fd1aac0d418cfcd1d072b07736196bb3f668526a4c5f6803e`.
* Model raw stdout: `07f3e0e430349d3ea5b383d5b9ee4e9994f120c8091d2c45a9f02195f8599819`.
* Process ledger: `dbfa77a49b97f417877b4a6c0976188a66e3b348f029b1a03a68b7b171803ca6`.
* RESULT.json: `b3798f9ab16047fcb68bc7d8b8b6ce4f6a96c8b2e5818e0cd2fa38a1d4922f12`.
* Driver's original output manifest: `2cc79f23b47013220b34d87c8fbfb29072c94bfc4af15f0abbd5ddc63133f191`.

Original logs/manifests are unchanged. `SOURCE_AFTER.json` records clean manager checkout at the identical basis, exact product file hashes, unchanged frozen instrument and verified original output manifest. The final packet manifest additionally includes this report and source-after check; it excludes itself. No failure logs were omitted: there was no compilation or execution failure. The intentionally broken inert trace is retained as the planned red control, not represented as repaired production behavior.
