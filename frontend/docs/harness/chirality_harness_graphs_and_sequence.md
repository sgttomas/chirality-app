# Chirality Agent Harness (Claude Code Subprocess) — Architecture Graphs & Turn Sequence

This document contains three complementary views of the **AGENT_HARNESS_SPEC-v2.3** implementation:

1. **Module dependency graph** — how the GUI, API routes, and harness modules depend on each other at runtime.
2. **Implementation plan dependency graph** — how the build phases depend on each other (what must be implemented first).
3. **Single `/turn` sequence diagram** — the exact event ordering for one streamed turn over SSE, from request to process exit.

All diagrams are provided in **Mermaid** syntax for easy rendering in GitHub, Obsidian, Notion (Mermaid-enabled), or Mermaid Live.

---

## 1) Module dependency graph (runtime)

```mermaid
flowchart LR
  subgraph GUI["Chirality GUI (Next.js)"]
    Chat["Chat Pane"]
    Term["Terminal Pane"]
    Files["File Tree / Preview"]
  end

  subgraph API["Next.js API Routes (server-side)"]
    Turn["POST /api/harness/turn\n(SSE: UIEvents)"]
    Interrupt["POST /api/harness/interrupt"]
    SessCreate["POST /api/harness/session/create"]
    SessList["GET /api/harness/session/list"]
    SessGet["GET /api/harness/session/:id"]
    SessDel["DELETE /api/harness/session/:id"]
  end

  GUI --> Turn
  GUI --> Interrupt
  GUI --> SessCreate
  GUI --> SessList
  GUI --> SessGet
  GUI --> SessDel

  subgraph Harness["Harness Modules (per v2.3)"]
    SM["SessionManager\n(create/resume/save/list/delete)\n(.chirality/sessions/*.json)"]
    PM["PersonaManager\n(load/list/buildSystemPrompt)\n(frontmatter + context assembly)"]
    CCM["ClaudeCodeManager\n(startTurn/interrupt/kill)\n(child process + run orchestration)"]
    SP["StreamParser\n(NDJSON → UIEvents)\n(defensive JSON parsing)"]
    ENV["EnvFilter\n(denylist → whitelist)\n(API key never logged)"]
    LOG["Observability Logger\n(JSONL + rotation)\n(.chirality/logs/harness.log)"]
  end

  subgraph External["External Systems"]
    FS["Filesystem\n- projectRoot/README.md\n- projectRoot/AGENTS.md\n- projectRoot/agents/AGENT_*.md\n- .chirality/prompts/*\n- .chirality/sessions/*\n- .chirality/logs/*"]
    CLI["Claude Code CLI process\n(claude -p ... --output-format stream-json)"]
    CCStore["Claude Code session store\n(~/.claude/...)"]
    OS["OS signals\n(SIGINT/SIGTERM/SIGKILL)"]
  end

  Turn --> SM
  SM -->|Session (incl. claudeSessionId)| Turn
  Turn -->|Session + message| CCM

  CCM --> PM
  PM --> FS
  PM -->|writes| FS

  CCM --> ENV
  ENV -->|filtered env| CLI

  CCM -->|spawn| CLI
  CCM --> OS
  CLI --> CCStore

  CLI -->|stdout: NDJSON| SP
  SP -->|UIEvents| Turn
  Turn -->|SSE UIEvents| GUI

  Turn -->|save after completion| SM
  SM --> FS

  CCM --> LOG
  LOG --> FS
```

---

## 2) Implementation plan dependency graph (phases)

```mermaid
flowchart TD
  P1["Phase 1\nClaudeCodeManager + StreamParser\n- spawn claude -p\n- env filtering\n- NDJSON parsing → UIEvents\n- interrupt/kill\n- basic tests"]
  P2["Phase 2\nPersonaManager + Context Injection\n- frontmatter parsing\n- prompt assembly + caching\n- prompt file output\n- 16k token budget truncation"]
  P3["Phase 3\nSessionManager + Persistence\n- .chirality/sessions/*.json\n- claudeSessionId capture/resume path\n- save hooks"]
  P4["Phase 4\nAPI Routes + GUI Wiring\n- SSE /turn stream\n- interrupt endpoint\n- session CRUD\n- UI event routing"]

  P1 --> P2
  P1 --> P3
  P1 --> P4
  P2 --> P4
  P3 --> P4
```

