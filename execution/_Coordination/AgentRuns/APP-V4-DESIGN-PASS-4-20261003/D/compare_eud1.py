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
  'connector', and 'both' when the relied-on claims are exactly the key's K2
  set (ruled by R23-45.1; was REFERRED before that ruling).
- K5 must-name: each required unsupported conclusion is found by a set of
  term groups, every group needing one match, in the reader's
  cannot_conclude list.
- K6 forbid (repaired for RV2 EUD1-R10; R23-48 item 2). Judged on structured
  fields first; phrase matching is only a supplement:
  1. Structured contradiction -> not met: P3's answer (a) names a node that
     is READY/ACTIVE only at S; an answer item carries anything beyond node,
     state and the state's own parenthetical (e.g. "T2 PLANNED, ready to
     dispatch"); DM-1/DM-2 claim admitted current support.
  2. Structured affirmation of the forbidden kinds -> required for met: for
     every PEC case, cannot_conclude must name each of the three forbidden
     kinds (empty work; readiness to start or dispatch; permission). If one
     is missing, the item is REFERRED: the reader may have concluded it.
  3. Supplement, free text (notes, and answer text): a sentence that matches
     the paraphrase lexicon (FORBID_LEXICON: "can begin", "may start",
     "ready to dispatch", "nothing is outstanding", "is finished", …) and
     carries no negator outside the matched phrase ("not", "cannot", "never",
     "n't", "no longer", "without", "nothing", "no") is NOT MET; with a
     negator it is REFERRED (negation is not parsed further).
  Otherwise met. RR-EUD1's eight K6 "met" verdicts were also confirmed by
  RV2's reading (RV2-EUD1, repair confirmation), not by this checker alone.
  **Limit (RV2 EUD1-R14; R23-52 item 2).** The lexicon cannot reach "in any
  wording" and is not grown further. A K6 "met" on a case whose free text
  (notes, source statement) is non-empty therefore carries
  `examiner_reading_required: true`, and the tally counts those items
  separately. Such a "met" is established for the structured fields only;
  the free text needs an examiner's reading before the verdict is relied
  on, as a "referred" item does. Known paraphrases the lexicon misses (RV2's
  N-2 "There is nothing left to do here.", N-6 "PEC permits dispatching
  T2.") are sensitivity cases that show the flag is raised, not that the
  checker catches them.
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
    "P6": [[["no response", "absent", "silence", "nothing"], ["pec"]],
           # second half of the key item (EUD1-R10): its silence or absence is not empty work
           [["silence", "absence", "absent"], ["empty work", "no work", "establishes nothing", "not empty", "nothing"]]],
    "DM-1": [[["3.0 m", "3.0m"], ["admitted"], ["currently", "now", "stale", "rev-b"]]],
    "DM-2": [[["domains"], ["no response", "nothing", "no results"]]],
}

FORBID_LEXICON = [
    # empty work / completion
    "no work remains", "no work is left", "nothing is outstanding", "nothing outstanding", "nothing remains",
    "is finished", "are finished", "is idle", "all work is complete", "undertaking is complete",
    # readiness to start / dispatch
    "ready to start", "ready to dispatch", "can be dispatched", "may be dispatched",
    "can begin", "may begin", "can start", "may start", "can proceed", "may proceed",
    # permission
    "is permitted", "are permitted", "is allowed", "are allowed",
    # Domains
    "spacing is 3.0 m", "2.4 m is admitted",
]
NEGATORS = ("not ", "cannot", "never", "n't", "no longer", "without", "nothing", "no ")
KINDS = {  # forbidden kinds the reader must name in cannot_conclude (PEC cases)
    "empty work": ["no work", "empty work", "nothing remains", "idle"],
    "readiness": ["ready to start", "ready", "may start", "dispatch"],
    "permission": ["permitted", "permission"],
}
ANSWER_ITEM = re.compile(r"^\s*[A-Za-z0-9-]+:?\s*(\([^)]*\))?\s*:?\s*(READY|ACTIVE|BLOCKED|PLANNED|COMPLETE)(\s*\([^)]*\))?\s*$|"
                         r"^\s*[A-Za-z0-9-]+:?\s+(READY|ACTIVE|BLOCKED|PLANNED|COMPLETE)(\s*\([^)]*\))?\s*->\s*(READY|ACTIVE|BLOCKED|PLANNED|COMPLETE)(\s*\([^)]*\))?\s*$|^\s*[A-Za-z0-9-]+:?\s+added as [A-Z]+(\s*\([^)]*\))?\s*$")


