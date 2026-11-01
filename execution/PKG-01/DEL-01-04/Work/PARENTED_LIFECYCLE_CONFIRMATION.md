# Original-window lifecycle questions

The native qualification failure exposed a product presentation mismatch:
parentless macOS confirmations selected CFUserNotificationDisplayAlert, while
the owned-window route required an App-owned modal. Stop/Restart now pass their
actual IPC-invoking window; Quit retains the configured main window. Checked
borrowed handles prevent the dialog plugin's silent parentless fallback.
Question, default-safe choice, refusal, lifecycle and settlement meanings stay
unchanged. Missing parent or missing result does not authorize an act.

The implementation, focused test standing, original failed evidence and bounded
recovery prerequisite are recorded in
[the qualification account](../../../PKG-09/DEL-09-02/Work/PARENTED_LIFECYCLE_CONFIRMATION.md).
This supplies the DEL-01-04 native interaction input; it does not establish the
joined DEL-09-02 native journey or change either deliverable's ScopeOfWork or
needs. Other confirmation families, supplier/account behavior and SEAL-C stay
outside this change. The historical retained candidate is unchanged.

The separate [inactive owned-sheet recovery backend](../../../PKG-09/DEL-09-02/Work/OWNED_SHEET_RECOVERY_BACKEND.md)
retains the exact App-created NSAlert lifetime for future bounded cancellation.
It does not activate a question timeout or change human reading time. Lifetime
policy, controller wiring, independent native-boundary review and real timing
remain explicit prerequisites.
