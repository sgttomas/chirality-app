"""Prepared J1 Stage A controller v5. Importing this module performs no OS/UI work.

One exact development App, retained main, related picker/confirmation phases,
and prebound normal AppKit termination. No CLI/native run is selected by this PR.
"""
from dataclasses import dataclass, field
from pathlib import Path
import ctypes as C
import hashlib
import json
import os
import time
from copy import deepcopy


class Refusal(RuntimeError):
    pass


class NotReady(Refusal):
    def __init__(self, message, category=None):
        super().__init__(message)
        self.category = category


def require(ok, why):
    if not ok:
        raise Refusal(why)


def cleanup_receipt(record, kind, value, errors):
    """Evidence failure never suppresses an identity-validated cleanup request."""
    try:
        record(kind, deepcopy(value))
    except BaseException as error:
        errors.append({'record': kind, 'error': repr(error)})


def setup_effects(subject, locations):
    """Full eaf5d057 DesktopSetup::preview_statement for new settings only."""
    checked_locations(locations, subject)
    return (
        f"Create NEW App-owned settings folder: {locations['Settings folder']}\n"
        "with an empty config.toml, an empty AGENTS.md and an empty skills folder.\n"
        f"Create NEW App-owned account directory: {locations['Sign-in folder']}\n"
        "Link its config.toml, AGENTS.md and skills to those new settings.\n"
        "Read, import or change no other Codex settings, home or credential.\n"
        f"Project for next launch: {subject.project}\n"
        f"Save a private pending request in {locations['Saved choices']}.\n"
        "Codex: the copy included with this App (bundled-owner-use-development).\n"
        "The current workspace, homes, account/model choices, records and prepared messages stay unchanged. "
        "No automatic quit/restart/login/conversation."
    )


def checked_question(view, subject, locations):
    title, separator, body = view.text.partition('\n')
    require(separator and title in ('Desktop setup — next launch only', 'Desktop setup')
            and body == setup_effects(subject, locations),
            'native full effects differ from reviewed project/destinations; abbreviated questions unsupported')


def checked_packet(packet, reviewed):
    """Compare members to the reviewed receipt BEFORE opening their paths."""
    expected = {}
    for row in reviewed:
        manifest, name = row['manifest'], row['path']
        require(manifest in ('PACKET.sha256', 'case-manifest.sha256'), 'unreviewed manifest')
        require(name not in expected.setdefault(manifest, {}), 'duplicate reviewed member')
        expected[manifest][name] = row['sha256']
    require(set(expected) == {'PACKET.sha256', 'case-manifest.sha256'}
            and all(expected.values()), 'reviewed packet member sets unavailable')
    for manifest in ('PACKET.sha256', 'case-manifest.sha256'):
        actual = {}
        for line in (packet / manifest).read_text().splitlines():
            digest, name = line.split(None, 1)
            name = name.strip().lstrip('*')
            require(name not in actual, 'duplicate packet member')
            actual[name] = digest
        require(actual == expected[manifest], 'packet manifest differs from reviewed receipt')
        for name, digest in actual.items():
            path = packet / name
            require(path.resolve().is_relative_to(packet.resolve())
                    and hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                    'reviewed packet/project changed')


@dataclass(frozen=True)
class Subject:
    source: str
    bundle: str
    identifier: str
    executable: str
    executable_sha256: str
    project: str
    app_data: str
    main_title: str = 'Chirality'


@dataclass
class Control:
    ref: object
    role: str
    label: str
    enabled: bool
    value: object = None
    writable: bool = False


@dataclass
class View:
    main: object
    root: object
    controls: list = field(default_factory=list)
    text: str = ''
    webarea: bool = False
    locations: dict = field(default_factory=dict)

    def one(self, label, roles=('AXButton',), enabled=True, prefix=False):
        found = [c for c in self.controls if c.role in roles
                 and (c.label.startswith(label) if prefix else c.label == label)
                 and (not enabled or c.enabled is True)]
        require(len(found) == 1, 'unique phase control unavailable: ' + label)
        return found[0]


def phase_root(ax, app, original, phase):
    """Original main remains fixed. Only direct/linked sheets are admitted.

    ax is the actual owned-AX adapter below; tests replace OS effects only.
    File lists, Recent Items and other applications are never queried here.
    """
    require(ax.role(original) == 'AXWindow', 'retained main role unavailable')
    windows = ax.refs(app, 'AXWindows', optional=False)
    require(len(windows) <= 4, 'App window expansion')
    direct = ax.refs(original, 'AXSheets') + ax.refs(original, 'AXChildren')
    candidates = []
    for ref in direct + windows:
        if ax.same(ref, app) or ax.same(ref, original):
            continue
        role = ax.role(ref)  # role() checks original PID before reading content
        if role not in ('AXWindow', 'AXSheet', 'AXDialog'):
            continue
        parent = ax.ref(ref, 'AXParent')
        linked = any(ax.same(ref, x) for x in ax.refs(original, 'AXSheets'))
        related = linked or (parent is not None and ax.same(parent, original))
        if not related:
            # A nested Go-to-folder sheet is acceptable only through the one
            # already related picker, never through the application by itself.
            for outer in ax.refs(original, 'AXSheets'):
                if parent is not None and ax.same(parent, outer):
                    related = True
        require(related, 'unexpected/unrelated App window; no substitution')
        require(role in ('AXSheet', 'AXDialog') or ax.value(ref, 'AXModal') is True,
                'extra App window is not a proven modal/picker')
        if not any(ax.same(ref, old) for old in candidates):
            candidates.append(ref)
    if phase in ('main', 'preview', 'saved'):
        require(not candidates, 'unexpected panel in main phase')
        return original
    require(phase in ('picker', 'confirmation'), 'unknown UI phase')
    # If two related panels exist, only a unique nested sheet can be the active
    # path-entry panel. This is a structural relation, not first-window choice.
    if phase == 'picker' and len(candidates) == 2:
        nested = [x for x in candidates if any(
            not ax.same(x, y) and ax.ref(x, 'AXParent') is not None
            and ax.same(ax.ref(x, 'AXParent'), y) for y in candidates)]
        require(len(nested) == 1, 'ambiguous nested picker')
        return nested[0]
    if not candidates:
        raise NotReady('related ' + phase + ' not exposed yet')
    require(len(candidates) == 1, 'unique related ' + phase + ' unavailable')
    return candidates[0]


