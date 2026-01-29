# Guidance: DEL-35.01 Training Materials

## Purpose

This guidance document supports the development of **Training Materials** for **PKG-35 Training & Handover**.

**Deliverable purpose:** Provides project management/control documentation for training materials required by the Employer's Requirements.

*Source: _CONTEXT.md, Decomposition Section 5 (PKG-35, DEL-35.01)*

**Deliverable classification:**
- **Type**: Document
- **Discipline**: Project Delivery
- **Responsible party**: D&B Contractor (with OEM/Supplier)

*Source: _CONTEXT.md*

**Project context:**
- **Project**: Canola Oil Transload Facility — Phase 1 (Design & Build)
- **Employer**: DP World Fraser Surrey Inc.
- **Location**: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Facility capacity**: 1,000,000 MT/annum throughput, 45,000 MT storage

*Source: Decomposition Section 1 (Project Context)*

## Principles

### Engineering Rationale

**Principle 1: Lifecycle Cost Optimization (OBJ-9)**

Training materials directly support **OBJ-9: Lifecycle Cost Optimization** by minimizing future operating and maintenance costs through effective knowledge transfer.

*Source: Decomposition Section 2 (Project Objectives), Section 6 (Objective-to-Deliverable Mapping showing DEL-35.01 supports OBJ-9)*
*See Specification.md requirement PR-04 for specific performance criteria related to lifecycle cost optimization.*

**How training materials contribute to lifecycle cost optimization:**
- **Reduced operating errors**: Well-trained operators make fewer mistakes, reducing product loss, equipment damage, and safety incidents
- **Improved maintenance effectiveness**: Clear maintenance procedures enable in-house maintenance, reducing reliance on external contractors
- **Faster troubleshooting**: Comprehensive troubleshooting guides minimize downtime when issues occur
- **Knowledge retention**: Documented procedures preserve institutional knowledge when personnel turnover occurs
- **Training efficiency**: Self-contained training materials enable efficient onboarding of new staff without external training courses
- **Regulatory compliance**: Proper training documentation supports compliance with occupational health and safety regulations, avoiding fines and work stoppages

*Source: **ASSUMPTION** — rationale for how training supports OBJ-9*

**Principle 2: Safe and Reliable Operation (OBJ-1)**

Training materials support **OBJ-1: Safe & Reliable Operation** by ensuring facility personnel are competent to operate and maintain systems safely and reliably.

*Source: Decomposition Section 2 (OBJ-1)*

**Safety and reliability considerations:**
- Personnel must understand process hazards (hot oil, confined spaces, spill risks)
- Personnel must be competent in emergency response procedures
- Personnel must understand safety interlocks and when manual overrides are appropriate
- Personnel must follow proper startup/shutdown sequences to avoid equipment damage
- Personnel must understand custody transfer procedures to ensure accurate measurement (supports OBJ-10)

*Source: **ASSUMPTION** — safety principles for bulk liquid terminal operations*

**Principle 3: Integration of OEM Expertise**

The Contractor shall coordinate with OEM/suppliers to leverage their equipment expertise while integrating it into a comprehensive facility training program.

*Source: _CONTEXT.md (Responsible: D&B Contractor with OEM/Supplier)*

**Rationale for OEM integration:**
- OEMs provide equipment-specific operational and maintenance knowledge
- OEMs provide troubleshooting expertise based on field experience
- OEMs provide warranty requirements and recommended practices
- Contractor integrates OEM content with facility-specific procedures and context
- Contractor ensures consistency across multiple OEM materials

*Source: **ASSUMPTION** — typical Design & Build approach to training development*

### Applicable Standards Context

**Quality Management:**
- **ISO 9001:2015** — Establishes framework for quality management in training material development, including document control, competence requirements, and continual improvement
  *Source: **ASSUMPTION** — typical project quality standard*

**Health, Safety, and Environmental:**
- **ISO 45001:2018** — Requires training as a key control for occupational health and safety risks; training materials demonstrate compliance with legal and regulatory requirements
- **ISO 14001:2015** — Requires environmental awareness training; training materials address spill prevention, containment, and response
  *Source: **ASSUMPTION** — applicable to bulk liquid terminal operations*

