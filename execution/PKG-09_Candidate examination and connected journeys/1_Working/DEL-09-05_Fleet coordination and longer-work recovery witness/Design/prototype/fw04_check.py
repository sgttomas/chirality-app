#!/usr/bin/env python3
"""FW-04 rehearsal check (DEL-09-05 DAC-v0.1 §4). Prototype only; not product code.

Compares the records of a decision-package fixture with an examiner's
observation of the person's decision (VER-004), and runs the negative
attribution variants in memory. It derives the decision independently of
DEL-06-02's decision_view.py (a second derivation, DAC §4.3).

Python 3 standard library, plus `jsonschema` only to validate the EXP result
records it writes against DEL-09-01's schema (given by --exp-schema).
Reads the fixture and observation read-only; writes only under --out.

Usage:
  python3 -B fw04_check.py --fixture <FX-DP1 dir> \
      --observation fixtures/examiner_observation.FX-DP1.json \
      --exp-schema <DEL-09-01 Design>/exam.result-record.schema.json \
      --criterion <DEL-09-05 ScopeOfWork.md> --out "$TMPDIR/fw04"
"""
import argparse, copy, hashlib, json, os, sys

def sha256_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def check_manifest(fx):
    bad = []
    for line in open(os.path.join(fx, 'MANIFEST.sha256')):
        h, rel = line.strip().split(None, 1)
        if sha256_file(os.path.join(fx, rel)) != h:
            bad.append(rel)
    return bad

def load_records(fx):
    return [json.loads(l) for l in open(os.path.join(fx, 'records', 'coordination.rs.jsonl')) if l.strip()]

def packages(records):
    return [r for r in records if r.get('kind') == 'act_request' and 'alternatives' in r.get('body', {})]

PERSON_RECORDER_ROLES = {'App interface (capturing surface)', 'App writer', 'host facility'}

def decision_for(pkg, records, fx, captures):
    """FW rules R-1…R-6 (DAC §4.3). Returns (decision record or None, list of (record id, reason not counted))."""
    body = pkg['body']; alts = {a['id'] for a in body['alternatives']}
    counted, not_counted = None, []
    for r in records:
        if r.get('kind') != 'human_act':
            continue
        b = r.get('body', {}); rel = b.get('relations', {})
        if rel.get('requestRef') != pkg['recordId']:
            continue
        rid = r.get('recordId')
        if b.get('actKind') != body.get('actKind'):
            not_counted.append((rid, 'R-2 act of another kind than the package names')); continue
        actor = b.get('decisionActor') or {}
        if not actor.get('displayName') or actor.get('kind') == 'agent':
            not_counted.append((rid, 'R-3 no person as decision actor')); continue
        if r.get('recorder', {}).get('role') not in PERSON_RECORDER_ROLES or r.get('recorder', {}).get('identity') == actor.get('displayName'):
            not_counted.append((rid, 'R-3 recorder not distinct from actor')); continue
        if body.get('actKind') == 'A16' and rel.get('alternativeChosen') not in alts:
            not_counted.append((rid, 'R-4 alternative not named by the package')); continue
        caps = [c for c in b.get('captureEvidence', []) if c.get('resolutionAtWrite') == 'resolved']
        cap = captures.get(caps[0]['ref']) if caps else None
        if cap is None:
            not_counted.append((rid, 'R-5 no resolvable capture evidence')); continue
        agree = (cap.get('requestRef') == pkg['recordId'] and cap.get('recordId') == rid
                 and cap.get('actKind') == b.get('actKind')
                 and cap.get('alternativeChosen') == rel.get('alternativeChosen')
                 and cap.get('actor', {}).get('displayName') == actor.get('displayName')
                 and cap.get('boundContent') == b.get('boundContent'))
        if not agree:
            not_counted.append((rid, 'R-5 capture evidence disagrees with the record')); continue
        counted = r  # R-6: the latest in written order is shown
    return counted, not_counted

def lapse(pkg, decision, fx):
    if decision is None:
        return None
    path = os.path.join(fx, pkg['body']['evidence']['ref'])
    if not os.path.exists(path):
        return 'unknown (unavailable)'
    now = 'sha256:' + sha256_file(path)
    bound = decision['body']['boundContent'][0]['value']
    return 'not lapsed' if now == bound else 'lapsed'

