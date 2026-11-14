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

record writes the content, then a completion marker binding its digest; compare validates both
records strictly and refuses an incomplete, edited or impossible record. compare prints the
shareable per-root summary. Its status is `unchanged` only when nothing at all
differs: any changed, removed or added entry in any root (the application bundle included), and
any root that appeared or disappeared, gives `differences found` and exit 1; 2 is a refusal. The
per-root and per-class breakdown says where; which differences are acceptable is not decided here.

Limits: an operator-run check on stable inputs. It is built so that an observation that was not
made, that failed, or that is incomplete cannot come out as success, and so that drift and
mistakes are caught. It is not built to withstand a writer changing the inputs during the run, nor
someone with write access forging a record: the completion marker detects truncation or an edit
that did not recompute it, and is not authentication.

Test it on invented trees only. Never run it on another person's home directory.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[3]
FORMAT = 'chirality-prior-data-inventory/v2'
SUMMARY_FORMAT = 'chirality-prior-data-inventory-summary/v1'
COMPARISON_FORMAT = 'chirality-prior-data-comparison/v1'
DIFFERENT = 'differences found'
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


def _lstat(path):
    """The entry's own metadata, or None only when it does not exist. Any other error refuses:
    an unreadable ancestor never makes a root read as absent."""
    try:
        return os.lstat(path)
    except FileNotFoundError:
        return None
    except OSError as error:
        raise Refused(f'unreadable ancestor or entry refused ({type(error).__name__})') from error


def _no_link_ancestry(path, what):
    path = Path(os.path.abspath(path))
    for parent in reversed((path, *path.parents)):
        info = _lstat(parent)
        if info is None:
            break
        require(not stat.S_ISLNK(info.st_mode), f'symbolic link in {what} refused')
    return path


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
    path = _no_link_ancestry(path, "a root's ancestry")
    info = _lstat(path)
    if info is None:
        return {'state': 'absent'}
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
    require(_lstat(path) is None, 'output exists; a new file is required')
    require('\n' not in str(path), 'line break in output path refused')
    parent = _no_link_ancestry(path.parent, 'the output path')
    require(parent.is_dir(), 'output folder must exist')
    for _, root in roots:
        root = Path(os.path.abspath(root))
        require(not _inside(str(path), str(root)), 'output inside a recorded root refused')
        if _lstat(root) is not None:
            require(_identity(root) not in {_identity(p) for p in (parent, *parent.parents)},
                    'output inside a recorded root refused')
    return path


def _write_new(path, value, sort_keys=True):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as output:
        output.write((json.dumps(value, indent=2, sort_keys=sort_keys) + '\n').encode())
        output.flush(); os.fsync(output.fileno())


COMPLETION_METHOD = 'sha256 over canonical JSON (sorted keys, no spaces) of {"format", "roots"}'


