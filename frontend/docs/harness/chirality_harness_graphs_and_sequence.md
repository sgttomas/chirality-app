# Chirality Agent Harness (Anthropic Agent SDK) — Architecture Graphs & Turn Sequence

This document describes the SDK-only harness runtime after wholesale cutover.

1. Module dependency graph (runtime)
2. Implementation dependency graph (cutover-oriented)
3. `/api/harness/turn` sequence diagram

## 1) Module dependency graph (runtime)

```mermaid
flowchart LR
  subgraph GUI["Chirality GUI (Next.js)"]
    Chat["Chat Pane"]
    Activity["Tool/Subagent Activity Pane"]
    Files["File Tree / Preview"]
  end

  subgraph API["Next.js API Routes"]
    Turn["POST /api/harness/turn\n(SSE: UIEvents)"]
    Interrupt["POST /api/harness/interrupt"]
    SessCreate["POST /api/harness/session/create"]
    SessBoot["POST /api/harness/session/boot"]
    SessList["GET /api/harness/session/list"]
    SessGet["GET /api/harness/session/:id"]
    SessDel["DELETE /api/harness/session/:id"]
  end

  GUI --> Turn
  GUI --> Interrupt
  GUI --> SessCreate
  GUI --> SessBoot
  GUI --> SessList
  GUI --> SessGet
  GUI --> SessDel

  subgraph Harness["Harness Modules"]
    SM["SessionManager\n(create/resume/save/list/delete)"]
    PM["PersonaManager\n(build append prompt + model)"]
    AR["AttachmentResolver\n(paths → content blocks)"]
    ASM["AgentSdkManager\n(startTurn/interrupt/kill)"]
    MAP["AgentSdkEventMapper\n(SDKMessage → UIEvent)"]
    LOG["Observability Logger\n(JSONL + rotation)"]
  end

  subgraph External["External Systems"]
    SDK["Anthropic Agent SDK query()"]
    FS["Filesystem\nREADME/AGENTS/personas\n.chirality/sessions\n.chirality/logs"]
  end

  Turn --> SM
  Turn --> AR
  Turn --> ASM
  ASM --> PM
  AR --> FS
  PM --> FS
  ASM --> SDK
  SDK --> MAP
  MAP --> Turn
  ASM --> LOG
  LOG --> FS
  SM --> FS
```

## 2) Implementation dependency graph (cutover)

```mermaid
flowchart TD
  P1["P1\nDependency + contracts\n(types/defaults + SDK manager scaffolding)"]
  P2["P2\nRuntime cutover\n(index/routes + parity options + logging)"]
  P3["P3\nLegacy removal\n/api/chat + CLI manager + NDJSON parser"]
  P4["P4\nValidation + docs sync\nSDK-native scripts + runbooks"]
  P5["P5\nMerge gates\nlint + tsc + section8 + manual parity"]

  P1 --> P2 --> P3 --> P4 --> P5
```

## 3) `/api/harness/turn` sequence diagram

```mermaid
sequenceDiagram
  autonumber
  participant GUI as Chirality GUI
  participant API as /api/harness/turn (SSE)
  participant SS as SessionManager
  participant AR as AttachmentResolver
  participant PM as PersonaManager
  participant ASM as AgentSdkManager
  participant SDK as Agent SDK query()
  participant MAP as AgentSdkEventMapper
  participant LOG as Logger

  Note over GUI,API: Optional prewarm boot path
  GUI->>API: POST /api/harness/session/boot { sessionId }
  API->>SS: resume(sessionId)
  API->>PM: getBootFingerprint(persona, mode)
  API->>ASM: startTurn(bootstrap message, plan mode)
  API->>SS: save(claudeSessionId, bootFingerprint, bootedAt)
  API-->>GUI: 200 { session, boot }

  GUI->>API: POST /api/harness/turn { sessionId, message, opts, attachments? }
  API-->>GUI: 200 text/event-stream

  API->>SS: resume(sessionId)
  SS-->>API: Session (projectRoot/persona/mode/claudeSessionId/model)

  opt attachments provided
    API->>AR: resolveAttachmentsToContentBlocks(message, attachmentPaths)
    AR-->>API: contentBlocks (+ per-file errors)
  end

  API->>PM: buildSystemPrompt(projectRoot, persona, mode)
  PM-->>API: base prompt (+ instructionRoot context)

  API->>ASM: startTurn(session, message, merged opts, contentBlocks?)
  ASM->>SDK: query({ prompt/content, options })

  loop SDK stream messages
    SDK-->>ASM: SDKMessage
    ASM->>MAP: mapSdkMessageToUiEvents
    MAP-->>ASM: UIEvent[]

    alt session:init
      ASM-->>API: session:init
      API->>SS: save(claudeSessionId/model)
      API-->>GUI: SSE session:init
    else chat/tool/session events
      ASM-->>API: mapped UIEvent
      API-->>GUI: SSE UIEvent
    end
  end

  ASM->>LOG: process:exit + parity logs
  ASM-->>API: process:exit
  API->>SS: terminal save
  API-->>GUI: SSE process:exit
  API-->>GUI: stream close
```