def sentences(text):
    return [x.strip() for x in re.split(r"(?<=[.;!?])\s+|\n", text or "") if x.strip()]


def lexicon_hits(texts):
    """-> list of (sentence, phrase, negated)."""
    out = []
    for t in texts:
        for snt in sentences(t):
            low = snt.lower()
            for ph in FORBID_LEXICON:
                if ph in low:
                    rest = low.replace(ph, " ")  # a negator inside the matched phrase itself does not negate it
                    out.append((snt, ph, any(n in rest for n in NEGATORS)))
    return out


def has_groups(texts, groups):
    for t in texts:
        tl = t.lower()
        if all(any(term in tl for term in g) for g in groups):
            return True
    return False


def score(acc, key):
    out = []

    def item(case, kid, verdict, why, **extra):
        out.append(dict({"case": case, "item": kid, "verdict": verdict, "why": why}, **extra))

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
                    # R23-45.1: 'both' meets 'connector' when the relied-on claims are exactly the key's K2 set
                    v = "met" if got == "connector" or (got == "both" and rel == set(k["K2_pec_claims_relied_on"])) else "not met"
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
        # K6 (structured first; lexicon as a supplement)
        verdict, why = "met", "no forbidden conclusion stated as supported; every forbidden kind named in cannot_conclude"
        ans = r.get("answer", {}) or {}
        answer_items = [x for part in ("a", "b", "c") for x in ans.get(part, [])]
        if c == "P3":
            bad = [x for x in ans.get("a", []) if re.search(r"\b(VC|E|O-B1|O-C1)\b", x)]
            if bad:
                verdict, why = "not met", f"answer (a) asserts stale states {bad}"
        extra = [x for x in answer_items if not ANSWER_ITEM.match(x)]
        if extra and verdict == "met":
            verdict, why = "not met", f"answer item(s) assert more than node and state: {extra}"
        if c.startswith("DM") and r.get("admitted_current_support_for_3_0_m") is True:
            verdict, why = "not met", "claims admitted current support for 3.0 m"
        free = [r.get("notes") or "", r.get("what_the_source_states_now") or ""] + answer_items
        hits = lexicon_hits(free)
        if verdict == "met" and any(not neg for _, _, neg in hits):
            verdict, why = "not met", "affirmative forbidden statement(s): " + "; ".join(f"'{s}'" for s, _, neg in hits if not neg)
        elif verdict == "met" and hits:
            verdict, why = "referred", "forbidden phrase(s) in a negated sentence; negation not parsed further: " + "; ".join(f"'{s}'" for s, _, _ in hits)
        if verdict == "met" and c in PEC:
            low = [x.lower() for x in cc]
            missing = [k for k, terms in KINDS.items() if not any(any(t in x for t in terms) for x in low)]
            if missing:
                verdict, why = "referred", f"cannot_conclude does not name {missing}; the reader may have concluded it"
        has_free = any((x or "").strip() for x in (r.get("notes"), r.get("what_the_source_states_now")))
        item(c, "K6", verdict, why, examiner_reading_required=bool(verdict == "met" and has_free))
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
    tally["met_needing_examiner_reading"] = sum(1 for r in res if r.get("examiner_reading_required"))
    for r in res:
        flag = " [free text: examiner reading required]" if r.get("examiner_reading_required") else ""
        print(f"{r['case']:12} {r['item']:3} {r['verdict']:9} {r['why']}{flag}")
    print(f"\n{tally['met']} met ({tally['met_needing_examiner_reading']} of them on free text needing an examiner's reading), "
          f"{tally['not met']} not met, {tally['referred']} referred, of {len(res)}")
    if "--out" in sys.argv:
        with open(sys.argv[sys.argv.index("--out") + 1], "w") as f:
            json.dump({"items": res, "tally": tally}, f, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()
