"""Successor-only phase A admission around the maintained native A controller.

No supplier execution or relaunch. The explicit identified build and invented
inputs are checked before binding a private import of the existing controller.
No historical namespace is reused or deleted. A failed launch's namespace
metadata is retained; this first-launch adapter does not automatically retry it.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
from datetime import datetime

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve()
REPO = HERE.parents[4]
T3 = Path('/Users/ryan/dev/chirality-t3')
BASE = HERE.with_name('native_setup_continuation.py')
OLD_IDENTIFIER = 'dev.chirality.app-v4.candidate.20261029-ukt5ir80'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(path, directory=False):
    metadata = path.lstat()
    require((stat.S_ISDIR if directory else stat.S_ISREG)(metadata.st_mode),
            'not a plain ' + ('directory: ' if directory else 'file: ') + str(path))
    require(path.resolve() == path, 'linked path ancestry: ' + str(path))


def load_base():
    spec = importlib.util.spec_from_file_location('successor_phase_A_base', BASE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Context:
    def __init__(self, build_root, record, inputs):
        # Canonical locations let the existing, reviewed execute path perform
        # its full prelaunch candidate inventory without replacing that check.
        self.build_root = Path(build_root).absolute()
        self.record_path = Path(record).absolute()
        self.inputs_path = Path(inputs).absolute()
        plain(self.build_root, directory=True)
        require(self.build_root.is_relative_to(T3 / 'scratch'), 'build root outside task scratch')
        require(self.record_path == self.build_root / 'identified/candidate-identification.json',
                'record must be the identified build record')
        require(self.inputs_path == self.build_root / 'witness-inputs/input-manifest.json',
                'inputs must be the explicit build witness manifest')
        self.preparation_path = self.build_root / 'preparation.json'
        for path in (self.record_path, self.inputs_path, self.preparation_path):
            plain(path)
        self.file_digests = {str(path): digest(path) for path in
                             (self.record_path, self.inputs_path, self.preparation_path)}
        identified = json.loads(self.record_path.read_text())
        prepared = json.loads(self.preparation_path.read_text())
        self.identifier = identified['bundle']['identifier']
        require(re.fullmatch(r'dev\.chirality\.app-v4\.candidate\.[A-Za-z0-9-]+', self.identifier)
                and self.identifier != OLD_IDENTIFIER, 'not a distinct successor namespace')
        require(identified['format'] == 'chirality.app-v4.candidate-identification/v3'
                and identified['route'] == 'native_development'
                and identified['app_candidate']['packaged'] is False,
                'not an identified development candidate')
        require(identified['source']['revision'] == prepared['revision']
                == identified['app_candidate']['revision'], 'successor source mismatch')
        require(prepared['identifier'] == self.identifier
                and prepared['configuration']['identifier'] == self.identifier
                and prepared['root'] == str(self.build_root)
                and identified['bundle']['name'] == prepared['configuration']['productName'] + '.app',
                'successor build namespace mismatch')
        require(identified['supplier']['bundled'] is True
                and identified['supplier']['pin'] == '0.160.0'
                and identified['supplier']['standing'] == 'unqualified-development',
                'unexpected supplier standing')
        self.identified = identified
        self.prepared = prepared

    def descriptor(self):
        return {'build_root': str(self.build_root), 'record': str(self.record_path),
                'inputs': str(self.inputs_path), 'files': self.file_digests}

    @classmethod
    def restore(cls, descriptor):
        context = cls(descriptor['build_root'], descriptor['record'], descriptor['inputs'])
        require(context.file_digests == descriptor['files'], 'admission source changed')
        return context

    def inputs(self):
        for name, expected in self.file_digests.items():
            plain(Path(name))
            require(digest(Path(name)) == expected, 'admission source changed: ' + name)
        value = json.loads(self.inputs_path.read_text())
        identified = self.identified
        bundle = self.build_root / 'target/debug/bundle/macos' / identified['bundle']['name']
        executable = bundle / identified['bundle']['executable']['path']
        require(value['candidate_key'] == identified['candidate_key']
                and value['bundle_identifier'] == self.identifier
                and value['bundle'] == str(bundle) and value['executable'] == str(executable)
                and value['executable_sha256'] == identified['bundle']['executable']['sha256'],
                'manifest differs from identified successor')
        require(value['expected_app_data'] == str(Path.home() / 'Library/Application Support' / self.identifier),
                'App-data path differs from successor identifier')
        fixture = self.inputs_path.parent
        paths = value['native_input_paths']
        require(set(paths) == {'shared_config', 'shared_agents', 'shared_skills', 'project'}, 'unexpected native input keys')
        expected_paths = {'shared_config': fixture / 'shared/config.toml',
                          'shared_agents': fixture / 'shared/AGENTS.md',
                          'shared_skills': fixture / 'shared/skills', 'project': fixture / 'project'}
        require(paths == {key: str(path) for key, path in expected_paths.items()},
                'native inputs outside new invented fixture')
        for key, path in expected_paths.items():
            directory = key in ('shared_skills', 'project')
            plain(path, directory=directory)
            if directory:
                require(not list(path.iterdir()), 'fixture directory not empty: ' + key)
            else:
                name = str(path.relative_to(fixture))
                require(value['files'].get(name) == digest(path), 'invented input changed: ' + key)
        for name, expected in value['files'].items():
            path = fixture / name
            require(path.is_relative_to(fixture) and '..' not in Path(name).parts,
                    'fixture manifest path escapes root')
            plain(path)
            require(digest(path) == expected, 'fixture file changed: ' + name)
        # No inherited or caller-supplied startup, provider, auth or project
        # environment. Setup is performed only through the native form.
        expected_env = {'HOME': str(Path.home()),
                        'PATH': str(bundle / 'Contents/Resources/codex/codex-path') + ':/usr/bin:/bin:/usr/sbin:/sbin',
                        'LANG': 'en_US.UTF-8', 'CODEX_HOME': str(fixture / 'fallback-codex-home'),
                        'TMPDIR': str(fixture / 'tmp')}
        require(value['environment'] == expected_env, 'unexpected launch environment')
        return copy.deepcopy(value)

    def namespaces(self, require_absent=True):
        result = {}
        for name, relative in [('AppData', 'Library/Application Support'),
                               ('WebKit', 'Library/WebKit'), ('Caches', 'Library/Caches')]:
            path = Path.home() / relative / self.identifier
            require(path.parent.resolve() == path.parent, 'linked namespace ancestry: ' + name)
            present = os.path.lexists(path)
            require(not (require_absent and present),
                    'successor namespace already exists; preserve state, no automatic retry: ' + name)
            entry = {'path': str(path), 'present': present}
            if present:
                # Metadata only, no traversal through links and no content read.
                info = path.lstat()
                entry['root'] = [info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns]
                rows = []
                for parent, dirs, files in (os.walk(path, followlinks=False) if stat.S_ISDIR(info.st_mode) else []):
                    for item in [Path(parent), *[Path(parent) / n for n in sorted(files + dirs)]]:
                        info = item.lstat()
                        rows.append([str(item.relative_to(path)), info.st_dev, info.st_ino,
                                     info.st_mode, info.st_size, info.st_mtime_ns])
                    require(len(rows) < 4000, 'namespace metadata exceeds bound')
                entry['metadata'] = rows
            result[name] = entry
        return result

    def bind(self):
        module = load_base()
        module.RETAINED = self.build_root
        module.IDENTIFIER = self.identifier
        module.inputs = self.inputs
        module.namespaces = self.namespaces
        # A.execute's prepared-controller check now binds the adapter source;
        # dependency checks below independently bind the unchanged A body.
        module.__file__ = str(HERE)
        return module


def dependency_digests():
    module = load_base()
    return {str(path): digest(path) for path in
            (BASE, module.RAW, REPO / 'app/examination/candidate_identity/identify.py',
             REPO / 'app/examination/candidate_identity/bundled_supplier.py',
             REPO / 'execution/PKG-09/DEL-09-01/Work/candidate-identity-v3/candidate-identification.schema.json')}


def policy(executable):
    return ('(version 1)\n(allow default)\n(deny network*)\n'
            '(deny file-read* (subpath ' + json.dumps(str(Path.home() / '.codex')) + '))\n'
            '(deny file-write* (subpath ' + json.dumps(str(Path.home() / '.codex')) + '))\n'
            '(deny process-fork)\n(deny process-exec)\n'
            '(allow process-exec (literal ' + json.dumps(executable) + '))\n')


def prepare(context):
    value = context.inputs()
    namespaces = context.namespaces()
    module = context.bind()
    root = Path(tempfile.mkdtemp(prefix='app-successor-native-A-', dir=T3 / 'scratch')).resolve()
    for name in ('codex-home', 'tmp'):
        (root / name).mkdir(mode=0o700)
    value['environment']['CODEX_HOME'] = str(root / 'codex-home')
    value['environment']['TMPDIR'] = str(root / 'tmp')
    rules = policy(value['executable'])
    (root / 'phase-A.sb').write_text(rules)
    (root / 'controller.py.txt').write_bytes(HERE.read_bytes())
    (root / 'base-controller.py.txt').write_bytes(BASE.read_bytes())
    module.write(root / 'admission.json', {'context': context.descriptor(), 'inputs': value,
                 'namespaces': namespaces, 'policy_sha256': module.sha(rules.encode()),
                 'controller_sha256': digest(HERE), 'dependency_sha256': dependency_digests(),
                 'prepared_at': module.now()})
    print(root)
    return root


def execute(root, window_end):
    plain(root, directory=True)
    require(root.is_relative_to(T3 / 'scratch'), 'attempt outside task scratch')
    record = json.loads((root / 'admission.json').read_text())
    require(record['dependency_sha256'] == dependency_digests(), 'controller dependency changed')
    context = Context.restore(record['context'])
    module = context.bind()
    expected = context.inputs()
    expected['environment']['CODEX_HOME'] = str(root / 'codex-home')
    expected['environment']['TMPDIR'] = str(root / 'tmp')
    require(record['inputs'] == expected, 'prepared launch inputs differ')
    require(90 < window_end - time.time() <= 300, 'invalid successor resource interval')
    # The exact generated policy is checked in addition to its saved digest.
    require((root / 'phase-A.sb').read_text() == policy(context.inputs()['executable']), 'phase-A policy differs')
    try:
        return module.execute(root, window_end)
    finally:
        try:
            module.write(root / 'namespace-after.json', context.namespaces(require_absent=False))
        except BaseException as error:
            module.write(root / 'namespace-after-error.json', {'error': str(error),
                         'standing': 'namespace metadata incomplete; no retry or cleanup authorized'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--build-root', type=Path)
    parser.add_argument('--record', type=Path)
    parser.add_argument('--inputs', type=Path)
    parser.add_argument('--execute', type=Path)
    parser.add_argument('--window-end')
    args = parser.parse_args()
    if args.prepare and args.build_root and args.record and args.inputs and not args.execute:
        prepare(Context(args.build_root, args.record, args.inputs))
    elif args.execute and args.window_end and not any((args.prepare, args.build_root, args.record, args.inputs)):
        sys.exit(execute(args.execute.absolute(), datetime.fromisoformat(args.window_end).timestamp()))
    else:
        parser.error('use --prepare --build-root ROOT --record RECORD --inputs MANIFEST, or --execute ATTEMPT --window-end UTC')
