# R14 rulings — on the receiver comparisons V18-1…V18-4

Integrator: HELP_HUMAN. Inputs: [comparisons/V18-1.md](comparisons/V18-1.md)
(2 BLOCKING, 5 MAJOR), [V18-2.md](comparisons/V18-2.md) (3 MAJOR),
[V18-3.md](comparisons/V18-3.md) (4 MAJOR), [V18-4.md](comparisons/V18-4.md)
(4 MAJOR), each with MINOR findings and NOTEs. R1–R13 stand. Every MINOR
finding is fixed by the repair node that owns its file unless it conflicts
with a ruling here; NOTEs are optional and reported.

## R14-1 One record container: RS holds, EXEC's entry bodies are referenced (V18-1 B-1) — INTEGRATION

Option (b) of V18-1, following the one precedent in the set (RS
`settings_version` already references AS's settings-in schema).

- RS format 0.1 is the only container: one entry per line, RS's header on
  every entry. EXEC's schema stops defining a container; it defines the
  **bodies** of the checkpoint entry kinds (CE-1…CE-19), and RS's R8 entry
  kinds reference those bodies (`$ref` by relative path).
- Every CE kind gets an RS entry kind, including those RS lacks today:
  `act_counted`, `item_decision`, `observation_lost`, `observation_recovered`,
  and an App-side `continued_past` annotation target. `recording_gap` becomes
  RS's "record write failed" limit, written in RS's order (after the late
  entries).
- **Shared spellings:** disposition words are WD §4.3.4's, spaced ("not
  reached"); the performance ordinal starts at 1; annotations are RS's
  structured objects; `run_ended.by` includes "run owner".
- LOOP §2.3's checkpoint events map to the same RS kinds (RS states the
  mapping; LOOP cites it).
- A prototype converts EXEC's valid example into RS entries and validates
  them: every entry valid, none without a kind.

## R14-2 An identified request in an App run (V18-1 B-2) — DERIVED

RS itself gives App-run identification to EXEC, and DECISION-K1 K1-1 has the
product record what it observes. So:

- RS drops "agent message naming kind, subject and purpose" as a way an App
  run identifies a request, and corrects its App-run example.
- RS `act_request`: `actKind`, `subject` and `purpose` become optional, each
  with an explicit "not named by the request" value; RS adds EXEC's request
  forms (including the host-recorded request) and the association with the
  current arrival.
- ADAPTER §7.7's sentence about the agent's request cites EXEC RC-5.
- The host loop's "A8 request issued" event is unchanged.

## R14-3 The record vocabulary covers what its suppliers emit (V18-1 M-1…M-5; V18-4 M-1; V18-2 M-3) — DERIVED

RS says it adopts P §9 and ADAPTER's evidence limits; it adds, in text and
schema: P's two new outcomes (refused — identity conflict; not known to
host); ADAPTER's outcome values and request kinds; ADAPTER's six evidence
labels; "act offered without a capture-evidence reference" (CA CAF-24, EXEC
A-7); R13-1's "basis lineage not supplied" and R13-2's two limits; an entry
for observation lost and recovered and for per-item decisions (via R14-1); a
"does not pass" value for the compatibility report; outcome values for the
loop's own refusals (parse, schema, turn cancel). The origin value is
`host`, and the source root is required, as WD and RS's own text say.

## R14-4 ADAPTER's observations carry what EXEC needs (V18-3 M-1, M-2, M-4; V18-4 M-2) — DERIVED

- Act observations carry the act's identity and capture time as the host
  records them, each with a "not supplied by host" value.
- A host-recorded request is an observation of its own; a request in the App
  conversation is EXEC's (RC-5), not ADAPTER's.
- An accepted item that is later refused stale or fails at application gets
  its observation (P PT-15, PT-16), for EXEC MX-7 and MX-8 and WD §4.3.7.
- Dispatch is observed at item start, and completion updates the same
  record (OBS-1b: the command item's `source` changes from `agent` at start
  to `unifiedExecStartup` at completion, and the command is shell-wrapped).
  ADAPTER OM-1 and EXEC AW-2 say the same; the start-time `source` is the one
  that marks a model-issued call.

## R14-5 Capability names mapped to capability groups (V18-2 M-1) — INTEGRATION

WD adds a group column to its capability-name table citing HOSTING §8.4.
HOSTING owns the supplier facts, so where the two differ on a member
(`functionCallOutput`, `mcpServer/elicitation/request`, `thread/shellCommand`),
HOSTING's grouping stands unless WD's name would then mean something the
group does not offer; in that case the repair returns it. HOSTING closes F-27
by citing WD's table. EXEC EV-3's presence rule uses the mapping.

## R14-6 Outcome token (V18-2 M-2) — DERIVED

WD's rule says it follows the outcome owner. WD uses `applied` (P §9), in
text, schema and fixtures together.

## R14-7 Apply R13 everywhere it is not yet said (V18-3 M-3; V18-4 M-3, M-4; V18-1 m-14)

Every "awaiting R13" or "until R13" in C, ADAPTER, RS, CA, XT and LOOP is
replaced by what R13 rules: R13-1 in C §5.2, CF-5, U-C14, the read-result
schema note, ADAPTER RD-2, RS R11 and CA CAF-10; R13-2 in RS R11 and its
schema, ADAPTER §11, CA CAF-32 and CAF-34, XT XC-06; R13-5 in LOOP §5.3;
R13-6's observations in HOSTING, ADAPTER, EXEC (the MCP-path cells stay
pending, with OBS-1's reason; the command-line cells take OBS-1b) and LOOP
§4.1's observed column.

## R14-8 The four SCA-V4-002 arcs (V18-4)

- N-18: WD cites P-v0.8's contributions; item-left events become explicit in
  P's schema (not only derivable).
- N-21: EXEC's `left` entry keeps its cause; EXEC accepts that P may omit
  resulting-object identities and records "not supplied" in that case; EXEC
  cites P-v0.8.
- N-24: covered by R14-4; EXEC and ADAPTER cite each other at their Wave B
  versions; EXEC F-32 (who issues the host reads) is answered in ADAPTER
  from what ADAPTER and C already state (reads the model issues through the
  host's tools or command; any read the App itself issues, such as a catalog
  read for the required-tool check, named as such). If the existing texts do
  not settle it, the repair returns it for R15 rather than choosing.
- X-1: EXEC's list of AWAITING INPUT cases adds CH-31 (ii).
