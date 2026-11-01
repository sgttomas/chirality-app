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
            with patch.object(retained,'ASSESSMENT_SHA',digest),patch.object(Path,'home',return_value=home),patch.object(Path,'read_bytes',no_opaque),patch.object(retained.subprocess,'run',side_effect=commands):
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