def checked_locations(locations, subject):
    require(set(locations) == {'Settings folder', 'Sign-in folder', 'Saved choices'},
            'all three write destinations must be observed')
    base = Path(subject.app_data)
    values = list(locations.values())
    require(len(set(values)) == 3, 'write destinations overlap')
    for value in values:
        path = Path(value)
        require(path.is_absolute() and '..' not in path.parts and path.is_relative_to(base),
                'write destination outside exact development ID')
    require(Path(locations['Saved choices']) == base / 'desktop-startup/request.json',
            'saved choices path differs')
    return locations


def checked_pending(value, subject, locations):
    """The retained eaf5 RequestedInputs/Reference/NativePath shape, not display JSON."""
    require(set(value) == {'version', 'supplier', 'app_data', 'account', 'shared', 'project'}
            and value['version'] == 1 and value['supplier'] == 'bundled-owner-use-development',
            'pending setup schema/supplier differs')
    def path(native):
        require(set(native) == {'encoding', 'bytes'} and native['encoding'] == 'unix_bytes', 'native path encoding differs')
        raw = native['bytes']
        require(isinstance(raw, list) and 0 < len(raw) <= 16384
                and all(type(x) is int and 0 <= x <= 255 for x in raw) and 0 not in raw, 'native path bytes invalid')
        result = Path(os.fsdecode(bytes(raw)))
        require(result.is_absolute() and '..' not in result.parts, 'native path is not absolute/clean')
        return result
    def reference(row, expected):
        require(isinstance(row, dict) and set(row) == {'location', 'resolved', 'object'}, 'reference shape differs')
        require(path(row['location']) == Path(expected) and path(row['resolved']) == Path(expected), 'saved reference differs')
        obj = row['object']
        require(isinstance(obj, dict) and set(obj) == {'device', 'inode'}
                and all(type(v) is int and v >= 0 for v in obj.values()), 'saved reference identity absent')
    checked_locations(locations, subject)
    reference(value['app_data'], subject.app_data)
    reference(value['account'], locations['Sign-in folder'])
    reference(value['project'], subject.project)
    shared = value['shared']
    require(isinstance(shared, list) and len(shared) == 3, 'three settings references required')
    for row, name in zip(shared, ('config.toml', 'AGENTS.md', 'skills')):
        reference(row, str(Path(locations['Settings folder']) / name))
    return {'project': subject.project, 'locations': dict(locations), 'pending_only': True}


