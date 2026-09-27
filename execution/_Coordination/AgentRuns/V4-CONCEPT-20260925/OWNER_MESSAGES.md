# Owner's later messages (verbatim)

Messages from the owner in the session after the answers of 2026-09-25,
reproduced exactly, in order. Each is quoted between rules.

## M-01 — reply to the harness-experiments proposal

---

oMLX is on my other machine.  I'd need to have you give instructions to another agent and then that agent leaves evidence you can accept.  Would that be okay?

---

HELPS_HUMANS replied yes and prepared `experiments/HX-01_BRIEF.md`
(commit `d7c7d2c5a`). The brief was never launched.

## M-02 — direction on tests and maintainability

---

But I don't really want to run those tests.  I think you can do more intellectual analysis before we need to get practical, because I don't know what I really expect to learn from those tests.  I know all those configurations work, but I won't know to what extent they work in all the ways that I want and anyways code maintainability is top of my concerns and none of that has to do with ability.  The best ability is maintainability.

---

## M-03 — reply to the maintainability analysis

---

I'm not convinced.  I think that's going to be hard to build my own ACP layer, why do you think it will the best option for maintainability?  After that, my next priority is functionality and losing the functionality from the native Codex harness is a big loss.  Those harnesses are the best in the world.  And having OAuth natively is also essential.  I want to build around the best harnesses in the world in the easiest to maintain manner.  How does that balance strike you?

---

## M-04 — two agent experiences; local models and privacy as third priority

---

That's appropriate for the Chirality App to wrap the full Codex experience, but for SWBPIPE a simpler agent experience and local models are acceptable.  Maybe your first proposal was discarded too quickly?  Because my third priority is having the local model server be the primary interface and be a good user experience and capabilities that keep up with developments and not have to depend upon a third party harness that sends data elsewhere.  So local models and data privacy are my third priority and having that still provide the user with an agent that can take the same actions as the human user ("semantic parity" as it's been called at times).

---

## M-05 — acceptance of the two-tier balance

---

This is the balance I was after.  Of course, the only certainty is that the pace of change will continue.  This is the best I can think of and should be the basis for v4.0 and if we learn better we can change for v5.0.

---

## M-06 — reservation about Windows and native webviews (question)

---

I have some reservations about adding a Windows version of these apps and having the Tauri native browser issue being a limiting factor.  Any thoughts on how much of a risk that is and if you see it differently or have a solution?

---

HELPS_HUMANS answered with `conceptual/MAINTAINABILITY_ANALYSIS.md` §11.3
(commit `9e87dae16`).

## M-07 — the two architecture choices

---

Go with Tauri and the minimal loop.

---
