#!/usr/bin/env python3
"""DOS cross-reference checks a schema cannot express (DEL-09-07 DOS-v0.1 §1, §4, §5). Prototype only; standard library.

DX-1  Every receipt named in either hand-over (handoff_del_11_03.receipts, handoff_del_09_11.receipt_refs) is listed in
      host_evidence as a host_receipt, with the same resolution_at_write. The index lists every receipt the results cite
      (DOS §1); a hand-over never names one the index lacks, and never restates its resolution differently.
DX-2  When both hand-overs are present, they carry the same receipt set: both concern the one LHQ-20 journey
      (DOS §4: "the receipts with their resolution status at write"; §5: "Host receipt … references").

Usage: python3 -B dos_check.py <manifest or examples file> [...]   Exit 0 when no manifest breaks DX-1 or DX-2.
"""
import json, sys

def problems(m):
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
    return out

def manifests(doc):
    if isinstance(doc, dict):
        return [doc]
    return [x.get('instance', x) for x in doc]

if __name__ == '__main__':
    bad = False
    for path in sys.argv[1:]:
        for m in manifests(json.load(open(path))):
            p = problems(m); bad |= bool(p)
            print(('FAILS ' if p else 'OK    ') + m.get('dossier_id', '?') + ('' if not p else ' — ' + '; '.join(p)))
    sys.exit(1 if bad else 0)
