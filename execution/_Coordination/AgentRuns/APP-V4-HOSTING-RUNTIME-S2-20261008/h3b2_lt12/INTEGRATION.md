# LT12 source integration

Receiving main 3d73db745edd3378e0bb254a1b263215ef0861e9 includes LT23 PR #1152 and terminal/two-cohort PR #1153. The latter merge and CI reporting/rerun evidence are retained in ../h3b2_terminal_export/postmerge. No prior evidence is replaced.

Five product/test/support files are copied byte-exact from author manifest f9b5104cce41e3ccf843597d5422eb7ff54b97f561552ebd86283f938bf4f5c1. Independent code READY c3d3b6264a050f120d9c12f864cef4ede68367b26aab64fa9d32f5ab0e158e4e covers actual lock lifetimes, original LT09 capability, EOF/Stop sequence fencing and both-feature 15-test runs. Author 69/2 and 45/1 suites overlap. Initial fixture failures and repairs remain raw in author evidence.

This is bounded actual LT12 same-H5 publication after installed LT09, with original LT09 also preserved for LT23. Existing invalid LT19 Stop-after-exit tuple and null fallback facts remain unresolved; there is no whole-trace validation. No REC/lib/setup change, new production authority, S3, SEAL-2, hydration, native/package or qualification claim.

Committed-head review, fresh committed/recompiled unchanged-format LT09 and LT09+LT23 exchanges, and named B receiving adoption are required next. Old cohorts/pins remain historical and unchanged; current-source guards must not be weakened. Neither exchange claims an LT12 export.
