# Temporary source freeze — execution held

Plan 2d6c6bf3eaee7f6e05a9b893e0afaa41f27859a3b3d1db8dac4af4c436f3ef7f; parent technical release permits source preparation only until independent exact-source review. Basis bf795b99d1f7093178b41ca93e638450eca2d8e0. Plan backcheck read: /private/tmp/CHILD_CUSTODY_EXAMINATION_PLAN_REVIEW.md.

No compilation, syntax compilation, instrument execution or process probe has occurred. The only created sources are examine.c and driver.py in this fresh owned directory. SOURCE_FREEZE.json binds them and the exact compilation argv. Later commands require its SHA-256 explicitly; compile and run are separate invocations and must remain held until review.

Mandatory refinements included: each timed native process explicitly unblocks SIGALRM; consumed-child state is irreversible and later failed assertions cannot trigger cleanup waits; isolated helpers ignore SIGPIPE so release EPIPE is logged and release is closed; fork failure never reaches wait; SIGCHLD default is set only inside isolated helpers/child; Python uses explicit Popen.wait timeouts without context-manager cleanup, kill, terminate or subprocess.run timeout. Any native failure stops before the model; timeout has no subsequent helper. Alarms are safety ceilings, not hard kernel deadlines or cleanup proof.

Native mode creates exactly one invented direct child. Child uses self setpgid, private pipes and _exit; no descendants, exec or OS signal calls. Only two getpgid observations before deliberate reap; no post-reap lookup. Model mode creates two pthreads per schedule, at most two concurrently, no child process. All signal/reuse entries are inert trace records. The deliberately broken control must produce one detected wrong-identity inert signal; it does not run a real signal.

Expected future commands after source review: installed Python driver.py compile --freeze-sha256 <reviewed hash>, followed only after successful compile by driver.py run --freeze-sha256 <same hash>. No command is scheduled automatically by source creation. Compiler failure is retained, and source repair requires renewed freeze/review. No shared Cargo target or repository tracked files are touched.