**Industry Best Practice:**
- **ANSI/API RP 75** — Provides guidance on safety and environmental management systems for onshore plants, including training program requirements
- **ISGOTT (International Safety Guide for Oil Tankers and Terminals)** — **ASSUMPTION**: May apply to marine loading operations training; **TBD**: Confirm applicability to canola oil operations
  *Source: **ASSUMPTION** — industry standards for bulk liquid terminals*

**Canadian Regulatory Context:**
- **TBD** — Occupational health and safety training requirements (federal and BC provincial)
- **TBD** — Environmental protection training requirements
- **TBD** — Transportation of dangerous goods training (if canola oil classified as such)
- **TBD** — Marine terminal safety regulations

*Source: **ASSUMPTION** — regulatory framework requires confirmation*

## Considerations

### Factors to Consider During Development

**Consideration 1: Target Audience Competency Levels**

Training materials must address diverse competency levels:
- **Entry-level operators**: Assume limited prior knowledge of bulk liquid terminal operations; provide foundational training
- **Experienced operators**: Provide facility-specific procedures and differences from other terminals
- **Maintenance technicians**: Assume trade qualifications but provide equipment-specific training
- **Supervisors/managers**: Provide operational overview and emergency response leadership training
- **Occasional users**: QA/QC inspectors, engineering staff — provide focused training on their specific interactions with the facility

*Source: **ASSUMPTION** — typical workforce diversity at industrial facilities*

**Strategy**: Develop modular training materials that can be tailored to audience needs. Separate foundational content from advanced content.

**Consideration 2: Training Timing and Facility Readiness**

Training material development must align with project schedule:
- **Preliminary training materials**: Based on design documentation (30%, 60%, 90%, IFC stage gates)
- **Draft training materials**: Incorporate construction modifications and as-built changes
- **Final training materials**: Updated post-commissioning to reflect operational learnings

*Source: **ASSUMPTION** — typical training material development progression during Design & Build project*

**Challenge**: Training materials must be substantially complete for pre-startup training, but final refinements require operational experience.

**Strategy**: Plan for training material updates during commissioning phase. Issue preliminary version for initial training, with final version issued at handover (DEL-35.03).

**Consideration 3: Integration with Other Deliverables**

Training materials must integrate content from multiple packages:

**Upstream dependencies (content sources):**
- **PKG-19 Control Systems**: Control system architecture, HMI operation, alarm management
- **PKG-27 Operations Management**: Operating procedures, standard operating procedures (SOPs)
- **PKG-31 Maintenance & Asset Management**: Maintenance procedures, preventive maintenance schedules
- **PKG-32 Health, Safety & Environmental Management**: Safety procedures, environmental procedures, permit-to-work
- **PKG-33 Emergency Response Planning**: Emergency response procedures, evacuation procedures, spill response
- Equipment packages (PKG-10, 11, 13, 14, 15, 16): Equipment-specific OEM manuals

*Source: **ASSUMPTION** based on package scope; see _DEPENDENCIES.md for coordination mode (NOT_TRACKED)*

**Coordination challenge**: Training material development depends on maturity of upstream deliverables. Incomplete upstream deliverables create TBDs in training content.

**Strategy**: Coordinate with package leads to obtain draft versions of key documents. Flag dependencies early in project schedule. Use placeholders with clear TBD markers where upstream content is not yet available.

**Consideration 4: Terminal Continuity (OBJ-5)**

Training must consider the operational context: Fraser Surrey Terminal is an active marine terminal, and Phase 1 construction must minimize disturbance to existing terminal operations.

*Source: Decomposition Section 2 (OBJ-5)*

**Training implications:**
- Personnel may already be familiar with terminal access, security, and general site procedures
- Training materials should differentiate new Phase 1 procedures from existing terminal procedures
- **ASSUMPTION**: Some trainees may be existing terminal personnel; avoid redundant training on terminal-wide procedures

*Source: **ASSUMPTION** — inference from OBJ-5*

**Consideration 5: Future Expandability (OBJ-8)**

The design facilitates Phase 2 expansion. Training materials should note expansion provisions and avoid creating training content that would require major rework for Phase 2.

*Source: Decomposition Section 2 (OBJ-8)*

**Training implications:**
- Identify where systems are designed with expansion capacity (e.g., control system I/O, electrical load centers)
- Avoid hardcoding assumptions that would change in Phase 2 (e.g., "the facility has three tanks" when Phase 2 may add more)
- Structure training to facilitate future updates

