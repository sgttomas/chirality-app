# Connector source observation CSP-v0.1

Named proposal C3-S2-OBS-01. Status: PROPOSED technical producer definition,
subject to independent review and manager selection. Basis: CFB-v0.3 with
its pinned v0.2 base; CRP-v0.3; DEL-07-02 REQ-002/004 and VER-002/004.
Existing contracts, schemas, saved-account reader and historical evidence
remain unchanged. This defines a bounded observation preview, not completed
source reconstruction, source admission or a performed native-selection act.

## 1. Selected smallest contribution

A dedicated native App source selector produces a host-private local text
snapshot. Preview the observed path, bytes/hash, bounded excerpts, revision
assertions and gaps for the same affected question. No account/source entry,
fact, supported conclusion, attachment supply or performed duty is emitted.
This first increment makes real local evidence available for reconstruction;
it does not force source-entry materialization when evidence is incomplete.

Production wiring may be implemented and exercised with injected selection
callbacks and scratch files offline. Actual native launch/selection witness
remains point-held; fixture selection is never labelled a person's act.
This definition authorizes no native launch by itself.

## 2. Session and native selection boundary

Require the explicit App project association used by the existing route view;
unknown/mismatched association refuses without falling back to cwd, thread,
Codex home or another project. Bind a host-owned observation session to that
project and one caller-supplied affected-question identity/text/asked/since
revision. Question revisions are requests, not observations about source bytes.
Freeze that question with each snapshot; later question edits create a new
preparation generation and cannot reattribute earlier evidence silently.

The renderer supplies only a session token/generation and a select action.
The native picker returns the path privately to the host. No IPC filename,
path, file body, digest, source DTO or imported saved account can mint a read
capability. Display paths and old selection references cannot reopen a source.
Cancel retains the previous observation explicitly labelled prior/historical
and the latest operation cancelled; it creates no new observation, read time
or successful-selection result. Stale session
completion cannot replace newer state. Selection observes bytes; it does not
supply them to Codex, a connector or any external destination.

For this initial slice, select one file within the explicitly associated
project. Reject paths outside that root and symlink traversal below the
resolved root; bind/open relative to retained verified directory handles with
no-follow semantics. Retain the established opened-directory versus mutable
pathname limitation from CRP: concurrent external renames can move an opened
object, and observations are not a continuous-path guarantee. Report detected
association/path changes; never silently redirect to a replacement. The
project boundary limits this slice's implementation; it is not a new global
source policy or an arbitrary-path approval. External files require a later
explicit receiving treatment; do not copy them into the project as a workaround.

## 3. Actual read observation

Open the selected regular file once, nonblocking where needed to avoid FIFO
hangs; reject directories/devices/FIFOs and symlinks. Read at most 262145 bytes
and accept at most 262144, matching the existing text carrier's bounded read
practice. Reject invalid UTF-8 and NUL-bearing content without truncation or
replacement decoding. The limit is a technical first-slice constraint, not a
claim that larger/nontext sources are invalid or unavailable everywhere.

Compute SHA-256 and preview text from the identical accepted byte buffer.
Record byte length, exact lossless path identity plus display path, observed
time/provenance, opened file identity and a fresh opaque observation reference.
The hash identifies bytes actually read; no claim that the file remained
unchanged throughout reading or after it is implied. If ordinary before/after
metadata checks detect mutation, report it and refuse a stable-preview claim;
matching checks cannot prove absence of transient writes. A mixed read is not
silently asserted to be a coherent historical revision. Retain only session
memory in this slice; process loss means capability/preview loss, not cold
reconstruction from path/hash DTOs.

Preview remains bound to that frozen buffer. Explicit reread/native reselection
creates a new observation; old preview is not silently updated. Reading a file
never establishes that its statements are correct or authoritative.

## 4. Revision standing — no inferred promotion

Preview carries these mutually explicit observations, not a route-account
`source.revision` claim:

| Kind | Exact meaning |
|---|---|
| unavailable | No revision evidence supplied; show revision gap and its effect/responsible route. |
| caller assertion | A caller entered a revision label; do not treat it as observed source metadata or Git evidence. |
| source text located | The frozen source contains the exact selected excerpt that the caller identifies as a revision statement; show its anchor and the caller's interpretation. Byte inclusion is checked; meaning, truth and authority are not. |
| Git object verified (later adapter only) | Resolved commit/tree/blob identity and read bytes are actually obtained from the selected repository at the requested revision; never enabled by a typed hash or working-tree match alone. |

A source can state a revision without that statement being authoritative;
locating a line proves inclusion only. Existing source schema permits the
source's own stated revision for non-repository sources but has no explicit
provenance slot to retain these preview distinctions. Therefore this slice
emits **no source entry or account**, even when revision text is located.
Do not overload `role`, `revision`, `fact.data` or gap prose to smuggle a
verified-revision meaning into an unchanged consumer. Deliberate later
materialization must define evidence/interpretation custody and consumer
presentation; choose a named schema successor only if existing fields cannot
preserve the needed distinction. It is not necessary to change schema now.

## 5. Anchors and excerpts

The producer accepts a line interval against an opaque observation reference,
not an arbitrary path. Lines are one-based, split on LF; CR before LF is
retained in the underlying bytes; a final empty segment after terminal LF is
not an additional selectable line. No Unicode normalization or whitespace
trimming changes the buffer. Empty files have zero selectable lines. Refuse
zero/reversed/out-of-range intervals. Return `L<n>` or `L<n>-L<m>`, the exact
selected text and its byte interval/hash relative to the whole snapshot.
Byte intervals are **zero-based, half-open `[start, end)`**, measured in the
original UTF-8 buffer, not character indices. A selected interval spans complete
selected lines: include each selected line's terminating LF when present,
including the last selected line's LF. Preserve the preceding CR in CRLF.
The last unterminated line includes all its remaining bytes. The excerpt hash
is SHA-256 of precisely `buffer[start:end]`; decoded excerpt text comes from
that same slice. Never append a missing newline. A terminal LF belongs to its
preceding line; it creates no additional selectable empty line. An LF-only
line is selectable and its excerpt includes that LF.

