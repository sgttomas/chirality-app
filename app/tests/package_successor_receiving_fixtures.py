"""Maintain invented package -> EXP -> SQ inputs; never a package/native witness."""
import builtins
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parent


def load(name, path, imports=None):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    if imports:
        def selected(name, globals=None, locals=None, fromlist=(), level=0):
            if level == 0 and name in imports:
                return imports[name]
            return builtins.__import__(name, globals, locals, fromlist, level)
        module.__dict__['__builtins__'] = dict(vars(builtins), __import__=selected)
    paths = list(sys.path)
    try:
        exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    finally:
        sys.path[:] = paths
    return module


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


adapter = load('package_receiving_fixture_adapter', APP / 'examination/package_receiving/adapter.py')
canonical = load('package_receiving_fixture_canonical', APP / 'examination/support_identity/canonical.py')
sq_rules = load('package_receiving_sq_rules', ROOT / 'execution/PKG-09/DEL-09-02/Work/prototype/check_sq.py')
producer = load('package_receiving_fixture_producer', APP / 'packaging/successor/check.py')
producer_fixtures = load('package_receiving_producer_fixtures', APP / 'packaging/successor/fixtures.py', {'check': producer})


class JoinedFixture:
    def __init__(self, root):
        self.root = Path(root)
        self.packet = self.root / 'packet'
        self.package = producer_fixtures.Fixture(self.packet)
        self.canonical = canonical.CanonicalSupport()
        self.receiver = adapter.Receiver(canonical=self.canonical)
        self.config = self.root / 'receiving-config.json'
        self.set_trust(self.package.trusted_publisher_sha256)
        source = APP / 'tests/group_b_sq_receiving_fixtures/development'
        for path in source.iterdir():
            if path.is_file():
                target = self.packet / ('sq-' + path.name)
                if target.exists():
                    raise ValueError('fixture filename collision: ' + path.name)
                shutil.copyfile(path, target)
        self.selection = json.loads((self.packet / 'sq-selection.json').read_bytes())
        self.dossier = json.loads((self.packet / 'sq-dossier.json').read_bytes())
        names = {path.name for path in source.iterdir() if path.is_file()}
        def relocate(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key == 'path' and isinstance(child, str) and child in names:
                        value[key] = 'sq-' + child
                    else:
                        relocate(child)
            elif isinstance(value, list):
                for child in value:
                    relocate(child)
        relocate(self.selection)
        self.selection['format'] = 'sq-exp-receiving-selection.package-s4.v1'
        self.selection['package_source_profile_sha256'] = adapter.PINS_SHA256
        self.selection['configuration_sha256'] = self.config_sha
        candidate = {k: self.package.request['candidate'][k] for k in ('revision', 'build_identity', 'codex_pin')}
        self.selection['candidate'] = copy.deepcopy(candidate)
        self.dossier['candidate'] = dict(candidate, package_record=self.package.request['record_id'])
        self.records = {}
        for artifact in self.selection['artifacts']:
            value = json.loads((self.packet / artifact['record']['path']).read_bytes())
            if artifact['kind'] == 'result':
                value['subject']['app_candidate'].update(revision=candidate['revision'], build_identity=candidate['build_identity'])
                value['configuration']['codex_pin'] = candidate['codex_pin']
            self.records[artifact['slot']] = value
        self.linked_slot = 'result-J-1'
        linked = self.records[self.linked_slot]
        linked['subject']['app_candidate'].update(packaged=True, package_record=self.package.request['record_id'])
        linked['configuration']['route']['kind'] = 'native_packaged'
        # Invented positive declaration only; no actual observation or package.
        linked['outcome'] = 'pass'
        linked['evidence'] = [{'ref': 'INVENTED-PACKAGED-OBSERVATION', 'provenance': 'test_definition', 'route': 'native_packaged'}]
        self.dossier['scenarios'][0]['steps'][0]['outcome'] = 'pass'
        self.selection['artifacts'].append({'slot': 'package-witness', 'kind': 'package_witness',
            'record': {'path': 'binding.json', 'sha256': '0' * 64},
            'binding': {'path': 'package-witness.binding.json', 'sha256': '0' * 64}})
        self.selection['packages'] = [{'ref': self.package.request['record_id'], 'slot': 'package-witness',
                                       'result_slots': [self.linked_slot]}]
        self.save()

    def replace_package_artifact(self, filename, raw):
        """Re-derive fixture reference hashes upward to exercise semantic joins."""
        pending = [(filename, self.package.put_raw(filename, raw))]
        while pending:
            changed_name, reference = pending.pop()
            for name, value in list(self.package.values.items()):
                if name == filename:
                    continue
                changed = False
                def visit(item):
                    nonlocal changed
                    if isinstance(item, dict):
                        if set(item) == {'path', 'sha256'} and item['path'] == changed_name:
                            if item != reference:
                                item.update(reference); changed = True
                        else:
                            for child in item.values(): visit(child)
                    elif isinstance(item, list):
                        for child in item: visit(child)
                visit(value)
                if changed:
                    pending.append((name, self.package.put(name, value)))
        self.package.request = copy.deepcopy(self.package.values['binding.json'])

    def set_trust(self, trust):
        raw = encoded({'format': 'exp-package-receiving-config/1', 'trusted_publisher_sha256': trust})
        self.config.write_bytes(raw)
        self.config_sha = adapter.sha(raw)

    def save(self, rebind_package=True):
        self.package.save()
        for artifact in self.selection['artifacts']:
            slot, kind = artifact['slot'], artifact['kind']
            if kind == 'package_witness':
                raw = (self.packet / 'binding.json').read_bytes()
                artifact['record']['sha256'] = adapter.sha(raw)
                if rebind_package:
                    report = self.receiver.receive(self.packet / 'binding.json', self.packet, self.config, self.config_sha)
                    binding = encoded(self.receiver.binding(raw, report, self.config_sha))
                    (self.packet / artifact['binding']['path']).write_bytes(binding)
                    artifact['binding']['sha256'] = adapter.sha(binding)
                continue
            value = self.records[slot]
            raw = encoded(value)
            (self.packet / artifact['record']['path']).write_bytes(raw)
            artifact['record']['sha256'] = adapter.sha(raw)
            binding = encoded(self.canonical.binding(kind, raw, self.selection['purpose']))
            (self.packet / artifact['binding']['path']).write_bytes(binding)
            artifact['binding']['sha256'] = adapter.sha(binding)
            if kind == 'result' and slot in self.selection['review']['results']:
                self.selection['review']['results'][slot] = {k: copy.deepcopy(value[k]) for k in ('subject', 'configuration', 'criterion')}
        for scenario in self.dossier['scenarios']:
            counted = [step for step in scenario['steps'] if step.get('counts', True)]
            if all(step['state'] == 'recorded' for step in counted):
                scenario['outcome'] = sq_rules.aggregate([step['outcome'] for step in counted])
        raw = encoded(self.dossier)
        (self.packet / self.selection['dossier']['path']).write_bytes(raw)
        self.selection['dossier']['sha256'] = adapter.sha(raw)
        self.selection['configuration_sha256'] = self.config_sha
        self.write_selection()

    def write_selection(self):
        raw = encoded(self.selection)
        self.path = self.packet / 'sq-selection.json'
        self.path.write_bytes(raw)
        self.sha = adapter.sha(raw)
