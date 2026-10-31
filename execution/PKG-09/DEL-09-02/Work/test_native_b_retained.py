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

if __name__=='__main__':unittest.main()
