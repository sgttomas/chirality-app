# Seed set plan

Standing: **proposed plan (agent).** How the conceptual work becomes the
seed set the owner will be asked to accept (OD-12). Revised as drafting
proceeds.

## 1. What the seed set is

The documents a fresh implementation session starts from (OD-13): the
product basis for v4.0, the references it relies on, and the open matters
with their owners and points of need. Everything else in this folder is
supporting record.

| Part | Path | Standing when presented | Role |
|---|---|---|---|
| **PRD** | `docs/PRD.md` | Proposed for acceptance | The product: purpose, users, activities, the two expressions and the connectors, capabilities, boundaries, constraints, interfaces, examination, open questions. Includes a short vocabulary. Requirements carry stable IDs. |
| **Architecture basis** | `docs/ARCHITECTURE.md` | Proposed for acceptance | The two agent tiers, the seams, the maintainability principles, supplier assumptions and pins, alternatives considered and why set aside, open architecture questions. |
| **Host integration** | `docs/HOST_INTEGRATION.md` | Proposed for acceptance | The contract every host implements: the capability catalog, semantic parity, proposals and basis binding, receipts, reserved human acts, and how connectors (PEC, Domains) are consumed. |
| **Examination** | `docs/EXAMINATION.md` | Proposed for acceptance | Principal scenarios walked through both expressions; verification versus validation; the replacement condition for v3.0.1 as an examinable scenario. |
| **Operating method** | `docs/OPERATING_METHOD.md` | Proposed for acceptance, after the Q-11 discussion | How v4 is built: the retained decomposition and work-graph loop guided by the manuals, pinned manual editions, the feedback loop, proportion rules. |
| Preserved foundation | `foundation/` | Preserved, unchanged; not proposed as requirements | The thesis, with its own standing |
| References | `reference/` | Identification only | Pins, source inventory, archives |
| Conceptual record | `conceptual/`, run record | Record; not proposed as requirements | Directions and decisions (D-01…), questions, analyses, exemplars and lessons |

Five documents, because each subject has a different reader: the owner and
any reader (PRD), whoever builds the pieces (architecture), whoever builds a
host (host integration), whoever examines the result (examination), and
whoever runs the work (operating method).

## 2. What is decided and where it goes

| Decision | Goes into |
|---|---|
| OD-01…OD-13 (the brief) | PRD purpose and scope; standing of the seed |
| D-01 standalone app is the App for Creating Workflows; same four agents everywhere | PRD expressions and roles |
| D-02 one host-integration contract, outside controller first then embedded | Host integration; architecture |
| D-03 workflows as method guidance with declared checkpoints | PRD capabilities; vocabulary |
| D-04 graduated autonomy | PRD interaction and decision rights |
| D-06 Mac first; OAuth, API key and local model, possibly at once | PRD constraints |
| D-07 where records live | PRD records; vocabulary |
| D-08 PEC and Domains as independent connectors | PRD connectors; host integration |
| D-09 project management option B | PRD capabilities |
| D-10 roles shown in the App, receding in hosts | PRD interaction |
| D-11 replacement condition | PRD conditions; examination |
| D-12 build method (under discussion) | Operating method |
| D-13 Codex reviewer, Claude fallback | Stage G |
| D-16…D-19 maintainability first, functionality second, local models and privacy third; the two-tier direction | Architecture; PRD constraints |

## 3. Open items and the defaults drafting will use

Drafting can proceed with these defaults, each marked in the documents as
**pending the owner's confirmation** until confirmed. None becomes an
accepted requirement by being drafted.

| Item | Default used in drafting | Where it lands |
|---|---|---|
| Q-01 working statement | Candidate A (`DISCUSSION_2026-09-25.md` §1), with "local-first in host applications" added | PRD opening |
| Q-04 (a) harness classifier approvals | A user choice in the Chirality App, like any permission setting; not used in hosts | PRD decision rights |
| Q-04 (b) invariant | An agent never originates or represents a human act (acceptance, checked mark, approval, reliance) in the human's name | PRD decision rights; host integration |
| Q-07 meaning of "Domains" | The domain packs (knowledge corpora with accepted decompositions and search indexes), distinct from domain engines | PRD connectors |
| Q-07 essential hosts | SWBPIPE and the Chirality App; PEC and Domains are connectors, not hosts | PRD users and activities |
| Q-08 further project-management scope | Option B only; the owner's "more to it" carried as an open question | PRD capabilities; open questions |
| Q-11 build method | The owner's proposal with the six conditions in `DISCUSSION_2026-09-25.md` §3; a thin project loop file pointing to the Field Book; agents record gaps where the manuals are silent and bring consequential ones to the owner; the owner revises the manuals from proposed changes | Operating method |
| Standalone App's stack (Electron + Next as in v3, or Tauri + React to share SWBPIPE's) | Left open in the architecture basis with the evidence from the v3 reuse reading, and a recommendation | Architecture open questions |
| Whether the App needs v3's Runtime service | Left open with the evidence from the same reading | Architecture open questions |

## 4. Sequence

1. Fold in the two reading returns (Pi libraries; v3 Runtime and frontend).
2. Draft the PRD's load-bearing sections — purpose, expressions,
   capabilities, decision rights and parity — and show them to the owner
   (plan checkpoint 4).
3. Draft the other four documents; reconcile them with the PRD.
4. Self-check: walk the examination scenarios through the set; list
   contradictions and guesses; repair.
5. Independent review by a Codex reviewer (D-13); repair and backcheck.
6. Present the identified seed set for acceptance; record the response.
