#!/usr/bin/env python3
"""EU-D1 reader comparison: score a reader's ACCOUNT.json against the frozen key.

Owner O-D. Written against the first real account (RR-EUD1, sha256 3b31e598…),
not against accounts the author constructed (tranche 1's lesson). Python 3
standard library; reads two files, writes nothing unless --out is given.

Every key item gets one of: met, not met, referred. "referred" means the key's
wording needs a judgment the checker does not make; the reason states the
reading the checker would apply, for HELP_HUMAN or the reviewer to rule.

Readings applied (stated so that a reviewer can challenge them):
- K1 standing: exact envelope and condition values.
- K2 relied claims: the claim ids the reader relies on, by their last
  segment ('pr:EUD1-P1#c1' -> 'c1'); 'none' or [] means the empty set.
- K3 answer: (a), (b), (c) compared with the key's q1_truth after
  normalisation (case, spaces, ':' after a node id, text after the state in
  (b)).
- K4 basis: key 'files' accepts only 'files' (any use of the connector there
  would be reliance CS-R1 excludes). Key 'files … required; the connector may
  be cited in addition' accepts 'files' or 'both'. Key 'connector' accepts
  'connector'; 'both' is REFERRED, because the key does not say whether
  adding the files beside a relied-on claim meets 'connector'.
- K5 must-name: each required unsupported conclusion is found by a set of
  term groups, every group needing one match, in the reader's
  cannot_conclude list.
- K6 forbid: not met if the reader's answer contradicts the truth in a way
  the forbidden item names, or if a forbidden phrase appears outside
  cannot_conclude in an affirmative sentence (notes are scanned; a hit there
  is REFERRED, since negation is not parsed). Otherwise met.
- K7/K8 (Domains): exact boolean; the source statement must name 2.4 m and
  rev-B, and some text must say rev-B's admission is not established.
- K9 independence: met if the answer starts 'No' and says the standing
  'does not change'; not met if it starts 'Yes'; otherwise referred.

Usage: compare_eud1.py ACCOUNT.json KEY.json [--out RESULT.json]
"""
import json
import re
import sys

PEC = ["P1", "P2", "P3", "P4", "P5", "P6"]


