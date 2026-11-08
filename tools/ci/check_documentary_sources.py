#!/usr/bin/env python3
"""Always-on current documentary correspondence against execution authoring inputs.

Historical source profiles and frozen bytes are retained, not reselected here.
The projection implementation and selector extents are the existing Group B ones.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILES = (
    'app/examination/standalone/sources.terms-v1.json',
    'app/examination/standalone/pre_run_inputs.terms-v1.pins.json',
    'execution/PKG-09/DEL-09-01/Work/support-identity-v1/documentary-condition.v3.json',
)


def projections(root=ROOT):
    def walk(value, key=None):
        if isinstance(value, dict):
            if 'selectors' in value and 'sha256' in value:
                yield value.get('path', key), value
            for name, child in value.items():
                yield from walk(child, name)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)
    for name in PROFILES:
        for source, value in walk(json.loads((Path(root) / name).read_bytes())):
            if isinstance(source, str) and source.startswith('execution/'):
                yield source.replace('/Design/', '/Work/'), value


def projector(root=ROOT):
    path = Path(root) / 'app/examination/documentary_condition.py'
    spec = importlib.util.spec_from_file_location('_repository_documentary_projection', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.project


def check(root=ROOT):
    project = projector(root)
    groups, selectors = 0, 0
    for source, value in projections(root):
        actual = hashlib.sha256(project((Path(root) / source).read_bytes(), value['selectors'])).hexdigest()
        if actual != value['sha256'].removeprefix('sha256:'):
            raise ValueError('Current documentary correspondence changed: ' + source)
        groups += 1
        selectors += len(value['selectors'])
    return {'current_projection_groups': groups, 'selector_applications': selectors}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
