"""Offline exact receipt checks and explicitly selected upstream notice supplement."""
import argparse
import hashlib
import importlib.util
import json
import os
import posixpath
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location('notice_plan_io', ROOT / 'app/packaging/production_inputs/prepare.py')
io = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(io)
files, require = io.files, io.require
WORK = 'execution/PKG-01/DEL-01-06/Work/supplier-notice-associations'
LIMITS = ['upstream Git text, not an archive member', 'explicit technical selection, not legal approval',
          'transitive coverage and four supplier binary/source/notice associations remain unresolved',
          'no download, build, signing or release authority']


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def read(path):
    return files.transfer(io.inventory.anchored(path), retain=True)[0]


def blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def plan(repo=ROOT):
    repo = io.inventory.anchored(repo)
    sources = {}
    def metadata(name):
        raw = read(repo / WORK / name); sources[name] = files.sha(raw)
        return files.parse(raw)
    codex = metadata('public-metadata.json')
    mac = metadata('macos-runtime-license-metadata.json')
    entries = []
    for row in codex['proposed_file_retrieval']:
        entries.append(dict(id='codex/' + files.relative(row['path']), url=row['url'],
                            size_bytes=row['size_bytes'], git_blob_sha1=row['git_blob_sha1'], kind='source-inspection'))
    row = mac['deduplicated_retrieval_proposal']
    entries.append(dict(id='objc2/LICENSE.md', url=row['url'], size_bytes=row['size_bytes'],
                        git_blob_sha1=row['git_blob_sha1'], kind='upstream-notice'))
    require(len({e['id'] for e in entries}) == len(entries), 'duplicate receipt identity')
    index_raw = read(repo / 'app/packaging/notices/index.json')
    index = files.parse(index_raw)
    require(mac['index_sha256'] == files.sha(index_raw), 'metadata index identity differs')
    for association in mac['crate_associations']:
        component = next(c for c in index['components'] if c['ecosystem'] == 'cargo' and c['package'] == association['package'])
        gap = component['notice_gap']
        repository = gap['repository']
        require(repository.startswith('https://github.com/'), 'unsupported upstream repository locator')
        resolved = files.relative(posixpath.normpath(posixpath.join(gap['path_in_vcs'], gap['readme_license_link'])))
        expected_url = ('https://raw.githubusercontent.com/' + repository.removeprefix('https://github.com/').removesuffix('.git')
                        + '/' + gap['revision'] + '/' + resolved)
        require(association['resolved_repository_path'] == resolved and association['immutable_url'] == expected_url,
                'upstream URL or README resolution differs')
        require(component['version'] == association['version'] and component['source']['archive_sha256'] == association['archive_sha256']
                and gap['revision'] == association['vcs_revision'] and gap['path_in_vcs'] == association['path_in_vcs']
                and gap['readme_sha256'] == association['readme_sha256'] and gap['readme_license_link'] == association['readme_link']
                and association['git_blob_sha1'] == row['git_blob_sha1'] and association['size_bytes'] == row['size_bytes'],
                'upstream association differs from current indexed gap')
    require(row['url'] in {a['immutable_url'] for a in mac['crate_associations']}, 'proposal URL differs from associated source')
    return dict(format='notice-receipt-plan/1', metadata_sha256=sources, index_sha256=files.sha(index_raw),
                entries=entries, associations=mac['crate_associations'])


def verify(intake, repo=ROOT):
    intake = io.inventory.anchored(intake)
    require(intake.is_dir(), 'existing physical intake directory required')
    selected = plan(repo)
    report = dict(format='notice-local-receipts/1', plan_sha256=files.sha(encode(selected)),
                  verified=[], missing=[], errors=[], limits=LIMITS)
    for entry in selected['entries']:
        try:
            raw = read(intake / entry['id'])
            require(len(raw) == entry['size_bytes'] and blob(raw) == entry['git_blob_sha1'], 'size or Git blob differs')
            report['verified'].append(dict(entry, sha256=files.sha(raw)))
        except FileNotFoundError:
            report['missing'].append(entry['id'])
        except (ValueError, OSError):
            report['errors'].append(entry['id'])
    return report


def selected_manifest(selection, selected):
    require(isinstance(selection, dict) and set(selection) == {'format', 'plan_sha256', 'components', 'basis'}, 'closed selection required')
    require(selection['format'] == 'upstream-notice-selection/1' and selection['plan_sha256'] == files.sha(encode(selected)), 'selection plan differs')
    names = selection['components']
    require(isinstance(names, list) and names and all(isinstance(n, str) for n in names)
            and len(set(names)) == len(names), 'nonempty unique component selection required')
    require(isinstance(selection['basis'], str) and selection['basis'].strip(), 'explicit reviewed text applicability basis required')
    associations = {a['package']: a for a in selected['associations']}
    require(set(names) <= set(associations), 'component outside maintained upstream association')
    # Deliberately no free-form private basis text/paths in the bundled manifest.
    return dict(format='upstream-notice-supplement/1', plan_sha256=selection['plan_sha256'],
                selection_sha256=files.sha(encode(selection)), index_sha256=selected['index_sha256'],
                associations=[associations[n] for n in sorted(names)], limits=LIMITS)


