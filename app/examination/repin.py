#!/usr/bin/env python3
"""Re-derive, or check, the examination source pins from current bytes.

Examination readers verify the files they read against SHA-256 digests. The
digests of evolving sources live in the source profiles listed in PROFILES and
in the generated lock `app/examination/pins.lock.json`, which replaces the
digest constants the readers used to carry in their own code.

    python3 app/examination/repin.py           # after a reviewed, legitimate change
    python3 app/examination/repin.py --check   # CI: fail when sources and pins disagree

Re-derivation recomputes every live entry below, repeating until profiles that
pin other profiles agree, then refreshes the lock's `current` section. Review
the resulting diff: it names exactly which pinned bytes changed. The lock must
hold exactly the entries in CURRENT and FROZEN below. Its `frozen` section
mirrors historical receipt digests anchored as constants in reader code; both
modes fail if an entry or its bytes differ from the anchor. Entries outside the rules below are
historical identities (frozen documentary Markdown selections, projection
digests, historical provenance) and are left as recorded.

This tool changes only digests. Adding or removing a pinned source, or changing
what an examination selects, is a reviewed edit to the profile itself.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCK = 'app/examination/pins.lock.json'
LOCK_FORMAT = 'chirality-examination-pin-lock/1'
CONDITION = 'execution/PKG-09/DEL-09-01/Design/support-identity-v1/documentary-condition.v3.json'
DIGEST = re.compile(r'(sha256:)?[0-9a-f]{64}')
HEX64 = re.compile(r'[0-9a-f]{64}')


class Map:
    """A path -> digest object. Non-string values are projection selections.

    Markdown entries are skipped unless `markdown=True`: in those profiles a
    changed Markdown source falls back to its frozen original bytes, so its
    digest names historical publication bytes, not the current file.
    """
    def __init__(self, *pointer, markdown=False):
        self.pointer, self.markdown = pointer, markdown

    def slots(self, value):
        for path, digest in value.items():
            if isinstance(digest, str) and (self.markdown or not path.endswith('.md')):
                yield value, path, path


class Refs:
    """A list, or a role -> item object, of {path, sha256} file references.

    Items carrying `selectors` record a documentary projection digest, not a
    file digest, and are skipped.
    """
    def __init__(self, *pointer):
        self.pointer = pointer

    def slots(self, value):
        for item in (value.values() if isinstance(value, dict) else value):
            if 'selectors' not in item:
                yield item, 'sha256', item['path']


class Ref:
    """One object naming a file under `key` with its digest under `sha256`."""
    def __init__(self, *pointer, key='path'):
        self.pointer, self.key = pointer, key

    def slots(self, value):
        yield value, 'sha256', value[self.key]


class Digest:
    """One digest field whose file is fixed by the profile's meaning."""
    def __init__(self, *pointer, key, path):
        self.pointer, self.key, self.path = pointer, key, path

    def slots(self, value):
        yield value, self.key, self.path


# Live source profiles. Every rule names entries whose consumer compares them
# with the current file bytes (the reader named in each comment).
PROFILES = {
    # distribution_receiving/receive.py current_inputs()
    'app/examination/distribution_receiving/inputs.json': [Map()],
    # package_receiving/adapter.py Receiver (all sources read from the checkout)
    'app/examination/package_receiving/sources.package-v1.json': [Map('sources', markdown=True)],
    # packaging/prepare.py check_basis(); historical_documentary_provenance stays as recorded
    'app/packaging/sources.json': [Map('sources')],
    # packaging/static_distribution/check.py source_model()
    'app/packaging/static_distribution/sources.json': [Map('sources')],
    # support_identity/canonical.py CanonicalSupport
    'app/examination/support_identity/canonical-pins.terms-v1.json': [
        Map('sources'), Ref('documentary_selection', key='manifest')],
    # sq_receiving/receive.py Receiver
    'app/examination/sq_receiving/pins.terms-v1.json': [
        Map('sources'), Ref('documentary_selection', key='manifest')],
    # sq_receiving/receive_packages.py Receiver; predecessor/profile refs describe the selection
    'app/examination/sq_receiving/pins.packages-v1.json': [
        Map('sources'), Ref('documentary_selection', key='manifest'),
        Ref('predecessor'), Ref('package_source_profile')],
    # standalone/prepare.py verified_sources()
    'app/examination/standalone/sources.terms-v1.json': [
        Refs('sources'), Digest('documentary_selection', key='manifest_sha256', path=CONDITION)],
    # standalone/pre_run_inputs.py PreRunInputs
    'app/examination/standalone/pre_run_inputs.terms-v1.pins.json': [
        Map('sources'), Refs('fixture_roles'), Ref('documentary_selection', key='manifest')],
    # native_forms/native_form.py consumer()
    'app/examination/native_forms/sources.terms-v1.json': [Refs('sources')],
    # native_forms/pre_run_form.py consumer()
    'app/examination/native_forms/pre_run_form.terms-v1.pins.json': [
        Map('sources'), Ref('documentary_selection', key='manifest')],
    # admission/current_admission.py: complete current documents, no frozen fallback
    'app/examination/admission/sources.current-v1.json': [
        Map('sources', markdown=True), Map('reader_dependencies')],
}


