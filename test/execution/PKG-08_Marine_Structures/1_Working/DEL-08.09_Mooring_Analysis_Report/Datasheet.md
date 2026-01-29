# Datasheet: DEL-08.09 Mooring Analysis Report

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-08.09 |
| Name | Mooring Analysis Report |
| Package | PKG-08 Marine Structures |
| Discipline | Marine |
| Type | Report |
| Responsible | D&B Contractor |
| Lifecycle State | INITIALIZED |

## Description

**Purpose:** Documents analysis and results for mooring analysis report required for design verification and approvals. *(Source: Decomposition line 289)*

**Report objective:** Analyzes forces in mooring lines and fenders when design vessels are moored under environmental conditions, verifying mooring arrangement adequacy and line loads within acceptable limits.

## Minimum Artifact Content

*(Source: Decomposition line 289)*

| Artifact | Status |
|---|---|
| Mooring analysis report | Required |
| Vessel assumptions | Required |
| Line loads | Required |
| Acceptance criteria | Required |

## Report Metadata (TBD)

| Attribute | Value |
|---|---|
| Report number | **TBD** |
| Design vessel(s) | **TBD** *(from ER)* |
| Environmental conditions | **TBD** *(wind, current, wave)* |
| Analysis method | **TBD** *(static/dynamic, software)* |

## Design Vessel Parameters (TBD)

| Parameter | Value | Status |
|---|---|---|
| Vessel type | **TBD** | Required |
| DWT / displacement | **TBD** | Required |
| LOA / beam / draft | **TBD** m | Required |
| Windage area (laden) | **TBD** m² | Required |
| Windage area (ballast) | **TBD** m² | Required |
| Freeboard (laden/ballast) | **TBD** m | Required |

## Environmental Conditions (TBD)

| Condition | Value | Source | Status |
|---|---|---|---|
| Design wind speed | **TBD** m/s | ER/metocean | Required |
| Wind direction(s) | **TBD** | ER | Required |
| Design current velocity | **TBD** m/s | DEL-08.10 | Required |
| Current direction(s) | **TBD** | DEL-08.10 | Required |
| Wave (if applicable) | **TBD** | ER/metocean | If applicable |
| Water level | **TBD** | ER | Required |

## Mooring Arrangement (TBD)

| Parameter | Value | Status |
|---|---|---|
| Number of lines | **TBD** | Required |
| Line configuration | **TBD** *(breast, spring, head, stern)* | Required |
| Mooring hook capacity | **TBD** kN | Required |
| Line type/MBL | **TBD** | Required |
| Bollard spacing | **TBD** m | Required |

## Interfaces (Advisory)

*Dependencies NOT_TRACKED:*

| Related Deliverable | Interface |
|---|---|
| DEL-08.10 Current Assessment | Input: current data |
| DEL-08.06 Berthing Energy | Shared vessel particulars |
| DEL-08.03 Structures Calculations | Output: mooring loads |
| PKG-09 Marine Outfitting | Mooring equipment specs |

## Key TBDs

1. ER clauses for mooring analysis methodology and criteria
2. Design vessel particulars
3. Metocean data (wind, current, wave)
4. Mooring arrangement assumptions

## Sources

- Decomposition line 289
- ER Vol 2 Parts 1-2 *(TBD)*
