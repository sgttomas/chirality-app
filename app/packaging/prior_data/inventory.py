#!/usr/bin/env python3
"""Record and compare data present under the App's identity before and after 4.0.0 runs.

DEL-01-06 REQ-008, AC-009, VER-008. 4.0.0 replaces v3.0.1 under one bundle identifier
(`com.chirality.app`): it takes v3.0.1's place in the Applications folder and starts with
whatever v3.0.1 and macOS left under that identity. This helper records, before installation,
the inventory and content identities of a set of roots the operator confirms, and compares a
second record made after the package has been installed, launched and run.

It reads only the roots it is given. It never follows a symbolic link, never reads a socket or
other special file, never reads a keychain, and never touches or launches an application. No
file content appears in any record: each entry keeps path, kind, mode, size and SHA-256 (a
link keeps its target text). The private record (mode 0600) keeps paths; the shareable summary
keeps only counts, classifications and digests, because file names can carry content.

Each root carries a class so that different findings stay apart; the helper separates them and
decides nothing about whether a change is acceptable:

  prior-data              data the prior version (v3.0.1) wrote itself
  current-data            4.0.0's own data folder
  system-per-identifier   files macOS keeps per bundle identifier
  application-bundle      the installed application; its replacement is expected

Commands:
  roots   print the default root set for the operator to confirm; reads none of it
  record  --root PATH ... --out NEW-PRIVATE-FILE --summary NEW-FILE
  compare BEFORE AFTER [--report NEW-PRIVATE-FILE]

compare prints the shareable per-root summary and exits 1 when any recorded entry is missing or
differs in any root (the application bundle included), 0 otherwise; 2 is a refusal.

Test it on invented trees only. Never run it on another person's home directory.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[3]
FORMAT = 'chirality-prior-data-inventory/v1'
SUMMARY_FORMAT = 'chirality-prior-data-inventory-summary/v1'
COMPARISON_FORMAT = 'chirality-prior-data-comparison/v1'
CLASSES = ('prior-data', 'current-data', 'system-per-identifier', 'application-bundle')
IDENTIFIER = 'com.chirality.app'   # docs/RELEASE_TARGET_4.0.0.md
BUNDLE_NAME = 'Chirality.app'

_spec = importlib.util.spec_from_file_location('prior_data_scan', ROOT / 'app/packaging/inventory.py')
scanner = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(scanner)


class Refused(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Refused(message)


def default_roots(home, identifier=IDENTIFIER, applications='/Applications'):
    """Path text only; nothing here is read or checked for existence."""
    library = Path(home) / 'Library'
    return [
        ('prior-data', library / 'Application Support/Chirality',
         "v3.0.1's own data folder (runtime/packages/cli/src/config.ts at tag v3.0.1)"),
        ('prior-data', library / 'Logs/Chirality', "v3.0.1's logs folder (Electron default for the product name)"),
        ('prior-data', library / 'LaunchAgents/com.chirality.runtime.plist',
         "v3.0.1's runtime LaunchAgent (runtime/packages/cli/src/launch-agent.ts at tag v3.0.1)"),
        ('current-data', library / 'Application Support' / identifier,
         "4.0.0's own data folder (Tauri App-data folder for the identifier)"),
        ('system-per-identifier', library / 'Preferences' / (identifier + '.plist'), 'preferences kept per bundle identifier'),
        ('system-per-identifier', library / 'Saved Application State' / (identifier + '.savedState'),
         'saved window state kept per bundle identifier'),
        ('system-per-identifier', library / 'Caches' / identifier, 'caches kept per bundle identifier'),
        ('system-per-identifier', library / 'HTTPStorages' / identifier, 'web storage kept per bundle identifier'),
        ('system-per-identifier', library / 'WebKit' / identifier, 'web view data kept per bundle identifier'),
        ('application-bundle', Path(applications) / BUNDLE_NAME,
         'the installed application; 4.0.0 takes v3.0.1\'s place here, so its replacement is expected'),
    ]


def _identity(path):
    value = os.stat(path, follow_symlinks=False)
    return value.st_dev, value.st_ino


def _clean(entry):
    """Only identities: no content, no derived content flags."""
    kept = {k: entry[k] for k in ('path', 'kind', 'mode') }
    if entry['kind'] == 'file':
        kept.update(size=entry['size'], sha256=entry['sha256'])
    elif entry['kind'] == 'symlink':
        kept['target'] = entry['target']
    return kept


SPECIAL = ((stat.S_ISSOCK, 'socket'), (stat.S_ISFIFO, 'fifo'), (stat.S_ISCHR, 'char-device'), (stat.S_ISBLK, 'block-device'))


def _special_kind(mode):
    return next((name for test, name in SPECIAL if test(mode)), 'other')


def _hash_file(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        start = os.fstat(fd)
        require(stat.S_ISREG(start.st_mode), 'root changed kind while being read')
        digest = hashlib.sha256()
        while chunk := os.read(fd, 1024 * 1024):
            digest.update(chunk)
        end = os.fstat(fd)
        require((start.st_size, start.st_mtime_ns, start.st_ctime_ns) == (end.st_size, end.st_mtime_ns, end.st_ctime_ns),
                'data changed while being read')
        return digest.hexdigest(), end.st_size
    finally:
        os.close(fd)


def _scan_root(path):
    """One root's identities. Raises on a link in its ancestry, an unreadable entry or a change."""
    require('\n' not in str(path) and '\r' not in str(path), 'line break in a root path refused')
    try:
        path = scanner.anchored(path)
    except ValueError as error:
        raise Refused('symbolic link in a root\'s ancestry refused') from error
    if not os.path.lexists(path):
        return {'state': 'absent'}
    info = os.lstat(path)
    mode = oct(stat.S_IMODE(info.st_mode))
    try:
        if stat.S_ISDIR(info.st_mode):
            tree = scanner.scan(path)
            entries = []
            for entry in tree['entries']:
                if entry['kind'] == 'other':
                    child = os.lstat(path / entry['path'])
                    require(not (stat.S_ISREG(child.st_mode) or stat.S_ISDIR(child.st_mode) or stat.S_ISLNK(child.st_mode)),
                            'data changed while being read')
                    entry = dict(entry, kind=_special_kind(child.st_mode))
                entries.append(_clean(entry))
            require(tree['root_mode'] == mode, 'data changed while being read')
            return {'state': 'present', 'kind': 'dir', 'mode': mode, 'entries': entries}
        if stat.S_ISREG(info.st_mode):
            digest, size = _hash_file(path)
            return {'state': 'present', 'kind': 'file', 'mode': mode, 'size': size, 'sha256': digest, 'entries': []}
        return {'state': 'present', 'kind': _special_kind(info.st_mode), 'mode': mode, 'entries': []}
    except PermissionError as error:
        raise Refused('unreadable entry refused (never omitted)') from error
    except ValueError as error:
        if isinstance(error, Refused):
            raise
        message = str(error)
        if 'line break' in message:
            raise Refused('a name containing a line break is refused') from error
        raise Refused('data changed while being read') from error


