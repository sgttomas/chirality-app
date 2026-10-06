"""Parent ownership channel. Supplier exec waits until its group is journalled."""
import os,select,signal,struct,threading,time,subprocess
from witness_common import save,require
class Ownership:
    def __init__(self,root):
        self.root=root;self.register_read,self.register_write=os.pipe();self.ack_read,self.ack_write=os.pipe();self.entries=[];self.errors=[];self.closing=False;self.lock=threading.Lock();self.worker=None
    def environment(self): return {'CHIRALITY_WITNESS_REGISTER_FD':str(self.register_write),'CHIRALITY_WITNESS_ACK_FD':str(self.ack_read)}
    def start(self):
        self.worker=threading.Thread(target=self.receive,daemon=True);self.worker.start()
    def inherited(self):return (self.register_write,self.ack_read)
    def handed_off(self):os.close(self.register_write);os.close(self.ack_read)
    def receive(self):
        pending=b''
        try:
            while True:
                data=os.read(self.register_read,8-len(pending))
                if not data:
                    require(not pending,'partial ownership record');break
                pending+=data
                if len(pending)!=8:continue
                pid,stage=struct.unpack('=ii',pending);pending=b''
                require(pid>1 and stage in (1,2),'invalid ownership record')
                require(os.getpgid(pid)==pid,'supplier did not enter its own group')
                with self.lock:
                    require(all(x['pid']!=pid for x in self.entries),'duplicate/reused supplier PID')
                    self.entries.append({'pid':pid,'pgid':pid,'stage':stage,'registeredBeforeExec':True,'retired':False})
                    save(self.root/'owned-processes.json',self.entries)
                    os.write(self.ack_write,b'X' if self.closing else b'A')
        except Exception as e:
            self.errors.append(repr(e));self.closing=True
        finally:
            os.close(self.register_read);os.close(self.ack_write)
    def signal_owned(self,sig,events):
        with self.lock:
            for entry in self.entries:
                if entry['retired']:continue
                try:os.killpg(entry['pgid'],sig);events.append({'pid':entry['pid'],'signal':sig,'result':'sent'})
                except ProcessLookupError:entry['retired']=True;events.append({'pid':entry['pid'],'signal':sig,'result':'absent; retired, never signal again'})
    def cleanup(self,process,grace=2):
        self.closing=True;events=[]
        # Keep harness alive initially so its direct supplier children can be waited/reaped.
        self.signal_owned(signal.SIGTERM,events)
        try:process.wait(timeout=grace)
        except subprocess.TimeoutExpired:pass
        self.signal_owned(signal.SIGKILL,events)
        try:process.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:process.wait(timeout=grace)
            except subprocess.TimeoutExpired:process.kill();process.wait(timeout=grace)
        if self.worker:self.worker.join(timeout=grace)
        # Late handshake records cannot exec after closing; cover them nonetheless.
        self.signal_owned(signal.SIGKILL,events)
        deadline=time.monotonic()+grace
        while time.monotonic()<deadline:
            self.signal_owned(0,events)
            if all(x['retired'] for x in self.entries):break
            time.sleep(.02)
        outcome={'harnessPid':process.pid,'harnessReaped':process.poll() is not None,'ownershipChannelClosed':self.worker is not None and not self.worker.is_alive(),'ownedGroups':self.entries,'errors':self.errors,'events':events,'descendantReaping':'Host/harness reaps its children while alive; orphan reaping belongs to OS, not claimed by launcher'}
        outcome['clean']=outcome['harnessReaped'] and outcome['ownershipChannelClosed'] and not self.errors and all(x['retired'] for x in self.entries)
        save(self.root/'cleanup.json',outcome);return outcome
