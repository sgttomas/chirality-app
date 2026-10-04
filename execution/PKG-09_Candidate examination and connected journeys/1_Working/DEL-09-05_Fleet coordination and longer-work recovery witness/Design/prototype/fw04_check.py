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

def agent_identities(records):
    """RV-EP EP-R2: RS's decisionActor ($defs/person) has no 'kind'. An agent actor shows up as an
    identity the run knows as an agent's: every requester of an act_request whose kind is 'agent'."""
    return {r['body']['requester']['identity'] for r in records
            if r.get('kind') == 'act_request' and r.get('body', {}).get('requester', {}).get('kind') == 'agent'}

def actor_names(actor):
    return {v for k, v in actor.items() if k in ('displayName', 'osAccount', 'codexAccount') and isinstance(v, str)}

def decision_for(pkg, records, fx, captures):
    """FW rules R-1…R-6 (DAC §3). Returns (current decision or None, not-counted list, counted history)."""
    body = pkg['body']; alts = {a['id'] for a in body['alternatives']}
    agents = agent_identities(records)
    # R-6 (R23-25, O-A): a correction (entry-level `corrects`, RS OF-5/W-3) is not a new decision; it takes
    # the place of the entry it corrects, and the latest correction is used. A later A16 that is not a
    # correction is a new decision and supersedes the earlier for current standing; both stay listed.
    corrected_by = {}
    for r in records:
        if r.get('corrects'):
            corrected_by[r['corrects']] = r
    def current_version(r):
        while r.get('recordId') in corrected_by:
            r = corrected_by[r['recordId']]
        return r
    history, not_counted = [], []
    for r0 in records:
        if r0.get('kind') != 'human_act' or r0.get('corrects'):
            continue
        r = current_version(r0)
        b = r.get('body', {}); rel = b.get('relations', {})
        if rel.get('requestRef') != pkg['recordId']:
            continue
        rid = r.get('recordId')
        if b.get('actKind') != body.get('actKind'):
            not_counted.append((rid, 'R-2 act of another kind than the package names')); continue
        actor = b.get('decisionActor') or {}
        names = actor_names(actor)
        if not actor.get('displayName') or names & agents or names & {body['requester']['identity']}:
            not_counted.append((rid, 'R-3 decision actor is an agent of the run or the requester, not a person')); continue
        rec = r.get('recorder', {})
        if rec.get('role') not in PERSON_RECORDER_ROLES or rec.get('identity') in names:
            not_counted.append((rid, 'R-3 recorder not distinct from actor')); continue
        if body.get('actKind') == 'A16' and rel.get('alternativeChosen') not in alts:
            not_counted.append((rid, 'R-4 alternative not named by the package')); continue
        caps = [c for c in b.get('captureEvidence', []) if c.get('resolutionAtWrite') == 'resolved']
        cap = captures.get(caps[0]['ref']) if caps else None
        if cap is None:
            not_counted.append((rid, 'R-5 no resolvable capture evidence')); continue
        agree = (cap.get('requestRef') == pkg['recordId'] and cap.get('recordId') in (rid, r0.get('recordId'))
                 and cap.get('actKind') == b.get('actKind')
                 and cap.get('alternativeChosen') == rel.get('alternativeChosen')
                 and cap.get('actor', {}).get('displayName') == actor.get('displayName')
                 and cap.get('boundContent') == b.get('boundContent'))
        if not agree:
            not_counted.append((rid, 'R-5 capture evidence disagrees with the record')); continue
        history.append(r)
    return (history[-1] if history else None), not_counted, history

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
        d, nc, _ = decision_for(p, records, fx, captures)
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
    ap.add_argument('--rs-design', required=True, help="DEL-04-03's Design folder (RS_RECORD.schema.json and prototype/minischema.py, read-only)")
    ap.add_argument('--as-design', required=True, help="DEL-04-02's Design folder (AS_SETTINGS_IN.schema.json, which RS references)")
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

    # RS validation of the fixture's records, and of every record this check constructs (RV-EP EP-R2)
    sys.path.insert(0, os.path.join(a.rs_design, 'prototype'))
    from minischema import Registry, validate as ms_validate
    reg = Registry(); rs_schema = reg.by_id[reg.load(os.path.join(a.rs_design, 'RS_RECORD.schema.json'))]
    reg.load(os.path.join(a.as_design, 'AS_SETTINGS_IN.schema.json'))
    def rs_errors(rec):
        return ms_validate(rec, rs_schema, reg)
    bad_fx = [(r['recordId'], rs_errors(r)[:1]) for r in records if rs_errors(r)]
    expect('setup', 'every fixture record is valid against RS (with its CE-4 and AS references)', not bad_fx, str(bad_fx)[:200])

    # P04-A package exactness (REQ-001; V4-PM-04). The reserving basis is read from the package file's
    # own `reservedBy` element (R23-24 item 1; RV-EP EP-R4), through the file the request cites.
    for p in packages(records):
        b = p['body']; ids = [x['id'] for x in b['alternatives']]
        f = json.load(open(os.path.join(fx, b['evidence']['ref'])))
        basis = f.get('reservedBy') or []
        ok = (b.get('actKind') and b.get('subject') and b.get('purpose') and b.get('scope') and len(ids) >= 2
              and len(set(ids)) == len(ids) and all(c['alternative'] in ids for c in b['consequences'])
              and set(ids) <= {c['alternative'] for c in b['consequences']}
              and b.get('requester', {}).get('kind') == 'agent'
              and len(basis) >= 1 and all(x.get('ref') and x.get('statement') for x in basis)
              and [x['id'] for x in f.get('alternatives', [])] == ids)
        expect('P04-A', 'package %s names the exact act, subject, purpose, scope, two or more alternatives, a consequence for each and its requester; its file names the basis that reserves it (reservedBy) and the same alternatives' % p['recordId'], ok)

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
    def variant(mutate, extra=None, cap_mutate=None):
        rs = copy.deepcopy([r for r in records if r is not act]); x = copy.deepcopy(act); mutate(x)
        rs.append(x)
        if extra: rs.extend(extra)
        caps = copy.deepcopy(captures)
        if cap_mutate: cap_mutate(caps)
        errs = rs_errors(x)
        d, nc, _ = decision_for(pkg1, rs, fx, caps)
        return d, nc, errs
    agent_id = pkg1['body']['requester']['identity']
    def agent_actor(x):
        x['body']['decisionActor'] = {'displayName': agent_id, 'identityVerified': False}
    def agent_capture(caps):
        for c in caps.values():
            if c.get('requestRef') == pkg1['recordId']:
                c['actor'] = {'displayName': agent_id, 'identityVerified': False}
    d, nc, errs = variant(agent_actor, cap_mutate=agent_capture)
    expect('P04-C', "N-1 an RS-valid act whose actor is the requesting agent's own identity, with agreeing capture evidence, decides nothing", not errs and d is None, (nc[0][1] if nc else '') + (' RS: %s' % errs[:1] if errs else ''))
    d, nc, errs = variant(lambda x: x['body'].__setitem__('captureEvidence', []))
    expect('P04-C', 'N-2 a record without resolvable capture evidence decides nothing', d is None, (nc[0][1] if nc else '') + (' (RS refuses this record too)' if errs else ''))
    d, nc, errs = variant(lambda x: x['body'].__setitem__('actKind', 'A5'))
    expect('P04-C', 'N-3 an act of another kind citing the package decides nothing', d is None, nc[0][1] if nc else '')
    d, nc, errs = variant(lambda x: x['body']['relations'].__setitem__('alternativeChosen', 'ALT-9'))
    expect('P04-C', 'N-4 an alternative the package does not name decides nothing', not errs and d is None, (nc[0][1] if nc else '') + (' RS: %s' % errs[:1] if errs else ''))
    # N-5's entries are non-act events; they are stand-ins whose only relevant property is that they are not
    # a human_act (R-1), so they are not RS-validated.
    rs = [r for r in records if r is not act] + [
        {'recordId': 'syn:op-1', 'kind': 'operation_entry', 'body': {'result': 'success', 'relations': {'requestRef': pkg1['recordId']}}},
        {'recordId': 'syn:close-1', 'kind': 'request_closed', 'body': {'cause': 'timeout', 'relations': {'requestRef': pkg1['recordId']}}},
        {'recordId': 'syn:ret-1', 'kind': 'return_received', 'body': {'relations': {'requestRef': pkg1['recordId']}}}]
    d, _, _ = decision_for(pkg1, rs, fx, captures)
    expect('P04-C', 'N-5 tool success, a timeout, a return arriving and silence decide nothing', d is None)

    # R-6 (R23-25, O-A): a later A16 supersedes for current standing; a correction is not a new decision.
    later = copy.deepcopy(act); later['recordId'] = 'rec:app:coord:0099'; later['seq'] = 99; later['writtenAt'] = 'w099'
    later['body']['relations']['alternativeChosen'] = 'ALT-1'
    later['body']['captureEvidence'] = [{'kind': 'capture evidence', 'ref': 'cap:later', 'resolutionAtWrite': 'resolved'}]
    caps2 = copy.deepcopy(captures); c0 = [c for c in caps2.values() if c.get('requestRef') == pkg1['recordId']][0]
    c1 = copy.deepcopy(c0); c1.update({'captureId': 'cap:later', 'recordId': 'rec:app:coord:0099', 'alternativeChosen': 'ALT-1'}); caps2['cap:later'] = c1
    d, _, hist = decision_for(pkg1, records + [later], fx, caps2)
    expect('P04-B', 'R-6: ' + 'a later A16 on the same package supersedes for current standing (ALT-1), and the earlier decision stays listed', not rs_errors(later) and d and d['recordId'] == 'rec:app:coord:0099' and len(hist) == 2)
    corr = copy.deepcopy(act); corr['recordId'] = 'rec:app:coord:0098'; corr['seq'] = 98; corr['writtenAt'] = 'w098'
    corr['corrects'] = act['recordId']; corr['correctionReason'] = 'scope text mis-recorded (invented)'
    corr['body']['scope'] = corr['body']['scope'] + ' — corrected'
    d, _, hist = decision_for(pkg1, records + [corr], fx, captures)
    expect('P04-B', 'R-6: ' + 'a correction (corrects, with reason) is not a new decision: one decision, shown in its corrected form', not rs_errors(corr) and d and d['recordId'] == 'rec:app:coord:0098' and len(hist) == 1, str(rs_errors(corr)[:1]))

    # P04-D lapse: the package file edited after the decision (on a scratch copy)
    import shutil
    scratch = os.path.join(a.out, 'fx-lapse'); shutil.rmtree(scratch, ignore_errors=True); shutil.copytree(fx, scratch)
    with open(os.path.join(scratch, 'project/decisions/PKG-1.json'), 'a') as f:
        f.write('\n')
    expect('P04-D', 'the decision shows lapsed after its package changes, and is still listed', lapse(pkg1, decision_for(pkg1, records, scratch, captures)[0], scratch) == 'lapsed')

    # P04-E other acts keep their own standing, no invented sequence: an RS-valid A4 by the person on another
    # App file, written before the decision.
    other = copy.deepcopy(act); other['recordId'] = 'rec:app:coord:0000'; other['seq'] = 1; other['writtenAt'] = 'w000'
    other['body']['actKind'] = 'A4'; other['body']['boundSubject'] = ['App file reports/stage-1.md (invented)']
    other['body']['relations'] = {}
    d, _, _ = decision_for(pkg1, [other] + records, fx, captures)
    expect('P04-E', 'an unrelated RS-valid A4 neither decides the package nor is required before the decision', not rs_errors(other) and d is not None and d['recordId'] == act['recordId'], str(rs_errors(other)[:1]))

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
