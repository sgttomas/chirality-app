from pathlib import Path

import pytest

from tools.source_catalog.source_database import resolve_domain_root


def test_explicit_domain_root_wins(tmp_path: Path) -> None:
    explicit = tmp_path / "elsewhere"
    assert resolve_domain_root(explicit, cwd=tmp_path) == explicit


def test_current_directory_must_be_a_domain_pack(tmp_path: Path) -> None:
    (tmp_path / "domain-pack.yaml").write_text("id: fixture\n", encoding="utf-8")
    assert resolve_domain_root(None, cwd=tmp_path) == tmp_path.resolve()


def test_missing_domain_root_fails_clearly(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="--domain-root is required"):
        resolve_domain_root(None, cwd=tmp_path)
