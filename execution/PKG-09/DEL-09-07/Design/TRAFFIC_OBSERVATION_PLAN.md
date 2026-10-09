# V4-EXM-23 traffic observation plan

- Contribution: DEL-09-07/TOP-v0.1 (unit LHQ-U2, with `QUALIFICATION_DOSSIER.md` and three schemas beside this file)
- Status: DRAFT DEFINITION — proposed, not run. **No capture has been made.** Nothing here observes SWBPIPE or any host.
- Run and node: `APP-V4-DESIGN-PASS-4-20261003`, owner O-C, 2026-10-03.
- Serves: LHQ §5.4 (unchanged from v0.1 to v0.2) steps 23-0, 23-9 and 23-10 (parts P23-A…P23-F); REQ-006, AC-006, VER-006; the traffic part of OUT-002.
- Inputs: `LOCAL_HOST_QUALIFICATION.md` (LHQ-v0.2, sha256 d59a1ea011fd860139603fb78c20a3f66b04984f1bc2501ac0af74083876b8f1; re-pinned at the tranche-2 closeout under R23-21 item 4 from LHQ-v0.1 `20361a0b…`. The version step v0.1→v0.2 changes only §3 (CI-5). §5.4 and the LHQ-23 case this plan serves are unchanged); rulings cited by ID (R23-21): R23-14 item 1, R23-15); DEL-05-01/LOOP-v0.9 §5.1.1 and §5.2 (2bac33a883b176e24cd17e6fb78361efea63ce4c254810dcf8ab6e1d13cd7004; C1 re-pin, R23-21 item 4); DEL-04-02/AS-v0.9 §3.2 (4eca598f13c8c0745f94c605b8940a094b55e57b9f7478c989824af229085857; C1 re-pin, R23-21 item 4); DEL-04-03/RS-v0.9 R11, R15 (a91882e74064495c5758110deae4cbc7280f3b2a12d0df8592f5238d1afd16e5, the committed bytes at `cec590c5c3`; the version relied on; nothing here relies on the A16 rows added under R23-18, so the pin stays (R23-21 item 3)); DEL-01-01 `OBS_1_0.158.0.md` §8 and B.5 (7b984b541edca0b14534d29115e77642c587a32f830bdf25a94a7ecca882cc43); DEL-03-04/GUIDE-v0.6 HC-7.3, HC-7.9.
- **Pin basis.** Pin-independent. The App's own Codex process is attributed and set aside (§3); its start-up contacts at either pin are not a criterion here (K-12; DECISION-5 governs a host's agent).
- **Tool facts and their standing.** The facts in §2.1 were read on the owner's Mac on 2026-10-03 without running any capture: `sw_vers` (macOS 26.6.2, build 25G83); `tcpdump --version` (tcpdump 4.99.1, Apple version 158, libpcap 1.10.1); `man tcpdump` (pktap interface and packet-metadata sections); `ls -l /dev/bpf0 /dev/bpf1` (`crw-------  root  wheel`). They are *stated by the manual* or *observed as file permissions*. No metadata behaviour has been observed in a capture; §5 calibrates it on the candidate machine before reliance.

## 1. What the observation must establish

LHQ-23 verifies V4-HOST-02 during V4-EXM-20's run (V4-EXM-23 as amended; R23-15: the added stimuli are named, and V4-EXM-20's own parts do not depend on them):

| Part | Property | What the capture contributes |
|---|---|---|
| P23-A | Requests go only to the selected model service and to destinations the person allowed, in advance or by an in-work grant | Every contact by the subject processes, with destination and time, to compare with the allow list and grants in force |
| P23-B | A declined or disallowed request reaches no destination | The absence of any contact to the declined or disallowed destination after the decline or refusal |
| P23-C | Nothing else is contacted unless turned on | The absence of contacts outside the allowed set over the whole window |
| P23-D | Every destination contacted is recorded and shown | The captured set, compared both ways with the host's destination record (RS R15) |
| P23-E | An unsandboxed outside process is examined within its stated limit (applicable only when declared before the run, LHQ §5.4; R23-19) | Its observed contacts, reported beside its declared destinations, never claimed to match them (LOOP NW-16) |
| P23-F | Native enforcement | Absence in the capture, joined with the native layer's refusal record and the interface-script attempt (§7) |

The capture is the **independent** observation. The host's own destination record is the thing compared, never the evidence of itself (REQ-006: "a … selected request log shall not substitute").

