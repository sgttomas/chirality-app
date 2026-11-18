"""Invented archives for the notice-only crate route (supplier_notices/crate_notices.py), the committed crate group
(supplier_notices/crates.py) and the voice-record comparison (supplier_notices/voice.py)."""
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import tarfile
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('crate_notices', ROOT / 'app/packaging/supplier_notices/crate_notices.py')
cn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cn)

SENTINEL = b'NOT-A-NOTICE-PAYLOAD-SENTINEL'
PACKAGE = ('demo', '1.0.0')


def crate(members, fmt=tarfile.GNU_FORMAT, name='demo-1.0.0'):
    """A gzip tar of (path, bytes | ('symlink'|'hardlink'|'dir'|'fifo', target)) under name/."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=fmt) as tar:
        for path, body in members:
            # A path beginning with '=' is used as the member name as written, without the package folder.
            info = tarfile.TarInfo(path[1:] if path.startswith('=') else f'{name}/{path}')
            if isinstance(body, tuple):
                kind, target = body
                info.type = {'symlink': tarfile.SYMTYPE, 'hardlink': tarfile.LNKTYPE, 'dir': tarfile.DIRTYPE,
                             'fifo': tarfile.FIFOTYPE}[kind]
                info.linkname = target or ''
                tar.addfile(info)
            else:
                info.size = len(body)
                tar.addfile(info, io.BytesIO(body))
    return gzip.compress(buffer.getvalue(), mtime=0)


class Recording:
    """A gzip reader that records every byte handed to the route; seeks pass through without returning data."""
    handed = []

    def __init__(self, fileobj):
        self.inner = gzip.GzipFile(fileobj=fileobj)

    def read(self, n=-1):
        data = self.inner.read(n)
        Recording.handed.append(data)
        return data

    def seek(self, offset, whence=io.SEEK_SET):
        return self.inner.seek(offset, whence)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.inner.close()


def ordinary():
    return [('Cargo.toml', b'[package] = not valid toml ' + SENTINEL), ('build.rs', b'panic!("' + SENTINEL + b'")'),
            ('README.md', SENTINEL * 50), ('LICENSE-MIT', b'MIT text\n'), ('LICENSE-APACHE', b'Apache text\n'),
            ('src/lib.rs', SENTINEL * 400), ('src/license.rs', SENTINEL), ('vendor/zlib/LICENSE', b'zlib text\n'),
            ('vendor/zlib/zlib.c', SENTINEL * 1000), ('COPYING.json', SENTINEL), ('notices/NOTICE.txt', b'notice\n')]


def test_selects_root_and_nested_notices_and_hands_over_no_other_payload(monkeypatch):
    raw = crate(ordinary())
    Recording.handed = []
    monkeypatch.setattr(tomllib, 'loads', lambda *a, **k: pytest.fail('a manifest was parsed'))
    entry = cn.index_entry(raw, PACKAGE, hashlib.sha256(raw).hexdigest(), opener=Recording)
    assert [n['path'] for n in entry['notices']] == ['LICENSE-APACHE', 'LICENSE-MIT', 'notices/NOTICE.txt',
                                                      'vendor/zlib/LICENSE']
    handed = b''.join(Recording.handed)
    assert SENTINEL not in handed
    # Everything handed over is a 512-byte header (or long-name data) or one of the selected notice bodies.
    assert entry['members'] == len(ordinary())
    texts = cn.extract_checked(raw, entry, opener=Recording)
    assert texts['vendor/zlib/LICENSE'] == b'zlib text\n'
    assert SENTINEL not in b''.join(Recording.handed)


def test_pax_and_long_names_are_followed():
    long = 'deep/' * 30 + 'LICENSE'
    for fmt in (tarfile.GNU_FORMAT, tarfile.PAX_FORMAT, tarfile.USTAR_FORMAT):
        members = [(long, b'deep licence\n'), ('a.rs', SENTINEL)] if fmt != tarfile.USTAR_FORMAT else \
            [('deep/' * 18 + 'LICENSE', b'deep licence\n'), ('a.rs', SENTINEL)]
        raw = crate(members, fmt=fmt)
        entry = cn.index_entry(raw, PACKAGE, hashlib.sha256(raw).hexdigest())
        assert [n['size_bytes'] for n in entry['notices']] == [13]


@pytest.mark.parametrize('size', ['-1', '+1', ' 1', '1.0'])
def test_invalid_pax_size_refuses_before_non_notice_payload_is_read(size):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.PAX_FORMAT) as tar:
        info = tarfile.TarInfo('demo-1.0.0/LICENSE')
        info.pax_headers = {'size': size}
        tar.addfile(info, io.BytesIO(b''))
        info = tarfile.TarInfo('demo-1.0.0/src/lib.rs')
        info.size = len(SENTINEL)
        tar.addfile(info, io.BytesIO(SENTINEL))
    raw = gzip.compress(buffer.getvalue(), mtime=0)
    Recording.handed = []
    with pytest.raises(cn.Refused, match='pax size must be a nonnegative decimal'):
        cn.index_entry(raw, PACKAGE, hashlib.sha256(raw).hexdigest(), opener=Recording)
    assert SENTINEL not in b''.join(Recording.handed)


def test_checksum_is_verified_before_the_archive_is_opened(monkeypatch):
    raw = crate(ordinary())
    opened = []
    monkeypatch.setattr(cn, '_members', lambda *a, **k: opened.append(1))
    with pytest.raises(cn.Refused, match='lockfile checksum'):
        cn.index_entry(raw, PACKAGE, '0' * 64)
    assert opened == []


@pytest.mark.parametrize('members, message', [
    ([('LICENSE', b'a'), ('LICENSE', b'b')], 'repeats a member'),
    ([('LICENSE', b'a'), ('license', b'b')], 'equal ignoring case'),
    ([('LICENSE', ('symlink', '../../etc/passwd'))], 'link member'),
    ([('LICENSE', b'a'), ('COPYING', ('hardlink', 'demo-1.0.0/LICENSE'))], 'link member'),
    ([('src/x.rs', ('symlink', 'y.rs'))], 'link member'),
    ([('fifo', ('fifo', None))], 'unsupported member type'),
    ([('=../LICENSE', b'a')], 'outside the package folder'),
    ([('=demo-1.0.0/../x/LICENSE', b'a')], 'unsafe member path'),
    ([('=/abs/LICENSE', b'a')], 'outside the package folder'),
    ([('=other-1.0.0/LICENSE', b'a')], 'outside the package folder'),
])
def test_refusals(members, message):
    raw = crate(members)
    with pytest.raises(cn.Refused, match=message):
        cn.index_entry(raw, PACKAGE, hashlib.sha256(raw).hexdigest())


def test_extraction_refuses_any_difference_from_the_index():
    raw = crate(ordinary())
    entry = cn.index_entry(raw, PACKAGE, hashlib.sha256(raw).hexdigest())
    changed = crate([m if m[0] != 'LICENSE-MIT' else ('LICENSE-MIT', b'MIT text!\n') for m in ordinary()])
    with pytest.raises(cn.Refused, match='lockfile checksum'):
        cn.extract_checked(changed, entry)
    for key, value in (('inventory_sha256', '0' * 64), ('members', 3)):
        with pytest.raises(cn.Refused, match='inventory differs'):
            cn.extract_checked(raw, {**entry, key: value})
    tampered = {**entry, 'notices': entry['notices'][1:]}
    with pytest.raises(cn.Refused, match='notices differ'):
        cn.extract_checked(raw, tampered)
    renamed = {**entry, 'checksum': hashlib.sha256(changed).hexdigest()}
    with pytest.raises(cn.Refused, match='notices differ|inventory differs'):
        cn.extract_checked(changed, renamed)


def test_a_notice_named_directory_or_source_file_is_not_selected():
    raw = crate([('LICENSES', ('dir', None)), ('LICENSES/MIT.txt', b'm'), ('LICENSES/check.py', SENTINEL),
                 ('src/copyright.rs', SENTINEL), ('third_party/x/COPYING', b'a'), ('license-check.py', SENTINEL),
                 ('NOTICE', ('dir', None)), ('NOTICE/data.bin', SENTINEL)])
    entry = cn.index_entry(raw, PACKAGE, hashlib.sha256(raw).hexdigest())
    assert [n['path'] for n in entry['notices']] == ['LICENSES/MIT.txt', 'third_party/x/COPYING']


def test_truncated_or_corrupt_headers_refuse():
    raw = bytearray(gzip.decompress(crate(ordinary())))
    raw[148] ^= 0x01
    corrupt = gzip.compress(bytes(raw), mtime=0)
    with pytest.raises(cn.Refused, match='checksum differs|malformed'):
        cn.index_entry(corrupt, PACKAGE, hashlib.sha256(corrupt).hexdigest())


# The committed 0.169.0 crate group (supplier_notices/crates.py): check needs no archive and refuses any drift.
crates_spec = importlib.util.spec_from_file_location('supplier_crates', ROOT / 'app/packaging/supplier_notices/crates.py')
crates = importlib.util.module_from_spec(crates_spec)
crates_spec.loader.exec_module(crates)


@pytest.fixture
def repo(tmp_path):
    import shutil
    for relative in ('app/packaging/supplier_notices', 'app/packaging/notices'):
        shutil.copytree(ROOT / relative, tmp_path / relative)
    return tmp_path


def edit(repo, relative, change):
    import json
    path = repo / relative
    value = json.loads(path.read_bytes())
    change(value)
    path.write_text(json.dumps(value))


def test_committed_group_checks_and_covers_every_locked_package():
    result = crates.check(ROOT)
    assert result['locks']['codex'] == {'packages': 1483, 'registry': 1296, 'git': 14, 'path': 173, 'text': 1393, 'held': 23, 'gap': 53,
                                        'no-publisher-text': 8, 'not-in-macos-package': 6}
    assert result['locks']['ripgrep'] == {'packages': 59, 'registry': 49, 'git': 0, 'path': 10, 'text': 59, 'held': 0, 'gap': 0,
                                          'no-publisher-text': 0, 'not-in-macos-package': 0}
    value = crates.packages(ROOT)
    assert 'Some may not be compiled into the macOS executables' in value['superset']
    for row in value['packages']:
        assert (row['standing'] in ('gap', 'no-publisher-text', 'not-in-macos-package')) == (not row['texts'])
        assert row['standing'] not in ('gap', 'no-publisher-text') or (row['reason'] and row['would_close'])
        assert row['standing'] != 'not-in-macos-package' or row['absence']['reverse_dependencies']
        # Every remaining gap carries its own reason, not the generic one.
        assert row['standing'] != 'gap' or 'no text is held for this crate version' not in row['reason']


def test_lockfile_drift_refuses(repo):
    lock = repo / crates.BASE / 'locks/codex-rs.Cargo.lock'
    lock.write_bytes(lock.read_bytes().replace(b'name = "zstd"', b'name = "zstdx"', 1))
    with pytest.raises(ValueError, match='lockfile differs'):
        crates.check(repo)


@pytest.mark.parametrize('source', ['workspaces', 'app_texts'])
def test_empty_text_associations_refuse_before_account_generation(repo, source):
    def empty(v):
        entry = next(w for w in v[source] if w['lock'] == 'ripgrep') if source == 'workspaces' else v[source][0]
        entry['texts'] = []
    edit(repo, crates.ASSOCIATIONS, empty)
    for operation in (crates.check, crates.packages):
        with pytest.raises(ValueError, match='must have at least one text'):
            operation(repo)


def test_a_missing_or_extra_index_row_refuses(repo):
    edit(repo, crates.INDEX, lambda v: v['registry'].pop(0))
    with pytest.raises(ValueError, match='differs from the lockfiles'):
        crates.check(repo)


def test_a_missing_changed_extra_or_linked_text_refuses(repo):
    store = repo / crates.TEXTS
    target = sorted(store.iterdir())[0]
    original = target.read_bytes()
    target.write_bytes(original + b'x')
    with pytest.raises(ValueError, match='bytes differ'):
        crates.check(repo)
    target.unlink()
    with pytest.raises(ValueError, match='missing'):
        crates.check(repo)
    target.write_bytes(original)
    (store / ('0' * 64)).write_bytes(b'INVENTED')
    with pytest.raises(ValueError, match='extra'):
        crates.check(repo)
    (store / ('0' * 64)).unlink()
    target.unlink()
    target.symlink_to(repo / 'app/packaging/supplier_notices/codex/LICENSE')
    with pytest.raises(ValueError, match='regular non-link'):
        crates.check(repo)


def test_an_index_digest_drift_refuses(repo):
    def change(v):
        row = next(r for r in v['registry'] if r['notices'])
        row['notices'][0]['sha256'] = 'f' * 64
    edit(repo, crates.INDEX, change)
    with pytest.raises(ValueError):
        crates.check(repo)


def test_git_association_must_match_the_lock_and_its_listing(repo):
    edit(repo, crates.ASSOCIATIONS, lambda v: v['git_sources'][0].update(revision='a' * 40))
    with pytest.raises(ValueError, match='another repository or revision'):
        crates.check(repo)


def test_git_text_must_be_its_listing_blob(repo):
    edit(repo, crates.ASSOCIATIONS, lambda v: v['git_sources'][0]['texts'][0].update(listing_blob='a' * 40))
    with pytest.raises(ValueError, match='listing names'):
        crates.check(repo)


def test_a_locked_git_package_without_association_refuses(repo):
    edit(repo, crates.ASSOCIATIONS, lambda v: v['git_sources'].pop())
    with pytest.raises(ValueError, match='no Git association'):
        crates.check(repo)


def test_stale_package_account_refuses(repo):
    edit(repo, crates.PACKAGES, lambda v: v['packages'].pop())
    with pytest.raises(ValueError, match='stale'):
        crates.check(repo)


def test_app_held_texts_are_a_reviewed_association_not_a_read_of_the_app_tree(repo):
    import shutil
    # The App's own notice texts can change without changing this group: check reads the crate store, not the App tree.
    shutil.rmtree(repo / 'app/packaging/notices/transitive')
    assert crates.check(repo)['locks']['codex']['held'] == 23
    edit(repo, crates.ASSOCIATIONS, lambda v: next(e for e in v['app_texts'] if e['reading_required']).update(reading_required=False))
    with pytest.raises(ValueError, match='reading requirement'):
        crates.check(repo)


# Publisher texts already held, associated to registry packages (registry_sources); invented edits of the committed group.
def publisher(v, name):
    return next(e for e in v['registry_sources'] if any(p['name'] == name for p in e['packages']))


def test_publisher_texts_ship_with_their_basis_and_objc2_ones_stay_held():
    rows = {(r['name'], r['version']): r for r in crates.packages(ROOT)['packages'] if r['lock'] == 'codex'}
    rtc = rows[('rtc-dtls', '0.20.3')]
    assert rtc['standing'] == 'text' and [t['publisher_text'] for t in rtc['texts']] == ['LICENSE-APACHE', 'LICENSE-MIT']
    assert rtc['repository'] == 'https://github.com/webrtc-rs/rtc' and 'saved listing' in rtc['basis']
    # The reading requirement follows the resolved route: the objc2 repository's text is held, whichever route ships it.
    for key in (('objc2', '0.6.3'), ('dispatch2', '0.3.0'), ('objc2-core-graphics', '0.3.2'), ('block2', '0.6.2')):
        assert rows[key]['standing'] == 'held' and rows[key]['texts'] and 'owner licence reading' in rows[key]['reason']


def test_a_publisher_text_association_needs_a_held_text_bound_to_its_listing(repo):
    edit(repo, crates.ASSOCIATIONS, lambda v: publisher(v, 'rtc-dtls').update(texts=[]))
    with pytest.raises(ValueError, match='at least one text'):
        crates.check(repo)


@pytest.mark.parametrize('change, message', [
    (lambda t: t.update(sha256='0' * 64), 'not held through another route'),
    (lambda t: t.update(size_bytes=t['size_bytes'] + 1, listing_size=t['size_bytes'] + 1), 'not held through another route'),
    (lambda t: t.update(listing_blob='0' * 40), 'not the blob and size its listing names'),
    (lambda t: t.update(listing_size=1), 'not the blob and size its listing names'),
    (lambda t: t.update(git_blob_sha1='0' * 40, listing_blob='0' * 40), 'differs from the blob its listing names'),
])
def test_a_changed_publisher_text_or_source_identity_refuses(repo, change, message):
    edit(repo, crates.ASSOCIATIONS, lambda v: change(publisher(v, 'rtc-dtls')['texts'][0]))
    with pytest.raises(ValueError, match=message):
        crates.check(repo)


@pytest.mark.parametrize('change, message', [
    (lambda e: e.update(revision='not-a-revision'), 'publisher repository, revision and basis'),
    (lambda e: e.update(repository='https://example.invalid/rtc'), 'publisher repository, revision and basis'),
    (lambda e: e.update(basis=''), 'publisher repository, revision and basis'),
    (lambda e: e.update(invented='x'), 'unknown registry-source association shape'),
])
def test_a_publisher_association_needs_its_source_identity(repo, change, message):
    edit(repo, crates.ASSOCIATIONS, lambda v: change(publisher(v, 'rtc-dtls')))
    with pytest.raises(ValueError, match=message):
        crates.check(repo)


def test_changed_checksum_unused_and_conflicting_associations_refuse(repo):
    import shutil
    pristine = repo.parent / 'pristine'
    shutil.copytree(repo / 'app/packaging/supplier_notices', pristine)

    def reset():
        shutil.rmtree(repo / 'app/packaging/supplier_notices')
        shutil.copytree(pristine, repo / 'app/packaging/supplier_notices')

    edit(repo, crates.ASSOCIATIONS, lambda v: publisher(v, 'rtc-dtls')['packages'][0].update(checksum='0' * 64))
    with pytest.raises(ValueError, match='names no locked package without another text route'):
        crates.check(repo)
    reset()
    invented = {'name': 'invented-crate', 'version': '1.0.0', 'checksum': '1' * 64, 'path_in_vcs': '', 'archive_metadata': {}}
    edit(repo, crates.ASSOCIATIONS, lambda v: publisher(v, 'rtc-dtls')['packages'].append(invented))
    with pytest.raises(ValueError, match='names no locked package without another text route'):
        crates.check(repo)
    reset()
    # The same package in two publisher associations.
    edit(repo, crates.ASSOCIATIONS, lambda v: v['registry_sources'].append(json_copy(publisher(v, 'rtc-dtls'))))
    with pytest.raises(ValueError, match='two registry-source associations'):
        crates.check(repo)
    reset()
    # A package whose archive carries its notices cannot take a second route.
    def second_route(v):
        index = json.loads((repo / crates.INDEX).read_text())
        row = next(r for r in index['registry'] if r['notices'] and 'codex' in r['locks'])
        publisher(v, 'rtc-dtls')['packages'].append({'name': row['package'], 'version': row['version'], 'checksum': row['checksum'],
                                                     'path_in_vcs': '', 'archive_metadata': {}})
    edit(repo, crates.ASSOCIATIONS, second_route)
    with pytest.raises(ValueError, match='more than one text route'):
        crates.check(repo)
    reset()
    # A package with a text route cannot also be recorded open or absent.
    for collection in ('gap_reasons', 'no_publisher_text', 'not_in_macos_package'):
        def mark(v, c=collection):
            target = publisher(v, 'rtc-dtls')['packages'][0]
            entry = json_copy(v[c][0])
            ident = {k: target[k] for k in ('name', 'version', 'checksum')}
            if 'packages' in entry:
                entry['packages'] = [ident]
            else:
                entry.update(ident)
            v[c].append(entry)
        edit(repo, crates.ASSOCIATIONS, mark)
        with pytest.raises(ValueError, match='has a text route and is also named'):
            crates.check(repo)
        reset()


def json_copy(value):
    return json.loads(json.dumps(value))



# Absence from the macOS package (not_in_macos_package): checked against the lockfile and a closed set of target forms.
def absent(v, name):
    return next(e for e in v['not_in_macos_package'] if e['name'] == name)


def test_six_packages_are_absent_by_declared_target_condition_and_named_with_their_evidence():
    rows = [r for r in crates.packages(ROOT)['packages'] if r['standing'] == 'not-in-macos-package']
    assert sorted((r['name'], r['version']) for r in rows) == [
        ('linux-keyutils', '0.2.4'), ('rustls-platform-verifier-android', '0.1.1'), ('socks5-protocol', '0.3.5'),
        ('winapi-i686-pc-windows-gnu', '0.4.0'), ('winapi-x86_64-pc-windows-gnu', '0.4.0'), ('winsplit', '0.1.0')]
    for row in rows:
        assert not row['texts'] and row['absence']['target'] == 'aarch64-apple-darwin'
        for dependent in row['absence']['reverse_dependencies']:
            assert dependent['edges'] and ('archive_manifest' in dependent or 'workspace_manifest' in dependent)
    socks = next(r for r in rows if r['name'] == 'socks5-protocol')
    assert [e['kind'] for d in socks['absence']['reverse_dependencies'] for e in d['edges']] == ['dev']


@pytest.mark.parametrize('table, expected', [
    ('[target.\'cfg(target_os = "linux")\'.dependencies]', (False, 'normal', None)),
    ('[target.\'cfg(target_os = "macos")\'.dependencies]', (True, 'normal', None)),
    ('[target.\'cfg(windows)\'.dev-dependencies]', (False, 'dev', None)),
    ('[target.i686-pc-windows-gnu.dependencies.winapi-i686-pc-windows-gnu]', (False, 'normal', 'winapi-i686-pc-windows-gnu')),
    ('[target.aarch64-apple-darwin.build-dependencies]', (True, 'build', None)),
])
def test_target_conditions_in_the_closed_forms(table, expected):
    assert crates.target_holds(table) == expected


@pytest.mark.parametrize('table, message', [
    ('[target.\'cfg(unix)\'.dependencies]', 'outside the closed forms'),
    ('[target.\'cfg(not(target_os = "macos"))\'.dependencies]', 'outside the closed forms'),
    ('[target.\'cfg(all(windows, target_env = "gnu"))\'.dependencies]', 'outside the closed forms'),
    ('[dependencies]', 'not a target-specific dependency table'),
    ('[target.\'cfg(windows)\'.features]', 'not a target-specific dependency table'),
])
def test_unknown_target_forms_refuse(table, message):
    with pytest.raises(ValueError, match=message):
        crates.target_holds(table)


@pytest.mark.parametrize('change, message', [
    # An incomplete, extra or repeated reverse-dependency set.
    (lambda e: e['reverse_dependencies'].clear(), 'differ from the lockfile'),
    (lambda e: e['reverse_dependencies'].append({**e['reverse_dependencies'][0], 'name': 'invented'}), 'differ from the lockfile'),
    (lambda e: e['reverse_dependencies'].append(json_copy(e['reverse_dependencies'][0])), 'differ from the lockfile'),
    # An unknown target form, or a condition that holds for macOS.
    (lambda e: e['reverse_dependencies'][0]['edges'][0].update(table='[target.\'cfg(unix)\'.dependencies]'), 'outside the closed forms'),
    (lambda e: e['reverse_dependencies'][0]['edges'][0].update(table='[target.\'cfg(target_os = "macos")\'.dev-dependencies]'),
     'is declared for aarch64-apple-darwin'),
    (lambda e: e['reverse_dependencies'][0]['edges'][0].update(table='[dependencies]'), 'not a target-specific'),
    (lambda e: e['reverse_dependencies'][0]['edges'].append({**e['reverse_dependencies'][0]['edges'][0],
                                                             'table': '[target.\'cfg(target_os = "macos")\'.dev-dependencies]'}),
     'is declared for aarch64-apple-darwin'),
    # The edge must name the package and its kind must be its table's.
    (lambda e: e['reverse_dependencies'][0]['edges'][0].update(text='invented = "0.1"'), 'does not name the package'),
    (lambda e: e['reverse_dependencies'][0]['edges'][0].update(kind='normal'), 'edge kind differs'),
    (lambda e: e['reverse_dependencies'][0]['edges'].clear(), 'records no edge'),
    # The manifest must be at the lockfile's repository and revision.
    (lambda e: e['reverse_dependencies'][0]['workspace_manifest'].update(revision='0' * 40), 'not at the lockfile'),
    (lambda e: e.update(target='x86_64-apple-darwin'), 'unknown not-in-macOS-package shape'),
])
def test_workspace_edge_evidence_must_establish_absence(repo, change, message):
    edit(repo, crates.ASSOCIATIONS, lambda v: change(absent(v, 'socks5-protocol')))
    with pytest.raises(ValueError, match=message):
        crates.check(repo)


@pytest.mark.parametrize('change, message', [
    (lambda e: e['reverse_dependencies'][0]['archive_manifest'].update(checksum='0' * 64), 'not the locked archive'),
    (lambda e: e['reverse_dependencies'][0]['edges'][0].update(
        table='[target.aarch64-apple-darwin.dependencies.winapi-x86_64-pc-windows-gnu]',
        text='[target.aarch64-apple-darwin.dependencies.winapi-x86_64-pc-windows-gnu]'), 'is declared for aarch64-apple-darwin'),
    (lambda e: e['reverse_dependencies'][0]['edges'][0].update(
        table='[target.x86_64-pc-windows-gnu.dependencies.winapi]', text='[target.x86_64-pc-windows-gnu.dependencies.winapi]'),
     'names another package'),
    (lambda e: e.update(checksum='0' * 64), 'names a package no lockfile locks with that checksum'),
])
def test_archive_edge_evidence_must_establish_absence(repo, change, message):
    edit(repo, crates.ASSOCIATIONS, lambda v: change(absent(v, 'winapi-x86_64-pc-windows-gnu')))
    with pytest.raises(ValueError, match=message):
        crates.check(repo)


def test_an_excluded_package_named_twice_or_also_open_refuses(repo):
    def both(v):
        entry = absent(v, 'winsplit')
        v['gap_reasons'].append({'packages': [{k: entry[k] for k in ('name', 'version', 'checksum')}], 'reason': 'INVENTED',
                                 'would_close': 'INVENTED'})
    edit(repo, crates.ASSOCIATIONS, both)
    with pytest.raises(ValueError, match='not_in_macos_package and gap_reasons both name'):
        crates.check(repo)


# A stated licence with no publisher text found is its own open standing; it never counts as a text.
def test_no_publisher_text_packages_ship_nothing_and_stay_open():
    rows = [r for r in crates.packages(ROOT)['packages'] if r['standing'] == 'no-publisher-text']
    assert sorted(r['name'] for r in rows) == ['crc32c', 'debugserver-types', 'deno_core_icudata', 'eventsource-stream', 'fax',
                                               'fax_derive', 'fxhash', 'io_tee']
    for row in rows:
        assert not row['texts'] and row['declared_license'] and 'owner\'s decision' in row['would_close']
    assert 'no-publisher-text' in crates.OPEN
    crc = next(r for r in rows if r['name'] == 'crc32c')
    assert 'zlib' in crc['reason'] and 'src/combine.rs' in crc['reason']
    fxhash = next(r for r in rows if r['name'] == 'fxhash')
    assert fxhash['revision'] is None and 'only a candidate' in fxhash['reason']


def test_unused_open_or_absent_associations_refuse(repo):
    for collection in ('no_publisher_text', 'not_in_macos_package', 'gap_reasons'):
        def unused(v, c=collection):
            entry = json_copy(v[c][0])
            invented = {'name': 'invented-crate', 'version': '1.0.0', 'checksum': '1' * 64}
            if 'packages' in entry:
                entry['packages'] = [invented]
            else:
                entry.update(invented)
            v[c].append(entry)
        saved = (repo / crates.ASSOCIATIONS).read_bytes()
        edit(repo, crates.ASSOCIATIONS, unused)
        with pytest.raises(ValueError, match=collection + ' names a package no lockfile locks with that checksum'):
            crates.check(repo)
        (repo / crates.ASSOCIATIONS).write_bytes(saved)


# The supplier's voice records (supplier_notices/voice.py), on invented records only.

voice_spec = importlib.util.spec_from_file_location('voice_records', ROOT / 'app/packaging/supplier_notices/voice.py')
voice = importlib.util.module_from_spec(voice_spec)
voice_spec.loader.exec_module(voice)

PIN = '9.9.9'
COMMIT = 'c' * 40
LIB_A = 'codex-resources/voice/lib/liba.dylib'
LIB_B = 'codex-resources/voice/lib/libb.dylib'
TEXT_A = 'codex-resources/voice/licenses/a.txt'
TEXT_B = 'codex-resources/voice/licenses/b.txt'
FILES = {LIB_A: b'invented library a', LIB_B: b'invented library b', TEXT_A: b'invented licence a', TEXT_B: b'invented licence b'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source(name, version, role='native-library'):
    return {'name': name, 'version': version, 'role': role, 'archive': f'{name}-{version}.tar', 'root': f'{name}-{version}',
            'url': f'https://example.invalid/{name}-{version}.tar.gz', 'sha256': sha(name.encode()), 'provenance': 'invented'}


def sources():
    return {'schema_version': 1, 'sources': [source('tool', '1.0', 'build-tool'), source('liba', '1.2'), source('libb', '3.4')],
            'bundled_sources': [{'name': 'inner', 'included_by': 'liba', 'revision': 'd' * 40, 'path': 'sub/inner',
                                 'provenance': 'invented'}]}


def manifest():
    return {'schemaVersion': 1, 'buildCommit': COMMIT, 'appTarget': voice.SUPPORTED_TARGET, 'voiceTarget': voice.SUPPORTED_TARGET,
            'appVersion': PIN, 'sha256': {path: sha(raw) for path, raw in FILES.items()}}


def rows():
    return [{'id': 'liba', 'version': '1.2', 'repository': 'https://example.invalid/liba-1.2.tar.gz', 'members': [LIB_A],
             'supplier_tree_texts': [TEXT_A]},
            {'id': 'libb', 'version': '3.4', 'repository': 'https://example.invalid/libb-3.4.tar.gz', 'members': [LIB_B],
             'supplier_tree_texts': [TEXT_B]}]


def encode(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def record(sources_raw, manifest_raw):
    entries = [{'path': p, 'kind': 'file', 'size': len(raw), 'sha256': sha(raw)} for p, raw in FILES.items()]
    entries += [{'path': voice.MEMBERS['sources.json'], 'kind': 'file', 'size': len(sources_raw), 'sha256': sha(sources_raw)},
                {'path': voice.MEMBERS['manifest.json'], 'kind': 'file', 'size': len(manifest_raw), 'sha256': sha(manifest_raw)}]
    return {'pin': PIN, 'source_commit': COMMIT, 'package_metadata': {'target': voice.SUPPORTED_TARGET},
            'inventory': {'entries': entries}}


def held(repo, sources_raw, manifest_raw):
    folder = repo / voice.RECORDS / PIN
    folder.mkdir(parents=True)
    (folder / 'sources.json').write_bytes(sources_raw)
    (folder / 'manifest.json').write_bytes(manifest_raw)
    return folder


def test_matching_records_establish_each_row(tmp_path):
    s, m = encode(sources()), encode(manifest())
    held(tmp_path, s, m)
    result = voice.establish(tmp_path, PIN, record(s, m), rows())
    assert result['rows'] == {'liba': {'version': '1.2', 'url': 'https://example.invalid/liba-1.2.tar.gz', 'sources_entry': 'liba'},
                              'libb': {'version': '3.4', 'url': 'https://example.invalid/libb-3.4.tar.gz', 'sources_entry': 'libb'}}
    assert sorted(result['records']) == ['manifest.json', 'sources.json']


def test_no_records_for_the_pin_establish_nothing(tmp_path):
    s, m = encode(sources()), encode(manifest())
    assert voice.establish(tmp_path, PIN, record(s, m), rows()) is None


@pytest.mark.parametrize('change, message', [
    ('changed-copy', 'differs from codex-resources/voice/sources.json'),
    ('link', 'regular non-link'),
    ('extra-file', 'holds other files'),
    ('record-size', 'differs from codex-resources/voice/manifest.json'),
])
def test_file_identity_must_equal_the_distribution_record(tmp_path, change, message):
    s, m = encode(sources()), encode(manifest())
    distribution = record(s, m)
    folder = held(tmp_path, s, m)
    if change == 'changed-copy':
        (folder / 'sources.json').write_bytes(s.replace(b'1.2', b'1.3'))
    elif change == 'link':
        target = tmp_path / 'elsewhere.json'
        target.write_bytes(s)
        (folder / 'sources.json').unlink()
        (folder / 'sources.json').symlink_to(target)
    elif change == 'extra-file':
        (folder / 'notes.txt').write_bytes(b'invented')
    else:
        next(e for e in distribution['inventory']['entries'] if e['path'] == voice.MEMBERS['manifest.json'])['size'] += 1
    with pytest.raises(ValueError, match=message):
        voice.establish(tmp_path, PIN, distribution, rows())


def compare(sources_value=None, manifest_value=None, row_values=None, distribution=None, pin=PIN):
    s = sources_value if isinstance(sources_value, bytes) else encode(sources_value or sources())
    m = manifest_value if isinstance(manifest_value, bytes) else encode(manifest_value or manifest())
    return voice.compare(s, m, pin, distribution or record(s, m), row_values or rows())


def edited(make, change):
    value = make()
    change(value)
    return value


def test_ordinary_comparison_passes():
    assert set(compare()) == {'liba', 'libb'}


@pytest.mark.parametrize('manifest_change, message', [
    (lambda v: v.update(appVersion='9.9.8'), 'not the pin'),
    (lambda v: v.update(buildCommit='e' * 40), 'not the distribution record\'s source commit'),
    (lambda v: v.update(appTarget='x86_64-apple-darwin'), 'another target'),
    (lambda v: v.update(voiceTarget='aarch64-unknown-linux-gnu'), 'another target'),
    (lambda v: v['sha256'].update({LIB_A: 'f' * 64}), 'a digest the distribution record does not have'),
    (lambda v: v['sha256'].update({'codex-resources/voice/lib/invented.dylib': 'f' * 64}), 'a digest the distribution record'),
    (lambda v: v['sha256'].pop(TEXT_B), 'files the supplier manifest does not list'),
    (lambda v: v.update(extra='invented'), 'unsupported shape'),
])
def test_manifest_must_agree_with_the_pin_commit_target_and_inventory(manifest_change, message):
    value = edited(manifest, manifest_change)
    s, m = encode(sources()), encode(value)
    distribution = record(s, m)
    # The record's digests stay the invented files' own, so a changed manifest digest is a disagreement.
    with pytest.raises(ValueError, match=message):
        voice.compare(s, m, PIN, distribution, rows())


def test_the_record_must_be_for_the_pin_and_supported_target():
    s, m = encode(sources()), encode(manifest())
    for change in (lambda r: r.update(pin='9.9.8'), lambda r: r['package_metadata'].update(target='x86_64-apple-darwin')):
        distribution = record(s, m)
        change(distribution)
        with pytest.raises(ValueError, match='not for the declared pin and supported target'):
            voice.compare(s, m, PIN, distribution, rows())


@pytest.mark.parametrize('sources_change, row_change, message', [
    # A native-library version or URL that differs from the row.
    (lambda v: v['sources'][1].update(version='1.3'), None, 'states liba 1.3, the table liba 1.2'),
    (lambda v: v['sources'][1].update(url='https://example.invalid/other.tar.gz'), None, 'states the source of liba'),
    (None, lambda r: r[1].update(version='3.5'), 'states libb 3.4, the table libb 3.5'),
    # An omitted entry, an entry no row accounts for, and duplicate or conflicting entries.
    (lambda v: v['sources'].pop(2), None, 'states the source of libb'),
    (lambda v: v['sources'].append(source('libc', '5.6')), None, 'no voice row accounts for: libc'),
    (lambda v: v['sources'].append(copy.deepcopy(v['sources'][1])), None, 'names one native library name twice'),
    (lambda v: v['sources'].append({**source('liba', '9.9'), 'url': 'https://example.invalid/liba-1.2.tar.gz'}), None,
     'names one native library name twice'),
    (lambda v: v['sources'].append({**source('liba2', '9.9'), 'url': 'https://example.invalid/liba-1.2.tar.gz'}), None,
     'names one native library url twice'),
    # A build tool does not establish a row.
    (lambda v: v['sources'][1].update(role='build-tool'), None, 'states the source of liba'),
    # Unsupported shapes.
    (lambda v: v['sources'][1].update(extra='x'), None, 'unsupported source entry'),
    (lambda v: v['sources'][1].update(role='plugin'), None, 'unsupported source entry'),
    (lambda v: v.update(schema_version=2), None, 'unsupported shape'),
])
def test_each_row_is_established_by_exactly_one_native_library_entry(sources_change, row_change, message):
    value = edited(sources, sources_change) if sources_change else sources()
    row_values = edited(rows, row_change) if row_change else rows()
    with pytest.raises(ValueError, match=message):
        compare(value, row_values=row_values)


def test_a_row_member_must_be_listed_by_the_supplier_manifest():
    row_values = edited(rows, lambda r: r[0]['members'].append('codex-resources/voice/lib/invented.dylib'))
    with pytest.raises(ValueError, match='files the supplier manifest does not list'):
        compare(row_values=row_values)


@pytest.mark.parametrize('raw, which', [
    (b'{"schema_version": 1, "schema_version": 1, "sources": [], "bundled_sources": []}', 'sources'),
    (encode(sources()).replace(b'"name": "liba",', b'"name": "liba", "name": "liba",'), 'sources'),
    (encode(manifest()).replace(b'"appVersion": "9.9.9",', b'"appVersion": "9.9.9", "appVersion": "9.9.9",'), 'manifest'),
    (b'not json', 'sources'),
])
def test_repeated_keys_or_invalid_json_refuse(raw, which):
    kwargs = {'sources_value': raw} if which == 'sources' else {'manifest_value': raw}
    with pytest.raises(ValueError, match='repeats a key|is not JSON'):
        compare(**kwargs)
