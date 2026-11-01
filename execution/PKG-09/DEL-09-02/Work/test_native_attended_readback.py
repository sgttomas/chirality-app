import unittest
from native_attended_readback import CountedAXLibrary
class Native:
    def __init__(self):self.calls=[]
    def AXRead(self,*args):self.calls.append(args);return 0
class Tests(unittest.TestCase):
    def test_total_call_cap_counts_nested_calls(self):
        native=Native();budget=CountedAXLibrary(native,10,cap=2,clock=lambda:0)
        budget.AXRead(1);budget.AXRead(2)
        with self.assertRaises(RuntimeError):budget.AXRead(3)
        self.assertEqual(len(native.calls),2)
    def test_deadline_refuses_before_native_call(self):
        native=Native();budget=CountedAXLibrary(native,0.1,clock=lambda:0)
        with self.assertRaises(RuntimeError):budget.AXRead(1)
        self.assertFalse(native.calls)
    def test_late_native_result_refuses(self):
        now=[0]
        class Slow:
            def AXRead(self):now[0]=11;return 0
        budget=CountedAXLibrary(Slow(),10,clock=lambda:now[0])
        with self.assertRaises(RuntimeError):budget.AXRead()
        self.assertEqual(budget.calls,1)

class ReadbackTests(unittest.TestCase):
    def fixture(self, terminal=False):
        from types import SimpleNamespace as N
        from native_attended_readback import source_after_cancel
        generation={'appSession':'B','home':'h','spawnCounter':1};identity={'pid':1};main={'window_id':2}
        inventory=[{'window_id':2,'on_screen':True}]
        observed={'rendered_state':'ready','lifecycle':([{'generation':generation,'transitionId':'LT-23'}] if terminal else [])}
        class Backend:
            def close(self):pass
        w=N(d=N(NativeBackend=Backend,bound_identity=lambda run,backend:identity),
            owned_inventory=lambda backend,pid:inventory,select_main=lambda backend,pid:main)
        saved=[];native=Native()
        run=N(stop_requested=True,stop_confirmed=False,generation=generation,ax_binding=(identity,main),
            ax=N(a=native),value={},main_rows=lambda:[],act_record=lambda name,value:saved.append((name,value)))
        b=N(decode_diagnostics=lambda strings,protocol:observed,
            source_gate=lambda obs,value,gen:gen,ready_gate=lambda obs,value:None)
        route=N(web_strings=lambda rows:[],web_control=lambda *args:'actual button')
        context={'posted':True,'identity':identity,'generation':generation,'before_inventory':inventory}
        return source_after_cancel,run,context,b,route,w,saved,native
    def test_actual_source_proof_and_original_library_restored(self):
        fn,run,ctx,b,route,w,saved,native=self.fixture()
        result=fn(run,ctx,None,15,b,route,w,clock=lambda:0)
        self.assertEqual(result['generation'],ctx['generation']);self.assertIs(run.ax.a,native)
        self.assertEqual(len(saved),1);self.assertEqual(result['LT23_rows'],[])
    def test_terminal_effect_cannot_be_reported_as_cancel(self):
        fn,run,ctx,b,route,w,saved,native=self.fixture(True)
        with self.assertRaises(RuntimeError):fn(run,ctx,None,15,b,route,w,clock=lambda:0)
        self.assertFalse(saved);self.assertIs(run.ax.a,native)
    def test_changed_source_callback_refuses_and_restores_library(self):
        fn,run,ctx,b,route,w,saved,native=self.fixture()
        def reject(*args):raise RuntimeError('source changed')
        b.source_gate=reject
        with self.assertRaises(RuntimeError):fn(run,ctx,None,15,b,route,w,clock=lambda:0)
        self.assertFalse(saved);self.assertIs(run.ax.a,native)

class RepresentativeWalkTests(unittest.TestCase):
    def test_real_BAX_walk_416_nodes_fits_readback_call_expansion(self):
        from native_b_ax import wrap_ax
        from types import SimpleNamespace as N
        class Library:
            def AXOwner(self):return 0
            def AXTimeout(self):return 0
            def AXRead(self):return 0
        class Base:
            def __init__(self):
                self.a=CountedAXLibrary(Library(),15,clock=lambda:0)
                self.c=N(CFEqual=lambda a,b:a==b);self.app='app'
            def own(self,e):self.a.AXOwner();self.a.AXTimeout()
            def attr(self,e,name):
                self.own(e);self.a.AXRead()
                if name=='AXRole':return 'AXWindow' if e==0 else 'AXStaticText'
                if name=='AXChildren':return list(range(1,416)) if e==0 else []
                if name=='AXValue':return 'actual fixture text'
                return None
        ax=wrap_ax(Base)();rows=ax.walk(0)
        self.assertEqual(len(rows),416);self.assertEqual(ax.a.calls,8320)
    def test_setup_keyboard_counts_and_requires_original_pid(self):
        class Keyboard:
            def CGEventPostToPid(self,pid,event):return None
        budget=CountedAXLibrary(Keyboard(),10,clock=lambda:0,setup_pid=42)
        budget.CGEventPostToPid(42,'event')
        with self.assertRaises(RuntimeError):budget.CGEventPostToPid(43,'event')
        with self.assertRaises(RuntimeError):CountedAXLibrary(Keyboard(),10,clock=lambda:0).CGEventPostToPid(42,'event')
        self.assertEqual(budget.calls,1)
