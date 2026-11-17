"""Recompute current Codex 0.167.0 notice/source associations from retained inputs.

Offline and read-only. It reads the canonical 0.167.0 vendor tree, the frozen
0.160.0 tree, the committed root notice texts and retained public metadata
responses; it executes no supplier code, opens no network connection, acquires
nothing and draws no licence or compliance conclusion. Marker matches are byte
clues, not source joins. The 0.160.0 observe.py and its saved results remain the
historical record of that subject.
"""
import argparse
import hashlib
import importlib.util
import json
import mmap
import os
import re
import stat
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reader = _load('notice_input_reader', 'app/packaging/static_distribution/check.py')
inventory = _load('vendor_inventory', 'app/packaging/inventory.py')
require = reader.require

PIN = '0.167.0'
TAG = 'rust-v0.167.0'
COMMIT = '086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a'
CODEX_RS_TREE = 'c98bbd639c8f04c69cfd8495ba74996c06385dad'
CANONICAL_MANIFEST = '158dd67072236253a694ca06d9bf7bfdebbe20d4a197bbf675433cbdddea7e7b'
PREVIOUS_PIN = '0.160.0'
PREVIOUS_MANIFEST = '327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12'
PACKAGE_ASSET = ('codex-package-aarch64-apple-darwin.tar.gz', 166340155,
                 'sha256:af45ed45d940d7998809622c1c0296d3098ed7d7fad695284422c228bd454517')
STANDALONE_ASSETS = ('codex-code-mode-host-aarch64-apple-darwin.tar.gz',
                     'codex-exec-server-aarch64-apple-darwin.tar.gz')
RESPONSES = ('root-tree.json', 'third_party-tree.json', 'third_party-v8-tree.json',
             'codex-rs-tree-recursive.json', 'scripts-tree.json', 'scripts-codex_package-tree.json',
             'latest-release.json', 'release-tag-object.json')
# The supplier's root LICENSE and NOTICE, checked below against the rust-v0.167.0 tree (byte-equal to 0.160.0's).
ROOT_TEXTS = 'app/packaging/supplier_notices/codex'
# rg release selector files of Codex 0.160.0, kept as received beside this reader:
# name -> (size, SHA-256, Git blob SHA-1).
SELECTOR_DIR = 'app/packaging/supplier_notices/codex-0.160.0/scripts/codex_package'
SELECTOR_FILES = {
    'rg': (2592, '41a10ca63365560d899a82b6f825fd7b420a18b34f660a98bffeece77eeae1f1',
           '3b7c34843aaafe4cf26a87b3daf5806195d4bb0e'),
    'ripgrep.py': (862, 'c70947d6f7df1aa5daeca3d0fa48e65a32ee38b4f6b35694f87b2e65a4467e32',
                   '155c5d323ec60ba9fc2dfafd807145f8b26fb38b'),
}
_texts = _load('supplier_package_texts', 'app/packaging/notices/package_texts.py')
# The tree's executables, read from this pin's distribution record rather than listed by hand.
SUPPLIER_BINARIES = tuple(_texts.executables(
    reader.parse((ROOT / 'app/src-tauri/resources/supplier' / PIN / 'CANONICAL_DISTRIBUTION.json').read_bytes())))
# Exact byte patterns; a count of zero shows only that this pattern is absent.
MARKERS = {
    'codex-rs CI path': rb'/Users/runner/work/codex/codex/codex-rs/',
    'exec-server crate label': rb'codex-exec-server0\.167\.0',
    'exec-server source path': rb'exec-server/src/[a-z_/]+\.rs',
    'code-mode-host source path': rb'code-mode-host/src/main\.rs',
    'crates.io registry source path': rb'registry/src/index\.crates\.io-[0-9a-f]+/[A-Za-z0-9_.+-]+',
    'skill-creator sample': rb'name: skill-creator',
    'skill-installer sample': rb'name: skill-installer',
    'Apache appendix': rb'APPENDIX: How to apply the Apache License',
    'bwrap': rb'bwrap',
    'v8::internal': rb'v8::internal',
    'ICU data name': rb'icudt\d+l',
    'Unicode terms heading': rb'Unicode, Inc\. and others\. License & terms of use',
    'Chromium libc++ namespace': rb'NSt4__Cr',
    'ripgrep version and revision': rb'\(JIT is available\)\n\d+\.\d+\.\d+[0-9a-f]{10}',
    'PCRE2 Unicode version and PCRE2 version': rb'\x00\d+\.\d+\.\d+\x00\d+\.\d+ \d{4}-\d{2}-\d{2}\x00',
}
SHOWN = {'ICU data name', 'ripgrep version and revision', 'PCRE2 Unicode version and PCRE2 version',
         'exec-server crate label'}