def stage(intake, selection_path, output, repo=ROOT):
    intake, selection_path, output, repo = map(io.inventory.anchored, (intake, selection_path, output, repo))
    selected = plan(repo)
    selection_raw = read(selection_path)
    selection = files.parse(selection_raw)
    manifest = selected_manifest(selection, selected)
    entry = next(e for e in selected['entries'] if e['id'] == 'objc2/LICENSE.md')
    raw = read(intake / entry['id'])
    require(len(raw) == entry['size_bytes'] and blob(raw) == entry['git_blob_sha1'], 'selected notice receipt differs')
    manifest['asset'] = dict(entry, path='LICENSE.md', sha256=files.sha(raw))
    io.no_overlap(output.parent, [repo, intake, selection_path.parent])
    require(read(selection_path) == selection_raw and read(intake / entry['id']) == raw and plan(repo) == selected, 'inputs changed during staging')
    output.mkdir(mode=0o700)
    io.write_new(output / 'INCOMPLETE.txt', b'Incomplete notice staging. Do not consume.\n')
    contents = {'LICENSE.md': raw, 'manifest.json': encode(manifest)}
    for name, content in contents.items():
        io.write_new(output / name, content)
        fd = os.open(output / name, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            os.fchmod(fd, 0o644); os.fsync(fd)
        finally:
            os.close(fd)
    io.write_new(output / 'COMPLETE.json', encode({'files': {n: files.sha(v) for n, v in contents.items()}}))
    fd = os.open(output, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd); (output / 'INCOMPLETE.txt').unlink(); os.fsync(fd)
    finally:
        os.close(fd)
    return check_stage(output, repo)


def check_stage(output, repo=ROOT):
    output = io.inventory.anchored(output)
    require(not os.path.lexists(output / 'INCOMPLETE.txt'), 'incomplete supplement')
    require({p.name for p in output.iterdir()} == {'COMPLETE.json', 'manifest.json', 'LICENSE.md'}, 'unexpected supplement contents')
    marker = files.parse(read(output / 'COMPLETE.json'))
    require(isinstance(marker, dict) and set(marker) == {'files'} and isinstance(marker['files'], dict)
            and set(marker['files']) == {'manifest.json', 'LICENSE.md'}, 'invalid supplement marker')
    contents = {n: read(output / n) for n in marker['files']}
    require(all(stat.S_IMODE(os.stat(output / n, follow_symlinks=False).st_mode) == 0o644 for n in contents),
            'bundled notice resources require mode 0644')
    require(all(files.sha(raw) == marker['files'][n] for n, raw in contents.items()), 'supplement changed')
    manifest = files.parse(contents['manifest.json']); selected = plan(repo)
    require(isinstance(manifest, dict) and set(manifest) == {'format', 'plan_sha256', 'selection_sha256', 'index_sha256', 'associations', 'limits', 'asset'}, 'invalid public manifest')
    require(manifest['format'] == 'upstream-notice-supplement/1' and manifest['plan_sha256'] == files.sha(encode(selected))
            and manifest['index_sha256'] == selected['index_sha256'] and manifest['limits'] == LIMITS, 'supplement basis differs')
    import re
    require(isinstance(manifest['selection_sha256'], str) and re.fullmatch('[0-9a-f]{64}', manifest['selection_sha256']), 'invalid selection digest')
    associations = manifest['associations']
    require(isinstance(associations, list) and associations and all(a in selected['associations'] for a in associations), 'unknown association')
    names = [a['package'] for a in associations]
    require(names == sorted(set(names)), 'duplicate or unordered association')
    entry = next(e for e in selected['entries'] if e['id'] == 'objc2/LICENSE.md')
    raw = contents['LICENSE.md']
    require(len(raw) == entry['size_bytes'] and blob(raw) == entry['git_blob_sha1'], 'upstream text differs')
    require(manifest['asset'] == dict(entry, path='LICENSE.md', sha256=files.sha(raw)), 'asset identity differs')
    return {'files': marker['files'], 'manifest': manifest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('plan')
    check = sub.add_parser('verify'); check.add_argument('--intake', type=Path, required=True)
    staging = sub.add_parser('stage')
    for name in ('intake', 'selection', 'output'): staging.add_argument('--' + name, type=Path, required=True)
    done = sub.add_parser('check-stage'); done.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'plan': result = plan()
        elif args.command == 'verify': result = verify(args.intake)
        elif args.command == 'stage': result = stage(args.intake, args.selection, args.output)
        else: result = check_stage(args.output)
        print(json.dumps(result, indent=2, sort_keys=True))
        return (2 if result.get('errors') else 1 if result.get('missing') else 0)
    except (ValueError, OSError, KeyError, TypeError, StopIteration):
        print(json.dumps({'valid': False, 'error': 'notice receipt or explicit selection refused'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
