# Chirality App v4 User Manual

**Working draft, 30 October 2026. Not yet a release manual.**

This manual is for the person using Chirality App. It explains how to work with
an agent, use a workflow, examine the result and improve a method for next time.
It is separate from the Project Management for Human–Agent Teams manual and
from the retired Chirality Agent User Manual, which described repository practice.

App v4 is in development. Its initial release will be for macOS; Windows will
follow. The instructions here are based on the development source. They have
not yet been checked by completing these tasks in a released desktop package.
Use the v3 release documentation for App 3.0.1.

## Start with the task

Tell the agent what you want to achieve, who will use the result, and what
information it may use. State any limits on changing files or contacting other
people. Provide the sources needed for the task and explain which are current.

For example:

> Help me prepare this month's project update. Use the approved plan and the
> progress notes in this folder. Draft the update in a new file. Identify
> missing information and changes from the plan. Do not send it to anyone.

Examine the proposed approach before consequential work begins. You do not need
a saved workflow for every task. Use one when its method fits the work, or when
you want to repeat and improve a method.

## Read by task

- [Use a workflow](using-workflows.md): choose the method and revision, provide
  inputs, run the work and examine the result.
- [Create and improve a workflow](creating-workflows.md): draft, try, review,
  register and reuse a method.
- [Define work](workflows/define-work.md): prepare a clear assignment.
- [Prepare an engineering estimate and schedule](workflows/engineering-planning.md):
  keep work, effort, cost and timing consistent.

The last two guides cover methods in the shared Chirality repository. Their
inclusion in this draft does not mean they are bundled or ready to run in App v4.
The release manual must identify the actual supplied version and installation
route for each workflow it covers.

## Chapters to complete against the release candidate

1. Install, update and start the App on macOS; add Windows instructions when its
   candidate is available.
2. Choose an account or model provider, understand permissions and select the
   working folder. Explain what leaves the computer for each supported option.
3. Start and continue a conversation; attach files; interrupt work and recover
   after an error or restart.
4. Complete a first task with sample files and inspect its output.
5. Use and maintain workflows, including library selection, trials and revisions.
6. Work with the supported embedded application, with its own operations and
   checks explained separately.
7. Find saved work, move or back it up, and report a problem.

## Editorial and verification basis

Keep explanations short and use the labels shown by the actual App. Introduce
technical terms only when they help someone make a choice. A workflow guide
needs a purpose, prerequisites, sample inputs, steps, expected results, checks,
common problems and limits. Screenshots should illustrate an action that has
been exercised in the candidate.

The initial draft was checked against `app/README.md`, `app/src/App.tsx` and
`app/src/WorkflowDrafts.tsx` at App source `40415db3`. The method guides use
Chirality's `define-work` and `integrated-engineering-estimate-schedule` packages
at `57af436412`. These source checks are not desktop walkthrough results.

Before publication, finish each procedure in an identified candidate with safe
sample files. Verify control names, output locations, recovery steps and the
actual workflow inventory. Keep unsupported procedures out of the released
edition. Record the candidate and any remaining limits here. The website should
publish a named edition of this source, not maintain a second editable manual.
