"""Invented metadata/profile negatives; opaque bytes are never read."""
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace as N
import unittest
from unittest.mock import patch
import native_attended_retained_shell as retained

class Tests(unittest.TestCase):
    def fixture(self,home):
        paths=retained.roots(home)
        for key,count in [('WebKit',21),('Caches',10)]:
            paths[key].mkdir(parents=True)
            for index in range(count-1):(paths[key]/('opaque-'+str(index))).write_text('invented opaque fixture')
        value={'format':'attended-post-attempt-metadata/v1','candidate':retained.CANDIDATE,
               'identifier':retained.IDENTIFIER,'prior_attempt':'app-attended-prepared-i_bow2kd',
               'stable_metadata':True,'namespaces':retained.metadata(home)}
        return value
    def test_exact_metadata_and_selected_digest_without_opaque_reads(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d).resolve();value=self.fixture(home);path=home/'assessment.json'
            raw=(json.dumps(value,indent=2)+'\n').encode();path.write_bytes(raw);path.chmod(0o600)
            digest=hashlib.sha256(raw).hexdigest()
            def commands(argv,**kwargs):return N(returncode=1 if argv[0].endswith('lsof') else 0,stdout='',stderr='')
            original=Path.read_bytes
            def no_opaque(path):
                if path.name.startswith('opaque-'):raise AssertionError('opaque bytes read')
                return original(path)
            with patch.object(retained,'ASSESSMENT_PATH',path),patch.object(retained,'ASSESSMENT_SHA',digest),patch.object(Path,'home',return_value=home),patch.object(Path,'read_bytes',no_opaque),patch.object(retained.subprocess,'run',side_effect=commands):
                result=retained.verify(path,digest,'/invented/App')
            self.assertEqual(result['version'],retained.VERSION);self.assertIsNone(result['saved_A']);self.assertIsNone(result['ledger'])
    def test_unknown_future_basis_refuses_before_any_process_observation(self):
        with patch.object(retained.subprocess,'run') as run,self.assertRaisesRegex(RuntimeError,'unselected'):
            retained.verify('/invented/nonexistent','f'*64,'/invented/App')
        run.assert_not_called()
    def test_metadata_drift_and_operational_state_refuse(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d).resolve();value=self.fixture(home)
            for field in ['size','mtime_ns','ctime_ns','inode','mode']:
                changed=copy.deepcopy(value['namespaces']);changed['WebKit']['metadata'][1][field]+=1
                with self.subTest(field=field),self.assertRaisesRegex(RuntimeError,'drift'):retained.check_snapshot(value,home,changed)
            changed=copy.deepcopy(value);changed['namespaces']['AppData']['present']=True
            with self.assertRaisesRegex(RuntimeError,'operational'):retained.shape(changed,home)
    def test_extra_file_or_symlink_not_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d).resolve();value=self.fixture(home);root=retained.roots(home)['Caches']
            (root/'extra').write_text('invented')
            with self.assertRaisesRegex(RuntimeError,'drift'):retained.check_snapshot(value,home,retained.metadata(home))
            (root/'alias').symlink_to(root/'extra')
            with self.assertRaisesRegex(RuntimeError,'linked'):retained.metadata(home)

class ReaderRefusals(unittest.TestCase):
    def exercise(self,change):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d).resolve();value=Tests().fixture(home);path=home/'assessment.json'
            raw=json.dumps(value).encode();path.write_bytes(raw);path.chmod(0o600);digest=hashlib.sha256(raw).hexdigest()
            selected=path
            if change=='copy':
                other=home/'copy';other.mkdir(mode=0o700);selected=other/'assessment.json';selected.write_bytes(raw);selected.chmod(0o600)
            if change=='mode':path.chmod(0o644)
            if change=='link':
                selected=home/'link.json';selected.symlink_to(path)
            if change=='hardlink':os.link(path,home/'second.json')
            if change=='removed':(retained.roots(home)['WebKit']/'opaque-0').unlink()
            def commands(argv,**kwargs):
                if argv[0].endswith('lsof'):return N(returncode=0 if change=='open' else 1,stdout='p123\n' if change=='open' else '',stderr='')
                return N(returncode=0,stdout='123 1 /invented/App' if change=='process' else '',stderr='')
            with patch.object(retained,'ASSESSMENT_PATH',path),patch.object(retained,'ASSESSMENT_SHA',digest),patch.object(Path,'home',return_value=home),patch.object(retained.subprocess,'run',side_effect=commands),self.assertRaises(RuntimeError):
                retained.verify(selected,digest,'/invented/App')
    def test_reader_refuses_copy_alias_mode_hardlink_drift_and_active_observation(self):
        for change in ['copy','mode','link','hardlink','removed','open','process']:
            with self.subTest(change=change):self.exercise(change)

