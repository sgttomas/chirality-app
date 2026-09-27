# Pinned references

Standing: **source identification.** This file names the exact revisions and
releases the v4 conceptual undertaking examines or preserves. It makes no
product claim. The source inventory, with what each source can support, is
[`SOURCE_INVENTORY.md`](SOURCE_INVENTORY.md).

## 1. Investigation revision

The revision the v4 undertaking reads for tracked sources.

| Field | Value |
|---|---|
| Repository | `sgttomas/chirality` |
| Revision | `2b0572fe049c8ffaa02d61b7dbbc3ae41bc589f6` (`main`, committed 2026-09-25 13:37 −0600, merge of PR #909) |
| Relation to `origin/main` | Equal when the undertaking began (fetched 2026-09-25) |
| Read with | `git show 2b0572fe0:<path>` from any checkout of the repository |

Tracked paths cited in v4 documents refer to this revision unless another
revision is named. Later changes on `main` do not alter the evidence base
until the working record admits them.

## 2. Fallback release (v3.0.1)

The published product that remains the fallback until the owner decides v4
has replaced it (OD-09).

| Field | Value |
|---|---|
| Release repository | `sgttomas/chirality-app` (public) |
| Release | [Chirality v3.0.1](https://github.com/sgttomas/chirality-app/releases/tag/v3.0.1), published 2026-09-20T03:29:16Z, marked Latest |
| Tag target | `95fa13d35bf3e75db217aa6b1da25a8573ae8eea` (release repository's framework snapshot) |
| Desktop application source | `sgttomas/chirality@485051eac923c759238948a54cd7bb094eee4899` (merge of PR #823, 2026-09-19), as stated in the release notes |
| Installer asset | `Chirality-3.0.1-arm64.dmg`, 339,832,416 bytes, SHA-256 `eea43a0d973d1cd401da58cfd7a7156d9e932503fbb0c469a799e3cec73fd2e3` (GitHub asset digest) |
| Checksum asset | `Chirality-3.0.1-arm64.dmg.sha256`, SHA-256 `b9761c0cfc925cbf6f172e5592f57716782e74a2b02a3478c3f1cd8866689134` |
| Platform | Apple Silicon, macOS 15 or later; signed and notarized per the release notes |

The desktop source commit is an ancestor of the investigation revision. The
84 commits between them that touch `projects/chirality-app-dev/` are
unreleased work; they are evidence about the v3 line, not part of the
fallback.

Earlier releases in `sgttomas/chirality-app`, for history:

| Release | Published | Tag target |
|---|---|---|
| v3.0.0 | 2026-09-13 | `343e6eed9d1a1b51ff4b087c0f73fcda305b0c7c` |
| v2.0.0 "Shared runtime and governed public export" | 2026-07-24 | `35a36faff275de1918008d46b7c418b43505bbb5` |
| v1.3.0 "Subagents and UI polish" | 2026-02-22 | no tag ref in the release repository; the release record names `main` |
| v1.2.0 "Official Mac Desktop App release" | 2026-02-18 | as above |
| v1.1.0 | 2026-02-16 | as above |
| v1.0.1 "Official public release … for Mac and Windows" | 2026-02-09 | as above |

## 3. Original checkout and Git-ignored archives

| Field | Value |
|---|---|
| Path | `/Users/ryan/ai-env/projects/chirality` |
| Checked-out revision | `main@06aff05a412b9e25ad022e5fc629c77ee51efbc6` (2026-09-23), 129 commits behind the investigation revision |
| Role | Holds Git-ignored archives that worktrees do not carry. Its tracked files are older than the investigation revision; read tracked sources from §1. |

The archive inventory, access rule, and content digests are in
[`archives/ARCHIVES.md`](archives/ARCHIVES.md).

## 4. Concurrent activity noted at start

| Item | Consequence for this undertaking |
|---|---|
| Branch `claude/archive-agent-runs`, commit `9ed9102a5` (2026-09-25 14:00, D-GOV-45), unmerged when observed | Would move closed agent run records out of the working tree of `main`, holding them at the annotated tag `archive/agent-runs-2026-09-25` (→ `8007c592`). Run records cited from the investigation revision remain readable there by `git show 2b0572fe0:<path>` whether or not the branch merges. |
| Tag `archive/agent-runs-2026-09-25` | Exists; points at `8007c59270bc83035eac8ec6eab65926cfe8668c`. |

## 5. This undertaking

| Field | Value |
|---|---|
| Working root | `projects/chirality-app-v4/` |
| Branch | `claude/chirality-app-v4-architecture-9f35c4` (worktree `chirality-app-v4-architecture-9f35c4`) |
| Run record | [`execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/`](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/) |
