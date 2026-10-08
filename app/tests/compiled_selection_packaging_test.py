"""Actual opt-in mapping and exact-byte closure checks; no build or launch."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import tomllib
import unittest

APP = Path(__file__).resolve().parents[1]
RUST = APP / 'src-tauri'
CONFIG = APP / 'packaging/unsigned'
NAMESPACE = 'distribution-development-reference'
EXPECTED = {
    'resources/distribution-development-reference/build-selection.s2.json': NAMESPACE + '/build-selection.s2.json',
    'resources/distribution-successor/synthetic-expected.json': NAMESPACE + '/expected.json',
    'resources/distribution-successor/synthetic-attestation.json': NAMESPACE + '/attestation.json',
    'resources/distribution-successor/synthetic-evidence.json': NAMESPACE + '/synthetic-evidence.json',
}


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError('duplicate config field')
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def resolve(root, reference):
    path = Path(reference['path'])
    if path.is_absolute() or '..' in path.parts: raise ValueError('escaping reference')
    raw = (root / path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != reference['sha256']: raise ValueError('reference byte mismatch')
    return json.loads(raw)


def closure(root):
    selection = load(root / 'build-selection.s2.json')
    if selection['format'] != 'build-selection.s2' or selection['method'] != 'codex-vendor-tree-v1':
        raise ValueError('wrong selection version')
    if selection['schema_ids'] != ['expected-reference.s1', 'adoption-attestation.s1']:
        raise ValueError('wrong selected schema cohort')
    expected = resolve(root, selection['expected'])
    attestation = resolve(root, selection['attestation'])
    if attestation['expected_reference'] != selection['expected']: raise ValueError('attestation subject differs')
    evidence = [expected['label_evidence'], expected['generation_correspondence'],
                expected['generated']['provenance'], expected['generated']['version_advance'],
                attestation['review_evidence'], attestation['adoption']['through_help_human'], attestation['adoption']['evidence']]
    evidence += [expected['archive'][key] for key in ('acquisition_authorization', 'custody', 'extraction_procedure')]
    for reference in evidence: resolve(root, reference)
    return selection


class Packaging(unittest.TestCase):
    def test_opt_in_config_preserves_base_and_adds_exact_four_files(self):
        ordinary = load(CONFIG / 'tauri.development.conf.json')
        selected = load(CONFIG / 'tauri.synthetic-selection.conf.json')
        expected = json.loads(json.dumps(ordinary))
        expected['bundle']['resources'].update(EXPECTED)
        self.assertEqual(selected, expected)
        self.assertEqual(len(set(EXPECTED.values())), 4)
        self.assertTrue(all(Path(p).parts[0] != 'distribution-reference' for p in EXPECTED.values()))

    def test_actual_resource_mapping_stages_exact_complete_closure(self):
        selected = load(CONFIG / 'tauri.synthetic-selection.conf.json')
        mappings = {s:d for s,d in selected['bundle']['resources'].items() if Path(d).parts[0] == NAMESPACE}
        self.assertEqual(mappings, EXPECTED)
        with tempfile.TemporaryDirectory() as tmp:
            resources = Path(tmp)
            for source, destination in mappings.items():
                target = resources / destination; target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(RUST / source, target)
                self.assertEqual(target.read_bytes(), (RUST / source).read_bytes())
            root = resources / NAMESPACE
            self.assertEqual({p.name for p in root.iterdir()}, {'build-selection.s2.json','expected.json','attestation.json','synthetic-evidence.json'})
            selection = closure(root)
            self.assertEqual(selection['expected']['path'], 'expected.json')
            self.assertEqual(selection['attestation']['path'], 'attestation.json')
            (root / 'synthetic-evidence.json').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'byte mismatch'): closure(root)

    def test_ordinary_configs_do_not_map_any_synthetic_selection_resource(self):
        for path in (CONFIG / 'tauri.development.conf.json', RUST / 'tauri.conf.json'):
            resources = load(path).get('bundle', {}).get('resources', {})
            self.assertIsInstance(resources, dict)
            self.assertFalse(set(resources).intersection(EXPECTED))
            self.assertFalse(any(Path(p).parts[0] == NAMESPACE for p in resources.values()))

    def test_custom_protocol_and_default_features_do_not_enable_synthetic_anchor(self):
        features = tomllib.loads((RUST / 'Cargo.toml').read_text())['features']
        self.assertIn('synthetic-distribution-anchor', features)
        def expanded(names):
            seen = set()
            while names:
                name = names.pop()
                if name not in seen:
                    seen.add(name); names.extend(features.get(name, []))
            return seen
        self.assertNotIn('synthetic-distribution-anchor', expanded(list(features.get('default', [])) + ['custom-protocol']))
        self.assertNotIn('distribution-successor', expanded(['synthetic-distribution-anchor']))


if __name__ == '__main__': unittest.main()