def norm(s):
    s = s.lower().replace("->", " -> ").replace(":", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def node_state(s):
    """'T2 (Tranche 2: …): PLANNED' -> 't2 planned'."""
    m = re.match(r"\s*([A-Za-z0-9-]+)\b.*?\b(READY|ACTIVE|BLOCKED|PLANNED|COMPLETE)\b", s)
    return f"{m.group(1).lower()} {m.group(2).lower()}" if m else norm(s)


def change(s):
    s = norm(s)
    s = s.replace(" added as ", " added as ")
    return s


MUST = {  # case -> list of required items, each a list of term groups (any term in a group)
    "P1": [[["c9", "presence"], ["correct", "working", "correctness"]]],
    "P2": [[["not adopted", "unqualified", "not_adopted"], ["reliance", "rely", "pec's word", "claim"]]],
    "P3": [[["vc", "o-b1", "o-c1"], ["active", "ready"], ["changed", "stale", "pin", "earlier", "e4a0c2c4c3"]]],
    "P4": [[["complete"], ["unparsed", "parsed"]]],
    "P5": [[["fallback"], ["set"]]],
    "P6": [[["no response", "absent", "silence", "nothing"], ["pec"]]],
    "DM-1": [[["3.0 m", "3.0m"], ["admitted"], ["currently", "now", "stale", "rev-b"]]],
    "DM-2": [[["domains"], ["no response", "nothing", "no results"]]],
}

FORBID_PHRASES = ["no work remains", "is ready to start", "may start", "is permitted", "is idle",
                  "spacing is 3.0 m", "2.4 m is admitted"]


def has_groups(texts, groups):
    for t in texts:
        tl = t.lower()
        if all(any(term in tl for term in g) for g in groups):
            return True
    return False


def score(acc, key):
    out = []

    def item(case, kid, verdict, why):
        out.append({"case": case, "item": kid, "verdict": verdict, "why": why})

    truth = key["q1_truth"]
    t_a = [node_state(x) for x in truth["a_rab_nodes_at_R"]]
    t_b = [node_state(x) for x in truth["b_other_open_nodes_at_R"]]
    t_c = sorted(change(x) for x in truth["c_changes_since_S"])
    cases = acc["cases"]
    for c in PEC + ["DM-1", "DM-2"]:
        k, r = key["cases"][c], cases.get(c)
        if r is None:
            for kid in k:
                item(c, kid, "not met", "case missing from the account")
            continue
        # K1
        ok = r.get("standing") == k["K1_standing"]
        item(c, "K1", "met" if ok else "not met", f"reader {r.get('standing')} vs key {k['K1_standing']}")
        cc = r.get("cannot_conclude", [])
        if c in PEC:
            rel = {x.split("#")[-1] for x in r.get("pec_claims_relied_on", []) if x.lower() != "none"}
            item(c, "K2", "met" if rel == set(k["K2_pec_claims_relied_on"]) else "not met", f"reader {sorted(rel)} vs key {k['K2_pec_claims_relied_on']}")
            ans = r.get("answer", {})
            a_ok = [node_state(x) for x in ans.get("a", [])] == t_a
            b_ok = [node_state(x) for x in ans.get("b", [])] == t_b
            c_ok = sorted(change(x.replace(":", "", 1)) for x in ans.get("c", [])) == sorted(change(x) for x in truth["c_changes_since_S"])
            item(c, "K3", "met" if a_ok and b_ok and c_ok else "not met", f"(a) {a_ok}, (b) {b_ok}, (c) {c_ok}")
            kb, rb = k["K4_basis"], r.get("basis", {})
            verdicts = []
            for part in ("a", "b", "c"):
                want, got = kb[part], rb.get(part)
                if want == "files":
                    v = "met" if got == "files" else "not met"
                elif want.startswith("files"):
                    v = "met" if got in ("files", "both") else "not met"
                elif want == "connector":
                    v = "met" if got == "connector" else ("referred" if got == "both" else "not met")
                else:
                    v = "referred"
                verdicts.append((part, v, got))
            worst = "not met" if any(v == "not met" for _, v, _ in verdicts) else ("referred" if any(v == "referred" for _, v, _ in verdicts) else "met")
            item(c, "K4", worst, "; ".join(f"({p}) reader '{g}' -> {v}" for p, v, g in verdicts)
                 + ("; checker's proposed reading: 'both' meets 'connector' when the relied-on claims are exactly the key's K2 set" if worst == "referred" else ""))
        else:
            got = r.get("admitted_current_support_for_3_0_m")
            item(c, "K7", "met" if got is k["K7_admitted_current_support_for_3_0_m"] else "not met", f"reader {got}")
            if "K8_what_the_source_states_now" in k:
                s = (r.get("what_the_source_states_now") or "").lower()
                adm = any("rev-b" in x.lower() and ("admission" in x.lower() or "admitted" in x.lower()) for x in cc)
                ok = "2.4 m" in s and "rev-b" in s and adm
                item(c, "K8", "met" if ok else "not met", f"2.4 m and rev-B named: {'2.4 m' in s and 'rev-b' in s}; rev-B admission not established: {adm}")
        # K5
        ok = all(has_groups(cc, groups) for groups in MUST[c])
        item(c, "K5", "met" if ok else "not met", "required unsupported conclusion found in cannot_conclude" if ok else "not found")
        # K6
        verdict, why = "met", "no forbidden conclusion stated as supported"
        if c == "P3":
            bad = [x for x in r.get("answer", {}).get("a", []) if re.search(r"\b(VC|E|O-B1|O-C1)\b", x)]
            if bad:
                verdict, why = "not met", f"answer (a) asserts stale states {bad}"
        notes = (r.get("notes") or "").lower() + " " + json.dumps(r.get("answer", {})).lower()
        hits = [p for p in FORBID_PHRASES if p in notes]
        if hits and verdict == "met":
            verdict, why = "referred", f"forbidden phrase(s) {hits} outside cannot_conclude; negation not parsed"
        item(c, "K6", verdict, why)
    ind = (cases.get("independence") or "").lower()
    if ind.startswith("no") and "does not change" in ind:
        v = "met"
    elif ind.startswith("yes"):
        v = "not met"
    else:
        v = "referred"
    item("INDEPENDENCE", "K9", v, "reader: " + ind[:120])
    return out


def main():
    acc = json.load(open(sys.argv[1]))
    key = json.load(open(sys.argv[2]))
    res = score(acc, key)
    tally = {v: sum(1 for r in res if r["verdict"] == v) for v in ("met", "not met", "referred")}
    for r in res:
        print(f"{r['case']:12} {r['item']:3} {r['verdict']:9} {r['why']}")
    print(f"\n{tally['met']} met, {tally['not met']} not met, {tally['referred']} referred, of {len(res)}")
    if "--out" in sys.argv:
        with open(sys.argv[sys.argv.index("--out") + 1], "w") as f:
            json.dump({"items": res, "tally": tally}, f, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
