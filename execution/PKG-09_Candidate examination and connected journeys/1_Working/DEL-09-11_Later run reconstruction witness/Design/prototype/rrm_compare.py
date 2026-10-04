#!/usr/bin/env python3
"""RRM examiner comparison (DEL-09-11 RRM-v0.1 §5). Prototype only; not product code.

Compares a reader's reconstruction account with the records of the input set
it was given. The examiner derives the truth from the records itself; the
account is never authority. Checks RC-1…RC-9 (RRM §5). Writes nothing except
EXP result records under --out (only when --exp-schema is given).

Usage:
  python3 -B rrm_compare.py --fixture <input-set root> \
     --input-set fixtures/IS-FX-DP1.input-set.json --account <account.json> \
     [--exp-schema <DEL-09-01>/exam.result-record.schema.json --criterion <ScopeOfWork.md> --out DIR]
Exit status 0 when every check holds, 1 when one fails, 2 when one is referred to the examiner
(an outcome/change claim with no outcome record and no recorded judgment; RC-9).
"""
import argparse, hashlib, json, os, re, sys

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def truth_from_records(root, items):
    recs = []
    for it in items:
        if it['path'].endswith('.jsonl') and it['standing'] == 'record':
            recs += [json.loads(l) for l in open(os.path.join(root, it['path'])) if l.strip()]
    pk = {r['recordId']: r for r in recs if r.get('kind') == 'act_request' and 'alternatives' in r.get('body', {})}
    out = {}
    for rid, p in pk.items():
        b = p['body']; alts = {a['id'] for a in b['alternatives']}; dec = None
        for r in recs:
            rb = r.get('body', {}); rel = rb.get('relations', {})
            if r.get('kind') == 'human_act' and rel.get('requestRef') == rid and rb.get('actKind') == b['actKind'] \
               and rel.get('alternativeChosen') in alts and rb.get('captureEvidence'):
                dec = {'alternative': rel['alternativeChosen'], 'actor': rb['decisionActor']['displayName'],
                       'recorder': r['recorder']['identity'], 'recorder_role': r['recorder']['role']}
        out[b['evidence']['ref']] = {'record': rid, 'decision': dec}
    return out

def bind_judgments(doc, account_path, acc):
    """RRM §5 (RV-EP EP-R1): a judgment file applies only to the account it names, by account id and the
    sha256 of the account file, and must name its examiner. Otherwise its judgments are ignored.
    Returns (judgments, note)."""
    if not doc:
        return {}, ''
    bound = doc.get('account') or {}
    if not isinstance(bound, dict) or not doc.get('examiner'):
        return {}, 'judgment file ignored: it does not name its account (id and sha256) and examiner'
    if bound.get('account_id') != acc.get('account_id') or bound.get('sha256') != sha(account_path):
        return {}, 'judgment file ignored: bound to another account (%s, %s)' % (bound.get('account_id'), str(bound.get('sha256'))[:12])
    return doc.get('judgments', {}), ''