def _root_record(cls, path):
    require(cls in CLASSES, 'unknown root class')
    observed = _scan_root(path)
    return {'class': cls, 'path': str(Path(os.path.abspath(path))), **observed}


def _manifest(root):
    """Digest over the root's own identity and its entries; names never leave the private record."""
    body = {k: root.get(k) for k in ('state', 'kind', 'mode', 'size', 'sha256', 'entries')}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _counts(entries):
    counts = {}
    for entry in entries:
        counts[entry['kind']] = counts.get(entry['kind'], 0) + 1
    return dict(sorted(counts.items()))


def record(roots):
    """roots: list of (class, path). Every root is read twice; any difference refuses the record."""
    paths = [str(Path(os.path.abspath(p))) for _, p in roots]
    require(len(paths) == len(set(paths)), 'duplicate root')
    require(roots, 'at least one root required')
    first = [_root_record(c, p) for c, p in roots]
    second = [_root_record(c, p) for c, p in roots]
    require(first == second, 'data changed while being read')
    return {'format': FORMAT, 'roots': first}


def summary(value):
    return {'format': SUMMARY_FORMAT, 'record_format': value['format'], 'roots': [
        {'index': i, 'class': r['class'], 'state': r['state'], 'root_kind': r.get('kind'),
         'entry_counts': _counts(r.get('entries', [])), 'manifest_sha256': _manifest(r)}
        for i, r in enumerate(value['roots'])]}


