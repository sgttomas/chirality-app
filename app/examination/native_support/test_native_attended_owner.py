import contextlib,io,json,os,tempfile
from pathlib import Path
from types import SimpleNamespace as N
import unittest
from native_attended_owner import OwnerChannel
class Tests(unittest.TestCase):
    def test_exact_actual_completion_once(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();(root/'B').mkdir()
            channel=OwnerChannel(root,'candidate',N(receipts={'B':{'admission_sha256':'a'*64}}),clock=lambda:0)
            with contextlib.redirect_stdout(io.StringIO()) as out:channel.deliver({'event':'owner-cancel-needed-now','incarnation':'B'})
            message=json.loads(out.getvalue());p=Path(message['completion_file'])
            p.write_text(json.dumps(message['completion_offer']));p.chmod(0o600)
            self.assertEqual(channel.completion('B',10),'Cancelled')
            with self.assertRaises(RuntimeError):channel.completion('B',10)
    def test_missing_or_other_incarnation_never_completes(self):
        with tempfile.TemporaryDirectory() as d:
            c=OwnerChannel(Path(d).resolve(),'candidate',N(receipts={}),clock=lambda:0)
            with self.assertRaises(RuntimeError):c.completion('B',10)
            with self.assertRaises(RuntimeError):c.deliver({'event':'owner-cancel-needed-now','incarnation':'B'})