def compare(root, ism, acc, ism_path, judgments=None):
    judgments = judgments or {}
    checks = []
    def chk(cid, text, ok, note=''):
        checks.append((cid, text, bool(ok), note))
    items = {i['path']: i for i in ism['items']}
    chk('RC-1', 'every input-set item has its stated sha256', all(sha(os.path.join(root, p)) == i['sha256'] for p, i in items.items()))
    ism_digest = sha(ism_path)
    chk('RC-2', 'the account names this input set', acc['input_set']['input_set_id'] == ism['input_set_id'] and acc['input_set']['sha256'] == ism_digest)
    authors = {a['identity'] for a in ism['source_journey']['run_authors']}
    chk('RC-3', 'the reader is not a run author (R23-10)', acc['reader']['identity'] not in authors and acc['reader']['separation'])
    bad_src = [(c['claim_id'], s['path']) for c in acc['claims'] for s in c.get('sources', []) if s['path'] not in items]
    chk('RC-4', 'every cited source is in the input set', not bad_src, str(bad_src))
    na = [(c['claim_id'], s['path']) for c in acc['claims'] if c['standing'] != 'unknown'
          for s in c.get('sources', []) if items.get(s['path'], {}).get('standing') == 'not_authority']
    # RRM §3: a `definition` item may support a check, never an act or an outcome (RV-EP EP-R6).
    act_kinds = ('decision', 'acceptance', 'change', 'outcome')
    na += [(c['claim_id'], s['path'] + ' (definition)') for c in acc['claims'] if c['standing'] != 'unknown' and c['kind'] in act_kinds
           for s in c.get('sources', []) if items.get(s['path'], {}).get('standing') == 'definition']
    chk('RC-5', 'no claim rests on an item that is not authority, and no act or outcome claim on a definition (REQ-004)', not na, str(na))
    truth = truth_from_records(root, ism['items'])
    # Subject of a claim (RRM §4, "Naming the subject"; repaired after RR-E): `about` names it by an
    # identifier — the package file path, the package id in that file, or the package's record id.
    # When `about` names no package, the package files among the claim's sources name it.
    ids = {}
    for ref, t in truth.items():
        pid = json.load(open(os.path.join(root, ref))).get('packageId')
        ids[ref] = [x for x in (ref, pid, t['record']) if x]
    def mentions(text, ident):
        return re.search(r'(?<![A-Za-z0-9])' + re.escape(ident) + r'(?![A-Za-z0-9])', text or '') is not None
    def subjects(c):
        named = [ref for ref, xs in ids.items() if any(mentions(c['about'], x) for x in xs)]
        if named:
            return named
        return [ref for ref in ids if any(sv['path'] == ref for sv in c.get('sources', []))]
    by_pkg = {ref: [] for ref in truth}
    for c in acc['claims']:
        for ref in subjects(c):
            by_pkg[ref].append(c)
    missing, contra = [], []
    for ref, t in truth.items():
        cs = by_pkg[ref]
        if not any(c['kind'] == 'request' for c in cs):
            missing.append((ref, 'request'))
        decs = [c for c in cs if c['kind'] == 'decision']
        if t['decision']:
            d = t['decision']
            if not decs:
                missing.append((ref, 'decision'))
            for c in decs:
                # the claim may add detail (e.g. "identity not verified"); it must name the recorded actor,
                # the recorded recorder (identity or role) and exactly the recorded alternative
                if c.get('alternative') != d['alternative'] or not mentions(c.get('actor', ''), d['actor']) \
                   or not (mentions(c.get('recorder', ''), d['recorder']) or mentions(c.get('recorder', ''), d['recorder_role'])):
                    contra.append((c['claim_id'], 'decision differs from the record'))
            for c in cs:
                if c['kind'] == 'no_decision':
                    contra.append((c['claim_id'], 'absence of a decision claimed where the records hold one'))
        else:
            if decs:
                contra.append(([c['claim_id'] for c in decs], 'decision claimed where the records hold none'))
            if not any(c['kind'] == 'no_decision' for c in cs):
                missing.append((ref, 'no_decision'))
    chk('RC-6', 'every package is reconstructed: its request, and its decision or the absence of one', not missing, str(missing))
    chk('RC-7', 'no claim contradicts the records (no fabricated, altered or denied decision)', not contra, str(contra))
    same = [c['claim_id'] for c in acc['claims'] if c['kind'] in ('decision', 'acceptance') and c.get('actor') and c.get('actor') == c.get('recorder')]
    chk('RC-8', 'every reconstructed act keeps actor distinct from recorder', not same, str(same))
    # RC-9 (repaired after RR-E). A claim that something changed or happened must cite a record of a
    # change or outcome. Absence claims (no_change, no_decision, no_outcome) are statements of what the
    # records do not hold and are compared under RC-6/RC-7. An `outcome` or `change` claim citing no
    # change or outcome record cannot be told apart, mechanically, from a statement of absence written
    # under that kind; the checker refers it to the examiner, whose recorded judgment decides
    # ('absence' holds; 'unsupported' fails). Without a judgment the check is REFERRED, never HOLDS.
    def outcome_record(sv):
        it = items.get(sv['path'], {})
        return it.get('standing') == 'host_evidence'
    refer, fail = [], []
    for c in acc['claims']:
        if c['kind'] not in ('change', 'outcome') or c['standing'] == 'unknown':
            continue
        if any(outcome_record(sv) for sv in c.get('sources', [])):
            continue
        j = judgments.get(c['claim_id'])
        if j == 'absence':
            continue
        (fail if j == 'unsupported' else refer).append(c['claim_id'])
    if fail:
        chk('RC-9', 'nothing is claimed changed or achieved without a record of it', False, 'unsupported by examiner judgment: ' + str(fail))
    elif refer:
        checks.append(('RC-9', 'nothing is claimed changed or achieved without a record of it', None, 'REFERRED to the examiner: ' + str(refer)))
    else:
        chk('RC-9', 'nothing is claimed changed or achieved without a record of it; what is unknown stays unknown', True)
    return checks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fixture', required=True); ap.add_argument('--input-set', required=True)
    ap.add_argument('--account', required=True); ap.add_argument('--judgments', help='examiner judgments on referred claims: JSON {claim_id: "absence"|"unsupported"}'); ap.add_argument('--exp-schema'); ap.add_argument('--criterion'); ap.add_argument('--out')
    a = ap.parse_args()
    ism = json.load(open(a.input_set)); acc = json.load(open(a.account))
    jdoc = json.load(open(a.judgments)) if a.judgments else {}
    judg, jnote = bind_judgments(jdoc, a.account, acc)
    if jnote:
        print('NOTE ' + jnote)
    checks = compare(a.fixture, ism, acc, a.input_set, judg)
    for cid, text, ok, note in checks:
        tag = 'HOLDS ' if ok is True else ('REFER ' if ok is None else 'FAILS ')
        print(tag + cid + ': ' + text + ('' if ok is True or not note else ' — ' + note[:240]))
    failed = [c for c in checks if c[2] is False]
    referred = [c for c in checks if c[2] is None]
    print('%d checks, %d failed, %d referred to the examiner' % (len(checks), len(failed), len(referred)))
    if a.exp_schema:
        import jsonschema
        schema = json.load(open(a.exp_schema)); fmt = schema['properties']['format']['const']
        crit_line = [l for l in open(a.criterion) if l.startswith('- **AC-004**')][0]
        rec = {'record_kind': 'exam_result', 'format': fmt, 'record_id': 'RRM-%s-rehearsal' % acc['account_id'],
               'support_revision': {'exp_version': fmt, 'schema_id': schema['$id']},
               'case': {'case_id': 'RR-E', 'owner_deliverable': 'DEL-09-11', 'part': 'reader rehearsal on the early-path fixture'},
               'criterion': {'source': 'DEL-09-11 ScopeOfWork AC-004', 'identity': 'sha256:' + hashlib.sha256(crit_line.encode()).hexdigest()},
               'activity': 'verification', 'run_basis': 'rehearsal',
               'subject': {'kind': 'double', 'double': 'FX-DP1 input set %s; account %s' % (ism['input_set_id'], acc['account_id']),
                           'file_digests': ['sha256:%s %s' % (i['sha256'], i['path']) for i in ism['items']]},
               'configuration': {'codex_pin': 'not_applicable', 'route': {'kind': 'model_only'}},
               'date': {'value': acc['reconstruction_date']['value'], 'source': acc['reconstruction_date']['source']},
               'outcome': 'fail' if failed else ('inconclusive' if referred else 'pass'),
               'evidence': [{'ref': 'prototype/rrm_compare.py', 'digest': 'sha256:' + sha(__file__), 'provenance': 'test_definition'},
                            {'ref': a.account, 'digest': 'sha256:' + sha(a.account), 'provenance': 'review_record'}]
                           + ([{'ref': a.judgments, 'digest': 'sha256:' + sha(a.judgments), 'provenance': 'review_record'}] if judg else []),
               'limits': ([{'label': jnote, 'vocabulary': 'DEL-09-11 RRM-v0.1'}] if jnote else []) + ([{'label': 'claims referred to the examiner without a judgment: %s' % [c[3] for c in referred], 'vocabulary': 'DEL-09-11 RRM-v0.1'}] if referred else []) + [{'label': 'rehearsal of the reader method on an invented decision fixture; not the V4-EXM-31 week-later witness on a host journey', 'vocabulary': 'DEL-09-11 RRM-v0.1'}],
               'currency': {'state': 'current'}}
        errs = [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(rec)]
        print(('HOLDS' if not errs else 'FAILS') + ' EXP record schema-valid ' + '; '.join(errs)[:200])
        if a.out:
            os.makedirs(a.out, exist_ok=True)
            json.dump(rec, open(os.path.join(a.out, rec['record_id'] + '.json'), 'w'), indent=2)
        if errs: failed.append('exp')
    sys.exit(1 if failed else (2 if referred else 0))

if __name__ == '__main__':
    main()
