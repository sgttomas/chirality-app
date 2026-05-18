#!/usr/bin/env python3
"""
recover_deepcut_multiblock_headers.py
Deterministically backfill known undercounted Deepcut compressor-train header pages.

This is a targeted recovery pass for the repeated multi-block top-header layout in:
    PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined

It overwrites the affected page stubs with row sets verified from the rendered
top-header crops and writes an optional recovery report CSV.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from normalize_equipment_stub_layout import parse_stub, render_stub


PDF_STEM_DEFAULT = "PFD-235633_E (4-25 Doe)_Process Flow Diagram_Combined"


PAGE_FIXTURES: dict[int, dict[str, object]] = {
    10: {
        "drawing": "PFD-235633-1100-001",
        "rows": [
            ["F-3200-1", "SALES GAS FILTER/COALESCER"],
            ["E-5718-1", "INLET/TEG DEHY CROSS EXCHANGER"],
        ],
    },
    34: {
        "drawing": "PFD-235633-3200-003",
        "rows": [
            ["F-3200-1", "SALES GAS FILTER COALESCER"],
        ],
    },
    40: {
        "drawing": "PFD-235633-4100-001",
        "rows": [
            ["V-4110-1", "CRYO FLARE K.O. DRUM"],
            ["V-4100-1", "H.P. FLARE K.O. DRUM"],
            ["H-4112-1", "CRYO FLARE K.O. DRUM HEATER"],
            ["P-4100-1", "HP FLARE K.O. DRUM TRANSFER PUMP"],
            ["FL-4120-1", "FLARE STACK"],
        ],
    },
    37: {
        "drawing": "PFD-235633-3400-001",
        "rows": [
            ["AC-3415-1", "SALES GAS BOOSTER INTERCOOLER"],
            ["V-3410-1", "SALES GAS BOOSTER 1ST STAGE SUCTION SCRUBBER"],
            ["C-3412-1", "SALES GAS BOOSTER 1ST STAGE CYLINDER"],
            ["AC-3425-1", "SALES GAS BOOSTER AFTERCOOLER"],
            ["V-3420-1", "SALES GAS BOOSTER 2ND STAGE SUCTION SCRUBBER"],
            ["C-3422-1", "SALES GAS BOOSTER 2ND STAGE CYLINDER"],
            ["K-3450-1", "RECIPROCATING GAS COMPRESSOR"],
            ["KD-3450-1", "SALES GAS BOOSTER COMPRESSOR DRIVER"],
            ["TK-3464-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["P-3464-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
        ],
    },
    20: {
        "drawing": "PFD-235633-2100-002",
        "rows": [
            ["V-2110-1", "INLET 1ST STAGE SUCTION SCRUBBER"],
            ["C-2111-1", "INLET 1ST STAGE CYLINDER"],
            ["K-2150-1", "RECIPROCATING GAS COMPRESSOR"],
            ["KM-2150-1", "INLET/SALES COMPRESSOR MOTOR"],
            ["AC-2115-1", "INLET GAS AFTERCOOLER"],
            ["TK-2164-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["ACF-2150-1", "AIR COOLER FRAME"],
            ["P-2164-1", "VACUUM PUMP"],
            ["P-2165-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
        ],
    },
    21: {
        "drawing": "PFD-235633-2100-003",
        "rows": [
            ["V-2210-1", "INLET 1ST STAGE SUCTION SCRUBBER"],
            ["C-2211-1", "INLET 1ST STAGE CYLINDER"],
            ["K-2250-1", "RECIPROCATING GAS COMPRESSOR"],
            ["KM-2250-1", "INLET/SALES COMPRESSOR MOTOR"],
            ["AC-2215-1", "INLET GAS AFTERCOOLER"],
            ["TK-2264-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["ACF-2250-1", "AIR COOLER FRAME"],
            ["P-2264-1", "VACUUM PUMP"],
            ["P-2265-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
        ],
    },
    22: {
        "drawing": "PFD-235633-2100-004",
        "rows": [
            ["V-2310-1", "INLET 1ST STAGE SUCTION SCRUBBER"],
            ["C-2311-1", "INLET 1ST STAGE CYLINDER"],
            ["K-2350-1", "RECIPROCATING GAS COMPRESSOR"],
            ["KM-2350-1", "INLET/SALES COMPRESSOR MOTOR"],
            ["AC-2315-1", "INLET GAS AFTERCOOLER"],
            ["TK-2364-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["ACF-2350-1", "AIR COOLER FRAME"],
            ["P-2364-1", "VACUUM PUMP"],
            ["P-2365-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
        ],
    },
    23: {
        "drawing": "PFD-235633-2100-005",
        "rows": [
            ["V-2410-1", "INLET 1ST STAGE SUCTION SCRUBBER"],
            ["C-2411-1", "INLET 1ST STAGE CYLINDER"],
            ["K-2450-1", "RECIPROCATING GAS COMPRESSOR"],
            ["KM-2450-1", "INLET/SALES COMPRESSOR MOTOR"],
            ["AC-2415-1", "INLET GAS AFTERCOOLER"],
            ["TK-2464-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["ACF-2450-1", "AIR COOLER FRAME"],
            ["P-2464-1", "VACUUM PUMP"],
            ["P-2465-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
        ],
    },
    24: {
        "drawing": "PFD-235633-2100-006",
        "rows": [
            ["V-2510-1", "INLET 1ST STAGE SUCTION SCRUBBER"],
            ["C-2511-1", "INLET 1ST STAGE CYLINDER"],
            ["K-2550-1", "RECIPROCATING GAS COMPRESSOR"],
            ["KM-2550-1", "INLET/SALES COMPRESSOR MOTOR"],
            ["AC-2515-1", "INLET GAS AFTERCOOLER"],
            ["TK-2564-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["ACF-2550-1", "AIR COOLER FRAME"],
            ["P-2564-1", "VACUUM PUMP"],
            ["P-2565-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
        ],
    },
    26: {
        "drawing": "PFD-235633-2100-008",
        "rows": [
            ["V-2120-1", "SALES 1ST STAGE SUCTION SCRUBBER"],
            ["C-2121-1", "SALES 1ST STAGE CYLINDER"],
            ["AC-2125-1", "SALES 1ST STAGE INTERCOOLER"],
            ["V-2130-1", "SALES 2ND STAGE SUCTION SCRUBBER"],
            ["C-2131-1", "SALES 2ND STAGE CYLINDER"],
            ["KD-2130-1", "INLET/SALES COMPRESSOR DRIVER"],
            ["K-2130-1", "RECIPROCATING GAS COMPRESSOR"],
            ["AC-2135-1", "SALES 2ND STAGE AFTERCOOLER"],
            ["ACF-2160-1", "AIR COOLER FRAME"],
        ],
    },
    27: {
        "drawing": "PFD-235633-2100-009",
        "rows": [
            ["V-2220-1", "SALES 1ST STAGE SUCTION SCRUBBER"],
            ["C-2221-1", "SALES 1ST STAGE CYLINDER"],
            ["AC-2225-1", "SALES 1ST STAGE INTERCOOLER"],
            ["V-2230-1", "SALES 2ND STAGE SUCTION SCRUBBER"],
            ["C-2231-1", "SALES 2ND STAGE CYLINDER"],
            ["KD-2230-1", "INLET/SALES COMPRESSOR DRIVER"],
            ["K-2230-1", "RECIPROCATING GAS COMPRESSOR"],
            ["AC-2235-1", "SALES 2ND STAGE AFTERCOOLER"],
            ["ACF-2260-1", "AIR COOLER FRAME"],
        ],
    },
    28: {
        "drawing": "PFD-235633-2100-010",
        "rows": [
            ["V-2320-1", "SALES 1ST STAGE SUCTION SCRUBBER"],
            ["C-2321-1", "SALES 1ST STAGE CYLINDER"],
            ["AC-2325-1", "SALES 1ST STAGE INTERCOOLER"],
            ["V-2330-1", "SALES 2ND STAGE SUCTION SCRUBBER"],
            ["C-2331-1", "SALES 2ND STAGE CYLINDER"],
            ["KD-2330-1", "INLET/SALES COMPRESSOR DRIVER"],
            ["K-2330-1", "RECIPROCATING GAS COMPRESSOR"],
            ["AC-2335-1", "SALES 2ND STAGE AFTERCOOLER"],
            ["ACF-2360-1", "AIR COOLER FRAME"],
        ],
    },
    29: {
        "drawing": "PFD-235633-2100-011",
        "rows": [
            ["V-2420-1", "SALES 1ST STAGE SUCTION SCRUBBER"],
            ["C-2421-1", "SALES 1ST STAGE CYLINDER"],
            ["AC-2425-1", "SALES 1ST STAGE INTERCOOLER"],
            ["V-2430-1", "SALES 2ND STAGE SUCTION SCRUBBER"],
            ["C-2431-1", "SALES 2ND STAGE CYLINDER"],
            ["KD-2430-1", "INLET/SALES COMPRESSOR DRIVER"],
            ["K-2430-1", "RECIPROCATING GAS COMPRESSOR"],
            ["AC-2425-1", "SALES 2ND STAGE AFTERCOOLER"],
            ["ACF-2460-1", "AIR COOLER FRAME"],
        ],
    },
    30: {
        "drawing": "PFD-235633-2100-012",
        "rows": [
            ["V-2520-1", "SALES 1ST STAGE SUCTION SCRUBBER"],
            ["C-2521-1", "SALES 1ST STAGE CYLINDER"],
            ["AC-2525-1", "SALES 1ST STAGE INTERCOOLER"],
            ["V-2530-1", "SALES 2ND STAGE SUCTION SCRUBBER"],
            ["C-2531-1", "SALES 2ND STAGE CYLINDER"],
            ["KD-2530-1", "INLET/SALES COMPRESSOR DRIVER"],
            ["K-2530-1", "RECIPROCATING GAS COMPRESSOR"],
            ["AC-2525-1", "SALES 2ND STAGE AFTERCOOLER"],
            ["ACF-2560-1", "AIR COOLER FRAME"],
        ],
    },
    54: {
        "drawing": "PFD-235633-5400-001",
        "rows": [
            ["V-5430-1", "AGC 3RD STAGE SCRUBBER"],
            ["C-5431-1", "AGC 3RD STAGE CYLINDER"],
            ["P-5405-1/5415-1", "1ST STAGE SUCTION SCRUBBER PUMP"],
            ["AC-5435-1", "AGC 3RD STAGE INTERCOOLER"],
            ["V-5410-1", "AGC 1ST STAGE SCRUBBER"],
            ["V-5440-1", "AGC 4TH STAGE SCRUBBER"],
            ["C-5441-1", "AGC 4TH STAGE CYLINDER"],
            ["C-5411-1", "AGC 1ST STAGE CYLINDER"],
            ["AC-5415-1", "AGC 1ST STAGE INTERCOOLER"],
            ["AC-5445-1", "AGC 4TH STAGE INTERCOOLER"],
            ["V-5420-1", "AGC 2ND STAGE SCRUBBER"],
            ["C-5451-1", "AGC 5TH STAGE CYLINDER"],
            ["C-5421-1", "AGC 2ND STAGE CYLINDER"],
            ["AC-5455-1", "AGC AFTERCOOLER"],
            ["TK-5464-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["AC-5425-1", "AGC 2ND STAGE INTERCOOLER"],
            ["ACF-5480-1", "AIR COOLER FRAME"],
        ],
    },
    55: {
        "drawing": "PFD-235633-5400-002",
        "rows": [
            ["V-5530-1", "AGC 3RD STAGE SCRUBBER"],
            ["C-5531-1", "AGC 3RD STAGE CYLINDER"],
            ["P-5505-1/5515-1", "1ST STAGE SUCTION SCRUBBER PUMP"],
            ["AC-5535-1", "AGC 3RD STAGE INTERCOOLER"],
            ["V-5510-1", "AGC 1ST STAGE SCRUBBER"],
            ["V-5540-1", "AGC 4TH STAGE SCRUBBER"],
            ["C-5511-1", "AGC 1ST STAGE CYLINDER"],
            ["C-5541-1", "AGC 4TH STAGE CYLINDER"],
            ["AC-5515-1", "AGC 1ST STAGE INTERCOOLER"],
            ["AC-5545-1", "AGC 4TH STAGE INTERCOOLER"],
            ["V-5520-1", "AGC 2ND STAGE SCRUBBER"],
            ["V-5550-1", "AGC 5TH STAGE SCRUBBER"],
            ["C-5551-1", "AGC 5TH STAGE CYLINDER"],
            ["C-5521-1", "AGC 2ND STAGE CYLINDER"],
            ["AC-5555-1", "AGC AFTERCOOLER"],
            ["TK-5564-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["AC-5525-1", "AGC 2ND STAGE INTERCOOLER"],
            ["ACF-5580-1", "AIR COOLER FRAME"],
        ],
    },
    58: {
        "drawing": "PFD-235633-5700-003",
        "rows": [
            ["V-5725-1", "TEG FLASH DRUM"],
            ["F-5750-1", "TEG SOLIDS FILTER"],
            ["F-5760-1", "CHARCOAL FILTER"],
            ["E-5740-1/5742-1", "LEAN/RICH TEG EXCHANGERS"],
            ["T-5770-1", "TEG STRIPPING COLUMN"],
            ["V-5775-1", "TEG SURGE DRUM"],
            ["F-5755-1", "RICH TEG SOLIDS FILTER"],
            ["T-5793-1", "TEG STILL COLUMN"],
            ["V-5798-1", "TEG REGEN OVHDS SCRUBBER"],
            ["P-5798-1/5797-1", "TEG REGEN OVHDS PUMP"],
            ["P-5780-1/5781-1", "TEG PUMPS"],
            ["E-5790-1", "TEG REBOILER"],
            ["E-5793-1", "TEG REFLUX CONDENSER"],
            ["AC-5795-1", "TEG REGEN COOLER"],
        ],
    },
    61: {
        "drawing": "PFD-235633-5900-001",
        "rows": [
            ["F-5910-1/5920-1", "MOLE SIEVE INLET FILTER/COALESCER"],
        ],
    },
    62: {
        "drawing": "PFD-235633-6100-001",
        "rows": [
            ["V-6130-1/6140-1/6150-1", "MOLECULAR SIEVE DRIERS"],
            ["V-6160-1", "MERCURY REMOVAL UNIT"],
            ["F-6151-1", "MOLE SIEVE DUST FILTER"],
            ["F-6155-1", "MRU DUST FILTER"],
        ],
    },
    63: {
        "drawing": "PFD-235633-6100-002",
        "rows": [
            ["K-6190-1/6195-1", "REGEN GAS COMPRESSOR"],
            ["E-6170-1", "REGEN GAS EXCHANGER"],
            ["AC-6180-1", "REGEN GAS AIR COOLER"],
            ["V-6185-1", "REGEN GAS SCRUBBER"],
        ],
    },
    64: {
        "drawing": "PFD-235633-6200-001",
        "rows": [
            ["E-6210-1", "BAHX"],
            ["V-6230-1", "COLD SEPARATOR"],
            ["XT-6300-1/XK-6300-1", "EXPANDER / EXPANDER COMPRESSOR"],
        ],
    },
    71: {
        "drawing": "PFD-235633-6500-002",
        "rows": [
            ["E-6505-1", "DEBUTANIZER FEED/BOTTOMS EXCHANGER"],
            ["AC-6580-1", "DEBUTANIZER BOTTOMS COOLER"],
        ],
    },
    74: {
        "drawing": "PFD-235633-6700-003",
        "rows": [
            ["TK-6760-1", "FRESH CAUSTIC STORAGE TANK"],
            ["P-6760/6765-1", "FRESH CAUSTIC TRANSFER PUMPS"],
            ["TK-6780-1", "SPENT CAUSTIC STORAGE TANK"],
            ["TK-6770-1", "DSO STORAGE TANK"],
        ],
    },
    76: {
        "drawing": "PFD-235633-6800-002",
        "rows": [
            ["V-6830-1/6840-1", "LPG MOLECULAR SIEVE DRYER"],
            ["V-6850-1", "LPG MOLECULAR SIEVE DRYER"],
            ["E-6870-1", "LPG MS REGEN GAS EXCHANGER"],
        ],
    },
    77: {
        "drawing": "PFD-235633-6800-003",
        "rows": [
            ["AC-6880-1", "LPG MS REGEN GAS COOLER"],
            ["E-6870-1", "LPG MS REGEN GAS EXCHANGER"],
            ["V-6885-1", "LPG MS REGEN GAS SCRUBBER"],
        ],
    },
    78: {
        "drawing": "PFD-235633-6800-004",
        "rows": [
            ["E-6890-1", "DE-ETHANIZER BOTTOMS EXCHANGER"],
            ["AC-6895-1", "DE-ETHANIZER BOTTOMS AIR COOLER"],
        ],
    },
    79: {
        "drawing": "PFD-235633-6900-001",
        "rows": [
            ["V-6900-1", "INCINERATOR K.O. DRUM"],
            ["P-6900-1", "INCINERATOR K.O. DRUM TRANSFER PUMP"],
            ["FL-6920-1", "INCINERATOR"],
            ["B-6920-1", "INCINERATOR BLOWER"],
        ],
    },
    81: {
        "drawing": "PFD-235633-7200-001",
        "rows": [
            ["V-7210-1", "STABILIZER FLASH/FEED SEPARATOR"],
            ["ST-7260-1/7270-1", "STABILIZER FEED PUMP INLET STRAINER"],
            ["P-7260-1/7270-1", "STABILIZER FEED PUMPS"],
        ],
    },
    82: {
        "drawing": "PFD-235633-7200-002",
        "rows": [
            ["E-7240-1", "STABILIZER FEED/BOT EXCH."],
            ["AC-7250-1", "STABILIZER BOTTOMS COOLER"],
            ["T-7200-1", "STABILIZER"],
            ["E-7230-1", "STABILIZER REBOILER"],
        ],
    },
    84: {
        "drawing": "PFD-235633-7400-001",
        "rows": [
            ["V-7410-1", "STABILIZER FLASH/FEED SEPARATOR"],
            ["ST-7460-1/7470-1", "STABILIZER FEED PUMP INLET STRAINER"],
            ["P-7460-1/7470-1", "STABILIZER FEED PUMPS"],
        ],
    },
    87: {
        "drawing": "PFD-235633-7500-002",
        "rows": [
            ["TK-7564-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["P-7566-1", "VACUUM PUMP"],
            ["P-7564-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
            ["V-7510-1", "SOC 1ST STAGE SCRUBBER"],
            ["C-7511-1", "STABILIZER OVERHEAD COMPRESSOR 1ST STAGE CYLINDER"],
            ["AC-7515-1", "STABILIZER OVERHEAD COMPRESSOR 1ST STAGE INTERCOOLER"],
            ["V-7520-1", "SOC 2ND STAGE SCRUBBER"],
            ["C-7521-1", "STABILIZER OVERHEAD COMPRESSOR 2ND STAGE CYLINDER"],
            ["AC-7525-1", "STABILIZER OVERHEAD COMPRESSOR 2ND STAGE INTERCOOLER"],
            ["ACF-7550-1", "AIR COOLER FRAME"],
        ],
    },
    88: {
        "drawing": "PFD-235633-7500-003",
        "rows": [
            ["V-7530-1", "SOC 3RD STAGE SCRUBBER"],
            ["C-7531-1", "STABILIZER OVERHEAD COMPRESSOR 3RD STAGE CYLINDER"],
            ["AC-7535-1", "STABILIZER OVERHEAD COMPRESSOR 3RD STAGE INTERCOOLER"],
            ["V-7540-1", "SOC 4TH STAGE SCRUBBER"],
            ["C-7541-1", "STABILIZER OVERHEAD COMPRESSOR 4TH STAGE CYLINDER"],
            ["AC-7545-1", "STABILIZER OVERHEAD COMPRESSOR 4TH STAGE INTERCOOLER"],
            ["KM-7560-1", "STABILIZER OVERHEAD COMPRESSOR MOTOR"],
            ["K-7550-1", "RECIPROCATING GAS COMPRESSOR"],
        ],
    },
    89: {
        "drawing": "PFD-235633-7500-004",
        "rows": [
            ["TK-7664-1", "PACKING VENT/DRAIN SEPARATION POT"],
            ["P-7666-1", "VACUUM PUMP"],
            ["P-7664-1", "SEAL POT WASTE OIL TRANSFER PUMP"],
            ["V-7610-1", "SOC 1ST STAGE SCRUBBER"],
            ["C-7611-1", "STABILIZER OVERHEAD COMPRESSOR 1ST STAGE CYLINDER"],
            ["AC-7615-1", "STABILIZER OVERHEAD COMPRESSOR 1ST STAGE INTERCOOLER"],
            ["V-7620-1", "SOC 2ND STAGE SCRUBBER"],
            ["C-7621-1", "STABILIZER OVERHEAD COMPRESSOR 2ND STAGE CYLINDER"],
            ["AC-7625-1", "STABILIZER OVERHEAD COMPRESSOR 2ND STAGE INTERCOOLER"],
            ["ACF-7650-1", "AIR COOLER FRAME"],
        ],
    },
    90: {
        "drawing": "PFD-235633-7500-005",
        "rows": [
            ["V-7630-1", "SOC 3RD STAGE SCRUBBER"],
            ["C-7631-1", "STABILIZER OVERHEAD COMPRESSOR 3RD STAGE CYLINDER"],
            ["AC-7635-1", "STABILIZER OVERHEAD COMPRESSOR 3RD STAGE INTERCOOLER"],
            ["V-7640-1", "SOC 4TH STAGE SCRUBBER"],
            ["C-7641-1", "STABILIZER OVERHEAD COMPRESSOR 4TH STAGE CYLINDER"],
            ["AC-7645-1", "STABILIZER OVERHEAD COMPRESSOR 4TH STAGE INTERCOOLER"],
            ["KD-7620-1", "STABILIZER OVERHEAD COMPRESSOR DRIVER"],
            ["K-7620-1", "RECIPROCATING GAS COMPRESSOR"],
        ],
    },
    91: {
        "drawing": "PFD-235633-9000-001",
        "rows": [
            ["TK-9010-1/9020-1", "PRODUCED WATER STORAGE TANK"],
            ["H-9010-1/9020-1", "ELECTRIC HEATER"],
        ],
    },
}


def canonical_rows(system_name: str, drawing: str, rows: list[list[str]]) -> list[list[str]]:
    return [[equipment_number, equipment_name, system_name, drawing] for equipment_number, equipment_name in rows]


def main() -> int:
    parser = argparse.ArgumentParser(description="Recover known Deepcut multi-block header pages.")
    parser.add_argument("source_dir")
    parser.add_argument("--pdf-stem", default=PDF_STEM_DEFAULT)
    parser.add_argument("--report-csv")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2

    report_rows: list[dict[str, str]] = []
    updated = 0
    missing_pages: list[int] = []
    mismatched_drawings: list[int] = []

    for page_num in sorted(PAGE_FIXTURES):
        fixture = PAGE_FIXTURES[page_num]
        stub_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_stub.md"
        if not stub_path.is_file():
            missing_pages.append(page_num)
            continue

        parsed = parse_stub(stub_path, page_num)
        expected_drawing = str(fixture["drawing"])
        if parsed["drawing"] and parsed["drawing"] != expected_drawing:
            mismatched_drawings.append(page_num)
            continue

        source_pdf = str(parsed["source_pdf"])
        source_page = str(parsed["source_page"])
        extraction_mode = str(parsed["extraction_mode"])
        system_name = str(parsed["system_name"])
        before_rows = [row[:] for row in parsed["rows"] if row[0] or row[1] or row[3]]
        after_rows = canonical_rows(system_name, expected_drawing, fixture["rows"])  # type: ignore[arg-type]

        new_data = {
            "source_pdf": source_pdf,
            "source_page": source_page,
            "extraction_mode": extraction_mode,
            "drawing": expected_drawing,
            "system_name": system_name,
            "rows": after_rows,
            "status": "SUCCESS",
            "note": "Top-of-sheet equipment header normalized by deterministic Deepcut cleanup pass.",
        }

        rendered = render_stub(page_num, new_data)
        if stub_path.read_text(encoding="utf-8") != rendered:
            stub_path.write_text(rendered, encoding="utf-8")
            updated += 1

        report_rows.append(
            {
                "page": str(page_num),
                "drawing": expected_drawing,
                "system_name": system_name,
                "rows_before": str(len(before_rows)),
                "rows_after": str(len(after_rows)),
                "recovered_count": str(max(0, len(after_rows) - len(before_rows))),
            }
        )

    if args.report_csv:
        report_path = Path(args.report_csv).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with report_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["page", "drawing", "system_name", "rows_before", "rows_after", "recovered_count"],
            )
            writer.writeheader()
            writer.writerows(report_rows)

    print(f"updated={updated}")
    print(f"missing_pages={','.join(str(page) for page in missing_pages) or 'none'}")
    print(f"mismatched_drawings={','.join(str(page) for page in mismatched_drawings) or 'none'}")
    if args.report_csv:
        print(f"report={Path(args.report_csv).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