LIMITS = [
    'No supplier execution, network access, acquisition, signature validation or legal conclusion.',
    'A blob/size identity or manifest declaration associates bytes with a source locator; it does not establish build equivalence, linked contents or notice applicability.',
    'Marker counts are byte clues in exact binaries. Absent patterns do not show absent code.',
]


def blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def read(path):
    raw, digest, size = reader.transfer(Path(path).absolute(), retain=True)
    return raw, digest, size


def received_selector(name, directory=None):
    """Read one received 0.160.0 selector file and refuse it unless its bytes carry the recorded identity."""
    raw, digest, size = read(Path(directory or ROOT / SELECTOR_DIR) / name)
    require((size, digest, blob(raw)) == SELECTOR_FILES[name], 'received Codex selector changed: ' + name)
    return raw, digest, size


def response(directory, name):
    raw, digest, size = read(Path(directory) / name)
    return reader.parse(raw), {'name': name, 'sha256': digest, 'size': size}


def files(vendor, expected_manifest):
    scanned = inventory.scan(vendor)
    require(scanned['manifest_sha256'] == expected_manifest, 'vendor manifest mismatch: ' + str(vendor))
    return {e['path']: e for e in scanned['entries'] if e['kind'] == 'file'}


def signature_range(raw):
    require(struct.unpack_from('<I', raw, 0)[0] == 0xfeedfacf, 'thin arm64 Mach-O required')
    count = struct.unpack_from('<I', raw, 16)[0]
    offset, found = 32, None
    for _ in range(count):
        command, size = struct.unpack_from('<II', raw, offset)
        if command == 0x1d:
            found = struct.unpack_from('<II', raw, offset + 8)
        offset += size
    require(found is not None, 'code-signature load command absent')
    return found


def markers(path, expected_sha256):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        metadata = os.fstat(fd)
        require(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1, 'invalid supplier file')
        with mmap.mmap(fd, 0, access=mmap.ACCESS_READ) as view:
            require(hashlib.sha256(view).hexdigest() == expected_sha256, 'supplier subject digest mismatch')
            rows = []
            for label, pattern in MARKERS.items():
                count, first, sample, distinct = 0, None, None, set()
                for match in re.finditer(pattern, view):
                    count += 1
                    if first is None:
                        first, sample = match.start(), match.group()
                    if label == 'crates.io registry source path':
                        distinct.add(match.group().rsplit(b'/', 1)[1])
                row = {'marker': label, 'pattern_hex': pattern.hex(), 'count': count, 'first_offset': first}
                if label in SHOWN and sample is not None:
                    row['first_match_hex'] = sample.hex()
                if distinct:
                    row['distinct_crate_directories'] = len(distinct)
                rows.append(row)
    finally:
        os.close(fd)
    return rows