## 2. Method

### 2.1 Primary: all-interface packet capture with process metadata (M-1)

On macOS, `tcpdump -i pktap,all` captures "packets from all interfaces, including loopback and tunnel interfaces", in pcap-ng, with per-packet metadata (`man tcpdump`). The metadata the manual lists includes interface, process name (`N`), process ID (`P`), process UUID (`U`), direction, flow identifier and service class; its filter keywords include `proc`, `pid`, `eproc` (effective process name) and `epid` (effective process ID). These are *stated by the manual*.

- **Why this method.** It is the only built-in method found that can attribute packets to the process that sent them, including loopback (a local model server on the same machine) and short-lived processes. OBS-1 used 250 ms socket snapshots and missed a ~30 ms process (OBS-1 B.5); snapshots cannot support "all traffic". **Inference, not stated by the manual:** that every outbound packet of a subject process carries its process metadata. The manual lists the metadata fields but does not say which packets carry them; inbound, kernel-generated and forwarded packets may carry none (BS-10). Calibration OV-1 and OV-2 test the claim on the candidate machine.
- **Privilege.** The BPF devices are `crw------- root wheel` on this Mac (observed), so the capture needs administrator rights. It is a permission the operating system asks for when the capture runs (R23-14 item 1; "the host" there is the examination machine, not SWBPIPE): the person starts the capture with their own administrator authentication, at run time. No agent holds or uses the person's credentials. If the person declines, LHQ-23 is *blocked* at its start, with the cause recorded (R23-20 item 2; LHQ LF-10); LHQ-20 can still run.
- **Snap length and payloads.** The capture keeps packet headers and the TLS ClientHello (for the server name), not payloads beyond that. The exact snap length is set at calibration (§5) and recorded. Payloads are not examined: V4-EXM-23 concerns destinations, not content.
- **Reading the metadata (method; PROPOSED).** The capture is written once with `-i pktap,all` to a pcap-ng file. Per-contact process fields are read from it with the display letters the manual lists (`-k NPUf`: process name, process ID, process UUID, flow identifier). The **effective process**, which the manual gives only as filter keywords, is read by filtered passes over the same file, one per subject process: `-Q "epid = ‹pid›"` and `-Q "eproc = ‹name›"`. Each packet found by such a pass is marked with that effective process. Packets with no process metadata are joined to a flow by the flow identifier `f` and take that flow's process; packets with neither go to BS-10. Calibration OV-2 tests the effective-process pass before any reliance on it.

### 2.2 Name resolution (M-2)

A destination is an address with, where obtainable, a name. Names come from (a) DNS answers in the same capture (UDP and TCP port 53, and multicast DNS) and (b) the TLS server name in the ClientHello. The name source is recorded per contact. Where neither is available (encrypted ClientHello, QUIC whose handshake is not decoded, DNS over HTTPS), the destination is the address only, with the limit "name not observed".

### 2.3 Process lineage (M-3)

The **subject process set** is the host application process and every process it starts, including outside processes (MCP servers). Lineage comes from three sources, each recorded with its source:

1. the pktap process ID and UUID on each packet;
2. the host's own outside-process record (LOOP NW-16; RS R15 `outside_process`), which names the processes it started;
3. process-start observations taken at the host's launch and at each outside-process start, for the parent relation.

A packet whose process is in the subject set, **or whose effective process is**, is a subject contact.

### 2.4 Cross-check (M-4)

Socket-table snapshots (`lsof -i`, `nettop`) run beside the capture. They do not establish completeness; they detect a gross capture failure: a long-lived connection seen in a snapshot but absent from the capture invalidates the window (§4 BS-4).

## 3. Attribution classes

