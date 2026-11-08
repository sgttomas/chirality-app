#!/usr/bin/env python3
"""CIR agreement check a schema cannot express (DEL-09-07 LHQ-v0.2 §3 CI-5; LHQ2-R1, R23-42 item 3). Prototype only; standard library.

CI-5 agreement  When a CIR carries both elements.app_candidate.value and app_candidate_subject, the two describe the same
                build. Mechanically: the mapping's revision and build_identity each occur in value. Whether
                packaged and package_record match the build is left to the examiner. The example marker " (invented)"
                is ignored on both sides. Passing this check is necessary, not sufficient; any other
                disagreement the examiner finds is equally a CIR defect.

Usage: python3 -B cir_check.py <CIR or examples file> [...]   Exit 0 when no record breaks the agreement rule.
"""
import json, sys

MARK = ' (invented)'

def norm(s):
    return s.replace(MARK, '').strip()

def problems(r):
    v = ((r.get('elements') or {}).get('app_candidate') or {}).get('value')
    m = r.get('app_candidate_subject')
    if v is None or m is None:
        return []
    out = []
    for f in ('revision', 'build_identity'):
        if f in m and norm(m[f]) not in norm(v):
            out.append('CI-5 app_candidate_subject.%s %r does not occur in elements.app_candidate.value %r' % (f, m[f], v))
    return out

def records(doc):
    if isinstance(doc, dict):
        return [doc]
    return [x.get('instance', x) for x in doc]

if __name__ == '__main__':
    bad = False
    for path in sys.argv[1:]:
        for r in records(json.load(open(path))):
            p = problems(r); bad |= bool(p)
            print(('FAILS ' if p else 'OK    ') + r.get('record_id', '?') + ('' if not p else ' — ' + '; '.join(p)))
    sys.exit(1 if bad else 0)
