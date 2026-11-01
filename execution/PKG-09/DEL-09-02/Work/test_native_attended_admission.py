import tempfile
from pathlib import Path
import unittest
from native_attended_admission import require_setup_only_ledger_absent

class Tests(unittest.TestCase):
    def test_absence_does_not_create_ledger(self):
        with tempfile.TemporaryDirectory() as d:
            require_setup_only_ledger_absent(d)
            self.assertEqual(list(Path(d).iterdir()),[])
    def test_any_unexpected_ledger_or_sidecar_refuses(self):
        for name in ['recovery.ledger.jsonl','recovery.ledger.sqlite','recovery.ledger.sqlite-journal','recovery.ledger.sqlite-wal']:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
                runtime=Path(d)/'runtime';runtime.mkdir();(runtime/name).write_text('invented')
                with self.assertRaises(RuntimeError):require_setup_only_ledger_absent(d)


class ExecBindingTests(unittest.TestCase):
    def test_original_sandbox_child_exec_transition_is_bounded_not_reselected(self):
        import os
        from types import SimpleNamespace as N
        from unittest.mock import patch
        from native_attended_admission import NativeAdmissions
        kernel={'pid':4,'ppid':os.getpid(),'uid':os.getuid(),'ruid':os.getuid(),'start_sec':5,'start_usec':6}
        samples=[dict(kernel,executable='/usr/bin/sandbox-exec'),dict(kernel,executable='/invented/App')]
        class Backend:
            def identity(self,pid):return samples.pop(0)
            def close(self):pass
        admissions=NativeAdmissions.__new__(NativeAdmissions);admissions.clock=lambda:0;admissions.births={}
        admissions.b=N(screen_support=N(w=N(d=N(NativeBackend=Backend,bound_identity=lambda run,backend:dict(kernel,executable='/invented/App')))))
        run=N(reservation=N(child=N(pid=4),observe=lambda:None),ui_deadline=10,value={'executable':'/invented/App'})
        with patch('time.sleep'):admissions.bind_birth('A',run)
        self.assertEqual(admissions.births['A']['executable'],'/invented/App');self.assertEqual(samples,[])
    def test_replaced_birth_during_exec_refuses(self):
        import os
        from types import SimpleNamespace as N
        from unittest.mock import patch
        from native_attended_admission import NativeAdmissions
        samples=[{'pid':4,'ppid':os.getpid(),'start_sec':5,'executable':'/usr/bin/sandbox-exec'},
                 {'pid':4,'ppid':os.getpid(),'start_sec':6,'executable':'/invented/App'}]
        class Backend:
            def identity(self,pid):return samples.pop(0)
            def close(self):pass
        a=NativeAdmissions.__new__(NativeAdmissions);a.clock=lambda:0;a.births={}
        a.b=N(screen_support=N(w=N(d=N(NativeBackend=Backend))))
        run=N(reservation=N(child=N(pid=4),observe=lambda:None),ui_deadline=10,value={'executable':'/invented/App'})
        with patch('time.sleep'),self.assertRaises(RuntimeError):a.bind_birth('A',run)
        self.assertFalse(a.births)
