"""Run the DEL-04-0x format prototype (R12-3). Prototype only; not product code.

  python3 run_prototype.py [scratch-dir]

1. Loads the three PROPOSED schemas (ACT policy-class record, AS settings-in,
   RS record entry) and checks them against the declared keyword subset.
2. Validates every valid and invalid example instance beside them.
3. Writes each valid RS example log through the prototype writer into a scratch
   folder and reads it back: the entries and the bytes must be identical.
4. Runs the writer and reader failure cases of RS §14 (write failure, partial
   entry, two recorders, unknown version, correction, sequence gap, semantic
   checks) and reports what each leaves.
5. Converts EXEC's valid recorder outputs into RS entries through the writer
   (R14-1; `exec_to_rs.py`): every entry valid, none without a kind.

Exit status 0 only when every expectation holds.
"""

import copy
import glob
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from minischema import Registry, validate          # noqa: E402
from record_store import Reader, Writer, WriteFailed, NonConformant, RS_ID   # noqa: E402

RS_DIR = os.path.dirname(HERE)
WORKING = os.path.dirname(os.path.dirname(RS_DIR))
ACT_DIR = glob.glob(os.path.join(WORKING, "DEL-04-01_*", "Design"))[0]
AS_DIR = glob.glob(os.path.join(WORKING, "DEL-04-02_*", "Design"))[0]

FAILURES = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        FAILURES.append(label)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def cases(path):
    data = load(path)
    return data if isinstance(data, list) else [{"case": os.path.basename(path), "instance": data}]


