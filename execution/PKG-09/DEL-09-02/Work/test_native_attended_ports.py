import tempfile
from pathlib import Path
from types import SimpleNamespace as N
from unittest.mock import patch
import unittest
from native_attended_ports import NativePorts

class Tests(unittest.TestCase):
    def ports(self,run):
        value={};a=N(check_birth=lambda label,r:None,value=value)
        b=N(release_support=N(normal_exit=lambda x:x=={'code':1,'status':0},
              request_for=lambda r:{'expected_app_exit':{'code':1,'status':0},'admission':r.admission_sha}))
        p=NativePorts(b,'/invented',value,a,lambda event:None,lambda label,end:'Cancelled',clock=lambda:0)
        p.owned_menu_quit=lambda run,end:run.ax.quit_ui()
        p.cleanup_original_main=lambda run,end:run.bound_main()
        p.runs['A']=run
        return p
    def run_fixture(self):
        events=[]
        run=N(sample=lambda:None,observed_processes=[],cleanup=False,ui_deadline=0,quit_requested=False,stop_requested=False,admission_sha='a'*64,root=Path('/invented/A'),
            extra_cleanup_ready=lambda:True,bound_main=lambda:events.append('bound'),
            ax=N(quit_ui=lambda:events.append('quit')),act_record=lambda n,v:events.append(n),
            reservation=N(observe=lambda:{'code':1,'status':0},administrative_reap=lambda e:events.append('reap') or 0,reaped=False),
            stop=N(set=lambda:events.append('stop-monitor')),thread=N(join=lambda timeout:None,is_alive=lambda:False))
        return run,events
    def test_quit_original_normal_exit_then_fresh_reap_only(self):
        run,events=self.run_fixture();p=self.ports(run)
        r=p.quit_normal('A',20)
        self.assertEqual(events[:2],['bound','quit']);self.assertLess(events.index('attended-admin-release-intent.json'),events.index('reap'))
        self.assertTrue(r['reaped']);self.assertEqual(r['supplier_settlement'],'not claimed')
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
    def test_unknown_helper_refuses_before_any_Quit(self):
        run,events=self.run_fixture();run.extra_cleanup_ready=lambda:False;p=self.ports(run)
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
        self.assertFalse(events)
    def test_nonzero_exit_never_reaped(self):
        run,events=self.run_fixture();run.reservation.observe=lambda:{'code':1,'status':1};p=self.ports(run)
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
        self.assertNotIn('reap',events)
    def test_unknown_guard_blocks_closure_receipt(self):
        run,events=self.run_fixture();run.thread.is_alive=lambda:True;p=self.ports(run)
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
        self.assertNotIn('A',p.closures)
    def test_Quit_never_affirms_pending_B_sheet(self):
        run,events=self.run_fixture();run.stop_requested=True;p=self.ports(run);p.runs['B']=run
        with self.assertRaises(RuntimeError):p.quit_normal('B',20)
        self.assertFalse(events)

class PreSpawnTests(unittest.TestCase):
    def test_resource_refusal_never_sets_launch_unknown_or_spawns(self):
        from types import SimpleNamespace as N
        from unittest.mock import patch
        stopped=[]
        class Run:
            def __init__(self,*args):
                self.screen=N();self.reservation=None;self.thread=None
                self.stop=N(set=lambda:stopped.append(True));self.safe_log=lambda *a,**k:None
            def sample(self,admission=False):raise RuntimeError('exclusive pending')
        value={};admissions=N(value=value,before_launch=lambda *args:None)
        b=N(check_observation_capabilities=lambda:None,ax_route_support=N(make_run=lambda b:Run))
        ports=NativePorts(b,'/invented',value,admissions,lambda event:None,lambda *args:None,clock=lambda:0)
        with patch('native_attended_ports.subprocess.Popen',side_effect=AssertionError('must not spawn')):
            with self.assertRaisesRegex(RuntimeError,'exclusive'):ports.launch('A',{'admission_sha256':'a'*64},295)
        self.assertIsNone(ports.pending_launch);self.assertIsNone(ports.runs['A'].reservation);self.assertEqual(stopped,[True])


