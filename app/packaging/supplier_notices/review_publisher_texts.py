#!/usr/bin/env python3
"""A reviewer's aid, not a CI check: the review-duty comparison for every publisher-text association.

    python3 -I app/packaging/supplier_notices/review_publisher_texts.py --archives MAP.json --listings DIR

For each package of `crates/associations.json` `registry_sources` it prints one line, `OK` or `MISMATCH` with what
differs. It compares the recorded values with the held evidence the checker does not read:

- the archive the lockfile locks (MAP.json maps `<name>-<version>.crate` to its absolute path). Each archive is read
  through `crate_notices.read_member`: its SHA-256 must equal the lockfile checksum before it is opened, its tar headers
  pass the route's checks, and only `.cargo_vcs_info.json` and `Cargo.toml` are read. Their sizes and SHA-256 must equal
  `archive_metadata`; the VCS record's revision must equal `archive_vcs_revision`; its `path_in_vcs` must equal the
  recorded one, or be absent where the recorded one is null (which then needs `path_basis`); the manifest's
  `package.repository` must equal `archive_repository` exactly, or be absent where that is null.
- the saved listing in DIR whose SHA-256 is the association's `response_sha256`: not truncated, with `entries` entries;
  each text is the blob and size the listing names at its path; and the texts are exactly the notice-named files of the
  package folder (its own files and those in a licence folder), or of the root where the folder holds none. Where the
  path is null, every folder with a Cargo.toml must give that same selection.

Nothing is extracted, executed or written; no network is used.
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
            problems = []
            checksum = locked.get((name, version))
            if checksum != package['checksum']:
                problems.append(f'lockfile checksum {checksum}, recorded {package["checksum"]}')
            else:
                raw = Path(archive_map[f'{name}-{version}.crate']).read_bytes()
                members = {m: route.read_member(raw, (name, version), checksum, m) for m in ('.cargo_vcs_info.json', 'Cargo.toml')}
                for member, data in members.items():
                    found = {'size_bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                    if found != package['archive_metadata'][member]:
                        problems.append(f'{member} is {found}, recorded {package["archive_metadata"][member]}')
                vcs = json.loads(members['.cargo_vcs_info.json'])
                if vcs.get('git', {}).get('sha1') != package['archive_vcs_revision']:
                    problems.append(f'VCS revision {vcs.get("git", {}).get("sha1")}, recorded {package["archive_vcs_revision"]}')
                if vcs.get('path_in_vcs') != package['path_in_vcs']:
                    problems.append(f'path_in_vcs {vcs.get("path_in_vcs", "(absent)")!r}, recorded {package["path_in_vcs"]!r}')
                stated = tomllib.loads(members['Cargo.toml'].decode()).get('package', {}).get('repository')
                if stated != package['archive_repository']:
                    problems.append(f'manifest repository {stated!r}, recorded {package["archive_repository"]!r}')
            if listing is None:
                problems.append('no saved listing has the recorded response SHA-256')
            else:
                tree = listing['tree']
                if listing.get('truncated') is not False or len(tree) != entry['listing']['entries']:
                    problems.append(f'listing truncated {listing.get("truncated")} with {len(tree)} entries, recorded '
                                    f'{entry["listing"]["entries"]}')
                by_path = {e['path']: e for e in tree}
                for text in entry['texts']:
                    item = by_path.get(text['source_path'], {})
                    if (item.get('type'), item.get('sha'), item.get('size')) != ('blob', text['git_blob_sha1'], text['size_bytes']):
                        problems.append(f'{text["source_path"]} is {item.get("sha")} ({item.get("size")}) in the listing')
                recorded = {t['source_path'] for t in entry['texts']}
                if package['path_in_vcs'] is None:
                    folders = sorted({e['path'].rpartition('/')[0] for e in tree if e['path'].split('/')[-1] == 'Cargo.toml'})
                    choices = {f or '(root)': sorted(selected(tree, f)) for f in folders}
                    if any(set(c) != recorded for c in choices.values()):
                        problems.append(f'path omitted; the folders with a Cargo.toml select {choices}')
                elif selected(tree, package['path_in_vcs']) != recorded:
                    problems.append(f'selection {sorted(selected(tree, package["path_in_vcs"]))}, recorded {sorted(recorded)}')
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
