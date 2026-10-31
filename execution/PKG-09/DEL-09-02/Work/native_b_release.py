"""Explicit task-operator release of a held B observer after App normal exit.

This is administrative cleanup, never qualification. The caller supplies the
already-held Run/Child, not a PID. The App/supplier sandbox must deny access to
this private control channel; filesystem ownership alone does not authenticate
a person or distinguish all processes running as the same user.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat

CONTROL = 'release-observer-after-app-exit.json'
ACTION = 'release-observer-after-app-exit'
ACTOR = 'controller under explicit task-operator disposition; not personal human act'
LIMIT = ('Administrative observer release only. No generation, LT-23, supplier '
         'settlement or B success is manufactured by waiting the original App.')


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def normal_exit(value):
    return (isinstance(value, dict) and set(value) == {'code', 'status'}
            and type(value['code']) is int and type(value['status']) is int
            and value == {'code': os.CLD_EXITED, 'status': 0})


def request_for(run):
    """Offer an exact request only from a current original-child exit reading."""
    digest = getattr(run, 'admission_sha', None)
    candidate = run.value.get('candidate_key')
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
        return None
    if not isinstance(candidate, str) or not candidate or run.reservation is None:
        return None
    try:
        observed = run.reservation.observe()
    except (OSError, RuntimeError):
        return None
    if not normal_exit(observed):
        return None
    return {'action': ACTION, 'candidate': candidate, 'admission_sha256': digest,
            'expected_app_exit': dict(observed)}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate administrative control field')
        result[key] = value
    return result


def _stamp(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid,
            info.st_nlink, info.st_size, info.st_mtime_ns)


@contextmanager
def _request(root):
    root = Path(root)
    before = root.lstat()
    require(root.is_absolute() and root.resolve() == root and stat.S_ISDIR(before.st_mode)
            and before.st_uid == os.getuid() and stat.S_IMODE(before.st_mode) == 0o700,
            'administrative control root is not a private owned plain directory')
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        held = os.fstat(directory)
        require((held.st_dev, held.st_ino) == (before.st_dev, before.st_ino), 'control root changed')
        descriptor = os.open(CONTROL, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        try:
            info = os.fstat(descriptor)
            require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                    and stat.S_IMODE(info.st_mode) == 0o600 and info.st_nlink == 1
                    and 0 < info.st_size <= 4096, 'administrative control file is not private, plain or bounded')
            raw = bytearray()
            while len(raw) <= 4096:
                chunk = os.read(descriptor, 4097 - len(raw))
                if not chunk:
                    break
                raw.extend(chunk)
            require(len(raw) == info.st_size and _stamp(os.fstat(descriptor)) == _stamp(info),
                    'administrative control changed while reading')
        finally:
            os.close(descriptor)
        yield directory, bytes(raw), json.loads(raw, object_pairs_hook=_unique_object)
    finally:
        os.close(directory)


def _write_once(directory, name, raw):
    descriptor = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=directory)
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(raw)


def release_if_requested(run, original_error):
    """None when absent; refuse before reap; return 1 after administrative reap.

    The caller invokes this only in its held-failure loop and consumes one
    request occurrence. The original-child method must recheck the exit before
    waiting. No normal Stop/Quit/qualification permission is substituted.
    """
    root = Path(run.root)
    if not os.path.lexists(root / CONTROL):
        return None
    with _request(root) as (directory, raw, request):
        expected = request_for(run)
        require(expected is not None, 'original App normal exit or admission binding unavailable')
        require(request == expected and normal_exit(request.get('expected_app_exit')),
                'administrative control does not match this admission and observed exit')
        # Both exclusive records must finish before the original Child is waited.
        # No stronger durable-media claim follows from these file writes.
        _write_once(directory, 'administrative-release-request.json', raw)
        intent = {'at': datetime.now(timezone.utc).isoformat(), 'request': request,
                  'request_sha256': hashlib.sha256(raw).hexdigest(), 'actor': ACTOR,
                  'original_error': str(original_error), 'limits': LIMIT}
        _write_once(directory, 'administrative-release-intent.json',
                    (json.dumps(intent, indent=2) + '\n').encode())
        code = run.reservation.administrative_reap(request['expected_app_exit'])

    # Once the actual Child has been reaped, later reporting errors must not
    # send this observer back into a hold claiming it still reserves that Child.
    run.cleanup = True
    errors = []
    for operation in (run.stop.set,
                      lambda: run.thread.join(timeout=8) if run.thread is not None else None):
        try:
            operation()
        except BaseException as error:
            errors.append(str(error)[:512])
    result = {'at': datetime.now(timezone.utc).isoformat(), 'candidate': run.value['candidate_key'],
              'phase': 'B', 'state': 'observer-released-after-external-app-exit', 'success': False,
              'original_error': str(original_error), 'actual_app_wait_code': code,
              'administrative_app_reap': True, 'original_app_reaped': True,
              'app_exit_observation': request['expected_app_exit'],
              'supplier_settled_observed': run.supplier_settled, 'generation': run.generation,
              'actor': ACTOR, 'post_reap_errors': errors, 'limits': LIMIT,
              'guard_reason': getattr(run, 'reason', None),
              'sampling_observations': getattr(run, 'sampling', {})}
    for operation in (lambda: run.record('administrative-release-result.json', result),
                      lambda: run.report(result)):
        try:
            operation()
        except BaseException as error:
            errors.append(str(error)[:512])
    return 1
