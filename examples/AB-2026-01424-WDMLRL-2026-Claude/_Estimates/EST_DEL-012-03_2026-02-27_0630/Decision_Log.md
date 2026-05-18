# Decision Log — EST_DEL-012-03_2026-02-27_0630

## Defaults Applied

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-001 | Rounding set to NONE (default) | No ROUNDING parameter provided in brief; default applied per protocol |
| DEC-002 | OUTPUT_LABEL set to DEL-012-03 | Provided in brief |

## Scope Resolution

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-008 | Scope resolved to single deliverable DEL-012-03 in PKG-012 | SCOPE=DEL-012-03 in brief; confirmed via decomposition and deliverable path |

## Pricing Derivations

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-003 | Interior door priced at $1,200 LS (parametric) | No door unit rate in PRICE_SOURCES. Derived parametrically: standard interior commercial door ($600 supply) + frame/hardware ($300) + installation labour ~4 hr x $80.60/hr ($322) rounded to $1,200. Confidence: LOW |
| DEC-004 | Electrical items (receptacles, lighting, data outlets) priced using composite parametric derivation from Construction_Labour_Rates.csv | No electrical device unit rates in PRICE_SOURCES. Receptacles: material ~$45/EA + 1.5 hr x $92.80/hr (T-05 plumber proxy for electrician, noting T-04 electrician at $96/hr also available; used blended approach). Lighting: fixture ~$350 + 3 hr install x $96/hr. Data: material ~$60/EA + 2 hr x $96/hr. Confidence: LOW |
| DEC-005 | HVAC coordination allowance priced at $750 LS | No HVAC coordination rate in PRICE_SOURCES. Derived: ~8 hr carpenter labour x $80.60/hr ($645) + materials (~$100) rounded to $750. Covers framing/blocking around HVAC penetrations. Confidence: LOW |
| DEC-006 | Accessibility features priced at $500 LS | No accessibility hardware rate in PRICE_SOURCES. Derived: lever door hardware set (~$200) + barrier-free threshold (~$100) + minor framing labour ~2.5 hr x $80.60/hr (~$200). Confidence: LOW |
| DEC-007 | Safety/life safety features priced at $800 LS | No safety fixture rate in PRICE_SOURCES. Derived: illuminated exit sign (~$150) + emergency light unit (~$300) + fire extinguisher bracket (~$50) + install labour ~3 hr x $96/hr (~$288) rounded to $800. Confidence: LOW |

## Fallback Uses

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-009 | DL-018 (millwork) priced as ALLOWANCE method instead of PARAMETRIC | Interior_Architectural_Rates.csv IA-05 is explicitly classified as ALLOWANCE basis. ALLOW_MIXED_METHODS=TRUE permits this. Logged per FALLBACK_POLICY=ALLOW_PARAMETRIC |

## Method Mix

| Method | Count | % |
|---|---|---|
| PARAMETRIC | 22 | 95.7% |
| ALLOWANCE | 1 | 4.3% |

Basis consistency: 95.7% of lines match BASIS_OF_ESTIMATE (PARAMETRIC). The single ALLOWANCE line is permitted by ALLOW_MIXED_METHODS=TRUE and logged as DEC-009.
