#!/usr/bin/env python3
"""DOS cross-reference checks a schema cannot express (DEL-09-07 DOS-v0.1 §1, §4, §5). Prototype only; standard library.

DX-1  Every receipt named in either hand-over (handoff_del_11_03.receipts, handoff_del_09_11.receipt_refs) is listed in
      host_evidence as a host_receipt, with the same resolution_at_write. The index lists every receipt the results cite
      (DOS §1); a hand-over never names one the index lacks, and never restates its resolution differently.
DX-2  When both hand-overs are present, they carry the same receipt set: both concern the one LHQ-20 journey
      (DOS §4: "the receipts with their resolution status at write"; §5: "Host receipt … references").
DX-3  A not-run case names no run (RR-EUF3, R23-49). Only LHQ-20 has hand-overs, so: when every EXP result the manifest
      cites for LHQ-20 has outcome `not-run`, there is no DEL-09-11 hand-over (its required journey, run authors and
      record set would name a run), and the DEL-11-03 hand-over names no acceptance act, no receipt and does not count
      as the completed witness. Outcomes come from EXP result records (record_id, outcome) passed with --outcomes.
      When an LHQ-20 outcome is not supplied, DX-3 is reported as not checked; it is never passed silently.

Usage: python3 -B dos_check.py [--outcomes <EXP records file>]... <manifest or examples file> [...]
Exit status (RV3 N8): 1 when any manifest breaks DX-1, DX-2 or DX-3; otherwise 2 when DX-3 could not be checked for
any manifest (an LHQ-20 outcome was not supplied); 0 only when every rule was checked and none is broken.
"""
import json, sys

def problems(m, outcomes=None):
    outcomes = outcomes or {}
    idx = {e['ref']: e['resolution_at_write'] for e in m.get('host_evidence', []) if e.get('kind') == 'host_receipt'}
    h11 = {r['ref']: r['resolution_at_write'] for r in (m.get('handoff_del_11_03') or {}).get('receipts', [])}
    h911 = {r['ref']: r['resolution_at_write'] for r in (m.get('handoff_del_09_11') or {}).get('receipt_refs', [])}
    out = []
    for where, rs in (('handoff_del_11_03', h11), ('handoff_del_09_11', h911)):
        for ref, res in rs.items():
            if ref not in idx:
                out.append('DX-1 %s names %s, which the host-evidence index does not list' % (where, ref))
            elif idx[ref] != res:
                out.append('DX-1 %s states %s as %s; the index has %s' % (where, ref, res, idx[ref]))
    if m.get('handoff_del_11_03') and m.get('handoff_del_09_11') and set(h11) != set(h911):
        out.append('DX-2 the hand-overs carry different receipt sets: DEL-11-03 %s, DEL-09-11 %s' % (sorted(h11), sorted(h911)))
    refs = [r for c in m.get('case_results', []) if c.get('case') == 'LHQ-20' for r in c.get('exam_result_refs', [])]
    unknown = [r for r in refs if r not in outcomes]
    notes = []
    if unknown:
        notes.append('DX-3 not checked: no outcome supplied for %s' % ', '.join(unknown))
    elif refs and all(outcomes[r] == 'not-run' for r in refs):
        h9 = m.get('handoff_del_09_11'); h3 = m.get('handoff_del_11_03') or {}
        if h9:
            out.append('DX-3 LHQ-20 is recorded not run, yet the DEL-09-11 hand-over names run %s' % h9.get('journey_run_ref', '?'))
        if h3.get('acceptance_acts'):
            out.append('DX-3 LHQ-20 is recorded not run, yet the DEL-11-03 hand-over names acceptance acts')
        if h3.get('receipts'):
            out.append('DX-3 LHQ-20 is recorded not run, yet the DEL-11-03 hand-over names receipts')
        if h3.get('counts_as_completed_witness'):
            out.append('DX-3 LHQ-20 is recorded not run, yet the DEL-11-03 hand-over counts as the completed witness')
    return out, notes

def load_outcomes(path):
    doc = json.load(open(path))
    recs = doc.get('records', [doc]) if isinstance(doc, dict) else doc
    return {r['record_id']: r['outcome'] for r in (x.get('instance', x) for x in recs)}

def manifests(doc):
    if isinstance(doc, dict):
        return [doc]
    return [x.get('instance', x) for x in doc]

if __name__ == '__main__':
    bad = unchecked = False
    args, outcomes = sys.argv[1:], {}
    while args and args[0] == '--outcomes':
        outcomes.update(load_outcomes(args[1])); args = args[2:]
    for path in args:
        for m in manifests(json.load(open(path))):
            p, notes = problems(m, outcomes); bad |= bool(p); unchecked |= bool(notes)
            print(('FAILS ' if p else 'OK    ') + m.get('dossier_id', '?') + ('' if not p else ' — ' + '; '.join(p))
                  + ('' if not notes else ' [' + '; '.join(notes) + ']'))
    sys.exit(1 if bad else 2 if unchecked else 0)