class StageA:
    TOTAL = 180
    WORK = 110
    STARTUP_SECONDS = 20
    STARTUP_READS = 10
    STARTUP_SPACING = 2
    READY_SECONDS = 5
    READY_READS = 3

    def __init__(self, subject, io, clock=time.monotonic, sleep=time.sleep, record=lambda *a: None):
        self.subject, self.io, self.clock, self.sleep, self.record = subject, io, clock, sleep, record
        self.used = False
        self.identity = None
        self.main = None
        self.cleanup_attempted = False
        self.acts = []

    def work(self):
        require(self.clock() < self.work_end, 'setup cutoff; begin prepared cleanup')
        self.io.check(self.identity)
        require(not self.io.supplier_started(), 'unexpected supplier start; stop setup')

    def observe(self, phase):
        end = min(self.work_end, self.clock() + 2)
        last = None
        for index in range(3):
            self.work()
            try:
                view = self.io.observe(self.main, phase, end)
                self.work()
                require(self.io.same(view.main, self.main), 'original main changed')
                require(self.clock() < end, 'phase observation returned late')
                self.record('phase-observation', {'phase': phase, 'at': self.clock(),
                                                 'webarea': view.webarea, 'control_count': len(view.controls)})
                return view
            except NotReady as error:
                last = str(error)
                if index < 2 and self.clock() < end:
                    self.sleep(min(.2, max(0, end - self.clock())))
        raise Refusal('phase not ready: ' + phase + '/' + str(last))

    def press(self, view, control, purpose):
        self.work()
        # Re-observe phase and resolve the same target immediately before input.
        fresh = self.io.revalidate(view, control, self.work_end)
        self.work()
        require(self.io.same(fresh.ref, control.ref) and fresh.enabled, 'stale/disabled phase target')
        self.record('press-intent', {'purpose': purpose, 'at': self.clock(), 'actor': 'agent'})
        self.acts.append(purpose)  # dispatch may be unknown; never retry it
        rc, error = None, None
        try:
            rc = self.io.press(fresh, self.work_end)
        except BaseException as exc:
            error = repr(exc)
            raise
        finally:
            self.record('press-result', {'purpose': purpose, 'rc': rc, 'error': error, 'at': self.clock()})
        require(rc == 0, 'unknown/refused dispatch; no repeat: ' + purpose)
        self.work()

    def startup(self):
        require(self.main is None, 'initial main already captured')
        started = self.clock()
        end = min(self.work_end, started + self.STARTUP_SECONDS)
        waiting = {'empty', 'self_only', 'cannot_complete', 'no_value'}
        for index in range(self.STARTUP_READS):
            self.work()
            if self.clock() >= end:
                break
            main, problem = None, None
            try:
                main = self.io.original_main(self.subject, end)
                self.io.check(self.identity)
            except BaseException as error:
                problem = error
            facts = dict(self.io.startup_facts())
            require(set(facts) == {'root_count', 'self_reference_count', 'match_count',
                                   'transient_return_category'}, 'unsafe startup fact schema')
            require(all(value is None or type(value) is int and 0 <= value <= 12
                        for key, value in facts.items() if key != 'transient_return_category'),
                    'startup count unavailable/invalid')
            require(facts['transient_return_category'] in waiting | {'ready', 'refused'},
                    'unclassified startup category')
            if problem is not None and not isinstance(problem, NotReady):
                facts['transient_return_category'] = 'refused'
            self.record('startup-window-read', {'pid': self.identity['pid'], 'observation': index + 1,
                                                'elapsed': self.clock() - started, **facts})
            if problem is not None:
                if not isinstance(problem, NotReady):
                    raise problem
                require(facts['transient_return_category'] in waiting,
                        'initial main refusal is not a waitable state')
            if self.clock() >= end:
                break  # a late observation never promotes readiness
            self.work()
            if main is not None:
                require(facts['transient_return_category'] == 'ready'
                        and facts['root_count'] == facts['match_count'] == 1
                        and facts['self_reference_count'] == 0, 'initial main binding not proven')
                self.main = main  # exactly one capture; content never reselects it
                return
            if index < self.STARTUP_READS - 1:
                self.sleep(min(self.STARTUP_SPACING, max(0, end - self.clock())))
        raise Refusal('bounded startup main readiness unavailable')

    def ready(self):
        require(self.main is not None, 'content readiness requires captured original main')
        end = min(self.work_end, self.clock() + self.READY_SECONDS)
        last = None
        for index in range(self.READY_READS):
            self.work()
            if self.clock() >= end:
                break
            try:
                view = self.io.observe(self.main, 'main', end)
                self.io.check(self.identity)
                require(self.io.same(view.main, self.main), 'main replaced during readiness')
                self.record('content-read', {'read': index + 1, 'at': self.clock(),
                                            'webarea': view.webarea, 'controls': len(view.controls)})
                if self.clock() >= end:
                    break
                if view.webarea:
                    view.one('Choose project folder…')
                    view.one('Start with new settings', ('AXRadioButton',), prefix=True)
                    view.one('Review setup', enabled=False)  # expected disabled before project
                    return view
            except NotReady as error:
                last = str(error)
            if index < self.READY_READS - 1:
                self.sleep(min(1.2, max(0, end - self.clock())))
        raise Refusal('bounded content readiness unavailable: ' + str(last))

    def project(self, view):
        self.press(view, view.one('Choose project folder…'), 'open project picker')
        picker = self.observe('picker')
        # These are conditional routes, not claims that NSOpenPanel publishes
        # them. The only discovery is this related panel's safe control subtree.
        entries = [c for c in picker.controls if c.role in ('AXTextField', 'AXComboBox')
                   and c.label in ('Go to the folder:', 'Go to folder:') and c.enabled and c.writable]
        if not entries:
            goto = [c for c in picker.controls if c.role == 'AXButton'
                    and c.label in ('Go to Folder…', 'Go to folder…') and c.enabled]
            require(len(goto) == 1, 'NATIVE_PATH_ENTRY_UNAVAILABLE: no observed supported path field or Go-to action')
            self.press(picker, goto[0], 'open observed Go-to-folder control')
            picker = self.observe('picker')
            entries = [c for c in picker.controls if c.role in ('AXTextField', 'AXComboBox')
                       and c.label in ('Go to the folder:', 'Go to folder:') and c.enabled and c.writable]
        require(len(entries) == 1, 'NATIVE_PATH_ENTRY_UNAVAILABLE: unique writable native path field absent')
        field = self.io.revalidate(picker, entries[0], self.work_end)
        self.work()
        require(field.writable and self.io.same(field.ref, entries[0].ref), 'path field changed')
        self.record('path-entry-intent', {'path': self.subject.project, 'actor': 'agent'})
        self.acts.append('native exact-project path entry')
        rc, error = None, None
        try:
            rc = self.io.enter_path(field, self.subject.project, self.work_end)
        except BaseException as exc:
            error = repr(exc)
            raise
        finally:
            self.record('path-entry-result', {'rc': rc, 'error': error, 'at': self.clock()})
        require(rc == 0 and self.io.read_value(field) == self.subject.project, 'native path entry/readback failed')
        picker = self.observe('picker')
        self.press(picker, picker.one('Go'), 'native Go to exact project')
        picker = self.observe('picker')
        require(self.subject.project in picker.text.splitlines(), 'picker does not expose selected exact directory')
        self.press(picker, picker.one('Open'), 'native Open exact project')
        view = self.observe('main')
        require(self.subject.project in view.text.splitlines(), 'exact project selection not shown by App')
        return view

    def setup(self):
        self.startup()
        view = self.project(self.ready())
        radio = view.one('Start with new settings', ('AXRadioButton',), prefix=True)
        if radio.value not in (True, 1, 1.0):
            self.press(view, radio, 'select new App-owned settings')
            view = self.observe('main')
        self.press(view, view.one('Review setup'), 'review setup')
        view = self.observe('preview')
        require('What setup will do' in view.text, 'write preview unavailable')
        disclosure = view.one('Exact locations', ('AXDisclosureTriangle', 'AXButton'))
        if disclosure.value not in (True, 1, 1.0):
            self.press(view, disclosure, 'read exact write locations')
            view = self.observe('preview')
        checked_locations(view.locations, self.subject)
        reviewed_locations = dict(view.locations)
        self.record('verified-write-locations', {'locations': view.locations, 'project': self.subject.project})
        self.press(view, view.one('Create settings and save for next launch…'), 'request native confirmation')
        question = self.observe('confirmation')
        checked_question(question, self.subject, reviewed_locations)
        names = {c.label for c in question.controls if c.role == 'AXButton' and c.enabled}
        require(names == {'Leave setup unchanged', 'Create settings and save for next launch', 'Cancel'},
                'native confirmation button set differs')
        self.record('native-confirmation', {'text': question.text, 'actor': 'agent development check'})
        self.press(question, question.one('Create settings and save for next launch'), 'native affirmative setup')
        view = self.observe('saved')
        require("You're set up" in view.text, 'saved UI not observed')
        self.record('saved-state', self.io.verify_saved(self.subject, reviewed_locations))
        return True

    def run(self):
        require(not self.used, 'one attempt only')
        self.used = True
        start = self.clock()
        self.started_at = start
        self.end, self.work_end = start + self.TOTAL, start + self.WORK
        result = {'actor': 'agent', 'source': self.subject.source, 'setup_saved': False,
                  'J1_complete': False, 'qualification': False, 'launches': 0}
        evidence_errors = []
        try:
            self.io.admit(self.subject)  # cleanup capability is prepared here too
            require(self.clock() < self.work_end, 'admission consumed setup budget')
            self.identity = self.io.launch_once(self.subject)
            result['launches'] = 1
            self.io.bind_cleanup(self.identity, self.subject)  # before any AX setup operation
            result['setup_saved'] = self.setup()
        except BaseException as error:
            result['setup_error'] = repr(error)
        finally:
            # A launch can establish identity then raise while writing its receipt.
            if self.identity is None:
                self.identity = getattr(self.io, 'identity', None)
            if self.identity is not None:
                result['launches'] = 1
                self.cleanup_attempted = True
                result['cleanup_started'] = self.clock() - start
                result['cleanup_within_reserved_interval'] = self.clock() <= self.end - 60
                cleanup_receipt(self.record, 'cleanup-intent',
                                {'at': self.clock(), 'original': self.identity,
                                 'mechanism': 'normal NSRunningApplication terminate',
                                 'no_parent_roundtrip': True}, evidence_errors)
                try:
                    # Does not use main/menu/title/picker or ask parent for input.
                    self.io.check(self.identity)
                    result['terminate_BOOL'] = self.io.normal_terminate(self.identity, self.subject)
                except BaseException as error:
                    result['cleanup_error'] = repr(error)
                try:
                    while self.clock() < self.end and not self.io.absent(self.identity):
                        self.sleep(min(.2, max(0, self.end - self.clock())))
                    result['original_absent'] = self.io.absent(self.identity)
                except BaseException as error:
                    result['original_absent'] = False
                    result['absence_error'] = repr(error)
            else:
                result['original_absent'] = not self.io.launch_unknown()
            result.update(elapsed=self.clock() - start, overrun=max(0, self.clock() - self.end),
                          actions=list(self.acts), slot_must_remain_held=not result['original_absent'],
                          launch_outcome_unknown=self.identity is None and self.io.launch_unknown())
            evidence_errors.extend(getattr(self.io, 'evidence_errors', []))
            result['evidence_errors'] = evidence_errors
            result['flow_complete'] = (result['setup_saved'] and result['original_absent']
                                       and result.get('terminate_BOOL') is True and result['overrun'] == 0
                                       and not result.get('setup_error') and not result.get('cleanup_error')
                                       and not evidence_errors)
            cleanup_receipt(self.record, 'result', result, evidence_errors)
            if evidence_errors:
                result['flow_complete'] = False
        return result


