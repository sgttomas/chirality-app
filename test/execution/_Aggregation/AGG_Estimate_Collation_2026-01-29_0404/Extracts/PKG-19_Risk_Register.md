# Risk Register

## Snapshot: EST_PKG19_DRAFT_2026-01-28_0015

This register identifies cost risks affecting PKG-19 Control Systems estimate.

---

## Risks

### R-001: Control System Vendor Selection

| Field | Value |
|-------|-------|
| ID | R-001 |
| Risk Driver | Price uncertainty |
| Cause | Vendor pricing varies significantly (+/- 20-30%) based on platform selection (DCS vs. PLC, tier) |
| Consequence | Material costs could be higher or lower than estimated |
| Affected CBS | MAT |
| Affected WBS | PKG-19 (all equipment) |
| Suggested Mitigation | Obtain budgetary quotes from 2-3 qualified vendors early in design |
| Contingency Handling | 25% contingency on MAT partially covers this uncertainty |

---

### R-002: I/O Count Growth

| Field | Value |
|-------|-------|
| ID | R-002 |
| Risk Driver | Quantity uncertainty |
| Cause | I/O point count estimated without final instrumentation design (PKG-20) |
| Consequence | Additional I/O modules, larger cabinets, more wiring required |
| Affected CBS | MAT, CD |
| Affected WBS | PKG-19 (I/O system) |
| Suggested Mitigation | Complete PKG-20 instrumentation design before finalizing control system scope |
| Contingency Handling | 25-30% contingency on MAT/CD partially covers growth |

---

### R-003: Software Development Scope Expansion

| Field | Value |
|-------|-------|
| ID | R-003 |
| Risk Driver | Scope uncertainty |
| Cause | Control strategies and HMI requirements not fully defined |
| Consequence | Software development hours increase; HMI graphics count increases |
| Affected CBS | E |
| Affected WBS | DEL-19.04 (Control System Software) |
| Suggested Mitigation | Define control narratives and HMI screen list before vendor award |
| Contingency Handling | 20% contingency on E covers moderate scope growth |

---

### R-004: Safety Instrumented System (SIS) Requirement

| Field | Value |
|-------|-------|
| ID | R-004 |
| Risk Driver | Scope uncertainty |
| Cause | HAZOP (PKG-27) not complete; SIL requirements unknown |
| Consequence | Separate SIS could add $200,000-400,000 to scope |
| Affected CBS | MAT, E, CD |
| Affected WBS | PKG-19 (if SIS added to scope) |
| Suggested Mitigation | Complete HAZOP early to identify SIS requirements |
| Contingency Handling | **NOT COVERED** — SIS is a scope exclusion; would require scope change if required |

---

### R-005: Cybersecurity Requirements

| Field | Value |
|-------|-------|
| ID | R-005 |
| Risk Driver | Scope uncertainty |
| Cause | Employer cybersecurity requirements not defined |
| Consequence | Additional firewalls, segmentation, compliance documentation |
| Affected CBS | MAT, E |
| Affected WBS | PKG-19 (network infrastructure) |
| Suggested Mitigation | Clarify cybersecurity requirements with Employer |
| Contingency Handling | 25% contingency on MAT partially covers additional equipment |

---

### R-006: Historian Platform Selection

| Field | Value |
|-------|-------|
| ID | R-006 |
| Risk Driver | Price uncertainty |
| Cause | OSIsoft PI vs. vendor-integrated historian varies significantly in cost |
| Consequence | OSIsoft PI could add $50,000-100,000 vs. estimate |
| Affected CBS | MAT |
| Affected WBS | PKG-19 (historian) |
| Suggested Mitigation | Confirm historian platform requirement with Employer |
| Contingency Handling | 25% contingency on MAT partially covers |

---

### R-007: Control Room Integration

