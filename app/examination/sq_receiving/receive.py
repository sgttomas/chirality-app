#!/usr/bin/env python3
"""Fixed-source SQ file receiving. No examination or qualification is performed."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PINS_SHA256 = '2ac5c1edb612985846bc265355c41d90510bf8b98631e84371dde33b628af205'


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
        raw = read_relative(HERE, 'pins.json')
        if sha(raw) != PINS_SHA256:
            raise ValueError('SQ reader pins changed')
        self.pins = json.loads(raw)
        self.sources = {}
        for name, expected in self.pins['sources'].items():
            data = read_relative(PROJECT, name)
            if sha(data) != expected:
                raise ValueError('selected source changed: ' + name)
            self.sources[name] = data

    def check(self, selection, digest):
        # Run only captured, pinned Python validators in a private source snapshot.
        # This is not native execution or hostile-filesystem custody.
        with tempfile.TemporaryDirectory(prefix='sq-receiving-') as temp:
            root = Path(temp)
            for name, data in self.sources.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            (root / 'reader-pins.json').write_text(json.dumps(self.pins))
            job = subprocess.run([sys.executable, '-B', str(root / 'app/examination/sq_receiving/worker.py'),
                                  str(Path(selection).absolute()), digest],
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
    args = parser.parse_args(argv)
    try:
        result = Receiver().check(args.selection, args.selection_sha256)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        result = {'selection_consistent': False, 'coverage': 'incomplete', 'input_error': str(error),
                  'current_reliance': False, 'qualification_established': False,
                  'actual_producer_use_verified': False, 'native_observation_verified': False,
                  'publication_authority_authenticated': False, 'method_adoption_authenticated': False}
    print(json.dumps(result, indent=2))
    return 0 if result.get('selection_consistent') and result.get('coverage') == 'complete' else 1


if __name__ == '__main__':
    sys.exit(main())
