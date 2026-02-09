# Unsaid
_Date: 2026-02-09_

This file holds what often stays implicit in “AI in professional engineering” conversations: the pressure, the failure modes, and the uncomfortable truths that matter when the work is regulated and liability is real.

It is intentionally more candid than a formal position statement.

---

## 1) The productivity narrative is a trap

Most “AI for engineering” messaging treats engineering as document production: generate faster reports, draft specs, automate emails.

That framing is not merely incomplete—it is professionally dangerous. It shifts attention away from what causes harm in real projects:

- unclear intent and scope
- unverified assumptions
- unmanaged interfaces between disciplines
- silent conflicts between sources
- weak change control and missing records
- overconfidence under uncertainty

AI can make documents appear *finished* long before the engineering is actually *done*. The risk is not that AI writes poor text; the risk is that people start treating polished text as evidence of correctness.

---

## 2) Over‑trust will be the dominant failure mode

In regulated work, the biggest human-factor risk is not “AI makes mistakes.”  
It is **humans trusting AI outputs too easily** because they are fluent, fast, and plausible.

Two uncomfortable implications follow:

- “Human-in-the-loop” is not a safety mechanism if the human is only skimming.  
  Skimming is not independent judgment.

- The people most vulnerable are the ones under time pressure and least supported by review culture.

If your workflow does not *force* careful review (diffs, evidence packs, gates), it will drift toward complacency—because humans optimize for time.

---

## 3) Deskilling is real, and it is a safety issue

If AI does the “junior engineer” work, organizations can accidentally remove the very practice loop that produces competence:

- doing the calculations
- making the mistakes (safely)
- being corrected
- learning how to check and why checks exist

A future where fewer engineers can independently verify is a future with more systemic risk—even if output volume is higher.

AI adoption plans that ignore training, mentorship, and progressive responsibility are not modernization. They are technical debt in human form.

---

## 4) “We used AI” will not be a defense

Regulators, insurers, and courts will not accept “the AI suggested it” as justification.

If anything, AI may raise expectations:

- Why didn’t you run obvious cross-checks?
- Why isn’t the record reproducible?
- Why did you accept outputs without verifying the basis?

Organizations should assume that **auditability will become a differentiator**: those who can show evidence and decision lineage will win trust; those who cannot will face friction, exclusions, and higher insurance costs.

---

## 5) Confidentiality and data gravity are not side issues

Engineering work contains:

- client confidential information
- security-sensitive details
- critical infrastructure data
- personal information (sometimes)
- IP and trade secrets

Once information flows into external model providers, plugins, or uncontrolled logs, you may create:
- contractual breaches
- regulatory exposure
- retention and discovery burdens

“Data minimization” is not just good hygiene. In many contexts it is an ethical and legal obligation.

---

## 6) The profession must set the norms, or the market will

If professional engineers do not define:

- what “acceptable AI assistance” looks like
- what records must exist
- what review is required
- what counts as competence with AI tools

…then vendors, procurement departments, and generic IT governance will define it for them—often optimized for cost and speed, not duty of care.

The early norms will calcify. They will become the reference point for regulation, insurance underwriting, and courtroom expectations.

---

## 7) We should talk about incentives honestly

Bad outcomes are often incentive-shaped:

- low fees → reduced time for review
- schedule pressure → acceptance of “good enough”
- fragmented responsibility → “not my scope”
- tool hype → unrealistic expectations from leadership

AI can amplify all of these if introduced as a speed mandate instead of a safety-and-quality system.

The path forward requires explicit counter-incentives:
- enforced gates
- separation of duties where needed
- clarity that safety work products are not optional “overhead”

---

## 8) What I want to say plainly, in another context

- **Engineering is one of the few places where “slow is smooth and smooth is fast” is literally true.**  
  Speed without verification is not efficiency; it is deferred harm.

- **We should treat AI integration like introducing a new material into a load‑bearing structure.**  
  You would not do that without testing, standards, and inspection.

- **The winning teams will be the ones who make judgment and evidence scale—not the ones who make text scale.**

- **If your AI system cannot say “I don’t know” and stop safely, it is not ready for regulated reliance.**

---

## 9) If this becomes a talk or essay, the title is:

**“Engineering is not content production. AI doesn’t change duty of care—only the failure modes.”**