def _inside(child, parent):
    return child == parent or child.startswith(parent.rstrip('/') + '/')


def _check_output(path, roots):
    path = Path(os.path.abspath(path))
    require(not os.path.lexists(path), 'output exists; a new file is required')
    require('\n' not in str(path), 'line break in output path refused')
    try:
        parent = scanner.anchored(path.parent)
    except ValueError as error:
        raise Refused('symbolic link in the output path refused') from error
    require(parent.is_dir(), 'output folder must exist')
    for _, root in roots:
        root = Path(os.path.abspath(root))
        require(not _inside(str(path), str(root)), 'output inside a recorded root refused')
        if os.path.lexists(root):
            require(_identity(root) not in {_identity(p) for p in (parent, *parent.parents)},
                    'output inside a recorded root refused')
    return path


def _write_new(path, value):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as output:
        output.write((json.dumps(value, indent=2, sort_keys=True) + '\n').encode())
        output.flush(); os.fsync(output.fileno())


def write_record(roots, out, summary_out):
    out, summary_out = _check_output(out, roots), _check_output(summary_out, roots)
    require(out != summary_out, 'record and summary must be different files')
    value = record(roots)
    shared = summary(value)
    _write_new(out, value)
    _write_new(summary_out, shared)
    return shared


def load(path):
    try:
        value = json.loads(Path(path).read_bytes())
    except (OSError, ValueError) as error:
        raise Refused('record unreadable') from error
    require(isinstance(value, dict) and value.get('format') == FORMAT and isinstance(value.get('roots'), list),
            'unknown record format')
    for root in value['roots']:
        require(root.get('class') in CLASSES and root.get('state') in ('absent', 'present'), 'invalid root in record')
    return value


def _key(entry):
    return {k: entry.get(k) for k in ('kind', 'mode', 'size', 'sha256', 'target')}


def compare_root(before, after):
    """One root's findings: entries unchanged, changed, removed and added; the root's own '.' included."""
    result = {'class': before['class'], 'path': before['path'], 'before': before['state'], 'after': after['state']}
    def table(root):
        if root['state'] == 'absent':
            return {}
        rows = {'.': {k: root.get(k) for k in ('kind', 'mode', 'size', 'sha256')}}
        rows.update({e['path']: _key(e) for e in root['entries']})
        return rows
    b, a = table(before), table(after)
    changed = sorted((p for p in b.keys() & a.keys() if b[p] != a[p]), key=str.encode)
    removed = sorted(b.keys() - a.keys(), key=str.encode)
    added = sorted(a.keys() - b.keys(), key=str.encode)
    recorded_dirs = {p for p, v in b.items() if v['kind'] == 'dir'}
    flagged = [p for p in added if (p.rsplit('/', 1)[0] if '/' in p else '.') in recorded_dirs]
    result['entries'] = {
        'changed': [{'path': p, 'differs_in': sorted(k for k in b[p] if b[p][k] != a[p].get(k))} for p in changed],
        'removed': removed, 'added': added, 'added_in_recorded_directory': flagged}
    result['counts'] = {'unchanged': len(b.keys() & a.keys()) - len(changed), 'changed': len(changed),
                        'removed': len(removed), 'added': len(added), 'added_in_recorded_directory': len(flagged)}
    if before['state'] == 'absent' and after['state'] == 'absent':
        finding = 'absent before and after'
    elif before['state'] == 'absent':
        finding = 'created (absent before)'
    elif after['state'] == 'absent':
        finding = 'removed'
    elif changed or removed:
        finding = 'changed'
    elif added:
        finding = 'unchanged entries; additions'
    else:
        finding = 'unchanged'
    if before['class'] == 'application-bundle' and finding in ('changed', 'removed'):
        finding += ' (replacement expected)'
    result['finding'] = finding
    return result


