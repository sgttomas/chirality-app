from __future__ import annotations

import sys
from pathlib import Path


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

from build_section_map import (  # noqa: E402
    parse_status_lifecycle,
    resolve_lifecycle_state,
    select_ktys_for_section,
)


KTYS = {
    "KTY-01_A": {"KnowledgeTypeID": "KTY-01_A", "ParentCategoryID": "CAT-001", "CanonicalSchemaNormalized": "EQUIPMENT"},
    "KTY-02_B": {"KnowledgeTypeID": "KTY-02_B", "ParentCategoryID": "CAT-002", "CanonicalSchemaNormalized": "UTILITY"},
    "KTY-03_C": {"KnowledgeTypeID": "KTY-03_C", "ParentCategoryID": "CAT-003", "CanonicalSchemaNormalized": "EQUIPMENT"},
}


def test_select_ktys_union_semantics():
    section = {
        "IncludeCategoryIDs": "CAT-001",
        "IncludeKnowledgeTypeIDs": "KTY-02_B",
        "IncludeCanonicalSchemas": "",
        "ExcludeCategoryIDs": "",
        "ExcludeKnowledgeTypeIDs": "",
    }
    assert select_ktys_for_section(section, KTYS) == ["KTY-01_A", "KTY-02_B"]


def test_select_ktys_exclusion():
    section = {
        "IncludeCategoryIDs": "",
        "IncludeKnowledgeTypeIDs": "",
        "IncludeCanonicalSchemas": "Equipment",
        "ExcludeCategoryIDs": "",
        "ExcludeKnowledgeTypeIDs": "KTY-03_C",
    }
    assert select_ktys_for_section(section, KTYS) == ["KTY-01_A"]


def test_lifecycle_filtering_retired(tmp_path):
    status = tmp_path / "_STATUS.md"
    artifact = tmp_path / "KA-01.md"
    status.write_text("LifecycleState: RETIRED\n", encoding="utf-8")
    artifact.write_text("active-looking content\n", encoding="utf-8")
    assert parse_status_lifecycle(status) == "RETIRED"
    assert resolve_lifecycle_state(True, ("", ""), status, artifact) == ("RETIRED", "_STATUS.md")


def test_lifecycle_filtering_active(tmp_path):
    status = tmp_path / "_STATUS.md"
    artifact = tmp_path / "KA-01.md"
    status.write_text("LifecycleState: INITIALIZED\n", encoding="utf-8")
    artifact.write_text("active content\n", encoding="utf-8")
    assert resolve_lifecycle_state(True, ("", ""), status, artifact) == ("ACTIVE", "_STATUS.md")


def test_lifecycle_precedence_sca_overrides_status(tmp_path):
    status = tmp_path / "_STATUS.md"
    artifact = tmp_path / "KA-01.md"
    status.write_text("LifecycleState: INITIALIZED\n", encoding="utf-8")
    artifact.write_text("active content\n", encoding="utf-8")
    assert resolve_lifecycle_state(True, ("RETIRED", "SCA_ACTION"), status, artifact) == ("RETIRED", "SCA_ACTION")


def test_tombstone_detection(tmp_path):
    status = tmp_path / "_STATUS.md"
    artifact = tmp_path / "KA-01.md"
    status.write_text("LifecycleState: INITIALIZED\n", encoding="utf-8")
    artifact.write_text("RETIRED_NO_FACTUAL_USE\n", encoding="utf-8")
    assert resolve_lifecycle_state(True, ("", ""), status, artifact) == ("RETIRED", "TOMBSTONE_HEADER")
