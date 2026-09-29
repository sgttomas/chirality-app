#!/usr/bin/env python3
"""Generate the P2 register-change proposal rows (preparation only; writes to OUT)."""
import sys, os, csv, json, re
S = sys.argv[1]; OUT = sys.argv[2]
sys.path.insert(0, S)
from load import regs, ROOT
from proposals import P
from grounding import G
R = regs()
ver = {v['c1']: v for v in json.load(open(S + '/verified.json'))}
nodes = {r['DeliverableID']: r for r in csv.DictReader(open(ROOT + '/_DAG/DAG-001/DeliverableNodes.csv'))}
scc = json.load(open(S + '/scc_result.json'))
LAYER = {k: v[2] for k, v in scc['S2_layers'].items()}
COLS = ['RegisterSchemaVersion','DependencyID','FromPackageID','FromDeliverableID','FromDeliverableName','DependencyClass','AnchorType','Direction','DependencyType','TargetType','TargetPackageID','TargetDeliverableID','TargetRefID','TargetName','TargetLocation','Statement','EvidenceFile','SourceRef','EvidenceQuote','Explicitness','RequiredMaturity','ProposedMaturity','SatisfactionStatus','Confidence','Origin','FirstSeen','LastSeen','Status','Notes']
# Expected SoW quote fragments, verbatim from the C1 proposed text (re-quote from applied bytes)
Q = {
 ('SC-04-01-2', None): 'It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02` and `DEL-09-09`, each of which declares it upstream in its own register.',
 ('SC-04-01-8', None): 'Operation-specific additions remain OPEN under OI-021 (owner via the outside SWB session and App/shared owner; before the connected-activity SoW).',
 ('SC-04-02-2', 'DEL-03-02'): 'It also consumes App v4 `DEL-03-02` proposal/outcome and direct-application origin semantics,',
 ('SC-04-02-2', 'DEL-03-01'): '`DEL-03-01` read-basis and standing facets,',
 ('SC-04-02-2', 'DEL-02-03'): 'and `DEL-02-03` hold-support values and checkpoint annotations.',
 ('SC-04-02-2', 'RECV'): 'Its visible autonomy state is received by `DEL-05-01`, `DEL-05-02`, `DEL-03-02`, `DEL-03-03` and `DEL-02-03`.',
 ('SC-04-03-1', 'DEL-04-01'): 'This format receives act kinds and classes from App `DEL-04-01`, settings-in from `DEL-04-02`,',
 ('SC-04-03-1', 'DEL-04-02'): 'This format receives act kinds and classes from App `DEL-04-01`, settings-in from `DEL-04-02`,',
 ('SC-04-03-1', 'DEL-03-01'): 'subject content identities and method designations from `DEL-03-01`,',
 ('SC-04-03-1', 'DEL-03-02'): 'operation outcomes, change-item content identities and receipt links from `DEL-03-02`,',
 ('SC-04-03-1', 'DEL-02-03'): 'hold-machine events and compatibility reports from `DEL-02-03`,',
 ('SC-04-03-1', 'DEL-03-03'): 'external dispatch entries from `DEL-03-03`,',
 ('SC-04-03-1', 'DEL-01-01'): 'and observed supplier facts (supplied guidance, model and destination, tool-permission settlements) from `DEL-01-01`.',
 ('SC-04-03-2', None): 'PKG-05 loop and panel receiving (`DEL-05-01`, `DEL-05-02`), PKG-06 decisions and the PKG-09 connected-activity and trace contracts (`DEL-09-06`, `DEL-09-09`) consume the record meaning',
 ('SC-02-01-1', 'DEL-03-02'): '`DEL-03-02` owns proposal/outcome semantics, including the governing checkpoint constraint, item dispositions and item-left events;',
 ('SC-02-01-1', 'DEL-01-01'): '`DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence;',
 ('SC-02-01-5', None): 'OI-001 and OI-002 were ruled for the first increment by DECISION-1 D2/D3 (carried by DEL-04-01).',
 ('SC-02-03-4', 'DEL-03-02'): '`DEL-03-02` owns proposal item dispositions, item-left events and the governing checkpoint constraint;',
 ('SC-02-03-4', 'DEL-04-02'): '`DEL-04-02` owns grant display states;',
 ('SC-02-03-4', 'DEL-03-03'): '`DEL-03-03` owns external-channel carriage and its assurance;',
 ('SC-02-03-4', 'DEL-01-01'): '`DEL-01-01` supplies observed supplier facts;',
 ('SC-02-03-4', 'DEL-01-04'): '`DEL-01-04` (later undertaking) constructs the App act control.',
 ('S5-1-1', None): '`DEL-04-02` owns the autonomy-grant display states and standing exchange, which this deliverable consumes as the grant in force carried on each dispatch;',
 ('S5-2-2', None): '`DEL-04-02` supplies autonomy-grant display states and active scope.',
 ('S5-2-3', None): '`DEL-02-03` supplies the hold-support values and hold-machine meanings (resume, re-hold, run end, act ordering, mixed decisions) that the panel displays.',
 ('S9-6-3', 'DEL-02-01'): 'App DEL-02-01 supplies portable declaration, identity and revision meaning;',
 ('S9-6-3', 'DEL-02-02'): 'App DEL-02-02 (later undertaking) supplies review and registration;',
 ('S9-6-3', 'DEL-03-01'): 'App DEL-03-01, DEL-03-02 and DEL-03-03 supply catalog/read-basis, proposal/outcome and external-receiving meanings;',
 ('S9-6-3', 'DEL-03-02'): 'App DEL-03-01, DEL-03-02 and DEL-03-03 supply catalog/read-basis, proposal/outcome and external-receiving meanings;',
 ('S9-6-3', 'DEL-03-03'): 'App DEL-03-01, DEL-03-02 and DEL-03-03 supply catalog/read-basis, proposal/outcome and external-receiving meanings;',
 ('S9-6-3', 'DEL-04-01'): 'App DEL-04-01 carries adopted operation policy and act distinctions and App DEL-04-02 grant display,',
 ('S9-6-3', 'DEL-04-02'): 'App DEL-04-01 carries adopted operation policy and act distinctions and App DEL-04-02 grant display,',
 ('S9-6-3', 'DEL-01-01'): 'App DEL-01-01 supplies the App-side supplied-guidance and model-destination evidence.',
 ('S9-9-4', 'DEL-05-01'): '`DEL-05-01` owns the App/shared embedded-loop receiving contribution used for the embedded surface of the three-channel trace;',
 ('S9-9-4', 'DEL-04-02'): '`DEL-04-02` owns grant display states;',
 ('S9-9-4', 'DEL-02-03'): '`DEL-02-03` owns the per-surface compatibility report and hold-support values.',
 ('S-04-6', None): "The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access), DEL-09-06's relay questions (the host-contribution column) and DEL-09-09's external trace cases,",
}
SOWLOC = {'SC-04-01-2':'CLM-002','SC-04-01-8':'TBD-001','SC-04-02-2':'CLM-002','SC-04-03-1':'CLM-004','SC-04-03-2':'REQ-005','SC-02-01-1':'CLM-002',
          'SC-02-01-5':'TBD-003','SC-02-03-4':'CLM-002','S5-1-1':'CLM-002','S5-2-2':'CLM-002','S5-2-3':'CLM-002','S9-6-3':'CLM-003','S9-9-4':'CLM-002','S-04-6':'CLM-002 or CLM-003','SC-04-01-10':'TBD-004 (new)','SC-04-02-6':'TBD-006 (new)','SC-02-01-6':'TBD-004 (new)','SC-02-03-1,':'CLM-003','SC-02-03-1':'CLM-003','S5-1-4':'TBD-003','SC-04-02-5':'TBD-001/TBD-002'}
