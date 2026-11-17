"""Invented archives for the notice-only crate route (supplier_notices/crate_notices.py)."""
import gzip
import hashlib
import importlib.util
import io
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
    assert result['locks']['codex'] == {'packages': 1483, 'registry': 1296, 'git': 14, 'path': 173, 'text': 1340, 'held': 5, 'gap': 138}
    assert result['locks']['ripgrep'] == {'packages': 59, 'registry': 49, 'git': 0, 'path': 10, 'text': 59, 'held': 0, 'gap': 0}
    value = crates.packages(ROOT)
    assert 'Some may not be compiled into the macOS executables' in value['superset']
    for row in value['packages']:
        assert (row['standing'] == 'gap') == (not row['texts'])
        assert row['standing'] != 'gap' or (row['reason'] and row['would_close'])


def test_lockfile_drift_refuses(repo):
    lock = repo / crates.BASE / 'locks/codex-rs.Cargo.lock'
    lock.write_bytes(lock.read_bytes().replace(b'name = "zstd"', b'name = "zstdx"', 1))
    with pytest.raises(ValueError, match='lockfile differs'):
        crates.check(repo)


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
    assert crates.check(repo)['locks']['codex']['held'] == 5
    edit(repo, crates.ASSOCIATIONS, lambda v: next(e for e in v['app_texts'] if e['reading_required']).update(reading_required=False))
    with pytest.raises(ValueError, match='reading requirement'):
        crates.check(repo)