def _content_digest(body):
    return hashlib.sha256(json.dumps({'format': body['format'], 'roots': body['roots']},
                                     sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def completed(body):
    """The record as written: its content, then a completion marker binding that content's digest,
    serialised last. A record without a matching marker was not completed and is refused."""
    return {'format': body['format'], 'roots': body['roots'],
            'completion': {'method': COMPLETION_METHOD, 'content_sha256': _content_digest(body)}}


def write_record(roots, out, summary_out):
    out, summary_out = _check_output(out, roots), _check_output(summary_out, roots)
    require(out != summary_out, 'record and summary must be different files')
    value = record(roots)
    shared = summary(value)
    _write_new(out, completed(value), sort_keys=False)
    _write_new(summary_out, shared)
    return shared


HEX64 = re.compile(r'[0-9a-f]{64}')
MODE = re.compile(r'0o[0-7]{1,4}')
EMPTY_SHA256 = hashlib.sha256(b'').hexdigest()
CONTROL = re.compile(r'[\x00-\x1f\x7f]')
ROOT_KINDS = ('dir', 'file', 'socket', 'fifo', 'char-device', 'block-device', 'other')
ENTRY_KINDS = ROOT_KINDS + ('symlink',)


def _valid_identity(item, where):
    """kind, mode and, for files, size and digest; for links, the target text; nothing else."""
    kind = item.get('kind')
    require(kind in ENTRY_KINDS, f'{where}: unknown kind')
    # Permission bits only, in the form oct() writes them.
    require(isinstance(item.get('mode'), str) and MODE.fullmatch(item['mode']) and oct(int(item['mode'], 8)) == item['mode'],
            f'{where}: mode missing or malformed')
    if kind == 'file':
        require(type(item.get('size')) is int and item['size'] >= 0, f'{where}: file size missing')
        require(isinstance(item.get('sha256'), str) and HEX64.fullmatch(item['sha256']), f'{where}: file digest missing')
        # A zero-byte file has exactly the digest of the empty input, and only it has.
        require((item['size'] == 0) == (item['sha256'] == EMPTY_SHA256), f'{where}: size and digest cannot both hold')
    if kind == 'symlink':
        require(isinstance(item.get('target'), str) and item['target'] and '\0' not in item['target'],
                f'{where}: link target missing or impossible')
    return kind


def _valid_relative(path):
    return (isinstance(path, str) and path and not path.startswith('/') and not CONTROL.search(path)
            and all(p not in ('', '.', '..') for p in path.split('/')))


def validate(value):
    """Refuse a record that fails validation, was not completed, or that a successful observation
    could not have produced."""
    require(isinstance(value, dict) and set(value) == {'format', 'roots', 'completion'}, 'record incomplete or not a record')
    require(value['format'] == FORMAT, 'unknown record format')
    marker = value['completion']
    require(isinstance(marker, dict) and set(marker) == {'method', 'content_sha256'} and marker['method'] == COMPLETION_METHOD,
            'record was not completed')
    require(isinstance(value['roots'], list) and value['roots'], 'record has no roots')
    paths = set()
    for i, root in enumerate(value['roots']):
        where = f'root {i}'
        require(isinstance(root, dict) and root.get('class') in CLASSES, f'{where}: unknown class')
        require(isinstance(root.get('path'), str) and root['path'].startswith('/') and not CONTROL.search(root['path'])
                and os.path.normpath(root['path']) == root['path'] and not root['path'].startswith('//'),
                f'{where}: path missing, not absolute, not normal or holding a control character')
        require(root['path'] not in paths, f'{where}: duplicate root'); paths.add(root['path'])
        if root.get('state') == 'absent':
            require(set(root) == {'class', 'path', 'state'}, f'{where}: an absent root holds nothing else')
            continue
        require(root.get('state') == 'present', f'{where}: unknown state')
        kind = _valid_identity(root, where)
        require(kind in ROOT_KINDS, f'{where}: a root cannot be a link')
        expected = {'class', 'path', 'state', 'kind', 'mode', 'entries'} | ({'size', 'sha256'} if kind == 'file' else set())
        require(set(root) == expected, f'{where}: fields do not match a {kind} root')
        entries = root['entries']
        require(isinstance(entries, list), f'{where}: entries missing')
        require(kind == 'dir' or not entries, f'{where}: only a directory root holds entries')
        seen, directories = [], set()
        for j, entry in enumerate(entries):
            here = f'{where} entry {j}'
            require(isinstance(entry, dict) and _valid_relative(entry.get('path')), f'{here}: path missing or malformed')
            ekind = _valid_identity(entry, here)
            fields = {'path', 'kind', 'mode'} | ({'size', 'sha256'} if ekind == 'file' else {'target'} if ekind == 'symlink' else set())
            require(set(entry) == fields, f'{here}: fields do not match a {ekind} entry')
            parent = entry['path'].rpartition('/')[0]
            require(not parent or parent in directories, f'{here}: parent directory not recorded')
            if ekind == 'dir':
                directories.add(entry['path'])
            seen.append(entry['path'])
        require(seen == sorted(seen, key=str.encode) and len(seen) == len(set(seen)),
                f'{where}: entries out of order or duplicated')
    require(isinstance(marker['content_sha256'], str) and marker['content_sha256'] == _content_digest(value),
            'record content does not match its completion marker')
    return value


def load(path):
    try:
        value = json.loads(Path(path).read_bytes())
    except (OSError, ValueError) as error:
        raise Refused('record unreadable') from error
    return validate(value)


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
    # Unchanged only when nothing at all differs: no changed, removed or added entry in any root,
    # and no root that appeared or disappeared. Which differences are acceptable is not decided here.
    differs = any(r['counts']['changed'] or r['counts']['removed'] or r['counts']['added'] or r['before'] != r['after']
                  for r in roots)
    return {'format': COMPARISON_FORMAT, 'status': DIFFERENT if differs else 'unchanged', 'roots': roots}


def shareable(comparison, before_raw, after_raw):
    """Per-root counts and classifications; no paths."""
    by_class = {}
    for root in comparison['roots']:
        totals = by_class.setdefault(root['class'], {'changed': 0, 'removed': 0, 'added': 0,
                                                     'added_in_recorded_directory': 0, 'roots_appeared': 0, 'roots_disappeared': 0})
        for k in ('changed', 'removed', 'added', 'added_in_recorded_directory'):
            totals[k] += root['counts'][k]
        totals['roots_appeared'] += root['before'] == 'absent' and root['after'] == 'present'
        totals['roots_disappeared'] += root['before'] == 'present' and root['after'] == 'absent'
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
        return 1 if result['status'] == DIFFERENT else 0
    except (Refused, OSError) as error:
        print(json.dumps({'refused': type(error).__name__ if not isinstance(error, Refused) else str(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
