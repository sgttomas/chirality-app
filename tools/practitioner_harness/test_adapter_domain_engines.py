#!/usr/bin/env python3
"""Domain-engines observation adapter tests (fixture tree)."""

from __future__ import annotations

import adapter_domain_engines
from test_self_check_fixtures import build_mini_repo


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_ruled_row_count_excludes_title_annotation(tmp_path):
    # The fixture register carries a bolded RULED annotation in its title
    # (the live register's shape) plus exactly one RULED table row; only
    # the row may count.
    repo = build_mini_repo(tmp_path)
    obs = adapter_domain_engines.observe_domain_engines(repo)
    assert obs.register_counts["RULED"] == 1
    fact = next(f for f in obs.facts if f.fact_id == "decisions.ruled_row_count")
    assert fact.value == "1"
    assert "rows" in fact.caveat


def test_profile_observations_are_keyed_per_profile_id(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(
        repo / "_DomainEngines" / "profiles" / "pec.yaml",
        """domain_profile:
  schema_version: "1.0"
  id: "pec"
  name: "PEC"
  profile_version: "0.1"
  profile_status: "DRAFT"
  integration_level: "MANUAL_BRIDGE"
  protected_write_paths:
    - "projects/pec/**"
  agent_writable_paths:
    - "_DomainEngines/proposals/pec/**"
""",
    )

    obs = adapter_domain_engines.observe_domain_engines(repo)

    assert set(obs.profile_observations) == {"open_pipe_stress", "pec"}
    assert obs.profile_observations["open_pipe_stress"].profile_path.name == (
        "open_pipe_stress.DRAFT.yaml"
    )
    assert obs.profile_observations["pec"].profile_path.name == "pec.yaml"
    assert obs.profile_observations["pec"].protected_write_paths == [
        "projects/pec/**"
    ]
    # Legacy single-profile fields remain bound to OpenPipeStress for existing
    # harness consumers while keyed observations carry PEC independently.
    assert obs.profile_data["domain_profile"]["id"] == "open_pipe_stress"
    facts = {fact.fact_id: fact.value for fact in obs.facts}
    assert facts["profile.profile_status"] == "ADOPTED"
    assert facts["profile.open_pipe_stress.profile_status"] == "ADOPTED"
    assert facts["profile.pec.profile_status"] == "DRAFT"