class PostReapTests(unittest.TestCase):
    ports=Tests.ports
    run_fixture=Tests.run_fixture
    def test_passive_settle_after_reap_allows_transient_residency(self):
        run,events=self.run_fixture();p=self.ports(run);samples=[]
        def sample():
            samples.append(True);run.observed_processes=['invented exiting supplier'] if len(samples)==1 else []
        run.sample=sample
        with patch('native_attended_ports.time.sleep'):
            result=p.quit_normal('A',20)
        self.assertEqual(len(samples),2);self.assertTrue(result['released'])
        self.assertIn('attended-admin-release-result.json',events)
    def test_actual_wait_is_recorded_when_resources_never_settle(self):
        run,events=self.run_fixture();p=self.ports(run);run.observed_processes=['invented survivor']
        with patch('native_attended_ports.time.sleep'),self.assertRaises(RuntimeError):p.quit_normal('A',20)
        self.assertIn('attended-admin-release-result.json',events);self.assertNotIn('A',p.closures)

class PreJourneyCleanupTests(unittest.TestCase):
    def fixture(self):
        identity={'pid':10,'birth':'original'};window={'window_id':20,'title':'original'}
        inventory=[{'window_id':20,'on_screen':True}];children=['group'];roots=['main'];closed=[];logged=[]
        class Backend:
            def close(self):closed.append(True)
        w=N(d=N(NativeBackend=Backend,bound_identity=lambda run,backend:dict(identity)),
            select_main=lambda backend,pid:dict(window),owned_inventory=lambda backend,pid:list(inventory))
        ax=N(last_window_observation=[{'AXRole':'AXWindow','AXTitle':'original','disposition':'owned-window-root'}],a=N(),main=lambda:'main',own=lambda e:None,windows=lambda:list(roots),c=N(CFEqual=lambda a,b:a==b),
            attr=lambda e,k:list(children) if (e,k)==('main','AXChildren') else ('AXSheet' if e=='sheet' else 'AXGroup'))
        def observed_windows():
            ax.last_window_observation=[{'AXRole':'AXWindow','AXTitle':'original','disposition':'owned-window-root'}]
            return list(roots)
        ax.windows=observed_windows
        run=N(ax_binding=None,screen=N(window=N(initial_binding=(dict(identity),dict(window)))),
              ax=ax,extra_cleanup_ready=lambda:True,safe_log=lambda *a,**k:logged.append(k))
        value={};admissions=N(value=value)
        b=N(screen_support=N(w=w),ax_route_support=N(window_number=lambda ax,e:20))
        ports=NativePorts(b,'/invented',value,admissions,lambda event:None,lambda *args:None,clock=lambda:0)
        return ports,run,identity,window,inventory,children,roots,closed,logged
    def test_failed_capture_before_journey_can_revalidate_exact_initial_main(self):
        p,r,*rest=self.fixture();library=r.ax.a
        self.assertEqual(p.cleanup_original_main(r,5),'main')
        self.assertIsNone(r.ax_binding);self.assertIs(r.ax.a,library)
        self.assertEqual(rest[-2],[True]);self.assertFalse(rest[-1][0]['qualification_binding_initialized'])
    def test_missing_changed_or_blocked_initial_main_never_authorizes_Quit(self):
        for case in ['missing','birth','window','sheet','extra-window','extra-AX','helper']:
            with self.subTest(case=case):
                p,r,identity,window,inventory,children,roots,closed,logged=self.fixture()
                if case=='missing':r.screen.window.initial_binding=None
                if case=='birth':identity['birth']='replacement'
                if case=='window':window['window_id']=21
                if case=='sheet':children.append('sheet')
                if case=='extra-window':inventory.append({'window_id':21,'on_screen':True})
                if case=='extra-AX':roots.append('dialog')
                if case=='helper':r.extra_cleanup_ready=lambda:False
                with self.assertRaises(RuntimeError):p.cleanup_original_main(r,5)
                self.assertFalse(any('qualification_binding_initialized' in record for record in logged))

