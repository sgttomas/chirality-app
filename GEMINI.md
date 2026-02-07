# Chirality Command Center // Project Memory

## System Architecture & Capability Report (v0.5 Prototype)

**Operational Model:** "The Glass Cockpit" / Filesystem-as-State
**Primary Function:** A GUI-wrapped Agentic CLI that orchestrates local development workflows via the Anthropic API.

### 1. Technical Stack
*   **Frontend:** Next.js (App Router), React, Tailwind CSS (v4).
*   **Design System:** "Neural/Glass" aesthetic. Dark mode, glassmorphism, EB Garamond (Serif) typography for UI, JetBrains Mono for data/code.
*   **Backend:** Next.js API Routes (`/api/chat`, `/api/fs`, `/api/project`) acting as a local proxy.
*   **State Persistence:** Local filesystem (`.sessions.json`) for session context (CWD, Env Vars); `localStorage` for UI preferences and API keys.
*   **AI Engine:** Anthropic SDK (Claude 3.5 Sonnet/Haiku) via direct API Key.

### 2. Agentic Architecture (The "Claude Code" Replication Layer)
The application replicates the functionality of the `claude-code` CLI tool but wraps it in a persistent, multi-modal GUI.

**Core Capabilities:**
*   **Tool Use / Function Calling:**
    *   `execute_command(cmd)`: Runs shell commands (`git`, `npm`, `ls`) directly on the host machine.
    *   `read_file(path)`: Reads raw content from the local filesystem.
    *   `write_file(path, content)`: Creates or overwrites files locally.
    *   `list_directory(path)`: Scans folder contents.
*   **Session Persistence:**
    *   Tracks **Current Working Directory (CWD)** via `.sessions.json`.
    *   Persists Environment Variables across turns.
    *   `cd` commands executed by the agent persist for subsequent messages.
*   **ANSI Rendering:** Shell output is captured and rendered with full ANSI color support (`ansi-to-html`).
*   **Dynamic Context Injection:**
    *   **System Prompt:** Automatically reads `README.md` and `AGENTS.md` on every request.
    *   **Auto-Prompting:** Automatically injects instructions (e.g., "Read agents/AGENT_DECOMP.md...") when switching Personas or Task Variants.

### 3. User Experience Modes (The "Views")

**A. The Portal (Home)**
*   **Purpose:** Navigation and Status.
*   **Features:**
    *   **Hex Grid:** Symmetrical, interconnected navigation to Agent Personas.
    *   **Dynamic Dashboard:** Scans any selected local folder for `PKG-*/1_Working/DEL-*` structures and displays real-time status from `_STATUS.md`.

**B. The Workbench (Persona-Driven)**
*   **Purpose:** Interactive, conversational engineering tasks.
*   **Layout:** 3-Pane `ResizableLayout` (Chat | Deliverable Tree | Live Preview).
*   **Mechanism:** Agent Persona switching (e.g., `DECOMP`, `CHANGE`) triggers auto-initialization.

**C. The Pipeline (Task-Driven)**
*   **Purpose:** High-volume, straight-through processing.
*   **Mechanism:** Select **Task Family** (`PREP*`, `AUDIT*`) -> Select **Variant** -> Auto-load instructions.
*   **Layout:** Sidebar focuses on "File Context" rather than navigation.

**D. Direct Link (Raw Terminal)**
*   **Purpose:** Ad-hoc CLI access.
*   **Mechanism:** `mode="direct"`. No persona framing. Pure System Session.

### 4. Key Implementation Patterns
*   **ResizableLayout:** A unified wrapper component that handles the 3-pane flexbox logic and resizers for all interactive views.
*   **ChatPanel:** A self-contained component handling message history, API key management (localStorage), session switching, and directory navigation.
*   **SystemFileTree:** Lazy-loading file browser that allows navigation outside the project root (unrestricted system access).

### 5. Future Roadmap Items (Identified during dev)
*   **Streaming Responses:** Currently, the agent response waits for full completion. Streaming text would improve "terminal feel."
*   **Interactive Input:** The agent cannot handle interactive prompts (e.g., password requests).
*   **Diff View:** The "Preview" pane currently shows the *current* state. A true "Diff" view for proposed changes would be valuable.
