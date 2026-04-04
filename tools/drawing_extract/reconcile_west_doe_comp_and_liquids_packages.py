#!/usr/bin/env python3
"""
Manual package reconciliation for the West Doe compression/liquids equipment extract.

The PFD-derived CSV remains authoritative. This script:
1. adds a `package_name` column to the existing PFD extract,
2. applies manual package inferences based on the DBM master list, and
3. appends a small set of strong master-only additions with DBM provenance.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


INLET_SEPARATOR_PACKAGE = "Inlet Separator Package (indicated)"
INLET_COMPRESSOR_PACKAGE = "Inlet Compressor Package (indicated)"
VRU_PACKAGE = "VRU Package"
HEAT_MEDIUM_MODULE = "Heat Medium System Module"
TEG_MODULE = "Module 570 - TEG Regeneration Module"
CONDENSATE_MERCAPTAN_PACKAGE = "Condensate Mercaptan Treating Unit (indicated)"
INLET_STABILIZER_PACKAGE = "Inlet Stabilizer Package (indicated)"
STAB_OVERHEAD_COMPRESSOR_PACKAGE = "Stabilizer Overhead Compressor Package (indicated)"
TANK_FARM_PUMP_MODULE = "Tank Farm Pump Module (indicated)"


MANUAL_ADDITIONS = [
    {
        "equipment_number": "PCV-1601-2",
        "equipment_name": "Inlet Pressure Control Valve - Package 1 (2x parallel per package)",
        "system_name": "INLET SEPARATOR",
        "drawing": "KTY-04-02",
        "source_page": "KA-13",
        "package_name": INLET_SEPARATOR_PACKAGE,
    },
    {
        "equipment_number": "PCV-1701-2",
        "equipment_name": "Inlet Pressure Control Valve - Package 2 (2x parallel per package)",
        "system_name": "INLET SEPARATOR",
        "drawing": "KTY-04-02",
        "source_page": "KA-13",
        "package_name": INLET_SEPARATOR_PACKAGE,
    },
    {
        "equipment_number": "AE-7103-2",
        "equipment_name": "4-Stream NIR Optical Spectroscopy Composition Analyzer - Stream 1 (Condensate, Stabilizer Bottoms)",
        "system_name": "STABILIZER UNIT",
        "drawing": "KTY-05-08",
        "source_page": "KA-01_Reference__Inlet-Condensate-Product-Analyzer.md",
        "package_name": "Inlet Condensate Product Analyzer System (indicated)",
    },
    {
        "equipment_number": "AE-7203-2",
        "equipment_name": "4-Stream NIR Optical Spectroscopy Composition Analyzer - Stream 2 (Condensate, Stabilizer Bottoms)",
        "system_name": "STABILIZER UNIT",
        "drawing": "KTY-05-08",
        "source_page": "KA-01_Reference__Inlet-Condensate-Product-Analyzer.md",
        "package_name": "Inlet Condensate Product Analyzer System (indicated)",
    },
    {
        "equipment_number": "420-2",
        "equipment_name": "Instrument Air Package",
        "system_name": "INSTRUMENT AIR PACKAGE",
        "drawing": "KTY-11-07",
        "source_page": "KA-01_Reference__Buildings.md",
        "package_name": "Vendor buyout package",
    },
    {
        "equipment_number": "830-2",
        "equipment_name": "4160V Inlet/Overheads Compressor Electrical Building",
        "system_name": "ELECTRICAL DISTRIBUTION",
        "drawing": "KTY-11-07",
        "source_page": "KA-01_Reference__Buildings.md",
        "package_name": "None",
    },
    {
        "equipment_number": "840-2",
        "equipment_name": "600V Electrical Building",
        "system_name": "ELECTRICAL DISTRIBUTION",
        "drawing": "KTY-11-07",
        "source_page": "KA-01_Reference__Buildings.md",
        "package_name": "None",
    },
    {
        "equipment_number": "990-2",
        "equipment_name": "LACT Electrical Building",
        "system_name": "CONDENSATE LACT",
        "drawing": "KTY-11-07",
        "source_page": "KA-01_Reference__Buildings.md",
        "package_name": "None",
    },
    {
        "equipment_number": "991-2",
        "equipment_name": "LACT Electrical Building",
        "system_name": "NRM CONDENSATE LACT",
        "drawing": "KTY-11-07",
        "source_page": "KA-01_Reference__Buildings.md",
        "package_name": "None",
    },
    {
        "equipment_number": "No tag",
        "equipment_name": "MV Motor Control Centre (MCC)",
        "system_name": "ELECTRICAL BUILDING MODULE",
        "drawing": "KTY-12-05",
        "source_page": "KA-02",
        "package_name": "Electrical Building Module",
    },
    {
        "equipment_number": "No tag",
        "equipment_name": "600V Motor Control Centre (MCC)",
        "system_name": "ELECTRICAL BUILDING MODULE",
        "drawing": "KTY-12-05",
        "source_page": "KA-02",
        "package_name": "Electrical Building Module",
    },
    {
        "equipment_number": "No tag",
        "equipment_name": "Plant PLC Control Panel",
        "system_name": "ELECTRICAL BUILDING MODULE",
        "drawing": "KTY-12-05",
        "source_page": "KA-02",
        "package_name": "Electrical Building Module",
    },
    {
        "equipment_number": "No tag",
        "equipment_name": "Allen-Bradley Compactlogix Controller",
        "system_name": "UNIT CONTROL SYSTEM (UCS) - COMPRESSION",
        "drawing": "KTY-13-08",
        "source_page": "KA-03",
        "package_name": "Unit Control System (UCS) - Compression",
    },
    {
        "equipment_number": "No tag",
        "equipment_name": "Spartan Controls Remvue Compressor Control Panel",
        "system_name": "UNIT CONTROL SYSTEM (UCS) - COMPRESSION",
        "drawing": "KTY-13-08",
        "source_page": "KA-03",
        "package_name": "Unit Control System (UCS) - Compression",
    },
    {
        "equipment_number": "No tag",
        "equipment_name": "Redlion DA30D Protocol Converter",
        "system_name": "MODBUS INTEGRATION - PACKAGED EQUIPMENT",
        "drawing": "KTY-13-10",
        "source_page": "KA-01",
        "package_name": "Modbus Integration - Packaged Equipment",
    },
    {
        "equipment_number": "No tag",
        "equipment_name": "Flow Computers (Stand-alone)",
        "system_name": "METERING SYSTEM",
        "drawing": "KTY-13-11",
        "source_page": "KA-01",
        "package_name": "Metering System",
    },
]


def infer_package_name(row: dict[str, str]) -> str:
    equipment_number = (row.get("equipment_number") or "").strip()
    system_name = (row.get("system_name") or "").strip()
    drawing = (row.get("drawing") or "").strip()
    source_page = (row.get("source_page") or "").strip()

    if equipment_number in {"V-1600-2", "V-1700-2"}:
        return INLET_SEPARATOR_PACKAGE

    if drawing.startswith("PFD-242510-2100-"):
        return INLET_COMPRESSOR_PACKAGE

    if drawing.startswith("PFD-242510-3100-"):
        return VRU_PACKAGE

    if drawing.startswith("PFD-242510-5100-"):
        return HEAT_MEDIUM_MODULE

    if drawing.startswith("PFD-242510-5700-"):
        return TEG_MODULE

    if system_name in {
        "CONDENSATE CAUSTIC UNIT",
        "CONDENSATE CAUSTIC UNIT - HEATERS",
        "CONDENSATE WATER WASH",
        "INCINERATOR KNOCK OUT DRUM",
    }:
        return CONDENSATE_MERCAPTAN_PACKAGE

    if system_name == "STABILIZER UNIT":
        return INLET_STABILIZER_PACKAGE

    if drawing.startswith("PFD-242510-7300-"):
        return INLET_STABILIZER_PACKAGE

    if drawing.startswith("PFD-242510-7500-"):
        return STAB_OVERHEAD_COMPRESSOR_PACKAGE

    if source_page in {"54", "55"}:
        return TANK_FARM_PUMP_MODULE

    return "None"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "equipment_number",
        "equipment_name",
        "system_name",
        "drawing",
        "source_page",
        "package_name",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_csv")
    args = parser.parse_args()

    source_csv = Path(args.source_csv).resolve()
    rows = load_rows(source_csv)

    updated_rows: list[dict[str, str]] = []
    package_assigned = 0
    for row in rows:
        updated_row = {
            "equipment_number": (row.get("equipment_number") or "").strip(),
            "equipment_name": (row.get("equipment_name") or "").strip(),
            "system_name": (row.get("system_name") or "").strip(),
            "drawing": (row.get("drawing") or "").strip(),
            "source_page": (row.get("source_page") or "").strip(),
            "package_name": infer_package_name(row),
        }
        if updated_row["package_name"] != "None":
            package_assigned += 1
        updated_rows.append(updated_row)

    existing_keys = {
        (
            row["equipment_number"],
            row["equipment_name"],
            row["drawing"],
            row["source_page"],
        )
        for row in updated_rows
    }

    additions_appended = 0
    for addition in MANUAL_ADDITIONS:
        key = (
            addition["equipment_number"],
            addition["equipment_name"],
            addition["drawing"],
            addition["source_page"],
        )
        if key in existing_keys:
            continue
        updated_rows.append(addition)
        existing_keys.add(key)
        additions_appended += 1

    write_rows(source_csv, updated_rows)

    print(f"rows_written={len(updated_rows)}")
    print(f"package_assigned_existing_rows={package_assigned}")
    print(f"master_only_additions={additions_appended}")
    print(f"output={source_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
