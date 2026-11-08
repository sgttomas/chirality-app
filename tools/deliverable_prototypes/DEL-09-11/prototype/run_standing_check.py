#!/usr/bin/env python3
"""Standing check of the comparison itself (DEL-09-11 RRM-v0.1 §5.1, SC-1…SC-3). Prototype only.

Runs rrm_compare.compare() on every account in the corpus and checks that each verdict is the
expected one. The corpus holds at least one INDEPENDENT reader's account (written by a reader
who is not the method's owner), because agreement with accounts the owner constructed did not
catch the RR-E defects. Run it after any change to rrm_compare.py, the reader brief or the
account schema.

Usage: python3 -B run_standing_check.py [--fixture <input-set root>]
(default: fixtures/RR-E-input, the nine files the RR-E reader was given, verified against RR-E's SUPPLIED.sha256)
Exit 0 when every verdict is as expected.
"""
import argparse, copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rrm_compare import compare, bind_judgments, package_identifiers, mentions
import jsonschema

F = os.path.join(HERE, 'fixtures')
ISM = os.path.join(F, 'IS-FX-DP1.input-set.json')
SCHEMA = json.load(open(os.path.join(HERE, '..', 'rrm.reconstruction-account.schema.json')))

def load(n): return json.load(open(os.path.join(F, n)))

