# Recordings at Codex 0.169.0

These ST5 and NV04 files retain the two scripted, no-model captures from the
verified stock distribution. They are supplier observations, not an App
candidate or qualification. `test_recordings_0169.py` checks their identities,
every captured protocol frame against this pin's schema, request/reply joins,
and the scenario facts below. The source was `record_at_pin.py` and
`recording_provider.py` at `5d19a7c29aead4142e3fbb977613a38aae070bc0`.

ST5 contains 35 frames. A command approval is requested; the scripted client
freezes its owned process group, writes an acceptance labelled as a scripted
capture rather than a person's act, and kills the frozen group. No resolution
or completion appears in the captured first generation. The second generation
reads interrupted history and resumes it. No new server request appears through
the captured resume reply. None of this establishes a successful command or
absence of messages beyond the captured interval.

NV04 contains 65 frames. The parent completes before its scripted child. Both
have their own completion and history; the parent's spawn item appears in each
captured history form before and after restart. This one ordering does not
establish ordering for other runs or completion of descendants from completion
of their parent.

Both captures supply `features.shell_snapshot = false` and
`allow_login_shell = false`, alongside plugins and analytics off. Their fresh
scratch homes have no sign-in or credentials. The provider listens on loopback,
forwards nothing and supplies fixed scripted responses. Contacts are not
observed; proxy variables are not isolation. Supplied settings alone are not
read-back evidence. Frames are redacted, not a claim of original wire bytes.

The retained 0.167.0 captures did **not** supply the two shell settings. ST5's
command is consequently captured with `/bin/zsh -lc` there and `/bin/zsh -c`
here. This is a capture-configuration difference, not an effect attributed to
the supplier pin. These recordings do not compare execution through a login
shell across pins. The Level lane's separately identified rows address both
configurations; these files establish none of that lane's results.

The cross-pin comparison keeps the same scenario and method groups separate
from value and shape differences. New nullable fields observed here include
`attachedToThreadId`, `contentTokenCount` and `moderation`. The historical
recordings, including their harness and ordering limits, remain unchanged.
