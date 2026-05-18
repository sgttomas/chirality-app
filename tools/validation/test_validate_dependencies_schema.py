import csv
import subprocess
import sys
from pathlib import Path

from validate_dependencies_schema import REQUIRED_COLUMNS


SCRIPT = Path(__file__).with_name("validate_dependencies_schema.py")


def write_valid_dependencies(path: Path, rows: list[dict[str, str]] | None = None) -> None:
    row = {column: f"{column}-value" for column in REQUIRED_COLUMNS}
    row["RegisterSchemaVersion"] = "v3.1"
    row["DependencyID"] = "DEP-TEST-001"
    rows = rows or [row]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_accepts_valid_dependencies_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "Dependencies.csv"
    write_valid_dependencies(csv_path)

    result = run_validator(csv_path)

    assert result.returncode == 0
    assert "VALID:" in result.stdout


def test_rejects_row_field_count_mismatch(tmp_path: Path) -> None:
    csv_path = tmp_path / "Dependencies.csv"
    header = ",".join(REQUIRED_COLUMNS)
    row = ["v3.1", "DEP-TEST-001"] + ["value"] * (len(REQUIRED_COLUMNS) - 1)
    csv_path.write_text(header + "\n" + ",".join(row) + "\n", encoding="utf-8")

    result = run_validator(csv_path)

    assert result.returncode == 1
    assert "field count mismatch" in result.stdout
    assert "DEP-TEST-001" in result.stdout


def test_rejects_invalid_register_schema_version(tmp_path: Path) -> None:
    csv_path = tmp_path / "Dependencies.csv"
    row = {column: f"{column}-value" for column in REQUIRED_COLUMNS}
    row["RegisterSchemaVersion"] = "v3.0"
    row["DependencyID"] = "DEP-TEST-002"
    write_valid_dependencies(csv_path, [row])

    result = run_validator(csv_path)

    assert result.returncode == 1
    assert "invalid RegisterSchemaVersion" in result.stdout
    assert "DEP-TEST-002" in result.stdout


def test_rejects_missing_required_column(tmp_path: Path) -> None:
    csv_path = tmp_path / "Dependencies.csv"
    columns = [column for column in REQUIRED_COLUMNS if column != "Notes"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerow({column: "v3.1" if column == "RegisterSchemaVersion" else "value" for column in columns})

    result = run_validator(csv_path)

    assert result.returncode == 1
    assert "Missing columns" in result.stdout
    assert "Notes" in result.stdout
