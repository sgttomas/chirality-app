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
        for relative in ('app/src-tauri/resources', 'app/packaging/unsigned', 'app/packaging/notices', 'app/packaging/sqlite_notice', 'app/packaging/font_notice', 'app/src/fonts', 'app/src-tauri/schemas'):
            shutil.copytree(ROOT / relative, self.source / relative)
        for relative in ('app/package-lock.json', 'app/src-tauri/Cargo.lock', 'app/src-tauri/Cargo.toml', 'app/src-tauri/tauri.conf.json', 'app/src/workspace.css', 'app/index.html'):
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
        self.assertIn('third-party-notices/fonts/index.json',dest);self.assertIn('third-party-notices/fonts/LICENSE-IBM-Plex-OFL.txt',dest)
        self.assertIn('distribution-reference/build-selection.s2.json',dest)
        self.assertNotIn('--debug',recipe['argv']);self.assertIn('--no-sign',recipe['argv'])
        self.assertNotIn('CHIRALITY_PUBLISHER_SELECTION',recipe['environment'])
        self.assertIn('CHIRALITY_PUBLISHER_SELECTION',recipe['unset_environment'])
        self.assertEqual(len(config['bundle']['resources']),52)
        self.assertEqual(len(dest),52)
        self.assertFalse(recipe['inherit_environment'])
        self.assertIn('CARGO_TARGET_DIR',recipe['required_environment'])
        self.assertNotIn('RUSTFLAGS',recipe['environment_allowlist'])
        self.assertNotIn('cargo_build_input', recipe)
        self.assertEqual(module.check_plan(self.output)['files'],result['files'])
        account=json.loads((self.output/'input-inventory.json').read_text())
        self.assertEqual(len(account['tool_sha256']),4)
        self.assertTrue(account['jsonschema_version'])
        self.assertFalse(result['build_executed']);self.assertFalse(result['signing_executed']);self.assertFalse(result['package_complete'])
    def test_explicit_cargo_input_preserves_config_bytes_and_host_target_scope(self):
        import tomllib
        self.run_plan(cargo_build_input=module.CARGO_BUILD_PRESET)
        recipe=json.loads((self.output/'build-recipe.json').read_text())
        contract=recipe['cargo_build_input']
        self.assertEqual(contract['sha256'], '82651ddc167d78065e4af475e439cd0c2fa0855b601f8fdda9a81ab263de42fc')
        self.assertEqual(module.sha(contract['text'].encode()),contract['sha256'])
        config=tomllib.loads(contract['text'])
        self.assertEqual(config,{'net':{'offline':True},'build':{'jobs':2},
            'profile':{'release':{'strip':'none','build-override':{'strip':'none'}}}})
        self.assertEqual(contract['release_opt_level'],3)
        self.assertEqual(contract['scope']['host'],'aarch64-apple-darwin')
        self.assertEqual(contract['scope']['target'],'aarch64-apple-darwin')
        self.assertEqual(set(contract['tool_sha256']),{'rustc','cargo','clang','ld'})
        self.assertNotIn('RUSTFLAGS', recipe['environment_allowlist'])
        self.assertEqual(set(module.check_plan(self.output)['files']),
                         {'tauri.package-inputs.conf.json','input-inventory.json','build-recipe.json'})

    def test_cargo_input_refuses_unknown_preset_and_changed_contract(self):
        with self.assertRaisesRegex(ValueError,'unsupported Cargo build input'):
            self.run_plan(cargo_build_input='all-platforms')
        self.assertFalse(self.output.exists())
        self.run_plan(cargo_build_input=module.CARGO_BUILD_PRESET)
        path=self.output/'build-recipe.json'; recipe=json.loads(path.read_text())
        recipe['cargo_build_input']['text']+='[profile.dev]\nstrip="none"\n'
        path.write_text(json.dumps(recipe))
        marker=self.output/'PLAN_COMPLETE.json';value=json.loads(marker.read_text())
        value['files']['build-recipe.json']=module.sha(path.read_bytes());marker.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError,'invalid Cargo build input contract'):module.check_plan(self.output)

    def test_cargo_input_refuses_changed_release_optimization(self):
        manifest=self.source/'app/src-tauri/Cargo.toml'
        manifest.write_text(manifest.read_text()+'\n[profile.release]\nopt-level = 1\n')
        with self.assertRaisesRegex(ValueError,'requires release opt-level 3'):
            self.run_plan(cargo_build_input=module.CARGO_BUILD_PRESET)
        self.assertFalse(self.output.exists())

    def test_cargo_input_preflight_refuses_scope_tool_and_config_mismatch(self):
        self.run_plan(cargo_build_input=module.CARGO_BUILD_PRESET)
        contract=module.cargo_build_input_contract(module.CARGO_BUILD_PRESET)
        home=self.root/'cargo-home';home.mkdir();config=home/'config.toml';config.write_bytes(contract['text'].encode())
        # Invented files exercise digest checks; never invoke a compiler in this test.
        tools={name:self.root/name for name in contract['tool_sha256']}
        for name,path in tools.items():path.write_bytes(('INVENTED '+name).encode())
        with self.assertRaisesRegex(ValueError,'platform scope mismatch'):
            module.verify_cargo_build_input(self.output,home,contract['scope']|{'sdk':'other'},tools)
        with self.assertRaisesRegex(ValueError,'exact resolved Cargo tool paths'):
            module.verify_cargo_build_input(self.output,home,contract['scope'],{})
        with self.assertRaisesRegex(ValueError,'toolchain mismatch'):
            module.verify_cargo_build_input(self.output,home,contract['scope'],tools)
        transfer=module.files.transfer
        def fixture_transfer(path, **kwargs):
            if Path(path) in tools.values():
                name=Path(path).name
                return (None,contract['tool_sha256'][name],{})
            return transfer(path,**kwargs)
        with patch.object(module.files,'transfer',side_effect=fixture_transfer):
            self.assertEqual(module.verify_cargo_build_input(self.output,home,contract['scope'],tools),contract['sha256'])
            config.write_text(contract['text'].replace('[profile.release]\nstrip = "none"','[profile.release]\nstrip = "debuginfo"'))
            with self.assertRaisesRegex(ValueError,'Cargo build config mismatch'):
                module.verify_cargo_build_input(self.output,home,contract['scope'],tools)
    def test_explicit_invented_publisher_input_binds_identifier_and_recipe(self):
        data={'format':'publisher-build-selection.s1','production_bundle_identifier':'invalid.example.chirality-v4','developer_id_team_identifier':'EXAMPLE001'}
        path=self.publisher_file()
        result=self.run_plan(test_identifier=None,publisher_input=path,publisher_sha256=module.sha(path.read_bytes()))
        config=json.loads((self.output/'tauri.package-inputs.conf.json').read_text())
        recipe=json.loads((self.output/'build-recipe.json').read_text())
        self.assertEqual(config['identifier'],data['production_bundle_identifier'])
        self.assertEqual(recipe['environment']['CHIRALITY_PUBLISHER_SELECTION'],'production-v1')
        # Every writable location the install and build use is named, so a driver can point each inside its run folder.
        for key in ('RUSTUP_HOME','NPM_CONFIG_PREFIX','NPM_CONFIG_LOGS_DIR','HOME','TMPDIR','CARGO_HOME','NPM_CONFIG_CACHE'):
            self.assertIn(key,recipe['environment_allowlist']); self.assertIn(key,recipe['required_environment'])
        self.assertEqual(recipe['environment']['NPM_CONFIG_UPDATE_NOTIFIER'],'false')
        self.assertNotIn(data['production_bundle_identifier'],json.dumps(result))
        self.assertNotIn(data['developer_id_team_identifier'],json.dumps(result))
    @staticmethod
    def tlv(tag, body):
        n=len(body)
        length=bytes([n]) if n<0x80 else bytes([0x80|((n.bit_length()+7)//8)])+n.to_bytes((n.bit_length()+7)//8,'big')
        return bytes([tag])+length+body
    def envelope(self, content, trailing=b''):
        t=self.tlv
        encap=t(0x30,t(0x06,module.DATA_OID)+t(0xa0,t(0x04,content)))
        signed=t(0x30,t(0x02,b'\x01')+t(0x31,b'')+encap+t(0x31,b'INVENTED signer info; never Apple-signed'))
        return t(0x30,t(0x06,module.SIGNED_DATA_OID)+t(0xa0,signed))+trailing
    def profile_value(self, **changes):
        import datetime
        value={'UUID':'INVENTED-PROFILE','Platform':['OSX'],'ProvisionsAllDevices':True,'TeamIdentifier':['EXAMPLE001'],
               'ApplicationIdentifierPrefix':['PREFIX0001'],'CreationDate':datetime.datetime(2020,1,1),'ExpirationDate':datetime.datetime(2099,1,1),
               'Entitlements':{'com.apple.application-identifier':'PREFIX0001.invalid.example.chirality-v4','com.apple.developer.team-identifier':'EXAMPLE001'}}
        value.update(changes); return value
    def profile_file(self, raw=None, **changes):
        import plistlib
        folder=self.root/'private-profile';folder.mkdir(exist_ok=True)
        path=folder/'invented.provisionprofile'
        path.write_bytes(raw if raw is not None else self.envelope(plistlib.dumps(self.profile_value(**changes))))
        return path
    def test_ambiguous_or_non_cms_profile_envelopes_refuse(self):
        import plistlib
        good=plistlib.dumps(self.profile_value()); bad=plistlib.dumps(self.profile_value(TeamIdentifier=['OTHER00001']))
        dup=good.replace(b'<key>TeamIdentifier</key>',b'<key>TeamIdentifier</key><array><string>OTHER00001</string></array><key>TeamIdentifier</key>',1)
        cases={'appended plist':self.envelope(good+bad.split(b'?>',1)[1]),'plist after envelope':self.envelope(good,trailing=bad),
               'non DER':b'0NOT-DER'+good,'duplicate key':self.envelope(dup),'binary plist':self.envelope(plistlib.dumps(self.profile_value(),fmt=plistlib.FMT_BINARY)),
               'wrong content type':self.envelope(good).replace(module.DATA_OID,module.SIGNED_DATA_OID,1)}
        for name,raw in cases.items():
            with self.subTest(name=name):
                path=self.profile_file(raw)
                with self.assertRaises(ValueError):self.run_plan(**self.production(path))
        self.assertFalse(self.output.exists())
    def test_profile_outside_validity_refuses(self):
        import datetime
        for changes in ({'ExpirationDate':datetime.datetime(2021,1,1)},{'CreationDate':datetime.datetime(2098,1,1)}):
            with self.subTest(changes=changes),self.assertRaisesRegex(ValueError,'not valid at preparation time'):
                self.run_plan(**self.production(self.profile_file(**changes)))
    def production(self, profile=None, profile_sha=None):
        path=self.publisher_file()
        kw=dict(test_identifier=None,publisher_input=path,publisher_sha256=module.sha(path.read_bytes()))
        if profile is not None: kw.update(provisioning_profile=profile,provisioning_profile_sha256=profile_sha or module.sha(profile.read_bytes()))
        return kw
    def test_selected_profile_is_embedded_at_contents_with_consistency_record(self):
        profile=self.profile_file()
        result=self.run_plan(**self.production(profile))
        config=json.loads((self.output/'tauri.package-inputs.conf.json').read_text())
        self.assertEqual(config['bundle']['macOS']['files'],{'embedded.provisionprofile':str(profile)})
        self.assertIsNone(config['bundle']['macOS']['signingIdentity'])
        account=json.loads((self.output/'input-inventory.json').read_text())['provisioning_profile']
        self.assertEqual(account['sha256'],module.sha(profile.read_bytes()))
        self.assertEqual(account['application_identifier'],'PREFIX0001.invalid.example.chirality-v4')
        self.assertIn('separate intake', account['standing']);self.assertIn('validity_checked_at',account);self.assertIn('unverified until build', account['standing']);self.assertNotIn('EXAMPLE001',json.dumps(result))
        self.assertNotIn(str(profile),json.dumps(config['bundle']['resources']))
    def test_profile_refuses_test_mode_wrong_digest_and_inconsistent_grants(self):
        profile=self.profile_file()
        with self.assertRaisesRegex(ValueError,'test mode'):self.run_plan(provisioning_profile=profile,provisioning_profile_sha256=module.sha(profile.read_bytes()))
        with self.assertRaisesRegex(ValueError,'selected digest'):self.run_plan(**self.production(profile,'0'*64))
        for changes,message in (({'TeamIdentifier':['OTHER00001']},'team'),
                                ({'Entitlements':{'com.apple.application-identifier':'PREFIX0001.other.app','com.apple.developer.team-identifier':'EXAMPLE001'}},'application identifier'),
                                ({'Platform':['iOS']},'macOS'),({'ProvisionedDevices':['device']},'macOS'),
                                ({'Entitlements':{'com.apple.application-identifier':'PREFIX0001.invalid.example.chirality-v4','com.apple.developer.team-identifier':'EXAMPLE001','get-task-allow':True}},'development')):
            with self.subTest(message=message):
                profile=self.profile_file(**changes)
                with self.assertRaisesRegex(ValueError,message):self.run_plan(**self.production(profile))
        self.assertFalse(self.output.exists())
    def test_profile_inside_source_or_vendor_refuses(self):
        for folder in (self.source,self.vendor):
            path=folder/'p.provisionprofile';path.write_bytes(self.profile_file().read_bytes())
            with self.subTest(folder=folder),self.assertRaisesRegex(ValueError,'outside source and vendor'):self.run_plan(**self.production(path))
            path.unlink()
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

    def test_0167_layout_cannot_borrow_the_older_distribution_reference(self):
        self.metadata.update(version='0.167.0', execServer='bin/codex-exec-server')
        (self.vendor/'codex-package.json').write_text(json.dumps(self.metadata))
        helper = self.vendor/'bin/codex-exec-server'
        helper.write_bytes(bytes.fromhex('cffaedfe') + b'INVENTED; never execute')
        helper.chmod(0o755)
        with self.assertRaisesRegex(ValueError, 'selected vendor does not match mapped supplier reference'):
            self.run_plan(pin='0.167.0', expected_manifest=module.inventory.scan(self.vendor)['manifest_sha256'])
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
    def test_stale_or_unindexed_font_notice_refuses_before_output(self):
        fonts=self.source/'app/src/fonts'
        (fonts/'invented-extra.woff2').write_bytes(b'INVENTED font bytes')
        with self.assertRaises(ValueError):self.run_plan()
        self.assertFalse(self.output.exists())
        (fonts/'invented-extra.woff2').unlink()
        license=fonts/'LICENSE-IBM-Plex-OFL.txt';license.write_bytes(license.read_bytes()+b'modified')
        with self.assertRaises(ValueError):self.run_plan()
        self.assertFalse(self.output.exists())

if __name__=='__main__':unittest.main()