class PreJourneyQuitPathTests(unittest.TestCase):
    def test_full_quit_path_after_helper_refusal_uses_independent_binding(self):
        p,r,identity,window,inventory,children,roots,closed,logged=PreJourneyCleanupTests().fixture()
        events=[]
        r.cleanup=False;r.ui_deadline=0;r.quit_requested=False;r.stop_requested=False
        r.admission_sha='a'*64;r.root=Path('/invented/A')
        r.reservation=N(reaped=False,observe=lambda:{'code':1,'status':0})
        def reap(observed):r.reservation.reaped=True;events.append('original wait');return 0
        r.reservation.administrative_reap=reap
        r.act_record=lambda name,value:events.append(name)
        r.sample=lambda:None;r.observed_processes=[]
        r.stop=N(set=lambda:events.append('stop guard'));r.thread=N(join=lambda timeout:None,is_alive=lambda:False)
        r.bound_main=lambda:(_ for _ in ()).throw(RuntimeError('owned AX journey not initialized'))
        p.admissions.check_birth=lambda label,run:None;p.runs['A']=r
        p.b.release_support=N(normal_exit=lambda value:value=={'code':1,'status':0},
            request_for=lambda run:{'expected_app_exit':{'code':1,'status':0}})
        p.owned_menu_quit=lambda run,end:events.append('one owned menu Quit')
        receipt=p.quit_normal('A',295)
        self.assertTrue(receipt['reaped']);self.assertTrue(receipt['released'])
        self.assertEqual(events.count('one owned menu Quit'),1);self.assertIsNone(r.ax_binding)
        self.assertLess(events.index('one owned menu Quit'),events.index('original wait'))

class AcquiredChildFailureTests(unittest.TestCase):
    def test_failures_after_spawn_before_AX_or_first_capture_retain_original_custody(self):
        for stage in ('start-log','AX-load','AX-init','first-capture'):
            with self.subTest(stage=stage),tempfile.TemporaryDirectory(prefix='acquired-child-failure-') as d:
                root=Path(d).resolve();(root/'A').mkdir();(root/'A/phase.sb').write_text('fixture-policy')
                child=N(pid=123);stops=[];reports=[];births=[]
                def fail():raise RuntimeError('invented '+stage)
                class Guard:
                    def __init__(self,**kwargs):self.live=False
                    def start(self):self.live=True
                    def is_alive(self):return self.live
                    def join(self,timeout):self.live=False
                class Run:
                    def __init__(self,*args):
                        self.reservation=None;self.thread=None;self.ax=None;self.ax_binding=None
                        self.stop=N(set=lambda:stops.append(True));self.monitor=lambda:None
                        self.screen=N(window=N(initial_binding=None,acquire_initial_window=lambda:None,capture=fail))
                        self.sample=lambda **kwargs:None;self.safe_log=lambda *a,**k:None;self.alive=lambda:None
                    def log(self,*args,**kwargs):
                        if stage=='start-log':fail()
                def ax_factory(*args):
                    if stage=='AX-init':fail()
                    return N(press=lambda e:None,key=lambda *a,**k:None)
                def load_ax():
                    if stage=='AX-load':fail()
                    return ax_factory
                value={'executable':'/invented/App','native_input_paths':{'project':str(root)}}
                admissions=N(value=value,before_launch=lambda *args:None,policy=lambda *args:'fixture-policy',
                    environment=lambda label:{},bind_birth=lambda label,run:births.append(run.reservation.child),
                    check_birth=lambda label,run:None)
                b=N(check_observation_capabilities=lambda:None,
                    ax_route_support=N(make_run=lambda b:Run,bounded_ax=lambda ax:ax),
                    ax_support=N(wrap_ax=lambda ax:ax),base=N(load_ax=load_ax),
                    AppReservation=lambda original:N(child=original,reaped=False))
                ports=NativePorts(b,root,value,admissions,reports.append,lambda *a:None,clock=lambda:0)
                with patch('native_attended_ports.threading.Thread',Guard),patch('native_attended_ports.subprocess.Popen',return_value=child) as spawn:
                    if stage=='first-capture':
                        self.assertEqual(ports.launch('A',{'admission_sha256':'a'*64},295),'A')
                        with self.assertRaisesRegex(RuntimeError,stage):ports.ordinary_setup_save('A',160)
                    else:
                        with self.assertRaisesRegex(RuntimeError,stage):ports.launch('A',{'admission_sha256':'a'*64},295)
                    spawn.assert_called_once()
                self.assertIs(ports.runs['A'].reservation.child,child)
                self.assertFalse(ports.runs['A'].reservation.reaped);self.assertTrue(ports.runs['A'].thread.is_alive())
                self.assertIsNone(ports.pending_launch);self.assertIsNone(ports.runs['A'].ax_binding)
                self.assertFalse(stops);self.assertFalse(ports.closures)
                ports.retain_and_report('A',295,failure={'original_error':'invented '+stage,'cleanup_error':None})
                self.assertEqual(reports[0]['failure']['original_error'],'invented '+stage)
                self.assertEqual(reports[0]['retained_incarnations'],['A'])
                self.assertEqual(reports[0]['live_guard_incarnations'],['A'])