def verdict(fx, acc, acc_path, jdoc):
    """acc_path is the account's file, or None for an in-memory mutation (whose bytes no judgment names)."""
    errs = list(jsonschema.Draft202012Validator(SCHEMA).iter_errors(acc))
    if errs:
        return {'schema': 'rejected'}
    if acc_path is None:
        import tempfile
        t = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False); json.dump(acc, t); t.close(); acc_path = t.name
    judg, _ = bind_judgments(jdoc, acc_path, acc)
    res = compare(fx, json.load(open(ISM)), acc, ISM, judg)
    return {'failed': sorted(c[0] for c in res if c[2] is False), 'referred': sorted(c[0] for c in res if c[2] is None)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fixture', default=os.path.join(F, 'RR-E-input'), help='input-set root; default: the exact bytes the RR-E reader was given')
    a = ap.parse_args()
    P = lambda n: os.path.join(F, n)
    ind = load('account.independent.RR-E.json'); ind_j = load('judgments.independent.RR-E.json'); bad2_j = load('judgments.bad2.json')
    m1 = copy.deepcopy(ind); [c.__setitem__('alternative', 'ALT-1') for c in m1['claims'] if c['claim_id'] == 'C-05']
    m2 = copy.deepcopy(ind)
    for c in m2['claims']:
        if c['claim_id'] == 'C-07':
            c.update({'kind': 'decision', 'actor': 'Engineer A', 'recorder': 'app-interface:local', 'alternative': 'ALT-1'})
    m3 = copy.deepcopy(ind); [c.__setitem__('about', 'PKG-2 decision') for c in m3['claims'] if c['claim_id'] == 'C-05']
    m4 = copy.deepcopy(ind)
    for c in m4['claims']:
        if c['claim_id'] == 'C-06':
            c.update({'kind': 'no_decision', 'about': 'PKG-1 decision'})
    unbound = copy.deepcopy(ind_j); unbound['account'] = {'account_id': 'some other account', 'sha256': '0' * 64}
    # A judgment never carries over to a changed account, so the mutations also leave C-09 referred (EP-R1).
    corpus = [
        ('SC-1 independent RR-E account, with its bound examiner judgment on C-09', ind, P('account.independent.RR-E.json'), ind_j, {'failed': [], 'referred': []}),
        ('SC-1 independent RR-E account, no judgment: C-09 is referred, nothing fails', ind, P('account.independent.RR-E.json'), {}, {'failed': [], 'referred': ['RC-9']}),
        ('SC-2 RR-E with a judgment bound to another account: ignored, C-09 referred', ind, P('account.independent.RR-E.json'), unbound, {'failed': [], 'referred': ['RC-9']}),
        ('SC-2 RR-E with the judgment file of another account (bad2): ignored', ind, P('account.independent.RR-E.json'), bad2_j, {'failed': [], 'referred': ['RC-9']}),
        ('SC-2 RR-E with C-05 altered to ALT-1', m1, None, ind_j, {'failed': ['RC-7'], 'referred': ['RC-9']}),
        ('SC-2 RR-E claiming a decision on PKG-2', m2, None, ind_j, {'failed': ['RC-6', 'RC-7'], 'referred': ['RC-9']}),
        ('SC-2 RR-E with the PKG-1 decision filed under PKG-2', m3, None, ind_j, {'failed': ['RC-6', 'RC-7'], 'referred': ['RC-9']}),
        ('SC-2 RR-E denying the PKG-1 decision', m4, None, ind_j, {'failed': ['RC-7'], 'referred': ['RC-9']}),
        ('SC-3 constructed good', load('account.good.json'), P('account.good.json'), {}, {'failed': [], 'referred': []}),
        ('SC-3 constructed bad1 (decision from the agent message)', load('account.bad1.json'), P('account.bad1.json'), {}, {'failed': ['RC-5', 'RC-6', 'RC-7'], 'referred': []}),
        ('SC-3 constructed bad2, judged unsupported', load('account.bad2.json'), P('account.bad2.json'), bad2_j, {'failed': ['RC-9'], 'referred': []}),
        ('SC-3 constructed bad2, no judgment', load('account.bad2.json'), P('account.bad2.json'), {}, {'failed': [], 'referred': ['RC-9']}),
        ('SC-3 constructed bad3 (reader is a run author)', load('account.bad3.json'), P('account.bad3.json'), {}, {'failed': ['RC-3'], 'referred': []}),
        ('SC-3 constructed bad4 (no sources)', load('account.bad4.json'), P('account.bad4.json'), {}, {'schema': 'rejected'}),
    ]
    bad = 0
    for name, acc, path, j, exp in corpus:
        got = verdict(a.fixture, acc, path, j)
        ok = got == exp; bad += not ok
        print(('AS EXPECTED ' if ok else 'UNEXPECTED  ') + name + ': ' + json.dumps(got) + ('' if ok else ' expected ' + json.dumps(exp)))
    # SC-2: a decision claim resting only on a `definition` item (RRM §3; EP-R6), on a scratch copy of the
    # supplied input set with the digest-rule definition added. Expected: RC-5 fails.
    import shutil, tempfile, hashlib
    root = tempfile.mkdtemp(); shutil.copytree(a.fixture, root, dirs_exist_ok=True)
    os.makedirs(os.path.join(root, 'definitions'), exist_ok=True)
    shutil.copy(os.path.join(F, 'definitions', 'aac-offer-digest-0.1.md'), os.path.join(root, 'definitions'))
    ism = json.load(open(ISM)); ism['input_set_id'] = 'SC-DEF-scratch'
    dpath = 'definitions/aac-offer-digest-0.1.md'
    ism['items'].append({'path': dpath, 'sha256': hashlib.sha256(open(os.path.join(root, dpath), 'rb').read()).hexdigest(),
                         'standing': 'definition', 'source': {'path': 'APP_ACT_CONTROL.md', 'sha256': '0' * 64}})
    ip = os.path.join(root, 'ism.json'); json.dump(ism, open(ip, 'w'))
    md = copy.deepcopy(ind); md['input_set'] = {'input_set_id': ism['input_set_id'], 'sha256': hashlib.sha256(open(ip, 'rb').read()).hexdigest()}
    for c in md['claims']:
        if c['claim_id'] == 'C-05':
            c['sources'] = [{'path': dpath, 'locator': 'the digest rule'}]
    res = compare(root, ism, md, ip, {})
    got = {'failed': sorted(c[0] for c in res if c[2] is False), 'referred': sorted(c[0] for c in res if c[2] is None)}
    exp = {'failed': ['RC-5'], 'referred': ['RC-9']}
    ok = got == exp; bad += not ok; corpus.append(None)
    print(('AS EXPECTED ' if ok else 'UNEXPECTED  ') + 'SC-2 a decision claim resting only on a definition item: ' + json.dumps(got) + ('' if ok else ' expected ' + json.dumps(exp)))
    # SC-3 on the R23-24 refreeze: input set IS-FX-DP1-3 (namespaced packageId; the subject rule's last-segment form).
    ism3p = os.path.join(F, 'IS-FX-DP1-3.input-set.json'); root3 = os.path.join(F, 'IS-FX-DP1-3-input')
    for name, fn, exp in [('SC-3 constructed good on IS-FX-DP1-3', 'account.good.IS-FX-DP1-3.json', {'failed': [], 'referred': []}),
                          ('SC-3 RR-E-shaped account on IS-FX-DP1-3 ("PKG-1 …" subjects; no bound judgment)', 'account.rre-shape.IS-FX-DP1-3.json', {'failed': [], 'referred': ['RC-9']})]:
        acc = load(fn)
        res = compare(root3, json.load(open(ism3p)), acc, ism3p, {})
        got = {'failed': sorted(c[0] for c in res if c[2] is False), 'referred': sorted(c[0] for c in res if c[2] is None)}
        ok = got == exp; bad += not ok; corpus.append(None)
        print(('AS EXPECTED ' if ok else 'UNEXPECTED  ') + name + ': ' + json.dumps(got) + ('' if ok else ' expected ' + json.dumps(exp)))
    # SC-1 (second independent reader): RR-F's account on IS-FX-DP1-3, exactly the files it was given.
    acc = load('account.independent.RR-F.json')
    res = compare(root3, json.load(open(ism3p)), acc, ism3p, {})
    got = {'failed': sorted(c[0] for c in res if c[2] is False), 'referred': sorted(c[0] for c in res if c[2] is None)}
    exp = {'failed': [], 'referred': []}
    ok = got == exp; bad += not ok; corpus.append(None)
    print(('AS EXPECTED ' if ok else 'UNEXPECTED  ') + 'SC-1 independent RR-F account on IS-FX-DP1-3 (no judgment needed): ' + json.dumps(got) + ('' if ok else ' expected ' + json.dumps(exp)))
    # SC-2 overlapping tails (RV hardening): PKG-1 and PKG-1-b admit no short form; distinct tails do.
    ov = package_identifiers({'a.json': ('pkg:t:PKG-1', 'rec:1'), 'b.json': ('pkg:t:PKG-1-b', 'rec:2')})
    ds = package_identifiers({'a.json': ('pkg:t:PKG-1', 'rec:1'), 'b.json': ('pkg:t:PKG-2', 'rec:2')})
    ok = ('PKG-1' not in ov['a.json'] and 'PKG-1-b' not in ov['b.json'] and 'pkg:t:PKG-1' in ov['a.json']
          and 'PKG-1' in ds['a.json'] and 'PKG-2' in ds['b.json']
          and not mentions('pkg:t:PKG-1-b decision', 'pkg:t:PKG-1') and mentions('pkg:t:PKG-1-b decision', 'pkg:t:PKG-1-b')
          and mentions('PKG-1 decision.', 'PKG-1') and not mentions('PKG-1-b decision', 'PKG-1'))
    bad += not ok; corpus.append(None)
    print(('AS EXPECTED ' if ok else 'UNEXPECTED  ') + 'SC-2 overlapping tails PKG-1 / PKG-1-b admit no short form, and the full id pkg:t:PKG-1 is not found inside pkg:t:PKG-1-b; PKG-1 / PKG-2 admit their tails: ' + json.dumps({'overlap': ov, 'distinct': ds}))
    print('%d cases, %d unexpected' % (len(corpus), bad))
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
