#!/usr/bin/env python3
"""Fail closed on incomplete/incorrect native fixture evidence. No guest actions."""
import json
from pathlib import Path
import re
import sys


def verify_a(events):
    """Require the new A proof; this is never a replacement for the suite checks."""
    def one(kind):
        found = [r for r in events if r[3] == kind]
        if len(found) != 1:
            raise ValueError('P02-A missing/duplicate ' + kind)
        return found[0]
    def fields(kind, keys):
        row = one(kind)
        parts = row[4].split(';')
        if [p.split('=')[0] for p in parts] != keys.split():
            raise ValueError('P02-A malformed ' + kind)
        return dict(p.split('=', 1) for p in parts)
    def number(value):
        if not re.fullmatch(r'0|[1-9][0-9]{0,18}', value) or int(value) > 2**63 - 1:
            raise ValueError('P02-A invalid number')
        return int(value)
    deadline = fields('A_DEADLINE', 'startQpc untilQpc startMs untilMs frequency')
    start, until, start_ms, until_ms, frequency = [number(deadline[k]) for k in deadline]
    if frequency <= 0 or until - start != 8 * frequency or until_ms - start_ms != 8000:
        raise ValueError('P02-A original deadline invalid')
    read = fields('A_READ_START', 'handle leaderHandle untilMs untilQpc pendingBytes length')
    leader = fields('CREATED_LEADER', 'suspended safety handle')
    if (number(read['handle']) == 0 or read['leaderHandle'] != leader['handle'] or
            read['untilMs'] != deadline['untilMs'] or read['untilQpc'] != deadline['untilQpc'] or
            read['pendingBytes'] != '0' or read['length'] != '1'):
        raise ValueError('P02-A direct reader binding invalid')
    entry = re.fullmatch(r'qpc=([0-9]+);helper-entry;stdout=([0-9]+);stderr=([0-9]+)', one('HELPER_ENTRY')[4])
    if entry is None:
        raise ValueError('P02-A missing ENTRY handles')
    close = fields('A_CLOSE_CONFIRMATION', 'qpc stdout stderr alias stdoutOk stdoutError stderrAttempted stderrOk stderrError writeComplete')
    output, error = number(close['stdout']), number(close['stderr'])
    alias = output == error
    if (output == 0 or error == 0 or close['stdout'] != entry[2] or close['stderr'] != entry[3] or
            close['alias'] != str(alias) or close['stdoutOk'] != 'True' or
            close['stderrAttempted'] != str(not alias) or close['stderrOk'] != str(not alias) or
            close['writeComplete'] != 'True' or (alias and close['stderrError'] != '0')):
        raise ValueError('P02-A post-close proof invalid')
    if any(number(close[k]) > 2**31 - 1 for k in ('stdoutError', 'stderrError')):
        raise ValueError('P02-A invalid close error')
    result = fields('A_READ_RESULT', 'ok bytes error qpc completedMs workerStarted workerJoined failure')
    if any(result[k] != v for k, v in dict(ok='False', bytes='0', error='109',
            workerStarted='True', workerJoined='True', failure='none').items()):
        raise ValueError('P02-A read is not completed FALSE/109')
    proof = fields('A_READ_PROOF', 'closeConfirmed workerJoined beforeDeadline originalLeaderHandle')
    if proof != dict(closeConfirmed='True', workerJoined='True', beforeDeadline='True',
                     originalLeaderHandle=read['leaderHandle']):
        raise ValueError('P02-A live EOF proof incomplete')
    ordered = ['A_DEADLINE', 'CREATED_LEADER', 'HELPER_ENTRY', 'A_READ_START', 'A_READ_RESULT', 'A_READ_PROOF', 'OBSERVATION']
    positions = [events.index(one(k)) for k in ordered]
    if positions != sorted(set(positions)) or not (events.index(one('A_READ_START')) <
            events.index(one('A_CLOSE_CONFIRMATION')) < events.index(one('A_READ_PROOF'))):
        raise ValueError('P02-A proof order invalid')
    if (not start <= number(entry[1]) <= number(close['qpc']) <= one('A_CLOSE_CONFIRMATION')[0] < until or
            not one('A_READ_START')[0] <= number(result['qpc']) <= one('A_READ_RESULT')[0] < until or
            not start_ms <= number(result['completedMs']) < until_ms or
            not start <= one('A_DEADLINE')[0] <= one('OBSERVATION')[0] < until):
        raise ValueError('P02-A proof outside original deadline')


def verify_read_cleanup(rows):
    def one(case, kind):
        found = [r for r in rows if r[1] == case and r[3] == kind]
        if len(found) != 1:
            raise ValueError('A reader cleanup missing/duplicate ' + kind)
        return found[0]
    safety = one('suite', 'SAFETY_CLEANUP')
    read = one('P02-A', 'A_READ_RESULT')
    cleanup = one('suite', 'A_READ_CLEANUP')
    suffix = cleanup[4].removeprefix(read[4])
    match = re.fullmatch(r';deathProofQpc=([0-9]+);eofAfterDeathProof=(True|False);liveEofOutcomeUnchanged=True', suffix)
    if (match is None or not int(match[1]) <= safety[0] <= cleanup[0] or
            match[2] != str(int(read[4].split(';qpc=')[1].split(';')[0]) >= int(match[1]))):
        raise ValueError('A reader cleanup not observed or inconsistent')


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
            if case == 'P02-A':
                verify_a(events)
            results[case] = 'PASS'
    cleanup = [r for r in rows if r[3] == 'SAFETY_CLEANUP']
    if len(cleanup) != 1 or cleanup[0][4] != 'allRetainedHandlesSignaled=true;active=0':
        raise ValueError('safety cleanup not observed')
    verify_read_cleanup(rows)
    results['cleanup'] = 'all retained process HANDLEs signaled; safety Job active=0'
    return results

if __name__ == '__main__':
    print(json.dumps(verify(Path(sys.argv[1]).read_text()), indent=2))