class CleanupRootAndPressTests(unittest.TestCase):
    def test_real_window_filter_dropped_unknown_root_still_refuses_cleanup(self):
        from native_b_ax import wrap_ax
        p,r,*_=PreJourneyCleanupTests().fixture()
        class Base:
            def __init__(self):self.app='app';self.c=N(CFEqual=lambda a,b:a==b)
            def windows(self):return ['main','unknown']
            def own(self,e):pass
            def attr(self,e,name):return ({'AXRole':'AXWindow','AXTitle':'original'} if e=='main' else {}).get(name)
        filtered=wrap_ax(Base)()
        def windows():
            result=filtered.windows();r.ax.last_window_observation=filtered.last_window_observation;return result
        r.ax.windows=windows
        with self.assertRaisesRegex(RuntimeError,'unclassified'):p.cleanup_original_main(r,5)
        self.assertEqual(filtered._admitted_window_roots,['main'])
    def test_late_helper_or_inventory_change_and_role_failures_refuse(self):
        for case in ['helper','inventory','AXUnknown','AXPopover','AXMenu','AXWindow','None','children','number','deadline','bounds']:
            with self.subTest(case=case):
                p,r,identity,window,inventory,children,roots,closed,logged=PreJourneyCleanupTests().fixture()
                if case=='helper':
                    calls=iter([True,False]);r.extra_cleanup_ready=lambda:next(calls)
                elif case=='inventory':
                    calls=iter([list(inventory),[]]);p.b.screen_support.w.owned_inventory=lambda *args:next(calls)
                elif case=='children':children.extend(['group']*8)
                elif case=='number':p.b.ax_route_support.window_number=lambda *args:999
                elif case=='deadline':p.clock=lambda:6
                elif case=='bounds':window['bounds']={'X':1}
                else:
                    old=r.ax.attr
                    r.ax.attr=lambda e,k,old=old,case=case: (None if case=='None' else case) if (e,k)==('group','AXRole') else old(e,k)
                with self.assertRaises(RuntimeError):p.cleanup_original_main(r,5)
                self.assertFalse(any('qualification_binding_initialized' in record for record in logged))
    def test_actual_menu_path_revalidates_before_intent_and_press(self):
        events=[]
        class Adapter:
            app='app'
            def __init__(self,ax):pass
            def same(self,a,b):return a==b
            def owner(self,e):return 10
            def timeout(self,e,t):return 0
            def read(self,e,k):
                data={'app':{'AXTitle':'App','AXMenuBar':'bar'},'bar':{'AXRole':'AXMenuBar','AXChildren':['top']},
                      'top':{'AXRole':'AXMenuBarItem','AXTitle':'App','AXChildren':['menu']},
                      'menu':{'AXRole':'AXMenu','AXChildren':['quit']},
                      'quit':{'AXRole':'AXMenuItem','AXTitle':'Quit App','AXEnabled':True}}
                events.append('read:'+e+':'+k);return 0,data[e][k]
            def press(self,e):events.append('press');return 0
            def close(self):events.append('close')
        p,r,*_=PreJourneyCleanupTests().fixture()
        r.reservation=N(child=N(pid=10));r.act_record=lambda name,value:events.append(name)
        def refuse(run,end):events.append('fresh cleanup');raise RuntimeError('late modal')
        p.cleanup_original_main=refuse
        with patch('native_attended_ports.NativeAdapter',Adapter),self.assertRaisesRegex(RuntimeError,'late modal'):
            p.owned_menu_quit(r,5)
        self.assertIn('read:quit:AXEnabled',events);self.assertIn('fresh cleanup',events)
        self.assertNotIn('owned-menu-quit-intent.json',events);self.assertNotIn('press',events)
        self.assertEqual(events[-1],'close')
        # Exercise the same production traversal in read-only preflight mode.
        events.clear();p.cleanup_original_main=lambda *args:events.append('fresh cleanup')
        Adapter.actions=lambda self,e:['AXPress']
        with patch('native_attended_ports.NativeAdapter',Adapter):p.owned_menu_quit(r,5,post=False)
        self.assertIn('owned-menu-quit-preflight.json',events)
        self.assertNotIn('owned-menu-quit-intent.json',events);self.assertNotIn('press',events)
        self.assertLess(events.index('fresh cleanup'),events.index('owned-menu-quit-preflight.json'))
        self.assertEqual(events[-1],'close')
        events.clear();Adapter.actions=lambda self,e:[]
        with patch('native_attended_ports.NativeAdapter',Adapter),self.assertRaisesRegex(RuntimeError,'action unavailable'):
            p.owned_menu_quit(r,5,post=False)
        self.assertNotIn('owned-menu-quit-preflight.json',events);self.assertNotIn('press',events)