| Field | Value |
|-------|-------|
| ID | R-007 |
| Risk Driver | Interface uncertainty |
| Cause | MCC building design (PKG-21/22) not complete; control room layout TBD |
| Consequence | Late changes to cabinet layout, cable routing, HVAC requirements |
| Affected CBS | CD, CI |
| Affected WBS | PKG-19 (installation) |
| Suggested Mitigation | Coordinate early with building design team |
| Contingency Handling | 30% contingency on CD/CI covers moderate rework |

---

### R-008: Vendor FAT Location

| Field | Value |
|-------|-------|
| ID | R-008 |
| Risk Driver | Price uncertainty |
| Cause | FAT location not defined; may require travel outside BC |
| Consequence | Travel and per diem costs for FAT attendance |
| Affected CBS | COM |
| Affected WBS | PKG-19 (commissioning) |
| Suggested Mitigation | Specify local FAT capability in vendor selection criteria |
| Contingency Handling | 30% contingency on COM covers moderate travel cost |

---

### R-009: Integration with Existing Terminal Systems

| Field | Value |
|-------|-------|
| ID | R-009 |
| Risk Driver | Interface uncertainty |
| Cause | Interface requirements with existing Terminal control systems unclear |
| Consequence | Additional integration effort, protocol converters, testing |
| Affected CBS | MAT, E, COM |
| Affected WBS | PKG-19 |
| Suggested Mitigation | Define Terminal interface requirements early (PKG-34) |
| Contingency Handling | Overall contingency partially covers |

---

### R-010: Network Infrastructure Complexity

| Field | Value |
|-------|-------|
| ID | R-010 |
| Risk Driver | Scope uncertainty |
| Cause | Network architecture not designed; fiber runs, switch counts estimated |
| Consequence | Longer cable runs, more switches, complex routing |
| Affected CBS | MAT, CD |
| Affected WBS | PKG-19 (network infrastructure) |
| Suggested Mitigation | Complete network architecture design early |
| Contingency Handling | 25-30% contingency on MAT/CD covers moderate growth |

---

## Risk Summary

| ID | Risk | Probability | Impact | Priority |
|----|------|-------------|--------|----------|
| R-001 | Vendor selection pricing | HIGH | MEDIUM | HIGH |
| R-002 | I/O count growth | MEDIUM | MEDIUM | MEDIUM |
| R-003 | Software scope expansion | MEDIUM | MEDIUM | MEDIUM |
| R-004 | SIS requirement added | MEDIUM | HIGH | HIGH |
| R-005 | Cybersecurity requirements | MEDIUM | LOW | MEDIUM |
| R-006 | Historian platform | MEDIUM | LOW | LOW |
| R-007 | Control room integration | LOW | MEDIUM | LOW |
| R-008 | FAT location travel | LOW | LOW | LOW |
| R-009 | Terminal system integration | MEDIUM | MEDIUM | MEDIUM |
| R-010 | Network complexity | MEDIUM | LOW | LOW |

---

## Contingency Allocation

| CBS | Base Amount | Contingency % | Contingency | Risk Coverage |
|-----|-------------|---------------|-------------|---------------|
| E | $240,000 | 20% | $48,000 | R-003 (software scope) |
| MAT | $920,000 | 25% | $230,000 | R-001, R-002, R-005, R-006, R-010 |
| CD | $380,000 | 30% | $114,000 | R-002, R-007, R-010 |
| CI | $68,000 | 30% | $20,000 | R-007 |
| PM | $120,000 | 15% | $18,000 | General |
| P | $18,000 | 15% | $3,000 | General |
| COM | $55,000 | 30% | $17,000 | R-008, R-009 |
| **Total** | **$1,801,000** | **25.0%** | **$450,000** | |

---

## Unmitigated Risks (Outside Contingency)

| Risk | Potential Impact | Notes |
|------|------------------|-------|
| R-004: SIS requirement | +$200,000 to +$400,000 | Scope exclusion; would be scope change |
| Major scope change | Variable | Changes beyond 30% growth not covered |
