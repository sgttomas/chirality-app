#!/usr/bin/env python3
"""Constructed native-item scenarios for the DEL-01-03 view model.

Fixture standing (HOSTING §9.2): every frame here is `constructed` from the
generated 0.158.0 types; none is `recorded`. run_cases.py validates each frame
against the committed 0.158.0 JSON Schema bundle of DEL-01-01. Invented
material only: thread, turn and item identities, commands and texts are
fixture subjects, not observations of Codex behaviour.
"""

P = "thr-fixture-parent"
C1 = "thr-fixture-child-1"
C2 = "thr-fixture-child-2"
T0 = 1790000000000  # fixture clock origin (Unix ms); TEST VALUE


def ready(g, label="codex-cli 0.158.0", experimental=True, result="development-unverified",
          detail=None):
    return {"ev": "ready", "g": g, "record": {
        "declaredPin": "0.158.0", "observedLabel": label,
        "verification": {"result": result, "detail": detail},
        "qualificationRef": None,
        "declaredCapabilities": {"experimentalApi": experimental, "requestAttestation": False}}}


class Stream:
    """Assigns receipt positions per generation, as the host would (HOSTING §5 Order)."""

    def __init__(self, g=1):
        self.g = g
        self.pos = 0
        self.events = []

    def add(self, ev):
        self.events.append(ev)
        return self

    def frame(self, method, params, dt=0):
        self.pos += 1
        self.events.append({"ev": "frame", "g": self.g, "pos": self.pos,
                            "frame": {"method": method, "params": params, "emittedAtMs": T0 + dt}})
        return self

    def new_generation(self, g):
        self.g = g
        self.pos = 0
        return self


def turn(tid, status="inProgress", items=None):
    return {"id": tid, "items": items or [], "status": status, "error": None,
            "startedAt": None, "completedAt": None, "durationMs": None, "itemsView": "summary"}


def plan_item(iid, text):
    return {"type": "plan", "id": iid, "text": text}


def cmd(iid, status, source="agent", out=None, code=None):
    return {"type": "commandExecution", "id": iid, "pluginId": None, "scriptPath": None,
            "command": "/bin/zsh -lc 'python3 size_pump.py --fixture'", "cwd": "/fixture/workspace",
            "processId": None, "source": source, "status": status,
            "commandActions": [{"type": "unknown", "command": "python3 size_pump.py --fixture"}],
            "aggregatedOutput": out, "exitCode": code, "durationMs": None}


def file_change(iid, status):
    return {"type": "fileChange", "id": iid, "status": status,
            "changes": [{"path": "/fixture/workspace/notes/sizing.md", "kind": {"type": "add"},
                         "diff": "+Invented sizing note\n"}]}


def mcp(iid, status, error=None):
    return {"type": "mcpToolCall", "id": iid, "server": "fixture-server", "tool": "lookup_invented_part",
            "status": status, "arguments": {"part": "P-EX-1"}, "appContext": None, "mcpAppUi": None,
            "pluginId": None, "readOnlyHint": True, "result": None, "error": error, "durationMs": None}


def dyn(iid, status, success=None, content=None):
    return {"type": "dynamicToolCall", "id": iid, "namespace": None, "tool": "fixture_tool",
            "arguments": {}, "status": status, "contentItems": content, "success": success,
            "durationMs": None}


def collab(iid, tool, status, receivers, states, sender=P):
    return {"type": "collabAgentToolCall", "id": iid, "tool": tool, "status": status,
            "senderThreadId": sender, "receiverThreadIds": receivers,
            "prompt": "Check the invented head figure.", "model": None, "reasoningEffort": None,
            "agentsStates": states}


def subagent(iid, kind, child, path="/root/reviewer"):
    return {"type": "subAgentActivity", "id": iid, "kind": kind, "agentThreadId": child, "agentPath": path}


def thread_obj(tid, parent=None, status="idle", role=None, nickname=None, depth=1):
    src = ({"subAgent": {"thread_spawn": {"parent_thread_id": parent, "depth": depth,
                                           "agent_path": "/root/reviewer", "agent_nickname": nickname,
                                           "agent_role": role}}}
           if parent else "appServer")
    return {"id": tid, "sessionId": "ses-fixture-1", "parentThreadId": parent, "preview": "",
            "ephemeral": False, "projectId": None, "modelProvider": "fixture-local", "model": None,
            "createdAt": 1790000000, "updatedAt": 1790000100, "status": {"type": status},
            "cwd": "/fixture/workspace", "cliVersion": "0.158.0", "source": src,
            "agentNickname": nickname, "agentRole": role, "turns": []}


# ---------------------------------------------------------------------------

