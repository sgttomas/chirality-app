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