*Source: **ASSUMPTION** — inference from OBJ-8*

**Consideration 6: Custody Transfer Accuracy (OBJ-10)**

Training materials must ensure personnel are competent in custody transfer procedures to support **OBJ-10: Custody Transfer Accuracy**.

*Source: Decomposition Section 2 (OBJ-10)*

**Training requirements:**
- Metering system operation and calibration
- Meter proving procedures
- Data recording and reporting
- Custody transfer documentation
- Troubleshooting metering issues

*Source: **ASSUMPTION** — typical custody transfer training topics*

**Consideration 7: Language and Cultural Factors**

**TBD** — Confirm workforce demographics and language requirements.

**Potential considerations:**
- Multiple language versions if workforce includes non-English speakers
- Use of visuals, diagrams, and photos to transcend language barriers
- Simplified language for non-native speakers
- Cultural considerations in safety training (risk perception, communication styles)

*Source: **ASSUMPTION** — common consideration for industrial training programs*

**Consideration 8: Format and Delivery Media**

Training material format affects usability and maintenance:

**Format options:**
- **Printed manuals**: Durable for field reference, but updates are costly
- **Electronic documents (PDF)**: Easily distributed and searchable, but require access to computers/tablets
- **Presentations (PowerPoint)**: Good for classroom instruction, editable for updates
- **Videos/multimedia**: Effective for procedural training, but expensive to produce and update
- **E-learning modules**: Enable self-paced learning and tracking, but require development investment

*Source: **ASSUMPTION** — typical training media options*

**Strategy**: Use multiple formats. Written manuals for reference and detailed procedures. Presentations for classroom sessions. Videos for specific high-value procedures (e.g., loading arm connection). **TBD** — Confirm format preferences with Employer.

## Trade-offs

### Competing Concerns to Evaluate

**Trade-off 1: Comprehensiveness vs. Usability**

**Competing concerns:**
- **Comprehensiveness**: Training materials should cover all systems and procedures in detail to ensure completeness
- **Usability**: Excessively long or detailed materials overwhelm trainees and are difficult to navigate

**Evaluation factors:**
- Trainee attention span and learning capacity
- Time available for training before facility startup
- Future use as reference materials vs. initial learning

**Approach**:
- Provide tiered content: Overview/summary content for initial learning, detailed content for reference
- Use modular structure: Trainees can focus on relevant modules
- Provide quick reference guides/checklists for common procedures
- Reserve comprehensive detail for troubleshooting sections and appendices

*Source: **ASSUMPTION** — typical training material design challenge*

**Trade-off 2: Early Completion vs. Accuracy**

**Competing concerns:**
- **Early completion**: Training materials needed early for pre-startup training
- **Accuracy**: Training materials must reflect as-built conditions, which are not fully known until construction completion

**Evaluation factors:**
- Project schedule constraints (training must occur before commissioning)
- Risk of training personnel on incorrect procedures (safety and operational risks)
- Cost of re-training if materials require major corrections

**Approach**:
- Develop preliminary materials based on IFC (Issued for Construction) design documents
- Implement structured review and update process during construction and commissioning
- Flag known variances between design and as-built status
- Plan for training material updates and re-training/refresher sessions post-commissioning

*Source: **ASSUMPTION** — typical Design & Build training material timing challenge*

**Trade-off 3: Generic Content vs. Facility-Specific Content**

**Competing concerns:**
- **Generic content**: Incorporate OEM manuals and industry best practices (lower cost, leverages existing content)
- **Facility-specific content**: Tailor all content to this specific facility (higher quality, but higher development cost)

**Evaluation factors:**
- Budget and schedule for training material development
- Availability of quality OEM training materials
- Criticality of facility-specific context (unique equipment, specific procedures, site-specific hazards)

**Approach**:
- Use OEM materials as foundation for equipment-specific training
- Supplement OEM materials with facility-specific operating context, procedures, and integration information
- Develop original facility-specific content for systems integration, startup/shutdown sequences, and site-specific safety procedures
- Clearly differentiate OEM content from Contractor-developed content for future maintenance

*Source: **ASSUMPTION** — typical approach balancing cost and quality; aligns with Responsible party: D&B Contractor with OEM/Supplier per _CONTEXT.md*

**Trade-off 4: Training Material Depth vs. Development Schedule**