---

## 3) `/turn` sequence diagram (exact event ordering)

```mermaid
sequenceDiagram
  autonumber
  participant GUI as Chirality GUI
  participant API as /api/harness/turn (SSE)
  participant SS as SessionStore
  participant PM as PersonaManager
  participant CCM as ClaudeCodeManager
  participant ENV as EnvFilter
  participant CLI as Claude Code (child process)
  participant SP as StreamParser
  participant LOG as JSONL Logger

  GUI->>API: POST /api/harness/turn { sessionId, message, opts }
  API-->>GUI: 200 text/event-stream (SSE opened)

  API->>SS: load(sessionId)
  SS-->>API: Session{ id, mode, persona, projectRoot, claudeSessionId? }

  API->>PM: buildPromptFile(session, opts)
  PM->>PM: read README.md / AGENTS.md / persona md (cached by mtime)
  PM->>PM: apply token budget + truncation rules
  PM-->>API: { systemPromptFilePath }

  API->>CCM: startTurn(session, message, systemPromptFilePath, opts)

  CCM->>ENV: filterEnv(process.env) (denylist → whitelist)
  ENV-->>CCM: filteredEnv

  CCM->>CLI: spawn claude -p ... --output-format stream-json --include-partial-messages --verbose --append-system-prompt-file <file> [--resume <claudeSessionId>] ...
  note over CLI,CCM: Claude Code runs its own agent loop + tools internally

  par stdout NDJSON stream
    CLI-->>SP: NDJSON: { type:"system", subtype:"init", session_id, model, tools... }
    SP-->>API: UIEvent: session:init { sessionId, claudeSessionId, model, tools }
    API-->>GUI: SSE: session:init
    API->>SS: update(sessionId, { claudeSessionId })
    SS-->>API: ok

    loop token streaming (0..N)
      CLI-->>SP: NDJSON: stream_event text_delta
      SP-->>API: UIEvent: chat:delta { sessionId, text }
      API-->>GUI: SSE: chat:delta
    end

    loop tool executions (0..M)
      CLI-->>SP: NDJSON: stream_event content_block_start(tool_use)
      SP-->>API: UIEvent: tool:start { sessionId, toolUseId, name, input }
      API-->>GUI: SSE: tool:start

      note over CLI: Claude Code runs tool (Bash/Read/Edit/etc)

      CLI-->>SP: NDJSON: { type:"user", message:{ content:[{ type:"tool_result", tool_use_id, ... }] } }
      SP-->>API: UIEvent: tool:result { sessionId, toolUseId, content, isError }
      API-->>GUI: SSE: tool:result

      loop more token streaming (0..K)
        CLI-->>SP: NDJSON: stream_event text_delta
        SP-->>API: UIEvent: chat:delta
        API-->>GUI: SSE: chat:delta
      end
    end

    CLI-->>SP: NDJSON: { type:"result", subtype:"success", ...usage/cost..., result:"final text" }
    SP-->>API: UIEvent: chat:complete { sessionId, text }
    API-->>GUI: SSE: chat:complete

    SP-->>API: UIEvent: session:complete { sessionId, costUsd, usage }
    API-->>GUI: SSE: session:complete

    API->>SS: save(sessionId, { updatedAt, lastCost, lastUsage })
    SS-->>API: ok

    API->>LOG: append(turn summary + key events) (redacted)
    LOG-->>API: ok
  and stderr (debug)
    CLI-->>CCM: stderr lines (debug)
    CCM->>LOG: append(stderr) (redacted)
  end

  CLI-->>CCM: process exit { code, signal }
  CCM-->>API: exit(code, signal)
  API-->>GUI: SSE: process:exit { sessionId, code, signal }

  API-->>GUI: SSE stream closed
```
