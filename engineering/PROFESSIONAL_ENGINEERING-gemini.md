# PROFESSIONAL_ENGINEERING.md
**Standard for the Use of Agentic Systems in Regulated Practice**

## 1. The Core Axiom
In regulated, high-stakes environments—where failure harms life, public safety, or critical infrastructure—**Artificial Intelligence is not a replacement for engineering judgment; it is a material that must be engineered.**

Chirality AI defines an "Agent" not as a Large Language Model (LLM), but as a **controlled system architecture**:
> **Agent = Model + Instructions + Tools + State + Governance**

The model provides the cognitive substrate (reasoning, perception); the *architecture* provides the agency (control, memory, safety).

## 2. The Engineer-of-Record (EoR) Principle
Professional liability is personal and non-transferable.
* **No Agent Authority:** No AI agent may approve, certify, seal, or issue work for reliance.
* **Human-at-the-Gate:** We reject "human-in-the-loop" as too passive. We practice **Human-at-the-Gate**. Agents may execute work within bounded states, but only a human Professional Engineer can open the gate that transitions a draft to a deliverable.
* **Duty of Competence:** An engineer must not use an agent to perform work they are not competent to verify manually.

## 3. Architecture as Safety
Safety is not a guardrail added after training; it is a property of the system topology.

### 3.1 The Cognitive Boundary
We do not ask agents to "figure it out." We **pre-structure the cognitive space**:
* **Deterministic Layer:** Schemas, validators, checklists, and calculations are defined in code, not prompts.
* **Probabilistic Layer:** Agents are reserved for **combinatorics** (sorting, searching, drafting) and **uncertainty** (interpreting ambiguity).
* **Rule:** If a task can be validated by a schema, it must be constrained by a schema.

### 3.2 Filesystem is the Only Truth
In professional practice, **State = Liability**.
* **No Hidden Memory:** If a decision exists only in a chat log or a vector database, it does not exist.
* **Artifact-First:** Agents must read from and write to the filesystem.
* **Audit Trail:** Git history is the legal record of project evolution.

## 4. Operational Constraints (The "Non-Negotiables")

### 4.1 The "No Invention" Rule
In high-stakes engineering, hallucination is not creativity; it is a lie.
* **Unknowns are Explicit:** Agents must output `TBD` or `UNKNOWN` rather than guess a plausible value.
* **Assumptions are Labeled:** Any gap filled by the agent must be explicitly logged in an `Assumptions_Register.md`.

### 4.2 Provenance is Mandatory
"Trust me" is not an engineering concept.
* **Citation:** Every extraction, summary, or parameter value must cite its source file and section.
* **Traceability:** Every output artifact must trace back to a specific set of input constraints and a specific version of the agent instructions.

### 4.3 Conflict Surfacing
Agents must not resolve conflicts silently.
* If Source A says "100MPa" and Source B says "120MPa," the agent’s job is not to pick the average; it is to **halt and report the conflict** to the Engineer.

## 5. The Three-Layer Governance Model
To maintain control, we decompose agency into three distinct roles:

| Role | Scope | Responsibility | Human Equivalent |
| :--- | :--- | :--- | :--- |
| **Type 0 (Architect)** | **Governance** | Defines the "physics" of the project: standards, schemas, templates, and safety rules. | Principal / Chief Engineer |
| **Type 1 (Manager)** | **Orchestration** | Plans workflows, decomposes tasks, routes information, and assembles evidence. | Project Manager / Lead |
| **Type 2 (Specialist)** | **Execution** | Performs narrow, stateless, checkable tasks (e.g., "Extract Loads", "Format Spec"). | Junior Engineer / Drafter |

## 6. Risk & Verification
Verification must be proportional to risk.
* **Low Risk:** Agent output + Automated Syntax Check.
* **Medium Risk:** Agent output + Human Spot Check.
* **High Risk (Safety Critical):** Agent output + Independent Calculation + Full Line-by-Line Review.

**We do not automate engineering judgment. We engineer a harness that allows judgment to scale.**