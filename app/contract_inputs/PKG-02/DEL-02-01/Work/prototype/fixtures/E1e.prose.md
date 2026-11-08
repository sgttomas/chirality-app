---
name: supports-approve
description: Gather a spacing review's findings and the engineer's criteria,
  write an approval package for the engineer's engineering approval, and
  report the sustained-load results for the accountable professional's
  reliance decision.
---
# Prepare supports for approval and reliance

## Gather
Take the findings of the named spacing-review run and the criteria file the
engineer supplies. Read the supports on the run.

## Prepare
Write the approval package file into the project. It is agent-prepared; never
describe it as approved.

## Ask for approval
Checkpoint `CP-approve`. Ask the engineer for engineering approval of the
package, in the App's act control. If they decline, stop and report.

## Report loads
Read the sustained-load results for LC-1 and report them by reference in a
message whose first line is `## Load findings — supports-approve`.

## Ask for reliance
Checkpoint `CP-rely`. Ask the accountable professional whether they rely on
these results for the support design. If they decline, stop and report.

## Return
Report which acts were performed, by whom, and what is unknown.

## Declared part
The block below is this workflow's declared part (DEL-02-01 WD-v0.8 §3.5). It
states what the method expects, needs, stops for and returns. It grants no
permission, and it is not evidence that anything happened.