| Class | Rule | Counts toward |
|---|---|---|
| **Subject** | Process or effective process is the host process or a child that is not an unsandboxed outside process | P23-A…P23-D: every subject contact must be allowed and recorded |
| **Outside process (unsandboxed)** | Process is an MCP server or other outside process the host started, not sandboxed (LOOP NW-16) | P23-E only: reported beside its declared destinations, within the stated limit "process network not observed"; never counted against P23-A or P23-D, and never claimed to match its declaration (LHQ 23-7, 23-9) |
| **App Codex** | Process in the App candidate's Codex process tree | Set aside and listed. DECISION-5 governs a host's agent; the App's Codex keeps the person's configuration (K-12) |
| **System on behalf (attributed)** | A system process whose effective process is in the subject set (for example name resolution, or a networking process acting for the host's interface) | Subject (by the effective process rule) |
| **System, not attributed** | A system process with no effective process in the subject set | Listed in an annex with times. Never counted as a host contact and never as "clean". Where its timing coincides with a subject action, it carries the limit "possibly caused by the host, not attributed" |
| **Other** | Any other process | Excluded; retained only as a count of processes and of packets (§6) |

All host traffic is in scope, not only the agent's: V4-EXM-23 says "all network traffic from the host is observed". A host's own update check or analytics is therefore a subject contact, judged by NW-14 ("off unless the person turns it on").

## 4. Blind spots (named; each produces a recorded limit)

| # | Blind spot | Effect | Treatment |
|---|---|---|---|
| BS-1 | Work done for the host by a system service without an effective-process mark (inference: certificate revocation checks, background URL sessions, some name lookups) | A contact the host caused may appear unattributed | "System, not attributed" annex. An entry whose timing coincides with a subject action is flagged "possibly caused by the host, not attributed" and, unless resolved by evidence (§5 baseline B-0), makes P23-C and, where its destination is not in the allowed set, P23-A *inconclusive* (§7) |
| BS-2 | Encrypted names (encrypted ClientHello, undecoded QUIC, DNS over HTTPS) | Destination known by address only | "name not observed"; the comparison uses the address and the host record's resolved address where it has one; otherwise the contact is *unmatched* |
| BS-3 | Traffic before the capture starts or after it stops | Missed contacts | The capture starts before the host launches and stops after every subject process exits (§5 sequence); a subject process alive outside the window makes the window incomplete |
| BS-4 | Packets the kernel drops | Missed contacts | tcpdump's drop count is recorded; any drop makes the window incomplete for P23-A, P23-C, P23-D |
| BS-5 | Communication that is not network traffic (Unix-domain sockets, XPC) | A local model server reached over a Unix socket is not captured | Recorded per configuration; that model-service contact is then evidenced only by the host record, with the limit "model service contact not captured (non-network IPC)" |
| BS-6 | Outside processes started outside the host's process tree (for example through the system's launch service) | Their traffic is not attributed | Reported with NW-16's "process network not observed"; never claimed absent |
| BS-7 | Process ID reuse | A later process inherits an ID | Attribution uses process ID together with process UUID where the metadata carries it |
| BS-8 | Effective-process marking behaviour is not observed on this OS version | Delegated traffic may not carry the host as effective process | Calibration OV-2 (§5) is a pass condition of P23-A, P23-C and P23-D (§7); until it holds, delegated traffic is "attribution not established" and those parts are *inconclusive* |
| BS-9 | Contacts made by a remote "local" model server (LOOP MS-11) onward from its own machine | Not visible from this machine | Out of scope: the host's contact is the server itself, which is captured |
| BS-10 | Packets with no process metadata (inbound, kernel-generated or forwarded) that no flow identifier joins to a process | Their process is unknown | Annex as "unattributed packet", treated like BS-1: flagged when coincident with a subject action, with the same effect on P23-A and P23-C unless resolved by B-0 |
| BS-11 | A configured system proxy, VPN relay or network extension that relays traffic | The captured destination is the relay, not the real destination | Precondition read and recorded before the run (OV-5): none configured. If one is configured and cannot be removed for the run, every contact through it is "destination behind relay", and P23-A and P23-D are *inconclusive* |

## 5. Calibration and run sequence (at run time, on the candidate machine)

Calibration runs on the identified candidate and configuration before the LHQ-20 run, with invented material. Each check is recorded in the traffic observation record.

- **OV-1 Native-layer request.** One request from the host's native layer to a known allowed destination. It must appear as a subject contact with the expected name source.
- **OV-2 Interface (webview) request.** One request from the host's interface that the native layer allows. It must appear attributed to the host, by process or by effective process. If not, BS-8 holds and the limit is recorded.
- **OV-3 Name lookup.** One lookup for the destination of OV-1. It must be captured and its answer must map the contact's address.
- **OV-4 Drop check.** Zero kernel drops over the calibration window at the chosen snap length.
- **OV-5 No relay.** The system proxy and VPN settings are read (for example `scutil --proxy`, `scutil --nc list`) and recorded; none is configured for the run (BS-11).
- **B-0 Baseline window.** Before the host launches, the capture runs for a window with no host process. Recurring system traffic seen in B-0 resolves an annex entry of the same process and destination as "not host-caused (baseline)". Anything not seen in B-0 stays flagged. This resolves flags; it never adds a pass.

