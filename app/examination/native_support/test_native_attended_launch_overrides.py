"""Exercise the actual ports.launch input/focus overrides with invented objects only."""
import sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace as N
from unittest.mock import patch
from native_attended_ports import NativePorts
class LaunchOverrideTests(unittest.TestCase):
    def test_wrappers(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();(root/'A').mkdir();(root/'A/phase.sb').write_text('p')
            calls=[];front=[True]
            class Guard:
                def __init__(self,**k):pass
                def start(self):pass
            class Run:
                def __init__(self,*a):
                    self.reservation=None;self.thread=None;self.ax=None
                    self.screen=N(window=N());self.sample=lambda **k:None;self.monitor=None
                    self.bound_main=lambda press=False:calls.append(("bound_main",press));self.alive=lambda:None
                def log(self,*a,**k):pass
            class Lib:
                def AXUIElementSetAttributeValue(self,e,name,value):calls.append(('set',e,name));return 0
            class AX:
                def __init__(self,*a):self.app='app';self.a=Lib();self.c=None
                def attr(self,e,k):calls.append(('read',k));return front[0]
                def own(self,e):pass
                def string(self,s):return s
                def press(self,e):calls.append(('PRESS',e))
                def key(self,*a,**k):calls.append(('KEY',a))
                def focus(self,e):calls.append(('BASE-FOCUS-SETS-AXFrontmost',e))
            value={'executable':'/invented/App','native_input_paths':{'project':str(root)}}
            adm=N(value=value,before_launch=lambda *a:None,policy=lambda *a:'p',environment=lambda l:{},
                  bind_birth=lambda *a:None,check_birth=lambda *a:calls.append('birth'))
            b=N(check_observation_capabilities=lambda:None,ax_route_support=N(make_run=lambda b:Run,bounded_ax=lambda ax:ax),
                ax_support=N(wrap_ax=lambda ax:ax),base=N(load_ax=lambda:AX),AppReservation=lambda c:N(child=c))
            p=NativePorts(b,root,value,adm,lambda e:None,lambda *a:None,clock=lambda:0)
            with patch('native_attended_ports.threading.Thread',Guard),patch('native_attended_ports.subprocess.Popen',return_value=N(pid=1)):
                p.launch('A',{'admission_sha256':'a'*64},295)
            run=p.runs['A']
            self.assertFalse(run.first_press_focus());self.assertIn(('bound_main',True),calls)
            for verified,fm in [(False,True),(True,False)]:
                run.foreground_verified=verified;front[0]=fm;calls.clear()
                for op in (lambda:run.ax.press('x'),lambda:run.ax.key(1),lambda:run.ax.focus('x')):
                    with self.assertRaisesRegex(RuntimeError,'verified original foreground lost'):op()
                self.assertFalse([c for c in calls if c[0] in ('PRESS','KEY','set','BASE-FOCUS-SETS-AXFrontmost')])
            run.foreground_verified=True;front[0]=True;calls.clear()
            with patch('ctypes.c_void_p.in_dll',return_value=N(value='true')):run.ax.focus('field')
            run.ax.press('x');run.ax.key(1)
            sets=[c for c in calls if c[0]=='set']
            self.assertEqual(sets,[('set','field','AXFocused')])  # never AXFrontmost
            self.assertIn(('PRESS','x'),calls);self.assertIn(('KEY',(1,)),calls)
            self.assertNotIn(('BASE-FOCUS-SETS-AXFrontmost','field'),calls)
