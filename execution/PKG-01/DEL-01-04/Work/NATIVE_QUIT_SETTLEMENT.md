# Native Quit settlement receiving note

This implementation note accompanies the unchanged pinned
`NATIVE_INTERACTION_RECEIVING.md`; it does not replace or re-pin that source.

For ordinary native Quit, the 2026-10-30 repair receives actual owned-process
settlement from DEL-01-02 before allowing App exit. Failure or unknown cleanup
shows a native **Quit Chirality — still running** message with the supplied
limit; the App remains available and Host diagnostics retain source/custody
facts. A `stopped` rendering alone is not proof of cleanup. Starting a supplier
or adding a key home while Quit is under way is refused; a pending key setup
causes Quit to remain unstarted with a retry message. These are operational
outcomes, not new human-act or release criteria. System termination retains
DEL-01-02's separate observation limits. ScopeOfWork and dependency conditions
are unchanged.
