"""Prototype writer and reader for the PROPOSED record format (RS-v0.9 §13, §14).

Prototype only (R12-3): it shows the format and the failure behaviour of the
writer and reader sequences. It is not product code, selects no placement
(OI-014) and no path, and uses the Python 3 standard library only.

Storage unit (PROPOSED, RS §13.1): one append-only log per run and writer, one
JSON object per line, UTF-8, each line ended by "\n"; acts captured outside any
run go to the writer's act log.
"""

import json
import os

from minischema import validate

FORMAT = "chirality.rs.record"
KNOWN_VERSION = (0, 1)
RS_ID = "urn:chirality:app-v4:del-04-03:rs-record:0.1"
ENTRY_REF = {"$ref": RS_ID + "#/$defs/entry"}


class WriteFailed(Exception):
    pass


class NonConformant(Exception):
    pass


def _version(text):
    major, minor = text.split(".")
    return int(major), int(minor)


class Writer:
    """W-0 open, W-1 append, W-2 flush after failure, W-3 correct (RS §14.1)."""

    def __init__(self, path, registry, recorder, context, run_id=None, clock=None, fail=None):
        self.path, self.registry = path, registry
        self.recorder, self.context, self.run_id = recorder, context, run_id
        self.clock = clock or (lambda n: f"w{n:03d}")
        self.fail = fail or (lambda entry: False)   # failure injection for the prototype
        self.pending = []                           # entries not yet written, in order
        self.failed_ids = []
        self.next_seq = 1
        self.recovered_partial = False
        self._open()

    # W-0: open, find the next sequence number, terminate a partial last line
    def _open(self):
        if not os.path.exists(self.path):
            return
        with open(self.path, "rb") as fh:
            data = fh.read()
        last_seq = 0
        for line in data.split(b"\n"):
            try:
                last_seq = max(last_seq, json.loads(line).get("seq", 0))
            except (ValueError, AttributeError):
                pass
        self.next_seq = last_seq + 1
        if data and not data.endswith(b"\n"):
            with open(self.path, "ab") as fh:        # never truncate or edit: terminate it
                fh.write(b"\n")
                fh.flush()
                os.fsync(fh.fileno())
            self.recovered_partial = True
            self.append("evidence_limit", {"label": "partial entry not recovered",
                                           "detail": f"an unterminated entry after seq {last_seq} is kept unread"},
                        record_id=f"rec:{self.recorder['identity'].replace('/', '-')}:recovery:{last_seq + 1}")

    def _complete(self, kind, body, record_id, extra):
        entry = {"format": FORMAT, "formatVersion": "%d.%d" % KNOWN_VERSION, "recordId": record_id,
                 "kind": kind, "recorder": self.recorder, "context": self.context}
        if self.run_id:
            entry["runId"] = self.run_id
        entry.update(extra or {})
        entry["body"] = body
        return entry

    # W-1: validate, then append one line with one write and fsync
    def append(self, kind, body, record_id, extra=None, recorder=None):
        entry = self._complete(kind, body, record_id, extra)
        if recorder:
            entry["recorder"] = recorder
        self.pending.append(entry)
        return self.flush()

    def flush(self):
        written = []
        while self.pending:
            entry = dict(self.pending[0])
            entry["seq"] = self.next_seq
            entry.setdefault("writtenAt", self.clock(self.next_seq))
            ordered = {k: entry[k] for k in ("format", "formatVersion", "recordId", "kind", "recorder", "context",
                                             "runId", "seq", "writtenAt", "observedAt", "corrects",
                                             "correctionReason", "body") if k in entry}
            errors = validate(ordered, ENTRY_REF, self.registry)
            if errors:
                self.pending.pop(0)
                raise NonConformant(f"{entry['recordId']}: not written: {errors[:2]}")
            line = (json.dumps(ordered, ensure_ascii=False) + "\n").encode("utf-8")
            try:
                if self.fail(ordered):
                    raise OSError("injected write failure")
                with open(self.path, "ab") as fh:
                    fh.write(line)
                    fh.flush()
                    os.fsync(fh.fileno())
            except OSError as exc:
                if ordered["recordId"] not in self.failed_ids:
                    self.failed_ids.append(ordered["recordId"])
                raise WriteFailed(f"{ordered['recordId']}: {exc}") from exc
            self.pending.pop(0)
            self.next_seq += 1
            written.append(ordered)
        # W-2: after a failure is overcome, say so in the record itself
        if self.failed_ids and written:
            late = ", ".join(self.failed_ids)
            self.failed_ids = []
            self.append("evidence_limit", {"label": "record write failed",
                                           "detail": f"written late after a failed write: {late}"},
                        record_id=f"rec:{self.recorder['identity'].replace('/', '-')}:late:{self.next_seq}")
        return written

    # W-3: a correction is a new entry of the same kind naming the corrected one
    def correct(self, corrected, body, record_id, reason):
        return self.append(corrected["kind"], body, record_id,
                           extra={"corrects": corrected["recordId"], "correctionReason": reason})


