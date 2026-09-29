#!/usr/bin/env python3
import sys, json, csv
S = sys.argv[1]
recs = json.load(open(S + '/out/p2_records.json'))
sys.path.insert(0, S)
from load import regs
R = regs()
ORDER = ['DEL-04-01','DEL-04-02','DEL-04-03','DEL-02-01','DEL-02-03','DEL-03-01','DEL-03-02','DEL-03-03','DEL-03-04','DEL-01-01','DEL-05-01','DEL-05-02','DEL-09-06','DEL-09-09','DEL-02-04','DEL-07-01','DEL-07-02','DEL-08-01','DEL-08-02']
NAME = {d: R[d][1][0]['FromDeliverableName'] for d in ORDER}
KIND = {'MIRROR':'mirror','NEWREP':'new arc (consumer row)','NEWMIR':'new arc (supplier row)','EXT':'non-deliverable row','EDIT':'field edit','PKG':'package row','NORM':'value normalization'}
def effect(r):
    k = r['kind']
    if r['disp'] in ('DROP','DEFER'):
        return 'none (not applied)'
    if k in ('NEWREP','NEWMIR'):
        return 'creates %s (%s)' % (r['arc'], r['layer'])
    if k == 'MIRROR':
        return 'drift; new SR-6 representative' if r['dir'] == 'UPSTREAM' else 'drift (MIRROR)'
    return 'drift (non-topological)'
def route(r):
    return {'EXTRACT':'extraction','EXTRACT*':'extraction after P1 wording, else declaration','NONE':'—','DECLARE':'human (register owner)'}[r['route']]
def tgt(r):
    t = r.get('tgt') or r.get('row') or ''
    return t.replace('EXT:', '')
def esc(s):
    return (s or '').replace('|', '\\|').replace('\n', ' ')
out = []
for d in ORDER:
    rs = [r for r in recs if r['host'] == d]
    if not rs: continue
    out.append('### %s — %s\n' % (d, NAME[d]))
    out.append('| C1 item | Change | Target / row | Disposition | Route | Grounding | Currency effect | Reason or note |')
    out.append('|---|---|---|---|---|---|---|---|')
    for r in rs:
        ch = KIND[r['kind']]
        if r['kind'] in ('MIRROR','NEWREP','NEWMIR','EXT'):
            ch += ': %s %s' % (r.get('dir',''), r.get('typ',''))
        why = r.get('why') or ''
        if r['kind'] == 'MIRROR' and r['disp'] in ('KEEP','AMEND'):
            why = (why + ' ' if why else '') + 'Counterpart %s verified ACTIVE on the same arc.' % r['cp']
        if r.get('newid'):
            why = ('Proposed ID %s. ' % r['newid']) + why
        disp = r['disp'] if r['disp'] != 'KEEP-CONFIRM' else 'KEEP (confirm at K1)'
        out.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (esc(r['c1']), esc(ch), esc(tgt(r)), disp, route(r), esc(r.get('ground') or '—'), effect(r), esc(why)))
    out.append('')
    rows = [r['csvrow'] for r in rs if r.get('csvrow')]
    if rows:
        out.append('Rows to add (29 canonical columns in [`proposed_rows/%s_proposed_rows.csv`](proposed_rows/%s_proposed_rows.csv)):\n' % (d, d))
        out.append('| DependencyID | Direction | DependencyType | TargetType | Target | RequiredMaturity | SatisfactionStatus | Statement | SourceRef | EvidenceQuote (expected) |')
        out.append('|---|---|---|---|---|---|---|---|---|---|')
        for x in rows:
            out.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (x['DependencyID'], x['Direction'], x['DependencyType'], x['TargetType'], x['TargetDeliverableID'] or x['TargetRefID'], x['RequiredMaturity'], x['SatisfactionStatus'], esc(x['Statement']), esc(x['SourceRef']), esc(x['EvidenceQuote'])))
        out.append('')
open(S + '/out/per_deliverable.md', 'w').write('\n'.join(out))
print(len(out))
