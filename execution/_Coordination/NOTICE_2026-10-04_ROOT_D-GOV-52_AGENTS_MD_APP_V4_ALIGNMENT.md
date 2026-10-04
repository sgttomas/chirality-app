# Notice — Root AGENTS.md: instruction-change timing and App-process settings (D-GOV-52)

Root `AGENTS.md` changed in tranche `ROOT-DGOV52-APPLICATION-20261004`
(sha256 `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`;
was `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd`). The
owner approved it on 2026-10-04: "I approve A1 and B1, go ahead". Exact text
and reasoning: `docs/governance_harness/_PROPOSALS/D-GOV-52_agents-md-app-v4-alignment_2026-10-03/PACKET.md`.

Two passages changed:

1. "Instruction changes take effect at a verified idle boundary or, where the
   App fixes a conversation's role guidance for its life, in new
   conversations only, preserving prior supplied content and conversation
   history."
2. Added after "does not … veto the user's Codex configuration …": "A setting
   the App passes only to Codex processes it owns, such as turning off
   Codex's analytics, is not a veto: it is shown and recorded, and the user's
   configuration file is unchanged."

This notice is coordination, not authority. Your loop decides whether to
adopt, amend or decline.

**App v4:**
- Adoption is recorded in run `APP-V4-DESIGN-PASS-4-20261003`, R23-30.
- ROLE-v0.2 F-R9 and the Root citations in HOSTING-v0.9 §2/§8.2 and
  ACCESS-v0.2 §9/U-A9 are updated at those files' next revision.
- U-A9 is App v4's; R23-30 rules it "yes".
