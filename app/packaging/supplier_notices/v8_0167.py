"""Recompute the Codex 0.167.0 code-mode-host V8-stack source/terms association offline.

Reads retained Codex, V8 and rusty_v8 public metadata and source text plus the
committed terms texts. It executes nothing, opens no network connection and draws
no licence or compliance conclusion. Source pins and version markers locate
inputs; they do not show what the shipped code-mode-host links.
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

CODEX_COMMIT = '086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a'
V8 = {'repository': 'https://github.com/v8/v8', 'tag': '15.2.124.1', 'commit': 'd848a2b3d3aedda62fd825ce5326e5c9d32db96f'}
CRATE = {'repository': 'https://github.com/seanh-oai/rusty_v8', 'commit': '350c5a859a9b3c84ab8701b3ad51e3b7699b30c0',
         'name': 'v8', 'version': '152.2.0'}
ARCHIVE = ('librusty_v8_ptrcomp_sandbox_release_aarch64-apple-darwin.a.gz',
           'feab9ae0384bebaa99c1d000654462c9d42123d587185c7876aaeef7d76ff749',
           'https://github.com/openai/codex/releases/download/rusty-v8-v152.2.0/librusty_v8_ptrcomp_sandbox_release_aarch64-apple-darwin.a.gz')
# Pins named in Codex's Bazel graph that V8 15.2.124.1's DEPS must name identically.
SHARED_DEPS = {'icu': ('third_party/icu', '/chromium/deps/icu.git'),
               'libcxx': ('third_party/libc++/src', '/external/github.com/llvm/llvm-project/libcxx.git'),
               'libcxxabi': ('third_party/libc++abi/src', '/external/github.com/llvm/llvm-project/libcxxabi.git')}
TERMS = (('v8', 'LICENSE'), ('v8', 'LICENSE.v8'), ('v8', 'LICENSE.fdlibm'), ('v8', 'LICENSE.strongtalk'),
         ('crate', 'LICENSE'))
LOCAL = {'v8': 'app/packaging/supplier_notices/v8-15.2.124.1', 'crate': 'app/packaging/supplier_notices/rusty_v8-350c5a85'}
RESPONSES = ('v8-ref-tag.json', 'v8-root-tree.json', 'fork-root-tree.json', 'fork-gitmodules')
SOURCES = {'codex-MODULE.bazel': ('codex-root', 'MODULE.bazel'),
           'codex-third_party-v8-dependencies.bzl': ('codex-v8', 'dependencies.bzl'),
           'codex-third_party-v8-rusty_v8_152_2_0.sha256': ('codex-v8', 'rusty_v8_152_2_0.sha256'),
           'codex-third_party-v8-README.md': ('codex-v8', 'README.md'),
           'v8-DEPS': ('v8', 'DEPS'), 'rusty_v8-Cargo.toml': ('crate', 'Cargo.toml')}
LIMITS = [
    'No execution, network access, acquisition, signature validation or legal conclusion.',
    'Codex documents that release builds link its published rusty-v8-v152.2.0 archive built from this Bazel graph; the shipped code-mode-host is not joined to that archive or graph here.',
    'V8 states that externally maintained libraries and sub-directory LICENSE files carry their own terms; those, ICU, libc++/libc++abi, llvm-libc and the other pinned V8 dependencies are not covered by these texts.',
]


def blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def read(path):
    return reader.transfer(Path(path).absolute(), retain=True)


def one(pattern, text, label):
    found = re.findall(pattern, text, re.S)
    require(len(found) == 1, 'expected one ' + label)
    return found[0]


def build(codex_metadata, metadata):
    codex_metadata, metadata = Path(codex_metadata), Path(metadata)
    trees = {}
    root = reader.parse(read(codex_metadata / 'root-tree.json')[0])
    require(root['sha'] == CODEX_COMMIT, 'Codex root tree is not the selected commit')
    v8_listing = reader.parse(read(codex_metadata / 'third_party-v8-tree.json')[0])
    third = reader.parse(read(codex_metadata / 'third_party-tree.json')[0])
    require(third['sha'] == {e['path']: e for e in root['tree']}['third_party']['sha'], 'Codex third_party mismatch')
    require(v8_listing['sha'] == {e['path']: e for e in third['tree']}['v8']['sha'], 'Codex third_party/v8 mismatch')
    trees['codex-root'] = {e['path']: e for e in root['tree']}
    trees['codex-v8'] = {e['path']: e for e in v8_listing['tree']}

    kept, parsed = [], {}
    for name in RESPONSES:
        raw, digest, size = read(metadata / name)
        kept.append({'name': name, 'sha256': digest, 'size': size})
        parsed[name] = raw
    ref = reader.parse(parsed['v8-ref-tag.json'])
    require(ref['ref'] == 'refs/tags/' + V8['tag'] and ref['object'] == {**ref['object'], 'sha': V8['commit'], 'type': 'commit'},
            'V8 tag does not name the selected commit')
    v8_tree = reader.parse(parsed['v8-root-tree.json'])
    fork_tree = reader.parse(parsed['fork-root-tree.json'])
    require(v8_tree['sha'] == V8['commit'] and not v8_tree['truncated'], 'V8 tree is not the tagged commit')
    require(fork_tree['sha'] == CRATE['commit'] and not fork_tree['truncated'], 'rusty_v8 tree is not the pinned commit')
    trees['v8'] = {e['path']: e for e in v8_tree['tree']}
    trees['crate'] = {e['path']: e for e in fork_tree['tree']}
    require(trees['crate']['.gitmodules']['sha'] == blob(parsed['fork-gitmodules']), 'rusty_v8 .gitmodules differs')

    text = {}
    for local, (tree, path) in SOURCES.items():
        raw, digest, size = read(metadata / 'source' / local)
        entry = trees[tree][path]
        require(entry['size'] == size and entry['sha'] == blob(raw), 'source text differs: ' + local)
        text[local] = raw.decode()
    module, deps = text['codex-MODULE.bazel'], text['v8-DEPS']
    engine = one(r'(engine_repository\(\s*name = "v8",.*?\n\))', module, 'V8 engine block')
    require(one(r'strip_prefix = "v8-([0-9.]+)"', engine, 'V8 engine pin') == V8['tag'], 'Codex V8 engine pin changed')
    require(f'https://github.com/v8/v8/archive/refs/tags/{V8["tag"]}.tar.gz' in module, 'V8 source URL changed')
    require(one(r'name = "v8_crate_152_2_0",.*?strip_prefix = "rusty_v8-([0-9a-f]{40})"', module, 'v8 crate pin') == CRATE['commit'],
            'Codex v8 crate pin changed')
    archive_pin = one(r'name = "rusty_v8_152_2_0_aarch64_apple_darwin_archive",.*?sha256 = "([0-9a-f]{64})"', module, 'archive pin')
    require(archive_pin == ARCHIVE[1] and ARCHIVE[2] in module, 'Codex prebuilt archive pin changed')
    require(f'{ARCHIVE[1]}  {ARCHIVE[0]}' in text['codex-third_party-v8-rusty_v8_152_2_0.sha256'], 'archive checksum list changed')
    pins = {}
    for key, (deps_path, remote) in SHARED_DEPS.items():
        in_deps = one(re.escape(f"'{deps_path}':") + r"\s*Var\('chromium_url'\) \+ '" + re.escape(remote) + r"' \+ '@' \+ '([0-9a-f]{40})'",
                      deps, 'V8 DEPS ' + key)
        codex = text['codex-third_party-v8-dependencies.bzl'] + module
        require(f'commit = "{in_deps}"' in codex and remote in codex, 'Codex and V8 DEPS disagree: ' + key)
        pins[key] = {'remote': 'https://chromium.googlesource.com' + remote, 'commit': in_deps,
                     'agrees_with_v8_deps': True, 'terms_text_held': False}
    llvm_libc = one(r'name = "rusty_v8_llvm_libc",.*?commit = "([0-9a-f]{40})"', module, 'llvm-libc pin')
    pins['llvm_libc'] = {'remote': 'https://chromium.googlesource.com/external/github.com/llvm/llvm-project/libc.git',
                         'commit': llvm_libc, 'agrees_with_v8_deps': None, 'terms_text_held': False}
    manifest = tomllib.loads(text['rusty_v8-Cargo.toml'])['package']
    require((manifest['name'], manifest['version']) == (CRATE['name'], CRATE['version']), 'rusty_v8 crate identity changed')
    fork_v8 = trees['crate']['v8']
    require(fork_v8['type'] == 'commit', 'rusty_v8 v8 entry is not a submodule')

    terms = []
    for origin, name in TERMS:
        raw, digest, size = read(ROOT / LOCAL[origin] / name)
        entry = trees[origin][name]
        require(entry['size'] == size and entry['sha'] == blob(raw), 'terms text differs: ' + name)
        source = V8 if origin == 'v8' else CRATE
        terms.append({'repository': source['repository'], 'commit': source['commit'], 'path': name,
                      'local_text': LOCAL[origin] + '/' + name, 'size_bytes': size, 'sha256': digest, 'git_blob_sha1': entry['sha']})
    return {
        'format': 'codex-code-mode-host-v8-association/1',
        'tool_sha256': reader.sha(Path(__file__).read_bytes()),
        'codex_commit': CODEX_COMMIT,
        'v8_engine': {**V8, 'codex_patches': re.findall(r'"(//[^"]+\.patch)"', engine)},
        'v8_crate': {**CRATE, 'license': manifest['license'], 'fork_v8_submodule_commit': fork_v8['sha'],
                     'fork_v8_submodule_differs_from_engine_pin': fork_v8['sha'] != V8['commit']},
        'prebuilt_archive': {'name': ARCHIVE[0], 'sha256': ARCHIVE[1], 'url': ARCHIVE[2], 'held': False},
        'other_pins': pins,
        'terms_texts': terms,
        'retained_responses': kept,
        'limits': LIMITS,
    }


def render(value):
    return json.dumps(value, indent=1) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('codex_metadata', help='directory holding the retained Codex 0.167.0 tree responses')
    parser.add_argument('metadata', help='directory holding the retained V8/rusty_v8 responses and source texts')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', metavar='FILE')
    mode.add_argument('--check', metavar='FILE')
    args = parser.parse_args()
    rendered = render(build(args.codex_metadata, args.metadata))
    if args.write:
        Path(args.write).write_text(rendered)
    else:
        require(Path(args.check).read_text() == rendered, 'retained record differs')
    print(reader.sha(rendered.encode()))
