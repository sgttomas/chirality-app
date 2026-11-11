#!/usr/bin/env python3
"""Explicit SQ package/S4 successor; original SQ reader remains unchanged."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
# Generated digests; re-derive with `python3 app/examination/repin.py` (examination/README.md).
PIN_LOCK_PATH = PROJECT / 'app/examination/pins.lock.json'


def locked_digest(section, path):
    """The pin lock's digest for path, or None when the lock is unreadable or lacks it.

    None never equals a digest, so the reader's own check refuses through its usual report.
    """
    try:
        value = json.loads(PIN_LOCK_PATH.read_bytes())[section][path]
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return value if isinstance(value, str) else None


PINS_SHA256 = locked_digest('current', 'app/examination/sq_receiving/pins.packages-v1.json')


def _lock_bytes():
    try:
        return PIN_LOCK_PATH.read_bytes()
    except OSError:
        return b''


PIN_LOCK_BYTES = _lock_bytes()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_relative(root, name):
    if not isinstance(name, str) or not name or PurePosixPath(name).is_absolute() or '\\' in name or any(p in ('', '.', '..') for p in name.split('/')):
        raise ValueError('non-canonical relative path')
    path = Path(root)
    for part in name.split('/'):
        path = path / part
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError('symbolic link refused')
    if not stat.S_ISREG(mode):
        raise ValueError('not a regular file')
    return path.read_bytes()


class Receiver:
    def __init__(self):
        raw = read_relative(HERE, 'pins.packages-v1.json')
        if sha(raw) != PINS_SHA256:
            raise ValueError('SQ reader pins changed')
        self.pins = json.loads(raw)
        self.sources = {}
        helper = 'app/examination/support_identity/support_identity.py'
        data = read_relative(PROJECT, helper)
        if sha(data) != self.pins['sources'][helper]:
            raise ValueError('selected source changed: ' + helper)
        spec = importlib.util.spec_from_file_location('_sq_publication_sources', PROJECT / helper)
        source_reader = importlib.util.module_from_spec(spec)
        exec(compile(data, str(PROJECT / helper), 'exec'), source_reader.__dict__)
        self.source_reader = source_reader
        self.sources[helper] = data
        for name, expected in self.pins['sources'].items():
            data = self.sources.get(name)
            if data is None:
                data = read_relative(PROJECT, name)
            if sha(data) != expected:
                raise ValueError('selected source changed: ' + name)
            self.sources[name] = data

    def check(self, selection, digest, configuration, configuration_sha256):
        selected_raw = read_relative(Path(selection).absolute().parent, Path(selection).name)
        if sha(selected_raw) != digest:
            raise ValueError('selection digest mismatch')
        purpose = self.source_reader.parse(selected_raw)['purpose']
        if purpose not in ('current_producer_declaration', 'historical_correspondence'):
            raise ValueError('unsupported purpose')
        if purpose != 'current_producer_declaration':
            raise ValueError('package/S4 successor requires explicit current purpose; use original reader for history')
        self.source_reader.checked_digest(configuration_sha256)
        configuration = Path(configuration).absolute()
        configuration_bytes = read_relative(configuration.parent, configuration.name)
        if sha(configuration_bytes) != configuration_sha256:
            raise ValueError('receiving configuration digest mismatch')
        # Run only captured, pinned Python validators in a private source snapshot.
        # This is not native execution or hostile-filesystem custody.
        with tempfile.TemporaryDirectory(prefix='sq-receiving-') as temp:
            root = Path(temp)
            for name, data in self.sources.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            (root / 'reader-pins.json').write_text(json.dumps(self.pins))
            # Snapshot readers verify their profiles against the same generated lock.
            (root / 'app/examination/pins.lock.json').write_bytes(PIN_LOCK_BYTES)
            (root / 'receiving-configuration.json').write_bytes(configuration_bytes)
            job = subprocess.run([sys.executable, '-B', str(root / 'app/examination/sq_receiving/worker_packages.py'),
                                  str(Path(selection).absolute()), digest,
                                  str(root / 'receiving-configuration.json'), configuration_sha256],
                                 cwd=root, capture_output=True, text=True, timeout=60)
            if job.returncode != 0:
                raise ValueError('captured SQ checker could not run')
            report = json.loads(job.stdout)
            report.update(reader_pins_sha256=PINS_SHA256, tool_sha256=sha(Path(__file__).read_bytes()))
            return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('selection')
    parser.add_argument('--selection-sha256', required=True)
    parser.add_argument('--configuration', required=True)
    parser.add_argument('--configuration-sha256', required=True)
    args = parser.parse_args(argv)
    try:
        result = Receiver().check(args.selection, args.selection_sha256, args.configuration, args.configuration_sha256)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        result = {'selection_consistent': False, 'coverage': 'incomplete', 'input_error': str(error),
                  'current_reliance': False, 'qualification_established': False,
                  'actual_producer_use_verified': False, 'native_observation_verified': False,
                  'publication_authority_authenticated': False, 'method_adoption_authenticated': False}
    print(json.dumps(result, indent=2))
    return 0 if result.get('selection_consistent') and result.get('coverage') == 'complete' else 1


if __name__ == '__main__':
    sys.exit(main())