def main():
    scratch = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="b4-proto-")
    os.makedirs(scratch, exist_ok=True)
    reg = Registry()
    ids = {}
    for name, d, f in (("ACT", ACT_DIR, "ACT_POLICY_CLASS_RECORD.schema.json"),
                       ("AS", AS_DIR, "AS_SETTINGS_IN.schema.json"),
                       ("RS", RS_DIR, "RS_RECORD.schema.json")):
        ids[name] = reg.load(os.path.join(d, f))
        print(f"loaded {name} schema {ids[name]} (subset check passed)")

    # 2. example instances
    print("\n== example instances ==")
    groups = [
        ("ACT", ACT_DIR, "ACT_POLICY_CLASS_RECORD.valid.example.json", True),
        ("ACT", ACT_DIR, "ACT_POLICY_CLASS_RECORD.invalid.examples.json", False),
        ("AS", AS_DIR, "AS_SETTINGS_IN.valid.examples.json", True),
        ("AS", AS_DIR, "AS_SETTINGS_IN.invalid.examples.json", False),
        ("RS", RS_DIR, "RS_RECORD.invalid.examples.json", False),
    ]
    for name, d, f, expect_valid in groups:
        schema = reg.by_id[ids[name]]
        for c in cases(os.path.join(d, f)):
            errs = validate(c["instance"], schema, reg)
            ok = (not errs) if expect_valid else bool(errs)
            detail = "" if expect_valid else f" -> {errs[0][:110]}"
            check(ok, f"{name} {c['case']} {'valid' if expect_valid else 'invalid'} as expected{detail}")
    rs_logs = sorted(glob.glob(os.path.join(RS_DIR, "RS_RECORD.valid.*.example.jsonl")))
    rs_schema = reg.by_id[ids["RS"]]
    for path in rs_logs:
        with open(path, encoding="utf-8") as fh:
            entries = [json.loads(l) for l in fh if l.strip()]
        bad = [(e["recordId"], validate(e, rs_schema, reg)[:1]) for e in entries if validate(e, rs_schema, reg)]
        check(not bad, f"RS {os.path.basename(path)}: {len(entries)} entries valid {bad if bad else ''}")

    # 3. round trip
    print("\n== write and read back ==")
    reader = Reader(reg)
    for path in rs_logs:
        with open(path, "rb") as fh:
            src_bytes = fh.read()
        src = [json.loads(l) for l in src_bytes.decode("utf-8").splitlines() if l.strip()]
        out = os.path.join(scratch, "rt-" + os.path.basename(path))
        if os.path.exists(out):
            os.remove(out)
        w = Writer(out, reg, src[0]["recorder"], src[0]["context"], src[0].get("runId"))
        for e in src:
            extra = {k: e[k] for k in ("writtenAt", "observedAt", "corrects", "correctionReason") if k in e}
            w.append(e["kind"], e["body"], e["recordId"], extra=extra, recorder=e["recorder"])
        log = reader.read_log(out)
        same_entries = log["entries"] == src
        with open(out, "rb") as fh:
            same_bytes = fh.read() == src_bytes
        check(same_entries and same_bytes and not log["limits"] and not log["nonconformant"],
              f"round trip {os.path.basename(path)}: {len(log['entries'])} entries equal={same_entries} bytes equal={same_bytes}")
        v = reader.view([log])
        print(f"     view: acts={len(v['acts'])} corrected={list(v['correctedBy'].items())} limits={v['limits']} nonconformant={v['nonconformant']}")

    # 4. failure cases
    print("\n== failure cases (RS §14.3) ==")
    host_src = [json.loads(l) for l in open(os.path.join(RS_DIR, "RS_RECORD.valid.host-run.example.jsonl"), encoding="utf-8")]
    app_src = [json.loads(l) for l in open(os.path.join(RS_DIR, "RS_RECORD.valid.app-run.example.jsonl"), encoding="utf-8")]
    rec, ctx, run = host_src[0]["recorder"], host_src[0]["context"], host_src[0]["runId"]

    # FC-1 write failure: entry 0007 fails once, is kept pending, then written late with a limit
    p = os.path.join(scratch, "fc1-write-failure.jsonl")
    if os.path.exists(p):
        os.remove(p)
    state = {"armed": True}

    def fail_once(entry):
        if entry["recordId"].endswith("0007") and state["armed"]:
            state["armed"] = False
            return True
        return False
    w = Writer(p, reg, rec, ctx, run, fail=fail_once)
    reported = None
    for e in host_src[:9]:
        try:
            w.append(e["kind"], e["body"], e["recordId"], recorder=e["recorder"])
        except WriteFailed as exc:
            reported = str(exc)
    log = reader.read_log(p)
    kinds = [x["kind"] for x in log["entries"]]
    ids_written = [x["recordId"][-4:] for x in log["entries"]]
    check(reported is not None and "0007" in reported, f"FC-1 failure reported to the caller: {reported}")
    check(ids_written[:6] == ["0001", "0002", "0003", "0004", "0005", "0006"] and "0007" in ids_written
          and "record write failed" in [x["body"].get("label") for x in log["entries"] if x["kind"] == "evidence_limit"],
          f"FC-1 entry 0007 written late in order with 'record write failed'; order {ids_written}")
    check(not log["limits"], "FC-1 no sequence gap: seq is assigned only on a successful write")

    # FC-2 partial entry: crash mid-line, reopen, append
    p = os.path.join(scratch, "fc2-partial.jsonl")
    with open(p, "wb") as fh:
        for e in host_src[:3]:
            fh.write((json.dumps(e, ensure_ascii=False) + "\n").encode())
        fh.write(json.dumps(host_src[3], ensure_ascii=False).encode()[:57])      # torn write
    before = reader.read_log(p)
    check("partial entry at end (not read)" in before["limits"] and len(before["entries"]) == 3,
          f"FC-2 reader before recovery: 3 entries, limits {before['limits']}")
    w = Writer(p, reg, rec, ctx, run)
    w.append(host_src[4]["kind"], host_src[4]["body"], host_src[4]["recordId"], recorder=host_src[4]["recorder"])
    after = reader.read_log(p)
    labels = [x["body"].get("label") for x in after["entries"] if x["kind"] == "evidence_limit"]
    check(w.recovered_partial and "partial entry not recovered" in labels and len(after["entries"]) == 5
          and any("partial entry at line" in l for l in after["limits"]),
          f"FC-2 after reopen: torn line kept and terminated, limit written, {len(after['entries'])} entries, reader limits {after['limits']}")

    # FC-3 two recorders: host facility direct capture + App faithful record of the same act
    p_host = os.path.join(scratch, "fc3-host.jsonl")
    p_app = os.path.join(scratch, "fc3-app.jsonl")
    for q in (p_host, p_app):
        if os.path.exists(q):
            os.remove(q)
    act = copy.deepcopy(host_src[17])          # A4 on S-4, host facility, cap:T16a
    wh = Writer(p_host, reg, act["recorder"], ctx, run)
    wh.append("human_act", act["body"], act["recordId"])
    faithful = copy.deepcopy(act["body"])
    faithful["recordingMode"] = "faithful recording"
    wa = Writer(p_app, reg, {"role": "agent", "identity": "app-agent-seat:1"}, {"surface": "App"}, run)
    wa.append("human_act", faithful, "rec:app:run-13:0101")
    v = reader.view([reader.read_log(p_host), reader.read_log(p_app)])
    check(len(v["acts"]) == 1 and len(v["acts"][0]["records"]) == 2 and v["acts"][0]["governing"] == act["recordId"]
          and not v["acts"][0]["recordersDisagree"],
          f"FC-3a same act, two records: counted once, direct capture governs: {v['acts']}")
    disagreeing = copy.deepcopy(faithful)
    disagreeing["boundContent"] = [{"method": "m-fx", "value": "S-4@r17"}]
    wa.append("human_act", disagreeing, "rec:app:run-13:0102")
    v = reader.view([reader.read_log(p_host), reader.read_log(p_app)])
    check(any(l.startswith("recorders disagree") for l in v["limits"]),
          f"FC-3b records of one capture disagree on content: limit {[l for l in v['limits'] if l.startswith('recorders')]}")

    # FC-4 unknown version: newer minor read limited; other major refused; other format refused
    p = os.path.join(scratch, "fc4-versions.jsonl")
    newer_minor = dict(host_src[0], formatVersion="0.2", recordId="rec:x:0001")
    newer_minor["body"] = dict(newer_minor["body"], someNewElement="x")
    other_major = dict(host_src[1], formatVersion="1.0", seq=2, recordId="rec:x:0002")
    other_format = dict(host_src[2], format="something.else", seq=3, recordId="rec:x:0003")
    with open(p, "w", encoding="utf-8") as fh:
        for e in (newer_minor, other_major, other_format):
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    log = reader.read_log(p)
    check(len(log["limited"]) == 1 and len(log["refused"]) == 2,
          f"FC-4 limited {[x[2] for x in log['limited']]}; refused {[x[1] for x in log['refused']]}")

    # FC-5 correction: both readable; the corrected one is marked; kind cannot change
    log = reader.read_log(os.path.join(RS_DIR, "RS_RECORD.valid.app-run.example.jsonl"))
    v = reader.view([log])
    check(v["correctedBy"] == {"rec:app:run-12:0009": "rec:app:run-12:0015"}
          and any(e["recordId"] == "rec:app:run-12:0009" for e in log["entries"]),
          f"FC-5a correction: both entries readable, 0009 corrected by 0015")
    p = os.path.join(scratch, "fc5-bad-correction.jsonl")
    if os.path.exists(p):
        os.remove(p)
    w = Writer(p, reg, app_src[0]["recorder"], app_src[0]["context"], app_src[0]["runId"])
    ended = next(e for e in app_src if e["kind"] == "run_ended")
    w.append("run_ended", ended["body"], ended["recordId"])
    w.append("evidence_limit", {"label": "missing receipt"}, "rec:app:run-12:0901",
             extra={"corrects": ended["recordId"], "correctionReason": "wrong kind"})
    v = reader.view([reader.read_log(p)])
    check(any("keep the corrected entry's kind" in m for _, ms in v["nonconformant"] for m in ms),
          "FC-5b a correction that changes the kind is nonconformant")

    # FC-6 sequence gap (an entry lost outside the writer)
    p = os.path.join(scratch, "fc6-gap.jsonl")
    with open(p, "w", encoding="utf-8") as fh:
        for e in host_src[:3] + host_src[5:7]:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    log = reader.read_log(p)
    check("entries missing (sequence gap 4..5)" in log["limits"], f"FC-6 {log['limits']}")

    # FC-7 writer refuses a nonconformant entry; reader semantic checks
    p = os.path.join(scratch, "fc7.jsonl")
    if os.path.exists(p):
        os.remove(p)
    w = Writer(p, reg, rec, ctx, run)
    bad = copy.deepcopy(host_src[17]["body"])
    bad["captureEvidence"] = []
    try:
        w.append("human_act", bad, "rec:x:0701")
        refused = False
    except NonConformant:
        refused = True
    check(refused and not os.path.exists(p), "FC-7a writer never writes an act without capture evidence")
    selfrec = copy.deepcopy(host_src[17])
    selfrec["recorder"] = {"role": "agent", "identity": "Engineer A"}
    proc = copy.deepcopy(host_src[12])
    proc["body"].pop("limitRef")
    with open(p, "w", encoding="utf-8") as fh:
        for i, e in enumerate((selfrec, proc), start=1):
            fh.write(json.dumps(dict(e, seq=i), ensure_ascii=False) + "\n")
    v = reader.view([reader.read_log(p)])
    msgs = [m for _, ms in v["nonconformant"] for m in ms]
    check(any(m.startswith("HA-2") for m in msgs) and any("process network not observed" in m for m in msgs),
          f"FC-7b reader flags {msgs}")

    # FC-7c (RS-v0.9 R-7): an A15 binds the reviewed bytes; schema-valid entries whose bound content differs
    # from the reviewed content, or whose registered entries are out of order, are flagged by the reader
    acts_src = [json.loads(l) for l in open(os.path.join(RS_DIR, "RS_RECORD.valid.act-log.example.jsonl"), encoding="utf-8")]
    one = copy.deepcopy(acts_src[0])
    one["body"]["boundContent"] = [{"method": one["body"]["boundContent"][0]["method"], "value": "wfrev:other"}]
    many = copy.deepcopy(acts_src[3])
    many["body"]["relations"]["registeredEntries"].reverse()
    p = os.path.join(scratch, "fc7c.jsonl")
    with open(p, "w", encoding="utf-8") as fh:
        for i, e in enumerate((one, many), start=1):
            fh.write(json.dumps(dict(e, seq=i), ensure_ascii=False) + "\n")
    log = reader.read_log(p)
    v = reader.view([log])
    msgs = [m for _, ms in v["nonconformant"] for m in ms]
    check(not log["nonconformant"] and len(msgs) == 2 and all("WR ID-2" in m for m in msgs),
          f"FC-7c schema-valid A15 entries not bound to their reviewed content flagged by the reader: {msgs}")

    # 5. EXEC -> RS (R14-1)
    print("\n== EXEC recorder outputs as RS entries (R14-1) ==")
    import exec_to_rs                                         # noqa: E402
    rows, problems = exec_to_rs.kind_coverage(reg)
    check(not problems and len(rows) == 19, f"R14-1 all {len(rows)} CE bodies have an RS kind referencing them: {problems or 'yes'}")
    r = exec_to_rs.convert(scratch, reg, quiet=True)
    check(not r["refused"] and r["valid"] == r["converted"] == r["outputs"] and not r["limits"],
          f"R14-1 EXEC's valid example: {r['valid']} of {r['outputs']} entries valid, refused {len(r['refused'])}")
    total, valid, kinds, more = exec_to_rs.convert_more(scratch, reg)
    check(not more and valid == total, f"R14-1 other CH runs and samples: {valid} of {total} entries valid")

    print(f"\nscratch: {scratch}")
    print("RESULT:", "all expectations held" if not FAILURES else f"{len(FAILURES)} failed")
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
