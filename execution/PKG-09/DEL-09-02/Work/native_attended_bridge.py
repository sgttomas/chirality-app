"""Private controller/manager event receipts; never an App control endpoint."""
import json
import os
from pathlib import Path
import stat
import time
import uuid
from datetime import datetime, timezone

PARENT='0f35714c-46fb-45d8-9c97-c927c6587c1e'

def require(ok, message):
    if not ok:raise RuntimeError(message)

def private_directory(path):
    p=Path(path);s=p.lstat()
    require(p.is_absolute() and p.resolve()==p and stat.S_ISDIR(s.st_mode)
            and s.st_uid==os.getuid() and stat.S_IMODE(s.st_mode)==0o700,'private physical directory required')
    return p

def read(path):
    p=Path(path);private_directory(p.parent)
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1
            and stat.S_IMODE(s.st_mode)==0o600 and 0<s.st_size<=65536,'private bounded single-link JSON required')
        raw=os.read(fd,65537);after=os.fstat(fd)
        stamp=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_uid,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
        require(len(raw)==s.st_size and stamp(s)==stamp(after)==stamp(p.lstat()),'private JSON changed')
        def unique(items):
            out={}
            for k,v in items:require(k not in out,'duplicate JSON key');out[k]=v
            return out
        return json.loads(raw,object_pairs_hook=unique)
    finally:os.close(fd)

def publish(path, value):
    path=Path(path);private_directory(path.parent)
    require(not os.path.lexists(path),'receipt already exists; no replacement')
    import fcntl
    lock=os.open(path.parent/'.publication.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    temp=None
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        require(not os.path.lexists(path),'receipt already exists; no replacement')
        temp=path.parent/('.'+path.name+'.'+uuid.uuid4().hex)
        fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as out:json.dump(value,out,sort_keys=True);out.write('\n');out.flush();os.fsync(out.fileno())
        require(not os.path.lexists(path),'receipt appeared; refuse overwrite')
        os.rename(temp,path)
    finally:
        if temp is not None and temp.exists():temp.unlink()
        os.close(lock)

class ReceiptBridge:
    def __init__(self,root,candidate,run_id,admissions,clock=time.monotonic,sleep=time.sleep,wall=time.time,simulation=False):
        self.root=private_directory(root);self.candidate=candidate;self.run_id=run_id;self.admissions=admissions
        self.clock,self.sleep,self.wall=clock,sleep,wall
        self.simulation=simulation
        self.events=self.root/'bridge';private_directory(self.events)
        self.counter=0;self.offers={};self.consumed=set()
    def emit(self,event):
        self.counter+=1;event_id='%04d'%self.counter
        value=dict(event,run_id=self.run_id,candidate=self.candidate,event_id=event_id,
                   parent_thread=PARENT,emitted_at=datetime.now(timezone.utc).isoformat(),delivery='not yet acknowledged',simulation=self.simulation)
        if isinstance(event.get('fixed_end'),(int,float)):
            value['fixed_end_utc']=datetime.fromtimestamp(self.wall()+event['fixed_end']-self.clock(),timezone.utc).isoformat()
        if event.get('event')=='owner-cancel-needed-now':
            label=event['incarnation'];admission=self.admissions.receipts[label]
            offer={'action':'owner-cancel-completed','run_id':self.run_id,'candidate':self.candidate,
                'incarnation':label,'event_id':event_id,'admission_sha256':admission['admission_sha256'],
                'actual_owner_reply':'Cancelled'}
            require(label not in self.offers,'owner fallback already offered')
            self.offers[label]=offer;value['completion_offer']=offer
        publish(self.events/(event_id+'.event.json'),value)
        try:print(json.dumps({'event':'attended-manager-forward','run_id':self.run_id,'event_id':event_id,
                          'event_path':str(self.events/(event_id+'.event.json')),'parent_thread':PARENT}),flush=True)
        except (BrokenPipeError,OSError):pass # queued file persists; absent transport receipt refuses continuation
        return event_id
    def deliver(self,event):
        event_id=self.emit(event)
        # T3 tool result is evidence of transport acceptance, never owner reading.
        end=self.clock()+8 # transport only; never extends any UI/action deadline
        receipt=self.events/(event_id+'.delivery.json')
        while self.clock()<end:
            if receipt.exists():
                value=read(receipt)
                require(value.get('run_id')==self.run_id and value.get('event_id')==event_id
                        and value.get('parent_thread')==PARENT and value.get('message_id')
                        and value.get('transport')=='t3_thread_send', 'delivery receipt differs')
                require(value.get('simulation',False)==self.simulation,'simulation receipt cannot authorize native continuation')
                require(value.get('accepted') is True,'T3 delivery failed')
                return
            self.sleep(.05)
        raise RuntimeError('T3 delivery not acknowledged; retained custody, no input continuation')
    def completion(self,label,end):
        require(label in self.offers and label not in self.consumed,'no unconsumed owner offer')
        offer=self.offers[label];path=self.events/(offer['event_id']+'.completion.json')
        while self.clock()<end:
            if path.exists():
                value=read(path);require(value.get('offer')==offer and value.get('owner_message_id') and value.get('simulation',False)==self.simulation,
                    'actual owner completion binding unavailable')
                self.consumed.add(label);return 'Cancelled'
            self.sleep(min(.1,max(0,end-self.clock())))
        raise RuntimeError('owner completion is not yet received; retain custody without deadline rearm')
    def late_completion(self,label):
        if label not in self.offers or label in self.consumed:return None
        path=self.events/(self.offers[label]['event_id']+'.completion.json')
        if not path.exists():return None
        return self.completion(label,self.clock()+.1)

def delivery_receipt(root,event_id,receipt):
    root=private_directory(root);require(event_id.isdigit() and len(event_id)==4,'invalid event id')
    event=read(root/'bridge'/(event_id+'.event.json'))
    require(receipt.get('parent_thread')==PARENT and receipt.get('run_id')==event['run_id']
            and receipt.get('event_id')==event_id and receipt.get('transport')=='t3_thread_send'
            and type(receipt.get('accepted')) is bool,'transport receipt scope differs')
    if receipt['accepted']:require(isinstance(receipt.get('message_id'),str) and receipt['message_id'],'missing T3 message id')
    publish(root/'bridge'/(event_id+'.delivery.json'),receipt)

def owner_completion(root,event_id,actual_reply,owner_message_id):
    root=private_directory(root);require(event_id.isdigit() and len(event_id)==4,'invalid event id')
    event=read(root/'bridge'/(event_id+'.event.json'));delivery=read(root/'bridge'/(event_id+'.delivery.json'))
    require(delivery.get('accepted') is True and delivery.get('run_id')==event['run_id'],'owner offer not delivered')
    require(event.get('completion_offer') and actual_reply=='Cancelled' and isinstance(owner_message_id,str)
            and owner_message_id,'actual new owner completion required')
    publish(root/'bridge'/(event_id+'.completion.json'),{'offer':event['completion_offer'],
        'owner_message_id':owner_message_id,'simulation':event.get('simulation',False),'recorded_at':datetime.now(timezone.utc).isoformat()})