class DispatchTests(unittest.TestCase):
    def test_final_clock_check_follows_A_preflight(self):
        import native_attended_admission as admission
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();phase=root/'A';phase.mkdir(mode=0o700)
            for name in ['tmp','helper-tmp','codex-home']:(phase/name).mkdir()
            (phase/'phase.sb').write_text('fixture')
            now=[0];a=admission.NativeAdmissions.__new__(admission.NativeAdmissions)
            a.root=root;a.build_root=root;a.plan_sha='a'*64;a.state_basis={'path':'fixture','sha256':'b'*64}
            a.receipts={'A':{'admission_id':'fixture'}};a.recheck_inputs=lambda:None
            a.value={'bundle':'/invented/App','window_route':{'helper_sources':{}}};a.plan={'build_identity':'fixture'}
            a.identify=N(identity=lambda inv:'fixture',inventory=lambda path:{})
            a.clock=lambda:now[0];a.policy=lambda *args:'fixture'
            def late(*args):now[0]=161
            with patch.object(admission,'preflight_a',side_effect=late) as check,self.assertRaisesRegex(RuntimeError,'final admission crossed'):
                a.before_launch('A',a.receipts['A'],295)
            check.assert_called_once_with(root,a.plan_sha,a.identify,a.state_basis)
    def test_cli_requires_both_retained_flags(self):
        import subprocess,sys
        entry=Path(__file__).with_name('native_attended_entry.py')
        for flag,value in [('--retained-basis','/invented/basis'),('--retained-sha256','a'*64)]:
            r=subprocess.run([sys.executable,'-I','-B',str(entry),'prepare','--build-root','/invented',flag,value],capture_output=True,text=True,timeout=5)
            self.assertNotEqual(r.returncode,0);self.assertIn('both retained basis and digest required',r.stderr)
    def test_entry_check_rejects_same_digest_basis_at_other_path(self):
        import native_attended_entry as entry
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700)
            manifest={'controller_root':str(root),'entry_source':str(Path(entry.__file__).resolve()),
                'candidate':entry.CANDIDATE,'plan_sha256':entry.PLAN_SHA,'total_seconds':295,
                'Stop_entry_reserve':135,'launch_limit':2,'Stop_confirmation':False,'PR69_active':False,
                'state_basis':{'path':'/invented/copy.json','sha256':retained.ASSESSMENT_SHA}}
            path=root/'prepared.json';path.write_text(json.dumps(manifest));path.chmod(0o600)
            with patch.object(entry,'SCRATCH',root.parent),self.assertRaisesRegex(RuntimeError,'retained basis descriptor changed'):
                entry.check(root,entry.sha(path))
    def test_preflight_rejects_wrong_candidate_identifier_and_extra_descriptor(self):
        import native_attended_admission as admission
        for change in ['candidate','identifier','descriptor']:
            with self.subTest(change=change),tempfile.TemporaryDirectory() as d:
                root=Path(d).resolve();fixture=root/'witness-inputs';fixture.mkdir()
                for name in ['shared','shared/skills','project','fallback-codex-home','tmp']:(fixture/name).mkdir()
                for name in ['shared/config.toml','shared/AGENTS.md']:(fixture/name).write_text('invented')
                bundle=root/'target/debug/bundle/macos/Fixture.app';bundle.mkdir(parents=True)
                exe=bundle/'Contents/MacOS/app';exe.parent.mkdir(parents=True);exe.write_text('fixture only')
                build={'exit_code':0,'profile':'debug','features':['custom-protocol'],'command':['--debug'],'source_revision':'a'*40}
                (root/'build-invocation.json').write_text(json.dumps(build))
                candidate='wrong' if change=='candidate' else retained.CANDIDATE
                identifier='wrong' if change=='identifier' else retained.IDENTIFIER
                plan={'format':'attended-invented-input-plan/v1','launch_ready':False,'saved_A':None,'ledger':None,
                    'launch_limit':2,'total_seconds':295,'minimum_remaining_before_Stop':135,'Stop_confirmation_allowed':False,
                    'PR69_active':False,'candidate':candidate,'identifier':identifier,'source_revision':'a'*40,
                    'build_identity':'fixture-build','build_profile':'debug','features':['custom-protocol'],
                    'build_invocation_sha256':admission.sha(root/'build-invocation.json'),'executable':str(exe),'executable_sha256':admission.sha(exe),
                    'input_paths':{k:str(fixture/v) for k,v in [('shared_config','shared/config.toml'),('shared_agents','shared/AGENTS.md'),('shared_skills','shared/skills'),('project','project')]},
                    'files':{name:admission.sha(fixture/name) for name in ['shared/config.toml','shared/AGENTS.md']}}
                (fixture/'input-plan.json').write_text(json.dumps(plan))
                (root/'build-observation.json').write_text(json.dumps({'candidate_key':candidate,'identifier':identifier,
                    'source_revision':'a'*40,'build_identity':'fixture-build','bundle':str(bundle)}))
                identify=N(identity=lambda inv:'fixture-build',inventory=lambda path:[],app_data_state=lambda name:{})
                basis={'path':str(retained.ASSESSMENT_PATH),'sha256':retained.ASSESSMENT_SHA}
                if change=='descriptor':basis['unexpected']=True
                with patch.object(retained,'verify') as verify,self.assertRaises(RuntimeError):
                    admission.preflight_a(root,admission.sha(fixture/'input-plan.json'),identify,basis)
                verify.assert_not_called()

