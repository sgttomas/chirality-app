# Product questions for software PRD development

Use the questions that affect the present undertaking. They help HELPS_HUMANS develop a product account with the human; they are not mandatory headings, automatic requirements, or a completeness score. Return to the relevant question when an example, source, or correction changes the understanding.

## Purpose and the people who rely on the result

What can someone accomplish with the proposed product that they cannot adequately accomplish now? Who experiences the difficulty, who uses the result, who operates it, and who bears consequences when it behaves incorrectly? A caller of an API, the developer using a library, and the operator of a service may be different people with different needs.

For a feature within an existing product, identify what remains governed by the parent basis and what this project adds. For a new product, explain its place in the surrounding activity. “Build a service” does not yet identify what the service is for. “Let approved clients retrieve the current inspection record without receiving another client's records” makes several product questions visible without specifying its architecture.

Distinguish evidence of a need from a proposed response. A report of a user difficulty can support investigation. The agent's recommended feature remains a proposal until adopted. Do not invent personas, survey findings, usage frequency, or market demand to make a rationale look complete.

## Product boundary and inherited basis

Which capability belongs to this undertaking? Which behaviour must remain intact? What does another system or organisation provide? What is outside the product altogether, and what is merely outside one component's responsibility?

For a library, its application-facing interface may be part of the product while the host application's screens are outside it. Error information needed by that application can still be part of the library's obligation. For an editor feature, excluding persistence of a pending proposal does not exclude saving document content after a proposal has been applied.

An existing implementation supplies evidence of behaviour. It may also contain defects or accidental restrictions. Identify the accepted specification or human direction that gives a behaviour the standing of a commitment to preserve. Where that basis is absent, expose the decision rather than assuming every current behaviour is correct or disposable.

A replacement project can define a new product outcome and a transition from an existing system. Distinguish it from a request simply to repair, upgrade, or operate that system. The transition can be product-development scope when expressly included; the workflow does not absorb unrelated maintenance through that inclusion.

## Vocabulary, state, and the course of use

Which objects matter, and which similar terms mean different things? Identify the state being read, proposed, modified, saved, delivered, or relied upon. Distinguish a request from a completed result, a preview from an accepted change, and an old revision from the current one where those differences affect the product.

Follow representative activity from its starting conditions to the result. Include interruptions and exceptions that threaten the purpose. For a service, this may involve a caller submitting a request, receiving an acknowledgement, checking progress, and obtaining a result. Whether acknowledgement promises durable receipt is a product question. The required response to a repeated request may be consequential even though there is no visible user interface.

For a batch-processing product, examine the input set, validation, incomplete processing, rejected records, outputs, and what a rerun should preserve. This is a product definition for reusable software, not permission to operate on a production dataset or conduct a one-off analysis.

Use tables when they make conditions and resulting obligations easier to compare. A state-and-action table complements a narrative of use. It should preserve distinctions that a list of feature names obscures.

## Data and interfaces

What information enters and leaves, and who owns or may use it? What does the receiving party need to interpret the result? Consider identity, units, versions, timing, validity, and the meaning of absent or partial data where applicable.

Separate an agreed interface constraint from a proposed mechanism. “The existing client must continue to receive the fields it relies on” can be a product commitment. An exact transport, schema, or version may be an inherited constraint, a specifically selected design, or a choice still open. The PRD should make its standing clear.

Where an external service or data source is necessary, identify what has actually been checked: availability, contract, content, licensing or permitted use, and known limitations as relevant. Do not promise an integration from a name alone. Bring unresolved access or authority questions to the human when the product's proposed reliance depends on them.

Use synthetic or authorised redacted examples to explain sensitive interfaces. State when those examples leave a material property unexamined. Source preservation is not permission to duplicate credentials or private data.

## Quality, operating conditions, and consequences

Which conditions would make a function unusable or unacceptable even if its nominal action works? Consider reliability, responsiveness, throughput, recovery, accessibility, security, privacy, resource limits, installation, compatibility, and operation only to the extent they affect the product.

Turn a consequential preference into an assessable condition where the basis supports it. If the human needs a particular response time, identify the scenario, environment, workload, and grounds for the target. If the limit is unknown, preserve the need and plan the work that will establish a defensible target. A convenient round number is not a requirement merely because it is easy to test.

Describe which failures must be prevented, exposed, recoverable, or referred to a person. Consider who can detect a failure and what action they can take. An error message with no usable recovery route can leave the intended activity incomplete. An apparently successful result can be more misleading when it omits the information needed to recognise its limitations.

For software containing agents, examine what those product agents can read, propose, change, and initiate, and which actions require the product user's decision. Keep those product requirements distinct from the roles of the development team creating the software. Do not assume that a product must reproduce the team's own organisation.

## Verification and validation

What future observation or examination would show that a requirement is satisfied? What would show that the intended activity is adequately supported? The first concerns verification; the second also needs validation of use. A simulation or prototype supplies evidence only within the circumstances exercised.

For an API product, an examination can include representative callers, permitted and forbidden access, incomplete inputs, repeated requests, and recoverable failures. For a library, examples can show what a consuming program is entitled to expect and how misuse is reported. For an editor, observe the connected user activity and resulting document state.

Record the principal future means of examination without writing the entire eventual test suite or inventing local `AC-*` and `VER-*` identities. FEED will develop local production contracts and their verification relationships. Requirements and acceptance scenarios in the PRD give that work a source; later tests do not create obligations retroactively.

## Open design, delivery, and the next use

Which unanswered questions can remain open while decomposition and setup proceed? Identify their constraints, affected work, resolution owner, and the condition by which an answer is needed. A question may be manageable while concentrated in one design conversation and become disruptive after several independent contributors adopt incompatible answers.

What is to be delivered and to whom? Include installation, distribution, data transition, compatibility, documentation, operator preparation, or support transfer where they determine a usable outcome. These may shape the PRD even though detailed release planning comes later. Identifying continuing support responsibility does not turn the workflow into a maintenance method.

A large product can use one coherent overview with normative annexes for major capabilities or interfaces. Define which documents belong to the proposed accepted basis and how their boundaries relate. Preserve shared requirements in one identifiable home. A subsidiary specification cannot quietly change the parent's commitment. The eventual project division remains the responsibility of decomposition.

## An adaptable PRD arrangement

Choose an order that explains the actual product. One possible arrangement is:

1. Purpose, intended users or consumers, and outcomes.
2. Existing context, inherited basis, and scope boundaries.
3. Product vocabulary and connected activities or operating scenarios.
4. Required capabilities, behaviour, and interfaces.
5. Quality constraints and relevant operating conditions.
6. Principal verification and validation expectations.
7. Open decisions, assumptions, limitations, and their treatment.
8. Delivery expectations and references to the supporting basis.

A feature document may combine several of these. A larger product may distribute them across an identified normative set. Do not populate empty sections with generic prose or omit a consequential subject because a sample outline lacks its heading.