EXT = {
 'EXT:OI-021': ('OI-021', 'Owner via outside SWB session and App/shared owner — operation-specific reserved additions and first connected operation', ROOT + '/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv#OI-021', 'UPSTREAM', 'CONSTRAINT'),
 'EXT:OI-018': ('OI-018', 'Open issue OI-018 (SoW TBD-003) — owner as recorded in Open_Issues.csv', ROOT + '/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv#OI-018', 'UPSTREAM', 'CONSTRAINT'),
 'EXT:DECISION-4-GOV': ('APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4', 'Owner — governance phase (enforced checkpoints and App-side run holds; D6 closed for Phase 1)', ROOT + '/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md', 'UPSTREAM', 'CONSTRAINT'),
 'EXT:DEP-001-RELAY': ('DEP-001', 'External SWBPIPE owner — human-relayed question set (RELAY_QUESTIONS_SWBPIPE.md); answered 2026-09-28', ROOT + '/_Decomposition/External_Dependencies.csv#DEP-001', 'DOWNSTREAM', 'HANDOVER'),
 'EXT:DECISION-5-OPEN': ('APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5', 'Owner — V4-HOST-02 accepted-basis revision and LOOP N-OPEN-4 (category switch vs named entries)', ROOT + '/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md', 'UPSTREAM', 'CONSTRAINT'),
}
def conv(d):  # the host register's SatisfactionStatus convention for unfulfilled execution rows
    vals = [r['SatisfactionStatus'] for r in R[d][1] if r['DependencyClass'] == 'EXECUTION' and r['Status'] == 'ACTIVE']
    return 'PENDING' if vals.count('PENDING') >= vals.count('TBD') else 'TBD'
