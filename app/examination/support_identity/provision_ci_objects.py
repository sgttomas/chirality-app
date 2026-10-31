"""Verify the reader's fixed local snapshot of original repository sources."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

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
    parser.parse_args()
    source = HERE / 'support_identity.py'
    revision = constant(source, 'DOCUMENTARY_SOURCE_COMMIT')
    declaration = checked_json(HERE / 'declaration.v1.json', constant(source, 'DECLARATION_SHA256'))
    objects = dict(declaration['sources'])
    for lock, consumer in [(HERE / 'canonical-pins.terms-v1.json', HERE / 'canonical.py'),
                           (HERE.parent / 'sq_receiving/pins.terms-v1.json', HERE.parent / 'sq_receiving/receive.py')]:
        pins = checked_json(lock, constant(consumer, 'PINS_SHA256'))
        for path, digest in pins['sources'].items():
            if path.endswith('.md'):
                if path in objects and objects[path] != digest:
                    raise ValueError('mixed original source identity: ' + path)
                objects[path] = digest
    size = 0
    for path, expected in objects.items():
        parts = path.split('/')
        if any(part in ('', '.', '..') for part in parts) or '\\' in path:
            raise ValueError('non-canonical frozen source path: ' + path)
        target = HERE / 'frozen'
        if target.is_symlink():
            raise ValueError('linked frozen source root')
        for part in parts:
            target = target / part
            if target.is_symlink():
                raise ValueError('linked frozen source: ' + path)
        data = target.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('fixed original source unavailable or different: ' + path)
        size += len(data)
    print(json.dumps({'fixed_source_commit': revision, 'verified_objects': len(objects), 'source_bytes': size}))


if __name__ == '__main__':
    main()
