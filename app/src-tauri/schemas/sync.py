#!/usr/bin/env python3
"""Verify maintained schema copies against their source mapping; --sync updates copies.

Run from any directory, offline. A source update requires reviewed contract adoption;
this helper only copies bytes and records hashes, it supplies no acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sync', action='store_true')
parser.add_argument('--catalog-adapter', action='store_true',
                    help='Use the separately maintained catalog/receiving resource manifest')
parser.add_argument('--runtime-core', action='store_true', help='Use the current runtime resource source map')
parser.add_argument('--resource', help='Select one runtime resource for bounded current derivation')
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[2]
if args.runtime_core:
    directory = here.parent / 'resources/runtime_core'
    path = directory / 'MANIFEST.json'
    manifest = json.loads(path.read_text())
    rows = [r for r in manifest['resources'] if args.resource is None or r['file'] == args.resource]
    if not rows:
        parser.error('runtime resource is not in the maintained source map')
    for row in rows:
        logical = row['source'].removeprefix('projects/chirality-app-v4/').replace('/Design/', '/Work/')
        source = (root / logical.replace('execution/', 'app/contract_inputs/', 1)).read_bytes()
        copied = directory / row['file']
        digest = hashlib.sha256(source).hexdigest()
        if args.sync:
            copied.write_bytes(source)
            row['sha256'] = row['sourceSha256'] = digest
            row['standing'] = 'maintained current source schema'
        else:
            assert copied.read_bytes() == source, f"runtime copy mismatch: {row['file']}"
            assert row['sha256'] == row['sourceSha256'] == digest, f"runtime source hash mismatch: {row['source']}"
    if args.sync:
        path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f"{len(rows)} runtime resources match selected source bytes and hashes")
    raise SystemExit(0)
if args.catalog_adapter:
    directory = here.parent / 'resources/catalog_adapter'
    path = directory / 'manifest.json'
    selected = json.loads(path.read_text())
    for row in selected:
        logical = row['source'].removeprefix('projects/chirality-app-v4/').replace('/Design/', '/Work/')
        source = (root / logical.replace('execution/', 'app/contract_inputs/', 1)).read_bytes()
        copied = directory / row['file']
        digest = hashlib.sha256(source).hexdigest()
        if args.sync:
            copied.write_bytes(source)
            row['sha256'] = digest
        else:
            assert copied.read_bytes() == source, f"catalog/receiving copy mismatch: {row['file']}"
            assert digest == row['sha256'], f"catalog/receiving source hash mismatch: {row['source']}"
    if args.sync:
        path.write_text(json.dumps(selected, indent=2) + '\n')
    print(f"{len(selected)} catalog/receiving resources match selected source bytes and hashes")
    raise SystemExit(0)
manifest_path = here / 'manifest.json'
manifest = json.loads(manifest_path.read_text())
for row in manifest['resources']:
    source = (root / row['source'].replace('execution/', 'app/contract_inputs/', 1)).read_bytes()
    copied = here / row['file']
    digest = hashlib.sha256(source).hexdigest()
    if args.sync:
        copied.write_bytes(source)
        row['sha256'] = digest
        row['id'] = json.loads(source)['$id']
    else:
        assert copied.read_bytes() == source, f"schema copy mismatch: {row['file']}"
        assert digest == row['sha256'], f"source hash mismatch: {row['source']}"
        assert json.loads(source)['$id'] == row['id'], f"schema ID mismatch: {row['file']}"
for row in manifest.get('file_fixtures', []):
    source = (root / row['source'].replace('execution/', 'app/contract_inputs/', 1)).read_bytes()
    copied = here / row['file']
    digest = hashlib.sha256(source).hexdigest()
    if args.sync:
        copied.write_bytes(source)
        row['sha256'] = digest
    else:
        assert copied.read_bytes() == source, f"fixture copy mismatch: {row['file']}"
        assert digest == row['sha256'], f"fixture source hash mismatch: {row['source']}"
fixture = manifest['fixture']
entries = []
for row in fixture['sources']:
    source = (root / row['source'].replace('execution/', 'app/contract_inputs/', 1)).read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    if args.sync:
        row['sha256'] = digest
    else:
        assert digest == row['sha256'], f"fixture source hash mismatch: {row['source']}"
    entries.extend(json.loads(line) for line in source.decode().splitlines() if line)
fixture_path = here / fixture['file']
if args.sync:
    fixture_path.write_text(json.dumps(entries, indent=2) + '\n')
else:
    assert json.loads(fixture_path.read_text()) == entries, 'maintained fixture mismatch'
if args.sync:
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print(f"{len(manifest['resources'])} schema resources match source bytes, hashes and declared IDs")
