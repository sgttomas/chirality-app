#!/usr/bin/env python3
"""A reviewer's aid, not a CI check: the review-duty comparison for every publisher-text association.

    python3 -I app/packaging/supplier_notices/review_publisher_texts.py --archives MAP.json --listings DIR

For each package of `crates/associations.json` `registry_sources` it prints one line, `OK` or `MISMATCH` with what
differs. It compares these recorded values with the held evidence the checker does not read, and nothing else:

- the archive's stated values. MAP.json maps `<name>-<version>.crate` to the archive; its SHA-256 must equal the
  lockfile checksum before it is opened (`crate_notices.read_member`, which also applies the route's header checks), and
  only `.cargo_vcs_info.json` and `Cargo.toml` are read. Their sizes and SHA-256 must equal `archive_metadata`; the VCS
  record's revision must equal `archive_vcs_revision`; its `path_in_vcs` must equal the recorded one, and a recorded
  null must be a VCS record with no `path_in_vcs` key (an explicit null in the record is a mismatch); the manifest's
  `package.repository` must equal `archive_repository` exactly, or be absent where that is null.
- the listing's blob and size at each selected path. The saved listing in DIR whose SHA-256 is `response_sha256` must
  not be truncated and must have `entries` entries, and each text must be the blob and size it names at `source_path`.
- the selection. The texts must be exactly the notice-named files of the package folder (its own files and those in a
  licence folder directly below), or of the root where the folder holds none. Where the path is null, the listing must
  have at least one folder holding a `Cargo.toml` file (an entry of type blob), and every such folder must give that
  same selection.
- the stored bytes. Each text's bytes, held in `crates/texts/<sha256>`, must have the recorded size, SHA-256 and Git blob.

It does not read a `path_basis`: that is prose a reviewer reads against the listing. Nothing is extracted, executed or
written; no network is used.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


crates = load_module('review_aid_crates', HERE / 'crates.py')
route = crates.route


def selection(tree, folder):
    """The notice-named files of a folder: its own files, and those in a licence folder directly below it."""
    prefix = folder + '/' if folder else ''
    chosen = set()
    for entry in tree:
        if entry.get('type') != 'blob' or not entry['path'].startswith(prefix):
            continue
        parts = entry['path'][len(prefix):].split('/')
        if (len(parts) == 1 or (len(parts) == 2 and route.NOTICE_FOLDER.match(parts[0]))) and route.is_notice(entry['path']):
            chosen.add(entry['path'])
    return chosen


def selected(tree, folder):
    own = selection(tree, folder)
    return own if own or not folder else selection(tree, '')


def listings(folder):
    found = {}
    for path in sorted(Path(folder).iterdir()):
        if path.is_file() and not path.is_symlink() and path.suffix == '.json':
            found[hashlib.sha256(path.read_bytes()).hexdigest()] = path
    return found


def manifest_folders(tree):
    """The folders holding a file named Cargo.toml: entries of type blob only (a directory named Cargo.toml is not one)."""
    return sorted({e['path'].rpartition('/')[0] for e in tree if e.get('type') == 'blob' and e['path'].split('/')[-1] == 'Cargo.toml'})


def compare(repo, entry, package, members, listing):
    """What differs between one package's recorded values and the held evidence given: `members` maps
    `.cargo_vcs_info.json` and `Cargo.toml` to the bytes read from its archive, and `listing` is the saved listing (None
    where none has the recorded SHA-256). Returns the list of differences, empty when there are none."""
    problems = []
    for member, data in members.items():
        found = {'size_bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        if found != package['archive_metadata'][member]:
            problems.append(f'{member} is {found}, recorded {package["archive_metadata"][member]}')
    vcs = json.loads(members['.cargo_vcs_info.json'])
    if vcs.get('git', {}).get('sha1') != package['archive_vcs_revision']:
        problems.append(f'VCS revision {vcs.get("git", {}).get("sha1")}, recorded {package["archive_vcs_revision"]}')
    if package['path_in_vcs'] is None:
        if 'path_in_vcs' in vcs:
            problems.append(f'path_in_vcs {vcs["path_in_vcs"]!r} is stated in the VCS record, recorded null')
    elif vcs.get('path_in_vcs') != package['path_in_vcs']:
        problems.append(f'path_in_vcs {vcs.get("path_in_vcs", "(absent)")!r}, recorded {package["path_in_vcs"]!r}')
    stated = tomllib.loads(members['Cargo.toml'].decode()).get('package', {}).get('repository')
    if stated != package['archive_repository']:
        problems.append(f'manifest repository {stated!r}, recorded {package["archive_repository"]!r}')
    for text in entry['texts']:
        stored = Path(repo) / crates.TEXTS / text['sha256']
        raw = stored.read_bytes() if stored.is_file() and not stored.is_symlink() else None
        if raw is None or (len(raw), hashlib.sha256(raw).hexdigest(), crates.git_blob(raw)) != (
                text['size_bytes'], text['sha256'], text['git_blob_sha1']):
            problems.append(f'{text["source_path"]}: the stored bytes are not the recorded size, digest and blob')
    if listing is None:
        problems.append('no saved listing has the recorded response SHA-256')
        return problems
    tree = listing['tree']
    if listing.get('truncated') is not False or len(tree) != entry['listing']['entries']:
        problems.append(f'listing truncated {listing.get("truncated")} with {len(tree)} entries, recorded {entry["listing"]["entries"]}')
    by_path = {e['path']: e for e in tree}
    for text in entry['texts']:
        item = by_path.get(text['source_path'], {})
        if (item.get('type'), item.get('sha'), item.get('size')) != ('blob', text['git_blob_sha1'], text['size_bytes']):
            problems.append(f'{text["source_path"]} is {item.get("sha")} ({item.get("size")}) in the listing')
    recorded = {t['source_path'] for t in entry['texts']}
    if package['path_in_vcs'] is None:
        folders = manifest_folders(tree)
        choices = {f or '(root)': sorted(selected(tree, f)) for f in folders}
        if not folders:
            problems.append('path omitted and the listing has no folder holding a Cargo.toml file')
        elif any(set(c) != recorded for c in choices.values()):
            problems.append(f'path omitted; the folders with a Cargo.toml select {choices}')
    elif selected(tree, package['path_in_vcs']) != recorded:
        problems.append(f'selection {sorted(selected(tree, package["path_in_vcs"]))}, recorded {sorted(recorded)}')
    return problems


def review(repo, archives, folder):
    associations = crates.load_associations(repo)
    locked = {}
    for lock in associations['locks']:
        for key, package in crates.locked(repo, lock).items():
            if crates.kind(package) == 'registry':
                locked[key] = package['checksum']
    archive_map = crates.archive_map(archives)
    saved = listings(folder)
    lines, failures = [], 0
    for entry in associations['registry_sources']:
        raw_listing = saved.get(entry['listing']['response_sha256'])
        listing = json.loads(raw_listing.read_bytes()) if raw_listing else None
        for package in entry['packages']:
            name, version = package['name'], package['version']
            checksum = locked.get((name, version))
            if checksum != package['checksum']:
                problems = [f'lockfile checksum {checksum}, recorded {package["checksum"]}']
            else:
                raw = Path(archive_map[f'{name}-{version}.crate']).read_bytes()
                members = {m: route.read_member(raw, (name, version), checksum, m) for m in ('.cargo_vcs_info.json', 'Cargo.toml')}
                problems = compare(repo, entry, package, members, listing)
            failures += bool(problems)
            lines.append(('MISMATCH ' if problems else 'OK ') + f'{name} {version} ({entry["repository"]} '
                         f'{entry["revision"][:8]}, path {package["path_in_vcs"]!r})' + (': ' + '; '.join(problems) if problems else ''))
    return lines, failures


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--archives', required=True)
    parser.add_argument('--listings', required=True)
    args = parser.parse_args()
    lines, failures = review(REPO, args.archives, args.listings)
    print('\n'.join(lines))
    print(f'{len(lines)} packages, {failures} with a mismatch')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
