# PROFESSIONAL_ENGINEERING.md — The Intersection of Agentic AI and Professional Duty

> **"Engineering is not the art of building things; it is the art of building things that do not fall down."**

This repository (`Chirality App`) is not a toy. It is a harness for deploying Artificial Intelligence within the **regulated, high-stakes, and professionally liable** environment of Engineering, Procurement, and Construction (EPC).

This document defines the philosophy, theory, and ethical obligations that govern the use of agents in this project.

---

## 1. The Theory: Classical Agency in a New Substrate

We reject the notion that "Agentic AI" is a mystical new capability. We adhere to the **Classical Multi-Agent Systems (MAS)** definition:

> **Agency is a system-level property, not a model capability.**

Long before Large Language Models (LLMs), agentic systems were defined by **beliefs, goals, intentions, coordination, and control under uncertainty**.

What has changed is not the definition of an agent, but the **cognitive substrate**:
- **Classical Agents:** Expensive to build; rigid perception; brittle reasoning.
- **Modern Agents (LLMs):** Cheap perception; flexible reasoning; fluid communication.

**The implication:** LLMs dramatically reduce the cost of building agents, but they do not remove the need for **System Architecture**. An LLM without a control architecture is not an agent; it is a chatbot. An agent is defined by **control loops** over time.

---

## 2. The Architecture: Designing Cognitive Boundaries

In this project, we do not "prompt engineer" magic outcomes. We **architect cognitive boundaries**.

### The Core Design Principle
**Structure the space, not the flow.**

Instead of hand-wiring fragile chains of thought, we decompose the engineering problem *before* the agent enters the loop. We isolate:
1.  **Stable Constraints:** Physics, codes, standards, schemas, file formats.
2.  **Known Transformations:** Data normalization, calculation, formatting.
3.  **Genuine Uncertainty:** Interpretation, strategic tradeoffs, synthesis.

**Agents are only allowed to operate in the third category.**

### The "Filesystem as State" Axiom
In professional engineering, **State = Liability**.
- If a decision cannot be reproduced, it is professional negligence.
- If the project state exists only in a vector database or a chat history, it is un-auditable.

Therefore, **The Filesystem is the Only Truth.**
- Agents read files.
- Agents write files.
- Agents commit to Git.
- **Git is the Audit Trail.**

This forces the agent to externalize its "mental state" into durable artifacts (Scope Ledgers, Decision Logs, Snapshots) that a human Professional Engineer can stamp.

---

## 3. The Professional Obligation: Duty of Care

As licensed professionals, we are bound by a **Standard of Care**. We are personally and legally responsible for the work we seal, regardless of the tools used to produce it.

### The "Human-in-the-Loop" Fallacy vs. "Human-at-the-Gate"
A "human-in-the-loop" who merely watches text stream by is not exercising engineering judgment; they are being lulled into complacency.

We implement **Human-at-the-Gate**:
- Agents do the work (Drafting, Checking, Aggregating).
- The work stops at a **Gate** (Git staging area, Approval Milestone).
- The Human opens the Gate.

### The Liability Hierarchy
To debug failure in a high-stakes environment, we use the Type 0/1/2 model:

| Failure Type | Source | Responsibility |
| :--- | :--- | :--- |
| **Type 2 (Execution)** | The Specialist Agent made a calculation or syntax error. | **Correctable.** Fix the prompt/tool. |
| **Type 1 (Orchestration)** | The Manager Agent skipped a step or dropped context. | **Systemic.** Fix the workflow architecture. |
| **Type 0 (Alignment)** | The Architect Agent (Human) set the wrong goal or standard. | **Professional Negligence.** The Human is at fault. |

---

## 4. Operational Rules for Chirality Agents

To satisfy our professional ethics, all agents in this repo must adhere to these rules:

1.  **No Silent Invention:** If a parameter is missing, the agent MUST output `TBD`. It MUST NOT statistically guess a value that looks plausible. Plausibility is the enemy of engineering truth.
2.  **Provenance is Mandatory:** Every assertion, extraction, or summary must cite its source (filename, section). "Trust me" is not an engineering concept.
3.  **Conflict Surfacing:** If two documents disagree, the agent MUST NOT resolve it. It MUST surface the conflict to the Human.
4.  **Deterministic Degredation:** If the agent is confused, it should fail safely and visibly, not hallucinate a "smooth" path forward.

## 5. Summary

We use AI to handle **combinatorics** (sorting, matching, checking, drafting), so that Humans can focus on **semantics** (meaning, intent, safety, judgment).

We do not ask the AI to "be an engineer." We use the AI to build a better harness for our own engineering judgment.