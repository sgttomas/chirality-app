#!/usr/bin/env python3
"""Validate root instruction entrypoints and the Claude import contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EXPECTED_CLAUDE = "@AGENTS.md\n"
PROJECTS = ("chirality-app-dev", "chirality-piping")

ROLE_PATTERNS = (
    re.compile(r"\bHELP_HUMAN\b"),
    re.compile(r"\bWORKING_ITEMS\b"),
    re.compile(r"\bTASK\b"),
    re.compile(r"\bCHANGE\b"),
    re.compile(r"\bAgent 0\b"),
    re.compile(r"\bAgent 1\b"),
    re.compile(r"\bAgent 2\b"),
)
ROUTING_VERB = re.compile(
    r"\b(?:invoke|invokes|launch|launches|delegate|delegates|dispatch|dispatches|"
    r"report|reports|select|selects|persist|persists|persisted|persisting|fan-in)\b",
    re.IGNORECASE,
)
REFERENCE_SIGNAL = re.compile(
    r"\b(?:governed by|defined in|described in|see|follow|per)\b",
    re.IGNORECASE,
)
CANONICAL_REFERENCE = re.compile(
    r"(?:`?AGENTS\.md`?|canonical agent instructions?|governed instrument|D-APP-\d+)",
    re.IGNORECASE,
)
PRESCRIPTIVE_SIGNAL = re.compile(
    r"\b(?:must|shall|us(?:e|es|ed|ing)|record(?:s|ed|ing)?|"
    r"persist(?:s|ed|ing)?|assign(?:s|ed|ing)?|serializ(?:e|es|ed|ing)|"
    r"hold(?:s|ing)?|held|requir(?:e|es|ed|ing))\b",
    re.IGNORECASE,
)
TOPOLOGY_HEADING = re.compile(
    r"\b(?:multi-agent orchestration|runtime role[- ]routing(?: matrix)?|execution topology|"
    r"work[- ]graph schema)\b",
    re.IGNORECASE,
)
MECHANICS_CLUSTERS = (
    (
        "selection-authority/posture",
        re.compile(
            r"\b(?:selection authority|TERMINAL_FAN_OUT_IN|"
            r"SUPERVISED_MANY_TO_MANY|execution posture)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "child-session persistence",
        re.compile(
            r"(?:\bchild sessions?\b|\bchild-session persistence schema\b|"
            r"\bpersist(?:s|ed|ing)?\b.{0,50}\b(?:child|session|graph)\b|"
            r"AgentRuns/<RunID>)",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "parent/sibling relays",
        re.compile(
            r"\b(?:parent-mediated|siblings? (?:do not|must not)|"
            r"report(?:s|ed|ing)? to (?:its |the )?parent|relay rules?)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "concurrent-write/fan-in ownership",
        re.compile(
            r"\b(?:concurrent writes?|fan-in gates?|integration owner|"
            r"shared-write ownership)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "model/capability assignment",
        re.compile(
            r"\b(?:MODEL-AGNOSTIC|capability tier|model substitution|"
            r"model assignment)\b",
            re.IGNORECASE,
        ),
    ),
)


def _project_launchers(root_init_text: str, project_name: str) -> list[str]:
    blocks = re.findall(
        r"(?ms)^<init-prompt>\n.*?^</init-prompt>\n?",
        root_init_text,
    )
    project_token = f"projects/{project_name}"
    return [block for block in blocks if project_token in block]


def _selects_help_human(project_init_text: str) -> bool:
    return bool(
        re.search(
            r"Act as\s+`?HELP_HUMAN`?\s+for\s+`?\{WORKING_ROOT\}`?(?:\.|\s|$)",
            project_init_text,
        )
    )


def _paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def _sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    heading = ""
    body: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            if heading or body:
                sections.append((heading, "\n".join(body)))
            heading = line
            body = []
        else:
            body.append(line)
    if heading or body:
        sections.append((heading, "\n".join(body)))
    return sections


def _is_by_reference(paragraph: str) -> bool:
    return (
        bool(REFERENCE_SIGNAL.search(paragraph))
        and bool(CANONICAL_REFERENCE.search(paragraph))
        and not bool(ROUTING_VERB.search(paragraph))
        and not bool(PRESCRIPTIVE_SIGNAL.search(paragraph))
    )


def _structural_duplication_findings(path: Path, repo_root: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(repo_root)
    findings: list[str] = []

    for heading, body in _sections(text):
        if heading and TOPOLOGY_HEADING.search(heading):
            findings.append(
                f"{rel} duplicates canonical runtime mechanics in section "
                f"'{heading.lstrip('#').strip()}'"
            )
        operative_body = "\n\n".join(
            paragraph for paragraph in _paragraphs(body) if not _is_by_reference(paragraph)
        )
        clusters = [
            label
            for label, pattern in MECHANICS_CLUSTERS
            if pattern.search(operative_body)
        ]
        if len(clusters) >= 2:
            findings.append(
                f"{rel} duplicates canonical runtime mechanics clusters: "
                + ", ".join(clusters)
            )

    for paragraph in _paragraphs(text):
        if _is_by_reference(paragraph):
            continue
        role_count = sum(bool(pattern.search(paragraph)) for pattern in ROLE_PATTERNS)
        if role_count >= 2 and ROUTING_VERB.search(paragraph):
            findings.append(
                f"{rel} duplicates canonical role routing in paragraph: "
                f"'{paragraph.splitlines()[0][:100]}'"
            )

    return findings


def validate(repo_root: Path) -> list[str]:
    findings: list[str] = []
    agents = repo_root / "AGENTS.md"
    claude = repo_root / "CLAUDE.md"
    root_init = repo_root / "init" / "init-prompt.md"
    if not agents.is_file():
        findings.append("missing root AGENTS.md")
    if not claude.is_file():
        findings.append("missing root CLAUDE.md")
    elif claude.read_text(encoding="utf-8") != EXPECTED_CLAUDE:
        findings.append("CLAUDE.md must contain exactly '@AGENTS.md\\n'")

    root_init_text = root_init.read_text(encoding="utf-8") if root_init.is_file() else ""
    for project_name in PROJECTS:
        project_root = repo_root / "projects" / project_name
        if not project_root.is_dir():
            continue
        project_agents = project_root / "AGENTS.md"
        project_init = project_root / "init" / "init-prompt.md"
        loop_init = project_root / "loop" / "LOOP_INIT.md"
        workplans = sorted((project_root / "loop").glob("WORKPLAN_*.md"))
        current_workplan = workplans[-1] if workplans else None
        profile = project_root / "software-workflow.json"
        for required in (project_agents, project_init, loop_init, profile):
            if not required.is_file():
                findings.append(f"{required.relative_to(repo_root)} is missing")
        if current_workplan is None:
            findings.append(
                f"{(project_root / 'loop').relative_to(repo_root)} has no WORKPLAN_*.md"
            )

        if project_agents.is_file():
            text = project_agents.read_text(encoding="utf-8").lower()
            for phrase in ("software_workflow_profile.md",):
                if phrase not in text:
                    findings.append(
                        f"{project_agents.relative_to(repo_root)} is missing '{phrase}'"
                    )

        help_human_entry = False
        if project_init.is_file():
            project_init_text = project_init.read_text(encoding="utf-8")
            help_human_entry = _selects_help_human(project_init_text)
            if not root_init.is_file():
                findings.append("missing root init/init-prompt.md")
            else:
                catalog_launchers = _project_launchers(root_init_text, project_name)
                if len(catalog_launchers) != 1:
                    findings.append(
                        "root init/init-prompt.md must contain exactly one tagged "
                        f"launcher for projects/{project_name}; found {len(catalog_launchers)}"
                    )
                elif project_init_text != catalog_launchers[0]:
                    findings.append(
                        f"{project_init.relative_to(repo_root)} does not byte-match the "
                        f"tagged root launcher for projects/{project_name}"
                    )
            if help_human_entry:
                for phrase in (
                    "Read `{REPO_ROOT}/AGENTS.md`.",
                    "Read `{REPO_ROOT}/agents/AGENT_HELP_HUMAN.md`.",
                    "Act as `HELP_HUMAN` for `{WORKING_ROOT}`.",
                    "Read `{WORKING_ROOT}/loop/LOOP_INIT.md`",
                ):
                    if phrase not in project_init_text:
                        findings.append(
                            f"{project_init.relative_to(repo_root)} is missing '{phrase}'"
                        )

        if help_human_entry:
            for path in (loop_init, current_workplan):
                if path is not None and path.is_file():
                    findings.extend(_structural_duplication_findings(path, repo_root))

        if loop_init.is_file():
            text = loop_init.read_text(encoding="utf-8")
            if "when the managed runtime is active" in text:
                findings.append(
                    f"{loop_init.relative_to(repo_root)} retains the retired pre-bridge fallback"
                )
        if profile.is_file():
            try:
                payload = json.loads(profile.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                findings.append(f"{profile.relative_to(repo_root)} is not valid JSON")
            else:
                if payload.get("schema") != "chirality-software-workflow/v1":
                    findings.append(f"{profile.relative_to(repo_root)} has the wrong schema")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    findings = validate(Path(args.repo_root).resolve())
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        return 1
    print("PASS: root instruction entrypoints are canonical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