class NativeAX:
    """Concrete App-only AX access. Constructed only by a future selected runner.

    The runner owns launch admission, original identity and cleanup. This class
    takes that binding, never discovers another app or activates a window.
    """
    EXCLUDED = {'AXTable', 'AXOutline', 'AXBrowser', 'AXList', 'AXMenu', 'AXMenuBar', 'AXPopUpButton'}

    def __init__(self, backend, pid, check, clock=time.monotonic, project=None):
        self.b, self.pid, self.check, self.clock = backend, pid, check, clock
        self.project = project
        self.app = backend.app(pid)
        self.main = None
        self.last_phase = None
        self.last_root = None
        self.end = None

    def same(self, a, b):
        return self.b.equal(a, b)

    def value(self, ref, name):
        # Every property checks remote owner; full original birth/path/hash is
        # sampled before/after the bounded phase and again before input. Do not
        # hash a debug executable hundreds of times while decoding one tree.
        rc, owner = self.b.owner(ref)
        require(rc == 0 and owner == self.pid, 'AX reference is not original-App owned')
        row, refs = self.b.attribute(ref, name)
        if row['return_code'] in (-25204, -25212):
            raise NotReady('transient AX value: ' + name + '/' + str(row['return_code']),
                           category='cannot_complete' if row['return_code'] == -25204 else 'no_value')
        if row['return_code'] == -25205:
            return None
        require(row['return_code'] == 0, 'AX read refused: ' + name + '/' + str(row['return_code']))
        if row['type']['name'] == 'AXUIElement':
            require(len(refs) == 1, 'invalid scalar AX reference')
            return refs[0]
        if row['type']['name'] == 'CFArray':
            return refs
        return row['value']

    def role(self, ref):
        return self.value(ref, 'AXRole')

    def optional_value(self, ref, name):
        """NoValue is absence for nullable content metadata, not readiness."""
        require(name in ('AXTitle', 'AXDescription', 'AXValue', 'AXChildren'),
                'structural/source attributes are not optional content metadata')
        try:
            return self.value(ref, name)
        except NotReady as error:
            if error.category == 'no_value':
                return None
            raise

    def refs(self, ref, name, optional=True):
        try:
            value = self.value(ref, name)
        except NotReady as error:
            if optional and error.category == 'no_value':
                return []
            raise
        if value is None and optional:
            return []
        require(isinstance(value, list) and len(value) <= 12, 'bounded AX reference array unavailable: ' + name)
        return value

    def ref(self, ref, name):
        value = self.value(ref, name)
        require(value is None or not isinstance(value, list), 'expected scalar AX reference: ' + name)
        return value

    def initial_main(self, title):
        self.initial_facts = {'root_count': None, 'self_reference_count': None,
                              'match_count': None, 'transient_return_category': 'refused'}
        try:
            self.check()
            roots = self.refs(self.app, 'AXWindows', optional=False)
            self.initial_facts['root_count'] = len(roots)
            self_count = sum(self.same(ref, self.app) for ref in roots)
            self.initial_facts['self_reference_count'] = self_count
            if not roots or self_count == len(roots):
                category = 'empty' if not roots else 'self_only'
                self.initial_facts.update(match_count=0, transient_return_category=category)
                raise NotReady('initial main not exposed', category=category)
            require(len(roots) == 1, 'unexpected extra initial App window')
            main = roots[0]
            require(self.role(main) == 'AXWindow', 'initial main role differs')
            matches = int(self.value(main, 'AXTitle') == title)
            self.initial_facts['match_count'] = matches
            require(matches == 1, 'actual initial main title differs')
            require(self.main is None or self.same(main, self.main), 'captured main cannot be replaced')
            self.check()
            self.main = main
            self.initial_facts['transient_return_category'] = 'ready'
            return self.main
        except NotReady as error:
            if error.category in ('cannot_complete', 'no_value'):
                self.initial_facts['transient_return_category'] = error.category
            self.check()  # bind even a partial/not-ready sample to the original
            raise

    def _controls(self, root, picker, deadline):
        if picker:
            return self._picker_controls(root, deadline)
        stack, seen, controls, text, webarea = [(root, 0)], [], [], [], False
        while stack:
            require(self.clock() < deadline and len(seen) < 500, 'phase AX walk budget')
            ref, depth = stack.pop()
            if any(self.same(ref, old) for old in seen):
                continue
            seen.append(ref)
            require(depth <= 18, 'phase AX depth')
            role = self.role(ref)
            if role in self.EXCLUDED - {'AXList'}:
                continue  # other non-content collections stay excluded
            # This is the App-owned main/preview/confirmation content branch.
            # Its HTML list contains the first-use controls. Native picker
            # lists remain excluded by the separate _picker_controls path.
            webarea |= role == 'AXWebArea'
            if role in ('AXButton', 'AXRadioButton', 'AXDisclosureTriangle', 'AXTextField', 'AXComboBox'):
                title = self.optional_value(ref, 'AXTitle') or self.optional_value(ref, 'AXDescription') or ''
                value = self.optional_value(ref, 'AXValue')
                controls.append(Control(ref, role, title, self.value(ref, 'AXEnabled') is True, value, False))
            elif role in ('AXStaticText', 'AXHeading'):
                value = self.optional_value(ref, 'AXValue') or self.optional_value(ref, 'AXTitle') or ''
                if isinstance(value, str):
                    text.append(value)
            children = self.optional_value(ref, 'AXChildren')
            if children is not None:
                require(isinstance(children, list) and len(children) <= 80, 'phase child bound')
                stack.extend((child, depth + 1) for child in reversed(children))
        return controls, '\n'.join(text), webarea

    def _picker_controls(self, root, deadline):
        # Conditional supported schema: direct panel controls only. No generic
        # group/scroll-area discovery and no static-text/file/history values.
        # An unknown structure refuses before any descendant content is read.
        require(self.role(root) in ('AXSheet', 'AXDialog', 'AXWindow'), 'picker root role differs')
        children = self.refs(root, 'AXChildren', optional=False)
        typed = [(ref, self.role(ref)) for ref in children]
        admitted = {'AXButton', 'AXTextField', 'AXComboBox', 'AXPathControl', 'AXStaticText'}
        require(all(role in admitted or role in self.EXCLUDED for _, role in typed),
                'NATIVE_PATH_ENTRY_UNAVAILABLE: unclassified picker structure')
        controls, paths = [], []
        for ref, role in typed:
            require(self.clock() < deadline, 'picker control budget')
            if role in self.EXCLUDED or role == 'AXStaticText':
                continue
            if role == 'AXPathControl':
                if getattr(self, 'path_entry_verified', False):
                    value = self.value(ref, 'AXValue')
                    require(isinstance(value, str) and value == self.project,
                            'NATIVE_PATH_ENTRY_UNAVAILABLE: exact current directory not exposed')
                    paths.append(value)
                continue  # never inspect breadcrumb/history children
            title = self.optional_value(ref, 'AXTitle') or self.optional_value(ref, 'AXDescription') or ''
            allowed = (('Go', 'Open', 'Cancel', 'Go to Folder…', 'Go to folder…') if role == 'AXButton'
                       else ('Go to the folder:', 'Go to folder:'))
            if title not in allowed:
                continue  # control metadata only; never its value/children
            writable = role in ('AXTextField', 'AXComboBox') and self._settable(ref)
            controls.append(Control(ref, role, title, self.value(ref, 'AXEnabled') is True, None, writable))
        return controls, '\n'.join(paths), False

    def observe(self, main, phase, deadline):
        self.check()
        require(self.main is not None and self.same(main, self.main), 'original main binding missing')
        root = phase_root(self, self.app, main, phase)
        if phase == 'confirmation':
            title = self.value(root, 'AXTitle') or ''
            require(title in ('Desktop setup — next launch only', 'Desktop setup'), 'native question title differs')
        controls, text, webarea = self._controls(root, phase == 'picker', deadline)
        if phase == 'confirmation':
            text = (self.value(root, 'AXTitle') or '') + '\n' + text
        # Locations are dt/dd text from the normal Exact locations disclosure.
        locations = {}
        if phase == 'preview':
            lines = text.splitlines()
            for name in ('Settings folder', 'Sign-in folder', 'Saved choices'):
                positions = [i for i, line in enumerate(lines) if line == name]
                if len(positions) == 1 and positions[0] + 1 < len(lines):
                    locations[name] = lines[positions[0] + 1]
        self.check()
        require(self.clock() < deadline, 'phase observation returned late')
        self.last_phase, self.last_root, self.end = phase, root, deadline
        self.last_view = View(main, root, controls, text, webarea, locations)
        return self.last_view

    def _settable(self, ref):
        fn = self.b.a.AXUIElementIsAttributeSettable
        fn.restype, fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.POINTER(C.c_bool)]
        value = C.c_bool()
        rc = fn(ref, self.b.string('AXValue'), C.byref(value))
        return rc == 0 and bool(value.value)

    def revalidate(self, view, control, deadline):
        phase = self.last_phase
        current = self.observe(view.main, phase, deadline)
        require(self.same(current.root, view.root), 'phase root changed before action')
        if phase in ('preview', 'confirmation'):
            require(current.text == view.text and current.locations == view.locations,
                    'reviewed phase content changed before action')
        found = [c for c in current.controls if self.same(c.ref, control.ref) and c.role == control.role
                 and c.label == control.label and c.enabled]
        require(len(found) == 1, 'phase target changed')
        return found[0]

    def _bound_target(self, control, deadline):
        self.check()
        require(self.clock() < deadline, 'phase cutoff before input')
        current = phase_root(self, self.app, self.main, self.last_phase)
        require(self.same(current, self.last_root), 'phase changed immediately before input')
        require(self.role(control.ref) == control.role and self.value(control.ref, 'AXEnabled') is True,
                'target role/enabled changed')
        label = self.optional_value(control.ref, 'AXTitle') or self.optional_value(control.ref, 'AXDescription') or ''
        require(label == control.label, 'target label changed')
        parent, seen = control.ref, []
        for _ in range(19):
            if self.same(parent, current):
                return
            require(not any(self.same(parent, old) for old in seen), 'target parent cycle')
            seen.append(parent)
            parent = self.ref(parent, 'AXParent')
            require(parent is not None, 'target relationship unavailable')
        raise Refusal('target outside phase subtree')

    def press(self, control, deadline):
        self._bound_target(control, deadline)
        fn = self.b.a.AXUIElementCopyActionNames
        fn.restype, fn.argtypes = C.c_int, [C.c_void_p, C.POINTER(C.c_void_p)]
        value = C.c_void_p()
        rc = fn(control.ref, C.byref(value))
        if value.value:
            self.b.held.append(value.value)
        require(rc == 0 and value.value, 'target action list unavailable')
        require('AXPress' in [self.b.scalar(x) for x in self.b.array(value.value, 12)], 'AXPress unsupported')
        self.check()
        require(self.clock() < deadline, 'phase cutoff before press')
        if self.last_phase == 'confirmation':
            previous = self.last_view
            current = self.observe(self.main, 'confirmation', deadline)
            require(self.same(previous.root, current.root) and previous.text == current.text,
                    'native statement changed immediately before affirmative')
            require(any(self.same(c.ref, control.ref) and c.label == control.label and c.enabled
                        for c in current.controls), 'native affirmative changed')
        fn = self.b.a.AXUIElementPerformAction
        fn.restype, fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p]
        return fn(control.ref, self.b.string('AXPress'))

    def enter_path(self, control, path, deadline):
        self._bound_target(control, deadline)
        require(self.clock() < deadline and control.writable and self._settable(control.ref), 'path input unavailable')
        require(control.label in ('Go to the folder:', 'Go to folder:'), 'unidentified native path input')
        self.check()
        require(self.clock() < deadline, 'phase cutoff before path write')
        fn = self.b.a.AXUIElementSetAttributeValue
        fn.restype, fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.c_void_p]
        return fn(control.ref, self.b.string('AXValue'), self.b.string(path))

    def read_value(self, control):
        value = self.value(control.ref, 'AXValue')
        if control.label in ('Go to the folder:', 'Go to folder:') and value == self.project:
            self.path_entry_verified = True
        return value