E = 'app/examination/'
# The exact lock catalog. `current` lists every digest a reader takes from the
# lock instead of carrying it in code; repin derives them from current bytes.
CURRENT = (
    E + 'admission/admission_check.py',                     # current_admission DEPENDENCIES
    E + 'admission/admission_rules.py',                     # current_admission DEPENDENCIES
    E + 'admission/sources.current-v1.json',                # current_admission
    E + 'distribution_receiving/inputs.json',               # distribution receive
    E + 'distribution_receiving/receive.py',                # distribution terminal
    E + 'documentary_condition.py',                         # prepare, terms_condition
    E + 'native_forms/pre_run_form.terms-v1.pins.json',     # pre_run_form
    E + 'package_receiving/sources.package-v1.json',        # package adapter
    E + 'sq_receiving/pins.packages-v1.json',               # SQ receive_packages
    E + 'sq_receiving/pins.terms-v1.json',                  # SQ receive
    E + 'standalone/pre_run_inputs.terms-v1.pins.json',     # pre_run_inputs
    E + 'support_identity/canonical-pins.terms-v1.json',    # canonical
)
# `frozen` lists retained historical receipts. Their digests are anchored as
# immutable constants in the reader code named here, never in the lock alone;
# the lock's entries must equal those anchors and repin never rewrites them.
FROZEN = {
    E + 'distribution_receiving/pins.stop-admission-lt09-v1.json':
        (E + 'distribution_receiving/receive.py', 'PINS_SHA256'),
    E + 'distribution_receiving/pins.build-selection-lt09-v1.json':
        (E + 'distribution_receiving/receive.py', 'BUILD_SELECTION_PINS_SHA256'),
    E + 'distribution_receiving/pins.stop-admission-terminal-v1.json':
        (E + 'distribution_receiving/terminal.py', 'PINS_SHA256'),
    E + 'distribution_receiving/pins.build-selection-terminal-v1.json':
        (E + 'distribution_receiving/terminal.py', 'BUILD_SELECTION_PINS_SHA256'),
}
assert not set(CURRENT) & set(FROZEN), 'a lock entry cannot be both current and frozen'


class PinError(ValueError):
    pass


def anchor(root, reader, name):
    """An immutable historical digest constant from reader code."""
    for node in ast.parse((Path(root) / reader).read_bytes()).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            value = node.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str) and HEX64.fullmatch(value.value):
                return value.value
    raise PinError(f'missing historical anchor {name} in {reader}')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def resolve(root, relative):
    """A deliverable's `Design/` before 2026-10-30 means its `Work/`, as the readers resolve it."""
    match = re.match(r'(execution/PKG-\d+/DEL-\d+-\d+/)Design/', relative)
    if match is None or os.path.lexists(os.path.join(root, match.group(1) + 'Design')):
        return relative
    return match.group(1) + 'Work/' + relative[match.end():]


def at(value, pointer):
    for key in pointer:
        value = value[key]
    return value


def slots(profile, value):
    for rule in PROFILES[profile]:
        for container, key, path in rule.slots(at(value, rule.pointer)):
            if not isinstance(container[key], str) or not DIGEST.fullmatch(container[key]):
                raise PinError(f'{profile}: invalid digest for {path}')
            yield container, key, path