**Competing concerns:**
- **Depth**: Detailed, high-quality training materials support OBJ-9 (lifecycle cost optimization) by enabling self-sufficient operations
- **Development schedule**: Extensive training material development requires significant time and resources

**Evaluation factors:**
- Project schedule milestones and handover date
- Availability of subject matter experts for content development
- Employer's expectations for training material quality and completeness

**Approach**:
- Prioritize critical safety and operational training (minimum viable training for safe startup)
- Develop comprehensive training materials for complex/critical systems
- Provide foundational training materials for less-critical systems, with references to OEM manuals for details
- **TBD** — Confirm prioritization and level of detail with Employer

*Source: **ASSUMPTION** — typical project trade-off*

**Trade-off 5: Standardization vs. Optimization**

**Competing concerns:**
- **Standardization**: Use standard training templates and formats across all modules for consistency and easier maintenance
- **Optimization**: Tailor format and approach to each topic for maximum training effectiveness

**Evaluation factors:**
- Ease of future updates (standardized formats easier to maintain)
- Learning effectiveness (optimized formats may improve comprehension for specific topics)
- Development efficiency (standardized templates faster to produce)

**Approach**:
- Establish standard templates for manuals and presentations
- Allow flexibility for topic-specific needs (e.g., troubleshooting flowcharts, safety checklists)
- Maintain consistent look-and-feel and navigation structure across all materials

*Source: **ASSUMPTION** — typical documentation standardization approach*

## Examples

### Reference Examples and Precedents

**Example 1: Training Manual Structure**

**ASSUMPTION: Typical training manual structure for a facility system:**

```
1. Introduction
   1.1 Purpose and Scope
   1.2 System Overview
   1.3 Key Equipment and Components

2. Safety and Environmental Considerations
   2.1 Hazards and Risk Controls
   2.2 Personal Protective Equipment (PPE)
   2.3 Permit Requirements
   2.4 Environmental Protection Measures

3. System Description
   3.1 Process Flow Description
   3.2 Equipment Details
   3.3 Control Philosophy
   3.4 Safety Interlocks and Alarms

4. Operating Procedures
   4.1 Pre-Startup Checks
   4.2 Startup Procedure
   4.3 Normal Operations
   4.4 Shutdown Procedure
   4.5 Emergency Shutdown

5. Maintenance and Troubleshooting
   5.1 Routine Maintenance Tasks
   5.2 Common Issues and Solutions
   5.3 Troubleshooting Flowcharts

6. References and Appendices
   6.1 Related Documents (SOPs, P&IDs, OEM manuals)
   6.2 Glossary of Terms
   6.3 Contact Information (vendors, emergency contacts)
```

*Source: **ASSUMPTION** — typical training manual structure for industrial facilities*

**Example 2: Training Presentation Approach**

**ASSUMPTION: Training presentation best practices:**
- **Slide count**: Target 30-50 slides for a 2-3 hour training session (allows time for discussion and questions)
- **Content per slide**: One key concept per slide; avoid text-heavy slides
- **Visuals**: Include system diagrams, photos of equipment, and process flow diagrams
- **Interactive elements**: Include review questions, discussion prompts, and scenario-based exercises
- **Summary slides**: Recap key points at end of each major section

*Source: **ASSUMPTION** — adult learning best practices*

**Example 3: Quick Reference Guide Format**

**ASSUMPTION: Quick reference guide (laminated card or poster) for common procedures:**

```
[Front side]
RAILCAR UNLOADING — QUICK START GUIDE

PRE-CONNECTION CHECKS:
□ Railcar positioned and brakes set
□ Bonding cable connected
□ Spill containment in place
□ PPE donned (hard hat, safety glasses, gloves)

CONNECTION SEQUENCE:
1. Open railcar dome lid
2. Verify product level and quality
3. Connect unloading hose (check gasket)
4. Connect vapor return hose (if applicable)
5. Verify all valves closed before pressurizing

[Back side]
EMERGENCY PROCEDURES:
- SPILL: Close valves, activate spill response team
- FIRE: Activate fire alarm, evacuate, call emergency services
- INJURY: Administer first aid, call for medical assistance
Emergency Contact: [phone number]
```

*Source: **ASSUMPTION** — typical quick reference format for operations*

**Example 4: Competency Assessment Matrix**