Examples below use JSON string escaping solely to display exact bytes; offsets
count decoded UTF-8 bytes, not characters in the displayed escape spelling.

| Original text | Selection | Byte interval | Exact excerpt |
|---|---|---|---|
| `"a\nb\n"` | L1 | [0, 2) | `"a\n"` |
| `"a\nb\n"` | L2 | [2, 4) | `"b\n"` |
| `"a\r\nb\n"` | L1 | [0, 3) | `"a\r\n"` |
| `"a\r\nb\n"` | L1-L2 | [0, 5) | `"a\r\nb\n"` |
| `"a\nb"` | L2 | [2, 3) | `"b"` |
| `"\n"` | L1 | [0, 1) | `"\n"` |
| `"é\nb"` | L1 | [0, 3) | `"é\n"` |
| `""` | L1 | refused: zero lines | none |

For `"a\n"`, L2 is refused: there is one selectable line, not two.
Check any caller-supplied expected excerpt against those exact bytes; mismatch
is explicit, never approximate matching. Escaped rendering is required.

An anchor proves a location within those observed bytes. It does not validate
an agent's paraphrase, supported conclusion, claimed revision or authority.
Source-content text is data, never executable instructions. Existing saved
account anchors remain literal; this producer does not activate source/evidence
links in the read-only reader or reinterpret historic anchor conventions.

## 6. Exact Git case and point of need

A selected working-tree file at a repository path supplies local bytes only.
Do not set its revision to HEAD, branch tip or a requested commit. Dirty files,
untracked files and unchanged files all retain this same observation boundary.
The first increment can show a requested Git revision as caller assertion and
an explicit unresolved Git-binding gap; it must not pretend the adapter exists.

The next bounded Git adapter, if selected, must start from explicit host-owned
repository/project and selected path identities; resolve the requested revision
to an actual full commit, locate that tree's regular blob at the exact path,
and read/hash those blob bytes without filters, worktree substitution or network.
Observe both commit and blob identities and distinguish them from local read
hashes. Since/at comparisons read both exact commits separately. Missing object,
path, non-blob/gitlink, ambiguity or failure becomes a gap; no fetch, shell
interpolation, hooks, remote helpers or external content conversion is allowed.
Selecting a current local file does not prove it existed at the requested pin.
The adapter's invocation/path resolution and host support need their own exact
implementation brief and tests; this definition does not release that code
or grant arbitrary repository/path RPC access.

## 7. Gaps, reconstruction and actor boundaries

For missing/unreadable/oversized/nontext/outside-slice sources, missing revision,
unresolved requested commit or anchor mismatch, retain same-question continuity
and explicit observed reason/effect. Responsibility is a caller/manager-assigned
route, visibly unassigned until actually supplied; never invent an actor.
Independent supported work is not blocked by a failed observation. No source
read is invented and no unsupported question part becomes supported.

Agent-authored facts/conclusions require a separate actual locate/compare
contribution with evidence, not this read operation. Manager review/integration
and necessary person cross-undertaking coordination remain separate actual
acts. Default preview shows these unperformed/outstanding; not-required needs
an explicit reason from its accountable actor. Do not author a performed duty,
need satisfaction, connector adoption/current standing, readiness, completion
or permission. C1 connector semantics remain independent inputs; no response
is needed to expose a file route and no provider wire contract is introduced.

## 8. Offline acceptance boundary

Required implementation tests use real scratch-file reads with injected picker
callbacks, never labelled an actual native selection witness. Check:

- Correct bytes/hash/path/length; empty file; max size and max+1; invalid UTF-8,
  NUL, unreadable/missing, directory/FIFO and symlink; no partial success.
- Cancel, stale session/generation, project mismatch/outside root, renderer
  forged path/hash/reference, concurrent replacement and observed mutation.
- Same frozen preview after file changes; explicit reread yields new identity;
  no cold recreation from exported DTO, no send or persistence side effect.
- Exact line/byte anchors for LF/CRLF, Unicode, terminal newline and empty file;
  every §5 example must assert exact zero-based half-open offsets, retained
  last-line LF/CRLF and excerpt hash; out-of-range and changed/mismatched
  expected excerpt refuse.
- Typed Git hash, source revision text and worktree HEAD coincidence never
  produce Git-verified standing or a source/account entry.
- Same question under constructed absent/stale/partial/failing triggers;
  explicit gaps/responsibility assignment and no duty/connector promotion.
- UI renders revision standing, gaps and read limits separately, with escaped
  source content; existing read-only account view remains unchanged.

Later Git adapter requires exact commit/blob fixtures including dirty worktree,
changed branch tip, missing historic path/object, distinct since/at anchors,
non-blob and invalid revision; no network/provider dependency. Native App
witness and complete source reconstruction remain separate obligations.

## 9. Technical selection and consequential limits

Within DEL-07-02 ownership: bounded observation DTO/session, size and text limits,
anchor syntax, native selector binding, offline tests and preview presentation.
Independent review and manager selection precede implementation fan-in.
No additional human gate is created for these technical details. New external
source policy, changed persisted meaning, provider/fleet prerequisite, actor-act
semantics or owner-reserved authority returns to HELP_HUMAN before adoption.