def normal_terminate(backend, identity, subject, record, appkit, check, evidence_errors=None):
    """Concrete one-request cleanup. appkit is the narrow AppKit adapter below.

    No AX/main/title dependency. Identity and AppKit correspondence precede the
    single selector; an unknown return is consumed, never retried.
    """
    evidence_errors = [] if evidence_errors is None else evidence_errors
    check(identity)
    with appkit.target(identity['pid']) as target:
        actual = appkit.describe(target)
        require(actual == {'pid': identity['pid'], 'bundle_identifier': subject.identifier,
                           'executable': subject.executable}, 'AppKit target correspondence differs')
        check(identity)
        cleanup_receipt(record, 'normal-terminate-intent',
                        {'identity': identity, 'AppKit': actual, 'actor': 'agent'}, evidence_errors)
        rc, error = None, None
        try:
            check(identity)
            rc = appkit.terminate(target)
            return rc
        except BaseException as exc:
            error = repr(exc)
            raise
        finally:
            cleanup_receipt(record, 'normal-terminate-result',
                            {'BOOL': rc, 'error': error, 'effect_proved': False}, evidence_errors)

class AppKit:
    """Exact-PID normal termination only; no activate/forceTerminate selector."""
    def __init__(self):
        self.framework = C.CDLL('/System/Library/Frameworks/AppKit.framework/AppKit')
        self.objc = C.CDLL('/usr/lib/libobjc.A.dylib')
        self.objc.objc_getClass.restype, self.objc.objc_getClass.argtypes = C.c_void_p, [C.c_char_p]
        self.objc.sel_registerName.restype, self.objc.sel_registerName.argtypes = C.c_void_p, [C.c_char_p]
        self.obj = C.CFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p)(('objc_msgSend', self.objc))
        self.objpid = C.CFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_int)(('objc_msgSend', self.objc))
        self.pidcall = C.CFUNCTYPE(C.c_int, C.c_void_p, C.c_void_p)(('objc_msgSend', self.objc))
        self.utf8 = C.CFUNCTYPE(C.c_char_p, C.c_void_p, C.c_void_p)(('objc_msgSend', self.objc))
        self.boolean = C.CFUNCTYPE(C.c_bool, C.c_void_p, C.c_void_p)(('objc_msgSend', self.objc))
        self.void = C.CFUNCTYPE(None, C.c_void_p, C.c_void_p)(('objc_msgSend', self.objc))

    def sel(self, value):
        return self.objc.sel_registerName(value)

    def target(self, pid):
        from contextlib import contextmanager
        @contextmanager
        def retained():
            pool = self.obj(self.objc.objc_getClass(b'NSAutoreleasePool'), self.sel(b'new'))
            require(pool, 'AppKit pool unavailable')
            try:
                target = self.objpid(self.objc.objc_getClass(b'NSRunningApplication'),
                                     self.sel(b'runningApplicationWithProcessIdentifier:'), pid)
                require(target, 'original AppKit target unavailable')
                yield target
            finally:
                self.void(pool, self.sel(b'drain'))
        return retained()

    def describe(self, target):
        bundle = self.obj(target, self.sel(b'bundleIdentifier'))
        url = self.obj(target, self.sel(b'executableURL'))
        path = self.obj(url, self.sel(b'path')) if url else None
        require(bundle and path, 'AppKit bundle/executable unavailable')
        return {'pid': self.pidcall(target, self.sel(b'processIdentifier')),
                'bundle_identifier': self.utf8(bundle, self.sel(b'UTF8String')).decode('utf-8'),
                'executable': self.utf8(path, self.sel(b'UTF8String')).decode('utf-8')}

    def terminate(self, target):
        return bool(self.boolean(target, self.sel(b'terminate')))

    def candidate_pids(self, identifier):
        # Only this development identifier. No process-name or all-app sweep.
        string = C.CFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_char_p)(('objc_msgSend', self.objc))
        arg = C.CFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)(('objc_msgSend', self.objc))
        count = C.CFUNCTYPE(C.c_ulong, C.c_void_p, C.c_void_p)(('objc_msgSend', self.objc))
        index = C.CFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_ulong)(('objc_msgSend', self.objc))
        pool = self.obj(self.objc.objc_getClass(b'NSAutoreleasePool'), self.sel(b'new'))
        require(pool, 'AppKit pool unavailable')
        try:
            text = string(self.objc.objc_getClass(b'NSString'), self.sel(b'stringWithUTF8String:'), identifier.encode())
            values = arg(self.objc.objc_getClass(b'NSRunningApplication'),
                         self.sel(b'runningApplicationsWithBundleIdentifier:'), text)
            n = count(values, self.sel(b'count'))
            require(n <= 4, 'development identifier process expansion')
            return [self.pidcall(index(values, self.sel(b'objectAtIndex:'), i), self.sel(b'processIdentifier')) for i in range(n)]
        finally:
            self.void(pool, self.sel(b'drain'))