**Sequence.** (1) Close other applications that use the network, where the person agrees. (2) The person starts the capture with administrator authentication and starts the cross-check snapshots. (3) OV-5, then the baseline window B-0, with no host process running. (4) Launch the host candidate, inside the capture window. (5) Calibration OV-1…OV-4, which needs the running host. Calibration contacts go to the examiner's own test endpoints and are recorded with their calibration check, in a marked calibration interval; they are **excluded** from the LHQ-20/LHQ-23 comparison of §7 and are never counted as the run's contacts, but only under CB-1 (§7): the examiner declares the calibration endpoints and marks the calibration interval in the record (`calibration_setup`) before the run. (6) Run LHQ-20 with LHQ-23's stimuli (LHQ §5.4). (7) Quit the host and wait until every subject process has exited. (8) Stop the capture and record its drop count. (9) Hash the capture file. (10) Derive the contact list (§6) and run the comparison (§7).

## 6. Handling and the record

- The raw capture stays on the examination machine, outside the repository. It is not committed or relayed. It may contain traffic from the person's other applications.
- The dossier keeps the **traffic observation record** (`lhq.traffic-observation.schema.json`): capture identity and sha256; tool versions; the privilege grant (who granted, when, as stated by the person); interfaces; window; drop count; snap length; calibration results; the subject process set with its lineage sources; one entry per subject contact (destination address, name and name source, process and effective process, first and last time, attribution class); the unattributed-system annex; two counts for *other* (processes and packets); and the limits.
- **Times.** Every time in the record (window, calibration interval, contacts, annex entries, the privilege grant) is written in one ISO-8601 UTC form, `YYYY-MM-DDThh:mm:ss[.fraction]Z`. The schema enforces it with a pattern, and `prototype/top_check.py` also parses times as instants rather than comparing strings.
- Payload bytes are never recorded. The person's other applications are kept only as those two counts, never by name.

## 7. Comparison and native enforcement

**Allowed set at time t.** From the CIR's initial allow list, the A12 records of grants and their scopes (once, this run, always), the model choice (the selected model service, and for a cloud model its sign-in service; LOOP NW-9) and the always-off items (NW-14), applied in time order. Grant scopes follow LOOP NW-11.

**Per subject contact** (capture → record; contacts of the outside-process class are reported under P23-E instead):

- *matched-allowed*: a host record entry (`destination_contacted`) names it, and its allowing entry is in force at t;
- *matched-not-allowed*: recorded, but no allowing entry was in force → P23-A **fail**;
- *unrecorded*: no record entry → P23-D **fail** (and P23-A **fail** if not allowed);
- *unmatched (name not observed)*: cannot be compared → P23-A and P23-D **inconclusive** for that contact.

**Per record entry** (record → capture): a recorded contact with no captured counterpart → P23-D **inconclusive**, or **fail** if the window is complete and the destination is a network destination (not BS-5).

**Declines and refusals:** any subject contact to a declined destination after the decline, or to the disallowed destination of stimulus 23-5, → P23-B **fail**. The agent-visible result "destination not allowed by the person" is checked in the run record (LOOP NW-13).

**Completeness rule (LHQ §5.4; R23-15):** every part whose evidence includes the capture — P23-A, P23-B, P23-C, P23-D, and P23-E as far as its observed traffic is used — passes only if **all calibration checks OV-1…OV-5 held** (LHQ §5.4: "if TOP's calibration did not hold") and the window is complete (BS-3, BS-4). P23-A and P23-D also need every subject contact *matched-allowed*. P23-C also needs **no unresolved flagged annex entry** (BS-1, BS-10), and P23-A needs none whose destination is outside the allowed set. Otherwise each such part is *inconclusive* where no observation failed, and *fail* where one did. A failed observation is positive evidence and fails its part whatever the completeness.

