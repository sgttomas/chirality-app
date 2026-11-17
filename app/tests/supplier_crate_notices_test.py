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
