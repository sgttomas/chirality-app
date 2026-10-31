"""Verify bounded cached SQLite source preparation, never extract or execute it."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import tomllib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def require(condition):
    if not condition:
        raise ValueError("SQLite notice input correspondence refused")


def check(archive=None):
    index = json.loads((HERE / 'index.json').read_bytes())
    require(index['format'] == 'sqlite-notice-preparation/1')
    package = next(p for p in tomllib.loads((ROOT / 'app/src-tauri/Cargo.lock').read_text())['package']
                   if p['name'] == index['crate'] and p['version'] == index['crate_version'])
    require(package['checksum'] == index['archive_sha256'])
    require({a['path'] for a in index['assets']} == {'libsqlite3-sys.LICENSE', 'sqlite3-source-header.txt'})
    for asset in index['assets']:
        raw = (HERE / asset['path']).read_bytes()
        require(len(raw) == asset['size'] and hashlib.sha256(raw).hexdigest() == asset['sha256'])
    if archive:
        data = Path(archive).read_bytes()
        require(len(data) == index['archive_size'] and hashlib.sha256(data).hexdigest() == index['archive_sha256'])
        with tarfile.open(archive) as tar:
            for asset in index['assets']:
                member = tar.getmember(asset['archive_member'])
                require(member.isfile())
                raw = tar.extractfile(member).read()
                require(hashlib.sha256(raw).hexdigest() == asset['full_member_sha256'])
                require(raw[asset['offset']:asset['offset'] + asset['size']] == (HERE / asset['path']).read_bytes())
            for member, key in [('Cargo.toml', 'manifest_sha256'), ('build.rs', 'build_rs_sha256')]:
                raw = tar.extractfile(f"libsqlite3-sys-{index['crate_version']}/{member}").read()
                require(hashlib.sha256(raw).hexdigest() == index[key])
    return {'assets_match': True, 'archive_checked': archive is not None, 'sqlite_version': index['sqlite_version'],
            'standing': 'source preparation only; no compiled inclusion, license approval or transitive completeness'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive')
    args = parser.parse_args()
    print(json.dumps(check(args.archive)))