class Derivation:
    """Derive every live digest from current bytes, without writing."""

    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.overlay = {}
        self.missing = []

    def read(self, relative):
        relative = resolve(self.root, relative)
        if relative in self.overlay:
            return self.overlay[relative]
        target = self.root / relative
        if target.is_symlink():
            raise PinError('linked pinned source refused: ' + relative)
        return target.read_bytes()

    def digest(self, owner, path):
        if resolve(self.root, path) == LOCK:
            raise PinError(owner + ': the pin lock cannot itself be pinned')
        try:
            return sha(self.read(path))
        except FileNotFoundError:
            self.missing.append(f'{owner}: pinned source missing: {path}')
            return None

    def run(self):
        for _ in range(len(PROFILES) + 2):
            changed = False
            for profile in PROFILES:
                raw = self.read(profile)
                value = json.loads(raw)
                for container, key, path in slots(profile, value):
                    digest = self.digest(profile, path)
                    if digest is not None:
                        prefix = 'sha256:' if container[key].startswith('sha256:') else ''
                        container[key] = prefix + digest
                if encode(value) != raw:
                    self.overlay[profile] = encode(value)
                    changed = True
            if not changed:
                break
        else:
            raise PinError('profiles pin each other in a cycle; repin cannot converge')
        raw = self.read(LOCK)
        lock = json.loads(raw)
        if (not isinstance(lock, dict) or lock.get('format') != LOCK_FORMAT
                or set(lock) != {'format', 'regenerate', 'current', 'frozen'}):
            raise PinError('unknown pin lock format')
        self.validate_lock(lock)
        current = lock['current'] if isinstance(lock['current'], dict) else {}
        regenerated = dict(lock, current={path: self.digest(LOCK, path) or current.get(path)
                                          for path in sorted(CURRENT)},
                           frozen=dict(sorted(self.anchors.items())))
        if encode(regenerated) != raw:
            self.overlay[LOCK] = encode(regenerated)
        return self

    def validate_lock(self, lock):
        """Compare the lock with the catalog: exact entry sets, digest syntax and anchors."""
        self.anchors = {path: anchor(self.root, *source) for path, source in FROZEN.items()}
        self.lock_problems, self.frozen_problems = [], []
        current, frozen = lock['current'], lock['frozen']
        if not isinstance(current, dict):
            self.lock_problems.append('current section is not an object')
            current = {}
        if not isinstance(frozen, dict):
            self.frozen_problems.append('frozen section is not an object')
            frozen = {}
        for path in sorted(set(CURRENT) - set(current)):
            self.lock_problems.append('current entry missing: ' + path)
        for path in sorted(set(current) - set(CURRENT)):
            note = ' (historical receipt reclassified as current)' if path in FROZEN else ''
            self.lock_problems.append('unexpected current entry: ' + path + note)
        for path, digest in sorted(current.items()):
            if not isinstance(digest, str) or not HEX64.fullmatch(digest):
                self.lock_problems.append('malformed current digest: ' + path)
        for path in sorted(set(self.anchors) - set(frozen)):
            self.frozen_problems.append('frozen entry missing: ' + path)
        for path in sorted(set(frozen) - set(self.anchors)):
            note = ' (current entry reclassified as frozen)' if path in CURRENT else ''
            self.frozen_problems.append('unexpected frozen entry: ' + path + note)
        for path, expected in sorted(self.anchors.items()):
            reader, name = FROZEN[path]
            if path in frozen and frozen[path] != expected:
                self.frozen_problems.append(f'frozen entry differs from its anchor {name} in {reader}: {path}')
            if self.digest(LOCK, path) not in (None, expected):
                self.frozen_problems.append(
                    f'frozen evidence changed: {path} (restore the retained bytes; repin never re-pins them)')

    def changes(self):
        """Pinned sources whose recorded digest differs from current bytes."""
        result = []
        for path, data in sorted(self.overlay.items()):
            old = json.loads((self.root / path).read_bytes())
            new = json.loads(data)
            if path == LOCK:
                before = old['current'] if isinstance(old.get('current'), dict) else {}
                after = new['current']
                result += [(path, name) for name in after if before.get(name) != after[name]]
                continue
            pairs = zip(slots(path, old), slots(path, new))
            result += [(path, source) for (a, k, source), (b, _, _) in pairs if a[k] != b[k]]
        return result

    def write(self):
        for path, data in self.overlay.items():
            (self.root / path).write_bytes(data)


def main(argv=None, root=ROOT):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true', help='report disagreement and exit 1; write nothing')
    args = parser.parse_args(argv)
    try:
        derivation = Derivation(root).run()
    except (PinError, OSError, ValueError, KeyError, TypeError) as error:
        print('repin: ' + str(error), file=sys.stderr)
        return 2
    # Frozen problems are never repaired. Current-section problems fail the
    # check; re-derivation regenerates that section from the catalog.
    problems = derivation.missing + [LOCK + ': ' + p for p in derivation.frozen_problems]
    if args.check:
        problems += [LOCK + ': ' + p for p in derivation.lock_problems]
    changes = derivation.changes()
    for problem in problems:
        print('repin: ' + problem, file=sys.stderr)
    if args.check:
        if changes:
            print('Pinned examination sources differ from their recorded digests:', file=sys.stderr)
            for profile, source in changes:
                print(f'  {profile}: {source}', file=sys.stderr)
            print('Review the change, then run `python3 app/examination/repin.py` and commit the result.',
                  file=sys.stderr)
        if problems or changes:
            return 1
        print('Examination pins agree with current sources.')
        return 0
    if problems:
        print('repin: nothing written', file=sys.stderr)
        return 1
    derivation.write()
    for profile, source in changes:
        print(f're-pinned {profile}: {source}')
    if not changes:
        print('Examination pins already agree with current sources.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
