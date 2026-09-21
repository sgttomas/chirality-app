#!/usr/bin/env python3
"""Session-scoped fixture-repo template cache for the harness test suite.

Building a fixture repo costs directory fan-out and (for git-backed repos)
several `git` subprocess calls, and the suite builds hundreds of them. The
conftest session fixture installs a template root here; builders then
construct each distinct repo shape once per session and hand every test its
own `shutil.copytree` copy. Tests mutate their repos, so the template itself
is never handed out.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

_root: Path | None = None
_templates: dict[tuple, Path] = {}


def set_root(root: Path | None) -> None:
    """Install (or clear) the session template root; clears the cache."""
    global _root
    _root = root
    _templates.clear()


def materialize(key: tuple, build: Callable[[Path], None], dest: Path) -> Path:
    """Copy the template repo for `key` to `dest`, building it on first use.

    Outside a pytest session (no root installed — e.g. a test module run as
    a plain script) it builds directly at `dest`, preserving the builders'
    original uncached behaviour.
    """
    if _root is None:
        build(dest)
        return dest
    template = _templates.get(key)
    if template is None:
        template = _root / f"template-{len(_templates):04d}" / "repo"
        build(template)
        _templates[key] = template
    shutil.copytree(template, dest)
    return dest
