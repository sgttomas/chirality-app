"""Explicit CI provisioning of the reader's fixed repository source objects."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]


def constant(path, name):
    for node in ast.parse(path.read_bytes()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError('missing fixed reader constant: ' + name)


def checked_json(path, expected):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('source lock differs: ' + path.name)
    return json.loads(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true', help='Explicitly fetch the fixed commit and missing blobs from origin')
    args = parser.parse_args()
    source = HERE / 'support_identity.py'
    revision = constant(source, 'DOCUMENTARY_SOURCE_COMMIT')
    declaration = checked_json(HERE / 'declaration.v1.json', constant(source, 'DECLARATION_SHA256'))
    objects = dict(declaration['sources'])
    for lock, consumer in [(HERE / 'canonical-pins.v1.json', HERE / 'canonical.py'),
                           (HERE.parent / 'sq_receiving/pins.json', HERE.parent / 'sq_receiving/receive.py')]:
        pins = checked_json(lock, constant(consumer, 'PINS_SHA256'))
        for path, digest in pins['sources'].items():
            if path.endswith('.md'):
                if path in objects and objects[path] != digest:
                    raise ValueError('mixed original source identity: ' + path)
                objects[path] = digest
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
    if args.fetch:
        env.pop('GIT_NO_LAZY_FETCH', None)
        subprocess.run(['git', 'fetch', '--depth=1', '--filter=blob:none', '--no-tags', 'origin', revision],
                       cwd=PROJECT, env=env, check=True, timeout=120)
    else:
        env['GIT_NO_LAZY_FETCH'] = '1'
    size = 0
    for path, expected in objects.items():
        result = subprocess.run(['git', 'cat-file', 'blob', revision + ':projects/chirality-app-v4/' + path],
                                cwd=PROJECT, env=env, capture_output=True, timeout=30)
        if result.returncode or hashlib.sha256(result.stdout).hexdigest() != expected:
            raise ValueError('fixed original source unavailable or different: ' + path)
        size += len(result.stdout)
    print(json.dumps({'fixed_source_commit': revision, 'verified_objects': len(objects), 'source_bytes': size}))


if __name__ == '__main__':
    main()
