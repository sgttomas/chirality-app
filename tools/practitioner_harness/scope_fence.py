#!/usr/bin/env python3
"""Fence path matching (Phase 4) — brief `write_scope` / `prohibited_paths`
glob entries compiled to anchored regexes over POSIX repo-relative paths.

Grammar (the whole pattern must match the whole path — anchored full match):
- `**` as a whole segment matches across segments: a trailing `/**` means
  STRICTLY UNDER the directory (`a/**` matches `a/x` and `a/x/y`, never `a`
  itself); a leading `**/` or interior `/**/` matches zero or more whole
  segments; a bare `**` matches any path.
- `*` matches within one segment (`[^/]*`); `?` exactly one non-separator
  character. Neither treats dotfiles specially — `docs/*` matches
  `docs/.hidden` (the fence text is the whole rule; no hidden-file carve-out
  is invented, K-INVENT-1).
- Matching is CASE-SENSITIVE: the fence is what the human adopted,
  case-exact (D-GOV-04) — a case-variant path does NOT match.
- Deny wins over allow: a path matching any `prohibited_paths` entry is
  judged prohibited even when it also matches `write_scope`.
- A trailing `/` on a pattern is normalized to `/**` (a directory entry
  fences its subtree; changed paths from git are files, which a bare
  directory string could never equal).

Pure matching only — no filesystem access, no git, no findings. The judgment
tokens below are data values consumed by `cmd_scope_check` / `cmd_closeout`.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache

JUDGMENT_PROHIBITED = "prohibited"
JUDGMENT_IN_WRITE_SCOPE = "in_write_scope"
JUDGMENT_OUTSIDE_WRITE_SCOPE = "outside_write_scope"


@dataclass
class PathJudgment:
    """One path judged against a fence. `matched_pattern` is the fence entry
    that decided the judgment ("" when nothing matched)."""

    path: str
    judgment: str
    matched_pattern: str = ""


def _segment_regex(segment: str) -> str:
    """One non-`**` pattern segment -> regex (star runs stay in-segment)."""
    out: list[str] = []
    i = 0
    while i < len(segment):
        ch = segment[i]
        if ch == "*":
            # Collapse a star run; a '**' embedded WITHIN a segment (e.g.
            # 'a**b') is not a whole-segment '**' and stays within-segment.
            while i + 1 < len(segment) and segment[i + 1] == "*":
                i += 1
            out.append("[^/]*")
        elif ch == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(ch))
        i += 1
    return "".join(out)


@lru_cache(maxsize=None)
def fence_pattern_regex(pattern: str) -> re.Pattern[str]:
    """Compile one fence glob entry to its anchored, case-sensitive regex."""
    normalized = pattern.strip()
    if normalized.endswith("/"):
        normalized = normalized.rstrip("/") + "/**"
    segments = normalized.split("/") if normalized else []
    parts: list[str] = []
    for idx, seg in enumerate(segments):
        last = idx == len(segments) - 1
        if seg == "**":
            if last:
                # trailing '/**' (or bare '**'): one-or-more of anything —
                # strictly under the prefix already emitted.
                parts.append(".+")
            else:
                parts.append("(?:[^/]+/)*")  # zero or more whole segments
            continue
        parts.append(_segment_regex(seg) + ("" if last else "/"))
    return re.compile(r"\A" + "".join(parts) + r"\Z")


def pattern_matches(pattern: str, path: str) -> bool:
    return fence_pattern_regex(pattern).match(path) is not None


def match_any(path: str, patterns: Iterable[str]) -> str | None:
    """The first fence entry matching `path`, else None."""
    for pattern in patterns:
        if pattern_matches(pattern, path):
            return pattern
    return None


def judge_path(
    path: str, write_scope: Iterable[str], prohibited_paths: Iterable[str],
) -> PathJudgment:
    """Judge one POSIX repo-relative path against a fence. Deny (prohibited)
    wins over allow (write_scope); anything matching neither is outside."""
    hit = match_any(path, prohibited_paths)
    if hit is not None:
        return PathJudgment(path, JUDGMENT_PROHIBITED, hit)
    hit = match_any(path, write_scope)
    if hit is not None:
        return PathJudgment(path, JUDGMENT_IN_WRITE_SCOPE, hit)
    return PathJudgment(path, JUDGMENT_OUTSIDE_WRITE_SCOPE)
