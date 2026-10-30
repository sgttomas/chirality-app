"""Offline value checks for the Codex 0.160.0 macOS arm64 supplier reference.

Reads committed bytes only; never reads, extracts or executes a supplier tree.
Passing establishes record consistency and the pinned attestation join, not the authenticity of review or adoption.
"""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
S1 = HERE.parents[1]
DESIGN = S1.parent  # bundle root: every artifact path below is relative to it
sys.path.insert(0, str(S1))
import model  # noqa: E402

EXPECTED = {'path': 'distribution-s1/references/codex-0.160.0-macos-arm64/expected.json',
            'sha256': '754eebae912023aebe40cab157c0882081bec2d1d9db518627986526371a2a37'}
SELECTED_ATTESTATION_SHA256 = '09e1fae9d243462132803d868174b70ddae111bde2106aa2351ebfe74c793fe9'
ATTESTATION = {'path': 'distribution-s1/references/codex-0.160.0-macos-arm64/attestation.json',
               'sha256': SELECTED_ATTESTATION_SHA256}
APP_MANIFEST =model.ROOT / 'projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/MANIFEST.sha256'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Reference(unittest.TestCase):
    def setUp(self):
        self.e = model.resolve(EXPECTED, DESIGN, 'expected-reference.s1')

    def test_schema_inventory_and_evidence_bytes(self):
        e = self.e
        self.assertEqual(model.inventory.validate(e['inventory']), [])
        self.assertEqual((e['pin'], e['platform'], e['generated']['pin']), ('0.160.0', 'macOS arm64', '0.160.0'))
        refs = [e['label_evidence'], e['generation_correspondence'], e['generated']['provenance'],
                e['generated']['version_advance']]
        refs += [e['archive'][k] for k in ('acquisition_authorization', 'custody', 'extraction_procedure')]
        for ref in refs:
            model.resolve(ref, DESIGN)

    def test_label_tree_and_generation_joins(self):
        e = self.e
        files = {x['path']: x for x in e['inventory']['entries'] if x['kind'] == 'file'}
        probe = json.loads(model.resolve(e['label_evidence'], DESIGN))
        parsed = re.fullmatch(r'codex-cli ([0-9]+\.[0-9]+\.[0-9]+)\n?', probe['run']['stdout'])
        self.assertEqual(parsed.group(1), e['pin'])
        self.assertEqual(probe['run']['exit_code'], 0)
        self.assertEqual(probe['tree']['manifest_sha256'], e['inventory']['manifest_sha256'])
        self.assertEqual(probe['tree']['executable_sha256'], files['bin/codex']['sha256'])
        generation = json.loads(model.resolve(e['generated']['provenance'], DESIGN))
        self.assertEqual(generation['supplierSha256'], files['bin/codex']['sha256'])
        self.assertEqual(generation['version'], 'codex-cli ' + e['pin'])
        manifest = (DESIGN / 'generated/0.160.0/MANIFEST.sha256').read_bytes()
        self.assertEqual(sha(manifest), e['generated']['manifest_sha256'])
        self.assertEqual(sha(APP_MANIFEST.read_bytes()), e['generated']['manifest_sha256'])
        identity = json.loads((DESIGN / 'generated/0.160.0/SUPPLIER_IDENTITY.json').read_text())
        self.assertEqual(identity['generatedOutputIdentity']['manifestSha256'], e['generated']['manifest_sha256'])
        self.assertEqual(identity['generatedOutputIdentity']['pin'], e['pin'])
        rows = manifest.decode().splitlines()[1:]
        for variant, stats in generation['stats'].items():
            prefix = variant + '/'
            body = ''.join(r.replace('  ' + prefix, '  ', 1) + '\n' for r in rows if r.split('  ', 1)[1].startswith(prefix))
            self.assertEqual(sha(body.encode()), stats['manifestSha256'], variant)

    def test_changed_bytes_refuse(self):
        changed = dict(EXPECTED, sha256='0' * 64)
        with self.assertRaises(ValueError):
            model.resolve(changed, DESIGN, 'expected-reference.s1')
        inventory = json.loads(json.dumps(self.e['inventory']))
        inventory['entries'][0]['mode'] = 448
        self.assertFalse(model.inventory.compare(self.e['inventory'], inventory)['equal'])

    def test_selected_attestation(self):
        # The pinned digest stands in for the trusted build selection; the file's
        # own current digest never selects itself.
        self.assertEqual(model.reference(EXPECTED, ATTESTATION, DESIGN, SELECTED_ATTESTATION_SHA256)['pin'], '0.160.0')
        with self.assertRaises(ValueError):
            model.reference(EXPECTED, ATTESTATION, DESIGN, '0' * 64)
        changed = dict(ATTESTATION, sha256='0' * 64)
        with self.assertRaises(ValueError):
            model.reference(EXPECTED, changed, DESIGN, changed['sha256'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
