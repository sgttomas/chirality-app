"""Private manager channel, not an App IPC or cancellation authority endpoint.

The active manager forwards each emitted owner-cancel-needed-now event to
Agent0 immediately through T3, and publishes completion only after the actual
owner response for this incarnation. No screenshot/old response counts.
"""
import json
import os
from pathlib import Path
import time
from native_b_window import private_json


class OwnerChannel:
    def __init__(self, root, candidate, admissions, clock=time.monotonic, sleep=time.sleep):
        self.root,self.candidate,self.admissions=Path(root),candidate,admissions
        self.clock,self.sleep=clock,sleep
        self.offers={};self.consumed=set()

    def deliver(self, event):
        value=dict(event,candidate=self.candidate,manager_must_forward_to_parent_now=True)
        label=value.get('incarnation')
        if value.get('event')=='owner-cancel-needed-now':
            receipt=self.admissions.receipts.get(label)
            if receipt is None:raise RuntimeError('no exact incarnation admission for owner request')
            offer={'action':'owner-cancel-completed','candidate':self.candidate,'incarnation':label,
                   'admission_sha256':receipt['admission_sha256'],'actual_owner_reply':'Cancelled'}
            self.offers[label]=offer
            value['completion_offer']=offer
            value['completion_file']=str(self.root/label/'owner-cancel-completed.json')
            value['publication']='Only after actual new owner completion; private0600 single-link temp + atomic rename; no personal-human attribution to agent'
        # Emission precedes optional file evidence. The supervising tool session
        # must remain actively read; absence of forwarding is not delivery proof.
        print(json.dumps(value),flush=True)

    def completion(self,label,end):
        if label not in self.offers or label in self.consumed:raise RuntimeError('owner completion not offered or reused')
        path=self.root/label/'owner-cancel-completed.json'
        while self.clock()<end:
            if os.path.lexists(path):
                value=private_json(path,4096)
                if value!=self.offers[label]:raise RuntimeError('owner completion source/incarnation differs')
                self.consumed.add(label)
                return 'Cancelled'
            self.sleep(min(.1,max(0,end-self.clock())))
        raise RuntimeError('owner completion not received before fixed allowance; retain custody')
