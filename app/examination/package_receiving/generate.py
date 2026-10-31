#!/usr/bin/env python3
"""Derive only the new package receiving profile and SQ successor closure."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
E = 'app/examination/'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def write(path, value):
    (ROOT / path).write_bytes(encode(value))


def constant(path, value):
    target = ROOT / path
    text, count = re.subn(r"PINS_SHA256 = '[0-9a-f]{64}'", "PINS_SHA256 = '" + value + "'", target.read_text())
    if count != 1:
        raise ValueError('expected one reader pin constant: ' + path)
    target.write_text(text)


def main():
    path = ROOT / 'app/packaging/successor/check.py'
    spec = importlib.util.spec_from_file_location('_package_producer_generation', path)
    producer = importlib.util.module_from_spec(spec); spec.loader.exec_module(producer)
    dependencies = producer.source_dependencies()
    producer_sources = sorted(dependencies)
    for relative, expected in dependencies.items():
        if sha((ROOT / relative).read_bytes()) != expected:
            raise ValueError('producer source changed during generation: ' + relative)
    for relative in (E + 'support_identity/canonical.py', E + 'support_identity/canonical-pins.terms-v1.json'):
        dependencies[relative] = sha((ROOT / relative).read_bytes())
    profile = {'format': 'exp-package-s4-receiving/1', 'producer_format': 'packaged-s4-binding/1',
               'producer_report': 'packaged-s4-check/1', 'producer_sources': producer_sources,
               'sources': dict(sorted(dependencies.items())),
               'standing': 'explicit source/relationship selection; no release or live authority'}
    profile_path = E + 'package_receiving/sources.package-v1.json'
    write(profile_path, profile)
    constant(E + 'package_receiving/adapter.py', sha((ROOT / profile_path).read_bytes()))
    original = ROOT / (E + 'sq_receiving/pins.terms-v1.json')
    pins = json.loads(original.read_bytes())
    pins['format'] = 'sq-package-s4-reader-pins/1'
    pins['predecessor'] = {'path': E + 'sq_receiving/pins.terms-v1.json', 'sha256': sha(original.read_bytes())}
    pins['package_source_profile'] = {'path': profile_path, 'sha256': sha((ROOT / profile_path).read_bytes())}
    pins['sources'].pop(E + 'sq_receiving/worker.py')
    additions = dict(dependencies)
    for relative in (profile_path, E + 'package_receiving/adapter.py', E + 'sq_receiving/worker_packages.py'):
        additions[relative] = sha((ROOT / relative).read_bytes())
    for relative, expected in additions.items():
        if relative in pins['sources'] and pins['sources'][relative] != expected:
            raise ValueError('conflicting legacy/successor source, do not repin silently: ' + relative)
        pins['sources'][relative] = expected
    path = E + 'sq_receiving/pins.packages-v1.json'
    write(path, pins)
    constant(E + 'sq_receiving/receive_packages.py', sha((ROOT / path).read_bytes()))


if __name__ == '__main__':
    main()
