"""Recompute the Codex 0.167.0 rg -> ripgrep 15.2.0 source-text association offline.

Reads the canonical 0.167.0 rg binary, the received Codex rg release selector,
the committed ripgrep licence texts and retained ripgrep public metadata/source
text. Executes nothing, opens no network connection and draws no licence or
compliance conclusion. Version, revision and crate-path strings are clues; they
do not join the shipped binary to the selected release archive.
"""
import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('notice_input_reader', ROOT / 'app/packaging/static_distribution/check.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
require = reader.require

RG_SHA256 = '13424ef22134a65a211e490475bc17a4671e4fad3c82ad4c613fe5978f022a6d'
SELECTOR = 'execution/PKG-01/DEL-01-06/Work/supplier-notice-associations/approved-receipt-20261102/sources/codex/scripts/codex_package/rg'
SELECTOR_BLOB = '3b7c34843aaafe4cf26a87b3daf5806195d4bb0e'
ARCHIVE_URL = 'https://github.com/BurntSushi/ripgrep/releases/download/15.2.0/ripgrep-15.2.0-aarch64-apple-darwin.tar.gz'
TAG, TAG_OBJECT = '15.2.0', '6ec72defacfb042f203ca0b4bf2513a0a5505a7e'
COMMIT = 'e89fff89ac9af12e8d4ce9d5fd07beb408ca730f'
TEXTS = 'app/packaging/supplier_notices/ripgrep-15.2.0'
LICENCE_FILES = ('COPYING', 'LICENSE-MIT', 'UNLICENSE')
RESPONSES = ('ripgrep-ref-tag.json', 'ripgrep-tag-object.json', 'ripgrep-root-tree.json')
LIMITS = [
    'No execution, network access, acquisition, signature validation or legal conclusion.',
    'The selector, tag and embedded revision associate the shipped rg with the selected ripgrep source revision; they are not a byte join with the selected release archive.',
    'PCRE2 terms are not covered here; ripgrep 15.2.0 locks pcre2-sys 0.2.10, whose source text is not held.',
]


def blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def read(path):
    return reader.transfer(Path(path).absolute(), retain=True)


def build(rg_path, metadata):
    metadata = Path(metadata)
    raw_rg, rg_sha, rg_size = read(rg_path)
    require(rg_sha == RG_SHA256, 'rg is not the canonical 0.167.0 subject')
    selector_raw, selector_sha, _ = read(ROOT / SELECTOR)
    require(blob(selector_raw) == SELECTOR_BLOB, 'received rg selector changed')
    platform = json.loads(selector_raw.split(b'\n', 2)[2])['platforms']['macos-aarch64']
    require(platform['providers'] == [{'url': ARCHIVE_URL}], 'selector names another archive')

    loaded = {}
    for name in RESPONSES:
        raw, digest, size = read(metadata / name)
        loaded[name] = (reader.parse(raw), {'name': name, 'sha256': digest, 'size': size})
    ref, tag, tree = (loaded[n][0] for n in RESPONSES)
    require(ref['ref'] == 'refs/tags/' + TAG and ref['object']['sha'] == TAG_OBJECT, 'tag reference changed')
    require(tag['sha'] == TAG_OBJECT and tag['tag'] == TAG and tag['object'] == {**tag['object'], 'sha': COMMIT, 'type': 'commit'},
            'tag object does not name the selected commit')
    require(tree['sha'] == COMMIT and not tree['truncated'], 'tree response is not the tagged commit')
    entries = {e['path']: e for e in tree['tree']}

    texts = []
    for name in LICENCE_FILES:
        raw, digest, size = read(ROOT / TEXTS / name)
        require(entries[name]['size'] == size and entries[name]['sha'] == blob(raw), 'licence text differs: ' + name)
        texts.append({'path': name, 'local_text': TEXTS + '/' + name, 'size_bytes': size,
                      'sha256': digest, 'git_blob_sha1': entries[name]['sha']})
    lock_raw, lock_sha, lock_size = read(metadata / 'source/Cargo.lock')
    require(entries['Cargo.lock']['size'] == lock_size and entries['Cargo.lock']['sha'] == blob(lock_raw),
            'retained ripgrep Cargo.lock differs')
    packages = tomllib.loads(lock_raw.decode())['package']
    registry = {f"{p['name']}-{p['version']}": p for p in packages if p.get('source', '').startswith('registry+')}

    revision = re.findall(rb'\(JIT is available\)\n(\d+\.\d+\.\d+)([0-9a-f]{10})', raw_rg)
    require(len(revision) == 1, 'single ripgrep version/revision clue required')
    version, prefix = (part.decode() for part in revision[0])
    crates = sorted({m.rsplit(b'/', 1)[1].decode()
                     for m in re.findall(rb'registry/src/index\.crates\.io-[0-9a-f]+/[A-Za-z0-9_.+-]+', raw_rg)})
    pcre2_sys = next(p for p in packages if p['name'] == 'pcre2-sys')
    return {
        'format': 'codex-rg-ripgrep-association/1',
        'tool_sha256': reader.sha(Path(__file__).read_bytes()),
        'subject': {'path': 'codex-path/rg', 'sha256': rg_sha, 'size': rg_size},
        'selector': {'path': 'scripts/codex_package/rg', 'git_blob_sha1': SELECTOR_BLOB, 'sha256': selector_sha,
                     'macos_aarch64': platform},
        'source': {'repository': 'https://github.com/BurntSushi/ripgrep', 'tag': TAG, 'tag_object': TAG_OBJECT,
                   'commit': COMMIT, 'retained_responses': [loaded[n][1] for n in RESPONSES],
                   'cargo_lock': {'size_bytes': lock_size, 'sha256': lock_sha, 'git_blob_sha1': entries['Cargo.lock']['sha']}},
        'embedded_clues': {'version': version, 'revision_prefix': prefix,
                           'revision_prefix_matches_tag_commit': version == TAG and COMMIT.startswith(prefix),
                           'registry_crate_directories': crates,
                           'all_in_locked_registry_packages': all(c in registry for c in crates)},
        'licence_texts': texts,
        'pcre2_sys_locked': {'version': pcre2_sys['version'], 'checksum': pcre2_sys['checksum'],
                             'held': False},
        'limits': LIMITS,
    }


def render(value):
    return json.dumps(value, indent=1) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rg')
    parser.add_argument('metadata', help='directory holding the retained ripgrep responses and source/Cargo.lock')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', metavar='FILE')
    mode.add_argument('--check', metavar='FILE')
    args = parser.parse_args()
    text = render(build(args.rg, args.metadata))
    if args.write:
        Path(args.write).write_text(text)
    else:
        require(Path(args.check).read_text() == text, 'retained record differs')
    print(reader.sha(text.encode()))