def derive(records, fx, captures):
    out = {}
    for p in packages(records):
        d, nc = decision_for(p, records, fx, captures)
        out[p['body']['evidence']['ref']] = {
            'state': 'decided' if d else 'pending',
            'alternative': d['body']['relations'].get('alternativeChosen') if d else None,
            'actor': d['body']['decisionActor']['displayName'] if d else None,
            'recorder': d['recorder']['role'] if d else None,
            'lapse': lapse(p, d, fx), 'not_counted': nc}
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fixture', required=True); ap.add_argument('--observation', required=True)
    ap.add_argument('--exp-schema', required=True); ap.add_argument('--criterion', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    fx = a.fixture; os.makedirs(a.out, exist_ok=True)
    results = []  # (part, expectation, held, note)

    def expect(part, text, held, note=''):
        results.append((part, text, bool(held), note)); print(('HOLDS ' if held else 'FAILS ') + part + ': ' + text + (' — ' + note if note else ''))

    before = {l.split(None, 1)[1].strip(): l.split()[0] for l in open(os.path.join(fx, 'MANIFEST.sha256'))}
    expect('setup', 'fixture MANIFEST verifies', not check_manifest(fx))
    records = load_records(fx)
    captures = {}
    for f in os.listdir(os.path.join(fx, 'aac')):
        c = json.load(open(os.path.join(fx, 'aac', f)))
        if c.get('format') == 'chirality.aac.capture-evidence':
            captures[c['captureId']] = c
    obs = json.load(open(a.observation))
    view = derive(records, fx, captures)

    # P04-A package exactness (REQ-001; V4-PM-04)
    for p in packages(records):
        b = p['body']; ids = [x['id'] for x in b['alternatives']]
        ok = (b.get('actKind') and b.get('subject') and b.get('purpose') and b.get('scope') and len(ids) >= 2
              and len(set(ids)) == len(ids) and all(c['alternative'] in ids for c in b['consequences'])
              and set(ids) <= {c['alternative'] for c in b['consequences']}
              and p.get('body', {}).get('requester', {}).get('kind') == 'agent'
              and 'reserved to the person by' in b.get('purpose', ''))
        expect('P04-A', 'package %s names the exact act, subject, purpose, scope, two or more alternatives, a consequence for each, its requester and the basis that reserves it' % p['recordId'], ok)

    # P04-B faithful positive record vs observation
    for o in obs['observations']:
        v = view.get(o['package_file'])
        if o['observed'] == 'act performed':
            ok = v and v['state'] == 'decided' and v['alternative'] == o['alternative'] and v['actor'] == o['person'] and v['recorder'] != o['person'] and v['lapse'] == 'not lapsed'
            expect('P04-B', 'record of %s agrees with the observed act (person, alternative, actor ≠ recorder, bound to the package as decided)' % o['package_file'], ok)
        else:
            expect('P04-B', 'no decision is recorded for %s, where no act was observed' % o['package_file'], v and v['state'] == 'pending')

    # P04-C negatives (REQ-004: success, return, silence, timeout, another act, message text)
    msg = open(os.path.join(fx, 'conversation', 'agent-message.txt')).read()
    expect('P04-C', "an agent message claiming a decision does not decide PKG-2", 'chose' in msg and view['project/decisions/PKG-2.json']['state'] == 'pending')
    pkg1 = [p for p in packages(records) if p['body']['evidence']['ref'] == 'project/decisions/PKG-1.json'][0]
    act = [r for r in records if r.get('kind') == 'human_act'][0]
    def variant(mutate, extra=None):
        rs = copy.deepcopy([r for r in records if r is not act]); x = copy.deepcopy(act); mutate(x)
        rs.append(x)
        if extra: rs.extend(extra)
        d, nc = decision_for(pkg1, rs, fx, captures)
        return d, nc
    d, nc = variant(lambda x: x['body'].__setitem__('decisionActor', {'kind': 'agent', 'displayName': 'thread:fx-u1-manager'}))
    expect('P04-C', 'N-1 an act whose actor is the agent decides nothing', d is None, nc[0][1] if nc else '')
    d, nc = variant(lambda x: x['body'].__setitem__('captureEvidence', []))
    expect('P04-C', 'N-2 a record without resolvable capture evidence decides nothing', d is None, nc[0][1] if nc else '')
    d, nc = variant(lambda x: x['body'].__setitem__('actKind', 'A5'))
    expect('P04-C', 'N-3 an act of another kind citing the package decides nothing', d is None, nc[0][1] if nc else '')
    d, nc = variant(lambda x: x['body']['relations'].__setitem__('alternativeChosen', 'ALT-9'))
    expect('P04-C', 'N-4 an alternative the package does not name decides nothing', d is None, nc[0][1] if nc else '')
    rs = [r for r in records if r is not act] + [
        {'recordId': 'syn:op-1', 'kind': 'operation_entry', 'body': {'result': 'success', 'relations': {'requestRef': pkg1['recordId']}}},
        {'recordId': 'syn:close-1', 'kind': 'request_closed', 'body': {'cause': 'timeout', 'relations': {'requestRef': pkg1['recordId']}}},
        {'recordId': 'syn:ret-1', 'kind': 'return_received', 'body': {'relations': {'requestRef': pkg1['recordId']}}}]
    d, _ = decision_for(pkg1, rs, fx, captures)
    expect('P04-C', 'N-5 tool success, a timeout, a return arriving and silence decide nothing', d is None)

    # P04-D lapse: the package file edited after the decision (on a scratch copy)
    import shutil
    scratch = os.path.join(a.out, 'fx-lapse'); shutil.rmtree(scratch, ignore_errors=True); shutil.copytree(fx, scratch)
    with open(os.path.join(scratch, 'project/decisions/PKG-1.json'), 'a') as f:
        f.write('\n')
    expect('P04-D', 'the decision shows lapsed after its package changes, and is still listed', lapse(pkg1, decision_for(pkg1, records, scratch, captures)[0], scratch) == 'lapsed')

    # P04-E other acts keep their own standing, no invented sequence
    other = {'recordId': 'syn:a4-1', 'kind': 'human_act', 'recorder': {'role': 'App interface (capturing surface)'},
             'body': {'actKind': 'A4', 'decisionActor': {'displayName': 'Engineer A'}, 'relations': {}}}
    d, _ = decision_for(pkg1, [other] + records, fx, captures)
    expect('P04-E', 'an unrelated A4 neither decides the package nor is required before the decision', d is not None and d['recordId'] == act['recordId'])

    after = {rel: sha256_file(os.path.join(fx, rel)) for rel in before}
    expect('setup', 'the fixture is unchanged after the check', after == before)

    # EXP result records (rehearsal on the fixture double), validated against DEL-09-01's schema
    import jsonschema
    schema = json.load(open(a.exp_schema)); val = jsonschema.Draft202012Validator(schema)
    crit_line = [l for l in open(a.criterion) if l.startswith('- **AC-004**')][0]
    crit_id = 'sha256:' + hashlib.sha256(crit_line.encode()).hexdigest()
    digests = ['sha256:%s %s' % (h, rel) for rel, h in sorted(before.items())]
    me = 'sha256:' + sha256_file(__file__)
    parts = {}
    for part, text, held, note in results:
        if part == 'setup':
            continue
        parts.setdefault(part, []).append(held)
    exps = []
    for part, helds in sorted(parts.items()):
        expv = schema['properties']['format']['const']  # follow the EXP version given (R23-21)
        rec = {'record_kind': 'exam_result', 'format': expv, 'record_id': 'DAC-FW04-%s-rehearsal' % part,
               'support_revision': {'exp_version': expv, 'schema_id': schema['$id']},
               'case': {'case_id': 'FW-04', 'owner_deliverable': 'DEL-09-05', 'part': part},  # no scenario on a rehearsal (EXP)
               'criterion': {'source': 'DEL-09-05 ScopeOfWork AC-004', 'identity': crit_id},
               'activity': 'verification', 'run_basis': 'rehearsal',
               'subject': {'kind': 'double', 'double': 'FX-DP1 (DEL-06-02 early-path fixture, provisional) with a constructed examiner observation', 'file_digests': digests},
               'configuration': {'codex_pin': 'not_applicable', 'route': {'kind': 'model_only'}},
               'date': {'value': '2026-10-03', 'source': 'observed_clock'},
               'outcome': 'pass' if all(helds) else 'fail',
               'evidence': [{'ref': 'prototype/fw04_check.py', 'digest': me, 'provenance': 'test_definition'}],
               'limits': [{'label': 'rehearsal on an invented fixture; no person acted, no examiner observed; establishes nothing about a candidate', 'vocabulary': 'DEL-09-05 DAC-v0.1'}],
               'currency': {'state': 'current'}}
        errs = [e.message for e in val.iter_errors(rec)]
        expect('setup', 'EXP record for %s is schema-valid' % part, not errs, '; '.join(errs)[:200])
        exps.append(rec)
    json.dump(exps, open(os.path.join(a.out, 'fw04-exp-records.json'), 'w'), indent=2, ensure_ascii=False)
    failed = [r for r in results if not r[2]]
    print('%d expectations, %d failed' % (len(results), len(failed)))
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
