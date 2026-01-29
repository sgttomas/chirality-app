# Risk Register

## PKG-11 Marine Loading System Estimate

| ID | Risk Driver | Cause → Consequence | Affected CBS/WBS | Suggested Mitigation | Contingency Handling |
|----|-------------|---------------------|------------------|---------------------|---------------------|
| R-001 | Equipment - Loading Arm Pricing | No OEM quotes → Loading arm price highly uncertain ($800k-$1.5M range) | MAT / PKG-11 | Obtain budgetary quotes from 2-3 OEMs early | 25% contingency on MAT |
| R-002 | Scope - Arm Configuration | Arm type undefined (single vs dual, reach, ERC type) → May require more expensive configuration | MAT / PKG-11 | Confirm design vessel data and loading envelope requirements | MAT contingency |
| R-003 | Scope - Pipe Routing | No layout drawings → Double-walled pipe length may vary significantly | MAT, CD / PKG-11 | Complete DEL-11.01 with pipe routing | 25-30% contingency on pipe items |
| R-004 | Price - No Quotes | No vendor quotes for any items → All pricing via allowances with high uncertainty | All CBS | Obtain budgetary quotes for major items | Elevated contingency on all buckets |
| R-005 | Interface - PKG-08 | Loading arm foundation design → Foundation capacity, embedment, and marine loads | CD interface | Coordinate with PKG-08 for foundation requirements early | Foundation in PKG-08 scope |
| R-006 | Interface - Marine Access | Marine work logistics → May require crane barge, tug assist, weather windows | CD, CI / PKG-11 | Develop installation methodology in DEL-11.01 | Marine logistics premium in CI |
| R-007 | Technical - Vessel Envelope | Unknown design vessel data → Loading arm reach/slew may need revision | MAT, E / PKG-11 | Obtain design vessel manifold data; complete DEL-11.03 calculations | Design contingency |
| R-008 | Schedule - Long Lead | Loading arm is long-lead equipment (6-12 months) → May impact project schedule | MAT / PKG-11 | Early procurement planning; DEL-11.06 qualification | Schedule risk (not costed) |
| R-009 | Interface - PKG-19 | ESD/control integration → Complex safety system interfaces | CD, COM / PKG-11 | Early coordination with PKG-19 for signal lists and ESD logic | Commissioning contingency |
| R-010 | Commissioning - Complexity | Marine loading commissioning complexity → Extended testing and vendor support | COM / PKG-11 | Plan for OEM commissioning support; FAT witnessing | 30% contingency on COM |
| R-011 | Environmental - Weather | Marine work weather-dependent → Schedule delays possible | CD, CI / PKG-11 | Schedule marine work in optimal weather windows | CI factor includes weather |
| R-012 | Quality - Specialty Work | Double-walled pipe and loading arm are specialty items → Limited qualified contractors | CD / PKG-11 | Pre-qualify specialty contractors | Contractor premium in rates |
| R-013 | Regulatory - Marine Terminal | Marine terminal safety/regulatory requirements → May require additional features | E, MAT / PKG-11 | Review Transport Canada and Vancouver Fraser Port Authority requirements | Design contingency |

## Contingency Summary

| CBS | Base Amount | Contingency % | Contingency $ | Rationale |
|-----|-------------|---------------|---------------|-----------|
| E | $125,000 | 20% | $25,000 | All allowances; scope definition risk |
| MAT | $1,485,000 | 25% | $371,000 | All allowances; loading arm price uncertainty; equipment selection |
| CD | $595,000 | 30% | $179,000 | Marine installation complexity; specialty work; weather risk |
| CI | $107,000 | 30% | $32,000 | Factor-based from CD; marine coordination |
| PM | $119,000 | 15% | $18,000 | Factor-based |
| P | $30,000 | 15% | $5,000 | Factor-based |
| COM | $79,000 | 30% | $24,000 | Commissioning complexity; OEM coordination; ESD integration |
| **TOTAL** | **$2,540,000** | **25.7%** | **$654,000** | Weighted average |

## Contingency Method

**Method:** PCT_BY_BUCKET with allowance adjustment per fallback typical model

**Basis:**
- All line items are allowances (100% allowance-based estimate)
- Per fallback model: +10% above baseline contingency for buckets with ≥80% allowance share
- Loading arm is single largest cost element (~37% of base) with significant price uncertainty
- Marine work inherently has higher uncertainty than land-based construction
- Applied across all CBS buckets due to LOW confidence level
