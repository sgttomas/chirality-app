"""Recompute the Codex 0.167.0 rg -> ripgrep 15.2.0 source-text association offline.

Reads the canonical 0.167.0 rg binary, the received Codex rg release selector,
the committed ripgrep licence texts and retained ripgrep public metadata/source
text. Executes nothing, opens no network connection and draws no licence or
compliance conclusion. Version, revision and crate-path strings are clues; they
do not join the shipped binary to the selected release archive.
"""
import argparse
import hashlib
import html
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
# Codex's rg release selector (scripts/codex_package/rg): its identity and macOS arm64 platform row.
SELECTOR_BLOB = '3b7c34843aaafe4cf26a87b3daf5806195d4bb0e'
SELECTOR_SHA256 = '41a10ca63365560d899a82b6f825fd7b420a18b34f660a98bffeece77eeae1f1'
ARCHIVE_URL = 'https://github.com/BurntSushi/ripgrep/releases/download/15.2.0/ripgrep-15.2.0-aarch64-apple-darwin.tar.gz'
SELECTOR_PLATFORM = {'size': 1764284, 'hash': 'sha256',
                     'digest': '3750b2e93f37e0c692657da574d7019a101c0084da05a790c83fd335bad973e4',
                     'format': 'tar.gz', 'path': 'ripgrep-15.2.0-aarch64-apple-darwin/rg',
                     'providers': [{'url': ARCHIVE_URL}]}
TAG, TAG_OBJECT = '15.2.0', '6ec72defacfb042f203ca0b4bf2513a0a5505a7e'
COMMIT = 'e89fff89ac9af12e8d4ce9d5fd07beb408ca730f'
TEXTS = 'app/packaging/supplier_notices/ripgrep-15.2.0'
LICENCE_FILES = ('COPYING', 'LICENSE-MIT', 'UNLICENSE')
RESPONSES = ('ripgrep-ref-tag.json', 'ripgrep-tag-object.json', 'ripgrep-root-tree.json')
LIMITS = [
    'No execution, network access, acquisition, signature validation or legal conclusion.',
    'The selector, tag and embedded revision associate the shipped rg with the selected ripgrep source revision; they are not a byte join with the selected release archive.',
    'The pcre2-sys chain binds published crate metadata and source revisions by checksum, VCS record, tags and blobs; it does not observe what the shipped rg statically links.',
]
# pcre2-sys 0.2.10 -> vendored PCRE2 10.46 and sljit source revisions (public metadata/source text).
PCRE2_SYS = {'version': '0.2.10', 'repository': 'https://github.com/BurntSushi/rust-pcre2',
             'tag': 'pcre2-sys-0.2.10', 'commit': 'fd05026e1bf3ad62b3876cf9bd952dc742368462'}
PCRE2 = {'version': '10.46', 'repository': 'https://github.com/PCRE2Project/pcre2', 'tag': 'pcre2-10.46',
         'commit': 'b2bd4254b379b9d7dc9a3dda060a7e27009ccdff'}
SLJIT = {'repository': 'https://github.com/zherczeg/sljit', 'commit': 'e51eabbfb8eabc6526f56e4e88b29fb10d1ee048'}
PCRE2_RESPONSES = ('index-pcre2-sys.txt', 'crate-0.2.10.json', 'docsrs-vcs.html', 'refs-tags.json', 'tag-object.json',
                   'root-tree.json', 'pcre2-sys-tree.json', 'upstream-tree.json', 'pcre2-ref-tag.json',
                   'pcre2-tag-object.json', 'pcre2-tree-recursive.json', 'pcre2-gitmodules', 'sljit-tree-recursive.json')
# Vendored file -> PCRE2 release path where update-pcre2 renames it.
VENDOR_RENAMES = {'include/config.h': 'src/config.h.generic', 'include/pcre2.h': 'src/pcre2.h.generic',
                  'src/pcre2_chartables.c': 'src/pcre2_chartables.c.dist'}
TERMS = (('pcre2-sys/COPYING', 'app/packaging/supplier_notices/ripgrep-15.2.0/COPYING', 'crate'),
         ('pcre2-sys/LICENSE-MIT', 'app/packaging/supplier_notices/pcre2-sys-0.2.10/LICENSE-MIT', 'crate'),
         ('pcre2-sys/UNLICENSE', 'app/packaging/supplier_notices/ripgrep-15.2.0/UNLICENSE', 'crate'),
         ('LICENCE.md', 'app/packaging/supplier_notices/pcre2-10.46/LICENCE.md', 'pcre2'),
         ('LICENSE', 'app/packaging/supplier_notices/sljit-e51eabbf/LICENSE', 'sljit'))


def blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def read(path):
    return reader.transfer(Path(path).absolute(), retain=True)


