"""Invented-state admission tests; no App, supplier or actual account reads."""
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('retained_tests',HERE/'native_b_retained.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class Retained(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir='/Users/ryan/dev/chirality-t3/scratch',prefix='retained-admission-fixture-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.db=self.root/'ledger.sqlite'
        c=sqlite3.connect(self.db);c.executescript('CREATE TABLE ledger_meta(key,value); INSERT INTO ledger_meta VALUES ("schema","1"); CREATE TABLE ledger_entry(seq INTEGER PRIMARY KEY,entry TEXT);')
        self.rows=[{'kind':'session_started','session':'fixture','at':'start'},
                   {'kind':'quit_requested','session':'fixture','at':'quit','liveTurns':[],'outstandingEntries':[],'activeDescendants':[]},
                   {'kind':'session_ended','session':'fixture','at':'end','how':'quit','stopRequests':[]}]
        c.executemany('INSERT INTO ledger_entry VALUES (?,?)',[(i,json.dumps(v)) for i,v in enumerate(self.rows)]);c.commit();c.close()
        self.schema=self.root/'schema.json';self.schema.write_text('{"type":"object"}')
        self.addCleanup(patch.stopall)
        patch.object(r,'DATABASE_SHA',r.digest(self.db)).start()
        self.lsof=patch.object(r.subprocess,'run',return_value=SimpleNamespace(returncode=1,stdout='',stderr='')).start()
    def test_exact_three_rows_and_readonly_hash_preserved(self):
        before=r.digest(self.db);v=r.ledger_projection(self.db,self.schema)
        self.assertEqual(v['listed_work_counts'],[0,0,0]);self.assertEqual(before,r.digest(self.db))
        self.assertEqual(self.lsof.call_count,2)
        self.assertTrue(all('--' in call.args[0] and str(self.db) in call.args[0] for call in self.lsof.call_args_list))
    def test_sidecar_or_current_descriptor_or_unknown_observation_refuses(self):
        for suffix in ('-wal','-shm','-journal'):
            side=Path(str(self.db)+suffix);side.touch()
            with self.assertRaisesRegex(RuntimeError,'sidecar'):r.ledger_projection(self.db,self.schema)
            side.unlink()
        for result in [SimpleNamespace(returncode=0,stdout='p123\n',stderr=''),SimpleNamespace(returncode=1,stdout='',stderr='cannot observe')]:
            self.lsof.return_value=result
            with self.assertRaisesRegex(RuntimeError,'descriptor'):r.ledger_projection(self.db,self.schema)
    def test_changed_database_and_required_ledger_facts_refuse(self):
        c=sqlite3.connect(self.db);self.rows[1]['liveTurns']=['invented'];c.execute('UPDATE ledger_entry SET entry=? WHERE seq=1',(json.dumps(self.rows[1]),));c.commit();c.close()
        with self.assertRaisesRegex(RuntimeError,'database changed'):r.ledger_projection(self.db,self.schema)
        with patch.object(r,'DATABASE_SHA',r.digest(self.db)):
            with self.assertRaisesRegex(RuntimeError,'lists work'):r.ledger_projection(self.db,self.schema)
    def test_writer_or_sidecar_appearing_after_read_refuses(self):
        self.lsof.side_effect=[SimpleNamespace(returncode=1,stdout='',stderr=''),SimpleNamespace(returncode=0,stdout='p123',stderr='')]
        with self.assertRaisesRegex(RuntimeError,'descriptor'):r.ledger_projection(self.db,self.schema)
    def test_metadata_refuses_links_and_ownership_and_tracks_opaque_drift(self):
        opaque=self.root/'opaque.sqlite';opaque.write_bytes(b'never parse supplier contents')
        before=r.metadata({'fixture':self.root},{})
        opaque.write_bytes(b'changed')
        self.assertNotEqual(before,r.metadata({'fixture':self.root},{}))
        link=self.root/'foreign';link.symlink_to('/tmp')
        with self.assertRaisesRegex(RuntimeError,'symlink'):r.metadata({'fixture':self.root},{})
        link.unlink()
        with patch.object(r.os,'getuid',return_value=os.getuid()+1):
            with self.assertRaisesRegex(RuntimeError,'ownership'):r.metadata({'fixture':self.root},{})
    def test_basis_version_and_projection_drift_refuse(self):
        basis=self.root/'basis.json';basis.write_text(json.dumps({'version':'old'}))
        with self.assertRaisesRegex(RuntimeError,'version'):r.admit(SimpleNamespace(setup=SimpleNamespace(T3=Path('/Users/ryan/dev/chirality-t3'))),basis)
        baseline={'version':r.VERSION,'a_root':str(self.root),'projection_path':str(self.schema),'a_files':{}}
        basis.write_text(json.dumps(baseline))
        with patch.object(r,'observation',return_value=(None,{},None,{**baseline,'changed':True})):
            with self.assertRaisesRegex(RuntimeError,'state/source/projection'):r.admit(SimpleNamespace(setup=SimpleNamespace(T3=Path('/Users/ryan/dev/chirality-t3'))),basis)

    def test_saved_request_bytes_and_reference_tuple_must_both_match(self):
        raw=b'invented saved request';bindings={'request_sha256':__import__('hashlib').sha256(raw).hexdigest(),'request':{'home':'invented'}}
        with patch.object(r,'REQUEST_SHA',bindings['request_sha256']):
            r.saved_request_gate(raw,{'home':'invented'},bindings)
            for changed_raw,changed_record in [(b'changed',{'home':'invented'}),(raw,{'home':'foreign'})]:
                with self.assertRaisesRegex(RuntimeError,'saved A'):r.saved_request_gate(changed_raw,changed_record,bindings)
    def test_auth_addition_or_missing_supplier_file_or_extra_tmp_refuses(self):
        account=self.root/'account';account.mkdir()
        for name in r.SUPPLIER_NAMES|set(r.LINKS):
            if name=='tmp':(account/name).mkdir();(account/name/'arg0').mkdir()
            else:(account/name).touch()
        r.account_layout(account)
        extra=account/'auth.json';extra.touch()
        with self.assertRaisesRegex(RuntimeError,'supplier/auth'):r.account_layout(account)
        extra.unlink();extra=account/'tmp/foreign';extra.touch()
        with self.assertRaisesRegex(RuntimeError,'tmp metadata'):r.account_layout(account)
        extra.unlink();(account/'installation_id').unlink()
        with self.assertRaisesRegex(RuntimeError,'supplier/auth'):r.account_layout(account)

    def test_required_links_reject_regular_file_and_wrong_target(self):
        account=self.root/'links';account.mkdir();paths={}
        for name,key in r.LINKS.items():
            target=self.root/('target-'+key);target.touch();paths[key]=str(target)
            (account/name).symlink_to(target)
        r.required_links(account,paths)
        (account/'AGENTS.md').unlink();(account/'AGENTS.md').write_text('regular replacement')
        with self.assertRaisesRegex(RuntimeError,'required account link'):r.required_links(account,paths)
        (account/'AGENTS.md').unlink();(account/'AGENTS.md').symlink_to(self.schema)
        with self.assertRaisesRegex(RuntimeError,'required account link'):r.required_links(account,paths)
    def test_hardlink_and_descriptor_timeout_refuse(self):
        linked=self.root/'db-link';os.link(self.db,linked)
        with self.assertRaisesRegex(RuntimeError,'additional links'):r.owned_plain(self.db)
        linked.unlink()
        self.lsof.side_effect=r.subprocess.TimeoutExpired('lsof',3)
        with self.assertRaises(r.subprocess.TimeoutExpired):r.ledger_projection(self.db,self.schema)
    def test_observation_rejects_wrong_original_source_and_projection_provenance(self):
        b=SimpleNamespace(setup=SimpleNamespace(T3=self.root))
        a=self.root/'scratch/app-successor-native-A-irf2swd9'
        projection=self.root/'scratch/app-native-next-admission-35viga7p/retained-runtime-projection.json'
        with self.assertRaisesRegex(RuntimeError,'A source'):r.observation(b,self.root,projection)
        with self.assertRaisesRegex(RuntimeError,'projection source'):r.observation(b,a,self.schema)
        projection.parent.mkdir(parents=True);projection.write_text('{}')
        with self.assertRaisesRegex(RuntimeError,'projection changed'):r.observation(b,a,projection)
    def test_retained_inputs_bind_original_files_paths_and_exact_new_directory_names(self):
        fixture=self.root/'witness-inputs';(fixture/'shared/skills/.system').mkdir(parents=True)
        (fixture/'project/.chirality').mkdir(parents=True);(fixture/'project/.chirality/project.json').write_text('opaque generated metadata')
        (fixture/'shared/config.toml').write_text('invented');(fixture/'shared/AGENTS.md').write_text('invented')
        identity='invented.namespace';bundle=self.root/'target/debug/bundle/macos/invented.app'
        executable=bundle/'Contents/MacOS/invented'
        paths={'shared_config':str(fixture/'shared/config.toml'),'shared_agents':str(fixture/'shared/AGENTS.md'),'shared_skills':str(fixture/'shared/skills'),'project':str(fixture/'project')}
        value={'candidate_key':r.CANDIDATE,'bundle_identifier':identity,'bundle':str(bundle),'executable':str(executable),'executable_sha256':'invented-sha',
               'expected_app_data':str(Path.home()/'Library/Application Support'/identity),'native_input_paths':paths,
               'files':{n:r.digest(fixture/n) for n in ('shared/config.toml','shared/AGENTS.md')},
               'environment':{'HOME':str(Path.home()),'PATH':str(bundle/'Contents/Resources/codex/codex-path')+':/usr/bin:/bin:/usr/sbin:/sbin','LANG':'en_US.UTF-8','CODEX_HOME':str(fixture/'fallback-codex-home'),'TMPDIR':str(fixture/'tmp')}}
        manifest=fixture/'input-manifest.json';manifest.write_text(json.dumps(value))
        context=SimpleNamespace(inputs_path=manifest,build_root=self.root,identifier=identity,file_digests={str(manifest):r.digest(manifest)},
                                identified={'candidate_key':r.CANDIDATE,'bundle':{'name':'invented.app','executable':{'path':'Contents/MacOS/invented','sha256':'invented-sha'}}})
        self.assertEqual(r.retained_inputs(context),value)
        extra=fixture/'shared/skills/foreign';extra.touch()
        with self.assertRaisesRegex(RuntimeError,'shared-skills'):r.retained_inputs(context)
        extra.unlink();(fixture/'project/foreign').touch()
        with self.assertRaisesRegex(RuntimeError,'project entries'):r.retained_inputs(context)
        (fixture/'project/foreign').unlink();(fixture/'shared/config.toml').write_text('changed')
        with self.assertRaisesRegex(RuntimeError,'fixture file'):r.retained_inputs(context)

if __name__=='__main__':unittest.main()
