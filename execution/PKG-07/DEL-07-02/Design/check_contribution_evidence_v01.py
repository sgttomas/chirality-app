"""CCE definition-only cold consistency checks. NEVER mints native/scope authority."""
import copy
import runpy
import contextlib
import io
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry, Resource
ROOT=Path(__file__).resolve().parent
load=lambda n:json.loads((ROOT/n).read_text())
schema=load('connector.route-account.v0.5.schema.json')
message=load('connector.contribution-message.v0.1.schema.json')
for s in (schema,message):Draft202012Validator.check_schema(s)
validator=Draft202012Validator(schema)
standing=load('connector.standing.schema.json')
base_validator=Draft202012Validator(load('connector.route-account.v0.4.schema.json'),registry=Registry().with_resource(standing['$id'],Resource.from_contents(standing)))
with contextlib.redirect_stdout(io.StringIO()):
    base_semantics=runpy.run_path(str(ROOT/'check_record_reconstruction_v04.py'))['validate']
fixture=load('contribution_evidence_v01.fixture.json')
base_bytes=(ROOT/'record_reconstruction_v04.fixture.json').read_bytes()
sha=lambda b:hashlib.sha256(b if isinstance(b,bytes) else b.encode()).hexdigest()
def req(ok,why):
    if not ok:raise ValueError(why)
def unique(pairs):
    d={}
    for k,v in pairs:
        req(k not in d,'duplicate JSON key');d[k]=v
    return d
def parse(t):return json.loads(t,object_pairs_hook=unique)
def blob(b,kind=None):
    req(b['sha256']==sha(b['text']) and b['byte_length']==len(b['text'].encode()),'artifact byte binding')
    value=parse(b['text'])
    if kind:
        Draft202012Validator(message['$defs'][kind]).validate(value)
    return value

def receipt(r,kind,content=None):
    req(r['kind']==kind,'receipt kind')
    req(r['home_reference']==r['generation']['home'],'generation home')
    req(int(r['response_receipt_position'])>int(r['dispatch_receipt_floor']),'response before dispatch')
    req(int(r['dispatch_receipt_floor']) < int(r['item_receipt_position']) <= int(r['terminal_receipt_position']),'native receipt order')
    if kind=='file_change':
        req(r['item_type']=='fileChange' and r['phase'] is None and r['supplied_role']=='TASK','writer item/role')
    else:
        req(r['item_type']=='agentMessage' and r['phase']=='final_answer','final agent item')
        roles=['TASK'] if kind=='answer_emission' else ['HELP_HUMAN','WORKING_ITEMS']
        req(r['supplied_role'] in roles,'contribution role')
        req(r['content_sha256']==content,'native content binding')
    refs={x['kind']:x for x in r['sources']}
    req(len(refs)==5 and set(refs)=={'request','result','item_event','terminal_event','role_supply'},'source reference inventory')
    req(all(x['method']==('sha256:role_guidance_utf8' if x['kind']=='role_supply' else 'sha256:host_parsed_frame_json_utf8') for x in r['sources']),'source method')
    req(refs['request']['identity']==r['request_reference'] and refs['role_supply']['identity']==r['role_supply_reference'],'source identity')
    # Every locator/hash remains a recorded claim; this function establishes no authenticity.