def sc_plans():
    """Plan mode: plan item with deltas (preview differs from the completed text), a
    revision in a later turn; checklist updates in default mode."""
    s = Stream(1).add(ready(1))
    s.frame("turn/started", {"threadId": P, "turn": turn("turn-fixture-1")}, 1)
    s.frame("item/started", {"threadId": P, "turnId": "turn-fixture-1",
                             "item": plan_item("item-fixture-plan-1", ""), "startedAtMs": T0 + 2}, 2)
    s.frame("item/plan/delta", {"threadId": P, "turnId": "turn-fixture-1",
                                "itemId": "item-fixture-plan-1", "delta": "1. Read the datasheet"}, 3)
    s.frame("item/plan/delta", {"threadId": P, "turnId": "turn-fixture-1",
                                "itemId": "item-fixture-plan-1", "delta": "\n2. Draft"}, 4)
    s.frame("item/completed", {"threadId": P, "turnId": "turn-fixture-1",
                               "item": plan_item("item-fixture-plan-1",
                                                 "1. Read the invented pump datasheet.\n2. Draft the sizing note."),
                               "completedAtMs": T0 + 5}, 5)
    s.frame("turn/completed", {"threadId": P, "turn": turn("turn-fixture-1", "completed")}, 6)
    s.frame("turn/started", {"threadId": P, "turn": turn("turn-fixture-2")}, 7)
    s.frame("item/completed", {"threadId": P, "turnId": "turn-fixture-2",
                               "item": plan_item("item-fixture-plan-2",
                                                 "1. Read the invented pump datasheet.\n2. Draft the sizing note.\n"
                                                 "3. Ask the person to check the head figure."),
                               "completedAtMs": T0 + 8}, 8)
    s.frame("turn/completed", {"threadId": P, "turn": turn("turn-fixture-2", "completed")}, 9)
    # Default mode: checklist updates (whole plan each time, no revision identity: P-10)
    s.frame("turn/started", {"threadId": P, "turn": turn("turn-fixture-3")}, 10)
    steps = [{"step": "Read the datasheet", "status": "inProgress"},
             {"step": "Draft the sizing note", "status": "pending"}]
    s.frame("turn/plan/updated", {"threadId": P, "turnId": "turn-fixture-3",
                                  "explanation": None, "plan": steps}, 11)
    s.frame("turn/plan/updated", {"threadId": P, "turnId": "turn-fixture-3",
                                  "explanation": None, "plan": steps}, 12)
    steps2 = [{"step": "Read the datasheet", "status": "completed"},
              {"step": "Draft the sizing note", "status": "inProgress"}]
    s.frame("turn/plan/updated", {"threadId": P, "turnId": "turn-fixture-3",
                                  "explanation": "Datasheet read.", "plan": steps2}, 13)
    s.frame("turn/completed", {"threadId": P, "turn": turn("turn-fixture-3", "completed")}, 14)
    s.add({"ev": "read", "method": "thread/items/list", "params": {"threadId": P, "turnId": "turn-fixture-1"},
           "at": T0 + 15, "result": {"data": [
               {"turnId": "turn-fixture-1", "item": plan_item(
                   "item-fixture-plan-1", "1. Read the invented pump datasheet.\n2. Draft the sizing note."),
                "startedAtMs": None, "completedAtMs": None}], "nextCursor": None, "backwardsCursor": None}})
    return s.events


def sc_plans_history():
    """After relaunch: history reads return the two plan items; checklist updates are not
    in history (TurnPlanStep occurs only in TurnPlanUpdatedNotification)."""
    s = Stream(2).add(ready(2))
    s.add({"ev": "read", "method": "thread/turns/list", "params": {"threadId": P}, "at": T0 + 100,
           "result": {"data": [turn("turn-fixture-1", "completed"), turn("turn-fixture-2", "completed"),
                               turn("turn-fixture-3", "completed")],
                      "nextCursor": None, "backwardsCursor": None}})
    s.add({"ev": "read", "method": "thread/items/list", "params": {"threadId": P}, "at": T0 + 101,
           "result": {"data": [
               {"turnId": "turn-fixture-1", "item": plan_item(
                   "item-fixture-plan-1", "1. Read the invented pump datasheet.\n2. Draft the sizing note."),
                "startedAtMs": None, "completedAtMs": None},
               {"turnId": "turn-fixture-2", "item": plan_item(
                   "item-fixture-plan-2", "1. Read the invented pump datasheet.\n2. Draft the sizing note.\n"
                   "3. Ask the person to check the head figure."), "startedAtMs": None, "completedAtMs": None},
               {"turnId": "turn-fixture-4", "item": cmd("item-fixture-cmd-9", "inProgress"),
                "startedAtMs": None, "completedAtMs": None}],
               "nextCursor": None, "backwardsCursor": None}})
    return s.events


