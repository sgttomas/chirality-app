# From General Capability to Situated Participation

**The Chirality App v4 Thesis**

*Why an application for making methods is the first exemplar of Chirality*

## Abstract

A general agent can produce substantial work without understanding its purpose
in the same committed sense as the person who will rely on it. More capable
reckoning therefore increases both what a person can undertake and the
importance of how the agent participates. A conversational interface alone does
not establish which application objects the agent means, what an action changed,
whether its outcome is known or what the person has accepted.

This thesis argues that an application can make agent capability practically
useful by sustaining a relation among purpose, meaningful objects, possible
actions and inspectable consequences. The person remains engaged in judgment
throughout that relation. The application contributes access and operations;
the agent contributes inquiry and action; reusable methods carry learning from
one undertaking into another. None of these contributions alone determines a
usable result.

The Chirality App is the first exemplar because its subject is method itself.
A person and an agent can develop a way of working through conversation, try it,
examine its effects and make it available for further use. The method becomes
an object of work without becoming an exhaustive orchestration. This gives the
framework a concrete application before it enters the more demanding semantics
of an engineering product such as SWBPIPE.

App v4 tests this argument through native supplier hosting, workflow identity
and trials, explicit human acts, and recovery that distinguishes intent,
acknowledgment and observed outcome. The implementation also supplies
counterexamples to easy claims of completeness: a turn interrupted while its
command continued, trial fidelity that does not establish method quality, and
records whose existence does not establish human engagement. These cases help
explain the architecture without proving its overall effectiveness.

The thesis proposes a route to proliferation through shared meanings and
host-specific operations. It does not establish a universally reusable runtime,
automatic application generation or general professional adequacy. Its
practical claims remain open to use, failure and comparison with simpler means.

## 1. The problem behind the application

An agent working beside an application can give advice about what a person
should do. An agent working within it can also inspect the relevant objects,
prepare a change, apply it within authority and examine its consequences. That
possibility changes the relation between conversation and work. The conversation
can become a place from which the work is carried forward, rather than a source
of instructions the person must translate into a separate sequence of actions.

The value does not arise merely from reducing clicks. Translation is also a
point at which meaning can be lost. A spoken reference to “that case” must
identify a particular object. A proposed revision must concern the version that
was examined. A result must be understood under the conditions that produced
it. If an agent and a person act through different versions of those meanings,
they can appear to collaborate while changing different things.

The research question is therefore: **why and under what conditions should an
application enable a general agent to participate in its work, and why should
workflow authoring be the first exemplar of that participation?**

The question concerns the reasons for building the application. It is broader
than how to embed a model and narrower than a theory of every possible agent.
The product requirements state what App v4 is to provide. This thesis examines
why those provisions belong together, what their implementation teaches, and
where the reasoning remains unproved.