def validate(a,base_raw=base_bytes,target_pre=None,target_post=None):
    validator.validate(a)
    req(len(json.dumps(a,ensure_ascii=False,separators=(',',':')).encode())<=1048576,'account byte cap')
    base=parse(base_raw.decode());base_validator.validate(base);base_semantics(base)
    req(a['base_account']['sha256']==sha(base_raw) and a['base_account']['byte_length']==len(base_raw),'base bytes')
    req(a['base_account']['account_id']==base['account_id'] and a['question_id']==base['question']['id'],'base identity/question')
    answer=blob(a['answer']['artifact'],'answer');receipt(a['answer']['receipt'],'answer_emission',a['answer']['artifact']['sha256'])
    expected_gaps={f'/gaps/{i}' for i in range(len(base['gaps']))};expected_conflicts={c['contradiction_id'] for c in base['contradictions']}
    def bindings(body):
        req(body['account_sha256']==a['base_account']['sha256'] and body['question_id']==a['question_id'],'message subject')
        req(set(body['retained_gap_pointers'])==expected_gaps and set(body['retained_contradiction_ids'])==expected_conflicts,'omitted limitations')
    bindings(answer)
    claims={c['claim_id']:c for c in answer['claims']};req(len(claims)==len(answer['claims']),'duplicate answer claim')
    for c in claims.values():
        req(bool(c['base_claim_ids'] or c['fact_ids'] or c['comparison_ids']),'uncited answer claim')
        for key,items,idkey in [('base_claim_ids',base['claims'],'claim_id'),('fact_ids',base['facts'],'fact_id'),('comparison_ids',base['comparisons'],'comparison_id')]:
            req(set(c[key]) <= {x[idkey] for x in items},'unsupported claim reference')
    plan=blob(a['plan'],'plan') if a['plan'] else None
    if plan:
        path=plan['target_path'];req('\0' not in path and not path.startswith('/') and all(p not in ('','..','.') for p in path.split('/')),'literal target')
        req(plan['account_sha256']==a['base_account']['sha256'] and plan['answer_sha256']==a['answer']['artifact']['sha256'],'plan subject')
        req(plan['block_template'].count('{{CCE_REVIEW_SHA256}}')==1,'review substitution count')
        req(plan['block_template'].count(plan['block_marker'])==1,'result marker count')
        req(plan['account_sha256'] in plan['block_template'] and plan['answer_sha256'] in plan['block_template'],'inserted subject refs')
        req(plan['insertion_offset'] <= plan['preimage_length'],'insert offset')
    review=None
    if a['review']:
        review=blob(a['review']['artifact'],'review');bindings(review)
        receipt(a['review']['receipt'],'manager_review_emission',a['review']['artifact']['sha256'])
        req(review['answer_sha256']==a['answer']['artifact']['sha256'],'review exact answer')
        req({f['claim_id'] for f in review['claim_findings']}==set(claims) and len(review['claim_findings'])==len(claims),'review claim coverage')
        x,y=a['answer']['receipt'],a['review']['receipt']
        req((x['home_reference'],x['thread_id'])!=(y['home_reference'],y['thread_id']),'separate manager role conversation')
        req(x['request_reference']!=y['request_reference'],'distinct contribution request')
        if review['disposition']=='reviewed_for_integration':req(plan and review['plan_sha256']==a['plan']['sha256'],'review plan binding')
        else:req(review['plan_sha256'] is None,'nonintegration review plan')
    if a['integration']:
        i=a['integration'];req(review and review['disposition']=='reviewed_for_integration' and plan,'integration prerequisites')
        req(not a['known_conflicts'] and a['integration_attempt'] is None,'conflicting/uncertain integration')
        receipt(i['operation'],'file_change')
        req(i['operation']['request_reference'] not in (a['answer']['receipt']['request_reference'],a['review']['receipt']['request_reference']),'dedicated writer request')
        req(i['target_path']==plan['target_path'] and i['preimage_sha256']==plan['preimage_sha256'],'target binding')
        block=plan['block_template'].replace('{{CCE_REVIEW_SHA256}}',a['review']['artifact']['sha256']).encode()
        req(i['inserted_block_sha256']==sha(block),'review substitution bytes')
        obs={x['kind']:x for x in i['target_observations']}
        req(set(obs)=={'preimage','postimage','reread'} and len({x['identity'] for x in obs.values()})==3,'independent target source inventory')
        for k,o in obs.items():req(o['sha256']==i[k+'_sha256'] and o['file_identity']==i[k+'_identity'],'target source binding')
        req(i['postimage_sha256']==i['reread_sha256'] and i['postimage_identity']==i['reread_identity'],'independent reread differs')
        req(i['observed_postimage_length']==plan['preimage_length']+len(block),'postimage length')
        if target_pre is not None:
            req(sha(target_pre)==plan['preimage_sha256'] and len(target_pre)==plan['preimage_length'],'actual preimage')
            off=plan['insertion_offset'];target_pre[:off].decode();target_pre[off:].decode()
            req(plan['block_marker'].encode() not in target_pre,'section already present')
            expected=target_pre[:off]+block+target_pre[off:]
            req(target_post==expected and sha(expected)==i['postimage_sha256'],'unexpected graph change')
            req(i['prefix_sha256']==sha(target_pre[:off]) and i['suffix_sha256']==sha(target_pre[off:]),'unrelated-byte digest')
    else:req(bool(a['gaps']),'missing integration must remain gap')
    receipts=[a['answer']['receipt']]+([a['review']['receipt']] if a['review'] else [])+([a['integration']['operation']] if a['integration'] else [])
    identities={};positions={};prior={}
    for r in receipts:
        g=tuple(r['generation'][k] for k in ('appSession','home','spawnCounter'))
        if g in prior:req(int(r['dispatch_receipt_floor']) >= prior[g],'causal stage before prior completion')
        prior[g]=max(int(r['terminal_receipt_position']),int(r['response_receipt_position']))
        for source in r['sources']:
            key=(g,source['identity']);value=(source['kind'],source['method'],source['sha256'])
            req(key not in identities or identities[key]==value,'conflicting source identity');identities[key]=value
            field={'item_event':'item_receipt_position','terminal_event':'terminal_receipt_position','result':'response_receipt_position'}.get(source['kind'])
            if field:
                key=(g,r[field]);value=(source['identity'],source['sha256'])
                req(key not in positions or positions[key]==value,'conflicting stream position');positions[key]=value
    return 'cold consistency only; native authorship, scope authorization and write custody NOT established'