def sc_plan_incomplete():
    s = Stream(1).add(ready(1))
    s.frame("turn/started", {"threadId": P, "turn": turn("turn-fixture-5")}, 1)
    s.frame("item/plan/delta", {"threadId": P, "turnId": "turn-fixture-5",
                                "itemId": "item-fixture-plan-5", "delta": "1. Partial"}, 2)
    s.frame("turn/plan/updated", {"threadId": P, "turnId": "turn-fixture-5", "explanation": None,
                                  "plan": [{"step": "Partial", "status": "inProgress"}]}, 3)
    s.frame("item/started", {"threadId": P, "turnId": "turn-fixture-5", "item": cmd("item-fixture-cmd-5", "inProgress"),
                             "startedAtMs": T0 + 4}, 4)
    s.add({"ev": "runtime", "kind": "register", "threadId": P, "itemId": "item-fixture-cmd-5",
           "requestId": "srv-fixture-5", "state": "outstanding", "origin": None})
    s.frame("item/started", {"threadId": P, "turnId": "turn-fixture-5", "item": cmd("item-fixture-cmd-6", "inProgress"),
                             "startedAtMs": T0 + 5}, 5)
    s.add({"ev": "closed", "g": 1, "reason": "exited-unexpectedly"})
    return s.events


def sc_recovery_reads():
    """Same App session, after the supplier restarted: history reads settle what the closed
    generation left incomplete or unknown (PL-09, TI-12). Constructed; whether Codex history holds
    these completions after an exit is OBS-2 pending (O-2)."""
    s = Stream(2).add(ready(2))
    s.add({"ev": "read", "method": "thread/items/list", "params": {"threadId": P, "turnId": "turn-fixture-5"},
           "at": T0 + 300, "result": {"data": [
               {"turnId": "turn-fixture-5", "item": plan_item("item-fixture-plan-5", "1. Partial, completed."),
                "startedAtMs": None, "completedAtMs": None},
               {"turnId": "turn-fixture-5", "item": cmd("item-fixture-cmd-5", "declined"),
                "startedAtMs": None, "completedAtMs": None}],
               "nextCursor": None, "backwardsCursor": None}})
    return s.events


def sc_plan_turn_ended():
    """A plan item streaming when its turn ends (PL-06); a checklist update after the turn end (CL-04)."""
    s = Stream(1).add(ready(1))
    tu = "turn-fixture-10"
    s.frame("item/started", {"threadId": P, "turnId": tu, "item": plan_item("item-fixture-plan-10", ""),
                             "startedAtMs": T0 + 1}, 1)
    s.frame("turn/plan/updated", {"threadId": P, "turnId": tu, "explanation": None,
                                  "plan": [{"step": "Only step", "status": "inProgress"}]}, 2)
    s.frame("turn/completed", {"threadId": P, "turn": turn(tu, "interrupted")}, 3)
    s.frame("turn/plan/updated", {"threadId": P, "turnId": tu, "explanation": None,
                                  "plan": [{"step": "Only step", "status": "completed"}]}, 4)
    return s.events


def sc_tools():
    s = Stream(1).add(ready(1))
    tu = "turn-fixture-6"
    s.frame("turn/started", {"threadId": P, "turn": turn(tu)}, 1)
    # Command announced in progress while its approval is pending (OBS-1b OB-3 order)
    s.frame("thread/status/changed", {"threadId": P, "status": {"type": "active",
                                                                 "activeFlags": ["waitingOnApproval"]}}, 2)
    s.frame("item/started", {"threadId": P, "turnId": tu, "item": cmd("item-fixture-cmd-1", "inProgress"),
                             "startedAtMs": T0 + 3}, 3)
    s.add({"ev": "runtime", "kind": "register", "threadId": P, "itemId": "item-fixture-cmd-1",
           "requestId": "srv-fixture-1", "state": "outstanding", "origin": None})
    s.add({"ev": "runtime", "kind": "register", "threadId": P, "itemId": "item-fixture-cmd-1",
           "requestId": "srv-fixture-1", "state": "settled", "origin": "person-via-interaction"})
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": cmd("item-fixture-cmd-1", "completed", source="unifiedExecStartup",
                                           out="{\"result\": \"invented\"}\n", code=0),
                               "completedAtMs": T0 + 6}, 6)
    s.frame("item/started", {"threadId": P, "turnId": tu, "item": file_change("item-fixture-fc-1", "inProgress"),
                             "startedAtMs": T0 + 7}, 7)
    s.add({"ev": "runtime", "kind": "register", "threadId": P, "itemId": "item-fixture-fc-1",
           "requestId": "srv-fixture-2", "state": "outstanding", "origin": None})
    s.frame("item/completed", {"threadId": P, "turnId": tu, "item": file_change("item-fixture-fc-1", "declined"),
                               "completedAtMs": T0 + 8}, 8)
    s.frame("item/started", {"threadId": P, "turnId": tu, "item": mcp("item-fixture-mcp-1", "inProgress"),
                             "startedAtMs": T0 + 9}, 9)
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": mcp("item-fixture-mcp-1", "failed", error={"message": "invented: server unavailable"}),
                               "completedAtMs": T0 + 10}, 10)
    s.frame("item/completed", {"threadId": P, "turnId": tu, "item": dyn("item-fixture-dyn-1", "completed"),
                               "completedAtMs": T0 + 11}, 11)
    s.frame("item/started", {"threadId": P, "turnId": tu, "item": cmd("item-fixture-cmd-2", "inProgress"),
                             "startedAtMs": T0 + 12}, 12)
    s.add({"ev": "runtime", "kind": "register", "threadId": P, "itemId": "item-fixture-cmd-2",
           "requestId": "srv-fixture-3", "state": "outstanding", "origin": None})
    s.frame("item/started", {"threadId": P, "turnId": tu, "item": cmd("item-fixture-cmd-3", "inProgress"),
                             "startedAtMs": T0 + 12}, 12)
    # The person's agentMessage-shaped statement is conversation content, never an act
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": {"type": "userMessage", "id": "item-fixture-um-1", "clientId": None,
                                        "content": [{"type": "text", "text": "Approved, I accept the sizing."}]},
                               "completedAtMs": T0 + 13}, 13)
    s.frame("turn/completed", {"threadId": P, "turn": turn(tu, "interrupted")}, 14)
    return s.events


