from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import tools.validation.discover_test_surfaces as discover


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_discover_surfaces_from_fixture_tree(tmp_path: Path) -> None:
    write(tmp_path / "tools/example/test_alpha.py", "def test_one():\n    pass\n\nclass TestTwo:\n    pass\n")
    write(
        tmp_path / "projects/chirality-app-dev/frontend/src/__tests__/app.test.ts",
        "import { test, it } from 'vitest';\ntest('a', () => {});\nit('b', () => {});\n",
    )
    write(tmp_path / "projects/chirality-piping/tests/test_model.py", "def test_model():\n    pass\n")
    write(
        tmp_path / "projects/chirality-piping/apps/desktop/src/App.test.tsx",
        "import { it } from 'vitest';\nit('renders', () => {});\n",
    )
    write(
        tmp_path / "projects/chirality-piping/core/demo/src/lib.rs",
        "#[test]\nfn validates() {}\n\n#[cfg(test)]\nmod tests {}\n",
    )

    report = discover.discover(tmp_path)
    by_id = {surface["id"]: surface for surface in report["surfaces"]}

    assert by_id["tools-python"]["file_count"] == 1
    assert by_id["tools-python"]["test_symbol_count"] == 2
    assert by_id["chirality-app-dev-frontend-vitest"]["test_symbol_count"] == 2
    assert by_id["openpipestress-pytest"]["test_symbol_count"] == 1
    assert by_id["openpipestress-desktop-vitest"]["test_symbol_count"] == 1
    assert by_id["openpipestress-rust"]["test_symbol_count"] == 1
    assert report["totals"]["surface_count"] == 5


def test_cli_emits_json_by_default(tmp_path: Path) -> None:
    write(tmp_path / "tools/example/test_alpha.py", "def test_one():\n    pass\n")

    result = subprocess.run(
        [sys.executable, "tools/validation/discover_test_surfaces.py", str(tmp_path)],
        check=True,
        text=True,
        capture_output=True,
    )

    report = json.loads(result.stdout)
    assert report["schema"] == "chirality-test-surfaces/v1"
    assert report["totals"]["test_symbol_count"] == 1