class Reader:
    """R-1…R-8 (RS §14.2). Produces a run view and the reader-found limits."""

    def __init__(self, registry):
        self.registry = registry

    def read_log(self, path):
        with open(path, "rb") as fh:
            data = fh.read()
        out = {"path": os.path.basename(path), "entries": [], "limited": [], "refused": [],
               "nonconformant": [], "limits": []}
        lines = data.split(b"\n")
        trailing_partial = bool(data) and not data.endswith(b"\n")
        if lines and lines[-1] == b"":
            lines = lines[:-1]
        for n, raw in enumerate(lines, start=1):
            if not raw.strip():
                continue
            try:
                entry = json.loads(raw)
            except ValueError:
                last = n == len(lines)
                label = "partial entry at end (not read)" if (last and trailing_partial) else f"unreadable line {n}"
                if not last and raw and not raw.endswith(b"}"):
                    label = f"partial entry at line {n} (not read)"
                out["limits"].append(label)
                continue
            # R-2 format name, R-3 version
            if entry.get("format") != FORMAT:
                out["refused"].append((n, "not a record entry of this format"))
                continue
            try:
                major, minor = _version(entry.get("formatVersion", "x.x"))
            except ValueError:
                out["refused"].append((n, "unreadable version"))
                continue
            if major != KNOWN_VERSION[0]:
                out["refused"].append((n, f"unreadable version {major}.{minor}"))
                continue
            if minor > KNOWN_VERSION[1]:
                out["limited"].append((n, entry.get("recordId"), f"read limited: format {major}.{minor} is newer than {KNOWN_VERSION[0]}.{KNOWN_VERSION[1]}"))
                entry["_limited"] = True
                out["entries"].append(entry)
                continue
            # R-4 schema
            errors = validate(entry, ENTRY_REF, self.registry)
            if errors:
                out["nonconformant"].append((entry.get("recordId"), errors[:2]))
                continue
            out["entries"].append(entry)
        # R-5 sequence
        seqs = [e["seq"] for e in out["entries"] if "seq" in e]
        if len(seqs) != len(set(seqs)):
            out["limits"].append("duplicate sequence numbers")
        for a, b in zip(seqs, seqs[1:]):
            if b != a + 1:
                out["limits"].append(f"entries missing (sequence gap {a + 1}..{b - 1})")
        return out

    def view(self, logs):
        entries = [e for log in logs for e in log["entries"]]
        by_id = {e["recordId"]: e for e in entries}
        limits = [l for log in logs for l in log["limits"]]
        nonconf = [x for log in logs for x in log["nonconformant"]]
        # R-6 corrections
        corrected_by = {}
        for e in entries:
            if "corrects" in e:
                corrected_by[e["corrects"]] = e["recordId"]
                if e["corrects"] in by_id and by_id[e["corrects"]]["kind"] != e["kind"]:
                    nonconf.append((e["recordId"], ["a correction must keep the corrected entry's kind"]))
        # R-7 semantic checks the JSON Schema subset cannot express
        for e in entries:
            b = e.get("body", {})
            if e["kind"] in ("human_act",) and not e.get("_limited"):
                actor = b["decisionActor"]
                names = {actor.get(k) for k in ("displayName", "osAccount", "codexAccount", "hostActor")} - {None}
                if e["recorder"]["identity"] in names:
                    nonconf.append((e["recordId"], ["HA-2: recorder named as decision actor"]))
                if b.get("actKind") == "A15":
                    # RS-v0.9 R-7: the A15 binds the reviewed bytes (WR ID-2; C-01; L-4)
                    rel = b.get("relations", {})
                    entries_ = rel.get("registeredEntries") or [
                        {"subject": (b["boundSubject"] or [None])[0], "reviewedDraft": rel.get("reviewedDraft")}]
                    subjects, contents = b["boundSubject"], b["boundContent"]
                    if len(entries_) != len(subjects) or len(entries_) != len(contents):
                        nonconf.append((e["recordId"], ["A15: registered entries, bound subjects and bound contents do not correspond one-to-one"]))
                    else:
                        for i, x in enumerate(entries_):
                            if x["subject"] != subjects[i] or (x.get("reviewedDraft") or {}).get("content") != contents[i]:
                                nonconf.append((e["recordId"], [f"A15: entry {i + 1} is not bound to its reviewed content (WR ID-2)"]))
                                break
            if e["kind"] == "outside_process" and not b.get("sandboxed"):
                ok = any(x["kind"] == "evidence_limit" and x["body"]["label"] == "process network not observed"
                         and x["body"].get("subjectRef") == b["processId"] for x in entries)
                if not ok:
                    nonconf.append((e["recordId"], ["unsandboxed outside process without 'process network not observed'"]))
            if e["kind"] == "destination_contacted" and b["allowedBy"]["kind"] == "in-work grant":
                if b["allowedBy"].get("grantRef") not in by_id:
                    nonconf.append((e["recordId"], ["contact names an in-work grant that is not in the record"]))
        # R-8 two recorders: group act records by capture evidence
        groups = {}
        for e in entries:
            if e["kind"] == "human_act" and e["recordId"] not in corrected_by:
                key = tuple(sorted(c["ref"] for c in e["body"]["captureEvidence"]))
                groups.setdefault(key, []).append(e)
        acts = []
        for key, recs in groups.items():
            direct = [r for r in recs if r["body"]["recordingMode"] == "direct capture"]
            governing = direct[0] if direct else recs[0]
            sig = lambda r: (r["body"]["actKind"], tuple(r["body"]["boundSubject"]),
                             json.dumps(r["body"]["boundContent"], sort_keys=True))
            disagree = len({sig(r) for r in recs}) > 1
            if disagree:
                limits.append(f"recorders disagree: {', '.join(r['recordId'] for r in recs)}")
            acts.append({"captureEvidence": list(key), "records": [r["recordId"] for r in recs],
                         "governing": governing["recordId"], "recordersDisagree": disagree})
        return {"entries": len(entries), "acts": acts, "correctedBy": corrected_by,
                "limits": limits, "nonconformant": nonconf,
                "limited": [x for log in logs for x in log["limited"]],
                "refused": [x for log in logs for x in log["refused"]]}
