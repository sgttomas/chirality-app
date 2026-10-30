# Use a workflow

A workflow is a reusable set of instructions for doing a kind of work. It can
include reference material, templates and checks. It does not supply the facts
of your project or decide whether you may rely on the result.

## Choose a suitable method

Read its purpose and expected result. Check that you can provide its required
inputs and carry out its checks. If the method does not fit, explain the
mismatch to the agent before starting. Do not fill missing facts with invented
values simply to complete a template.

For one small task, a clear brief may be enough. A workflow is useful when the
method has several connected steps, when a check is easy to miss, or when you
expect to repeat the work.

## Choose the library and conversation

The development App provides **Open project workflow library…** and
**Open user workflow library…**. Choose the library containing the method you
intend to use. Check the displayed project and library before proceeding.

Choose the **Workflow chat** that should use the method. Browsing a library
without a chat lets you inspect its contents; it does not select a workflow
for a new conversation. Each chat keeps its own selection.

Read the workflow text and any resources that affect your task. A bundled
candidate can currently be inspected, but the development App explicitly says
it is not runnable as a shipped workflow while release registration is pending.
Do not treat that candidate label as a completed release feature.

## Select a revision

Where the App offers **Select revision**, check the revision you are selecting.
Registered revisions preserve the reviewed content. Editing a separate copy
of the workflow does not change that revision.

A newer revision does not silently replace the one selected for your chat.
Decide whether to use it, especially if the current work depends on earlier
instructions. A run that has started keeps its revision.

If selection is unavailable, read the reason shown. The development App may
require review and confirmation before a revision can be used in the current
session. Follow the offered review route. Copying files or changing their names
is not a substitute for resolving the reported problem.

## Provide the task inputs

Tell the agent the result you need, the sources it should use and where it may
put outputs. Explain dates, units and other conventions that affect the work.
Name missing inputs and any provisional assumptions you permit.

Before sending prepared text, read it. Check the chosen method, files and task.
After sending, check whether the App reports a successful submission. Sending
instructions does not by itself show that the model followed them or completed
the task.

## Examine the result

Compare the output with the requested result and the source information.
Check consequential calculations, unsupported claims, omissions and departures
from the method. Use an independent check where the work requires one.

Ask the agent to repair specific problems and explain the effects of changed
inputs. Keep the useful result and enough source information to understand and
check it later. Accepting a workflow into a library does not approve every
result it produces.

If the method itself needs improvement, [revise a draft](creating-workflows.md)
and test it on a representative case. Keep the earlier revision available for
work that still depends on it.
