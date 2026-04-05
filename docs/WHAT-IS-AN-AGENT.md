# What Is an Agent?

**agent = LLM + instructions + access to files + use of tools**

That's it. Nine words.

That definition is operational, not metaphysical. It tells you what kind of runtime system Chirality is talking about. It does not mean that an AI agent is a responsible person or a bearer of professional duty.

---

## What Is a *Good* Agent?

```
good_agent = agent_1(agent_2)
```

Agent 1 orchestrates the instructions for Agent 2.

Good agents do one type of thing really well. And *only* that one type of thing.

Orchestrate them in your workflow between decision points. That is how you get speed, and that is how you get output you can trust in professional engineering work.

---

## What Is a *Great* Agent?

```
great_agent = agent_0(agent_1(agent_2))
```

Agent 0 brings the human and Agent 1 into alignment.

This is why you really only need three layers of nested agents. More complex architectures can exist, but they have tradeoffs.

---

## The Three Layers

| Layer | Name | Role |
|-------|------|------|
| **Agent 0** | The Architect | Writes and maintains the instructions, after the human determines alignment |
| **Agent 1** | The Manager | Orchestrates which instructions, files, and tools go to which specialist |
| **Agent 2** | The Specialist | Takes actions according to instructions |

---

## What This Does and Does Not Mean

In Chirality, an AI agent is a bounded artificial actor. It can read files, use tools, generate claims, and modify project state within its write scope. In regulated practice, that same agent is treated as one of the "others" whose work a human professional supervises and reviews before relying on it.

So there are two different questions:

- What kind of system is this? An agent in the technical sense above.
- How is its work treated? As delegated work under human supervision, review, and accountability.

The human remains the accountable party. The agent contributes content and action inside a governed workflow; the human decides what to rely on.

---

## Why This Works

**Trust through specialization.** By narrowing the scope of Agent 2, you reduce the probability of hallucination. It doesn't need to know the entire project history—it only needs to know how to execute the specific function Agent 1 handed it.

**Human authority at every gate.** Agents propose; humans decide. No agent can approve deliverables, resolve conflicts, or issue work for reliance. The human stays in responsible charge throughout—the system accelerates the work, not the decisions.

**Speed.** Smaller contexts and specialized instructions process faster and cheaper than massive, general-purpose prompts.

**Debuggability.** If the output is wrong, you know exactly where to look:

- Bad output → Fix Agent 2's tools
- Wrong task attempted → Fix Agent 1's instructions
- Misunderstood goal → Fix Agent 0's alignment

---

## Teams and Project Management

A team of agents is not just a software pattern. In Chirality it is a project-management structure.

The decomposition, folder hierarchy, stable IDs, lifecycle states, dependencies, gates, reviews, and change controls are the same organizational devices that a human team would use to structure work. The difference is that Chirality makes that structure directly inspectable in the filesystem rather than hiding it in meetings, dashboards, and memory.

This is why many-agent orchestration matters. It is not only about parallelism. It is about making delegated work legible enough that a human can supervise it, review it, and accept responsibility for the result.

---

## Scaling: The Fan-Out / Fan-In Pattern

The human interfaces with a single Agent 1 instance through chat. Agent 1 assigns tasks to nested Agent 2 instances running in parallel:

| Stage | What Happens |
|-------|--------------|
| **Fan-Out** | Agent 1 receives direction from the human, assigns tasks to Agent 2 instances |
| **Process** | Agent 2 instances execute simultaneously |
| **Fan-In** | Agent 1 collects results and returns the final output to the human |

**Isolation of failure.** If one Agent 2 instance crashes, the others continue unaffected.

**Context hygiene.** Each Agent 2 instance spawns with zero state. No context drift from previous tasks.

---

## Example: Invoice Processing

The human chats with Agent 1:

> "Process the invoices in this folder."

Agent 1 then assigns the task to Agent 2 instances—each one extracts Date, Amount, and Vendor from a single PDF. Agent 1 collects the results and merges them into a CSV.

All of this is done by Agent 2 types, orchestrated by Agent 1.

---

## Summary

*Good agents do one thing well. Great agents are composed of good agents. The human decides what to rely on.*

---

## In This Project

Chirality implements this model with a governed agent instruction suite (see [`docs/REPO_INVENTORY.md`](REPO_INVENTORY.md) for current counts), a formal invariant system, and governance documents that make the whole thing auditable. To go deeper:

- [`README.md`](../README.md) — Project overview and architecture
- [`AGENTS.md`](../AGENTS.md) — Agent index and matrix
- [`CHIRALITY_FRAMEWORK.md`](../CHIRALITY_FRAMEWORK.md) — Why agents, teams, governance, and professional knowledge fit together the way they do
- [`PROFESSIONAL_ENGINEERING.md`](../PROFESSIONAL_ENGINEERING.md) — Why AI agents are treated as "others" under professional supervision and review
- [`DBM_Agent_Instruction_Architecture.md`](DBM_Agent_Instruction_Architecture.md) — Full design basis
