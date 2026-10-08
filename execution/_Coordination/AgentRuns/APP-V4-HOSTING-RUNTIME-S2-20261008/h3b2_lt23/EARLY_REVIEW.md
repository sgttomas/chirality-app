# Early independent code review finding

Independent TASK runtime_review traced the WIP implementation before source freeze. Terminal worker ownership appeared limited to Store/prior/event/token/Weak Inner/controller and Store leases ended before completion, but LT09 completion checked only attempt/H5/event sequence. App closing could occur before Exit Stop reserved LT23, allowing paused LT09 to install during that interval. This contradicted the released closing fence.

Manager routed same controller→Inner closing protection and a deterministic paused-LT09→closing-before-terminal-capture→resume negative. Author reports repair and new regression; runtime proof and final exact-head review remain pending. This finding is retained even if later tests pass. No accepted meaning was narrowed.

The first focused compile additionally found a maintained namespace test constructor missing the new shared controller field. Author repaired by cloning the original controller and retained /private/tmp/lt23-first-default.log. No runtime success follows from this compile repair.
