"""Unsigned package-input preparation; no App/supplier/signing execution."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('production_input_prepare', ROOT / 'app/packaging/production_inputs/prepare.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class ProductionInputs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'source'
        for relative in ('app/src-tauri/resources', 'app/packaging/unsigned', 'app/packaging/notices', 'app/packaging/sqlite_notice', 'app/src-tauri/schemas'):
            shutil.copytree(ROOT / relative, self.source / relative)
        for relative in ('app/package-lock.json', 'app/src-tauri/Cargo.lock', 'app/src-tauri/Cargo.toml', 'app/src-tauri/tauri.conf.json'):
            shutil.copyfile(ROOT / relative, self.source / relative)
        self.vendor = self.root / 'vendor'; self.vendor.mkdir()
        for name in ('bin', 'codex-path', 'codex-resources'): (self.vendor / name).mkdir()
        (self.vendor / 'bin/codex').write_bytes(bytes.fromhex('cffaedfe') + b'INVENTED; DO NOT EXECUTE')
        (self.vendor / 'bin/codex').chmod(0o755)
        (self.vendor / 'codex-path/rg').write_bytes(b'INVENTED helper')
        (self.vendor / 'codex-resources/input.txt').write_bytes(b'INVENTED resource')
        self.metadata = {'layoutVersion':1,'version':'9.9.9','target':'aarch64-apple-darwin','variant':'codex',
                         'entrypoint':'bin/codex','resourcesDir':'codex-resources','pathDir':'codex-path'}
        (self.vendor / 'codex-package.json').write_text(json.dumps(self.metadata))
        self.bind_vendor_reference()
        self.output = self.root / 'output'
        self.kw = dict(source_root=self.source,vendor=self.vendor,expected_manifest=module.inventory.scan(self.vendor)['manifest_sha256'],
                       pin='9.9.9',revision='a'*40,output=self.output,test_identifier='dev.chirality.app-v4.package-test.invented')

    def bind_vendor_reference(self):
        tree=module.inventory.scan(self.vendor)
        root=self.source/'app/src-tauri/resources/distribution-reference'
        selection=json.loads((root/'build-selection.s2.json').read_text())
        path=root/selection['expected']['path']; expected=json.loads(path.read_text())
        entries=[{'path':'.','kind':'dir','mode':int(tree['root_mode'],8)}]
        for e in tree['entries']:
            v={'path':e['path'],'kind':e['kind'],'mode':int(e['mode'],8)}
            if e['kind']=='file':v.update(size=e['size'],sha256=e['sha256'])
            entries.append(v)
        expected['pin']='9.9.9';expected['generated']['pin']='9.9.9'
        expected['inventory'].update(entries=entries,manifest_sha256=tree['manifest_sha256'])
        path.write_text(json.dumps(expected));selection['expected']['sha256']=module.sha(path.read_bytes())
        path=root/selection['attestation']['path'];attestation=json.loads(path.read_text())
        attestation['expected_reference']=selection['expected']
        path.write_text(json.dumps(attestation));selection['attestation']['sha256']=module.sha(path.read_bytes())
        (root/'build-selection.s2.json').write_text(json.dumps(selection))

    def publisher_file(self, identifier='invalid.example.chirality-v4'):
        folder=self.root/'private-input';folder.mkdir(exist_ok=True)
        path=folder/'publisher.json'
        path.write_text(json.dumps({'format':'publisher-build-selection.s1','production_bundle_identifier':identifier,'developer_id_team_identifier':'EXAMPLE001'}))
        return path
    def run_plan(self, **changes):
        return module.prepare(**(self.kw | changes))
    def test_explicit_upstream_supplement_is_mapped_and_revalidated(self):
        helper_spec = importlib.util.spec_from_file_location('notice_receipt_fixture', ROOT / 'app/tests/notice_receipts_test.py')
        helper = importlib.util.module_from_spec(helper_spec); helper_spec.loader.exec_module(helper)
        fixture, r = helper.fixture, helper.r
        intake = self.root / 'notice-intake'
        fixture(self.source, intake)
        private = self.root / 'notice-private'; private.mkdir()
        selection = private / 'selection.json'
        selection.write_bytes(r.encode(dict(format='upstream-notice-selection/1',
            plan_sha256=r.files.sha(r.encode(r.plan(self.source))), components=['objc2'], basis='invented selection')))
        supplement = self.root / 'supplement'
        r.stage(intake, selection, supplement, self.source)
        self.run_plan(upstream_notices=supplement)
        config = json.loads((self.output / 'tauri.package-inputs.conf.json').read_bytes())
        resources = config['bundle']['resources']
        self.assertEqual(resources[str(supplement / 'LICENSE.md')], 'third-party-notices/upstream/LICENSE.md')
        self.assertEqual(resources[str(supplement / 'manifest.json')], 'third-party-notices/upstream/manifest.json')
        self.assertFalse(any('COMPLETE' in name or str(private) in name or str(intake) in name for name in resources))
        module.check_plan(self.output)
        (supplement / 'LICENSE.md').write_text('modified')
        with self.assertRaises(ValueError): self.run_plan(output=self.root / 'other', upstream_notices=supplement)

    def test_default_none_release_plan_has_all_resources_and_no_execution(self):
        result = self.run_plan()
        config=json.loads((self.output/'tauri.package-inputs.conf.json').read_text())
        recipe=json.loads((self.output/'build-recipe.json').read_text())
        self.assertEqual(config['version'],'4.0.0')
        self.assertEqual(config['bundle']['macOS'],{'minimumSystemVersion':'15.0','signingIdentity':None})
        dest=set(config['bundle']['resources'].values())
        self.assertIn('codex/',dest);self.assertIn('third-party-notices/index.json',dest)
        self.assertIn('third-party-notices/sqlite-preparation/sqlite3-source-header.txt',dest)
        self.assertIn('distribution-reference/build-selection.s2.json',dest)
        self.assertNotIn('--debug',recipe['argv']);self.assertIn('--no-sign',recipe['argv'])
        self.assertNotIn('CHIRALITY_PUBLISHER_SELECTION',recipe['environment'])
        self.assertIn('CHIRALITY_PUBLISHER_SELECTION',recipe['unset_environment'])
        self.assertEqual(len(config['bundle']['resources']),50)
        self.assertEqual(len(dest),50)
        self.assertFalse(recipe['inherit_environment'])
        self.assertIn('CARGO_TARGET_DIR',recipe['required_environment'])
        self.assertNotIn('RUSTFLAGS',recipe['environment_allowlist'])
        self.assertEqual(module.check_plan(self.output)['files'],result['files'])
        account=json.loads((self.output/'input-inventory.json').read_text())
        self.assertEqual(len(account['tool_sha256']),3)
        self.assertTrue(account['jsonschema_version'])
        self.assertFalse(result['build_executed']);self.assertFalse(result['signing_executed']);self.assertFalse(result['package_complete'])
    def test_explicit_invented_publisher_input_binds_identifier_and_recipe(self):
        data={'format':'publisher-build-selection.s1','production_bundle_identifier':'invalid.example.chirality-v4','developer_id_team_identifier':'EXAMPLE001'}
        path=self.publisher_file()
        result=self.run_plan(test_identifier=None,publisher_input=path,publisher_sha256=module.sha(path.read_bytes()))
        config=json.loads((self.output/'tauri.package-inputs.conf.json').read_text())
        recipe=json.loads((self.output/'build-recipe.json').read_text())
        self.assertEqual(config['identifier'],data['production_bundle_identifier'])
        self.assertEqual(recipe['environment']['CHIRALITY_PUBLISHER_SELECTION'],'production-v1')
        self.assertNotIn(data['production_bundle_identifier'],json.dumps(result))
        self.assertNotIn(data['developer_id_team_identifier'],json.dumps(result))
    def test_missing_or_ambiguous_identity_refuses(self):
        for changes in ({'test_identifier':None},{'test_identifier':'invalid.example.production'},
                        {'publisher_input':self.root/'missing'},{'publisher_sha256':'0'*64}):
            with self.subTest(changes=changes),self.assertRaises(ValueError): self.run_plan(**changes)
        self.assertFalse(self.output.exists())
    def test_publisher_wrong_digest_and_extra_fields_refuse(self):
        path=self.publisher_file()
        with self.assertRaises(ValueError):self.run_plan(test_identifier=None,publisher_input=path,publisher_sha256='0'*64)
        data={'format':'publisher-build-selection.s1','production_bundle_identifier':'invalid.example.app','developer_id_team_identifier':'EXAMPLE001','requirement':'caller logic'}
        path.write_text(json.dumps(data))
        with self.assertRaises(Exception):self.run_plan(test_identifier=None,publisher_input=path,publisher_sha256=module.sha(path.read_bytes()))
        self.assertFalse(self.output.exists())

    def test_missing_private_file_and_test_namespace_in_production_refuse(self):
        with self.assertRaises(FileNotFoundError):
            self.run_plan(test_identifier=None,publisher_input=self.root/'missing.json',publisher_sha256='0'*64)
        path=self.publisher_file('dev.chirality.app-v4.package-test.other')
        with self.assertRaisesRegex(ValueError,'test namespace'):
            self.run_plan(test_identifier=None,publisher_input=path,publisher_sha256=module.sha(path.read_bytes()))

    def test_vendor_reference_mismatch_refuses_even_with_matching_manifest(self):
        (self.vendor/'codex-resources/input.txt').write_bytes(b'changed vendor')
        manifest=module.inventory.scan(self.vendor)['manifest_sha256']
        with self.assertRaisesRegex(ValueError,'mapped supplier reference'):
            self.run_plan(expected_manifest=manifest)
        self.assertFalse(self.output.exists())

    def test_alias_overlap_and_input_embedding_refuse(self):
        case=Path(str(self.source).replace('/source','/SOURCE'))
        if case.exists() and module.identity(case)==module.identity(self.source):
            with self.assertRaisesRegex(ValueError,'overlap'):
                self.run_plan(output=case/'app/src-tauri/resources/instructions/plan')
        alias=Path('/System/Volumes/Data'+str(self.source))
        if alias.exists() and module.identity(alias)==module.identity(self.source):
            with self.assertRaisesRegex(ValueError,'overlap'):
                self.run_plan(output=alias/'app/plan')
        embedded=self.source/'embedded-vendor';shutil.copytree(self.vendor,embedded)
        with self.assertRaisesRegex(ValueError,'disjoint'):self.run_plan(vendor=embedded)
        path=self.source/'app/src-tauri/resources/instructions/private.json'
        path.write_bytes(self.publisher_file().read_bytes())
        with self.assertRaisesRegex(ValueError,'outside source and vendor'):
            self.run_plan(test_identifier=None,publisher_input=path,publisher_sha256=module.sha(path.read_bytes()))

    def test_incomplete_write_has_no_usable_completion_marker(self):
        real=module.write_new
        def fail(path, raw):
            if path.name=='input-inventory.json':raise OSError('invented write failure')
            real(path,raw)
        with patch.object(module,'write_new',side_effect=fail),self.assertRaises(OSError):self.run_plan()
        self.assertTrue((self.output/'INCOMPLETE.txt').is_file())
        self.assertFalse((self.output/'PLAN_COMPLETE.json').exists())
        with self.assertRaisesRegex(ValueError,'incomplete'):module.check_plan(self.output)

    def test_resource_link_and_recheck_mutation_refuse(self):
        link=self.source/'app/src-tauri/resources/instructions/extra-link';link.symlink_to('AGENTS.md')
        with self.assertRaisesRegex(ValueError,'link/special'):self.run_plan()
        link.unlink()
        real=module.inventory.scan;calls=0
        def mutate(path):
            nonlocal calls
            if Path(path)==self.vendor:
                calls+=1
                if calls==2:(self.vendor/'codex-resources/input.txt').write_bytes(b'changed during plan')
            return real(path)
        with patch.object(module.inventory,'scan',side_effect=mutate),self.assertRaisesRegex(ValueError,'vendor changed'):
            self.run_plan()
        self.assertFalse(self.output.exists())

    def test_empty_directories_glob_metadata_and_checkout_refuse(self):
        (self.vendor/'empty').mkdir()
        with self.assertRaisesRegex(ValueError,'empty resource'):self.run_plan()
        (self.vendor/'empty').rmdir()
        for value in (True,1.0):
            self.metadata['layoutVersion']=value
            (self.vendor/'codex-package.json').write_text(json.dumps(self.metadata))
            with self.assertRaisesRegex(ValueError,'must be an integer'):
                self.run_plan(expected_manifest=module.inventory.scan(self.vendor)['manifest_sha256'])
        (self.source/'.git').write_text('INVENTED checkout marker')
        with self.assertRaisesRegex(ValueError,'not a checkout'):self.run_plan()

    def test_glob_vendor_and_duplicate_destination_refuse(self):
        glob=self.root/'vendor*';shutil.copytree(self.vendor,glob)
        with self.assertRaisesRegex(ValueError,'glob'):self.run_plan(vendor=glob)
        path=self.source/'app/packaging/unsigned/tauri.attested-reference.conf.json'
        value=json.loads(path.read_text())
        value['bundle']['resources']['resources/distribution-reference/build-selection.s2.json']='third-party-notices/index.json'
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError,'duplicate resource destination'):self.run_plan()

    def test_case_alias_output_refuses(self):
        alias=Path(str(self.vendor).replace('/vendor','/VENDOR'))
        if not alias.exists() or module.identity(alias)!=module.identity(self.vendor):self.skipTest('case-sensitive filesystem')
        with self.assertRaisesRegex(ValueError,'overlap'):self.run_plan(output=alias/'codex-resources/plan')

    def test_firmlink_output_refuses(self):
        alias=Path('/System/Volumes/Data'+str(self.source))
        if not alias.exists() or module.identity(alias)!=module.identity(self.source):self.skipTest('no macOS Data firmlink alias')
        with self.assertRaisesRegex(ValueError,'overlap'):self.run_plan(output=alias/'app/plan')
    def test_vendor_manifest_links_and_metadata_refuse(self):
        with self.assertRaises(ValueError):self.run_plan(expected_manifest='0'*64)
        (self.vendor/'link').symlink_to('bin/codex')
        with self.assertRaises(ValueError):self.run_plan(expected_manifest=module.inventory.scan(self.vendor)['manifest_sha256'])
        (self.vendor/'link').unlink()
        with self.assertRaises(ValueError):self.run_plan(pin='0.0.0')
        self.assertFalse(self.output.exists())
    def test_no_overwrite_overlap_or_symlink_output(self):
        self.run_plan()
        before=(self.output/'build-recipe.json').read_bytes()
        with self.assertRaises(FileExistsError):self.run_plan()
        self.assertEqual(before,(self.output/'build-recipe.json').read_bytes())
        with self.assertRaises(ValueError):self.run_plan(output=self.vendor/'output')
        alias=self.root/'alias';alias.symlink_to(self.output,target_is_directory=True)
        with self.assertRaises(ValueError):self.run_plan(output=alias/'child')
    def test_missing_mapped_notice_refuses_before_output(self):
        (self.source/'app/packaging/notices/index.json').unlink()
        with self.assertRaises(FileNotFoundError):self.run_plan()
        self.assertFalse(self.output.exists())

if __name__=='__main__':unittest.main()