def nextid(d, used):
    n = max(int(r['DependencyID'].split('-')[-1]) for r in R[d][1]) + 1 + used
    return 'DEP-%s-%s-%03d' % (d[4:6], d[7:9], n)
recs = []; used = {}
for p in P:
    v = ver[p['c1']]; g = G.get(p['c1'], (None, None, None, None))
    rec = dict(v)
    rec['ground'] = g[0]
    if g[1]: rec['disp'] = g[1]
    if g[2]: rec['route'] = g[2]
    if g[3]: rec['why'] = (g[3] if not rec.get('why') or g[1] else rec['why'] + ' ' + g[3])
    arc = p.get('arc')
    if p['kind'] in ('NEWREP', 'NEWMIR'):
        rec['layer'] = LAYER.get(arc, 'n/a (dropped)')
    elif p['kind'] == 'MIRROR':
        rec['layer'] = v.get('in_dag001')
    recs.append(rec)
    applies = rec['disp'] in ('KEEP', 'AMEND', 'ADD', 'KEEP-CONFIRM') and p['kind'] in ('MIRROR', 'NEWREP', 'NEWMIR', 'EXT')
    rec['applies'] = applies
    if not applies: continue
    h = p['host']; hn = nodes[h]
    did = nextid(h, used.get(h, 0)); used[h] = used.get(h, 0) + 1
    rec['newid'] = did
    row = {c: '' for c in COLS}
    row.update(RegisterSchemaVersion='v3.1', DependencyID=did, FromPackageID=hn['PackageID'], FromDeliverableID=h, FromDeliverableName=hn['DeliverableName'],
               DependencyClass='EXECUTION', AnchorType='NOT_APPLICABLE', Direction=p['dir'], DependencyType=p['typ'], Explicitness='EXPLICIT',
               ProposedMaturity='', SatisfactionStatus=conv(h), Confidence='HIGH', Origin='EXTRACTED', FirstSeen='<application date>', LastSeen='<application date>', Status='ACTIVE')
    t = p['tgt']
    if t.startswith('DEL-'):
        tn = nodes[t]
        row.update(TargetType='DELIVERABLE', TargetPackageID=tn['PackageID'], TargetDeliverableID=t, TargetName=tn['DeliverableName'], TargetLocation=tn['ExecutionPath'], RequiredMaturity='INITIALIZED')
    else:
        ref, name, loc, _, _ = EXT[t]
        row.update(TargetType='EXTERNAL', TargetRefID=ref, TargetName=name, TargetLocation=loc, RequiredMaturity='TBD')
    row['Statement'] = p['stmt']
    gr = rec['ground'] or ''
    corr = re.match(r'(S[C]?-?[0-9A-Z]*-[0-9]+(?:-[0-9]+)?|S\d-\d-\d|S9-\d-\d)', gr)
    key = None
    if gr.startswith('P1') or rec['route'] == 'EXTRACT*':
        row['EvidenceFile'] = 'ScopeOfWork.md'
        row['SourceRef'] = 'ScopeOfWork.md#<section of the P1 SoW sentence, if P1 adds one>'
        row['EvidenceQuote'] = '<quote the applied P1 sentence; if P1 adds none, record as a human declaration (see route)>'
        row['Confidence'] = 'HIGH'
    elif gr.startswith('SOW-NOW'):
        row['EvidenceFile'] = 'ScopeOfWork.md'; row['SourceRef'] = 'ScopeOfWork.md#' + ('OUT-004' if 'OUT-004' in gr else 'TBD-003')
        row['EvidenceQuote'] = '<quote from current SoW at application>'
    else:
        cid = gr.split(' ')[0].rstrip(',')
        row['EvidenceFile'] = 'ScopeOfWork.md'
        row['SourceRef'] = 'ScopeOfWork.md#%s (as revised per C1 %s)' % (SOWLOC.get(cid, '<section>'), cid)
        cand = [(cid, t), (cid, None)]
        if cid == 'SC-04-02-2' and p['dir'] == 'DOWNSTREAM': cand = [(cid, 'RECV')]
        for k in cand:
            if k in Q: row['EvidenceQuote'] = Q[k]; key = k; break
        if not row['EvidenceQuote']:
            row['EvidenceQuote'] = '<quote the applied %s sentence>' % cid
    corro = ('corroborated_by=%s:%s "%s"' % (v.get('evfile'), v.get('evline'), v.get('quote'))) if v.get('evfile') else 'corroborated_by=none in Design'
    lay = rec.get('layer')
    arcnote = ('arc=%s (%s)' % (arc, 'NEW; ' + ({'candidate': 'candidate layer, SCC-002 / SCC-CASE-002', 'admitted': 'admitted layer'}.get(lay, lay)))) if p['kind'] in ('NEWREP', 'NEWMIR') else ('arc=existing (%s in DAG-001); SR-6 %s' % (v.get('in_dag001'), 'MIRROR' if p['dir'] == 'DOWNSTREAM' else 'new representative (consumer UPSTREAM)')) if p['kind'] == 'MIRROR' else 'non-topological'
    row['Notes'] = 'FACT: %s; proposal=APP-V4-BASIS-ALIGN-20260928 P2 %s (C1 %s); %s; %s; quote_status=%s' % (
        ('grounded by C1 ' + gr) if gr and not gr.startswith('P1') else ('SoW grounding pending P1 (fallback: human declaration)' if gr.startswith('P1') else 'grounded by current SoW text'),
        p['c1'], p['c1'], arcnote, corro, 'expected text from C1 proposal; re-quote from applied SoW bytes' if key else 'to quote at application')
    rec['csvrow'] = row
json.dump(recs, open(OUT + '/p2_records.json', 'w'), indent=1, default=list)
os.makedirs(OUT + '/proposed_rows', exist_ok=True)
by = {}
for r in recs:
    if r.get('csvrow'): by.setdefault(r['host'], []).append(r['csvrow'])
for h, rows in sorted(by.items()):
    with open(OUT + '/proposed_rows/%s_proposed_rows.csv' % h, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
# counts
from collections import Counter
c = Counter((r['host'], r['kind'], r['disp'], r['route']) for r in recs)
for k, n in sorted(c.items()): print(k, n)
print('rows to apply', sum(1 for r in recs if r.get('csvrow')))
