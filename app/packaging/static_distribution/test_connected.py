"""Invented fixtures; real command and built Rust scanner, never supplier execution.
Set DISTRIBUTION_STATIC_BIN explicitly. Wrappers in two tests are named race seams.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
PREPARE = HERE.parent / 'prepare.py'
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').exists())
SCANNER = os.environ.get('DISTRIBUTION_STATIC_BIN')


def sha(raw): return hashlib.sha256(raw).hexdigest()


class Fixture:
    def __init__(self, root, scanner):
        self.root, self.scanner = root, Path(scanner)
        self.artifacts = root / 'artifacts'; self.artifacts.mkdir()
        self.published = root / 'published'; self.published.mkdir()
        for name in ('bin', 'codex-path', 'codex-resources'): (self.published / name).mkdir()
        (self.published / 'bin/codex').write_bytes(bytes.fromhex('cffaedfe') + b'SYNTHETIC BYTES; NEVER EXECUTE')
        (self.published / 'bin/codex').chmod(0o755)
        (self.published / 'codex-package.json').write_text('{"fixture":"not a supplier package"}\n')
        self.packaged = root / 'packaged'; shutil.copytree(self.published, self.packaged)
        inventory = json.loads(subprocess.check_output([str(self.scanner), 'scan', str(self.published)]))
        evidence = self.put('evidence.json', {'standing': 'invented; no observation, human act or qualification', 'incidental': {'path':'not-a-dependency.json','sha256':'3'*64}})
        expected = {'format':'expected-reference.s1','method':'codex-vendor-tree-v1','pin':'9.9.9','platform':'macOS arm64',
            'archive':{'official_source_locator':'synthetic only','sha256':'2'*64,'acquisition_authorization':evidence,'custody':evidence,'extraction_procedure':evidence,'source_subtree':'vendor/synthetic'},
            'inventory':inventory,'launcher':{'kind':'direct-vendor','relative_executable':'bin/codex','path_prefix_relative':'codex-path','removed_wrapper_variables':['CODEX_MANAGED_PACKAGE_ROOT','CODEX_MANAGED_BY_NPM']},
            'generated':{'pin':'9.9.9','kind':'json-schema','variant':'experimental','formatter_policy':'synthetic','manifest_sha256':'1'*64,'provenance':evidence,'version_advance':evidence},
            'label_evidence':evidence,'generation_correspondence':evidence,'author':'synthetic author'}
        er = self.put('expected.json', expected)
        ar = self.put('attestation.json', {'format':'adoption-attestation.s1','expected_reference':er,'author':'synthetic author','independent_reviewer':'synthetic reviewer','reviewed_revision':'synthetic revision','review_evidence':evidence,'adoption':{'actor':'synthetic owner','through_help_human':evidence,'decision':'adopt-for-supplier-reference','evidence':evidence},'limits':['invented; no qualification']})
        selection = self.put('build.json', {'format':'build-selection.s2','method':'codex-vendor-tree-v1','schema_ids':['expected-reference.s1','adoption-attestation.s1'],'expected':er,'attestation':ar})
        legacy = json.loads((HERE / 'fixtures/legacy-template.json').read_text())
        installer = self.put_raw('installer.dmg', b'SYNTHETIC INSTALLER; NOT A DISK IMAGE')
        legacy['app']['installer']['sha256_before_notarisation'] = installer['sha256']
        for side in ('published','packaged'):
            legacy['codex'][side]={'manifest_sha256':inventory['manifest_sha256'],'files':2,'macho_files':1}
        executable = next(e for e in inventory['entries'] if e['path']=='bin/codex')
        legacy['codex']['executables'][0]['sha256_published']=executable['sha256']
        legacy['codex']['executables'][0]['sha256_packaged']=executable['sha256']
        old = self.put('legacy.json', legacy)
        ir = self.put('inventory.json', {'format':'inventory-artifact.s1','inventory':inventory})
        package = self.put('package.json', {'format':'pkg-identity.s1','distribution_status':'reference-equal','legacy_package':legacy,'expected_reference':er,'adoption_attestation':ar,'published_inventory':ir,'packaged_inventory':ir,'verification_artifact':None,'mach_o_paths':['bin/codex']})
        candidate = self.put('candidate.json', {'app_revision':legacy['app']['revision'],'build_identity':legacy['app']['build_identity'],'package_record_id':legacy['record_id'],'installer_sha256_before_notarisation':installer['sha256']})
        self.request={'format':'static-distribution-input/1','build_selection':selection,'s1_package':package,'legacy_package':old,'terms':self.put_raw('terms.json',(HERE/'fixtures/terms.json').read_bytes()),'candidate':candidate,'installer':installer,'scanner':{'sha256':sha(self.scanner.read_bytes()),'declared_source_revision':'synthetic operator selection; not authenticated source provenance'}}
        self.save()

    def put_raw(self, name, raw):
        (self.artifacts/name).write_bytes(raw)
        return {'path':name,'sha256':sha(raw)}
    def put(self, name, value): return self.put_raw(name,(json.dumps(value,indent=2)+'\n').encode())
    def save(self): (self.artifacts/'request.json').write_text(json.dumps(self.request))
    def run(self, prepare=PREPARE, published=True, scanner=None):
        command=[sys.executable,str(prepare),'static-distribution','--request',str(self.artifacts/'request.json'),'--scanner',str(scanner or self.scanner),'--packaged-tree',str(self.packaged)]
        if published: command += ['--published-tree',str(self.published)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=30,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        try: value=json.loads(result.stdout)
        except ValueError: raise AssertionError(result.stderr + result.stdout)
        return result.returncode,value


@unittest.skipUnless(SCANNER, 'explicit built DISTRIBUTION_STATIC_BIN required; never auto-build/download')
class Connected(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve(); self.f=Fixture(self.root,SCANNER)
    def test_real_command_exact_join_never_mints_trust(self):
        code,out=self.f.run();self.assertEqual(code,0,out)
        self.assertEqual(out['standing'],'development-unverifiable');self.assertEqual(out['comparison'],'consistent')
        self.assertTrue(out['value_checks']['S1 package values'])
        self.assertEqual(out['scanner']['sha256'],self.f.request['scanner']['sha256'])
        self.assertEqual(out['selected_artifacts']['legacy.json'],self.f.request['legacy_package']['sha256'])
        self.assertIn('No trusted compiled',out['blockers'][0]);self.assertNotIn('observed_version_label',out)
    def test_opaque_json_evidence_does_not_create_dependencies(self):
        code,out=self.f.run();self.assertEqual(code,0,out)
        self.assertIn('evidence.json',out['selected_artifacts'])
        self.assertNotIn('not-a-dependency.json',out['selected_artifacts'])
        self.assertFalse(any('not-a-dependency' in item for item in out['blockers']))
    def test_legacy_inventory_command_remains_standard_library_only(self):
        env={k:v for k,v in os.environ.items() if k != 'PYTHONPATH'}
        result=subprocess.run([sys.executable,'-S',str(PREPARE),'inventory',str(self.f.published)],capture_output=True,text=True,env=env,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        self.assertIn('manifest_sha256',json.loads(result.stdout))
    def test_mode_only_change_is_mismatch_despite_same_manifest(self):
        (self.f.packaged/'bin/codex').chmod(0o644)
        code,out=self.f.run();self.assertEqual(code,1,out)
        self.assertEqual(out['measurements']['published']['inventory']['manifest_sha256'],out['measurements']['packaged']['inventory']['manifest_sha256'])
        self.assertIn('packaged reference complete inventory',out['mismatches'])
    def test_changed_bytes_are_measured_mismatch(self):
        (self.f.packaged/'bin/codex').write_bytes(b'different')
        code,out=self.f.run();self.assertEqual(code,1,out);self.assertIn('packaged executable bin/codex',out['mismatches'])
    def test_missing_attestation_does_not_hide_tree_or_candidate_contradiction(self):
        (self.f.artifacts/'attestation.json').unlink()
        (self.f.packaged/'bin/codex').chmod(0o644)
        candidate=json.loads((self.f.artifacts/'candidate.json').read_text());candidate['build_identity']='another'
        self.f.request['candidate']=self.f.put('candidate.json',candidate);self.f.save()
        code,out=self.f.run();self.assertEqual(code,1,out)
        self.assertIn('candidate identity',out['mismatches']);self.assertIn('packaged reference complete inventory',out['mismatches'])
        self.assertTrue(any('closure unavailable' in b for b in out['blockers']))
    def test_unmeasured_side_remains_explicit(self):
        code,out=self.f.run(published=False);self.assertEqual(code,0,out)
        self.assertEqual(out['measurements']['published'],{'state':'unmeasured'});self.assertEqual(out['comparison'],'incomplete')
        self.assertNotIn('published legacy manifest',out['value_checks'])
    def test_exact_legacy_bytes_and_duplicate_json_refuse(self):
        (self.f.artifacts/'legacy.json').write_bytes((self.f.artifacts/'legacy.json').read_bytes()+b' ')
        code,out=self.f.run();self.assertEqual(code,2,out);self.assertIn('byte mismatch',out['error'])
        request=self.f.artifacts/'request.json';request.write_text('{"format":"x","format":"y"}')
        code,out=self.f.run();self.assertEqual(code,2,out);self.assertIn('duplicate JSON',out['error'])
    def test_link_and_fifo_inputs_refuse_without_blocking(self):
        path=self.f.artifacts/'installer.dmg';path.unlink();os.mkfifo(path)
        code,out=self.f.run();self.assertEqual(code,2,out);self.assertIn('special',out['error'])
        path.unlink();path.symlink_to(self.f.artifacts/'evidence.json')
        code,out=self.f.run();self.assertEqual(code,2,out)
    def test_type_change_in_actual_tree_refuses(self):
        path=self.f.packaged/'bin/codex';path.unlink();path.symlink_to(self.f.published/'bin/codex')
        code,out=self.f.run();self.assertEqual(code,2,out);self.assertIn('scanner refused',out['error'])
    def test_installer_bytes_must_match_candidate_identity(self):
        self.f.request['installer']=self.f.put_raw('installer.dmg',b'new selected installer');self.f.save()
        code,out=self.f.run();self.assertEqual(code,1,out);self.assertIn('installer exact bytes',out['mismatches'])
    def clone_consumer(self):
        clone=self.root/'source-clone';clone.mkdir();(clone/'AGENTS.md').write_text('Synthetic source-root marker.')
        pins=json.loads((HERE/'sources.json').read_text())
        paths=list(pins['sources']) + [str(p.relative_to(ROOT)) for p in (PREPARE,HERE.parent/'inventory.py',HERE/'check.py',HERE/'__init__.py',HERE/'sources.json')]
        for name in paths:
            destination=clone/name;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,destination)
        return clone,clone/PREPARE.relative_to(ROOT),pins
    def mutation_scanner_seam(self,target):
        # Explicit test-only race seam; the golden test invokes the actual Rust binary directly.
        wrapper=self.root/'mutation-scanner.py'
        wrapper.write_text('#!'+sys.executable+'\nfrom pathlib import Path\nimport os,sys\np=Path('+repr(str(target))+')\np.write_bytes(p.read_bytes()+b" ")\nos.execv('+repr(str(self.f.scanner))+',['+repr(str(self.f.scanner))+',*sys.argv[1:]])\n')
        wrapper.chmod(0o700)
        self.f.request['scanner']['sha256']=sha(wrapper.read_bytes());self.f.save()
        return wrapper
    def test_changed_canonical_source_refuses_before_model_execution(self):
        clone,prepare,pins=self.clone_consumer()
        target=clone/pins['model'];target.write_bytes(target.read_bytes()+b'\n')
        code,out=self.f.run(prepare=prepare);self.assertEqual(code,2,out);self.assertIn('canonical static source changed',out['error'])
    def test_original_source_changed_after_snapshot_refuses(self):
        clone,prepare,pins=self.clone_consumer()
        wrapper=self.mutation_scanner_seam(clone/pins['model'])
        code,out=self.f.run(prepare=prepare,scanner=wrapper);self.assertEqual(code,2,out);self.assertIn('stale original',out['error'])
    def test_original_artifact_changed_after_snapshot_refuses(self):
        wrapper=self.mutation_scanner_seam(self.f.artifacts/'expected.json')
        code,out=self.f.run(scanner=wrapper);self.assertEqual(code,2,out);self.assertIn('stale original',out['error'])
    def test_selected_scanner_tamper_refuses(self):
        self.f.request['scanner']['sha256']='0'*64;self.f.save()
        code,out=self.f.run();self.assertEqual(code,2,out);self.assertIn('scanner byte digest',out['error'])
    def test_selected_legacy_rules_remain_required(self):
        legacy=json.loads((self.f.artifacts/'legacy.json').read_text())
        legacy['signing']['recorded_by']=legacy['signing']['performed_by']
        self.f.request['legacy_package']=self.f.put('legacy.json',legacy);self.f.save()
        code,out=self.f.run();self.assertEqual(code,1,out);self.assertIn('legacy PKG duties: PK-R3',out['mismatches'])
    def test_reference_json_without_json_suffix_still_freezes_nested_closure(self):
        # Repoint both selected parents to the same unchanged bytes under a neutral name.
        expected=self.f.artifacts/'expected.json';renamed=self.f.put_raw('expected.record',expected.read_bytes())
        att=json.loads((self.f.artifacts/'attestation.json').read_text());att['expected_reference']=renamed
        ar=self.f.put('attestation.json',att)
        selection=json.loads((self.f.artifacts/'build.json').read_text());selection.update(expected=renamed,attestation=ar)
        self.f.request['build_selection']=self.f.put('build.json',selection)
        package=json.loads((self.f.artifacts/'package.json').read_text());package.update(expected_reference=renamed,adoption_attestation=ar)
        self.f.request['s1_package']=self.f.put('package.json',package);self.f.save();expected.unlink()
        code,out=self.f.run();self.assertEqual(code,0,out);self.assertIn('evidence.json',out['selected_artifacts'])
    def test_terms_pk_r4_is_checked_separately(self):
        terms=json.loads((self.f.artifacts/'terms.json').read_text())
        terms['state']='response_received'
        terms['response']={'source_ref':'synthetic','custody':'synthetic','obtained_by':terms['recorded_by'],'applies_to':'synthetic','received_on':'2026-10-03'}
        self.f.request['terms']=self.f.put('terms.json',terms);self.f.save()
        code,out=self.f.run();self.assertEqual(code,1,out);self.assertIn('terms PK-R4: PK-R4',out['mismatches'])
    def test_invalid_complete_inventory_is_not_accepted_by_equal_hash(self):
        inventory=json.loads((self.f.artifacts/'inventory.json').read_text())
        inventory['inventory']['entries'].append(dict(inventory['inventory']['entries'][0]))
        changed=self.f.put('inventory.json',inventory)
        package=json.loads((self.f.artifacts/'package.json').read_text())
        package.update(published_inventory=changed,packaged_inventory=changed)
        self.f.request['s1_package']=self.f.put('package.json',package);self.f.save()
        code,out=self.f.run();self.assertEqual(code,2,out);self.assertIn('invalid selected published inventory',out['error'])
    def test_nullable_side_artifact_keeps_measured_facts_and_mismatch_precedence(self):
        package=json.loads((self.f.artifacts/'package.json').read_text())
        package.update(published_inventory=None,distribution_status='unverifiable')
        self.f.request['s1_package']=self.f.put('package.json',package);self.f.save()
        code,out=self.f.run();self.assertEqual(code,0,out);self.assertEqual(out['comparison'],'incomplete')
        self.assertEqual(out['measurements']['published']['state'],'measured')
        self.assertNotIn('published selected complete inventory',out['value_checks'])
        self.assertTrue(any('published inventory artifact not selected' in b for b in out['blockers']))
        (self.f.published/'bin/codex').chmod(0o644)
        code,out=self.f.run();self.assertEqual(code,1,out);self.assertEqual(out['comparison'],'mismatch')
        self.assertIn('published reference complete inventory',out['mismatches'])
    def test_unknown_selection_version_refuses(self):
        value=json.loads((self.f.artifacts/'build.json').read_text());value['format']='build-selection.unknown'
        self.f.request['build_selection']=self.f.put('build.json',value);self.f.save()
        code,out=self.f.run();self.assertEqual(code,2,out);self.assertIn('unknown build selection',out['error'])

if __name__ == '__main__': unittest.main()
