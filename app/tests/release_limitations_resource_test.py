"""The release's limitations list ships byte for byte as release/LIMITATIONS.md (DEL-01-06 AC-008).

Advances exit criterion 12 at the source: the mapping is exact in the base configuration and
in the prepared package plan, and the plan's recorded digest is the document's own. Whether
the signed package carries it is observed on the package, not here."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = '../../docs/RELEASE_LIMITATIONS_4.0.0.md'
DESTINATION = 'release/LIMITATIONS.md'
DOCUMENT = ROOT / 'docs/RELEASE_LIMITATIONS_4.0.0.md'

spec = importlib.util.spec_from_file_location('limitations_production_inputs', ROOT / 'app/tests/production_inputs_test.py')
helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)


class BaseConfiguration(unittest.TestCase):
    def test_document_maps_exactly_to_the_bundle_resource(self):
        resources = json.loads((ROOT / 'app/src-tauri/tauri.conf.json').read_bytes())['bundle']['resources']
        self.assertEqual(resources.get(SOURCE), DESTINATION)
        self.assertEqual([s for s, d in resources.items() if d.rstrip('/') == DESTINATION or DESTINATION.startswith(d)], [SOURCE])
        self.assertEqual((ROOT / 'app/src-tauri' / SOURCE).resolve(), DOCUMENT.resolve())
        self.assertTrue(DOCUMENT.is_file() and not DOCUMENT.is_symlink())


class PreparedPlan(unittest.TestCase):
    """A fixture plan from a copied source export, as production_inputs_test prepares one."""
    bind_vendor_reference = helper.ProductionInputs.bind_vendor_reference

    def setUp(self):
        helper.ProductionInputs.setUp(self)

    def recorded(self):
        helper.module.prepare(**self.kw)
        config = json.loads((self.output / 'tauri.package-inputs.conf.json').read_bytes())
        account = json.loads((self.output / 'input-inventory.json').read_bytes())
        return config['bundle']['resources'], account['resource_inputs']

    def test_plan_maps_the_document_once_with_its_own_digest(self):
        resources, inputs = self.recorded()
        self.assertEqual(resources[SOURCE], DESTINATION)
        self.assertEqual([s for s, d in resources.items() if d == DESTINATION], [SOURCE])
        self.assertEqual(inputs[SOURCE]['destination'], DESTINATION)
        self.assertEqual(inputs[SOURCE]['sha256'], hashlib.sha256(DOCUMENT.read_bytes()).hexdigest())
        self.assertEqual(inputs[SOURCE]['size'], DOCUMENT.stat().st_size)

    def test_plan_records_the_bytes_of_the_selected_source(self):
        changed = b'# Invented limitations\n\n- invented entry\n'
        (self.source / 'docs/RELEASE_LIMITATIONS_4.0.0.md').write_bytes(changed)
        _, inputs = self.recorded()
        self.assertEqual(inputs[SOURCE]['sha256'], hashlib.sha256(changed).hexdigest())

    def test_plan_refuses_a_missing_document(self):
        (self.source / 'docs/RELEASE_LIMITATIONS_4.0.0.md').unlink()
        with self.assertRaises(Exception):
            helper.module.prepare(**self.kw)
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