**ASSUMPTION: Training materials should align with competency assessments (cross-reference DEL-35.02):**

| Task / Competency | Training Module | Assessment Method | Qualified Assessor |
|-------------------|-----------------|-------------------|-------------------|
| Railcar unloading connection | Module 2: Railcar Unloading Ops | Practical demonstration | Operations Supervisor |
| Emergency shutdown activation | Module 5: Emergency Response | Simulator exercise | HSE Manager |
| Custody transfer meter reading | Module 3: Metering Operations | Written test + practical | QA/QC Lead |

*Source: **ASSUMPTION** — typical competency-based training approach; aligns with DEL-35.02 scope*

**Example 5: Troubleshooting Flowchart Format**

**ASSUMPTION: Training materials should include troubleshooting aids:**

```
[Flowchart example: Pump will not start]

START: Pump will not start
  ↓
  Is pump control switch ON? → NO → Turn switch ON, retry
  ↓ YES
  Is pump available in control system? → NO → Check safety interlocks, resolve issues
  ↓ YES
  Does pump motor have power? → NO → Check electrical supply, circuit breakers, MCC
  ↓ YES
  Is pump suction valve open? → NO → Open suction valve
  ↓ YES
  Is pump discharge valve throttled correctly? → NO → Adjust discharge valve
  ↓ YES
  Contact maintenance for mechanical/electrical troubleshooting
```

*Source: **ASSUMPTION** — typical troubleshooting format for operations training*

### Anticipated Artifacts for Reference

Per _CONTEXT.md, anticipated artifacts are:
- **Training manuals**: Comprehensive written documentation
- **Training presentations**: Instructional slide decks and visual aids

*Source: _CONTEXT.md (Anticipated Artifacts)*

**Recommended training manual topics (based on facility systems):**
1. Facility Overview and Safety Orientation
2. Railcar Unloading System Operations
3. Storage Tank Operations
4. Marine Loading System Operations
5. Product Transfer and Metering Systems
6. Control Systems and HMI Operation
7. Electrical Systems Overview
8. Maintenance Procedures — Mechanical Equipment
9. Maintenance Procedures — Electrical and Instrumentation
10. Emergency Response and Spill Management
11. Environmental Compliance and Monitoring
12. Regulatory Compliance and Recordkeeping

*Source: **ASSUMPTION** — training topics inferred from facility scope per Decomposition Section 1.1*

**Recommended presentation topics:**
- System-specific presentations aligned with training manual structure
- Safety briefings (site orientation, permit-to-work, emergency procedures)
- Hands-on training session guides (to accompany practical exercises)

*Source: **ASSUMPTION** — typical presentation structure*

### Lessons Learned and Best Practices

**Best Practice 1: Early Engagement with Operations Team**
If the Employer has an established operations team, engage them early in training material development to:
- Understand their training needs and preferences
- Leverage their operational experience
- Ensure materials align with their operating philosophy
- Obtain buy-in for training approach

*Source: **ASSUMPTION** — typical best practice for training development*

**Best Practice 2: Use of Visuals**
Adult learners retain information better with visual aids. Include:
- System diagrams and P&IDs
- Equipment photographs (during construction and commissioning)
- Process flow diagrams
- Safety signage and labeling
- Video recordings of procedures (if budget allows)

*Source: **ASSUMPTION** — adult learning principles*

**Best Practice 3: Version Control Discipline**
Maintain strict version control from the start:
- Assign document numbers early
- Track revisions meticulously
- Clearly mark draft vs. final versions
- Archive superseded versions
- Coordinate updates across related documents

*Source: **ASSUMPTION** — lessons learned from document management challenges*

**Best Practice 4: Pilot Testing**
If schedule permits, conduct pilot training sessions with a small group:
- Identify gaps in content
- Test comprehension and usability
- Refine materials before full training rollout
- Adjust pace and level of detail based on feedback

*Source: **ASSUMPTION** — quality assurance best practice for training*

**Risk to Avoid: Training Material Obsolescence**
Training materials can become obsolete quickly if not updated:
- Implement change management process to trigger training material updates when facility modifications occur
- Assign ownership for training material maintenance post-handover (typically Employer/operator)
- Design materials to be easily updated (editable formats, modular structure)

*Source: **ASSUMPTION** — common risk for training materials over facility lifecycle*
