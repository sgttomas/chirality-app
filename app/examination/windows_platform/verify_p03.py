"""Strict P-03 source-bound trace checks. Invented unit rows are not native evidence."""
import re


def require(ok, why):
    if not ok:
        raise ValueError(why)


def fields(value):
    parts = [p.split('=', 1) for p in value.split(';')]
    require(all(len(p) == 2 for p in parts), 'invalid fields')
    require(len(dict(parts)) == len(parts), 'duplicate fields')
    return dict(parts)


def verify(raw, nonce, scenario):
    require(scenario in ('positive', 'wrong-slot', 'missing-observation'), 'scenario')
    require(re.fullmatch('[a-f0-9]{32}', nonce) is not None, 'nonce')
    require(len(raw) <= 128 * 1024, 'trace bound')
    rows = [line.split('\t') for line in raw.decode('ascii').splitlines()]
    require(rows and all(len(r) == 4 and r[1] == nonce and r[0].isdigit() for r in rows),
            'trace format/source')
    times = [int(r[0]) for r in rows]
    require(times == sorted(times), 'event order')
    kinds = ['IDENTITY', 'BOUND', 'DESCENDANT'] + ['REFUSED'] * 6 + [
        'STOP_CAUSE', 'STDIN_CLOSED', 'GRACE', 'PENDING_CAPTURE', 'SLOT_REPLACED',
        'REFUSED', 'PRE_TERMINATE', 'TERMINATE_ATTEMPT', 'TERMINATE_RESULT', 'REFUSED',
        'OBSERVATION_UNKNOWN' if scenario == 'missing-observation' else 'OBSERVATION',
        'RETIREMENT', 'CASE_DONE', 'CONTROLLER_CLEANUP', 'SAFETY_TERMINATE', 'SAFETY_CLEANUP']
    require([r[2] for r in rows] == kinds, 'missing/extra/reordered events or unknown cleanup')
    by_kind = {r[2]: r[3] for r in rows}
    identity = fields(by_kind['IDENTITY'])
    require(set(identity) == {'processMachine', 'nativeMachine', 'pointerBytes', 'frequency',
                              'experimentEnd', 'cleanupEnd'}, 'identity fields')
    require(all(v.isdigit() for v in identity.values()), 'identity values')
    require([identity[k] for k in ('processMachine', 'nativeMachine', 'pointerBytes')] ==
            ['0', '34404', '8'], 'native AMD64 identity')
    frequency, end, cleanup = [int(identity[k]) for k in ('frequency', 'experimentEnd', 'cleanupEnd')]
    require(frequency > 0 and times[0] < end < cleanup and cleanup - times[0] <= 18 * frequency,
            'original deadline bounds')
    require(times[-1] < cleanup, 'late cleanup')
    for time, _, kind, _ in rows:
        if kind not in ('CONTROLLER_CLEANUP', 'SAFETY_TERMINATE', 'SAFETY_CLEANUP'):
            require(int(time) < end, 'late experiment evidence')
    g = f'appSession={nonce};home=fixture-home;spawnCounter=1'
    g1 = f'appSession={nonce};home=fixture-home;spawnCounter=2'
    exact = {
        'BOUND': g, 'DESCENDANT': 'originalLeaderHandle=true;originalJobMember=true;live=true',
        'STOP_CAUSE': 'cause=explicit-fixture-stop;' + g, 'STDIN_CLOSED': g,
        'GRACE': 'testMilliseconds=150;leaderSignaled=true;descendantLive=true;originalActive=1',
        'PENDING_CAPTURE': g, 'SLOT_REPLACED': g1,
        'PRE_TERMINATE': 'originalDescendantLive=True;successorLive=True',
        'TERMINATE_ATTEMPT': 'target=current-slot-negative' if scenario == 'wrong-slot' else 'target=captured-original',
        'TERMINATE_RESULT': 'ok=True;error=0;confirmed=false',
        'RETIREMENT': 'CONFIRMED' if scenario == 'positive' else 'UNKNOWN',
        'CONTROLLER_CLEANUP': 'allRetainedActorsSignaled=true;allOriginalJobsActive=0;caseCompleted=True',
        'SAFETY_TERMINATE': 'fixture-cleanup-only',
        'SAFETY_CLEANUP': 'retainedControllerSignaled=true;active=0',
    }
    require(all(by_kind[k] == v for k, v in exact.items()), 'generation/outcome/cleanup mismatch')
    require([r[3] for r in rows if r[2] == 'REFUSED'] == [
        'second-bind', 'numeric-pid', 'serialized-pid', 'stale-session', 'stale-home',
        'stale-counter', 'stale-generation-start', 'success-alone;leader-only;zero-only'],
        'missing admission/retirement negative controls')
    t = {r[2]: int(r[0]) for r in rows}
    require((t['GRACE'] - t['STDIN_CLOSED']) * 1000 >= frequency * 150, 'short grace')
    if scenario == 'missing-observation':
        require(by_kind['OBSERVATION_UNKNOWN'] ==
                'injected-authoritative-job-query-unavailable;custody-retained=true', 'partial failure')
    else:
        expected = ('originalLeaderSignaled=True;originalDescendantSignaled=True;originalActive=0;'
                    'successorSignaled=False;successorActive=1') if scenario == 'positive' else (
                    'originalLeaderSignaled=True;originalDescendantSignaled=False;originalActive=1;'
                    'successorSignaled=True;successorActive=0')
        require(by_kind['OBSERVATION'] == expected, 'original/successor isolation evidence')
    require(re.fullmatch(re.escape(scenario) + r';elapsedTicks=[0-9]+',
                         by_kind['CASE_DONE']) is not None, 'case completion')
    return {'scenario': scenario, 'outcome': by_kind['RETIREMENT'], 'cleanup': 'OBSERVED',
            'mechanism_pass': scenario == 'positive'}
