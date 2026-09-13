# Chirality

Chirality helps you turn complex work into repeatable workflows and purpose-built tools that you own.

1. **Make complex work understandable.** Organize context into clear subjects, boundaries, dependencies, and responsibilities.
2. **Make it repeatable.** Develop workflows, checks, and purpose-built tools from that structure.
3. **Make it adaptable.** Adjust as conditions change and understanding grows. Carry accepted lessons into the work underway and the next project.

[Website](https://chirality.dev) · [Chirality App releases](https://github.com/sgttomas/chirality-app/releases)

## What it's for

Work with agents to organize the references for a task, develop a method, and put it to use.

That might mean preparing a design basis memorandum from an accepted, structured knowledge base. Preparing estimate inputs by organizing sources and assumptions and consolidating line items, units, and quantities. Or transforming data into a required format, then building custom software so next time you can run an ingestion pipeline instead of another agent session.

The work itself helps develop the way of doing it. A useful instruction becomes part of a method. A recurring check becomes a tool. A lesson changes how the next task is performed.

Chirality App provides an interface for this work. This repository contains the agent instructions, growing collection of methods, deterministic tools, runtime, and application source.

## Why build this?

Companies make the same mistakes repeatedly. People move and take the knowledge with them. Information is saved haphazardly. Lessons are recorded but get little traction. Each person develops their own way of completing the same task.

Agents don't automatically solve any of that. They can produce a huge volume of work that you weren't involved in pulling together. Even when it is usually right and correctly referenced, you still need to understand and agree with the basis and check the result.

Working with agents is project management.

There is coordination overhead in keeping everyone working from the correct information, and validation overhead in checking that the work used that information correctly. Chirality brings those concerns into the methods used to do the work.

There are no shortcuts around good discipline in document control and information management. Keep your filenames, versions, and references organized. Chirality helps you build effective task management on that foundation so your methods and lessons aren't lost or obscured.

## The work doesn't have to stay in the App

Methods, references, outputs, and decisions live in your files. Other people, applications, and agents can use them.

Chirality deliberately uses the filesystem for shared working state. Git records versions and changes. The project record can survive the conversation, the model, and the application used to create it.

Workflows can run within Chirality App, on another agent platform, or as standalone software you build with the agents. All work does not need to take place in Chirality.

Sometimes the useful outcome is a specialized tool that no longer needs an agent to do the task.

## Checking the work

Deterministic tools perform defined operations and checks. Agents do work that involves interpretation, prepare supporting evidence, and identify matters that need a decision.

Neither removes your responsibility to examine substantial claims against their sources or rationale. A citation helps you check a claim; it does not establish that the claim is correct.

The methods in this repository provide ways to preserve sources, distinguish assumptions from supported statements, record decisions, and review changes. The requirements and checks differ by workflow. An instruction to an agent is not, by itself, a guarantee that the application enforces it.

Use Chirality for work you are competent to evaluate. Apply review appropriate to the consequences.

## Your work remains yours

Chirality is free and open source under the MIT licence.

Using Chirality App does not require sending your organization's data to Chirality AI Ltd. Model access and data handling depend on your chosen configuration; using a hosted provider is different from running a model locally. Consult the App's release documentation for supported options.

You can use and adapt the published methods, bring your own, and build tools fitted to your needs. You don't need an engagement with Chirality to do that.

If you want help, Chirality AI Ltd. offers paid work to develop and refine methods, workflows, and tools with your organization. The results remain yours when the engagement ends.

[Work with us](https://chirality.ai/contact.html)

## Where to start

**To use the App:** visit the [release page](https://github.com/sgttomas/chirality-app/releases) and read the notes for the version you download. The desktop distribution targets Apple Silicon Macs running macOS 15 or newer. Version 3.0 is in development.

**To explore the methods:** start with [`workflows/README.md`](workflows/README.md). Choose a task whose result you can evaluate, inspect the method's inputs and review requirements, and adapt it to your work.

**To understand or develop the system:**

| Location | What you'll find |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) and [`agents/`](agents/) | Four roles, their instructions, and runtime registry |
| [`workflows/`](workflows/) | Reusable methods and their input, output, and review requirements |
| [`tools/`](tools/) | Deterministic utilities, checks, and transformations |
| [`projects/chirality-runtime/`](projects/chirality-runtime/) | Shared runtime, engine adapters, daemon, client, and CLI |
| [`projects/chirality-app-dev/`](projects/chirality-app-dev/) | Desktop application source and development documentation |
| [`projects/`](projects/) | Product and integration projects |
| [`docs/`](docs/) | Design basis, standards, contracts, and specifications |

The [runtime README](projects/chirality-runtime/README.md) covers runtime development. The [App documentation index](projects/chirality-app-dev/docs/README.md) links to application requirements and build instructions.

For the underlying principles, read [`docs/DIRECTIVE.md`](docs/DIRECTIVE.md). For agent execution rules, start with [`AGENTS.md`](AGENTS.md) and the instructions for the project you're working in.

This is an active development repository. Source code, development records, and release artifacts serve different purposes; work present here is not necessarily part of a released App.

## License

[MIT License](LICENSE.md)

Copyright © 2026 Ryan Tufts.