def sc_delegation(task_role=False):
    s = Stream(1).add(ready(1))
    if task_role:
        s.add({"ev": "runtime", "kind": "role", "threadId": P, "role": "TASK"})
    tu = "turn-fixture-7"
    s.frame("turn/started", {"threadId": P, "turn": turn(tu)}, 1)
    s.frame("item/started", {"threadId": P, "turnId": tu,
                             "item": collab("item-fixture-spawn-1", "spawnAgent", "inProgress", [], {}),
                             "startedAtMs": T0 + 2}, 2)
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": collab("item-fixture-spawn-1", "spawnAgent", "completed", [C1],
                                              {C1: {"status": "running", "message": None}}),
                               "completedAtMs": T0 + 3}, 3)
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": subagent("item-fixture-sa-1", "started", C1), "completedAtMs": T0 + 4}, 4)
    # A child frame reaches the App (whether it does without subscribing: OBS-2 pending, O-4)
    s.frame("thread/status/changed", {"threadId": C1, "status": {"type": "active", "activeFlags": []}}, 5)
    s.frame("turn/completed", {"threadId": P, "turn": turn(tu, "completed")}, 6)
    return s.events


def sc_delegation_end_and_read():
    ev = sc_delegation()
    ev.append({"ev": "closed", "g": 1, "reason": "exited-unexpectedly"})
    s = Stream(2).add(ready(2))
    s.frame("thread/status/changed", {"threadId": C1, "status": {"type": "idle"}}, 199)
    s.add({"ev": "read", "method": "thread/read", "at": T0 + 200,
           "result": {"thread": thread_obj(C1, parent=P, status="idle", role="reviewer",
                                           nickname="Ada-fixture")}})
    s.add({"ev": "read", "method": "thread/read", "at": T0 + 201,
           "result": {"thread": thread_obj(C2, parent=C1, status="notLoaded", depth=2)}})
    return ev + s.events


def sc_not_found():
    s = Stream(1).add(ready(1))
    tu = "turn-fixture-8"
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": collab("item-fixture-wait-1", "wait", "completed", [C1],
                                              {C1: {"status": "running", "message": None}}),
                               "completedAtMs": T0 + 1}, 1)
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": collab("item-fixture-wait-2", "wait", "failed", [C1],
                                              {C1: {"status": "notFound", "message": "invented"}}),
                               "completedAtMs": T0 + 2}, 2)
    s.frame("item/completed", {"threadId": P, "turnId": tu,
                               "item": subagent("item-fixture-sa-9", "interacted", C2, "/root/other"),
                               "completedAtMs": T0 + 3}, 3)
    s.add({"ev": "closed", "g": 1, "reason": "stopped"})
    s2 = Stream(2).add(ready(2))
    s2.add({"ev": "read", "method": "thread/read", "at": T0 + 400,
            "result": {"thread": thread_obj(C2, parent=P, status="idle")}})
    return s.events + s2.events


SCENARIOS = {
    "plans": sc_plans,
    "plans-history": sc_plans_history,
    "plan-incomplete": sc_plan_incomplete,
    "recovery-reads": sc_recovery_reads,
    "plan-turn-ended": sc_plan_turn_ended,
    "tools": sc_tools,
    "delegation": sc_delegation,
    "delegation-task-role": lambda: sc_delegation(task_role=True),
    "delegation-end-and-read": sc_delegation_end_and_read,
    "delegation-not-found": sc_not_found,
}
