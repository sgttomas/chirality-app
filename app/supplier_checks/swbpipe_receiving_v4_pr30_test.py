"""PR30 source correspondence; unchanged v4 fixture behavior, no host execution."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import swbpipe_catalog_v4_pr30_receiving as successor
import swbpipe_catalog_v4_receiving as original
import swbpipe_receiving_v4_test as behavior


class PR30SourceReceiving(unittest.TestCase):
    def test_exact_publication_subjects_share_catalog_not_source_identity(self):
        new=successor.selection();old=original.selection()
        self.assertEqual(new['commit'],'a659523a75dbbf2cdfcccdf8a667b6fb482e10ea')
        self.assertEqual(new['checked_head'],'0c729ce5d09636341521f117e075d1a8d07acf32')
        self.assertEqual(old['commit'],'9b6281e7eaca924e6166336b87b6d25937c1ca04')
        self.assertEqual(new['historical_test_citation']['commit'],old['commit'])
        self.assertNotEqual(original.PINS_SHA256,successor.PINS_SHA256)
        self.assertEqual(successor.load_catalog(),original.load_catalog())
        self.assertEqual(len(new['sources']),5)
        self.assertEqual(new['sources'][-1]['path'],'apps/desktop/src/features/model-tree/removalIntents.ts')
        self.assertNotIn('embeddedAgentM2.test.ts',[s['path'].split('/')[-1] for s in new['sources']])
        for source in new['sources'][:2]:
            self.assertEqual(source['bytes'],50864)
            self.assertEqual(source['sha256'],original.CATALOG_SHA256)

    def test_changed_missing_new_dependency_or_mixed_profile_refuses(self):
        pins=successor.selection()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for source in pins['sources']:
                target=root/source['snapshot'];target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((successor.ROOT/source['snapshot']).read_bytes())
            with patch.object(successor,'ROOT',root):
                successor.load_catalog()
                for source in pins['sources']:
                    path=root/source['snapshot'];raw=path.read_bytes()
                    path.write_bytes(raw+b'\n')
                    with self.subTest(source=source['path']),self.assertRaisesRegex(ValueError,'selected source changed'):successor.load_catalog()
                    path.unlink()
                    with self.assertRaises(FileNotFoundError):successor.load_catalog()
                    path.write_bytes(raw)
                for source in pins['sources'][2:4]:
                    previous=next(s for s in original.selection()['sources'] if s['path']==source['path'])
                    path=root/source['snapshot'];raw=path.read_bytes()
                    path.write_bytes((original.ROOT/previous['snapshot']).read_bytes())
                    with self.assertRaisesRegex(ValueError,'selected source changed'):successor.load_catalog()
                    path.write_bytes(raw)
        with patch.object(successor,'PINS',original.PINS):
            with self.assertRaisesRegex(ValueError,'selection changed'):successor.load_catalog()
        with patch.object(original,'PINS',successor.PINS):
            with self.assertRaisesRegex(ValueError,'selection changed'):original.load_catalog()

    def test_source_delta_retains_before_builder_and_remaining_producer(self):
        new=successor.selection();old=original.selection()
        def read(pins,suffix):
            source=next(s for s in pins['sources'] if s['path'].endswith(suffix))
            return (successor.ROOT/source['snapshot']).read_text()
        previous=read(old,'embeddedAgentSession.ts');current=read(new,'embeddedAgentSession.ts')
        self.assertEqual(previous[previous.index('export async function recordBefore'):],
                         current[current.index('export async function recordBefore'):])
        self.assertIn("import { nodeDeletionSummary, pipeDeletionSummary, supportDeletionSummary } from '../features/model-tree/removalIntents';",current)
        self.assertNotIn('export function engineDisplayNumber',current)
        shared=read(new,'removalIntents.ts')
        for name in ('nodeDeletionSummary','pipeDeletionSummary','supportDeletionSummary','applierDisplayNumber'):
            self.assertIn('export function '+name,shared)
        self.assertIn('if(blankText(record.label))return',current)
        self.assertIn('[record.from,record.to,record.material].some(blankText)',current)
        self.assertIn("typeof position[axis]==='number'&&Number.isFinite(position[axis])",current)
        # This is source correspondence, not running the formatter or native applier.

    def test_existing_focused_behavior_with_explicit_successor_catalog(self):
        # Reuse maintained exact tests rather than copying implementation tests.
        # Only source-specific assertions remain in the independent PR27 suite.
        methods=(
            'test_exact_before_text_requires_same_host_target_and_basis',
            'test_cursors_bind_family_filter_run_basis_and_offset',
            'test_records_live_basis_family_rows_and_utf8_limits',
            'test_unicode_record_pages_complete_without_ascii_escape_inflation',
            'test_javascript_entry_serialization_and_utf16_id_boundary',
            'test_drift_with_invalid_record_preserves_both_producer_check_points',
        )
        with patch.object(behavior,'CAT',successor.load_catalog()):
            for name in methods:
                with self.subTest(behavior=name):
                    case=behavior.V4Receiving(name)
                    result=unittest.TestResult()
                    # The reused legacy fixture mutates a shallow-copied page.
                    # Supply each invocation its original isolated page basis.
                    args=copy.deepcopy(behavior.ARGS);args['page']={'cursor':None,'limit':2}
                    with patch.object(behavior,'ARGS',args):case.run(result)
                    self.assertEqual(result.errors,[])
                    self.assertEqual(result.failures,[])
                    self.assertEqual(result.skipped,[])
                    self.assertEqual(result.testsRun,1)


if __name__=='__main__':unittest.main()
