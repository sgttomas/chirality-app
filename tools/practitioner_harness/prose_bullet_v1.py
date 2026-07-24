#!/usr/bin/env python3
"""prose-bullet-v1 — versioned _STATUS.md parser plugin (ruled baseline material).

Grammar agrees with the strict list parser in
projects/chirality-app-dev/frontend/src/lib/lifecycle/status-parser.ts and
extends it with 8 ordered assumption-bearing prose rules. Rule 1 yields
caveat class PARSED; rules 2-9 yield PARSED_WITH_ASSUMPTIONS; no match yields
UNPARSEABLE. First match wins.

DELIBERATE v1 LIMITATIONS (do NOT extend; the 9-rule set is ruled baseline
material behind the recorded drift baseline — 92/154 as measured 2026-07-01,
0/154 after the 2026-07-02 class-wide K-CONFLICT-1 correction; the ruleset
stays frozen because it produced the ruled measurement):
- "preserved/retained/kept/verified as/updated to X" phrasings -> UNPARSEABLE.
- Evidence-lifecycle bullets ("Evidence promoted to COMMITTED ...") must never
  yield a deliverable state: COMMITTED is not in the lifecycle-state vocabulary,
  so such bullets are non-lifecycle assertions -> UNPARSEABLE.
- Disclaimers such as "No ISSUED ... claim was made" must NOT match; the 9
  rules do not match them (regression-tested).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

DIALECT = "prose-bullet-v1"

# Caveat classes
PARSED = "PARSED"
PARSED_WITH_ASSUMPTIONS = "PARSED_WITH_ASSUMPTIONS"
UNPARSEABLE = "UNPARSEABLE"

# State vocabulary, longest-first so alternation cannot truncate a match.
STATE_VOCAB: tuple[str, ...] = (
    "SEMANTIC_READY",
    "IN_PROGRESS",
    "INITIALIZED",
    "PREPARATION",
    "CHECKING",
    "COMPLETED",
    "COMPLETE",
    "BLOCKED",
    "ISSUED",
    "REVIEW",
    "CLOSED",
    "OPEN",
    "READY",
    "DONE",
)

_S = "|".join(STATE_VOCAB)

FIELD_RE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*?)\s*$", re.MULTILINE)
HISTORY_HEADING_RE = re.compile(r"^##\s+History\b.*$", re.MULTILINE)
HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
BULLET_RE = re.compile(r"^- (.*)$")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

# Rule 1 — strict (the TS parser list regex; hyphen OR em-dash separator,
# optional trailing [notes]).
RULE_1_STRICT = re.compile(
    r"^\d{4}-\d{2}-\d{2}\s*(?:-|—)\s*State set to\s+(" + _S + r")\s+\(([^)]*)\)(?:\s+\[.*\])?\s*$"
)

# Rules 2-9 — ordered, first match wins; all yield PARSED_WITH_ASSUMPTIONS.
RULES_2_9: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("verb_moved", re.compile(
        r"\bState (?:moved to|advanced to|changed to|reset to|transitioned to|set/verified as|set to)\s+(" + _S + r")\b",
        re.IGNORECASE)),
    ("advanced_deliv", re.compile(
        r"\badvanced this deliverable to\s+(" + _S + r")\b")),
    ("advancing_from_to", re.compile(
        r"\badvancing\b[^.]*?\bfrom\s+(?:" + _S + r")\s+to\s+(" + _S + r")\b")),
    ("moving_to", re.compile(
        r"\bmoving\b[^.]*?\bto\s+(" + _S + r")\b")),
    ("transition_to", re.compile(
        r"\b(?:lifecycle )?transition to\s+(" + _S + r")\b")),
    ("set_state_to", re.compile(
        r"\bset state to\s+(" + _S + r")\b")),
    ("remains", re.compile(
        r"\b(?:lifecycle )?(?:state|Current State) remains\s+(" + _S + r")\b")),
    ("aligned_to", re.compile(
        r"\b(?:re)?aligned to\s+(" + _S + r")\b")),
)


@dataclass
class HistoryEntry:
    date: str | None
    raw: str
    state: str | None
    actor: str | None
    rule: str | None
    caveat_class: str


@dataclass
class ParsedStatusDoc:
    title: str | None
    fields: dict[str, str]
    history: list[HistoryEntry] = field(default_factory=list)
    doc_caveat_class: str = PARSED
    doc_caveats: list[str] = field(default_factory=list)

    @property
    def current_state(self) -> str | None:
        return self.fields.get("Current State")

    @property
    def last_updated(self) -> str | None:
        return self.fields.get("Last Updated")


def parse_bullet(text: str) -> HistoryEntry:
    """Classify one history bullet body (without the leading '- ')."""
    date = None
    m_date = DATE_PREFIX_RE.match(text)
    if m_date:
        date = m_date.group(1)
    m1 = RULE_1_STRICT.match(text)
    if m1:
        return HistoryEntry(
            date=date, raw=text, state=m1.group(1).upper(),
            actor=m1.group(2).strip() or None, rule="strict",
            caveat_class=PARSED,
        )
    for name, pattern in RULES_2_9:
        m = pattern.search(text)
        if m:
            return HistoryEntry(
                date=date, raw=text, state=m.group(1).upper(),
                actor=None, rule=name,
                caveat_class=PARSED_WITH_ASSUMPTIONS,
            )
    return HistoryEntry(
        date=date, raw=text, state=None, actor=None, rule=None,
        caveat_class=UNPARSEABLE,
    )


def _history_block(text: str) -> str | None:
    m = HISTORY_HEADING_RE.search(text)
    if not m:
        return None
    rest = text[m.end():]
    nxt = HEADING_RE.search(rest)
    return rest[: nxt.start()] if nxt else rest


def parse_status_document(text: str) -> ParsedStatusDoc:
    fields: dict[str, str] = {}
    for m in FIELD_RE.finditer(text):
        key = m.group(1).strip()
        if key not in fields:
            fields[key] = m.group(2).strip()
    title_m = TITLE_RE.search(text)
    doc = ParsedStatusDoc(title=title_m.group(1) if title_m else None, fields=fields)

    for required in ("Current State", "Last Updated"):
        if required not in fields:
            doc.doc_caveat_class = UNPARSEABLE
            doc.doc_caveats.append(f"missing required field '**{required}:**'")

    block = _history_block(text)
    if block is None:
        doc.doc_caveats.append("missing '## History' section")
    else:
        for line in block.splitlines():
            m = BULLET_RE.match(line)
            if m:
                doc.history.append(parse_bullet(m.group(1)))
    return doc


def last_state_assertion(
    entries: list[HistoryEntry],
    lifecycle_states: list[str] | tuple[str, ...],
) -> tuple[HistoryEntry | None, int]:
    """Return the last state-bearing assertion (caveat_class != UNPARSEABLE and
    state within the manifest lifecycle states) and the count of trailing
    UNPARSEABLE bullets after it."""
    lifecycle = {s.upper() for s in lifecycle_states}
    chosen_idx: int | None = None
    for idx in range(len(entries) - 1, -1, -1):
        e = entries[idx]
        if e.caveat_class != UNPARSEABLE and e.state and e.state in lifecycle:
            chosen_idx = idx
            break
    if chosen_idx is None:
        trailing = sum(1 for e in entries if e.caveat_class == UNPARSEABLE)
        return None, trailing
    trailing = sum(
        1 for e in entries[chosen_idx + 1:] if e.caveat_class == UNPARSEABLE
    )
    return entries[chosen_idx], trailing
