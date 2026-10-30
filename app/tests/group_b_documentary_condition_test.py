"""Current selected meaning and original historical support are distinct checks."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
PROJECT = APP.parent
MANIFEST = PROJECT / 'execution/PKG-09/DEL-09-01/Work/support-identity-v1/documentary-condition.v3.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


subject = load('documentary_condition_tests', APP / 'examination/documentary_condition.py')
canonical = load('documentary_canonical_tests', APP / 'examination/support_identity/canonical.py')
fixtures = load('documentary_canonical_fixtures', APP / 'tests/group_b_support_identity_canonical_test.py')


class DocumentaryConditionTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_bytes())

    def test_every_selected_passage_refuses_changed_meaning_and_duplicate_selector(self):
        for source in self.manifest['sources']:
            raw = (PROJECT / canonical.deliverable_path(PROJECT, source['path'])).read_bytes()
            text = raw.decode()
            for selector in source['selectors']:
                key = selector.get('heading', selector.get('case', selector.get('paragraphPrefix')))
                with self.subTest(source=source['path'], clause=key):
                    if 'heading' in selector:
                        line = next(line for line in text.splitlines(keepends=True) if line.rstrip('\r\n') == key)
                        altered = line + 'CHANGED REQUIRED MEANING\n'
                    elif 'case' in selector:
                        line = next(line for line in text.splitlines(keepends=True) if re.match(r'^\| ' + re.escape(key) + r'\b', line))
                        cells = line.split('|')
                        column = selector.get('columns', [0])[0]
                        cells[column + 1] += ' CHANGED REQUIRED MEANING '
                        altered = '|'.join(cells)
                    else:
                        line = next(line for line in text.splitlines(keepends=True) if line.startswith(key))
                        altered = line.rstrip('\r\n') + ' CHANGED REQUIRED MEANING\n'
                    before = subject.project(raw, [selector])
                    after = subject.project(text.replace(line, altered, 1).encode(), [selector])
                    self.assertNotEqual(before, after)
                    with self.assertRaisesRegex(ValueError, 'missing or repeated'):
                        subject.project((text + '\n' + line).encode(), [selector])

    def test_unread_sections_and_result_status_cells_do_not_change_meaning(self):
        for source in self.manifest['sources']:
            raw = (PROJECT / canonical.deliverable_path(PROJECT, source['path'])).read_bytes()
            with self.subTest(source=source['path']):
                self.assertEqual(subject.project(raw, source['selectors']),
                                 subject.project(raw + b'\n# Unrelated implementation note\nChanged observation.\n', source['selectors']))
            for selector in source['selectors']:
                if 'case' not in selector or 'columns' not in selector:
                    continue
                text = raw.decode()
                line = next(line for line in text.splitlines(keepends=True) if re.match(r'^\| ' + re.escape(selector['case']) + r'\b', line))
                cells = line.split('|')
                excluded = set(range(len(cells) - 2)) - set(selector['columns'])
                for column in excluded:
                    changed = cells.copy(); changed[column + 1] = 'New implementation observation '
                    with self.subTest(case=selector['case'], status_column=column):
                        self.assertEqual(subject.project(raw, [selector]),
                                         subject.project(text.replace(line, '|'.join(changed), 1).encode(), [selector]))
                trim = selector.get('trim_observation')
                if trim:
                    changed = cells.copy()
                    prefix = changed[trim['column'] + 1].split(trim['marker'], 1)[0]
                    changed[trim['column'] + 1] = prefix + trim['marker'] + ' New implementation observation '
                    self.assertEqual(subject.project(raw, [selector]),
                                     subject.project(text.replace(line, '|'.join(changed), 1).encode(), [selector]))

    def test_current_emission_and_receiving_refuse_drift_but_history_remains_checkable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            documents = root / 'documents'
            for source in self.manifest['sources']:
                target = documents / source['path']; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((PROJECT / canonical.deliverable_path(PROJECT, source['path'])).read_bytes())
            for name in self.manifest['terms_adoption']['artifacts']:
                target = documents / name; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((PROJECT / name).read_bytes())
            support = canonical.CanonicalSupport(documentary_root=documents)
            records, selected = fixtures.selection_for(support)
            current = root / 'current'; current.mkdir()
            path = fixtures.write_bundle(current, support, records, copy.deepcopy(selected))
            report = support.check(path, canonical.sha(path.read_bytes()))
            self.assertEqual(report['source_condition']['method'], 'selected-documentary-source-condition/v3-terms')
            self.assertFalse(report['producer_use_verified'])
            historical = root / 'historical'; historical.mkdir()
            selected['binding_purpose'] = 'historical_correspondence'
            history = fixtures.write_bundle(historical, support, records, selected)
            source = next(s for s in self.manifest['sources'] if s['path'].endswith('/EXAMINATION_PROTOCOL.md'))
            changed = documents / source['path']; raw = changed.read_bytes()
            heading = source['selectors'][0]['heading'].encode()
            changed.write_bytes(raw.replace(heading, heading + b'\nCHANGED REQUIRED MEANING', 1))
            with self.assertRaisesRegex(ValueError, 'documentary meaning changed'):
                support.binding('result', fixtures.fixtures.encoded(records['before']), 'current_producer_declaration')
            with self.assertRaisesRegex(ValueError, 'documentary meaning changed'):
                support.check(path, canonical.sha(path.read_bytes()))
            old = support.check(history, canonical.sha(history.read_bytes()))
            self.assertTrue(old['canonical_consistency_passed'])
            self.assertEqual(old['source_condition']['method'], 'original-frozen-source/v1')
            self.assertFalse(old['producer_use_verified'])

    def test_governing_dependencies_refuse_meaning_changes_outside_case_rows(self):
        dependencies = [
            ('EXAMINATION_PROTOCOL.md', 'DC-R5'),
            ('WORKSPACE_AND_REGISTRATION.md', '- **SP-3'),
            ('WORKFLOW_DECLARATION.md', '- **C-3**'),
            ('WORKSPACE_AND_REGISTRATION.md', '- **RC-2'),
            ('RECORD_SEMANTICS.md', '### 13.6a Native workflow supply receiving'),
            ('APP_ACT_CONTROL.md', '### 6.2 Selected P-2/Rust allocation'),
            ('NATIVE_INTERACTION_RECEIVING.md', '### 4.1 Kinds at'),
        ]
        for name, needle in dependencies:
            source = next(s for s in self.manifest['sources'] if s['path'].endswith('/' + name))
            raw = (PROJECT / canonical.deliverable_path(PROJECT, source['path'])).read_bytes()
            text = raw.decode()
            line = next(line for line in text.splitlines(keepends=True) if needle in line)
            altered = (line + 'CHANGED GOVERNING REQUIREMENT\n' if line.startswith('#')
                       else line.rstrip('\r\n') + ' CHANGED GOVERNING REQUIREMENT\n')
            changed = text.replace(line, altered, 1).encode()
            with self.subTest(file=name, governing_clause=needle):
                self.assertNotEqual(subject.project(raw, source['selectors']), subject.project(changed, source['selectors']))