def build(vendor, previous_vendor, metadata):
    current = files(vendor, CANONICAL_MANIFEST)
    previous = files(previous_vendor, PREVIOUS_MANIFEST)
    loaded = {name: response(metadata, name) for name in RESPONSES}
    root_tree, third_party, v8_tree, codex_rs, scripts, codex_package, release, tag = (
        loaded[name][0] for name in RESPONSES)

    require(tag['tag'] == TAG and tag['object'] == {**tag['object'], 'sha': COMMIT, 'type': 'commit'},
            'release tag does not name the selected commit')
    require(release['tag_name'] == TAG, 'release metadata is for another tag')
    assets = {a['name']: a for a in release['assets']}
    package = assets[PACKAGE_ASSET[0]]
    require((package['size'], package['digest']) == PACKAGE_ASSET[1:], 'canonical package asset identity changed')

    require(root_tree['sha'] == COMMIT and not root_tree['truncated'], 'root tree response is not the selected commit')
    top = {e['path']: e for e in root_tree['tree']}
    require(top['codex-rs']['sha'] == CODEX_RS_TREE, 'codex-rs subtree changed')
    require(codex_rs['sha'] == CODEX_RS_TREE and not codex_rs['truncated'], 'recursive codex-rs tree incomplete')
    require(third_party['sha'] == top['third_party']['sha'] and not third_party['truncated'], 'third_party tree mismatch')
    third = {e['path']: e for e in third_party['tree']}
    require(v8_tree['sha'] == third['v8']['sha'] and not v8_tree['truncated'], 'third_party/v8 tree mismatch')
    require(scripts['sha'] == top['scripts']['sha'] and not scripts['truncated'], 'scripts tree mismatch')
    package_scripts = {e['path']: e for e in scripts['tree']}
    require(codex_package['sha'] == package_scripts['codex_package']['sha'] and not codex_package['truncated'],
            'scripts/codex_package tree mismatch')
    selector_entries = {e['path']: e for e in codex_package['tree']}
    selectors = []
    for name in SELECTOR_FILES:
        raw, digest, size = received_selector(name)
        entry = selector_entries[name]
        selectors.append({'path': 'scripts/codex_package/' + name, 'size_bytes': entry['size'],
                          'git_blob_sha1': entry['sha'], 'received_0160_sha256': digest,
                          'equals_received_0160_text': entry['sha'] == blob(raw) and entry['size'] == size})

    root_notices = []
    for name in ('LICENSE', 'NOTICE'):
        raw, digest, size = read(ROOT / ROOT_TEXTS / name)
        entry = top[name]
        require(entry['type'] == 'blob' and entry['size'] == size and entry['sha'] == blob(raw),
                'retained root text differs from the selected commit: ' + name)
        root_notices.append({'path': name, 'local_text': ROOT_TEXTS + '/' + name, 'size_bytes': size,
                             'sha256': digest, 'git_blob_sha1': entry['sha']})

    manifest_raw, manifest_sha, _ = read(Path(vendor) / 'codex-resources/voice/manifest.json')
    manifest = reader.parse(manifest_raw)
    require(manifest_sha == current['codex-resources/voice/manifest.json']['sha256'], 'voice manifest changed')
    require(manifest['buildCommit'] == COMMIT and manifest['appVersion'] == PIN, 'voice manifest declares another build')
    for path, digest in manifest['sha256'].items():
        require(current[path]['sha256'] == digest, 'manifest-bound file differs: ' + path)

    old_rg, _, _ = read(Path(previous_vendor) / 'codex-path/rg')
    new_rg, new_rg_sha, _ = read(Path(vendor) / 'codex-path/rg')
    require(new_rg_sha == current['codex-path/rg']['sha256'], 'rg changed during read')
    old_sig, new_sig = signature_range(old_rg), signature_range(new_rg)

    components = []
    for path in SUPPLIER_BINARIES:
        entry = current[path]
        components.append({'path': path, 'sha256': entry['sha256'], 'size': entry['size'],
                           'manifest_bound_to_commit': path in manifest['sha256'],
                           'previous_sha256': previous.get(path, {}).get('sha256'),
                           'markers': markers(Path(vendor) / path, entry['sha256'])})

    same = sorted(p for p in current.keys() & previous.keys() if current[p]['sha256'] == previous[p]['sha256'])
    changed = sorted(p for p in current.keys() & previous.keys() if current[p]['sha256'] != previous[p]['sha256'])
    selected = sorted((e for e in codex_rs['tree'] if e['type'] == 'blob'
                       and (e['path'] in ('Cargo.lock', 'Cargo.toml') or e['path'].endswith('/Cargo.toml'))),
                      key=lambda e: e['path'])
    proposal_files = [{'path': 'codex-rs/' + e['path'], 'size_bytes': e['size'], 'git_blob_sha1': e['sha'],
                       'url': f"https://raw.githubusercontent.com/openai/codex/{COMMIT}/codex-rs/{e['path']}"}
                      for e in selected]
    associations = {
        'format': 'codex-notice-source-associations/1',
        'supplier_pin': PIN, 'target': 'aarch64-apple-darwin',
        'tool_sha256': reader.sha(Path(__file__).read_bytes()),
        'inputs': {'canonical_vendor_manifest_sha256': CANONICAL_MANIFEST,
                   'previous_vendor': {'pin': PREVIOUS_PIN, 'manifest_sha256': PREVIOUS_MANIFEST},
                   'retained_responses': [loaded[name][1] for name in RESPONSES]},
        'source': {'repository': 'https://github.com/openai/codex', 'tag': TAG, 'tag_object': tag['sha'],
                   'commit': COMMIT, 'codex_rs_tree': CODEX_RS_TREE,
                   'package_asset': {'name': PACKAGE_ASSET[0], 'size': PACKAGE_ASSET[1], 'digest': PACKAGE_ASSET[2]}},
        'voice_manifest': {'sha256': manifest_sha, 'buildCommit': COMMIT, 'bound_paths': sorted(manifest['sha256'])},
        'root_notice_association': root_notices,
        'inventory_delta': {'unchanged': same, 'changed': changed,
                            'removed': sorted(previous.keys() - current.keys()),
                            'added': sorted(current.keys() - previous.keys())},
        'rg_release_selector': selectors,
        'rg_previous_comparison': {
            'size': [len(old_rg), len(new_rg)], 'signature_range': [list(old_sig), list(new_sig)],
            'bytes_before_signature_equal': old_sig == new_sig and old_rg[:old_sig[0]] == new_rg[:new_sig[0]]},
        'supplier_binaries': components,
        'v8_third_party': [{'path': 'third_party/v8/' + e['path'], 'size_bytes': e['size'], 'git_blob_sha1': e['sha']}
                           for e in v8_tree['tree'] if e['path'].startswith('rusty_v8_')],
        'standalone_release_assets': [{'name': n, 'size': assets[n]['size'], 'digest': assets[n]['digest']}
                                      for n in STANDALONE_ASSETS],
        'limits': LIMITS,
    }
    proposal = {
        'format': 'codex-source-graph-acquisition-proposal/1',
        'repository': 'https://github.com/openai/codex', 'commit': COMMIT, 'codex_rs_tree': CODEX_RS_TREE,
        'selection': 'codex-rs/Cargo.lock and every codex-rs/**/Cargo.toml blob in the complete recursive codex-rs tree',
        'files': proposal_files, 'file_count': len(proposal_files),
        'total_bytes': sum(f['size_bytes'] for f in proposal_files),
        'standing': 'Public source-text read list (standing read-only inspection authority). A row is held only after its bytes are read and match size and Git blob. No dependency archive or binary acquisition, source graph resolution, binary join or notice coverage follows from this list.',
    }
    return {'associations.json': associations, 'source-graph-proposal.json': proposal}


def render(value):
    return json.dumps(value, indent=1, sort_keys=False) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vendor')
    parser.add_argument('previous_vendor')
    parser.add_argument('metadata', help='directory holding the retained public metadata responses')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', metavar='DIR')
    mode.add_argument('--check', metavar='DIR')
    args = parser.parse_args()
    outputs = build(args.vendor, args.previous_vendor, args.metadata)
    target = Path(args.write or args.check)
    for name, value in outputs.items():
        if args.write:
            (target / name).write_text(render(value))
        else:
            require((target / name).read_text() == render(value), 'retained record differs: ' + name)
    print(json.dumps({n: reader.sha(render(v).encode()) for n, v in outputs.items()}))
