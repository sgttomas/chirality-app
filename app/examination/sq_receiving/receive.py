#!/usr/bin/env python3
"""Fixed-source SQ file receiving. No examination or qualification is performed."""
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
PINS_SHA256 = 'c2e2f6f90634d4f33beeb1441a21767cf3eced14d4c63d0a3223acc334e30068'


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
                data = source_reader.publication_source(PROJECT, name, expected) if name.endswith('.md') else read_relative(PROJECT, name)
            if sha(data) != expected:
                raise ValueError('selected source changed: ' + name)
            self.sources[name] = data
        original_declaration = source_reader.parse(self.sources['app/examination/support_identity/declaration.v1.json'])
        self.original_sources = {name: source_reader.frozen_publication_source(PROJECT, name, digest)
                                 for name, digest in original_declaration['sources'].items()}
        self.original_sources.update({name: data for name, data in self.sources.items() if name.endswith('.md')})

    def check(self, selection, digest):
        selected_raw = read_relative(Path(selection).absolute().parent, Path(selection).name)
        if sha(selected_raw) != digest:
            raise ValueError('selection digest mismatch')
        purpose = self.source_reader.parse(selected_raw)['purpose']
        if purpose not in ('current_producer_declaration', 'historical_correspondence'):
            raise ValueError('unsupported purpose')
        current_documents = {}
        source_condition = {'method': 'original-frozen-source/v1',
                            'standing': 'original full-byte correspondence; current documentary meaning not checked',
                            'authority_authenticated': False}
        if purpose == 'current_producer_declaration':
            path = 'app/examination/documentary_condition.py'
            spec = importlib.util.spec_from_file_location('_sq_documentary_condition', PROJECT / path)
            module = importlib.util.module_from_spec(spec)
            exec(compile(self.sources[path], str(PROJECT / path), 'exec'), module.__dict__)
            manifest = self.sources['execution/PKG-09/DEL-09-01/Design/support-identity-v1/documentary-condition.v2.json']
            current_documents, source_condition = module.Condition(PROJECT, manifest, read_relative).capture('sq')
        # Run only captured, pinned Python validators in a private source snapshot.
        # This is not native execution or hostile-filesystem custody.
        with tempfile.TemporaryDirectory(prefix='sq-receiving-') as temp:
            root = Path(temp)
            for name, data in self.sources.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            for name, data in current_documents.items():
                target = root / 'current-documentary-inputs' / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            for name, data in self.original_sources.items():
                target = root / 'original-support' / name
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
            report['source_condition'] = source_condition
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
