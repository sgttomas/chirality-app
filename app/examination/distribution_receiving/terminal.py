#!/usr/bin/env python3
"""Fixed synthetic terminal-pair file correspondence; no native capability restore."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PINS_SHA256 = '98f71bbc466a0f6b8fc7fde8243d0066d743b204e0fd551d46f5c40df009ed65'
FORMAT = 'group-b-s1-terminal-reader-exchange.v1'
ADOPTION = 'B-S4-LT12-SOURCE-TERMINAL-v1'
LIMITS = [
    'Exported LT09/LT23 pair file correspondence only; no native semantic reader reexecution.',
    'Pre-spawn observation is unchanged, not renewed terminal integrity, custody or descendant proof.',
    'Serialized reports cannot authenticate producer history, application build, namespace or native-held references.',
    'Synthetic test executable and invented application candidate remain separate identities.',
    'No S3, native examination, qualification, canonical rollout or release established.',
    'No-follow reads are bounded observations, not an atomic hostile-filesystem snapshot.',
]


def load(name, path, raw=None):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(path.read_bytes() if raw is None else raw, str(path), 'exec'), module.__dict__)
    return module


# Verify the captured helper bytes before executing their definitions.
HELPER_SHA256 = 'd3902ff62136bf0f5e1b8bb10d9948ec5d2e07493428804425cca1b5c214c787'
helper_raw = (HERE / 'receive.py').read_bytes()
if hashlib.sha256(helper_raw).hexdigest() != HELPER_SHA256:
    raise ValueError('frozen predecessor engine changed')
base = load('_terminal_frozen_file_helpers', HERE / 'receive.py', helper_raw)


class PredecessorReceiver(base.Receiver):
    """Explicit new source selection for the unchanged predecessor algorithm.

    No historical pin file/initializer is changed or represented as passing.
    """
    def __init__(self, pins):
        self.pins = pins
        self.schemas = {}
        for name in ('observed-verification.s1', 'lifecycle-event.s1', 'distribution-closure-transport.s3'):
            schema = base.parse(base.relative(PROJECT, 'app/src-tauri/resources/distribution-successor/' + name + '.schema.json'))
            self.schemas[name] = base.Draft202012Validator(schema, registry=base.Registry())
        path = PROJECT / 'app/examination/support_identity/canonical.py'
        self.canonical = load('_terminal_canonical', path, base.read_file(path)).CanonicalSupport()


class TerminalReceiver:
    def __init__(self):
        raw = base.read_file(HERE / 'pins.lt12-source-terminal-v1.json')
        base.require(base.sha(raw) == PINS_SHA256, 'terminal pins changed')
        self.pins = base.parse(raw)
        for path, digest in self.pins['sources'].items():
            base.require(base.sha(base.relative(PROJECT, path)) == digest, 'terminal selected source changed: ' + path)
        self.predecessor = PredecessorReceiver(self.pins)
        self.canonical = self.predecessor.canonical

    def check(self, path, expected_sha, selection, selection_sha):
        path = Path(path)
        base.require(path.name == 'exchange.json', 'completed exchange.json marker required; diagnostic refused')
        # A queued/partial/diagnostic marker is not a completed exchange even if
        # copied alongside a renamed payload. Producer locators are data only.
        base.require(not (path.parent.parent / 'DIAGNOSTIC_SOURCE.json').exists()
                     and not (path.parent / 'exchange.diagnostic.json').exists()
                     and not (path.parent / 'DIAGNOSTIC_SOURCE.json').exists(), 'diagnostic marker refused')
        base.digest(expected_sha); raw = base.read_file(path)
        base.require(base.sha(raw) == expected_sha, 'terminal exchange digest mismatch')
        exchange = base.parse(raw)
        base.exact(exchange, ('format', 'case', 'producer', 'applicationCandidate', 'predecessor', 'terminal', 'selectedSourceMembers'), 'terminal exchange')
        base.require(exchange['format'] == FORMAT, 'unsupported terminal exchange')
        for role, event in [('predecessor', 'actualLt09'), ('terminal', 'actualLt23')]:
            base.exact(exchange[role], ('readback', event, 'members'), role)
        expected_names = {'exchange.json', 'predecessor', 'terminal'}
        if exchange['selectedSourceMembers'] is not None: expected_names.add('selected-source')
        base.require({p.name for p in path.parent.iterdir()} == expected_names, 'completed case inventory differs')
        for role in ('predecessor', 'terminal'):
            base.require({p.name for p in (path.parent / role).iterdir()} == {'publication'}, 'publication parent inventory differs')
        predecessor = exchange['predecessor']; terminal = exchange['terminal']
        before = base.members(path.parent / 'predecessor/publication', predecessor['members'])
        after = base.members(path.parent / 'terminal/publication', terminal['members'])
        source = None
        if exchange['selectedSourceMembers'] is not None:
            source = base.members(path.parent / 'selected-source', exchange['selectedSourceMembers'])
        else:
            base.require(not (path.parent / 'selected-source').exists(), 'unselected source directory refused')
        # Outer representation projection only: actual LT09/event/raw bytes are
        # unchanged. The historical algorithm, not its stale source selection,
        # performs all prior closure/candidate/canonical checks under new pins.
        with tempfile.TemporaryDirectory(prefix='s4-terminal-predecessor-', dir=Path(tempfile.gettempdir()).resolve()) as tmp:
            root = Path(tmp)
            for name, files in [('publication', before), ('selected-source', source)]:
                if files is not None:
                    for member, payload in files.items():
                        target = root / name / member; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(payload)
            projected = {k: exchange[k] for k in ('case', 'producer', 'applicationCandidate', 'selectedSourceMembers')}
            projected.update(format='group-b-s1-reader-exchange.v1', **predecessor)
            payload = json.dumps(projected).encode(); (root / 'exchange.json').write_bytes(payload)
            prior_report = self.predecessor.check(root / 'exchange.json', base.sha(payload), selection, selection_sha)
        readback = terminal['readback']; base.exact(readback, ('state', 'generation', 'evidence'), 'terminal readback')
        base.require(readback['state'] == 'read', 'terminal read unavailable or pending')
        e = readback['evidence']; old = predecessor['readback']['evidence']
        base.exact(e, ('reference', 'artifact', 'lifecycle', 'transport', 'outcome', 'standing', 'readStanding', 'unsupportedEnvelopes'), 'terminal evidence')
        ref = e['reference']; oldref = old['reference']
        base.exact(ref, ('format', 'publication', 'generation', 'observed', 'lifecycle', 'transport', 'reader'), 'terminal reference')
        base.require(ref['format'] == oldref['format'] and ref['reader'] == self.pins['reader'], 'terminal reader identity differs')
        base.contained(ref['publication'])
        base.require(ref['publication'] != oldref['publication'], 'terminal publication must be distinct')
        for key in ('outcome', 'standing', 'readStanding', 'unsupportedEnvelopes'):
            base.require(e[key] == old[key], 'terminal standing/boundary differs')
        values = {}
        for key, projected_name, schema in [('observed', 'artifact', 'observed-verification.s1'),
                                           ('lifecycle', 'lifecycle', 'lifecycle-event.s1'),
                                           ('transport', 'transport', 'distribution-closure-transport.s3')]:
            value = base.parse(base.referenced(after, ref[key])); values[key] = value
            base.require(value == e[projected_name], 'terminal raw/projection differs')
            base.require(not list(self.predecessor.schemas[schema].iter_errors(value)), 'terminal shape differs: ' + schema)
        observation = values['observed']; life = values['lifecycle']; transport = values['transport']; event = terminal['actualLt23']
        base.require(ref['observed'] == oldref['observed'] and base.referenced(after, ref['observed']) == base.referenced(before, oldref['observed']), 'pre-spawn observation bytes/reference differ')
        base.require(observation['phase'] == 'pre-spawn', 'observation phase differs')
        generation = oldref['generation']
        base.require(all(g == generation for g in (ref['generation'], readback['generation'], observation['generation'], transport['generation'], life['verification_generation'], event.get('generation'))), 'mixed terminal generation')
        base.require(life['verification_artifact'] == ref['observed'] and life['legacy_event'] == event, 'terminal event/reference differs')
        base.require(event.get('transitionId') == 'LT-23' and event.get('event') == 'tree-ended'
                     and event.get('fromState') == 'stopping' and event.get('toState') == 'stopped', 'unsupported terminal event')
        base.require(type(event.get('sequence')) is int and event['sequence'] > predecessor['actualLt09']['sequence'], 'terminal sequence not increasing')
        base.require(event.get('supplierStanding') == 'unverified-development'
                     and event.get('verificationResult', {}).get('result') != 'verified', 'terminal verified claim refused')
        prior_transport = old['transport']
        for key in ('format', 'method', 'sourceAssociation', 'reader', 'limit'):
            base.require(transport[key] == prior_transport[key], 'terminal source/reader association differs')
        base.require(transport['mirrorLocator'] != prior_transport['mirrorLocator']
                     and transport['mirrorLocator'].endswith('/' + ref['publication']), 'terminal publication locator differs')
        entries = {}
        for entry in transport['entries']:
            base.referenced(after, entry); base.require(entry['path'] not in entries, 'duplicate terminal member')
            entries[entry['path']] = entry['sha256']
        base.require(entries == {p: base.sha(b) for p, b in after.items() if p != ref['transport']['path']}, 'terminal transport closure differs')
        excluded_before = {oldref[k]['path'] for k in ('lifecycle', 'transport')}
        excluded_after = {ref[k]['path'] for k in ('lifecycle', 'transport')}
        base.require({p:b for p,b in before.items() if p not in excluded_before} ==
                     {p:b for p,b in after.items() if p not in excluded_after}, 'terminal shared closure bytes differ')
        return {'terminal_pair_file_correspondence_passed': True, 'receiving_adoption': ADOPTION,
                'exchange_sha256': expected_sha, 'selection_sha256': selection_sha,
                'exported_event_pair': ['LT-09', 'LT-23'], 'case': exchange['case'],
                'producer': exchange['producer'], 'application_candidate': exchange['applicationCandidate'],
                'generation': generation, 'predecessor_canonical_join': prior_report,
                'native_reference_authority': False, 'namespace_authority_authenticated': False,
                'terminal_integrity_established': False, 'terminal_authority_authenticated': False,
                'semantic_reader_reexecuted': False, 'producer_history_authenticated': False,
                'application_build_authenticated': False, 'qualification_established': False, 'limits': LIMITS}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exchange'); parser.add_argument('--exchange-sha256', required=True)
    parser.add_argument('--selection', required=True); parser.add_argument('--selection-sha256', required=True)
    args = parser.parse_args(argv)
    try:
        report = TerminalReceiver().check(args.exchange, args.exchange_sha256, args.selection, args.selection_sha256)
        print(json.dumps(report, indent=2)); return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({'terminal_pair_file_correspondence_passed': False, 'input_error': str(error),
                          'terminal_integrity_established': False, 'terminal_authority_authenticated': False,
                          'qualification_established': False, 'limits': LIMITS}, indent=2)); return 2


if __name__ == '__main__':
    sys.exit(main())
