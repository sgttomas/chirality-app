#!/usr/bin/env python3
"""TOP §7 CB-1 check of a traffic observation record (DEL-09-07 TOP-v0.1). Prototype only; standard library.

CB-1: a contact tagged `calibration_check` is calibration, and excluded from the §7 comparison, only when its
destination is one of `calibration_setup.endpoints` and its first and last times lie within
`calibration_setup.interval`. Times are parsed as ISO-8601 instants and compared as instants; a time
without a UTC offset is refused (the schema also requires the one form YYYY-MM-DDThh:mm:ss[.fraction]Z, TOP §6). Any other tagged contact is
mis-tagged: it is reported and compared as a run contact, so it cannot escape the comparison.

Usage: python3 -B top_check.py <record or examples file> [...]   Exit 0 when no record has a mis-tagged contact.
"""
import json, sys
from datetime import datetime, timezone

def instant(t):
    d = datetime.fromisoformat(t.replace('Z', '+00:00'))
    if d.tzinfo is None:
        raise ValueError('time without a UTC offset: %r' % t)
    return d.astimezone(timezone.utc)

def misstagged(rec):
    setup = rec.get('calibration_setup') or {}
    eps = set(setup.get('endpoints', [])); iv = setup.get('interval', {})
    out = []
    for i, c in enumerate(rec.get('contacts', [])):
        if 'calibration_check' not in c:
            continue
        reasons = []
        if c['destination_address'] not in eps:
            reasons.append('destination not a declared calibration endpoint')
        if not (instant(iv['start']) <= instant(c['first_seen']) and instant(c['last_seen']) <= instant(iv['end'])):
            reasons.append('outside the calibration interval')
        if reasons:
            out.append((i, c['destination_address'], reasons))
    return out

def run_contacts(rec):
    """The contacts the §7 comparison must include: every contact not validly calibration."""
    bad = {i for i, _, _ in misstagged(rec)}
    return [c for i, c in enumerate(rec.get('contacts', [])) if 'calibration_check' not in c or i in bad]

def records(doc):
    if isinstance(doc, dict) and doc.get('record_kind'):
        return [(doc.get('record_id'), doc)]
    return [((x.get('instance', x)).get('record_id'), x.get('instance', x)) for x in doc]

if __name__ == '__main__':
    any_bad = False
    for path in sys.argv[1:]:
        for rid, rec in records(json.load(open(path))):
            m = misstagged(rec)
            any_bad |= bool(m)
            print(('MIS-TAGGED ' if m else 'OK         ') + str(rid) + (' ' + json.dumps(m) if m else '') +
                  ' — run contacts compared: %d of %d' % (len(run_contacts(rec)), len(rec.get('contacts', []))))
    sys.exit(1 if any_bad else 0)
