# Governance Requirements Charter — Chirality Root (retained PRD lineage)

> **Owner merge-policy amendment — 2026-09-12.** D-8 and §5.3.1 below now
> record standing Git authorization for `sgttomas/chirality`, approved by Ryan
> Tufts in the HELP_HUMAN session and applied through this PR. This specific
> amendment supersedes the earlier merge defaults and K-MERGE-1 wording;
> it does not adopt the unrelated prospective migration clauses in this file.
> Revision 8 control and earlier candidate records below describe their
> historical bases, not the current merge-execution policy.

> PROSPECTIVE EXACT POST-IMAGE — NOT APPLIED. The runtime migration authority contract controls the named successor clauses only after its actual owner acceptance and effective propagation. Prior ratification remains the basis for unaffected requirements; historical product completion/ownership statements are prospectively superseded as specified below. No product gate, release or Root retirement is declared complete by these draft bytes.

> **Current status: ACCEPTED — Revision 8 is the current Root product
> basis.** D-GOV-31 adopted the exact Revision 7 candidate on 2026-07-29;
> the owner then simplified its merge-execution policy by direction recorded
> in `execution/_Coordination/LOOP_RECEIPTS.md` Receipt 64, arriving through
> PR review under the terminal-artifact rule (D-1). The Revision 8 policy
> became effective at
> `main@602dd71b8c123d8a47a36644db1453f515c0f778`.
>
> **Revision 8 reconciliation limit (historical).** That status layer and
> §10.5 reconciled document control only. They do not change any stable
> commitment, provenance-origin label, scope item, objective, count, or
> substantive requirement at that time. The 2026-09-12 amendment above now
> supersedes D-8 and annex §5.3.1 for merge execution.
>
> **Historical control preserved.** The following Revision 7 candidate-control
> block is retained as proposal history. Its references to “this candidate,”
> “current accepted product basis,” and pending adoption describe the state at
> Revision 7 candidate drafting; they do not override the current Revision 8
> status above or §10.5.
>
> **Status: `ADOPTION-READY — adopted only by the instrument named below`.
> Revision 7 amendment candidate (Candidate B — shared-CHANGE merge-gate scope).**
>
> **Current accepted product basis.** Revision 6 was adopted by D-GOV-28.
> Its placement copy is `docs/PRD_ROOT.md` at
> `main@4f7808acb2802443370d045efa198152934c1674` (sha256
> `0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d`).
> That accepted basis remains in force unless a later owner act adopts this
> candidate.
>
> **The adopting instrument** is D-GOV-31 using the exact-candidate-SHA
> pattern. Per the D-GOV-28 precedent, the D-GOV-31 decision record is
> created at adoption and carries any adopted status; this file never does.
> File creation, validation, commit, Git transport, review, or an owner
> selection between the two prepared candidates is not adoption. No
> SCOPE_CHANGE gate is approved by this candidate.
>
> **Minimal change envelope.** This candidate supersedes exactly one stable
> commitment: the §5.3 D-8 row ("never self-merge") is replaced by a
> successor merge-gate policy carried in the new annex §5.3.1, scoped
> to the shared change-management (CHANGE) role across all registered loops, with the M6 notice obligation stated in the annex. Document control is reconciled to Rev 7. Every other
> passage is byte-identical to the adopted Rev 6 placement copy; the exact
> changed-line set is declared in this candidate's `POLICY_DELTA.md`.
>
> **Authority and provenance.** This file confers no authority of its own
> (K-AUTH-1). The successor D-8 policy alone is new; it is labeled PROPOSED
> and takes effect only through an owner ruling in D-GOV-31 against this
> exact candidate. Inherited Rev 5 and Rev 6 provenance labels are retained
> without retroactive relabeling; TRANSCRIBED passages remain warranted only
> by their cited sources. Nothing here claims retroactive cure of any
> historical act.
>
> **InheritedSourceCorpusBasis:** `main@7ac718c7e` — the Rev 5 source corpus
> against which its inherited provenance labels were authored and reviewed.
> **Rev6AmendmentBasis:**
> `main@918bb48b8fcee66c031d0d6d4040a46089f96067` — retained basis for every
> sentence introduced or textually changed by Rev 6.
> **Rev7AmendmentBasis:**
> `main@4f7808acb2802443370d045efa198152934c1674` — the basis for every
> sentence introduced or textually changed by this amendment.
> **SourceCorpusBasis (composite):**
> `Inherited=main@7ac718c7e; Rev6Amendment=main@918bb48b8fcee66c031d0d6d4040a46089f96067; Rev7Amendment=main@4f7808acb2802443370d045efa198152934c1674`.
> This named composite is the Rev 7 D-14 source basis paired with the
> containing candidate commit; the component fields preserve which
> population was checked where.
> **Revision history:** Rev 1 `f15d51277`; Rev 2 `a72c2cd06`; Rev 3
> `f9d33fcd9`; Rev 4 `ae5a476f4`; Rev 5 adopted by D-GOV-22, candidate
> `d9ea86f88504cb8d859a4cf3f042bac00d38fe57`, accepted-candidate
> `90fae458bf485412e9c3a6295df193eb323c9774`; Rev 6 adopted by D-GOV-28,
> accepted-candidate `f78a83621cbd679e6af2c41199845aca74073480`, subject
> sha256 `0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d`.
> This Rev 7 candidate is attributable to its eventual containing commit; it
> asserts no SHA for itself.
> **Date:** 2026-07-29

---

## Provenance key

Every requirement, objective, and identity claim carries exactly one label.

| Label | Meaning | Reliance |
|---|---|---|
| **TRANSCRIBED** | Accepted or ratified doctrine, cited to its governing clause. Inherited Rev 5 labels retain their Rev 5 source-corpus verification; every exact-source sentence introduced or textually changed by Rev 6 is verified against the Rev6AmendmentBasis by the proposal-local validator. | In force because its source is in force — not because this document repeats it |
| **OWNER_DECLARED** | Owner-endorsed framing or an owner ruling **as transcribed or synthesized by Agent 0 in-session**. Exact wording is subject to owner confirmation or correction at adoption. **Not claimed verbatim unless quote-fenced.** | Not in force as doctrine; an in-session ruling is an owner act of record that becomes SHA-bound at the adoption instrument |
| **OBSERVED** | A **verifiable repository fact** — what a non-binding live surface says, or what git history shows — cited to file and line, carrying **no** doctrinal force. Distinguishes "this text exists in the tree" from "this text governs". | None. An OBSERVED item may be true and still bind nothing; it supports no reliance claim |
| **CLARIFIED** | An interpretation of accepted truth produced by the 2026-07-25 root-PRD inquiry (Agent 0 plus independent second-agent review, owner-mediated). Interpretation, not new authority. | Reading aid; the cited source governs |
| **PROPOSED** | A commitment that was new at the revision where it was introduced. The seventeen Rev 5 items carrying this label were accepted by D-GOV-22; O-11, newly proposed by Rev 6, was accepted by D-GOV-28; the D-8 successor merge-gate policy (§5.3 row D-8 and annex §5.3.1) originated as newly proposed by Rev 7. | The D-8 successor relies on D-GOV-31 as simplified by the owner direction recorded in Receipt 64 (Revision 8); the Rev 5 items rely on D-GOV-22; O-11 relies on D-GOV-28. The provenance-origin label is retained and does not imply current inertness. |

Quote fences (`>`) appear **only** around text warranted as verbatim, with its
record cited. Synthesized owner framing is presented as ordinary prose.

---

## 1. Governance identity and retained genus history

### 1.1 What Chirality Root is

**ID-0 — Historical ruled genus. [OWNER_DECLARED — preserved owner ruling of record]** The owner
ruled **RD-1** in-session on 2026-07-25, selecting the two-level formulation.
The ruled genus text:

> "Chirality Root is the canonical human-governed application environment
> and generative operating form for governed professional knowledge work.
> It contains a filesystem-native agent operating system together with the
> normative basis, developmental machinery, evidence, and human judgment
> by which that operating system is formed and governed."

*Ruled in-session; recorded in Receipt 37; SHA-bound at the adoption
instrument (RD-3). Selection and ruling mechanics are at §9.1.*

**Prospective identity reconciliation.** The quoted RD-1 genus remains an exact historical owner act. After effective migration, Root is the canonical human-governed repository control plane and shared instruction/tool steward; the generative operating form remains a governance method, not a continuing Root product working-root exception. This exact amendment prospectively supersedes the Root product implication of RD-1 as carried by D-GOV-22/23/24; it does not rewrite those records. DIRECTIVE §1 must adopt the paired exact successor paragraph before concordance can be claimed.

**PRD §1 ID-1 replacement — Governance and instruction stewardship.** Chirality Root is the human-governed repository control plane and the steward of shared instructions, tools and governance. Project roots own their product contracts, implementations, delivery scope and product evidence. Root maintains its own instructions through governed change tranches; that responsibility does not require or create a continuing Root product decomposition.

**PRD §1 ID-1a replacement — Explicit retirement of the product exception.** D-GOV-21's independently accepted Root product working-root exception remains historical and governs temporary custody until the effective transfer and retirement acts. On effective retirement, Root ceases to be an active product working root and root execution/ ceases to be an active product materialization surface. It remains the home of governance coordination and preserved historical product evidence. Separately authorized instruction changes continue under M2/G4; they do not acquire authorization merely from containment or from this declaration.

