from __future__ import annotations

import hashlib
import json
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any


SCHEMA = "chirality-software-workflow/v1"


def load_profile(path: Path) -> tuple[Path, dict[str, Any]]:
    profile_path = path.resolve()
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise ValueError(f"unsupported profile schema: {data.get('schema')!r}")
    project_root = (profile_path.parent / data.get("project_root", ".")).resolve()
    if not project_root.is_dir():
        raise ValueError(f"project_root does not exist: {project_root}")
    return project_root, data


def contained_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    candidate.relative_to(root.resolve())
    return candidate


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatchcase(path, pattern) for pattern in patterns)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
