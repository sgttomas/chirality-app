"""Sidecar JSON I/O for source-audit surfaces.

Each per-kind audit surface persists reviewer state in two sidecars under
the source's `audit/` directory:

  - `<role>_verified.json` : map of asset_id -> {verified_at, ...}
  - `<role>_flagged.json`  : map of asset_id -> {description, flagged_at, ...}

Where `<role>` is the asset kind (`figures`, `tables`, `images`). The
loader walks both the canonical path and timestamped browser-exported
fallbacks so user-dropped exports under `audit/` (or `audit/<kind>/working/`)
re-load on the next render.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def content_hash(text: str) -> str:
    """12-char sha1 of stripped text — stable, content-addressed key.

    Identical to `sha1_12()` in `render_source_html.py` and `eqhash()` in
    `audit_equations.py`; consolidated here as the canonical helper.
    """
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:12]


def load_sidecar(path: Path) -> dict:
    """Read a JSON sidecar; return {} on missing/invalid/empty."""
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data:
                return data
        except Exception:
            pass
    return {}


def load_sidecar_with_fallback(audit_dir: Path, role: str) -> dict:
    """Load a sidecar by role, with fallback through:

      1. canonical flat: `<audit_dir>/<role>.json`
      2. canonical nested: `<audit_dir>/<kind>/working/<role>.json` for any
         direct subdir of audit_dir that contains a `working/` folder
      3. exported flat: latest `<audit_dir>/*_<role>_*.json`
      4. exported nested: latest `<audit_dir>/<kind>/working/*_<role>_*.json`

    Returns the first non-empty match. Empty dict if none.

    Roles in this module are `<kind>_verified` / `<kind>_flagged` (e.g.
    `figures_verified`). The fallback resolver also reads legacy bare
    roles (`verified`, `flagged`, `backcheck`) from equation-audit's
    nested layout so prior equation review carries forward.
    """
    search_dirs: list[Path] = [audit_dir]
    if audit_dir.is_dir():
        for sub in sorted(audit_dir.iterdir()):
            working = sub / "working"
            if working.is_dir():
                search_dirs.append(working)

    for d in search_dirs:
        data = load_sidecar(d / f"{role}.json")
        if data:
            return data

    for d in search_dirs:
        candidates = sorted(d.glob(f"*_{role}_*.json"))
        if candidates:
            return load_sidecar(candidates[-1])

    return {}