checks=0
def expect(a,valid,**kwargs):
    global checks
    try:validate(a,**kwargs)
    except (ValueError,KeyError,ValidationError,UnicodeError) as e:
        if valid:raise AssertionError(str(e)) from e
    else:req(valid,'invalid definition fixture accepted')
    checks+=1

def edit(path,value):
    a=copy.deepcopy(fixture['account']);d=a
    for k in path[:-1]:d=d[k]
    d[path[-1]]=value;return a

def body_edit(which,key,value):
    a=copy.deepcopy(fixture['account']);b=a[which]['artifact'];v=parse(b['text']);v[key]=value;b['text']=json.dumps(v,separators=(',',':'));b['byte_length']=len(b['text'].encode());b['sha256']=sha(b['text']);a[which]['receipt']['content_sha256']=b['sha256'];return a

pre=fixture['target_preimage'].encode();post=fixture['target_postimage'].encode()
expect(fixture['account'],True,target_pre=pre,target_post=post)
expect(fixture['account'],True) # DOES NOT establish actual emission, authorization or writer origin.
for path,value in [
    (['formatVersion'],'0.4'),(['standing'],'accepted'),
    (['base_account','sha256'],'0'*64),(['question_id'],'other'),
    (['answer','receipt','supplied_role'],'WORKING_ITEMS'),
    (['review','receipt','supplied_role'],'TASK'),
    (['answer','receipt','phase'],None),(['answer','receipt','terminal_status'],'interrupted'),
    (['answer','receipt','kind'],'manager_review_emission'),
    (['answer','receipt','item_type'],'fileChange'),
    (['answer','receipt','generation','home'],'foreign'),
    (['answer','receipt','item_receipt_position'],'1'),
    (['answer','receipt','terminal_receipt_position'],'1'),
    (['answer','receipt','sources',0,'resolution_at_write'],'unresolvable'),
    (['answer','receipt','sources',0,'identity'],'forged-request'),
    (['answer','receipt','content_sha256'],'0'*64),
    (['review','artifact','text'],'done'),
    (['integration','operation','kind'],'answer_emission'),
    (['integration','operation','item_type'],'agentMessage'),
    (['integration','target_path'],'elsewhere.md'),
    (['integration','reread_sha256'],'0'*64),
    (['integration','reread_identity','inode'],'999'),
    (['integration','inserted_block_sha256'],'0'*64),
    (['integration','observed_postimage_length'],1),
    (['human_responsibility','standing'],'waived'),
]:expect(edit(path,value),False)
expect(body_edit('answer','account_sha256','0'*64),False)
expect(body_edit('answer','retained_gap_pointers',[]),False)
expect(body_edit('review','answer_sha256','0'*64),False)
expect(body_edit('review','claim_findings',[]),False)
expect(body_edit('review','disposition','changes_requested'),False)
a=edit(['known_conflicts'],[{'reference':'another-review','sha256':'0'*64,'effect':'conflicting disposition'}]);expect(a,False)
a=edit(['integration_attempt'],{'request_reference':'writer','target_path':'workgraph.md','standing':'uncertain','detail':'No success binding'});expect(a,False)
expect(fixture['account'],False,target_pre=pre+b'changed',target_post=post)
expect(fixture['account'],False,target_pre=pre,target_post=post.replace(b'outstanding',b'waived'))
# Exact message bytes matter, not a normalized reserialization or duplicate-key last value.
a=copy.deepcopy(fixture['account']);a['answer']['artifact']['text']=' '+a['answer']['artifact']['text'];expect(a,False)
a=copy.deepcopy(fixture['account']);b=a['answer']['artifact'];b['text']=b['text'][:-1]+',"kind":"answer"}';b['sha256']=sha(b['text']);b['byte_length']=len(b['text'].encode());a['answer']['receipt']['content_sha256']=b['sha256'];expect(a,False)
# Author-only is retained as author-only, never implied integration.
a=copy.deepcopy(fixture['account']);a.update(review=None,plan=None,integration=None);expect(a,True)
# A cold account remains internally valid even with fabricated origin locators: explicit limitation.
a=copy.deepcopy(fixture['account']);a['answer']['receipt']['request_reference']='invented';a['answer']['receipt']['sources'][0]['identity']='invented';expect(a,True)
# After-close persistence is historical recording only; no current source is created.
a=copy.deepcopy(fixture['account'])
for r in [a['answer']['receipt'],a['review']['receipt'],a['integration']['operation']]: r['liveness_at_recording']='historical_after_source_close'
expect(a,True,target_pre=pre,target_post=post)
a['integration']=None;a['integration_attempt']={'request_reference':'original-dispatched-writer','target_path':'workgraph.md','standing':'uncertain','detail':'Source closed before operation mint; actual outcome unknown, not cancelled-nothing'};expect(a,True)
expect(edit(['answer','receipt','sources',0,'method'],'sha256:original_rpc_wire'),False)
expect(edit(['integration','target_observations',2,'identity'],'constructed-target-postimage'),False)
expect(edit(['integration','target_observations',2,'sha256'],'0'*64),False)
expect(edit(['answer','receipt','response_receipt_position'],'1'),False)
# Retained reviewer mutations: invalid owner semantics cannot be repaired by rebinding hashes.
a=copy.deepcopy(fixture['account']);a.update(review=None,plan=None,integration=None)
b=parse(base_bytes.decode());b['facts'][0]['statement']='INVENTED invalid CRR fact';raw=json.dumps(b).encode()
a['base_account'].update(sha256=sha(raw),byte_length=len(raw))
v=parse(a['answer']['artifact']['text']);v['account_sha256']=sha(raw);text=json.dumps(v);a['answer']['artifact'].update(text=text,sha256=sha(text),byte_length=len(text.encode()));a['answer']['receipt']['content_sha256']=sha(text)
expect(a,False,base_raw=raw)
a=copy.deepcopy(fixture['account']);a['review']['receipt']['sources'][2]['identity']=a['answer']['receipt']['sources'][2]['identity'];expect(a,False)
a=copy.deepcopy(fixture['account'])
for key in ('dispatch_receipt_floor','item_receipt_position','terminal_receipt_position','response_receipt_position'):a['review']['receipt'][key]=a['answer']['receipt'][key]
expect(a,False)
a=copy.deepcopy(fixture['account']);a.update(review=None,plan=None,integration=None);a['answer']['receipt']['liveness_at_recording']='historical_after_source_close';expect(a,True)
a=copy.deepcopy(fixture['account']);a['integration']=None
for r in [a['answer']['receipt'],a['review']['receipt']]:r['liveness_at_recording']='historical_after_source_close'
expect(a,True)
print(f'CCE definition consistency cases: {checks} passed; NO native mint/authority/lifecycle implementation qualification')
