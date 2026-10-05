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
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[4]
manifest_path = here / 'manifest.json'
manifest = json.loads(manifest_path.read_text())
for row in manifest['resources']:
    source = (root / row['source']).read_bytes()
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
    source = (root / row['source']).read_bytes()
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
    source = (root / row['source']).read_bytes()
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
