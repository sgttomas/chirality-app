"""Shared test setup for the practitioner-harness suite.

Puts this directory on sys.path so tests import the harness modules bare,
and installs the session-scoped fixture-repo template root (see
harness_template_cache: identical fixture repos are built once per session
and copied per test; tests mutate their own copies).
"""

import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import pytest

import harness_template_cache


# Git 2.55 can launch detached maintenance after a fixture commit returns.
# Cached fixture repositories are copied immediately after they are built, so
# the transient .git/objects/maintenance.lock made that copy race with Git.
# Configure every Git subprocess in this pytest process, including raw
# subprocess.run calls in individual fixture builders, to keep fixture repos
# quiescent before harness_template_cache copies them.  The gc settings cover
# the older auto-gc path as well as the detached-maintenance path.
_FIXTURE_GIT_CONFIG = (
    ("maintenance.auto", "false"),
    ("gc.auto", "0"),
    ("gc.autoDetach", "false"),
)
try:
    _existing_git_config_count = int(os.environ.get("GIT_CONFIG_COUNT", "0"))
except ValueError as exc:
    raise RuntimeError("GIT_CONFIG_COUNT must be an integer") from exc
if _existing_git_config_count < 0:
    raise RuntimeError("GIT_CONFIG_COUNT must not be negative")
os.environ["GIT_CONFIG_COUNT"] = str(
    _existing_git_config_count + len(_FIXTURE_GIT_CONFIG)
)
for _offset, (_key, _value) in enumerate(_FIXTURE_GIT_CONFIG):
    _index = _existing_git_config_count + _offset
    os.environ[f"GIT_CONFIG_KEY_{_index}"] = _key
    os.environ[f"GIT_CONFIG_VALUE_{_index}"] = _value


@pytest.fixture(scope="session", autouse=True)
def _fixture_repo_templates(tmp_path_factory):
    harness_template_cache.set_root(tmp_path_factory.mktemp("repo-templates"))
    yield
    harness_template_cache.set_root(None)
