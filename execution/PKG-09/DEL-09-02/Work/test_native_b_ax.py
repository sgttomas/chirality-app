"""Pure mocked AX graph tests; no App, OS AX, supplier or temporary files."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('native_b_ax', Path(__file__).with_name('native_b_ax.py'))
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


class Ref:
    def __init__(self, key):
        self.key = key


class CF:
    @staticmethod
    def CFEqual(left, right):
        return left.key == right.key


class Base:
    def __init__(self):
        self.app = Ref('app')
        self.c = CF()
        self.pid = 42
        self.nodes = {'app': self.node('AXApplication', 'Invented App')}
        self.window_refs = []
        self.alive_calls = 0
        self.fail_after = None

    @staticmethod
    def node(role='AXGroup', title='', children=None, pid=42):
        return {'AXRole': role, 'AXTitle': title, 'AXChildren': children or [], 'pid': pid}

    def alive(self):
        self.alive_calls += 1
        if self.fail_after is not None and self.alive_calls > self.fail_after:
            raise RuntimeError('original reservation/deadline unavailable')

    def own(self, element):
        self.alive()
        if self.nodes[element.key]['pid'] != self.pid:
            raise RuntimeError('AX ownership differs')

    def attr(self, element, name):
        self.alive()
        return self.nodes[element.key].get(name)

    def windows(self):
        self.alive()
        return self.window_refs

    def press(self, _):
        raise AssertionError('tests must send no UI action')


class Readiness(unittest.TestCase):
    def setUp(self):
        self.ax = subject.wrap_ax(Base)()
        self.ax.nodes['main'] = Base.node('AXWindow', subject.MAIN_TITLE)

    def test_self_reference_never_becomes_main_and_delayed_window_is_observed(self):
        self.ax.window_refs = [Ref('app')]
        self.assertIsNone(self.ax.main_if_available())
        self.assertEqual(self.ax.window_observation()[0]['disposition'], 'application-self-reference')
        with self.assertRaises(subject.MainWindowUnavailable):
            self.ax.main()
        self.ax.window_refs.append(Ref('main'))
        self.assertEqual(self.ax.main_if_available().key, 'main')
        self.assertEqual(self.ax.main().key, 'main')

    def test_role_title_and_cf_identity_are_all_required(self):
        self.ax.nodes['dialog'] = Base.node('AXDialog', subject.MAIN_TITLE)
        self.ax.nodes['other'] = Base.node('AXWindow', 'Other title')
        self.ax.window_refs = [Ref('dialog'), Ref('other')]
        self.assertIsNone(self.ax.main_if_available())
        self.ax.window_refs = [Ref('main'), Ref('main')]
        self.assertEqual(len(self.ax.windows()), 1)
        self.assertEqual(self.ax.last_window_observation[-1]['disposition'], 'duplicate-reference')
        self.assertEqual(self.ax.main().key, 'main')
        self.assertIs(type(self.ax).press, Base.press)

    def test_ambiguous_or_foreign_window_refuses(self):
        self.ax.nodes['second'] = Base.node('AXWindow', subject.MAIN_TITLE)
        self.ax.window_refs = [Ref('main'), Ref('second')]
        with self.assertRaisesRegex(RuntimeError, 'ambiguous'):
            self.ax.main_if_available()
        self.ax.nodes['second']['pid'] = 99
        with self.assertRaisesRegex(RuntimeError, 'ownership differs'):
            self.ax.window_observation()

    def test_cycles_application_and_other_window_boundaries_are_pruned(self):
        self.ax.nodes.update({
            'group': Base.node(children=[Ref('main'), Ref('group'), Ref('app'), Ref('dialog'), Ref('other'), Ref('text')]),
            'dialog': Base.node('AXDialog', 'Separate dialog', [Ref('foreign-text')]),
            'other': Base.node('AXWindow', 'Other window', [Ref('foreign-text')]),
            'text': Base.node('AXStaticText', 'Actual selected-window content'),
            'foreign-text': Base.node('AXStaticText', 'Outside this window'),
        })
        self.ax.nodes['main']['AXChildren'] = [Ref('group')]
        self.ax.window_refs = [Ref('main'), Ref('dialog')]
        rows = self.ax.walk(self.ax.main())
        self.assertEqual([e.key for e, _, _ in rows], ['main', 'group', 'text'])
        self.assertEqual(self.ax.last_walk_observation['cycles_pruned'], 2)
        self.assertEqual(self.ax.last_walk_observation['application_boundaries_pruned'], 1)
        self.assertEqual(self.ax.last_walk_observation['window_boundaries_pruned'], 2)
        self.assertEqual(self.ax.walk(Ref('app')), [])

    def test_web_provenance_and_native_sheet_are_preserved(self):
        self.ax.nodes.update({'web': Base.node('AXWebArea', children=[Ref('button'), Ref('main')]),
                              'button': Base.node('AXButton', 'Web action'),
                              'sheet': Base.node('AXSheet', 'Native question')})
        self.ax.nodes['main']['AXChildren'] = [Ref('web'), Ref('sheet')]
        rows = self.ax.walk(Ref('main'))
        self.assertEqual([(e.key, web) for e, _, web in rows],
                         [('main', False), ('web', True), ('button', True), ('sheet', False)])
        # A shared object cannot become a native question through a second path.
        self.ax.nodes['main']['AXChildren'] = [Ref('button'), Ref('web')]
        with self.assertRaisesRegex(RuntimeError, 'native/Web boundary'):
            self.ax.walk(Ref('main'))

    def test_depth_node_and_reference_budgets_remain_bounded(self):
        for i in range(22):
            self.ax.nodes[str(i)] = Base.node(children=[Ref(str(i + 1))] if i < 21 else [])
        with self.assertRaisesRegex(RuntimeError, 'depth'):
            self.ax.walk(Ref('0'))
        self.ax.nodes['main']['AXChildren'] = [Ref('leaf-' + str(i)) for i in range(898)]
        self.ax.nodes.update({'leaf-' + str(i): Base.node() for i in range(899)})
        self.assertEqual(len(self.ax.walk(Ref('main'))), 899)
        self.ax.nodes['main']['AXChildren'].append(Ref('leaf-898'))
        with self.assertRaisesRegex(RuntimeError, 'AX expansion'):
            self.ax.walk(Ref('main'))
        self.ax.nodes['main']['AXChildren'] = [Ref('repeated-' + str(i)) for i in range(3)]
        self.ax.nodes.update({'repeated-' + str(i): Base.node(children=[Ref('leaf-0')] * 899) for i in range(3)})
        with self.assertRaisesRegex(RuntimeError, 'reference expansion'):
            self.ax.walk(Ref('main'))

    def test_liveness_and_foreign_descendant_checks_are_not_bypassed(self):
        self.ax.nodes['main']['AXChildren'] = [Ref('foreign')]
        self.ax.nodes['foreign'] = Base.node(pid=99)
        with self.assertRaisesRegex(RuntimeError, 'ownership differs'):
            self.ax.walk(Ref('main'))
        self.ax.nodes['main']['AXChildren'] = []
        self.ax.fail_after = self.ax.alive_calls + 2
        with self.assertRaisesRegex(RuntimeError, 'reservation/deadline'):
            self.ax.walk(Ref('main'))


if __name__ == '__main__':
    unittest.main()
