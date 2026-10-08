"""Offline packaging preparation tests; all inputs invented, supplier never executed."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

APP=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('packaging_inventory',APP/'packaging/inventory.py')
inventory=importlib.util.module_from_spec(spec); spec.loader.exec_module(inventory)
# prepare.py's local module import stays independent from B1 examination code.
sys.path.insert(0,str(APP/'packaging'))
import prepare


class PackagingPreparation(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()
        self.vendor=self.root/'vendor'; self.vendor.mkdir()
        for name in ('bin','codex-path','codex-resources'): (self.vendor/name).mkdir()
        (self.vendor/'bin/codex').write_bytes(bytes.fromhex('cffaedfe')+b'INVENTED, NOT EXECUTABLE CODE')
        (self.vendor/'bin/codex').chmod(0o755)
        (self.vendor/'codex-path/rg').write_text('INVENTED helper')
        (self.vendor/'codex-path/rg').chmod(0o755)
        self.metadata={'layoutVersion':1,'version':'0.160.0','target':'aarch64-apple-darwin','variant':'codex','entrypoint':'bin/codex','resourcesDir':'codex-resources','pathDir':'codex-path'}
        (self.vendor/'codex-package.json').write_text(json.dumps(self.metadata))
        self.inputs=self.root/'inputs.json'; self.inputs.write_text('{}')
        self.output=self.root/'stage'

    def run_prepare(self,**kwargs):
        params=dict(vendor=self.vendor,expected_manifest=inventory.scan(self.vendor)['manifest_sha256'],pin='0.160.0',revision='INVENTED',inputs=self.inputs,output=self.output)
        params.update(kwargs)
        return prepare.prepare(**params)

    def test_real_copy_is_equal_missing_inputs_stay_incomplete(self):
        result=self.run_prepare()
        self.assertTrue(result['staging_copy_comparison']['equal'])
        self.assertFalse(result['package_complete'])
        self.assertIn('role_set',result['input_account']['missing'])
        self.assertIsNone(result['configuration']['CF-5']['bundle_id'])
        self.assertEqual(set(result['first_package_checks'].values()),{'not-run'})
        self.assertEqual((self.output/'bundle/Contents/Resources/codex/bin/codex').read_bytes(),(self.vendor/'bin/codex').read_bytes())
        self.assertTrue((self.output/'preparation.json').is_file())
        self.assertFalse((self.output/'bundle/Contents/Info.plist').exists())

    def test_compare_detects_bytes_modes_root_modes_missing_and_extra(self):
        original=inventory.scan(self.vendor)
        destination=self.root/'copy'; shutil.copytree(self.vendor,destination)
        (destination/'codex-path/rg').chmod(0o644)
        self.assertIn('codex-path/rg',inventory.compare(inventory.scan(destination),original)['differing'])
        (destination/'codex-path/rg').write_text('changed')
        (destination/'bin/codex').unlink(); (destination/'extra').write_text('extra')
        destination.chmod(0o700)
        result=inventory.compare(inventory.scan(destination),original)
        self.assertFalse(result['equal']); self.assertFalse(result['root_mode_equal'])
        self.assertIn('bin/codex',result['missing']); self.assertIn('extra',result['extra'])

    def test_manifest_utf8_order_and_final_newline(self):
        for name in ('é','z'): (self.vendor/name).write_text(name)
        tree=inventory.scan(self.vendor)
        regular=sorted([e for e in tree['entries'] if e['kind']=='file'],key=lambda e:e['path'].encode('utf-8'))
        expected=''.join(e['sha256']+'  '+e['path']+'\n' for e in regular)
        self.assertEqual(tree['manifest_sha256'],inventory.sha256(expected.encode('utf-8')))

    def test_file_and_directory_links_not_followed_and_not_staged(self):
        external=self.root/'external'; external.mkdir(); (external/'secret').write_text('not read')
        (self.vendor/'file-link').symlink_to(external/'secret')
        (self.vendor/'dir-link').symlink_to(external,target_is_directory=True)
        tree=inventory.scan(self.vendor)
        self.assertEqual(sum(e['kind']=='symlink' for e in tree['entries']),2)
        self.assertFalse(any('secret' in e['path'] for e in tree['entries']))
        with self.assertRaisesRegex(ValueError,'links and special'): self.run_prepare()
        self.assertFalse(self.output.exists())
        changed=json.loads(json.dumps(tree)); next(e for e in changed['entries'] if e['path']=='file-link')['target']='another'
        self.assertIn('file-link',inventory.compare(changed,tree)['differing'])

    def test_root_symlinks_and_output_symlinks_refused(self):
        alias=self.root/'alias'; alias.symlink_to(self.vendor,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'): inventory.scan(alias)
        self.output.symlink_to(self.root/'elsewhere',target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'): self.run_prepare()
        self.assertFalse((self.root/'elsewhere').exists())

    def test_special_file_and_unrepresentable_name_refused(self):
        fifo=self.vendor/'fifo'; os.mkfifo(fifo)
        self.assertEqual(next(e for e in inventory.scan(self.vendor)['entries'] if e['path']=='fifo')['kind'],'other')
        with self.assertRaisesRegex(ValueError,'special'): self.run_prepare()
        fifo.unlink(); (self.vendor/'bad\nname').write_text('bad')
        with self.assertRaisesRegex(ValueError,'line break'): inventory.scan(self.vendor)

    def test_missing_tree_pin_manifest_or_entrypoint_refused(self):
        with self.assertRaises(OSError): inventory.scan(self.root/'absent')
        with self.assertRaisesRegex(ValueError,'manifest'): self.run_prepare(expected_manifest='0'*64)
        with self.assertRaisesRegex(ValueError,'metadata'): self.run_prepare(pin='0.158.0')
        (self.vendor/'bin/codex').chmod(0o644)
        with self.assertRaisesRegex(ValueError,'executable Mach-O'): self.run_prepare()
        self.assertFalse(self.output.exists())

    def test_selected_resources_are_inspected_without_claiming_placement(self):
        guidance=self.root/'AGENTS.md'; guidance.write_text('invented product guidance')
        self.inputs.write_text(json.dumps({'guidance':str(guidance),'bundle_id':'dev.invented.app','minimum_macos':'15.0'}))
        result=self.run_prepare()
        self.assertEqual(result['input_account']['items']['guidance']['state'],'inspected_not_staged')
        self.assertEqual(result['configuration']['CF-5']['minimum_macos'],'15.0')
        self.assertEqual(result['configuration']['CF-3']['P-3'],'not staged')
        self.assertFalse(result['package_complete'])

    def test_missing_selected_file_unknown_fields_and_duplicate_json_refused(self):
        for text in (json.dumps({'guidance':str(self.root/'absent')}),'{"token":"not permitted"}','{"bundle_id":null,"bundle_id":"x.y"}'):
            self.inputs.write_text(text)
            with self.assertRaises((OSError,ValueError)): self.run_prepare()
        self.assertFalse(self.output.exists())

    def test_output_never_reuses_or_overlaps_source(self):
        self.output.mkdir(); (self.output/'keep').write_text('unchanged')
        with self.assertRaises(FileExistsError): self.run_prepare()
        self.assertEqual((self.output/'keep').read_text(),'unchanged')
        with self.assertRaisesRegex(ValueError,'overlap'): self.run_prepare(output=self.vendor/'stage')

    def test_relative_and_dotdot_inputs_cannot_overlap_staging(self):
        workflows=self.root/'workflows'; workflows.mkdir()
        (self.root/'subdir').mkdir()
        original_cwd=Path.cwd()
        try:
            for relative in ('workflows','subdir/../workflows','./workflows'):
                with self.subTest(source=relative):
                    os.chdir(self.root)
                    self.inputs.write_text(json.dumps({'workflows':relative}))
                    before=inventory.scan(workflows)
                    destination=workflows/'stage'
                    with self.assertRaisesRegex(ValueError,'overlap'):
                        self.run_prepare(output=destination)
                    self.assertFalse(destination.exists())
                    self.assertTrue(inventory.compare(inventory.scan(workflows),before)['equal'])
            # Also exercise .. from a nested cwd, not just a lexical alias.
            os.chdir(self.root/'subdir')
            self.inputs.write_text(json.dumps({'workflows':'../workflows'}))
            with self.assertRaisesRegex(ValueError,'overlap'):
                self.run_prepare(output=workflows/'stage')
            self.assertFalse((workflows/'stage').exists())
        finally:
            os.chdir(original_cwd)

    def test_copy_failure_has_marker_and_no_success_report(self):
        with patch.object(prepare,'copy_supplier',side_effect=ValueError('simulated copy failure')):
            with self.assertRaisesRegex(ValueError,'copy failure'): self.run_prepare()
        self.assertTrue((self.output/'INCOMPLETE.txt').exists())
        self.assertFalse((self.output/'preparation.json').exists())

    def test_signature_display_failures_never_pass_fp0(self):
        tree=inventory.scan(self.vendor)
        failed=subprocess.CompletedProcess([],1,b'',b'code object is not signed at all')
        def fake_run(args,**kwargs):
            if kwargs.get('text'): return subprocess.CompletedProcess(args,1,'','code object is not signed at all')
            return failed
        with patch.object(inventory.subprocess,'run',side_effect=fake_run):
            result=inventory.inspect_signatures(tree)
        self.assertEqual(result['outcome'],'fail')
        self.assertFalse(result['files'][0]['fp0_file_preconditions'])

    def test_unavailable_signature_observation_is_inconclusive(self):
        tree=inventory.scan(self.vendor)
        def fake_run(args,**kwargs):
            if kwargs.get('text'): return subprocess.CompletedProcess(args,0,'','Authority=(unavailable)\nTeamIdentifier=2DC432GLL2\n')
            return subprocess.CompletedProcess(args,0,b'',b'warning: binary contains an invalid entitlements blob')
        with patch.object(inventory.subprocess,'run',side_effect=fake_run):
            result=inventory.inspect_signatures(tree)
        self.assertEqual(result['outcome'],'inconclusive')
        self.assertFalse(result['files'][0]['fp0_file_preconditions'])

    def test_malformed_entitlements_cannot_pass(self):
        tree=inventory.scan(self.vendor)
        def fake_run(args,**kwargs):
            if kwargs.get('text'):
                return subprocess.CompletedProcess(args,0,'','Authority=Developer ID Application: Example (2DC432GLL2)\nTeamIdentifier=2DC432GLL2\nTimestamp=now\nCodeDirectory flags=0x10000(runtime)\n')
            return subprocess.CompletedProcess(args,0,b'<?xml version="1.0"?><plist><dict>',b'')
        with patch.object(inventory.subprocess,'run',side_effect=fake_run):
            result=inventory.inspect_signatures(tree)
        self.assertEqual(result['outcome'],'inconclusive')

    def test_cli_bad_manifest_is_nonzero_without_output(self):
        proc=subprocess.run([sys.executable,str(APP/'packaging/prepare.py'),'prepare','--vendor',str(self.vendor),'--expected-manifest','0'*64,'--pin','0.160.0','--candidate-revision','INVENTED','--inputs',str(self.inputs),'--output',str(self.output)],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2,proc.stderr)
        self.assertFalse(json.loads(proc.stdout)['preparation_complete'])
        self.assertFalse(self.output.exists())


if __name__=='__main__': unittest.main(verbosity=2)