def pcre2_chain(metadata, locked):
    metadata = Path(metadata)
    raw_of, kept = {}, []
    for name in PCRE2_RESPONSES:
        raw, digest, size = read(metadata / name)
        raw_of[name] = raw
        kept.append({'name': name, 'sha256': digest, 'size': size})
    j = lambda name: reader.parse(raw_of[name])
    index = [json.loads(line) for line in raw_of['index-pcre2-sys.txt'].decode().splitlines() if line]
    entry = next(v for v in index if v['vers'] == PCRE2_SYS['version'])
    api = j('crate-0.2.10.json')['version']
    require(entry['cksum'] == locked['checksum'] == api['checksum'] and not entry['yanked'], 'crate checksum chain broken')
    require(api['repository'] == PCRE2_SYS['repository'], 'crate repository changed')
    # docs.rs renders the published crate's .cargo_vcs_info.json as highlighted HTML source text.
    shown = html.unescape(re.sub(r'<[^>]+>', '', raw_of['docsrs-vcs.html'].decode()))
    vcs = re.findall(r'"sha1": "([0-9a-f]{40})"\s*},\s*"path_in_vcs": "([^"]+)"', shown)
    require(vcs == [(PCRE2_SYS['commit'], 'pcre2-sys')], 'published VCS record differs')
    ref = next(r for r in j('refs-tags.json') if r['ref'] == 'refs/tags/' + PCRE2_SYS['tag'])
    tag = j('tag-object.json')
    require(ref['object']['sha'] == tag['sha'] and tag['object']['sha'] == PCRE2_SYS['commit'], 'pcre2-sys tag mismatch')
    root = j('root-tree.json')
    require(root['sha'] == PCRE2_SYS['commit'] and not root['truncated'], 'rust-pcre2 tree is not the tagged commit')
    crate_tree = j('pcre2-sys-tree.json')
    require(crate_tree['sha'] == {e['path']: e for e in root['tree']}['pcre2-sys']['sha'], 'pcre2-sys subtree mismatch')
    crate = {e['path']: e for e in crate_tree['tree']}
    upstream = j('upstream-tree.json')
    require(upstream['sha'] == crate['upstream']['sha'] and not upstream['truncated'], 'vendored upstream tree mismatch')
    for name, check in (('pcre2-sys-Cargo.toml', b'version = "0.2.10"'), ('pcre2-sys-update-pcre2', b'version="10.46"')):
        raw, _, size = read(metadata / 'source' / name)
        key = name.removeprefix('pcre2-sys-')
        require(crate[key]['size'] == size and crate[key]['sha'] == blob(raw) and check in raw, 'crate source differs: ' + key)
    ptag = j('pcre2-tag-object.json')
    require(j('pcre2-ref-tag.json')['object']['sha'] == ptag['sha'] and ptag['tag'] == PCRE2['tag']
            and ptag['object']['sha'] == PCRE2['commit'], 'PCRE2 tag mismatch')
    ptree = j('pcre2-tree-recursive.json')
    require(ptree['sha'] == PCRE2['commit'] and not ptree['truncated'], 'PCRE2 tree incomplete')
    pfiles = {e['path']: e for e in ptree['tree']}
    require(pfiles['deps/sljit']['type'] == 'commit' and pfiles['deps/sljit']['sha'] == SLJIT['commit'], 'sljit pointer changed')
    require(b'url = https://github.com/zherczeg/sljit.git' in raw_of['pcre2-gitmodules'], 'sljit submodule URL changed')
    stree = j('sljit-tree-recursive.json')
    require(stree['sha'] == SLJIT['commit'] and not stree['truncated'], 'sljit tree incomplete')
    sfiles = {e['path']: e for e in stree['tree']}
    counts = {'pcre2_release': 0, 'sljit': 0}
    for e in upstream['tree']:
        if e['type'] != 'blob':
            continue
        if e['path'].startswith('deps/sljit/'):
            require(sfiles[e['path'][len('deps/sljit/'):]]['sha'] == e['sha'], 'vendored sljit differs: ' + e['path'])
            counts['sljit'] += 1
        else:
            require(pfiles[VENDOR_RENAMES.get(e['path'], e['path'])]['sha'] == e['sha'], 'vendored PCRE2 differs: ' + e['path'])
            counts['pcre2_release'] += 1
    trees = {'crate': ({'pcre2-sys/' + k: v for k, v in crate.items()}, PCRE2_SYS), 'pcre2': (pfiles, PCRE2), 'sljit': (sfiles, SLJIT)}
    terms = []
    for source_path, local, kind in TERMS:
        raw, digest, size = read(ROOT / local)
        files, origin = trees[kind]
        require(files[source_path]['size'] == size and files[source_path]['sha'] == blob(raw), 'terms text differs: ' + local)
        terms.append({'repository': origin['repository'], 'commit': origin['commit'], 'path': source_path,
                      'local_text': local, 'size_bytes': size, 'sha256': digest, 'git_blob_sha1': blob(raw)})
    return {'crate': {**PCRE2_SYS, 'checksum': entry['cksum'], 'crate_size': api['crate_size'], 'license': api['license']},
            'pcre2': PCRE2, 'sljit': SLJIT, 'vendored_blobs_equal_to_sources': counts,
            'vendored_upstream_has_licence_file': any(e['path'].upper().startswith(('LICEN', 'COPYING')) or '/LICEN' in e['path'].upper()
                                                      for e in upstream['tree']),
            'terms_texts': terms, 'retained_responses': kept}


def build(rg_path, metadata, pcre2_metadata):
    metadata = Path(metadata)
    raw_rg, rg_sha, rg_size = read(rg_path)
    require(rg_sha == RG_SHA256, 'rg is not the canonical 0.167.0 subject')
    selector_sha, platform = SELECTOR_SHA256, dict(SELECTOR_PLATFORM)

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
        'pcre2_sys': pcre2_chain(pcre2_metadata, pcre2_sys),
        'limits': LIMITS,
    }


def render(value):
    return json.dumps(value, indent=1) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rg')
    parser.add_argument('metadata', help='directory holding the retained ripgrep responses and source/Cargo.lock')
    parser.add_argument('pcre2_metadata', help='directory holding the retained pcre2-sys/PCRE2/sljit responses and source texts')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', metavar='FILE')
    mode.add_argument('--check', metavar='FILE')
    args = parser.parse_args()
    text = render(build(args.rg, args.metadata, args.pcre2_metadata))
    if args.write:
        Path(args.write).write_text(text)
    else:
        require(Path(args.check).read_text() == text, 'retained record differs')
    print(reader.sha(text.encode()))