class NativeSession:
    """Specific Stage A OS adapter, inert until explicitly called after review.

    Preflight input is the reviewed corrected receipt plus packet hashes. Native
    launch remains a later selected operation. No execution occurs on import.
    """
    def __init__(self, subject, preflight, record, clock=time.monotonic, sleep=time.sleep):
        self.subject, self.preflight, self.record = subject, preflight, record
        self.clock, self.sleep = clock, sleep
        self.identity, self.ax, self.backend, self.appkit = None, None, None, None
        self.pending_launch, self.launched, self.termination_used = False, False, False
        self.evidence_errors = []

    def admit(self, subject):
        import subprocess
        require(subject == self.subject and subject.source == self.preflight['source'], 'subject source differs')
        require(subject.bundle == self.preflight['bundle'] and subject.identifier == self.preflight['identifier']
                and subject.app_data == str(Path.home() / 'Library/Application Support' / subject.identifier)
                and subject.main_title == 'Chirality', 'bundle/development ID/data/window subject differs')
        require(subject.executable == self.preflight['executable']
                and subject.executable_sha256 == self.preflight['executable_sha256'], 'subject executable differs')
        require(hashlib.sha256(Path(subject.executable).read_bytes()).hexdigest() == subject.executable_sha256,
                'retained executable changed')
        require(Path(subject.project).resolve() == Path(self.preflight['packet']) / 'session/project', 'invented project differs')
        require(not os.path.lexists(subject.app_data), 'existing AppData/setup: preserve and stop before launch')
        state = [{'path': row['path'], 'present': os.path.lexists(row['path'])}
                 for row in self.preflight['development_state']]
        packet = Path(self.preflight['packet'])
        checked_packet(packet, self.preflight['manifest_checks'])
        parent = subprocess.check_output(['/bin/ps', '-p', str(os.getppid()), '-o', 'command='], text=True, timeout=2)
        require('/Users/ryan/dev/chirality-t3/tools/t3_slot_run.sh' in parent, 'ordinary slot parent unavailable')
        # Prepare both cleanup APIs before launching: a load/signature failure
        # cannot spend a launch and only then discover cleanup was unavailable.
        import types
        reader_path = Path(__file__).with_name('native_b_diagnostic.py')
        raw = reader_path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == 'fd37834b301f138963cdfe76f8bf3a146aea373b99ab2c994546ff73c939af19',
                'reviewed identity/AX reader bytes changed')
        diagnostic = types.ModuleType('j1_reviewed_native_reader'); diagnostic.__file__ = str(reader_path)
        exec(compile(raw, str(reader_path), 'exec'), diagnostic.__dict__)
        class Bounded(diagnostic.NativeBackend):
            def bounded_element(inner, element):
                require(inner.kind(element)['name'] == 'AXUIElement', 'invalid AX object')
                require(inner.a.AXUIElementSetMessagingTimeout(element, .2) == 0, 'AX timeout unavailable')
        self.backend, self.appkit = Bounded(), AppKit()
        self.bsd_type = diagnostic.Bsd
        trusted = self.backend.a.AXIsProcessTrusted
        trusted.restype, trusted.argtypes = C.c_bool, []
        require(trusted(), 'AX trust unavailable; no permission prompt')
        require(not self.appkit.candidate_pids(subject.identifier), 'development instance already running')
        switches = [row['name'] for row in self.preflight['route_environment_presence_only']]
        require(not any(k in os.environ for k in switches), 'shell route-switch present')
        result = subprocess.run(['/bin/launchctl', 'print', 'gui/' + str(os.getuid())], capture_output=True, text=True, timeout=3)
        require(result.returncode == 0, 'GUI environment membership unavailable')
        in_env, sections, present = False, 0, []
        for line in result.stdout.splitlines():
            text = line.strip()
            if text == 'environment = {':
                in_env, sections = True, sections + 1
            elif in_env and text == '}':
                in_env = False
            elif in_env and '=>' in text and text.split('=>', 1)[0].strip() in switches:
                present.append(text.split('=>', 1)[0].strip())
        require(sections and not present, 'GUI route-switch present or membership unknown')
        self.record('admitted', {'source': subject.source, 'project': subject.project,
                                 'cleanup': 'normal terminate preloaded', 'route_keys_present': present, 'state_presence_only': state})

    def launch_once(self, subject):
        import subprocess
        require(not self.launched and not self.pending_launch, 'one launch only')
        self.record('launch-intent', {'argv': ['/usr/bin/open', '-n', subject.bundle], 'source': subject.source})
        self.pending_launch = True  # only the actual dispatch boundary can be unknown
        result = subprocess.run(['/usr/bin/open', '-n', subject.bundle], capture_output=True, text=True, timeout=5)
        require(result.returncode == 0, 'open failed/unknown launch outcome')
        pids = []
        for _ in range(12):
            pids = self.appkit.candidate_pids(subject.identifier)
            if pids:
                break
            self.sleep(.1)
        require(len(pids) == 1, 'original launch identity unavailable/ambiguous')
        identity = self.backend.identity(pids[0])
        require(identity['executable'] == subject.executable and identity['uid'] == identity['ruid'] == os.getuid()
                and os.getpgid(identity['pid']) == identity['pid'], 'new original process differs')
        self.identity = dict(identity)  # keep the original separate from receipt callbacks
        self.launched, self.pending_launch = True, False
        self.record('launched', {'identity': dict(identity), 'source': subject.source})
        return dict(identity)

    def bind_cleanup(self, identity, subject):
        self.check(identity)
        with self.appkit.target(identity['pid']) as target:
            require(self.appkit.describe(target) == {'pid': identity['pid'], 'bundle_identifier': subject.identifier,
                                                    'executable': subject.executable}, 'initial cleanup correspondence differs')
        self.record('cleanup-bound', {'identity': dict(identity), 'mechanism': 'normal terminate', 'no_AX_dependency': True})

    def check(self, identity):
        require(identity is not None and self.identity == identity, 'original binding missing')
        require(self.backend.identity(identity['pid']) == identity
                and os.getpgid(identity['pid']) == identity['pid'], 'original birth/UID/path/PGID changed')
        require(hashlib.sha256(Path(self.subject.executable).read_bytes()).hexdigest() == self.subject.executable_sha256,
                'original executable changed')

    def supplier_started(self):
        import subprocess
        result = subprocess.run(['/usr/bin/pgrep', '-P', str(self.identity['pid'])], capture_output=True, text=True, timeout=2)
        require(result.returncode in (0, 1), 'App child observation unavailable')
        children = [int(x) for x in result.stdout.split()]
        require(len(children) <= 12, 'App child expansion')
        for child in children:
            path = self.backend.identity(child)['executable']
            if path.endswith('/codex') or '/codex/' in path:
                self.record('unexpected-supplier', {'pid': child, 'executable': path, 'standing': 'stop/review; no supplier settlement claim'})
                return True
        return False

    def original_main(self, subject, deadline):
        if self.ax is None:
            self.ax = NativeAX(self.backend, self.identity['pid'], lambda: self.check(self.identity), self.clock, project=subject.project)
        return self.ax.initial_main(subject.main_title)

    def startup_facts(self):
        return dict(getattr(self.ax, 'initial_facts', {
            'root_count': None, 'self_reference_count': None, 'match_count': None,
            'transient_return_category': 'refused'}))

    def same(self, left, right):
        return self.backend.equal(left, right)

    def observe(self, main, phase, deadline):
        return self.ax.observe(main, phase, deadline)

    def revalidate(self, view, control, deadline):
        return self.ax.revalidate(view, control, deadline)

    def press(self, control, deadline):
        return self.ax.press(control, deadline)

    def enter_path(self, control, path, deadline):
        require(path == self.subject.project, 'only exact invented project permitted')
        return self.ax.enter_path(control, path, deadline)

    def read_value(self, control):
        return self.ax.read_value(control)

    def verify_saved(self, subject, locations):
        path = Path(subject.app_data) / 'desktop-startup/request.json'
        require(path.is_file() and not path.is_symlink(), 'saved request unavailable')
        raw = path.read_bytes()
        require(0 < len(raw) <= 65536, 'saved request bound')
        value = json.loads(raw)
        # Decode the actual lossless Reference paths; no display-string search.
        checked = checked_pending(value, subject, locations)
        return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'checked': checked, 'pending': value}

    def normal_terminate(self, identity, subject):
        require(not self.termination_used, 'normal terminate already consumed')
        self.termination_used = True
        return normal_terminate(self.backend, identity, subject, self.record, self.appkit, self.check,
                                self.evidence_errors)

    def process_birth(self, pid):
        # Birth-only observation does not impose the original process's UID or
        # executable on a replacement. It never authorizes input to that PID.
        info = self.bsd_type()
        size = C.sizeof(info)
        require(size == 136 and self.backend.p.proc_pidinfo(pid, 3, 0, C.byref(info), size) == size
                and info.pid == pid, 'kernel birth observation unavailable')
        return (int(info.start_sec), int(info.start_usec))

    def absent(self, identity):
        import subprocess
        result = subprocess.run(['/bin/ps', '-p', str(identity['pid']), '-o', 'pid=,lstart=,comm='],
                                capture_output=True, text=True, timeout=2)
        if result.returncode == 1:
            return not result.stdout.strip() and not getattr(result, 'stderr', '').strip()
        if result.returncode != 0:
            return False
        try:
            expected = (identity['start_sec'], identity['start_usec'])
            return self.process_birth(identity['pid']) != expected
        except BaseException:
            return False  # unknown is held, never treated as original absence

    def launch_unknown(self):
        return self.pending_launch or self.identity is not None

    def hold_until_absent(self, result):
        # A future slot runner must call this after a held result, never return
        # its lock while this development App may still be live. No new action.
        if not result['slot_must_remain_held']:
            return
        try:
            self.record('held', {'identity': deepcopy(self.identity), 'no_more_input': True})
        except BaseException:
            pass  # evidence failure cannot release a possibly live development App
        if self.identity is None:
            # A launch outcome with no original birth cannot establish absence
            # from a transient empty bundle lookup. Retain/report, never rebind.
            while self.pending_launch:
                self.sleep(1)
        else:
            while True:
                try:
                    if self.absent(self.identity):
                        break
                except BaseException:
                    pass  # a failed observation is not process absence
                self.sleep(1)
        self.record('late-absence', {'identity': deepcopy(self.identity), 'at': self.clock(), 'not_a_deadline_release': True})