def compare(before, after):
    require([(r['class'], r['path']) for r in before['roots']] == [(r['class'], r['path']) for r in after['roots']],
            'the two records name different roots')
    roots = [compare_root(b, a) for b, a in zip(before['roots'], after['roots'])]
    altered = any(r['counts']['changed'] or r['counts']['removed'] for r in roots)
    return {'format': COMPARISON_FORMAT, 'status': 'changed' if altered else 'unchanged', 'roots': roots}


def shareable(comparison, before_raw, after_raw):
    """Per-root counts and classifications; no paths."""
    by_class = {}
    for root in comparison['roots']:
        totals = by_class.setdefault(root['class'], {'changed': 0, 'removed': 0, 'added': 0})
        for k in totals:
            totals[k] += root['counts'][k]
    return {'format': COMPARISON_FORMAT + '-summary', 'status': comparison['status'],
            'before_record_sha256': hashlib.sha256(before_raw).hexdigest(),
            'after_record_sha256': hashlib.sha256(after_raw).hexdigest(),
            'by_class': by_class,
            'roots': [{'index': i, 'class': r['class'], 'before': r['before'], 'after': r['after'],
                       'finding': r['finding'], 'counts': r['counts']} for i, r in enumerate(comparison['roots'])],
            'standing': 'separates findings by root class; decides nothing about whether a change is acceptable'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    roots = commands.add_parser('roots', help='print the default root set to confirm; reads none of it')
    roots.add_argument('--home', default=os.path.expanduser('~'), help='home folder the paths are composed from (not read)')
    roots.add_argument('--identifier', default=IDENTIFIER)
    rec = commands.add_parser('record')
    for flag, cls in (('--root', 'prior-data'), ('--current-root', 'current-data'),
                      ('--system-root', 'system-per-identifier'), ('--bundle-root', 'application-bundle')):
        rec.add_argument(flag, action='append', default=[], dest=cls, metavar='PATH', help=f'a {cls} root (repeatable)')
    rec.add_argument('--out', required=True, help='new private record (mode 0600; keeps paths)')
    rec.add_argument('--summary', required=True, help='new shareable summary (counts and digests only)')
    cmp = commands.add_parser('compare')
    cmp.add_argument('before'); cmp.add_argument('after')
    cmp.add_argument('--report', help='new private per-entry report (mode 0600; keeps paths)')
    args = parser.parse_args(argv)
    try:
        if args.command == 'roots':
            print(json.dumps({'identifier': args.identifier,
                              'note': '4.0.0 replaces v3.0.1 under one bundle identifier; confirm each root before recording. '
                                      'Nothing here was read.',
                              'roots': [{'class': c, 'path': str(p), 'why': w}
                                        for c, p, w in default_roots(args.home, args.identifier)]}, indent=2))
            return 0
        if args.command == 'record':
            selected = [(cls, p) for cls in CLASSES for p in getattr(args, cls)]
            print(json.dumps(write_record(selected, args.out, args.summary), indent=2))
            return 0
        raws = [Path(p).read_bytes() for p in (args.before, args.after)]
        result = compare(load(args.before), load(args.after))
        if args.report:
            report = _check_output(args.report, [(r['class'], r['path']) for r in result['roots']])
            _write_new(report, result)
        print(json.dumps(shareable(result, *raws), indent=2))
        return 1 if result['status'] == 'changed' else 0
    except (Refused, OSError) as error:
        print(json.dumps({'refused': type(error).__name__ if not isinstance(error, Refused) else str(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
