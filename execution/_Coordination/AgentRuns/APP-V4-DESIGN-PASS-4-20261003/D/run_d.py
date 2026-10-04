#!/usr/bin/env python3
"""EU-D1 check: builds FX-EUD1 and every EU-D1 record into OUTDIR and checks them.

Bounded prototype (owner O-D; R23-34). Not product code. Needs Python 3 and
`jsonschema` (Draft 2020-12, with `referencing`). No network. Reads the
fixture, the Design files and DEL-09-01's EXP schema and checker
(read-only); writes only into OUTDIR.

  python3 -B run_d.py OUTDIR          # check; OUTDIR gets the build
  python3 -B run_d.py OUTDIR --freeze # also write evidence/ and the reader input set here

Checks:
  F  fixture: rebuilt bytes equal fixtures/FX-EUD1 (determinism; sources unchanged)
  S  schemas valid; every record valid; invalid examples refused
  E  expectations per case (standing, reliance, conclusions, route, CS-R1..R5)
  I  independence (CS-R4): each connector's records unchanged with the other's inputs removed
  T  route truth from the real work graph; the question key agrees with it
  X  EXP rehearsal records: EXP schema valid, EXP-R1/R3/R5 rules hold, aggregate as expected
  B  build is deterministic; without --freeze, the on-disk evidence/ equals the fresh build
     (evidence/ was named build/ until EUD1-R9: the root .gitignore excludes **/build/)
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eud1  # noqa: E402
import make_fixture  # noqa: E402

EXP_DIR = os.path.join(eud1.EXEC, "PKG-09_Candidate examination and connected journeys", "1_Working",
                       "DEL-09-01_Candidate examination infrastructure and evidence protocol", "Design")
RESULTS = []


def check(cid, ok, detail=""):
    RESULTS.append((cid, bool(ok), detail))


def jl(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tree_bytes(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            with open(p, "rb") as h:
                out[os.path.relpath(p, root)] = h.read()
    return out


# ---------------------------------------------------------------- schemas
SCHEMAS = {
    "standing": os.path.join(eud1.D0702, "connector.standing.schema.json"),
    "route": os.path.join(eud1.D0702, "connector.route-account.schema.json"),
    "pec": os.path.join(eud1.D0701, "pec.receiving-record.schema.json"),
    "domains": os.path.join(eud1.D0801, "domains.receiving-record.schema.json"),
}


def validators():
    loaded = {k: jl(p) for k, p in SCHEMAS.items()}
    for k, s in loaded.items():
        Draft202012Validator.check_schema(s)
        check(f"S-0 schema {k} is valid 2020-12", True)
    reg = Registry().with_resources([(s["$id"], Resource.from_contents(s)) for s in loaded.values()])
    return {k: Draft202012Validator(s, registry=reg) for k, s in loaded.items()}


def errs(v, rec):
    return [e.message for e in v.iter_errors(rec)]


# ---------------------------------------------------------------- expectations
EXPECT = {
    "P1": ("adopted", "current", {"c1", "c2", "c3", "c4", "c5", "c6", "c7"}, ["connector_reliance", "source_route", "connector_reliance"]),
    "P2": ("not_adopted", "current", set(), ["source_route"] * 3),
    "P3": ("adopted", "stale", set(), ["source_route"] * 3),
    "P4": ("adopted", "partial", set(), ["source_route"] * 3),
    "P5": ("adopted", "failing", set(), ["source_route"] * 3),
    "P6": ("unknown", "absent", set(), ["source_route"] * 3),
    # R23-40 (EUD1-R1): Q1 asked at S; adopted, current; c1 relied as a report of the record at its pin
    "P7": ("adopted", "current", {"c1"}, ["connector_reliance", "source_route"]),
    # OD-F1 (PR-7): c3's citation does not resolve, so c3 is unknown and (c) goes to the route
    "P8": ("adopted", "current", {"c1", "c2", "c4", "c5", "c6", "c7"}, ["connector_reliance", "source_route", "source_route"]),
}
ROUTE = {k: "ra:EUD1-Q1" for k in EXPECT}
ROUTE["P7"] = "ra:EUD1-Q1S"
NAMED = {  # an unsupported conclusion that must be named (CS-R3), matched on a phrase of its text
    "P1": ["presence fact"], "P2": ["not adopted"], "P3": ["pin precedes"], "P4": ["unparsed rows"],
    "P5": ["fallback signal is set"], "P6": ["no response"],
    "P7": ["reports what the work graph records at its pin", "CS-R2"], "P8": ["PR-7"],
}


def cs_r1(st):
    """CS-R1 per connector (EUD1-R2): PEC relies on 'record', Domains on 'admitted'."""
    tier = {"pec": "record", "domains": "admitted"}[st["connector"]]
    return st["envelope"] == "adopted" and st["condition"] == "current" and st.get("claim_tier") == tier


def all_standings(rec):
    yield rec["response_standing"]
    for c in rec.get("claims", []):
        yield c["standing"]
    for r in rec.get("results", []):
        yield r["standing"]


def check_pec(name, rec, case_ok):
    env, cond, relied, bases = EXPECT[name]
    rs = rec["response_standing"]
    ok = [rs["envelope"] == env, rs["condition"] == cond,
          {c["claim_id"] for c in rec["claims"] if c["standing"]["supports_reliance"]} == relied,
          [s["basis"] for s in rec["conclusions"]["supported"]] == bases,
          sorted(rec["conclusions"]["prohibited"]) == sorted(eud1.PROHIBITED),
          rec["route"] == {"needed": True, "account_ref": ROUTE[name]},
          name == "P7" or any(u["conclusion"].startswith("No work remains") for u in rec["conclusions"]["unsupported"]),
          all(any(p in u["why"] for u in rec["conclusions"]["unsupported"]) for p in NAMED[name]),
          rec["simulated"] is True and rec["input"]["fixture_standing"] == "constructed"]
    labels = ["envelope", "condition", "relied claims", "part bases", "CS-R2 listed", "route", "no-work named (n/a for P7: nodes are READY)", "CS-R3 named", "simulated"]
    ok.append(any(u["conclusion"].startswith("Any item is ready to start, complete or permitted") for u in rec["conclusions"]["unsupported"]))
    labels.append("CS-R2 (i)/(ii) named: no readiness, completion or permission from connector material")
    for l, o in zip(labels, ok):
        check(f"E-{name} {l}", o)
    # CS-R1 both directions on every standing
    r1 = all(st["supports_reliance"] == cs_r1(st) for st in all_standings(rec) if st is not rec["response_standing"])
    check(f"E-{name} CS-R1 both directions on claims", r1)
    # presence never relied on and shown with age
    pres = [c for c in rec["claims"] if c["standing"]["claim_tier"] == "presence_advisory"]
    check(f"E-{name} presence advisory, never relied, age shown", all(not c["standing"]["supports_reliance"] and "heartbeat_age_s" in c for c in pres))
    # stamp and envelope kept apart, absence has neither
    if name == "P6":
        check("E-P6 no stamp, envelope or claims", rec["stamp"] is None and rec["envelope_elements"] is None and rec["claims"] == [])
    else:
        check(f"E-{name} stamp and envelope apart", set(rec["stamp"]) == {"examined_through", "generated_at", "feed_freshness"} and "pin" in rec["envelope_elements"])
    case_ok[name] = all(ok) and r1


def check_domains(recs, case_ok):
    d1, d2 = recs["DM-1"], recs["DM-2"]
    r = {x["result_id"]: x for x in d1["results"]}
    ok1 = [d1["response_standing"]["envelope"] == "adopted", d1["response_standing"]["condition"] == "stale",
           r["r1"]["standing"]["claim_tier"] == "admitted" and r["r1"]["standing"]["condition"] == "stale" and not r["r1"]["standing"]["supports_reliance"],
           r["r2"]["standing"]["claim_tier"] == "located_not_admitted" and not r["r2"]["standing"]["supports_reliance"],
           r["r1"]["current_revision"] == "rev-B" and r["r1"]["indexed_revision"] == "rev-A",
           any("3.0 m" in u["conclusion"] for u in d1["conclusions"]["unsupported"]),
           d1["conclusions"]["supported"] and all(s["basis"] == "source_route" for s in d1["conclusions"]["supported"]),
           d1["route"]["account_ref"] == "ra:EUD1-QD"]
    for i, o in enumerate(ok1):
        check(f"E-DM-1 item {i + 1}", o)
    ok2 = [d2["response_standing"]["condition"] == "absent", d2["response_standing"]["envelope"] == "unknown",
           d2["results"] == [], d2["route"]["needed"] is True]
    for i, o in enumerate(ok2):
        check(f"E-DM-2 item {i + 1}", o)
    case_ok["DM-1"], case_ok["DM-2"] = all(ok1), all(ok2)


def check_routes(ra1, raq, truth, key):
    check("T-1 route Q1: no READY/ACTIVE/BLOCKED node at R", truth["rab"] == [])
    check("T-2 route Q1: other open nodes = T2", truth["other_open"] == ["T2"])
    exp = [("VC", "ACTIVE", "COMPLETE (R23-22)"), ("E", "ACTIVE", "COMPLETE (RR-E, RR-F)"), ("O-B1", "READY", "COMPLETE"),
           ("O-C1", "READY", "COMPLETE"), ("D", "PLANNED", "COMPLETE (PR)"), ("T2", None, "PLANNED")]
    check("T-3 route Q1: six changes, as the two committed files show", [(c["node"], c["from"], c["to"]) for c in truth["changes"]] == exp)
    check("T-4 route Q1: no node removed", truth["removed"] == [])
    kt = key["q1_truth"]
    keyc = [(f"{n} added as {t}" if f is None else f"{n} {f} -> {t}") for n, f, t in exp]
    check("T-5 key agrees with the route truth", kt["a_rab_nodes_at_R"] == [] and kt["b_other_open_nodes_at_R"] == ["T2 PLANNED"] and kt["c_changes_since_S"] == keyc)
    for ra in (ra1, raq):
        perf = [d for d in ra["duties"] if d["standing"] == "performed"]
        check(f"T-6 {ra['account_id']}: performed duties cite evidence; review not claimed", all(d.get("evidence") for d in perf)
              and any(d["duty"] == "review_integrate" and d["standing"] == "outstanding" for d in ra["duties"]))
    srcs = jl(os.path.join(HERE, "fixtures", "FX-EUD1", "sources", "SOURCES.json"))["sources"]
    check("T-7 route sources are the committed bytes", all(s["sha256"] == sha(make_fixture.git_show(s["revision"], s["path"])) for s in srcs))
    for k in ("P1", "P2", "P3", "P4", "P5", "P6", "DM-1", "DM-2"):
        check(f"T-8 key has case {k}", k in key["cases"])


def negatives(v):
    """Invalid examples the schemas must refuse."""
    rec = jl(os.path.join(OUT, "records", "PR-P3.json"))
    bad = []
    a = copy.deepcopy(rec); a["claims"][0]["standing"]["supports_reliance"] = True
    bad.append(("pec", a, "stale claim marked as supporting reliance (CS-R1)"))
    b = copy.deepcopy(jl(os.path.join(OUT, "records", "PR-P6.json"))); b["response_standing"]["envelope"] = "adopted"
    bad.append(("pec", b, "absent response with an adopted envelope"))
    c = copy.deepcopy(jl(os.path.join(OUT, "records", "PR-P6.json"))); c["claims"] = [copy.deepcopy(rec["claims"][0])]
    bad.append(("pec", c, "no-response record carrying a claim"))
    d = copy.deepcopy(rec); d["conclusions"]["prohibited"] = ["no_work"]
    bad.append(("pec", d, "prohibited list incomplete (CS-R2)"))
    e = copy.deepcopy(jl(os.path.join(OUT, "records", "RA-Q1.json"))); e["duties"][1]["standing"] = "performed"
    bad.append(("route", e, "review claimed performed without actor or evidence"))
    f = copy.deepcopy(rec); del f["simulated_terms"]
    bad.append(("pec", f, "simulated record without its simulated terms"))
    g = copy.deepcopy(jl(os.path.join(OUT, "records", "DR-DM-1.json"))); g["results"][1]["standing"]["supports_reliance"] = True
    bad.append(("domains", g, "unadmitted hit marked as supporting reliance (CS-R1)"))
    h = copy.deepcopy(jl(os.path.join(OUT, "records", "RA-Q1.json"))); h["duties"][0]["actor_role"] = "person"
    bad.append(("route", h, "locate_compare assigned to the person"))
    # EUD1-R2: cross-connector tiers and standings must not validate
    p1 = jl(os.path.join(OUT, "records", "PR-P1.json"))
    i = copy.deepcopy(p1); i["claims"][0]["standing"]["claim_tier"] = "admitted"
    bad.append(("pec", i, "PEC claim tiered 'admitted' with reliance (EUD1-R2 Q-a)"))
    d1 = jl(os.path.join(OUT, "records", "DR-DM-1.json"))
    j = copy.deepcopy(d1); r1 = j["results"][0]["standing"]
    r1.update(condition="current", claim_tier="record", supports_reliance=True)
    bad.append(("domains", j, "Domains result tiered 'record' with reliance (EUD1-R2 Q-b)"))
    k = copy.deepcopy(p1); k["claims"][0]["standing"]["connector"] = "domains"
    bad.append(("pec", k, "PEC record carrying a Domains-connector standing (EUD1-R2 Q-c)"))
    m = copy.deepcopy(p1); m["claims"][7]["standing"]["claim_tier"] = "located_not_admitted"
    bad.append(("pec", m, "PEC claim with a Domains tier"))
    for kind, r, why in bad:
        check(f"S-neg refused: {why}", errs(v[kind], r))
    # the sound P1 record still validates (control)
    check("S-neg control: unaltered PR-P1 valid", not errs(v["pec"], p1))


def independence(fx):
    """CS-R4: derive each connector's records with the other connector's inputs removed."""
    base_files, base, _ = eud1.build(fx, os.path.join(TMP, "ind-base"))
    for drop, keep in (("domains", ("P1", "P2", "P3", "P4", "P5", "P6", "P8")), ("pec", ("DM-1", "DM-2"))):
        fx2 = os.path.join(TMP, f"fx-no-{drop}")
        shutil.rmtree(fx2, ignore_errors=True)
        shutil.copytree(fx, fx2)
        shutil.rmtree(os.path.join(fx2, drop))
        recs = {}
        ra1, truth = eud1.route_q1(fx2)
        for k in keep:
            recs[k] = eud1.pec_record(fx2, k, truth) if k.startswith("P") else eud1.domains_record(fx2, k)
        same = all(recs[k] == base[k] for k in keep)
        check(f"I-1 {', '.join(keep[:2])}… unchanged with {drop} inputs removed", same)
    return True


def exp_check(exp_recs):
    spec = importlib.util.spec_from_file_location("check_exp", os.path.join(EXP_DIR, "prototype", "check_exp.py"))
    ce = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ce)
    v = Draft202012Validator(jl(os.path.join(EXP_DIR, "exam.result-record.schema.json")))
    expected = {"CW-EUD1-LC": "pass", "CW-EUD1-OC": "pass", "CW-EUD1-QC": "inconclusive"}
    for r in exp_recs:
        r["outcome"] = ce.aggregate(r["parts"])
        e = errs(v, r)
        check(f"X-1 {r['record_id']} valid against EXP schema", not e, "; ".join(e[:2]))
        check(f"X-2 {r['record_id']} EXP rules hold", not ce.rule_violations(r), str(ce.rule_violations(r)))
        check(f"X-3 {r['record_id']} outcome {r['outcome']} as expected", r["outcome"] == expected[r["record_id"]])
    return exp_recs


READER_FILES = ["records/RA-Q1.json", "records/RA-QD.json"] + [f"records/PR-P{i}.json" for i in range(1, 7)] + ["records/DR-DM-1.json", "records/DR-DM-2.json",
                "RUN_LOG.json"]  # OD-F2: the cited duty evidence


def build_all(fx, out):
    files, recs, truth = eud1.build(fx, out)
    cr = {}
    for k in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"):
        check_pec(k, recs[k], cr)
    check_domains(recs, cr)
    cr["OC-1"] = cr["P6"] and cr["DM-1"]
    cr["IA-2"] = cr["P1"] and cr["DM-2"]
    exp_recs = eud1.exp_records(fx, files, cr)
    for r in exp_recs:
        r["outcome"] = None
    return files, recs, truth, exp_recs, cr


def write_exp(out, exp_recs):
    for r in exp_recs:
        p = os.path.join(out, "records", "exp", r["record_id"] + ".json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(eud1.dump(r))


def reader_set(out):
    rs = os.path.join(out, "reader_input")
    shutil.rmtree(rs, ignore_errors=True)
    os.makedirs(rs)
    items = {}
    for rel in READER_FILES:
        items[rel] = open(os.path.join(out, rel), "rb").read()
    fx = os.path.join(HERE, "fixtures", "FX-EUD1")
    for rel in ("pec/ADOPTION_ACCOUNT.json",  # OD-F2: the cited authority for the 'adopted' envelope
                "sources/WORK_GRAPH@e4a0c2c4c3.md", "sources/WORK_GRAPH@e086dfff32.md", "domains/sources/SRC-1.md",
                "domains/sources/SRC-1@rev-A.md", "domains/sources/SRC-2.md", "domains/ADMISSION.json"):
        items["sources/" + rel.split("/")[-1] if rel.startswith("sources/") else rel] = open(os.path.join(fx, rel), "rb").read()
    items["CONNECTOR_FALLBACK.md"] = open(os.path.join(eud1.D0702, "CONNECTOR_FALLBACK.md"), "rb").read()
    items["READER_TASK.md"] = open(os.path.join(HERE, "reader", "READER_TASK.md"), "rb").read()
    for rel, b in items.items():
        p = os.path.join(rs, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(b)
    man = "".join(f"{sha(items[k])}  {k}\n" for k in sorted(items))
    with open(os.path.join(rs, "MANIFEST.sha256"), "w") as f:
        f.write(man)
    check("R-1 reader input set excludes the key and the raw constructed responses",
          not any("KEY" in k.upper() or re.match(r"pec/P[0-9]+\.json$", k) or k in ("domains/DM-1.json", "domains/DM-2.json") for k in items))
    cited = set()
    for rel in READER_FILES:
        if rel.startswith("records/PR-"):
            cited.add(json.loads(items[rel])["adoption"]["account_ref"].split(" ")[0])
        if rel.startswith("records/RA-"):
            cited |= {d["evidence"] for d in json.loads(items[rel])["duties"] if d.get("evidence")}
    check("R-2 every authority record the supplied records cite is supplied (OD-F2)", cited <= set(items), str(sorted(cited - set(items))))
    return items


def main():
    global OUT, TMP
    OUT = sys.argv[1]
    freeze = "--freeze" in sys.argv
    TMP = os.path.join(OUT, "_tmp")
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(TMP)
    fx_committed = os.path.join(HERE, "fixtures", "FX-EUD1")
    fx_fresh = os.path.join(TMP, "FX-EUD1")
    make_fixture.build(fx_fresh)
    check("F-1 fixture rebuilt byte-equal to fixtures/FX-EUD1", tree_bytes(fx_fresh) == tree_bytes(fx_committed))
    v = validators()
    files, recs, truth, exp_recs, cr = build_all(fx_committed, OUT)
    for rel in files:
        if rel.startswith("records/"):
            kind = "route" if "RA-" in rel else "pec" if "PR-" in rel else "domains"
            e = errs(v[kind], json.loads(files[rel]))
            check(f"S-1 {rel} valid", not e, "; ".join(e[:2]))
    negatives(v)
    check_routes(json.loads(files["records/RA-Q1.json"]), json.loads(files["records/RA-QD.json"]), truth["Q1"], jl(os.path.join(HERE, "key", "EUD1_KEY.json")))
    ts = truth["Q1-S"]
    check("T-9 route Q1-S: READY/ACTIVE/BLOCKED at S are VC, E, O-B1, O-C1", ts["rab"] == ["VC", "E", "O-B1", "O-C1"])
    check("T-10 route Q1-S: other open node at S is D", ts["other_open"] == ["D"])
    ras = json.loads(files["records/RA-Q1S.json"])
    check("T-11 route Q1-S: readiness to start named unsupported", any("may be started" in u["conclusion"] for u in ras["conclusions"]["unsupported"]))
    independence(fx_committed)
    exp_recs = exp_check(exp_recs)
    write_exp(OUT, exp_recs)
    # determinism of the build
    f2, _, _, e2, _ = build_all(fx_committed, os.path.join(TMP, "again"))
    check("B-1 build deterministic", f2 == files)
    items = reader_set(OUT)
    if freeze:
        dest = os.path.join(HERE, "evidence")
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(OUT, dest, ignore=shutil.ignore_patterns("_tmp"))
    elif os.path.isdir(os.path.join(HERE, "evidence")):
        a = tree_bytes(os.path.join(HERE, "evidence"))
        b = {k: x for k, x in tree_bytes(OUT).items() if not k.startswith("_tmp")}
        check("B-2 on-disk evidence/ equals the fresh build", a == b, str(sorted(set(a) ^ set(b)))[:200])
    shutil.rmtree(TMP, ignore_errors=True)
    failed = [r for r in RESULTS if not r[1]]
    for cid, ok, d in RESULTS:
        print(("PASS " if ok else "FAIL ") + cid + (f"  [{d}]" if d and not ok else ""))
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} checks held")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