def run_prepared(subject, preflight, record, clock=time.monotonic, sleep=time.sleep):
    """Future reviewed slot entry. Never invoked by this offline preparation.

    Hold even after a recording/controller exception; no return while the App
    may be live. No extra cleanup action is sent in this finalizer. A late
    closure is a separate fact and never turns the initial failed run into pass.
    """
    entered = clock()
    io = NativeSession(subject, preflight, record, clock, sleep)
    controller = StageA(subject, io, clock, sleep, record)
    result = None
    try:
        result = controller.run()
    finally:
        if result is None:
            try:
                live = io.launch_unknown() if io.identity is None else not io.absent(io.identity)
            except BaseException:
                live = True
            held = {'slot_must_remain_held': live}
        else:
            held = result
        try:
            io.hold_until_absent(held)
            if io.identity is not None:
                require(io.absent(io.identity), 'slot entry cannot return without original absence')
                origin = getattr(controller, 'started_at', entered)
                end = getattr(controller, 'end', origin + 180)
                closure = {'original': deepcopy(io.identity), 'original_absent': True,
                           'final_elapsed': clock() - origin, 'final_overrun': max(0, clock() - end),
                           'exit_status': None, 'exit_status_limit': 'LaunchServices-owned; no wait/reap status',
                           'initial_held': held['slot_must_remain_held']}
                record('final-closure', deepcopy(closure))
                if result is not None:
                    result = dict(result, **closure, slot_must_remain_held=False)
        finally:
            if io.backend is not None:
                io.backend.close()
    return result


def private_journal(root):
    """Concrete one-run evidence callback; no existing record is overwritten."""
    import stat
    root = Path(root)
    info = root.lstat()
    require(root.is_absolute() and root.resolve() == root and stat.S_ISDIR(info.st_mode)
            and info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o700,
            'private evidence directory required')
    sequence = 0
    def record(kind, value):
        nonlocal sequence
        require(kind and all(ch.isalnum() or ch in '-_' for ch in kind), 'invalid evidence record name')
        sequence += 1
        path = root / (f'{sequence:03d}-' + kind + '.json')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2)
            stream.flush(); os.fsync(stream.fileno())
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    return record
