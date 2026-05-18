"""Per-chunk HTML controls (radio chips + flag note) and initial-state lookup.

Each reviewable chunk in a per-kind audit surface carries a control bar
(Unreviewed / ✓ Verified / ⚠ Flag) and a free-text flag-note textarea.
The equations surface additionally tracks a system-set Backcheck state
that the reviewer responds to (but does not pick) — see
`initial_status_for_key`'s `backcheck` parameter.

State persists in browser localStorage and exports to the per-kind
sidecar JSON.
"""
from __future__ import annotations

import html


def render_chunk_controls(key: str, status: str, note: str) -> str:
    """Toolbar inside a reviewable chunk: radio chips + flag note textarea.

    Hoisted verbatim from `render_source_html.py` so the legacy
    `<book>.html` and the new per-kind surfaces share one control widget.
    """
    return (
        f'<div class="ctrl">'
        f'<span class="badge"></span>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="unreviewed">Unreviewed</label>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="verified">✓ Verified</label>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="flagged">⚠ Flag</label>'
        f'<textarea class="flagnote" placeholder="Flag note...">{html.escape(note)}</textarea>'
        f'</div>'
    )


def initial_status_for_key(
    key: str,
    verified: dict,
    flagged: dict,
    backcheck: dict | None = None,
) -> tuple[str, str]:
    """Return (status, note) for a chunk key given the loaded sidecars.

    Resolution priority: verified > flagged > backcheck > unreviewed. The
    `backcheck` argument is optional; callers that don't track backcheck
    state (figures/tables/images) omit it and the 3-state behavior is
    preserved. Equations supplies it.
    """
    if key in verified:
        return "verified", ""
    if key in flagged:
        return "flagged", flagged[key].get("description", "") or flagged[key].get("note", "")
    if backcheck and key in backcheck:
        return "backcheck", ""
    return "unreviewed", ""