**ID-2 — Human judgment is the governing hinge. [OWNER_DECLARED]** Only humans
author binding approvals; agent capability never confers authority; the
permanent accountability gap is why the hinge cannot be automated away.
*(Agent 0 synthesis; not verbatim.)* Supporting accepted doctrine
**[TRANSCRIBED]**: K-AUTH-1 (`docs/CONTRACT.md` §1.2); `AGENTS.md` §Delegation
and Entry Rules ("Delegation never implies capability inheritance … A child's
capability does not become a parent capability"); D-GOV-19 ruled proposition 5
(the permanent non-identity between externalizable information and accountable
knowing); D-GOV-17 (capability never confers authority regardless of steering).

**ID-3 — Historical lineage (owner testimony). [OWNER_DECLARED]** The owner
attests roughly three years of prior development lineage preceding this
repository. No in-repo source states this.

**ID-4 — In-repo history (git fact). [TRANSCRIBED]** This repository's git
history begins at commit `7bee9ae41`, "Initial migrated Chirality repository",
2026-05-18; no commit predates that month. `docs/DIRECTIVE.md` §2.2 ("Git Is
the Event Store") makes git the development record of record. ID-3 and ID-4
are stated separately and are **not** blended. See historical conflict
**C-3**, closed by D-GOV-22 (§10.2).

### 1.2 Historical genus concordance before this migration

**[CLARIFIED — current disposition]** D-GOV-23 applied the RD-1 two-level
genus to `docs/DIRECTIVE.md` §1 and closed C-1. D-GOV-24 completed propagation
across the remaining governed self-descriptions and records that the
contained-level phrase "agent operating system" remains valid for the
instruction surface. The README propagation was also completed. The Rev 5
"concordance pending" state is therefore satisfied by accepted later acts;
this Rev 6 candidate records the current state rather than reproducing the
closed divergence. Falsifier F5 remains a standing test against future
unrecorded divergence.

### 1.3 Authority limit

**[TRANSCRIBED]** It holds no professional authority. Agent outputs are drafts
and structured assistance (`docs/DIRECTIVE.md` §3.1); "Agent outputs carry no
professional authority" (§3.4); a green validation is structural evidence only
and never certification (K-DOMAIN-4; D-GOV-02 — BLOCK never means globally
proven safe or unsafe).

---

## 2. Problem and human users

### 2.1 The problem

**[TRANSCRIBED]** `docs/DIRECTIVE.md` §1 states three purposes: accelerate
deliverable-heavy work by structuring agent workflows around production
deliverables and decomposed knowledge; make agentic work auditable and
controllable so outputs can be relied upon in professional, regulated, and
high-stakes contexts; and keep humans in charge at every decision gate while
agents handle drafting, extracting, reconciling, decomposing, and organizing.

**[TRANSCRIBED]** The diagnosis (§2, epistemology): the problem "is not that
they produce bad outputs — it is that bad outputs are indistinguishable from
good ones by inspection." The response is to make epistemic status transparent
and auditable rather than to make the model more reliable. The load-bearing
architectural commitment (§1): "if the filesystem is the database,
architecture is a state-and-authority specification, not a service mesh."

### 2.2 Applicability

**[TRANSCRIBED, corrected in Rev 2]** Chirality Root is for **governed
professional knowledge work generally**. The clause at `docs/DIRECTIVE.md` §3
("This section applies when the system is used in environments where
deliverables are safety-significant, contractually binding, subject to
codes/standards, or produced under professional responsibility") states the
**activation boundary of the professional-responsibility model** — the point
at which §3's additional provisions become load-bearing — **not** the
applicability boundary of the product.

### 2.3 Users, actors, and consuming contexts

Agents and working roots are **not users** in the product sense. Two
distinctions are drawn below: **strata** (who or what interacts with the
product) and, first, **capacities** (which authority a person is exercising).

#### Human capacities are separable [CLARIFIED]

Four distinct capacities may be held by four different people. **Holding one
confers none of the others.**

| Capacity | What it authorizes | Governing source |
|---|---|---|
| **Root-governance authority** | Ruling on shared repository governance: authoring binding governance records, ratifying, superseding. | K-AUTH-1; D-GOV-04 identity matching against `docs/governance_harness/human_actors.md` |
| **Professional accountability for situated work** | Accepting scope and design basis, adjudicating technical conflicts, accepting residual risk, and issuing situated deliverables for reliance. | `docs/DIRECTIVE.md` §3.2 engineer-of-record principle |
| **Review** | Assessing whether work may be relied upon; gating a lifecycle transition; returning findings that stop or redirect work. | `docs/DIRECTIVE.md` §2 (epistemic architecture); the REVIEW gate role |
| **Product maintenance** | Changing the instruction surface, tools, skills, and harness under governance. | D-GOV-21 M2; `docs/SPEC.md` §0.2.1–§0.2.2 |

**Explicitly:** a professional practitioner does **not** thereby obtain
root-governance authority, and the root owner does **not** thereby become the
accountable professional for situated work in a variant. At the accepted basis
all four capacities happen to be held by one person; **that is a fact about
the present instantiation, not a property of the product.**

**[CLARIFIED] What the rulings settle here.** Under **RD-2** (RULED — A1+B2,
§9.2) v1 scopes jurisdiction to a single root owner and accountability to one
accountable owner per root; under **RD-5** (RULED — A with a staged
trajectory, §9.5) v1 targets the present owner-practitioner. **v1 therefore
need not support the four capacities being held by four different people** —
but the separability above is a property of the capacities themselves, not of
the v1 configuration, and it is what the B and C stages of the RD-5 trajectory
would exercise.

#### Strata

| Stratum | Who / what | Notes | Label |
|---|---|---|---|
| **Primary human users** | People exercising root-governance authority or professional accountability for situated work — directing governed work, ruling, approving, adjudicating, accepting residual risk, issuing for reliance. | The only actors who can perform the acts K-AUTH-1 reserves. Presently one person is registered as a permitted author of binding governance records (`docs/governance_harness/human_actors.md`) — which registers *that* capacity only, not the others. | CLARIFIED |
| **Secondary human users** | People exercising review or product-maintenance capacity: reviewers, auditors, maintainers, and people assessing whether work may be relied upon. | **They act, they do not merely observe** — a reviewer may gate a lifecycle transition or return findings that stop work, and a maintainer changes the instruction surface under governance. They do not thereby acquire root-governance authority. Their needs drive the epistemic architecture (`docs/DIRECTIVE.md` §2). | CLARIFIED |
| **System actors** (not users) | Agent 0 / Agent 1 / Agent 2 instances; deterministic tools; the runtime daemon and its clients. | `agent = LLM + instructions + declared files/context + tools + permissions` (`AGENTS.md`) — "an operational definition, not a claim of personhood or professional responsibility". They execute within permission boundaries and never hold authority. | TRANSCRIBED |
| **Consuming contexts** (not users) | `projects/*` and `domains/*` working roots; desktop-harness user-selected folders; other situated working roots; the public export. | They bind `{WORKING_ROOT}` against the one instruction root. They may extend the invariant catalog but MUST NOT weaken it (`docs/CONTRACT.md` §1). | TRANSCRIBED |

**Whom v1 is *for* is RULED as RD-5** (§9.5): **v1 = the present
owner-practitioner**, on a staged trajectory toward individual professional
knowledge workers generally and then multi-practitioner organizations. RD-2
(§9.2) is a separate question and answers a different one: governance
jurisdiction and act-level accountability, not product user scope.

---

## 3. Objectives and v1 success conditions

**Why this section exists.** `docs/DECOMPOSITION_STANDARD.md` requires a
conforming decomposition to derive **objectives from its source** (invariant
I7; Completeness requirements — "Objectives derived"). If this PRD becomes
that source, it must state objectives, or decomposition will have to infer the
product's direction from constitutional statements.

**Governance readiness boundary. [PROSPECTIVE successor to the D-GOV-22 v1 boundary]** Root readiness requires (a) accepted coverage of all 46 retained governance duties and all 104 historical scope dispositions; (b) an actually completed bounded governance/instruction change with source discovery, declared scope, checks, independent review, owner acceptance and Git closeout; and (c) an actual runtime-project governed run with recorded shared-instruction convergence. G0–G4 must validate the declared governance/historical mode. These are evidence obligations, not conditions falsely claimed complete by preparing successor records. The previous Root-product end-to-end stream and materialization predicates cease to be future Root requirements at effective retirement; their historical results remain preserved.

The seven stable objective IDs remain reserved. The unchanged discoverability, evidence-linkage, promotion and continuity duties retain their accepted substance and provenance; the specifically replaced clauses below require this new attributable act. Project product acceptance remains the owning project's responsibility.

| # | Objective | Governance success condition (testable) |
|---|---|---|
| **OBJ-1** | **Coherent and discoverable normative authority.** A reader can determine what governs, from the repository alone. | For every governance surface in the instruction root, a reader can determine without asking a person: which document is authoritative for a given question, whether it is ratified, and what superseded it. No ratified clause has an unrecorded conflicting live variant. *(C-1 and C-2 are historical closed examples; §10.2.)* |
| **OBJ-2** | **Governed production supported by accountable governance.** | GOV-03-06 demonstrates a bounded Root governance/instruction change through declared scope, implementation, independent checking and human acceptance. GOV-06-08 demonstrates actual bounded runtime-project operation on the accepted instruction basis. Every consequential acceptance, reliance and issuance judgment remains accountable-human work; objective tool preconditions remain lawful non-human gates. Root does not need a new product deliverable stream. |
| **OBJ-3** | **The human evaluation and iteration loops close.** Humans can evaluate and redirect on evidence. | **Two conditions, one universal and one sampled.** **(i) Structural completeness — universal:** *every* accepted change has a retrievable linkage from files alone between the evidence that informed it, the ruling that accepted it, and the state it changed. A missing link is a defect regardless of sampling. **(ii) Retrieval usability — sampled:** the linkage can be *followed* within a bounded time, verified as a retrieval exercise where **the time threshold and the tranche sample are fixed and recorded before the evaluation runs** — not chosen after seeing results. Completeness is a property of the record; usability is measured, not asserted. |
| **OBJ-4** | **Governed instruction self-maintenance without self-authorization.** | Failure falsifiers F1–F3 remain unobserved in the declared governance run population, supported by recorded observation evidence; no newly produced capability becomes the run's governing basis before acceptance; governance G0–G4 pass for each applicable change. Historical materialization findings stay historical. GOV-06-01 supplies the evidence contract. |
| **OBJ-5** | **Situated specialization with governed convergence.** Variants specialize; useful patterns come back lawfully. | **(i)** At least one candidate pattern originating in a situated working root reaches a **complete promotion disposition — accepted, rejected, or deferred with its evidence recorded** — through the developmental machinery with its evidence linkage intact. **A rejection or reasoned deferral satisfies this**: the objective tests that the pathway works, not that any candidate deserves promotion; no promotion is forced to pass v1. **(ii)** **Every root change that claims variant-derived provenance used the governed promotion path.** *(Stated positively and checkably against changes that make the claim — rather than as an unprovable negative about all changes by every possible route.)* |
| **OBJ-6** | **Reconstructible Root governance concurrency.** | For every Root governance run record under execution/_Coordination/, write ownership, dependencies and pending gates are reconstructible; interrupted, abandoned and crashed runs are detectably stale/orphaned. Sibling targets are disjoint or serialized. Cross-project references convey coordination, not ownership of client production or a new aggregated product function. GOV-06-02 supplies the review contract. |
| **OBJ-7** | **File-native continuity and recoverability.** Nothing load-bearing lives outside the checkout. | The full governed state — decisions, approvals, scope, evidence, and each loop's current position — survives loss of every non-file substrate (chat context, model memory, daemon state, local caches) and is recoverable from the checkout alone. |

The runtime-owned partition of product objectives is carried by its separately accepted charter and seven-carrier decomposition. Root governance coverage uses the 46 control instruments and source mapping; ordinary project decomposition still conforms to I7. An unmapped duty is an open defect, not permission to omit it. These replacements do not assert that any old demonstration passed.

**[CLARIFIED] Reading the objectives under the ruled v1 user scope.** RD-5 is
RULED at **A** — the present owner-practitioner (§9.5) — so "user" in OBJ-1,
OBJ-2, and OBJ-3 means that practitioner for v1. **OBJ-1's discoverability
condition still has independent content under A**, because the ruled scope is
not a terminus: the owner ruled a **staged trajectory** in which learning from
A produces a version for B (individual professional knowledge workers
generally) and then C (multi-practitioner organizations, the stated target
maturity). A product built only for its own author could satisfy
"discoverable" trivially; a product expressly built *toward* B and C cannot,
because the B stage is what a reader who did not build it must survive. The
trajectory is the reason OBJ-1 is tested rather than assumed at v1.

---

## 4. The four functional categories and their human-governed loop

### 4.1 The categories

**[PROSPECTIVE successor]** Four functional categories describe Root governance and its relationships to project work; they do not constitute a continuing Root product decomposition:

| Category | What it is |
|---|---|
| **Normative basis** | The ratified governance corpus and invariants |
| **Operative work** | Root instruction/tool stewardship and independently owned project products, including the runtime |
| **Developmental machinery** | Governance harness, decision records, loops and guards for accountable changes under each owning scope |
| **Evidence** | Receipts, run records, snapshots, audits — the record that makes reliance answerable |

### 4.2 The generative loop

**[OWNER_DECLARED]** The categories are related by a loop, not a partition
*(Agent 0 synthesis; not verbatim)*:

```text
normative basis        ──constrains──▶  operative work
operative work         ──produces────▶  artifacts and evidence
evidence               ──informs─────▶  human evaluation
developmental machinery──produces────▶  candidate changes + iteration evidence
human judgment         ──accepts / rejects / redirects──▶
accepted acts          ──change──────▶  normative or operative state ──▶ (loop)
```

The hinge is human judgment (ID-2): the loop has no closing step that an agent
can perform.

#### Three distinct human judgments [OWNER_DECLARED]

The single "human judgment" step above resolves into **three judgments that
must not be collapsed** *(Agent 0 synthesis; not verbatim)*. The first two are
loops in the diagram; the third is a lifecycle judgment that draws on both:

| Judgment | Input | Decides | Question it answers |
|---|---|---|---|
| **Evaluation judgment** *(loop)* | Operative evidence — the artifacts, claims, and records that operative work produced. | Accept, reject, or redirect **the work**. | Is this work good enough, and for what reliance? |
| **Iteration judgment** *(loop)* | Developmental candidates plus iteration evidence — proposed changes to the product itself and the record of how prior changes fared. | Accept, reject, or redirect **the change to the product**. | Should the product itself change, and in this way? |
| **Release judgment** *(lifecycle gate)* | **Both** operative evidence and developmental evidence, plus validation results, decomposition coverage, and guard state. | Whether **the current product state may be released**. | Is what exists now fit to be released, as it stands? |

**Release is not iteration.** It asks whether the present state may go out, not
whether the product should change; a release judgment may be "no" with no
change proposed, or "yes" with changes pending. It is **separately
human-gated** (§8.3).

**None is delegated to machinery.** Deterministic tools, guards, and validators
supply findings to all three and gate objective preconditions; they never
perform any of the judgments (K-AUTH-1; D-GOV-02's observation-boundary caveat;
D-GOV-17 — a validator finding may never mechanically reject owner-ruled
content).

**Why the distinctions matter here.** They have different inputs, failure
modes, and evidence needs. Conflating evaluation and iteration would let a
product-level change ride in on deliverable-level evidence, or block a sound
deliverable because the machinery that produced it is under revision. Folding
release into iteration would imply that nothing can be released without
changing something, and that a decision to change is a decision to ship.
OBJ-3 tests that the two loops close; §8.3 governs the release gate.

### 4.3 What the categories are and are not

**[CLARIFIED]**

- They classify **functions and authority relationships**, not filesystem
  buckets.
- They are **non-exclusive**. One artifact may participate in several.
  `AGENTS.md` is normative basis (K-AGENTS-1 makes it an authoritative
  governance surface), operative product (it is the live index agents execute
  against), and — through its change-notice rule — developmental machinery. A
  decision record is developmental machinery and evidence, and its ruling
  **establishes normative or operative accepted state according to its scope**
  — a ruling may settle a governance rule, an operative arrangement, or both,
  and does not invariably become normative basis.
- They **do not prescribe four packages** or authorize new Root product materialization. D-15 requires governance-control coverage; project product partitions remain subject to the ordinary decomposition pipeline.

---

## 5. Stable governance requirements

> **D-GOV-41 prospective registry interpretation.** For the authorized Root
> candidate, references below to the live agent index resolve jointly to
> `AGENTS.md` and `agents/registry.json`; method-registry references resolve to
> `workflows/README.md` and immediate `workflows/*/WORKFLOW.md` packages.
> This relocates O-1/O-5's instruction and method surfaces and preserves their
> registry discipline. Historical transcription rows retain their original
> bytes and provenance. Incompatible downstream consumers remain on their
> accepted basis pending their owning-loop adoption.


**Registry discipline (anti-rot).** This section states **stable product
commitments** and incorporates **dynamic registries by reference**. It cites
registries, not their members: the invariant catalog (`docs/CONTRACT.md` §1),
the live agent index (`AGENTS.md`), the live skill registry
(`skills/README.md` plus `skills/*/SKILL.md`), the tool registry
(`tools/REGISTRY.md`), and the export profile
(`exports/chirality-app/export_public.py`). Where live registry and narrative
disagree, **the live registry governs and the discrepancy is surfaced**
(K-AGENTS-1). The full transcription inventory — every clause, anchor, and
verified line reference behind these commitments — lives in the concordance
annex (§10.1) and is regenerable from it.

### 5.1 Normative basis

| ID | Commitment | Label and source |
|---|---|---|
| **N-1** | **For authoritative governance and project-coordination state**, the substrate is git-tracked plain files: no external database, server state, or configuration holds that truth; rebuildable gitignored projections are permitted and never citable as authority; if a decision is not in a versioned file it does not exist for purposes of reliance. **Stated exception (K-DOMAIN-1): domain engines own authoritative domain truth** — canonical model files, model states, analysis runs, comparisons, solver outputs, and handoff internals are engine-owned, are sanctioned authoritative domain truth, and are exempt from the rebuildable-projection rule. Chirality governs the work *around* the engine (profiles, manifests, proposals, review notes, gates); it is not the solver and is never the source of accepted engineering truth. | TRANSCRIBED — `docs/DIRECTIVE.md` §2.1, §2.2, §5; D-GOV-01 (Option A) **and its scope note**; K-DOMAIN-1 (`docs/CONTRACT.md` §1.12) and the §1.12 note exempting engine-owned stores. **The exception is stated here, not only in the annex, because the annex is never adopted.** |
| **N-2** | The invariant catalog is the binding constraint set Root governance and project work must continue to satisfy. **Incorporated by reference**: the catalog governs its own membership; this PRD maintains no parallel list of `K-*` IDs. | TRANSCRIBED — `docs/CONTRACT.md` §1; K-AGENTS-1 live-registry principle |
| **N-3** | Human authority at every consequential gate: only humans author binding approvals; approvals bind to a specific git SHA and are voided by content change; approvals are always binding and only binding; gates are dynamic per project with a stated minimum, and no machine BLOCK on the issuance judgment may be non-overridable. | TRANSCRIBED — K-AUTH-1, K-AUTH-2, K-BIND-1, K-GATE-1; `docs/DIRECTIVE.md` §2.3 |
| **N-4** | Epistemic discipline is architectural, not advisory: mandatory provenance; unknowns become `TBD` rather than guesses; conflicts are surfaced with pointers, never silently resolved; claims are calibrated to their warrant. | TRANSCRIBED — K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-CLAIM-1; `docs/DIRECTIVE.md` §2.4 |
| **N-5** | Write containment is architectural: every agent has an explicit declared write scope; every scope path and write target resolves under the active checkout or the task stops; task outputs to tool roots are immutable snapshots. | TRANSCRIBED — K-WRITE-1, K-WRITE-2, K-SNAP-1; `docs/SPEC.md` §0.2.3 |
| **N-6** | The authority chain is DIRECTIVE (why) → CONTRACT (binding invariants) → SPEC (structures and path anchoring) → TYPES (vocabulary), with `AGENTS.md` and `agents/` as the live instruction surface. Where a lower or candidate document conflicts with ratified governance, ratified governance controls and the conflict is surfaced. | TRANSCRIBED — `docs/DIRECTIVE.md` §Authority chain |
| **N-7** | The four pillars — ontology, epistemology, praxiology, axiology — are the system's accountability ontology; ontology, praxiology, and axiology exist to serve the epistemology. | TRANSCRIBED — `docs/DIRECTIVE.md` §2 |
| **N-8** | The professional-responsibility model holds where it activates (§2.2): AI outputs are drafts; the licensed professional retains scope, code selection, hazard acceptance, adjudication, and issuance rights; competence includes tool competence; the hierarchy of authority runs laws → codes → project specifications → verified analysis → professional judgment. | TRANSCRIBED — `docs/DIRECTIVE.md` §3 |
| **N-9** | The normative basis is a **constituent of the product**, not documentation about it: the requirement is that the running system continue to satisfy the invariants, not that it describe them. | CLARIFIED — interpretation of `docs/CONTRACT.md` §2 (every invariant has a live enforcement point) |

### 5.2 Operative product

| ID | Commitment | Label and source |
|---|---|---|
| **O-1** | `REPO_ROOT` is the home of the **shared instruction surface** (`AGENTS.md`, `CLAUDE.md`, `agents/`, `skills/`, `tools/`, root `docs/`, `init/`, `.github/workflows/`) — the release-managed agent operating system (the **instruction root**; see `DIRECTIVE.md` §2.6). The instruction surface is read-mostly: changing it is a repo-wide governance action, not ordinary working-root execution. | TRANSCRIBED — D-GOV-27 effect 5; `docs/SPEC.md` §0.2.1. Both sentences are copied byte-for-byte and declared in the Rev 6 transcription specification. |
| **O-2** | Chirality operates through instruction artifacts, deterministic tools and executable runtime. Root owns shared instruction/tool governance; projects/chirality-runtime owns the runtime product. Tools compute findings and never substitute for semantic judgment. Runtime transport executes and carries work but never grants project authority; user-data runtime state remains operational rather than project truth. | PROSPECTIVE — exact runtime migration successor; inactive until accepted effect |
| **O-3** | The runtime delegation hierarchy is Agent 0 Supervising Architect → Agent 1 Manager → Agent 2 Specialist, with declared entry rules and no delegation below Agent 2; Agent 2 exists in three construction forms. **The live index and role membership are incorporated by reference** to `AGENTS.md`; this PRD enumerates no agents. | TRANSCRIBED — `AGENTS.md`; `docs/DIRECTIVE.md` §2 (praxiology); D-GOV-11, D-GOV-12, D-GOV-13 |
| **O-4** | Capability never confers authority. Delegation implies no capability inheritance; a child's capability never becomes its parent's; every child remains subject to sealed context, gate approval, path containment, enforced read/write scope, and durable evidence. | TRANSCRIBED — `AGENTS.md` §Delegation and Entry Rules; K-SEAL-1, K-GHOST-1; D-GOV-17 |
| **O-5** | Method packs (`skills/`) and deterministic operations (`tools/`) are maintained as **live registries**, and the live registry is authoritative over any narrative list. Membership is incorporated by reference to `skills/README.md` and `tools/REGISTRY.md`. | TRANSCRIBED — `AGENTS.md` §TASK Skill Capabilities; K-AGENTS-1 |
| **O-6** | The path model defines two roots (`REPO_ROOT`, `WORKING_ROOT`), one containment rule, and a closed `{*_ROOT}` token registry; instruction, coordination, and plan files MUST NOT embed machine-absolute paths. | TRANSCRIBED — `docs/SPEC.md` §0.2–§0.3 |
| **O-7** | Governed work is structured as execution instances containing flat packages and deliverables with stable IDs, a canonical lifecycle state file, and human-triaged staleness propagation. | TRANSCRIBED — `docs/SPEC.md` §1, §3; K-HIER-1, K-ID-1, K-STATUS-1, K-STALE-1/2, K-VAL-1 |
| **O-8** | Deliverable-local dependency registers are authoritative. **No central dependency graph is *authoritative*** — but derived and aggregated graphs are lawful coordination state: on-demand read-only aggregation is provided for, and `FULL_GRAPH` dependency mode computes blockers from the declared graph. | TRANSCRIBED — K-DEP-1 (which itself provides for on-demand aggregation), K-DEP-2; `agents/AGENT_PROJECT_SETUP.md` (`FULL_GRAPH` mode). |
| **O-9** | Product work executes under its declared project working root. Root governance/instruction work executes only under separately authorized repository change scopes, with M2/G4 on shared instruction surfaces. After effective retirement, the D-GOV-21 Root product materialization exception is closed to new activation. Historical Root product files remain non-selectable evidence, and the runtime project does not inherit an instruction-write exception. | PROSPECTIVE — exact runtime migration successor; inactive until accepted effect |
| **O-10** | The instruction, tool and runtime layers remain distinct; no fourth machine substrate is claimed and no layer grants project authority. Shared governance responsibility is not runtime product ownership. Root instruction changes remain governance acts with accountable human acceptance. | PROSPECTIVE — exact runtime migration successor; inactive until accepted effect |
| **O-11** | Continuing stewardship of the generic runtime belongs to projects/chirality-runtime. Consequential runtime semantic work requires its accepted project scope carrier, declared write locus and actual implementation gates. The project owns versioned contracts, affected-client conformance or migration fan-in, regression and release evidence, and returns release disposition to its accountable human. App, PEC or another client's implementation does not transfer runtime ownership to that client. Root retains repository governance and cross-project coordination, not permanent runtime semantic or product-release custody. | PROSPECTIVE — exact runtime migration successor; inactive until accepted effect |

#### Shared-runtime architecture — exact ownership successor with retained boundary transcription

The unchanged statements below retain their source authority in
`docs/governance_harness/_DECISIONS/D-GOV-20_shared_runtime_local_agent_pilot.md`
§Ruled architecture. They are repeated here to keep the Root/App/PEC boundary
and the credentials, sessions, adapters, transport, state, registration,
hierarchy, pilot, and export seams from being repartitioned by new paraphrase.
Item 1 is the exact prospective migration replacement; unchanged statements retain D-GOV-20 authority and any actual later amendments. The migration candidate itself is not an owner act.

Annex note (2026-09-12): items 2, 3 and 4 above are read with the superseding
instrument D-GOV-43 (`docs/governance_harness/_DECISIONS/D-GOV-43_codex_host_replatform.md`
and its A2 supplement), published at git SHA
`d2878462be59a43b4afc175a8cce85abca9cf696`: the App owns a Runtime service
child that hosts stock Codex, credentials are custodied by Codex, and the
per-user daemon, LaunchAgent and residency requirements are retired. The
transcribed text is not rewritten.

1. Chirality's executable agent harness is the projects/chirality-runtime product workspace with provider-neutral contracts, orchestration, daemon, client, CLI and safe engine adapters. The runtime project owns product semantics, implementation and release evidence; Root owns shared governance and instruction policy. Items 2–10 and security, residency, preserved-authority, exclusions and implementation gates remain subject to their existing later accepted amendments; changing the location and owning project supplies no additional capability.
2. One opt-in per-user headless daemon exclusively owns runtime engines, credentials, sessions, delegation, tools, turn locks, interruption, and local-model residency.
3. The packaged Electron application supplies daemon mode so the existing app identity and encrypted `safeStorage` credential boundary remain single-owner.
4. Local control uses an authenticated project-scoped HTTP/1.1 API over a protected Unix-domain socket. No TCP control listener is authorized.
5. Runtime state beneath user data is operational and non-authoritative. Governed project truth, manifests, instructions, AgentRuns, approvals, and acceptance evidence remain checkout-contained.
6. Tracked `chirality.project.json` manifests declare stable project identity and authority references without secrets or machine-specific absolute paths. Registration stores resolved local paths and approval metadata outside the checkout; authority-affecting manifest changes require explicit re-registration.
7. Agent 0, Agent 1, and Agent 2 remain authority and responsibility contracts independent of engine or model. No durable model-to-role preference is established.
8. Humans and external agents may invoke Agent 1 directly; Agent 0 may govern Agent 1 managers; Agent 1 may delegate Agent 2 workers; Agent 2 may not delegate.
9. The initial vertical slice is one real Agent 1 run that delegates one bounded read-only task to one Pi/oMLX Agent 2 using the explicitly resident model, reviews the return, and emits canonical evidence and actual-model attribution.
10. The generic runtime, CLI, contracts, and safe adapters are eligible for the public Chirality App export. Credentials, machine state, and private PEC or Piping adapters are excluded.

The candidate deliberately adds no further seam partition. Runtime behavior
or consumer facts not settled by D-GOV-20 are carried as stable open items in
the D-GOV-28 proposal package. Any later proposed boundary sentence must name
its source and pass the same exact-byte concordance check or return to the
owner as a new proposal.

### 5.3 Developmental machinery

| ID | Commitment | Label and source |
|---|---|---|
| **D-1** | **A design change is carried by one of two terminal artifacts: it supersedes a `D-GOV-*` record, or it arrives as PR review — never a new plan document.** Where the vehicle is a decision record, that record carries status, verbatim owner ruling, SHAs, date, framing, accepted basis, and record convention; the register is navigational and the per-decision records govern. | TRANSCRIBED **at that scope** — the terminal-artifact rule as stated in `docs/governance_harness/_DECISIONS/_REGISTER.md` (§Terminal-artifact rule, restated in §Now actionable): "Design changes from here supersede a `D-GOV-*` record or arrive as PR review — never a new plan document." Record structure: the `_DECISIONS/` records themselves |
| **D-2** | **Within the two record classes where the convention already governs**, corrections to ruled content are superseding acts, not edits: **(i)** published D-GOV decision records carrying the `supersede-never-edit` record convention — a later correction to a ruled record supersedes it; and **(ii)** ruled candidate packets bound to an `AcceptedCandidateSHA` — amending the candidate would void the SHA the owner's ruling approved. **This commitment asserts nothing beyond those two classes.** | CLARIFIED — reads the convention as it stands in its own scope: D-GOV-21 `RecordConvention` field and §Status note ("Any later correction to the transcription is a superseding act, not an edit"); D-GOV-17's recorded-exception protocol; the implementation handoff's "amendment would void the AcceptedCandidateSHA". **The broader change-control rule is carried separately at D-16 (PROPOSED)** — a CLARIFIED label cannot establish it. |
| **D-4** | Attribution of rulings and adoptions matches an owner-curated identity allowlist; identity-dependent checks **refuse rather than guess**. The list is owner-curated and not extended programmatically. | TRANSCRIBED — D-GOV-04; `docs/governance_harness/human_actors.md` |
| **D-5** | Validation is deterministic and severity-typed (BLOCK / REVIEW / WARN / INFO / NOT_APPLICABLE, with exit-code semantics and human-only recorded BLOCK override); "BLOCK" never means globally proven safe or unsafe; and a validator finding may **never** mechanically reject content the owner has ruled — where ruled text trips a validator, the validator is defective. | TRANSCRIBED — D-GOV-02; D-GOV-17; `docs/CONTRACT.md` §1.7 note |
| **D-6** | Phase-crossing work is bound by the governance integration rules — derivative-package, snapshot, handoff-state, closure, sequencing, cycle-resolution, and change-notice routing. **Incorporated by reference** to `AGENTS.md` §Governance Integration Rules. | TRANSCRIBED — `AGENTS.md`; `docs/DIRECTIVE.md` §2.7 |
| **D-7** | Root governance runs through its session-init contract, deterministic intent-plan pointer and append-only receipts. Coordination records do not acquire authority from existence. Current owner steers and accepted instruments govern; discrepancies are recorded. The runtime project maintains its own accepted product entry and evidence. | PROSPECTIVE — exact runtime migration successor; inactive until accepted effect |
| **D-8** | Current and subsequent agents may commit, push, open/update PRs, and merge authorized work under the owner's standing Git grant in §5.3.1 and K-MERGE-1. Required CI and independent review cover the actual candidate; explicit holds and later directions prevail. Git integration grants no governed acceptance or product release. | Owner amendment 2026-09-12; supersedes earlier per-merge defaults across registered loops; prior D-GOV-31/Revision 8 records remain historical. |
| **D-9** | The decomposition pipeline is not waivable: packages and deliverables come only from an accepted decomposition. Nothing authorizes inventing packages from discussion. | TRANSCRIBED — D-GOV-21 packet §4 |
| **D-10** | The public-export boundary is an explicit allowlist profile that copies allowlisted content, sanitizes private absolute paths, writes a manifest and report, and fails on forbidden paths or leaks. **The profile is the boundary contract and is incorporated by reference**; membership is not restated here. | TRANSCRIBED — `exports/chirality-app/export_public.py`; K-EXPORT-1 |
| **D-11** | A tranche changing surfaces that downstream loops pin or mirror ships a routed coordination notice to each affected loop in the same tranche. The notice is coordination, not authority: the receiving loop adopts, amends, or declines under its own instruments. | TRANSCRIBED — `AGENTS.md` change-notice rule; D-GOV-21 M6 |
| **D-12** | Developmental machinery is substantive governed work, with an accountable owner, declared scope, evidence and acceptance; it is not exempt overhead. Root instruction/tool changes use M2/G4 tranches and retained control duties. Project developmental products use their accepted product scope. No Root product decomposition is required merely to maintain shared governance. | PROSPECTIVE — migration successor; requires exact owner acceptance and effective application |
| **D-13** | Once adopted, this PRD is amended only by a superseding instrument bound to a git SHA, and each revision is a new attributable act. **Immutable accepted revision artifacts are never overwritten at their paths.** As an explicit narrow successor to the former same-path prohibition, the canonical doctrinal placement `docs/PRD_ROOT.md` may be replaced only after its exact prior accepted bytes have been preserved at a named immutable revision path and the superseding owner instrument binds both prior and successor SHA-256 identities. For this migration, the prior Revision 8 artifact is `execution/_ScopeChange/SCA-005_2026-09-05_2344/ADDENDUM_REVIEW/ACCEPTED_ROOT_PRD_REV8.md`. Future revisions must likewise preserve their immediate accepted predecessor at a new immutable path before replacing the doctrinal placement. This exception applies only to that named doctrinal placement; all other adopted immutable artifact paths and D-16 declarations retain their existing prohibition. | **PROPOSED** |
| **D-14** | **Source-currency obligation.** An adopted PRD that incorporates accepted doctrine carries a standing currency check over **nine classes** — invariant IDs still exist and still support what cites them; live registries still exist and still carry the relied-on rule; source anchors still resolve; repeated enumerations still match their registries; provenance labels and counts still reconcile and any change is linked to a valid superseding instrument; and concordance with `docs/DIRECTIVE.md` §1 holds. The classes are enumerated in annex §4, where **five are mechanical and four require semantic judgment**. It pairs the **SourceCorpusBasis** (the sources) with the **containing commit** of the adopted bytes (the candidate). **The check is not built** — no generator, schema, or executable check exists at this basis; building it is a precondition of relying on it. **A currency failure is a REVIEW finding routed to the owner — never an automatic amendment** (K-AUTH-1; D-GOV-02). | **PROPOSED** |
| **D-15** | All four functional categories in §4.1 have traceable coverage in the 46 governance controls or a recorded reasoned unresolved disposition, with all seven runtime responsibilities accounted for in the separately accepted runtime project. This replaces only the first-Root-decomposition coverage predicate; it neither declares controls satisfied nor waives any project decomposition pipeline. | PROSPECTIVE — migration successor; requires exact owner acceptance and effective application |
| **D-16** | **Attributable change control over approved content.** Any change to previously approved content requires a **new attributable act bound to the resulting SHA**, and prior approved bytes **remain recoverable in Git**. Only artifact classes **explicitly declared immutable** — decision records, accepted candidate packets, and snapshots — are never overwritten at their path. **Living authoritative surfaces amend in place through accepted commits**: `AGENTS.md`, `docs/DIRECTIVE.md`, `docs/SPEC.md`, `docs/TYPES.md`, status files, and other current-state surfaces are meant to be edited, and freezing their pathnames would break the product rather than protect it. | **PROPOSED** — pattern basis: D-2's two immutable record classes; K-SNAP-1 (pointer files may be overwritten, snapshot folders must not); K-AUTH-2 (approvals bind to a SHA). Stating it as a general change-control commitment is new and takes effect only on adoption |

**Retired identifier — D-3.** `D-3` is deliberately absent. The
exact-candidate-SHA procedure it once carried is **not a product requirement**;
it is an **OBSERVED practice statement** at §6.2, which makes no authority
claim. **The identifier is retired and never reassigned** — D-4 through D-16
keep their IDs so that every cross-reference in the annex, the prior revisions,
and this run's record stays valid, and no future commitment may reuse `D-3`.

#### 5.3.1 Merge-gate policy — the D-8 successor

**Owner standing authorization, 2026-09-12.** Ryan Tufts approved the
following policy in the HELP_HUMAN session and directed its implementation,
independent review, applicable checks, and PR merge under this authorization.
The owner's approving message was: "I approve this. Will you carry out the
changes and open a PR and merge as now intended?" The policy and ordinary PR
history are the durable record; no separate approval registry is required.

For `sgttomas/chirality`, current and subsequent agents have standing
authorization to commit, push, create and update pull requests, and merge work
within the scope the owner has authorized, without requesting separate approval
for each Git operation. This replaces earlier per-merge approval defaults in
Root and project-local instructions across the repository. Existing explicit
holds and later owner directions take precedence. It does not authorize work
outside the assigned scope.

**Candidate and review.** Merge when required CI passes and independent review
has no unresolved blocking findings. The reviewer must be separate from the
author. Review and validation must cover the actual candidate revision;
changes after review require reassessment of the affected checks. Verify the
source HEAD when merging. A passing rerun does not establish that a previously
identified defect was repaired. Preserve the review, check results, source
revision, and resulting merge in ordinary PR/Git history rather than another
receipt chain or approval-token scheme.

**Acting on the owner's behalf.** Use the owner's configured Git and GitHub
credentials. Push through the configured SSH remote where available; merge PRs
through GitHub using the owner's authenticated account, ordinarily via the
GitHub CLI or API. This grants no authority to change repository protections
or account permissions. Preserve truthful commit authorship and agent
attribution. Acting as the owner's authorized agent does not mean the owner
personally reviewed the changes; do not describe agent review as personal
owner approval.

**Boundaries.** This is conditional standing authorization for Git integration,
not acceptance of future governed content. K-AUTH-1/2 continue to govern human
acceptance and its binding to the accepted content. The grant permits no scope
expansion, bypass of repository protections, acceptance of governed deliverables
on the owner's behalf, product release or publishing, force push, or history
rewrite. Required semantic decisions remain with their owning workflows and
the human. Ordinary implementation and Git closeout within authorized scope do
not require another owner confirmation.

Historical exact-action approvals and their records remain valid for the acts
they describe. Their SHA fields and token conventions are not a required format
for future execution under this standing grant.

### 5.4 Evidence

| ID | Commitment | Label and source |
|---|---|---|
| **E-1** | Every orchestration run persists a durable, versioned record tree under `_Coordination/AgentRuns/<RunID>/` capturing plan, work graph, briefs, returns, notices, dispositions, amendments, and final handoff state. Run IDs are created only when a real run begins; placeholder runs and briefs presented as executed children are prohibited. | TRANSCRIBED — `docs/SPEC.md` §9.8; `execution/_Coordination/LOOP_INIT.md` §5 |
| **E-2** | Phase-boundary decisions terminate in immutable snapshots; stopping work emits an explicit handoff state; each lawful tranche appends a minimal receipt. | TRANSCRIBED — `AGENTS.md` snapshot and handoff-state rules; K-SNAP-1; `LOOP_INIT.md` §7 |
| **E-3** | The three SHA roles are distinct and recorded distinctly: the **owner act binds approved content to its candidate SHA**; the **publication SHA identifies the durable ruling record**; the **EffectiveSHA identifies applied state**. | TRANSCRIBED — K-AUTH-2; D-GOV-21 record header. |
| **E-4** | Claims carry epistemic labels and progress through the warrant lifecycle `UNWARRANTED → CITED → REVIEWED → AUTHENTICATED`; authentication is an accountable actor's scoped, purpose-specific, SHA-bound act that neither creates knowledge nor establishes truth. | TRANSCRIBED — `docs/TYPES.md` §10.3–§10.4; D-GOV-19 ruled proposition 4; D-GOV-08 |
| **E-5** | Read-only audit and evaluation surfaces exist and are governed; **membership is incorporated by reference** to the live agent index. | TRANSCRIBED — `AGENTS.md` agent index; `docs/DIRECTIVE.md` §4.1 |
| **E-6** | Validation evidence is written only under declared generated paths under the mutation-control contract; the harness never writes governed authority files, and governed-file mutation by a validation command is an unconditional BLOCK. | TRANSCRIBED — D-GOV-01; harness phase-4 record in `_REGISTER.md` |
| **E-7** | A scope unit or phase is not closed because files were written: closure requires accepted authoritative truth, regenerated or explicitly deferred derivatives, recorded audit status, and surfaced unresolved blockers. | TRANSCRIBED — `AGENTS.md` closure rule; `docs/DIRECTIVE.md` §2.7 |
| **E-8** | **Evidence completeness is not evidence sufficiency.** The provenance ladder measures whether warrant is present, never whether it is adequate for a given reliance purpose; adequacy is a human judgment against scope and purpose. | CLARIFIED — D-GOV-08 Option B as implemented ("completeness, never sufficiency"); K-DOMAIN-4; K-CLAIM-1 |

---

## 6. Governance self-maintenance and concurrency direction

### 6.1 Historical materialization and prospective retirement

D-GOV-22/25/27 and later accepted scope amendments remain the historical authority for Root product adoption and materialization. Their historical counts and lifecycle observations are not rewritten. After exact successor acceptance, all 53 source carriers and six parent packages retire non-destructively; source IDs remain reserved and files remain evidence. Exactly seven runtime carriers and 46 accepted governance duties must exist before source retirement becomes effective. No Root product queue is reactivated to perform the migration.

### 6.2 Governance self-maintenance discipline

Root instruction/tool work remains within declared and independently authorized tranches. No run may consume its newly produced capability as an accepted governing basis before accountable acceptance. Frozen basis, scope checks, independent evidence and human gates remain mandatory where applicable; neither containment nor G4 supplies authorization. Until effective transfer and retirement, Root retains temporary custody under the current accepted instruments. The proposed governance mode is not a fallback around an unready product guard.

#### The exact-candidate-SHA procedure — an observed practice, not a rule

**[OBSERVED]** A five-step procedure has been exercised three times on
substantial governance proposals: **commit the exact candidate**; **record its
SHA**; **have the owner rule on that exact commit, recorded verbatim in a
fence**; **publish the ruling as a separate durable record**; **record the
merged implementation commit**, returning for exact-prose re-acceptance if
implementation would change approved prose. The instances of record are
**D-GOV-18** (approval at an exact commit), **D-GOV-19** (candidate SHA plus a
separate exact-prose ruling), and **D-GOV-21** (packet §14 mechanics;
`AcceptedCandidateSHA` / publication / `EffectiveSHA`).

**This states what the record shows and claims nothing more.** The actual
invariant is **K-AUTH-2** — every approval binds to a specific git SHA and is
voided by content change — and K-AUTH-2 **admits other vehicles**: a PR
approval against branch HEAD satisfies it differently. No governing clause
requires this particular multi-SHA packet procedure of every substantial
proposal, and **this document asserts none**. The procedure is available when
consequence warrants it, and professional judgment selects the vehicle.

**[CLARIFIED]** Promotion of the pattern into a PROPOSED requirement remains
available if evidence later shows that selecting among approval vehicles
causes ambiguity or failure — as a governed default with stated criteria, or
as a mandatory rule with "substantial" defined. Leaving it OBSERVED is the
product's own movement applied to itself: practice supplies evidence, evidence
informs judgment, and judgment alone makes the rule.

### 6.3 Concurrency direction

**[PROSPECTIVE scope reconciliation]** The four accepted mechanisms continue to constrain Root governance work: fine-grained write ownership with disjoint or serialized targets (M1);
a frozen instruction basis per run, so an in-flight run never consumes a
sibling's candidate instruction change (M3); worktree isolation for concurrent
children (M4); and a pre-dispatch work-graph check validating declared and
disjoint write targets before dispatch (G3).

**[CLARIFIED]** These four are what make OBJ-6 achievable rather than
aspirational: legibility of concurrent work is a property of declared,
file-recorded write ownership — not of coordination held in conversation. As
concurrent Agent 0 activity grows, the binding constraint is that every active
run's ownership and gates remain reconstructible from `_Coordination/` state,
which is why work graphs are recorded **before** dispatch rather than after.

---

## 7. Variant specialization and governed promotion

### 7.1 Downward: root serves variants

**[TRANSCRIBED]** One instruction root serves many working roots —
`projects/*`, `domains/*`, and desktop-harness user-selected folders — without
per-workspace instruction drift. A working root may extend the invariant
catalog and may overlay or specialize the agent suite, but **MUST NOT weaken**
framework governance. The retired D-GOV-21 Root product exception extends to no project; explicitly governed in-tree v1 registration and external v2 registration retain their distinct containment contracts. Domain engines own authoritative
domain truth; the root governs the work around them without becoming the
solver. Variant and export membership are incorporated by reference (§5,
registry discipline); the detailed inventory is in the annex.

### 7.2 Upward: governed promotion (the reciprocal half)

**[PROPOSED]** The reciprocal relationship — how the product has actually
grown — is stated as a new commitment:

1. Variants **specialize** root patterns for particular forms of knowledge
   work.
2. Their observed friction and successful patterns **may return as
   evidence-linked root candidates**.
3. **No variant automatically changes or weakens root.** A pattern's success
   in a working root is evidence, not authority.
4. **Promotion occurs only through the root's human-governed developmental
   machinery** — a candidate, a ruling, and an accepted tranche (§5.3).

**[CLARIFIED]** §7.1 and §7.2 together are what "generative operating form"
would mean operationally: specialization downward, evidence upward, authority
only through the human hinge. OBJ-5's success condition tests whether the
upward half actually works.

---

## 8. Non-goals, falsifiers, and release authority

### 8.1 Non-goals

**[TRANSCRIBED — restated from D-GOV-21 packet §4, in force and constraining
this PRD]** No change to the public-export boundary; no extension of the root
working-root exception to any other working root or to desktop-selected
folders; no waiver of the decomposition pipeline; no blanket authority for
future root-structure changes; no change to K-AUTH-1, K-AUTH-2, K-BIND-1,
K-GATE-1, K-SEAL-1, or any invariant or clause not named in packet §3.

**[TRANSCRIBED] Non-goals of this document specifically:** it adopts, accepts,
and ratifies nothing including itself — adoption is the named instrument's act,
performed by the owner (K-AUTH-1); it **records** the five owner rulings of §9
but performs none of the follow-on obligations they create, including the §9.1
concordance obligations; it creates no `PKG-*`/`DEL-*` and authorizes no
materialization;
it changes no instruction-surface file (any such change is an M2 governance
tranche requiring independent owner authorization); it does not re-litigate
the philosophical framework or thesis (governed by D-GOV-19; `docs/thesis/`
stands at CITED/REVIEWED, **not** AUTHENTICATED); it is not a roadmap
(`docs/PLAN.md` remains the roadmap surface); and it resolves none of the
conflicts in §10.2 — surfacing them is the act, ruling on them is the owner's.

**[CLARIFIED] Not decomposition.** This revision adds direction, not
partition. No packages, deliverables, acceptance tests, or priority rankings
are introduced; those are downstream, human-gated work under
`docs/DECOMPOSITION_STANDARD.md` and D-GOV-15/16.

### 8.2 Falsifiers

**[PROSPECTIVE successor observation contracts]** The six stable falsifier IDs remain reserved. Historical findings remain attached to their original subjects; no replacement relabels a finding PASS.

- **F1 — Containment failure.** A Root governance/instruction change corrupts the shared instruction basis relied on by a project, and the applicable declared-scope/frozen-basis/G0–G4/M6 controls fail to detect or gate the change.
- **F2 — Loop bypass.** Root governance work proceeds without the standing session-init, deterministic intent-plan pointer, append-only receipts and applicable independently authorized M2/G4/M6 change machinery.
- **F3 — Self-authorization.** A Root governance run consumes its newly produced capability as accepted governing basis before that capability's actual acceptance.
- **F4 — Requirements drift.** An accepted retained duty has no traceable governance successor or explicit unresolved disposition, or a transferred runtime scope row cannot be traced to its accepted project charter. Historical first-decomposition coverage remains evidence; it does not substitute for this current map.
- **F5 — Concordance failure.** The accepted Root charter and DIRECTIVE §1 contradict each other about ownership or identity without an explicit superseding act.
- **F6 — Label decay.** A provenance label changes without a superseding instrument, or an unaccepted proposed item is relied upon as adopted.

### 8.3 Release authority

**[PROSPECTIVE ownership successor; human gate retained]** Root instruction/tool publication and runtime product release are separately scoped human judgments. Root governance retains universal release policy and its own instruction-release assurance (GOV-06-07); the runtime project assembles its product release evidence and proposal. Each accountable human judges the actual release subject using operative and developmental evidence, applicable coverage and guard state. No CI result, migration, merge, control record or owner transfer is itself release approval. Universal K-AUTH-1 and existing client-specific release gates remain unchanged.

**It is not an iteration decision.** Release asks whether what exists may go
out, not whether the product should change. A release judgment may be negative
with no change proposed, or positive with changes pending; neither outcome is
a decision to change the product.

**[TRANSCRIBED] Supporting basis:** K-AUTH-1 (only humans author binding
approvals; no agent may issue work for reliance); D-GOV-02 (a BLOCK is
mechanically bounded to its declared observation boundary and never a global
safety verdict); `docs/DIRECTIVE.md` §7 (the runtime pilot "does not authorize
… release, publication, issuance, or professional reliance"); K-DOMAIN-4
(validation-passed is necessary, not sufficient).

---

## 9. Historical owner decisions — five predecessor decisions RULED

D-GOV-21 packet §11 expressly withheld four decisions and routed them here;
the first adversarial review identified a fifth. **All five are now ruled by
the owner, in-session, 2026-07-25.** This section is the **record of what was
decided** — the option slates are compressed to what was offered and what was
selected; the full slates as presented, with their consequences, remain in the
immutable prior revisions and in this run's briefs and reviews.

**Status of these rulings.** Each is an **owner act of record**. Recorded here
with its verbatim selection; **SHA-binding occurs at the adoption instrument**
(RD-3, §9.3), not in this file. Receipts of record: **Receipt 37** (RD-1) and
**Receipt 38** (RD-2..RD-5) in `execution/_Coordination/LOOP_RECEIPTS.md`.
Where a ruling diverges from an agent or reviewer recommendation, that is
recorded rather than smoothed over.

| # | Question | Ruling | Recorded at |
|---|---|---|---|
| **RD-1** | Genus wording | **C — two-level formulation** | §9.1 |
| **RD-2** | Jurisdiction and accountability | **A1 + B2**, with a declared evolution path | §9.2 |
| **RD-3** | Adoption instrument and concordance map | **A + y** | §9.3 |
| **RD-4** | Placement vs. the export boundary | **D — split with pointer** | §9.4 |
| **RD-5** | v1 user scope | **A**, on a staged A → B → C trajectory | §9.5 |

### 9.1 RD-1 — Genus wording · **RULED**

**Status: RULED** — owner, in-session, 2026-07-25. Recorded in Receipt 37.
**SHA-binding occurs at the adoption instrument** (RD-3), not here; this
section is the record of the act, not the act's binding surface.

**Selection, verbatim as recorded from the selection interface:**

> "C — Two-level formulation"

**Ruled genus text** — option C's formulation, originating in the first
independent adversarial review and reproduced exactly:

> "Chirality Root is the canonical human-governed application environment
> and generative operating form for governed professional knowledge work.
> It contains a filesystem-native agent operating system together with the
> normative basis, developmental machinery, evidence, and human judgment
> by which that operating system is formed and governed."

**The slate as presented** (retained so the ruling is legible against what was
offered):

| Option | Content | Disposition |
|---|---|---|
| **A** | Retain `docs/DIRECTIVE.md` §1's ratified genus; reword `README.md`. | Not selected |
| **B** | Adopt `README.md`'s genus; amend `docs/DIRECTIVE.md` §1. | Not selected |
| **C** | A two-level formulation: genus plus explicit differentia, stated once and propagated. | **SELECTED** |
| **D** | Defer: adopt with the conflict recorded and both variants cited. | Not selected |

#### Follow-on concordance obligations — historical record, now closed

The RD-1 ruling did not itself change a governance surface. It created three
separately governed obligations. Their current dispositions are:

| # | Obligation | Current disposition |
|---|---|---|
| **(a)** | Supersede the ratified `docs/DIRECTIVE.md` §1 genus clause through an exact-prose, human-gated act. | **CLOSED — D-GOV-23.** C-1 is closed. |
| **(b)** | Reword `README.md` to the ruled genus. | **CLOSED** as recorded by D-GOV-24's complete-propagation disposition. |
| **(c)** | Survey SPEC / TYPES / `AGENTS.md` prose and propagate where the ruled formulation changes the sense. | **CLOSED — D-GOV-24.** The contained-level uses that remain are deliberate. |

**[CLARIFIED]** The original sequencing remains evidence of why the acts were
separate: each instruction-surface change required its own owner authorization,
serialized integration, manifest, and routed notices. Rev 6 does not reopen or
repeat those acts.

### 9.2 RD-2 — Jurisdiction and accountability · **RULED**

**Status: RULED** — owner, in-session, 2026-07-25; Receipt 38. Two axes were
offered: **jurisdiction** (A1 single root owner / A2 owner plus named delegates
/ A3 governing body with a quorum rule) and **accountability** (B1 one
accountable human per consequential act / B2 one accountable owner per root).

**Ruling: A1 + B2**, with a declared evolution path. Owner verbatim:

> "A1+B2 could seemingly be scaled up to multi-practitioner using the PEC
> interface and a database, and attribution can be done more securely that
> way. If you agree I would go that way. And that database and PEC interface
> are not current scope. That can be something that may be incorporated as
> Chirality morphs and responds to usage with ongoing development and
> refinement."

**Agent 0 concurrence, recorded because the ruling was conditioned on it
[OWNER_DECLARED — Agent 0 act of record]:** Agent 0 agrees. The prior agent
recommendation in Rev 4 was A1+B1; the owner ruled **B2** with a scaling path,
and that is the ruling. The recommendation is recorded as not followed.

**What v1 carries [OWNER_DECLARED]:**

| Axis | Ruled for v1 | Effect on this document |
|---|---|---|
| **Jurisdiction** | **A1** — a single root owner governs the root. | Matches the live registry exactly (`docs/governance_harness/human_actors.md`, one registered actor); no delegation or quorum machinery is introduced. |
| **Accountability** | **B2** — one accountable owner per root, inherited by acts within it. | v1 does not require per-act accountability across multiple people; the four §2.3 capacities need not be separately held (§2.3). |
| **Sub-decision: who may amend `human_actors.md`** | **Status quo** — owner-curated; additions and removals are owner edits published by CHANGE; **not extended programmatically**. | TRANSCRIBED as it stands: D-GOV-04; `docs/governance_harness/human_actors.md` §Maintenance. Under B2 this follows from jurisdiction A1. |

**Evolution path [OWNER_DECLARED, expressly not current scope].** A1+B2 is
ruled as scalable toward multi-practitioner attribution mediated by the **PEC
interface with database backing**, which the owner states would also make
attribution more secure. **The database and PEC interface are not current
scope**; they may be incorporated as the product responds to usage through
ongoing development. A PEC-mediated future would also revisit the
`human_actors.md` sub-decision. *The referent of "the PEC interface" is not
resolved in this document; it is `TBD` rather than guessed (K-INVENT-1), and
the owner fixes it if and when that scope is opened.*

**Reconciliation with the substrate ruling [CLARIFIED].** Under **D-GOV-01**
(Option A, RULED 2026-07-01) git-tracked authored plain files are the **sole
authority** for Chirality governance state, and any database is a rebuildable
projection **never citable as authority**. A future PEC/database layer
therefore supplies the attribution **mechanism** while the authoritative
**record** stays file-native — unless a future ruling consciously amends
D-GOV-01. That amendment is not proposed here and would be its own governance
act.

**[TRANSCRIBED] Standing clarification, unchanged by the ruling.**
`docs/governance_harness/human_actors.md` identifies **permitted authors of
binding governance records** (D-GOV-04 identity matching). It is not a registry
of every person accountable for situated professional work, and B2 does not
make it one.

### 9.3 RD-3 — Adoption instrument and concordance map · **RULED**

**Status: RULED** — owner, in-session, 2026-07-25; Receipt 38. Three
instruments were offered (**A** a `D-GOV-*` record on the exact-candidate-SHA
pattern; **B** a dedicated PRD adoption record class; **C** the
corpus-ratification pattern) and two map forms (**x** one-directional,
requirement → DIRECTIVE §1; **y** bidirectional coverage matrix with uncovered
items marked `TBD`). Both carried the agent recommendation A+y.

**Selection, verbatim as recorded from the selection interface:**

> "A+y (Recommended)"

**What this fixes [OWNER_DECLARED]:**

| Element | Ruled |
|---|---|
| **Instrument** | A **`D-GOV-*` decision record** using the **exact-candidate-SHA pattern** over the exact bytes of this adoption-ready revision. It reuses machinery exercised three times (D-GOV-18/19/21 — see the §6.2 practice statement) and inherits register visibility and SHA binding (K-AUTH-2). |
| **Concordance map** | **Bidirectional** (form y): PRD ↔ `docs/DIRECTIVE.md` §1, with uncovered items on either side marked `TBD`. This is the artifact **F5** is checked against, and only the bidirectional form exposes drift in both directions. |
| **Sequencing** | **Historical selection, completed.** The adoption map was drawn against `docs/DIRECTIVE.md` §1 as it then stood and recorded the RD-1 divergence. D-GOV-23 later applied obligation (a) and closed C-1; D-GOV-24 completed the remaining propagation. |

**[CLARIFIED]** Choosing the D-GOV family means a product-requirements act is
hosted alongside governance acts. That was the offered cost of option A and is
accepted by the ruling; it is recorded here so the register's later readers
know the choice was deliberate.

### 9.4 RD-4 — Placement relative to the public-export boundary · **RULED**

**Status: RULED** — owner, in-session, 2026-07-25; Receipt 38. Packet §11 item
4 records this as a **publication decision**. Four placements were offered:
**A** root `docs/` (exported); **B** root `execution/` (not exported); **C**
root `docs/` with an export exclusion; **D** a split. No agent recommendation
was offered among A, C, and D — the disclosure dimension was the owner's to
weigh.

**Selection, verbatim as recorded from the selection interface:**

> "D — Split with pointer"

**What this fixes [OWNER_DECLARED]:**

| Element | Ruled |
|---|---|
| **Adopted bytes** | Placed in **root `docs/`**, publishing through the **existing** export allowlist — `docs` is already a root directory in the export profile, so **no boundary change occurs** and packet §4's non-goal is not offended. |
| **Candidates and revision evidence** | **Remain in root `execution/`** as immutable history, including this file and every prior revision. |
| **Pointer** | A pointer **identifies the adopted exact bytes**. This imposes **no two-way concordance burden**: the `execution/` candidates are historical evidence, not a maintained parallel copy. |
| **Future amendments** | The adopted PRD joins the instruction surface, so **every amendment is an M2 instruction-surface tranche** requiring independent owner authorization, a tranche manifest, routed notices, and export-manifest regeneration (D-GOV-21 M2/G4/M6). |

**[CLARIFIED]** The split mirrors the existing `_PROPOSALS/` vs `_DECISIONS/`
separation: the candidate surface holds what was proposed and how it changed;
the doctrinal surface holds what was adopted. **Placement is performed by the
adoption tranche, not by this file** — nothing here writes to root `docs/`.

### 9.5 RD-5 — v1 user scope · **RULED**

**Status: RULED** — owner, in-session, 2026-07-25; Receipt 38. Three scopes
were offered: **A** the present owner-practitioner; **B** individual
professional knowledge workers generally; **C** multi-practitioner
organizations. No agent recommendation was offered.

**Ruling: A for v1, on a staged progression A → B → C.** Owner verbatim:

> "It's for all of those, but I see it progressing over time as we start with
> A and learn from my use to make a better version for B which I can test out
> locally with multiple computers with multiple Agent 0 instances on each and
> learn from that and make a better C which is the target level of maturity
> for the platform."

**What this fixes [OWNER_DECLARED]:**

| Stage | Scope | Standing |
|---|---|---|
| **A** | The present owner-practitioner. | **v1 scope.** "User" in OBJ-1, OBJ-2, and OBJ-3 means this practitioner for v1 (§3). |
| **B** | Individual professional knowledge workers generally, with §2.2's responsibility model activating where applicable. | **Declared trajectory.** Informed by learning from A; **tested locally across multiple computers with multiple Agent 0 instances on each.** |
| **C** | Multi-practitioner organizations. | **Declared trajectory and the stated target level of maturity for the platform.** Informed by learning from B. |

**[CLARIFIED] Why the trajectory is load-bearing rather than aspirational.**
It is what keeps OBJ-1's discoverability condition from being trivially
satisfiable at v1 (§3), and it is the reason the §2.3 capacities are stated as
separable even though v1 does not require them to be separately held (§2.3).

**[CLARIFIED] Where the B-stage test intent already connects.** Multiple
computers each running multiple Agent 0 instances is exactly the population
**OBJ-6** and **§6.3** speak to — declared write ownership and reconstructible
run state as concurrent Agent 0 activity grows — and it is the kind of
deployment the shared runtime pilot (**D-GOV-20**: one opt-in per-user daemon
owning engines, sessions, delegation, and turn locks, with checkout-contained
project authority) already anticipates. **This states a connection, not a new
commitment**: no objective, requirement, or runtime obligation is added here.

**[CLARIFIED] Interaction with RD-2.** The RD-5 trajectory and the RD-2
evolution path point the same direction and are governed separately: RD-5
stages *who the product is for*; RD-2 (§9.2) stages *how attribution and
jurisdiction would scale*, and its B/C-stage machinery — the PEC interface and
database — is expressly not current scope.

---

## 10. Source concordance and document control

### 10.1 Concordance evidence (derivative packages)

The Rev 5 detailed transcription inventory — every clause, section anchor,
and verified line reference behind the Rev 5 commitments in §5, plus its
registry reference index and previously recorded items — remains at:

`execution/_Coordination/PRD_CANDIDATE_2026-07-25_concordance_annex.md`

Rev 6 does not silently mutate or overclaim that historical annex. Its
amendment-local exact-source inventory, runnable validator, deterministic
report, and stable uncovered-seam register are instead:

- `TRANSCRIPTION_SPEC.json`
- `validate_transcriptions.py`
- `CONCORDANCE_REPORT.json`
- `OPEN_ITEMS.csv`

These proposal-local files cover every exact-source sentence introduced or
textually changed by Rev 6 and labeled TRANSCRIBED. They are not a regenerated
full-PRD concordance annex.

**The derivative status is binding on how these artifacts may be used:**

- It is a **derivative package** under the `AGENTS.md` derivative-package
  rule: assembled from accepted upstream truth, citing its source SHAs, and
  **never a substitute** for that truth.
- It is a **derived publication artifact** in
  `docs/DECOMPOSITION_STANDARD.md` terms: not the amendment surface,
  explicitly labelled derived and non-authoritative.
- The Rev 5 annex is **specified for regeneration and proposed for checking** — annex §6
  gives the regeneration method and annex §4 specifies the D-14 check classes.
  **No full-annex generator or executable nine-class check exists at this
  basis**, and four of the nine check classes require semantic judgment.
  Rev 6's validator checks only its declared twelve exact-source sentences and
  open-item schema; it does not claim to discharge D-14.
- **It is never itself adopted. Adoption, if it occurs, binds the exact bytes
  of this main PRD only.**

The Rev 5 inventory remains in its annex to prevent the PRD from becoming
another drifting registry. Rev 6 follows the same principle with a small
machine-readable amendment inventory rather than extending prose enumeration.

### 10.2 Conflicts surfaced

**Rev 6 current-status note.** This table preserves the four Rev 5 discovery
records but updates their dispositions to the accepted current basis. C-1 was
closed by D-GOV-23; C-3 was closed by D-GOV-22; C-2 and C-4 were corrected by
PR #345 (merge `ba2b80bf2`, recorded in the root loop receipts). None is
reopened by Rev 6 and none is part of this amendment's runtime open-item
register.

| # | Conflict | Sources | Disposition |
|---|---|---|---|
| **C-1** | **Genus wording.** `docs/DIRECTIVE.md` §1 named an "agent operating system"; `README.md` named an "application environment"; the ruled genus (ID-0) used the two-level formulation. | Ratified governance vs. a non-binding/derivative surface (D-GOV-21 packet §3b) vs. the RD-1 ruling | **CLOSED — D-GOV-23** exact-prose supersession; D-GOV-24 completed the remaining top-level propagation. |
| **C-2** | **Invariant-index arithmetic.** The Rev 5 basis exposed disagreement between `docs/CONTRACT.md` §1's stated count and the live catalog. | `docs/CONTRACT.md` §1 index vs. §1.13 and §2 | **CLOSED — PR #345**, merge `ba2b80bf2`; current catalog text governs. |
| **C-3** | **Historical-note date.** The sealed brief stated an in-repo date inconsistent with git; the owner testimony and git fact required separate treatment. | Sealed brief vs. owner testimony vs. git history | **CLOSED — D-GOV-22.** Owner testimony confirmed; the earlier estimate is not load-bearing and is not to be repeatedly recited. |
| **C-4** | **Export description vs. export profile.** The Rev 5 basis omitted `runtime/` from the README description while the live export profile included it. | `README.md` vs. `exports/chirality-app/export_public.py` | **CLOSED — PR #345**, merge `ba2b80bf2`; the live profile remains the boundary contract. |

### 10.3 Historical Revision 7 amendment mechanics

This section is retained as Revision 7 candidate history. Its candidate-era
status statements are time-scoped to that proposal and are superseded for
current document control by §10.5; no historical proposal or ruling is
rewritten by this reconciliation.

**The accepted state before this candidate.** D-GOV-28 adopted Rev 6.
D-GOV-30 subsequently placed the verified facts of the 2026-07-28 merge
window (PRs #389–#408) into the Root governance record and prospectively
ratified four enumerated present-state items, expressly without amending
D-8 or LOOP_INIT §7 and expressly without retroactive cure. Those
instruments continue to govern. This candidate does not reopen them.

**The only changed stable commitment is D-8.** The Rev 6 D-8 row ("never
self-merge") is superseded by the successor row and annex §5.3.1. The
successor is PROPOSED and inert until an owner act adopts this exact Rev 7
candidate. Every other §5 commitment is byte-identical to the adopted
Rev 6 placement copy.

**Decision vehicle.** Two complete candidates are prepared side by side in
the D-GOV-31 proposal package — Candidate A (Root-only scope) and
Candidate B (shared-CHANGE scope) — each separately committed and hashed.
The owner first selects one committed candidate without adopting it; the
selected candidate is then re-audited by an HZN-GOV-01 rerun per
`execution/_Evaluation/CHIRALITY_PROGRAM_POST_REMEDIATION_HORIZON_2026-07-28_85EA0628/HANDOFF.md`;
findings are resolved; only then does the owner adopt through the D-GOV-31
record, created at adoption per the D-GOV-28 precedent, and the adopted
bytes are published through a human-gated merge under the still-current
D-8. This candidate never consumes its own not-yet-effective merge
exception.

**Scope limit.** Adopting Rev 7 establishes the successor product
requirement only. Propagation — the SOW-042 ledger row, DEL-04-06
requirement and evidence definitions, LOOP_INIT §7, the deterministic
enforcement points, tranche-manifest `self_merge` schema semantics, the shared CHANGE instruction surfaces, and routed M6 notices to every registered loop —
is enumerated with owners in this candidate's `POLICY_DELTA.md` and is
separately owned follow-on work. SHA-pinned historical mirrors, frozen
proposal packages, and receipts are expressly not rewritten.

### 10.4 Historical Revision 7 candidate document control

This table is the preserved Revision 7 candidate control record. Current
document control is in §10.5.

| Field | Value |
|---|---|
| Status | `ADOPTION-READY — adopted only by the instrument named below`, Revision 7 amendment candidate (Candidate B — shared-CHANGE merge-gate scope) |
| Adopting instrument | D-GOV-31, exact-candidate-SHA owner ruling pattern; its decision record is created at adoption per the D-GOV-28 precedent and carries any adopted status |
| Authority of this file itself | None. File creation, validation, commit, Git transport, review, or owner selection between candidates is not approval (K-AUTH-1). |
| Accepted predecessor | Rev 6 adopted by D-GOV-28; current placement `docs/PRD_ROOT.md` at `main@4f7808acb2802443370d045efa198152934c1674` (sha256 `0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d`) |
| InheritedSourceCorpusBasis | `main@7ac718c7e` — basis retained for inherited Rev 5 provenance labels |
| Rev6AmendmentBasis | `main@918bb48b8fcee66c031d0d6d4040a46089f96067` — retained basis for every sentence introduced or textually changed by Rev 6 |
| Rev7AmendmentBasis | `main@4f7808acb2802443370d045efa198152934c1674` — exact-source basis for every sentence introduced or textually changed by Rev 7 |
| SourceCorpusBasis | Composite: `Inherited=main@7ac718c7e; Rev6Amendment=main@918bb48b8fcee66c031d0d6d4040a46089f96067; Rev7Amendment=main@4f7808acb2802443370d045efa198152934c1674`; paired with the containing candidate commit per D-14 |
| This revision's bytes | The containing candidate commit, assigned at Git closeout. This file asserts no SHA for itself. |
| Prior revisions | Rev 1 `f15d51277`; Rev 2 `a72c2cd06`; Rev 3 `f9d33fcd9`; Rev 4 `ae5a476f4`; Rev 5 candidate `d9ea86f88504cb8d859a4cf3f042bac00d38fe57`, adopted by D-GOV-22; Rev 6 accepted-candidate `f78a83621cbd679e6af2c41199845aca74073480`, adopted by D-GOV-28 |
| Change envelope | D-8 successor merge-gate policy (shared-CHANGE scope); new annex §5.3.1; provenance-key and Rev 7 control reconciliation; nothing else |
| Root authority | D-GOV-20. D-T0-23 is named only as the coordinating Tier-0 counterpart and is not incorporated by reference. |
| Rev 6 evidence companions | `TRANSCRIPTION_SPEC.json`; `validate_transcriptions.py`; `CONCORDANCE_REPORT.json`; `OPEN_ITEMS.csv` — retained Rev 6 lineage in the D-GOV-28 proposal package; derivative evidence, never a substitute for sources or owner judgment |
| Provenance counts | **§5 stable commitments — 43 total: 32 TRANSCRIBED (N-1..N-8, O-1..O-9, D-1, D-4..D-7, D-9..D-11, E-1..E-7), 5 CLARIFIED (N-9, O-10, D-2, D-12, E-8), 6 PROPOSED-origin (D-8 successor, D-13, D-14, D-15, D-16, O-11).** D-GOV-22 accepted the four Rev 5 PROPOSED-origin commitments; D-GOV-28 accepted O-11; the D-8 successor alone is inert in Rev 7. The ten verbatim D-GOV-20 sentences are a transcription block, not ten additional stable IDs. |
| PROPOSED inventory | **19 provenance-labeled items:** the 17 Rev 5 items adopted by D-GOV-22, O-11 adopted by D-GOV-28, and the Rev 7 D-8 successor, which alone remains inert pending D-GOV-31. |
| Rev 6 open items | Stable machine-readable register in the D-GOV-28 proposal package's `OPEN_ITEMS.csv`; statuses restricted to OPEN or PROPOSED; carried unchanged by Rev 7 |
| Adoption condition | The D-8 successor policy takes effect only through an explicit D-GOV-31 owner ruling against the exact candidate SHA, after owner selection between the two committed candidates and an HZN-GOV-01 rerun against the selected candidate. Such adoption does not pre-approve any propagation act, SCOPE_CHANGE gate, or grant. |

### 10.5 Predecessor document control — Revision 8 (historical merge policy)

| Field | Current value |
|---|---|
| Status | `ACCEPTED — CURRENT PRODUCT BASIS`, Revision 8 |
| Authority instruments | D-GOV-31 adopted Revision 7 against exact subject SHA-256 `15fba9c36a197b36b281297af123115bcd3f282fe6c6f2fae05cd703b3743748`; the owner-directed simplification recorded in Receipt 64 produced Revision 8 through PR review under D-1 |
| Effective Revision 8 identity | `main@602dd71b8c123d8a47a36644db1453f515c0f778`; pre-reconciliation live subject SHA-256 `278f31ae99607f970e39c6535f809c93a7c5bf09b139ffa2cbbdbe3f08c3746c` |
| Revision lineage | Rev 5 adopted by D-GOV-22; Rev 6 adopted by D-GOV-28; Rev 7 adopted by D-GOV-31; Rev 8 is the Receipt-64 owner-directed simplification of the accepted Rev 7 merge-execution policy |
| Current change envelope | Revision 8 changes only the D-8 successor merge-gate policy and annex §5.3.1 from the bounded-grant form to owner direction recorded in ordinary closeout evidence; every other stable commitment remains as inherited from Revision 7 |
| D-8 standing at Revision 8 | `ADOPTED (Rev 8)`; human-gated PRs remain the standing default, owner direction may authorize merge execution, K-MERGE-1 remains unchanged, and stricter loop-local discipline remains controlling until locally adopted or acknowledged |
| Historical candidate evidence | The Revision 7 candidate header, amendment mechanics, and document-control table above remain deliberately preserved as time-scoped proposal history; they are not current-status claims |
| Effect of this reconciliation | Metadata/status alignment only. No scope, objective, stable commitment, topology, mapping, count, provenance-origin label, lifecycle, release, or reliance state changes |

## Prospective successor revision record

**PRD §10 prospective document control.** On actual acceptance/application, add a new current revision record identifying this exact amendment and applied bytes; preserve Revision 8 and its acceptance history. Regenerate the current concordance and source-currency derivatives against the accepted successor corpus. Until that act the current accepted PRD remains Revision 8. This candidate does not silently relabel old PROPOSED-origin obligations or erase their provenance.


## Migration revision control — prospective, not adopted

The preceding historical adoption records retain their original dates, labels and claims. They do not supply acceptance for this revision. This candidate is the exact prospective successor charter after effective transfer; pending acceptance, Revision 8 remains current. The final owner act must bind the reviewed candidate commit and manifest digest, preserve the prior immutable PRD bytes in their accepted snapshot/Git lineage, and separately identify publication and effective application. No acceptance/publication/effect identifier is fabricated here. Current provenance counts, source-currency and concordance derivatives must be regenerated against accepted successor bytes; old annex counts describe their named predecessor revisions only. D-14 remains an unsatisfied tool/evidence duty where its implementation is absent. Applying these postimages requires the same-tranche M2/G4 manifest, routed notices, allowed export regeneration and exact owning gates.