**CB-1 Calibration contacts (RV hardening).** A contact tagged `calibration_check` is calibration, and left out of the comparison above, only when its destination is one of the declared calibration endpoints **and** its first and last times lie within the marked calibration interval. A tagged contact that fails either condition is mis-tagged: it is reported, and it is compared as a run contact, so it cannot escape the comparison. The schema requires `calibration_setup` and keeps calibration contacts in the subject class; `prototype/top_check.py` (sha256 cf128073437772b3f14f2d7f5c42b2043087f19a1f4a9b82ba487a839b135139) applies CB-1 and lists the contacts the comparison must include. Its two violation examples (`lhq.traffic-observation.cb1-violations.examples.json`: a run contact tagged as calibration; a calibration-endpoint contact outside the interval) are schema-valid and both reported mis-tagged; the valid example passes, with four of five contacts compared.

**Native enforcement (P23-F).** It is candidate-specific and joins three pieces of evidence, none sufficient alone:

1. the native layer's refusal for stimulus 23-5 in the host record (recording PROPOSED; R12-10), together with that destination's absence from the capture;
2. a stimulus from the host's interface script that tries to reach a destination directly, refused, and absent from the capture;
3. static inspection of the candidate build's interface network capability and the credential's placement outside the script (GUIDE HC-7.3), labelled `static_inspection`, which supports and never substitutes (EXP evidence provenance).

A browser-only witness, a mock or a schema check is not evidence for P23-F (REQ-006).

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| Whether effective-process marking covers the host's delegated traffic on the candidate's OS | Calibration OV-2 at run time | Before relying on attribution of delegated traffic | BS-8 limit until it holds |
| Snap length | Set at calibration | Before the run | Recorded |
| Boundary-refusal recording (stimulus 23-5) | Next amendment (R23-14 item 2) | Before P23-F's first piece is fixed | Absence in the capture is still required |
| A host with no native layer or destination record (SWBPIPE today, SQ-30) | SWBPIPE owner; host joins deferred | Before LHQ-23 | LHQ-23 cannot start (LHQ §7) |

## Changes at repair (review RV-LHQ-U2; in place, version label unchanged)

| Finding | Repair |
|---|---|
| U2-R1 (MAJOR) attribution gaps never reached outcomes | §7's completeness rule needs all of OV-1…OV-5 (as LHQ §5.4 says). P23-C needs no unresolved flagged annex entry, and P23-A none whose destination is outside the allowed set. BS-1 and BS-8 state these effects. A baseline window B-0 can resolve a flag ("not host-caused (baseline)"); it never adds a pass |
| U2-R5 (MINOR) method beyond the man page | §2.1 marks "every outbound packet carries process metadata" as inference. A new method bullet states how the effective process is read (filtered passes with `-Q "epid = ‹pid›"` and `-Q "eproc = ‹name›"`, tested by OV-2) and how packets without metadata are joined by flow identifier. New BS-10 (packets with no process metadata) and BS-11 (proxy or relay), with OV-5 |
| U2-R6 (MINOR) schema did not enforce completeness | The traffic schema makes calibration an object with one entry per check, so each is present once. Any check other than *held* forces `complete: false` with `calibration_not_held`. A flagged annex entry must carry the limit and its resolution. Three new invalid examples (RV's T1…T3) are added; T1 is rejected with two errors from the same rule |
| U2-R7 (MINOR) privilege declined | *blocked* at the start, with the cause recorded (R23-20 item 2); LHQ LF-10 matches |
| U2-R8 (NOTE) | "The operating system asks for", with R23-14's "host" read as the examination machine |
| U2-R9 (NOTE) | No change |
| U2-R10 (MINOR, from the confirmation) | The sequence now launches the host after B-0 and before OV-1…OV-4. Calibration contacts are recorded in a marked calibration interval and excluded from the §7 comparison |
| U2-R11 (MINOR) | The traffic schema refuses a baseline resolution (`not_host_caused_baseline`) unless B-0 *held*. A new invalid example is added |
| CB-1 (RV hardening, from the confirmation) | Calibration tagging is bound to the declared test endpoints and the marked calibration interval (`calibration_setup`, required). A mis-tagged contact is compared as a run contact. Checked by `prototype/top_check.py` |
| Time form (RV note, from the confirmation) | One ISO-8601 UTC form is stated (§6) and enforced by a schema pattern on every time, with a new invalid example. `top_check.py` parses times as instants instead of comparing strings, and refuses a time without an offset. Rerun: valid example OK (4 of 5 compared); both CB-1 violations reported |
| Tranche-2 closeout pin (R23-21 item 4) | LHQ pin moved from v0.1 (`20361a0b…`) to v0.2, after reading v0.2's diff. Only §3 (CI-5) changed. §5.4 and LHQ-23, which this plan relies on, are unchanged |
