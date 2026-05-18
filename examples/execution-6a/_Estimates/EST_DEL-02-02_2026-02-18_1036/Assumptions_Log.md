# Assumptions Log: EST_DEL-02-02_2026-02-18_1036

## Quantity Assumptions

| AssumptionID | Assumption | Source/Rationale | Impact if Wrong |
|---|---|---|---|
| ASM-001 | Each apparatus bay area = 2,100 sf (195 m2). Total 4 bays = 8,400 sf (780 m2). | Midpoint of 2,000-2,200 sf range per Addendum 03 s1.21 and Datasheet. | +/- 5% on bay floor/ceiling lines (~$2,200 variance on $44,460 total) |
| ASM-002 | Decontamination area total = 285 sf (26.5 m2): decon room 175 sf (midpoint 150-200) + 2x shower/WR at 55 sf each (midpoint 50-60). | Midpoints of Functional Program ranges per Addendum 03 s1.21. | +/- 15% on decon fit-up lines (~$3,400 variance on $22,487 total) |
| ASM-003 | Compressed air distribution piping allowance = $20,000 for routing from compressor room to 4 apparatus bays with ceiling-mounted drops. | Typical municipal fire station compressed air distribution for 4 bays. No detailed routing available. Range estimate $15,000-$25,000; midpoint used. | +/- 25% ($5,000 variance) |
| ASM-004 | Bunker gear locker room area = 450 sf (41.8 m2), midpoint of 350-550 sf Duty Gear Room range. Partition wall area ~30 m2. | Addendum 03 s1.21. Locker room mapped to Duty Gear Room per CF-0202-02 proposal. | +/- 20% on room fit-up lines (~$1,900 variance on $9,545 total) |
| ASM-005 | Fire gear storage room area = 275 sf (25.5 m2), midpoint of 200-350 sf range. Partition wall area ~20 m2. | Addendum 03 s1.21. | +/- 25% on room fit-up lines (~$1,800 variance on $7,187 total) |
| ASM-006 | SCBA/cascade room area = 175 sf (16.3 m2), midpoint of 150-200 sf range. Partition wall area ~18 m2. | Addendum 03 s1.21. | +/- 15% on room fit-up lines (~$700 variance on $4,874 total) |
| ASM-007 | Compressor room area = 125 sf (11.6 m2), midpoint of 100-150 sf range. Fire-rated partitions assumed due to compressor equipment. Partition wall area ~16 m2. | Addendum 03 s1.21. Fire rating is an assumption (compressor rooms typically require fire separation). | +/- 20% on room fit-up lines (~$1,100 variance on $5,269 total) |
| ASM-008 | Medical/EMS storage room area = 60 sf (5.6 m2), midpoint of 50-70 sf range. Partition wall area ~10 m2. | Addendum 03 s1.21. | +/- 15% on room fit-up lines (~$600 variance on $4,057 total) |

## Rate Assumptions

| AssumptionID | Assumption | Source/Rationale | Impact if Wrong |
|---|---|---|---|
| ASM-009 | Bunker gear locker unit rate = $2,200 each (midpoint of $1,800-$2,500 range). | Equipment_Pricing.csv / EQ-06. Heavy-duty ventilated fire service lockers. | +/- $12,000 at 40 units ($3,200 variance per $400 rate change x 40 units = max $12,000) |
| ASM-010 | Breathing air compressor system = $55,000 (midpoint of $45,000-$65,000 range). | Equipment_Pricing.csv / EQ-08 and Mechanical_System_Rates.csv / MS-08. Both sources consistent. | +/- $10,000 based on system selection |
| ASM-011 | Bay sump assemblies = $4,500 each. | Mechanical_System_Rates.csv / MS-10 and Equipment_Pricing.csv / EQ-10. Recommended rate. | +/- $1,000/unit ($4,000 total at 4 units) |
| ASM-012 | Interior doors priced as composite: BE-11 ($1,800 HM door + frame) + BE-13 ($600 hardware set) = $2,400 per opening. | Building_Envelope_Rates.csv. Combined for complete opening. | +/- $400/opening ($2,800 total at 7 openings) |

## Design Assumptions

| AssumptionID | Assumption | Source/Rationale | Impact if Wrong |
|---|---|---|---|
| ASM-013 | Decon area partitions are wet-area type (cement board + moisture-resistant GWB) at IA-04 rate. | Decon function involves water/chemical exposure. IA-04 is the appropriate rate for wet areas. | If standard partitions used instead, cost decreases ~$3,000 |
| ASM-014 | Compressor room requires 1-hour fire-rated partitions. | Industry practice for rooms housing mechanical compressor equipment. Not explicitly stated in source documents. | If non-rated partitions acceptable, cost decreases ~$500 |
| ASM-015 | SCBA room and compressor room have exposed ceilings (paint only) for equipment access. Other support rooms have ACT ceilings. | Practical consideration: mechanical equipment rooms benefit from exposed ceiling access. | Cost impact minimal (~$300 if ceiling type changes) |
| ASM-016 | Apparatus bay ceilings receive exposed structure paint (spray-apply latex) per IA-07. | Standard practice for fire station apparatus bays; provides finished appearance without concealing structure. Consistent with IA-07 description. | If no ceiling finish required, saves $17,160 |
| ASM-017 | 7 hollow metal doors total for fire support rooms: 2 for decon area, 1 for bunker gear locker room, 1 for fire gear storage, 1 for SCBA room, 1 for compressor room, 1 for medical/EMS storage. | Derived from room count. Each room requires at minimum 1 access door. Decon area has 2 (entry + shower/WR access). | +/- 1-2 doors ($2,400-$4,800 variance) |
