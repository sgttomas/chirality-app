"""One-use Agent0 disposition for an already-exited ORIGINAL Child only."""
import os
from native_attended_bridge import PARENT,publish,read,require


def terminal(observed):
    require(isinstance(observed,dict) and set(observed)=={'code','status'}
            and type(observed['code']) is int and type(observed['status']) is int,'invalid exit observation')
    if observed['code']==os.CLD_EXITED:
        require(0<=observed['status']<=255,'invalid exit code')
        return {'kind':'exit','exit_code':observed['status'],'signal':None}
    require(observed['code'] in (os.CLD_KILLED,os.CLD_DUMPED) and observed['status']>0,'original Child not terminal')
    return {'kind':'signal','exit_code':None,'signal':observed['status']}


def offer(ports,bridge,label):
    run=ports.runs[label];reservation=run.reservation
    require(reservation is not None and not reservation.reaped and not reservation.lost,'original custody unavailable')
    require(run.extra_cleanup_ready(),'helpers not settled')
    birth=ports.admissions.births.get(label)
    require(birth and birth['pid']==reservation.child.pid,'original birth not established')
    observed=reservation.observe();fact=terminal(observed)
    require(not(fact['kind']=='exit' and fact['exit_code']==0),'normal0 uses existing release path')
    return {'action':'reap-observed-exited-original-child','run_id':bridge.run_id,'candidate':bridge.candidate,
            'incarnation':label,'admission_sha256':run.admission_sha,'original_birth':birth,
            'observed_exit':observed,'terminal':fact,'issuer_thread':PARENT,
            'standing':'FAILED; no supplier settlement, qualification or next launch'}


def publish_disposition(root,event_id,parent_message_id):
    require(event_id.isdigit() and len(event_id)==4,'invalid disposition event')
    event=read(root/'bridge'/(event_id+'.event.json'))
    delivered=read(root/'bridge'/(event_id+'.delivery.json'))
    require(delivered.get('accepted') is True and delivered.get('run_id')==event['run_id']
            and delivered.get('event_id')==event_id,'disposition event not delivered')
    selected=event.get('administrative_disposition_offer')
    require(event.get('event')=='attended-terminal-disposition-needed' and selected
            and selected['issuer_thread']==PARENT and parent_message_id
            and parent_message_id!=delivered.get('message_id'),'actual distinct Agent0 decision required')
    terminal(selected['observed_exit'])
    publish(root/'bridge'/(event_id+'.disposition.json'),{'offer':selected,
            'parent_decision_message_id':parent_message_id,'simulation':event.get('simulation',False)})


def consume(ports,bridge,label,event_id):
    path=bridge.events/(event_id+'.disposition.json')
    if not path.exists():return False
    consumed=bridge.events/(event_id+'.disposition-consumed.json')
    if consumed.exists():return False
    instruction=read(path)
    require(instruction.get('simulation',False)==bridge.simulation,'simulation disposition cannot authorize native wait')
    require(instruction.get('parent_decision_message_id'),'missing explicit parent decision')
    expected=offer(ports,bridge,label)
    require(instruction.get('offer')==expected,'disposition/actual original exit/birth differs')
    run=ports.runs[label];reservation=run.reservation
    publish(consumed,{'offer':expected,'parent_decision_message_id':instruction['parent_decision_message_id']})
    run.act_record('terminal-administrative-reap-intent.json',expected)
    require(run.extra_cleanup_ready() and reservation.observe()==expected['observed_exit'],
            'original exit/helper standing changed immediately before wait')
    actual=reservation.child.wait() # retained Popen only; no numeric process action
    reservation.reaped=True # actual reap remains true even if evidence/result differs
    wanted=(expected['terminal']['exit_code'] if expected['terminal']['kind']=='exit' else -expected['terminal']['signal'])
    run.act_record('terminal-administrative-reap-result.json',{'pre_reap_observation':expected,'actual_wait':actual,
        'expected_wait':wanted,'matches':actual==wanted,'success':False,'supplier_settlement':False,
        'all_resources_closed':False})
    require(actual==wanted,'actual wait differs; Child reaped but resources unresolved')
    return True
