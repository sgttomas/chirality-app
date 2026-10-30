# Starting an App v4 session

1. Send the contents of [init-prompt.md](init-prompt.md). Let the agent orient
   and report its understanding of the current basis and boundaries.
2. Send your steering as a separate message: the undertaking, its scope and any
   reserved choices. When you send a steering file by reference instead of
   pasting it, tell the agent explicitly to read and execute it as your steering.

The init prompt is reusable; its project entry is [LOOP_INIT.md](../loop/LOOP_INIT.md).
Initialization alone selects no undertaking. The agent loads other roles,
workflows and skills when the steered undertaking needs them.