class CleanupObservationEvidenceTests(unittest.TestCase):
    def test_failed_main_lookup_preserves_existing_root_and_attribute_facts(self):
        p,r,identity,window,inventory,children,roots,closed,logged=PreJourneyCleanupTests().fixture()
        def unavailable():
            r.ax.last_window_observation=[{'AXRole':None,'disposition':'not-a-window-root'}]
            r.ax.attribute_errors={'AXRole:-25204':1}
            raise RuntimeError('distinct owned main AXWindow unavailable')
        r.ax.main=unavailable
        with self.assertRaisesRegex(RuntimeError,'distinct owned'):p.cleanup_original_main(r,5)
        self.assertTrue(logged[-1]['AX_main_lookup_attempted'])
        self.assertEqual(logged[-1]['AX_window_observation'],r.ax.last_window_observation)
        self.assertEqual(logged[-1]['AX_attribute_errors'],{'AXRole:-25204':1})
        self.assertIsNone(r.ax_binding);self.assertEqual(closed,[True])
    def test_failure_before_lookup_does_not_present_stale_AX_as_current(self):
        p,r,identity,window,inventory,children,roots,closed,logged=PreJourneyCleanupTests().fixture()
        identity['birth']='changed'
        with self.assertRaises(RuntimeError):p.cleanup_original_main(r,5)
        self.assertFalse(logged[-1]['AX_main_lookup_attempted'])
        self.assertIsNone(logged[-1]['AX_window_observation'])

    def test_failure_during_lookup_does_not_reuse_previous_root_observation(self):
        p,r,*_=PreJourneyCleanupTests().fixture()
        r.ax.last_window_observation=[{'AXRole':'AXWindow','disposition':'old'}]
        r.ax.main=lambda:(_ for _ in ()).throw(RuntimeError('read failed before roots'))
        logged=[];r.safe_log=lambda *a,**k:logged.append(k)
        with self.assertRaises(RuntimeError):p.cleanup_original_main(r,5)
        self.assertIsNone(logged[-1]['AX_window_observation'])
