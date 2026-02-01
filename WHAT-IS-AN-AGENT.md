# What Is an Agent?

**agent = LLM + instructions + access to files + use of tools**

That's it. Nine words.

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

## Why This Works

**Trust through specialization.** By narrowing the scope of Agent 2, you reduce the probability of hallucination. It doesn't need to know the entire project history—it only needs to know how to execute the specific function Agent 1 handed it.

**Speed.** Smaller contexts and specialized instructions process faster and cheaper than massive, general-purpose prompts.

**Debuggability.** If the output is wrong, you know exactly where to look:

- Bad output → Fix Agent 2's tools
- Wrong task attempted → Fix Agent 1's instructions  
- Misunderstood goal → Fix Agent 0's alignment

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

| Agent | Analogy | Function |
|-------|---------|----------|
| **Agent 0** | The Compiler | Writes the prompts |
| **Agent 1** | The Runtime | Manages flow and state |
| **Agent 2** | The Thread | Stateless execution |

---

*Good agents do one thing well. Great agents are composed of good agents.*