class PostJSelectionTests(unittest.TestCase):
    def test_profiles_bind_exact_path_digest_and_prior_attempt(self):
        for path,digest,version,prior in [
            (retained.ASSESSMENT_PATH,retained.ASSESSMENT_SHA,retained.VERSION,'app-attended-prepared-i_bow2kd'),
            (retained.POST_J_PATH,retained.POST_J_SHA,'attended-retained-shell/v2','app-attended-prepared-j58087z7'),
            (retained.POST_EL3_PATH,retained.POST_EL3_SHA,'attended-retained-shell/v3','app-attended-prepared-el3pvau4')]:
            with self.subTest(version=version):
                self.assertEqual(retained.selected_profile(path,digest),(version,prior))
                with self.assertRaises(RuntimeError):retained.selected_profile(path.parent/'copy.json',digest)
        with self.assertRaises(RuntimeError):retained.selected_profile(retained.POST_J_PATH,retained.ASSESSMENT_SHA)
        with self.assertRaises(RuntimeError):retained.selected_profile(retained.ASSESSMENT_PATH,retained.POST_J_SHA)
    def test_v2_reader_requires_j580_subject_without_relabelling_v1(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d).resolve();value=Tests().fixture(home);path=home/'assessment.json'
            for prior,accepted in [('app-attended-prepared-i_bow2kd',False),('app-attended-prepared-j58087z7',True)]:
                value['prior_attempt']=prior;raw=json.dumps(value).encode()
                path.write_bytes(raw);path.chmod(0o600);digest=hashlib.sha256(raw).hexdigest()
                def commands(argv,**kw):return N(returncode=1 if argv[0].endswith('lsof') else 0,stdout='',stderr='')
                with patch.object(retained,'POST_J_PATH',path),patch.object(retained,'POST_J_SHA',digest),patch.object(Path,'home',return_value=home),patch.object(retained.subprocess,'run',side_effect=commands) as run:
                    if accepted:
                        result=retained.verify(path,digest,'/invented/App')
                        self.assertEqual(result['version'],'attended-retained-shell/v2')
                        self.assertIsNone(result['saved_A']);self.assertIsNone(result['ledger'])
                    else:
                        with self.assertRaisesRegex(RuntimeError,'subject differs'):retained.verify(path,digest,'/invented/App')
                        run.assert_not_called()

class PostEl3Tests(unittest.TestCase):
    def test_v3_cannot_relabel_prior_attempt_or_use_other_basis(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d).resolve();value=Tests().fixture(home)
            with self.assertRaisesRegex(RuntimeError,'subject differs'):
                retained.shape(value,home,'app-attended-prepared-el3pvau4')
            value['prior_attempt']='app-attended-prepared-el3pvau4'
            retained.shape(value,home,'app-attended-prepared-el3pvau4')
            for path in (retained.POST_J_PATH,retained.ASSESSMENT_PATH):
                with self.assertRaises(RuntimeError):retained.selected_profile(path,retained.POST_EL3_SHA)
