#!/usr/bin/env python3
"""Fail closed on incomplete/incorrect native fixture evidence. No guest actions."""
import json
from pathlib import Path
import sys


def verify(text):
    rows = []
    for line in text.splitlines():
        p = line.split('\t')
        if len(p) != 5 or not p[0].isdigit():
            raise ValueError('unrecognized native output: ' + line[:200])
        rows.append((int(p[0]), p[1], p[2], p[3], p[4]))
    if not rows or len({r[2] for r in rows}) != 1:
        raise ValueError('missing/mixed generation')
    if any(r[3] in ('REFUSAL', 'CLEANUP_UNKNOWN') for r in rows):
        raise ValueError('refusal or cleanup unknown: never pass')
    if any(a[0] > b[0] for a, b in zip(rows, rows[1:])):
        raise ValueError('observer time reversed')
    results = {}
    for case in ('P01-positive', 'P01-negative', 'P02-A', 'P02-B', 'P02-C'):
        events = [r for r in rows if r[1] == case]
        def one(kind):
            found = [r for r in events if r[3] == kind]
            if len(found) != 1:
                raise ValueError(case + ' missing/duplicate ' + kind)
            return found[0]
        def order(*kinds):
            positions = [events.index(one(k)) for k in kinds]
            if positions != sorted(set(positions)):
                raise ValueError(case + ' wrong order ' + str(kinds))
        one('CASE_CLEANUP')
        if one('CASE_CLEANUP')[4] != ('leaderSignaled=true;descendantSignaled=' +
                ('true' if case.startswith('P01') or case == 'P02-B' else 'not_created') + ';innerActive=0'):
            raise ValueError('case cleanup incomplete')
        order('ASSIGN_ATTEMPT', 'ASSIGNED', 'BOUND')
        order('CREATED_LEADER', 'RESUME_ATTEMPT', 'RESUMED', 'HELPER_ENTRY')
        if case.startswith('P01'):
            order('HELPER_ENTRY', 'HELPER_PRE', 'PRE_ACK', 'HELPER_CREATED', 'DESCENDANT_HANDLE', 'MEMBERSHIP', 'HELPER_FINAL', 'CONTAINMENT', 'CASE_CLEANUP')
            order('PRE_ACK', 'HELPER_EFFECT', 'MEMBERSHIP')
            # Independent helper QPCs must agree with causal observer acknowledgments.
            def qpc(kind):
                return int(one(kind)[4].split(';')[0].removeprefix('qpc='))
            if not (qpc('HELPER_ENTRY') <= qpc('HELPER_PRE') <= one('PRE_ACK')[0] <= qpc('HELPER_EFFECT')):
                raise ValueError('helper causal time invalid')
            if one('BOUND')[4] != f'appSession={rows[0][2]};home=fixture-home;spawnCounter={case}':
                raise ValueError('full invented-generation binding missing')
            negative = case == 'P01-negative'
            expected = f'inner={not negative};safety=True;live=True'
            if one('MEMBERSHIP')[4] != expected:
                raise ValueError('unknown/missing/incorrect membership')
            if negative:
                order('HELPER_EFFECT', 'ASSIGN_ATTEMPT', 'BOUND', 'HELPER_FINAL')
                order('DESCENDANT_HANDLE', 'ASSIGN_ATTEMPT')
                if one('CONTAINMENT')[4] != 'REJECT':
                    raise ValueError('broken launch falsely accepted')
                results[case] = 'REJECTED deliberately broken containment; safety contained'
            else:
                order('ASSIGNED', 'BOUND', 'RESUME_ATTEMPT')
                if one('BOUND')[0] > qpc('HELPER_ENTRY'):
                    raise ValueError('entry before bind')
                if one('CONTAINMENT')[4] != 'PASS':
                    raise ValueError('positive containment not established')
                results[case] = 'PASS'
        else:
            expected = {'P02-A': 'leaderSignaled=False;exit=259;eof=True',
                        'P02-B': 'leaderSignaled=true;exit=0;eof=false;descendantLive=true',
                        'P02-C': 'leaderSignaled=true;exit=259;exit259IsExit=true'}
            if one('OBSERVATION')[4] != expected[case] or one('CASE')[4] != 'PASS':
                raise ValueError(case + ' independent observations not established')
            order('BOUND', 'RESUME_ATTEMPT', 'OBSERVATION', 'CASE', 'CASE_CLEANUP')
            results[case] = 'PASS'
    cleanup = [r for r in rows if r[3] == 'SAFETY_CLEANUP']
    if len(cleanup) != 1 or cleanup[0][4] != 'allRetainedHandlesSignaled=true;active=0':
        raise ValueError('safety cleanup not observed')
    results['cleanup'] = 'all retained process HANDLEs signaled; safety Job active=0'
    return results

if __name__ == '__main__':
    print(json.dumps(verify(Path(sys.argv[1]).read_text()), indent=2))