The [PRD's purpose][A1] is to make a capable general agent act within and for an
application. Its objects, tools and workflows give the general capability a
particular field of action. The standalone App, where people create workflows,
is the exemplar. Engineering hosts supply their own domain reality and
operations. The distinction matters: an exemplar can show a pattern, while
each receiving application must establish what that pattern means in its work.

One objection is that a strong coding agent with files and a command line may
already be sufficient. For many development tasks that is a serious alternative.
An additional App is justified only where it improves the person's access to
the work, preserves useful meaning or makes action and examination easier.
The existence of agents does not establish demand for another interface.
Chirality's case depends on those practical benefits becoming observable.

## 2. Shared orientation, particular subject

The [Root thesis][R1] concerns the shared environment through which methods,
tools and applications can be developed. The App takes up a more particular
question: how that orientation becomes an environment someone can use to make
and carry out methods. SWBPIPE takes it into piping design and stress-model
authoring, where an apparently successful operation can yield a plausible but
wrong engineering result.

The three inquiries share a philosophical origin. [Appendix D][D1] preserves
the formal argument with shared definitions and concise commentary. C names
temporal dependence; the necessary meaning at issue is S's recognition of the necessity of contingency; N names
existential affirmation. G remains undefined. The conjecture is not expanded
here into a derivation of software mechanisms. Its place in the undertaking's
origin does not require a reader to assent to it before examining the practical
argument.

The four perspectives give that practical argument connected questions.
**Ontology** asks what the work concerns and which distinctions its
representations must preserve. **Epistemology** asks what supports an account
of the work and what is still unknown. **Praxeology** asks how purpose becomes
effective action through investigation and correction. **Axiology** asks why
that action matters and whether the means justify their costs.

In an application these questions meet in an ordinary operation. A request
concerns an identifiable object; its proposed effect rests on a reading of
that object; execution changes what can happen next; the person cares about
the consequences. Separating these questions analytically helps expose a
failure. Treating them as separate procedural duties would miss their relation.

The framework calls sophisticated agent inquiry and action **reckoning**.
This includes analysis, planning, criticism, comparison and adaptive execution.
**Judgment** is the person's situated, committed engagement with what the work
means, what matters and what they will stand behind. Judgment shapes the
question and the decision to pursue it before any final acceptance occurs.
An approval record can evidence an act; it does not contain or guarantee that
engagement. These terms follow the account developed in the [Root framework][R2].

This distinction permits extensive agent action. Reserving human judgment does
not imply that a person must issue every next command. Continuing authority
can give an agent room to investigate and repair while keeping the purpose and
consequential choices attributable. The difficult design problem is deciding
which boundaries make that arrangement workable for a particular activity.

## 3. Why making methods is the first exemplar

A useful method often begins before it can be specified. Someone encounters a
problem, tries a framing, discovers a missing distinction and changes how they
proceed. A successful sequence can then be examined for what might be useful
again. That learning is neither identical with the transcript nor reducible to
a list of commands stripped of their purpose.

Conversation is valuable here because the subject can develop during the
exchange. The person need not supply a complete specification before receiving
help. The agent can make an assumption visible, suggest a comparison or carry
out an investigation that changes what the person asks. The resulting method
can express both a purpose and a way to approach it without determining every
step in advance.

Workflow authoring makes this process itself available as work. A draft can be
read, tried and revised. Its intended inputs and returned evidence can be made
explicit. Someone can distinguish the version under trial from one selected
for reuse. When a later undertaking reveals a limitation, the method can be
corrected rather than merely supplemented with another instruction in an
ever-growing conversation.

This is why the App comes first in the explanatory sequence. It makes the
human–agent method accessible to its own inquiry. The agent contributes to
forming the conditions of its subsequent work, while the person remains able
to examine and decide upon that formation. The App's value lies in making this
cycle practicable, not in demonstrating that agents can generate workflow
text.

The example is also bounded enough to examine. A workflow has identifiable
source content, a draft and a use. A change in the draft can be compared with a
change in behaviour. The person can ask whether the method expresses the
intended purpose and whether its trial actually exercised that expression.
Those relations can be studied before the App supplies an agent with the
authority to change an engineering model.

There is a cost to this starting point. A method-authoring tool can become
absorbed in its own machinery. Elaborate registration and governance can make
it harder to perform the activity whose method is being developed. A successful
trial can become an unnecessary prerequisite for every revision. The product
therefore has to earn its structure through the learning and control it gives
the person. The current design makes a fresh-conversation trial available,
without making it a universal condition of registration.

### 3.1 A trial must examine the intended method

Earlier attachment-based trials did not supply a workflow in the same way as a
registered run. This was consequential: a favourable result could concern a
different framing or context, giving the author weak grounds for expecting the
method to behave similarly in use. The owner's subsequent direction made trial
fidelity an explicit design concern.[A2]

The current implementation takes a snapshot of the draft and uses the same
composer as a registered run of that content. An explicit header identifies
the activity as a trial. The run reference and the folder of associated files
differ because they identify the trial's own subject. A source test compares
those texts and checks the permitted differences. Preparation also detects a
draft changed during reading, and refuses to silently try another version.[I1]

This is an epistemic improvement through a concrete operation. It makes one
question answerable: was the intended method supplied in the relevant form?
It does not answer whether the method is good, whether the model attended to
every part or whether another use will succeed.

Two trial situations retain different value. A delegated trial can remain in
the context of authoring and return findings to that conversation. A clean
trial can expose dependence on context the author has taken for granted.
Neither context is universally superior. The author needs to understand what
was tried and why its result bears on intended use.

At the source revision examined here, both trial phases are implemented,
including linking, fidelity readings, comparison and bringing a trial or a real
run back to authoring. The native witness of both kinds remains open, and the
App does not yet read the supplier's delegation-availability signals. The source
thus supports an implementation account, with constructed examinations, rather
than a claim of fully demonstrated authoring practice.[A2][I2]

## 4. Methods should guide action without replacing inquiry

A reusable workflow must preserve enough of a method to be useful elsewhere.
It must also permit attention to circumstances its author did not anticipate.
If it is only a vague statement of purpose, the next participant may have to
rediscover everything. If it prescribes every action, it can force unsuitable
work or conceal a premise that no longer holds.

The App's distinction between prose method and a small declared part offers a
way to manage this tension. Prose can convey purpose, conditions, distinctions
and examples. Declarations can identify expected inputs, tools, human acts and
outputs that the product can expose. Neither makes the workflow a complete
description of the undertaking. The product observes selected features of the
method while the person and agent continue to interpret the work.[A1]

Role guidance has a similar purpose. Conception, integration and bounded
execution describe contributions that can otherwise become unowned. They need
not prescribe a separate conversation or agent for every contribution. An
undertaking may benefit from a manager or from parallel contributors; another
may be carried through by the person and one agent. Flexibility in arrangement
does not remove responsibility for bringing the result together.

Within App v4, this reasoning also leads to a concrete distinction: HELP_HUMAN,
HELPS_HUMANS and WORKING_ITEMS may be selected as conversation roles, while
TASK remains a bounded delegated role. Role choice can make an intended
contribution visible without establishing what the host permits it to do.
Repository authorization and product enforcement are separate subjects. A
permission granted to agents developing this repository does not silently alter
the App's runtime role settings or a receiving host's operation policy.[A1]

The native witness supplies a caution against treating a role arrangement as
an accomplished coordination system. It observed a manager spawning a child,
waiting, sending a follow-up and closing it. It also found that the manager
could not message an unrelated conversation through that route. Some native
activity appeared without the full prompt or relationship information needed
to establish receipt, review and integration. The App showed those limits
rather than inferring completed coordination from the child's existence.[O1]

This suggests a criterion for useful orchestration: it should make actual
responsibilities and returns easier to manage. A display of a team is not
evidence that the team has established a usable result. Native delegation can
provide considerable capability while leaving integration to an agent and a
person who remain engaged with the undertaking.

## 5. Meaningful perception and action

An application brings more than storage to an agent. It already distinguishes
objects, allowed operations, conditions and consequences. Those meanings are
often what makes the application useful to a person in the first place.
Agent participation becomes stronger when it can use them directly.

The host-integration contract consequently proposes a common capability
catalog and one route for validation and application. The person's interface,
embedded agent and an external controller should concern the same operations,
with the same reasons for unavailability. An agent may receive a structured
view rather than pixels; semantic parity concerns what the view and action
mean, not identical presentation.[A3]

Consider a proposed change based on an earlier read. If the object has since
changed, applying the proposal to the newly selected object would silently
change the subject. A basis identity and a stale refusal make the relationship
inspectable. Similarly, a retry after an uncertain response must not simply
create a second effect. These concerns arise from the meaning of the operation,
not from a need to give every agent action a ceremonial approval.

Perception and action constrain one another. The agent needs a view adequate to
the action it proposes. The result of the action must provide enough evidence
to continue. An application that offers powerful writes but incomplete reads
can produce decisive action on mistaken premises. One that offers rich context
but no useful operations leaves the person translating the result back into
work. The relevant unit of design is the connected activity.

The contract's distinctions between proposal, execution and human acceptance
follow from this relation. Operation success establishes that the operation
ran under its stated semantics. Acceptance identifies a person's act concerning
a subject. Professional reliance concerns another relation again. Combining
them in a single “success” indicator would make the interface simpler by making
its meaning less dependable.

This remains a transfer hypothesis for engineering hosts. The inspected App
source does not establish a qualified end-to-end App-to-SWBPIPE activity. Nor
does a common catalog prove that one declaration automatically generates a
good interface, tool and external adapter. The contract explicitly retains the
question of generated surfaces and remaining adapter work. That work must be
examined through an actual extension before claiming savings.[A3]

## 6. Preserving human judgment without multiplying gates

An agent can prepare a decision so well that the person has little additional
calculation to perform. The person still has to engage with what the decision
means. More polished preparation can assist that engagement or discourage it
by making the conclusion appear settled.

The application cannot ensure substantive judgment merely by requiring a
button press. It can make the subject clear, show the alternatives and
consequences, preserve the grounds and distinguish what was observed from what
was inferred. It can also prevent an automated rule from being recorded as an
actual human act. These are valuable contributions with limited claims.

The inspected permission code illustrates a narrower enforceable boundary.
Answers must conform to the native request and may not widen the requested
permissions. A constructed test rejects an affirmative answer attributed to an
App rule rather than permitted interaction. This supports claims about request
handling. It does not establish that a person's permission was informed or that
the resulting action was professionally adequate.[I3]

The same distinction limits claims about records of file checking, approval or
reliance. Identifying the content and act can preserve what was said and done.
The record does not turn a mistaken assessment into a correct one. Trustworthy
cold replay and native authenticity have additional implementation and
examination requirements that remain open in the current App account.[A4]

Preserving judgment also requires room for delegated action. Requiring a new
human act for every ordinary step can interrupt inquiry and consume the
attention needed for consequential choices. The host contract therefore
distinguishes operations that may apply within granted autonomy, proposals
that need acceptance and acts reserved to the person. The appropriate classes
belong to the host's actual work and adopted policy. The general framework
does not settle them for every application.[A3]

Checkpoint declarations make a further limit explicit. In the current phase
they guide the person and agents; software holding at checkpoints is deferred.
An interface can state an intended boundary without having enforced it. The
thesis must preserve that distinction rather than treating a declared workflow
as evidence of automatic governance.[A1][A3]

The values involved include user control, useful production, privacy and the
cost of attention. These can conflict. A stricter control can prevent one
failure and create delay or workarounds elsewhere. A design earns its place
through the consequences it improves, including whether the person can
understand and use it. This is why the App cannot be justified by counting its
controls.

## 7. Continuity is a relation to outcomes

Sustained work extends beyond a window's current display. A conversation may
continue while the view reloads; a request may remain outstanding; a command
may have changed a file before its response was lost. The practical question
after interruption is what happened and what can safely happen next.

Retaining a transcript helps, but does not answer every part of that question.
An intention recorded in text is not an applied operation. A write attempt is
not a received acknowledgment. A completed primary turn does not establish that
every descendant or process has stopped. Recovery needs access to the relevant
source of each fact and a way to preserve unknown outcomes.

App v4's process placement responds to this concern. The Rust host owns
supplier communication, records, file writes and human-act capture. The web
view presents and submits what the person initiates. Record and trial ticks
now run in their own host loops; the periodic status read writes no record.
Closing observation is therefore not designed to be the event that decides
whether recording continues.[A5][I4]

That source arrangement supports a property; it does not prove every failure
mode has been handled. Persistent replay, process loss, operating-system
behaviour and native use need their own evidence. The implementation explicitly
retains outstanding recovery and authenticity work rather than treating a
successful local reopen as a complete proof.[A4]

### 7.1 A counterexample supplied by the running application

In the first native witness, the person interrupted a turn running `sleep 90`.
The App observed the turn ending as interrupted, while the command had no live
completion item. After restarting Codex, supplier history reported the command
completed with exit zero and a duration of approximately ninety seconds.[O1]

The important finding is the divergence between ending a turn and establishing
that its work has stopped. This one observation cannot establish every
configuration's behaviour. It is nevertheless enough to defeat a universal
assumption that an interrupt necessarily stops every running command.

The App's display retained the live observation and later history separately.
Its label did not claim that the command had been prevented from completing.
The observation also showed a usability limit: nothing had told the person
that the command continued. Correctly bounded data can still leave the person
without the practical understanding they need.

This is the four perspectives working together. The distinction between turn
and command becomes ontologically consequential; the observations have
different grounds; continuation requires an appropriate action; the person
needs useful control rather than a technically defensible but insufficient
label. Actual use can expose a failure that no amount of consistency among
design documents settles.

## 8. Native capability and the application's contribution

A general harness already embodies substantial work in tool use, interruption,
questions, planning and delegation. Recreating those capabilities inside a
generic abstraction can discard useful behaviour and create a second system to
maintain. It can also conceal distinctions the supplier actually exposes.

The v4 architecture instead selects a stock, pinned supplier through its native
embedding interface. It preserves native items and presents them with their
source meanings. Chirality owns workflow use, the person–agent relationship,
host integration and the records needed for its particular acts and recovery.
The distinction identifies where the App contributes value and where it should
depend on capable existing means.[A5]

This is a design choice with costs. Native integration requires following
supplier changes and can tie useful interactions to a particular protocol.
Different suppliers may support different activities. Avoiding a generic
vocabulary does not remove the need for interpretation in the display. The
application still decides what to emphasize and how to expose a limitation.

The native witness makes those limits concrete. It observed delegation through
the selected supplier, but some activity did not supply the prompt and status
information needed for stronger claims. Preserving native capability allowed
the work to occur. It did not make every event fully observable or turn a
reported relationship into established integration.[O1]

The evidence favours examining the actual supplier path before constructing an
abstraction around assumptions. It does not prove that every abstraction or
separate service is harmful. The architecture itself acknowledges that earlier
supplier-host repairs combined several changes; their outcomes do not isolate
topology as the cause. Native hosting remains a hypothesis whose value depends
on maintained functionality and total cost.[A5]

## 9. Re-derivation carries learning, not merely requirements

The App's successive implementations raise a question larger than version
management. What should persist when capabilities, experience and the intended
product have changed enough to warrant another architecture?

Existing code carries both useful learning and contingent choices. A PRD can
help identify the commitments that should survive, but it cannot express every
interaction or failure discovered in use. Re-derivation therefore requires a
relationship among current purpose, requirements, source, observations and
owner interpretation. It is not compilation from a complete specification.

V4 preserves the core activity of developing methods through conversation. It
also identifies earlier request cards, plan views, registration, attachment
handling and recovery rules as reuse candidates. At the same time, it rejects
the old separate Runtime/socket topology and generic supplier-event
translation. These choices concern how to preserve useful experience while
replacing means that no longer fit the product's direction.[A5]

A rewrite can fail that purpose. It can discard subtle repairs, recreate
familiar defects or make a clean design less usable than its predecessor. The
relevant achievement is therefore the retention and improvement of useful
behaviour, not the speed with which a new codebase appears.

The native witness again supplies a small example. Identifier fields were
being autocorrected, and role headers accumulated when conversations changed.
Those defects were found by operating the actual App. The source now uses
exact-text input attributes and a conversation-specific role-header key. The
observation records that the repairs had automated checks but had not themselves
been witnessed natively.[O1][I5]

These are modest defects compared with the architectural claims, but they
matter to the argument. An application exists for someone to use. An incorrect
model identifier or misleading role display can defeat the intended activity
before the wider framework becomes relevant. Lived lessons must remain capable
of correcting the application at every scale.

## 10. Proliferation through particular applications

The App can demonstrate a way of making methods and using agents without
becoming the authority over every domain in which the method is used. This
limit is essential to proliferation. A piping application knows about models,
loads, cases and results; a different professional application will have
different objects and consequences. A generic agent vocabulary cannot replace
those meanings.

What can transfer is a set of useful relations: methods with identifiable
sources, agent access to meaningful operations, visible limits of perception,
common validation, attributable human acts and recoverable outcomes. What must
be supplied by each host is the domain interpretation, actual operation and
appropriate authority policy. A host can adopt shared types or components
where they serve those responsibilities without adopting a central executable
service.[A3][A5]

SWBPIPE is a demanding next instantiation because meaningful operation is
inseparable from engineering and numerical meaning. A successful tool call is
weak evidence if the model it changes no longer represents the intended
physical arrangement. A persuasive explanation cannot compensate for incorrect
solver inputs. The host must connect perception, change and result to its
domain engine, while the professional remains responsible for reliance.

This makes the proposed connected activity more informative than another
general connector demonstration. It asks whether the pattern survives contact
with a particular practice and its consequences. Domains may later improve
research context, but retrieval does not establish a source's standing or
applicability. The App can support the encounter with evidence without deciding
the engineering authority of what was retrieved.[A1][A3]

There are several ways this proliferation could fail. Host-specific adapters
may require so much work that shared contracts provide little economic benefit.
The catalog may be too generic to express consequential operations, or too
detailed for agents and people to use. Human-act recording may become an
administrative burden. A common interface may conceal differences that should
remain explicit. Transfer may depend so heavily on the originating owner's
translation that others cannot reproduce it.

These possibilities define tests of the thesis, not reasons to abandon the
attempt. The first question is whether a host activity becomes useful and
dependable. The next is what another operation, practitioner or application
requires to obtain that benefit. Counting exposed tools or shared schemas
would establish neither.

## 11. Discussion: what the case supports

The argument has three kinds of support. Product documents state adopted
purposes and design choices. Source inspection shows mechanisms through which
those choices are being realized. The dated native witness shows what occurred
in one actual configuration, including behaviour the prior account did not
fully anticipate. They support different claims and must remain distinguishable.

The most important result is a set of examinable connections. Workflow trials
connect a method's identity to the content supplied. Host operations connect
an action to its subject and basis. Recovery connects claims about completion
to observed outcomes. Human-act handling connects a recorded act to its content
without claiming that the record contains judgment. These mechanisms make the
thesis more than an aspiration.

Their presence does not establish that the App is fit for all its intended
work. The [examination account][A6] distinguishes verification of a candidate
from validation through realistic practitioner use. It also distinguishes
defined tests, historical passes and actual execution. This thesis has inspected
selected implementation and tests; it has not rerun the product or treated test
definitions as new passing evidence.

The principal practitioner and architectural author remain the owner. That
provides sustained purpose and unusually direct correction, but limits claims
about transfer. Another person may not share the vocabulary, infer the same
boundaries or tolerate the same amount of operational detail. An interface that
works through its author's continuing interpretation can still be incomplete
as a product.

There is also a risk of reconstructing the administrative burden that Root has
removed. Product records are justified where they preserve meaningful acts,
identify uncertain outcomes or make recovery possible. They become less useful
when the person must maintain representations of facts the application already
knows. The current removal of a separate registration-attempt journal, using
existing records and a liveness lock instead, illustrates that implementation
can be simplified while preserving a recovery question.[A4]

Useful evaluation would therefore examine both outcomes and costs. Can a person
make and improve a method without continual explanation from the developer?
Does an interruption leave them able to decide how to continue? Can a host
operation be added without duplicating its meaning across interfaces? Do the
records expose consequential uncertainty or merely increase the amount to
read? Such observations would strengthen or qualify the design hypotheses.

## 12. Conclusion

General agent capability becomes application capability through a relation to
what the application means and does. Useful participation requires accessible
objects, relevant context, meaningful operations and inspectable consequences.
The person's judgment shapes that participation throughout, while agent
reckoning can carry substantial inquiry and action within authority.

Workflow authoring is a fitting first exemplar because it makes the means of
work into something the person and agent can examine together. A method can be
formed through use, tried in an identified form and revised through its effects.
Its reuse carries learning without settling every subsequent undertaking in
advance. The App's purpose is to make that relationship usable.

App v4 gives the argument concrete form through native supplier capability,
workflow identity and trials, explicit human-act distinctions and outcome-aware
recovery. Its actual observations also discipline the argument. A completed
turn need not mean a stopped command. A faithful trial need not establish a good
method. A recorded act does not guarantee judgment. A coherent architecture
does not ensure a useful interface.

The same orientation can proliferate through applications when shared meanings
support the host's own reality. SWBPIPE tests that proposition against engineering
objects, numerical consequences and professional use. Its success cannot be
inferred from the App, and the App's success cannot be inferred from Root.
Each has a particular subject and needs appropriate evidence.

The central claim is accordingly conditional: an application can make general
agents more useful by enabling meaningful participation while preserving the
person's relation to purpose, evidence and commitment. How well it does so is a
question of use, including failures and control costs. The capacity to revise
the means while preserving that purpose is part of the thesis itself.

## Source basis and reading

This explanatory thesis uses repository revision
`a602024416ace9652f61bb2043889c307fd4e09d` for App requirements, implementation
and dated observations. Links name current files for convenient reading; a
later revision can change implementation standing. No source here is cited as
fresh verification of an external supplier. The historical foundation under
`foundation/thesis/` remains unchanged. The thesis creates no product requirement,
permission, acceptance or qualification.

- **R1:** [Root thesis: A Generative Environment for Human–Agent Work][R1].
- **R2:** [The Chirality Framework][R2], especially knowledge, reckoning and
  judgment, the four perspectives and control costs.
- **D1:** [Shared conjecture][D1], preserved argument and definitions.
- **A1:** [App v4 PRD][A1], §§1–4: purpose, exemplar, roles, methods and host
  expressions. These are product commitments, not delivery evidence.
- **A2:** [Workflow workspace and registration design][A2], §§4.2, 5.5, 6,
  11 and 17: trial meaning, host placement and current implementation account.
- **A3:** [Host integration][A3], §§2–7: catalog, perception, changes,
  human acts and autonomy; §§8–9: connecting responsibilities and limits.
- **A4:** [App implementation account][A4], current path and storage/remaining
  work: useful source overview with explicitly unfinished witnesses.
- **A5:** [Architecture basis][A5], §§1–5: priorities, native hosting,
  process placement, reuse and shared responsibilities.
- **A6:** [Examination][A6], §§1–3: verification, validation and evidence limits.
- **I1:** [Trial implementation][I1] and [trial tests][I1T]: snapshot and
  registered-run text comparison. The tests were inspected, not rerun here.
- **I2:** [Trial flows][I2]: preparation, send, linking, fidelity and bring-back;
  delegation availability explicitly remains unestablished by live reads.
- **I3:** [Native request handling][I3]: request-specific answers, permission
  subsets and refusal of an App-rule affirmative origin.
- **I4:** [Host ticks][I4] and [host entry points][I4B]: autonomous observation
  loops and read-only status. [Stop-record tests][I4T] examine intent,
  acknowledgment, observed termination and reopening through constructed cases.
- **I5:** [Exact-text fields][I5] and [conversation presentation][I5B]: repairs
  corresponding to the first native witness's input and role-header defects.
- **O1:** [First native App witness, 10 October 2026][O1]: one development
  build and supplier configuration; observations, defects and explicit exclusions.

[R1]: ../../../../docs/thesis/README.md
[R2]: ../../../../docs/thesis/CHIRALITY_FRAMEWORK.md
[D1]: appendix_d_framework_s.md
[A1]: ../PRD.md
[A2]: ../../execution/PKG-02/DEL-02-02/Design/WORKSPACE_AND_REGISTRATION.md
[A3]: ../HOST_INTEGRATION.md
[A4]: ../../app/README.md
[A5]: ../ARCHITECTURE.md
[A6]: ../EXAMINATION.md
[I1]: ../../app/src-tauri/src/workflow_trials.rs
[I1T]: ../../app/src-tauri/src/workflow_trials_tests.rs
[I2]: ../../app/src-tauri/src/trial_flows.rs
[I3]: ../../app/src-tauri/src/native_requests.rs
[I4]: ../../app/src-tauri/src/host_tick.rs
[I4B]: ../../app/src-tauri/src/lib.rs
[I4T]: ../../app/src-tauri/src/stop_records_host_tests.rs
[I5]: ../../app/src/exactText.ts
[I5B]: ../../app/src/App.tsx
[O1]: ../../execution/PKG-01/DEL-01-02/Design/NATIVE_WITNESS_2026-10-10.md
