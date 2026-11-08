"""Proposed message-only definition checks; no native mint, carrier adoption or authority."""
import copy,hashlib,json,runpy,contextlib,io
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError
ROOT=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    old=runpy.run_path(str(ROOT/'check_contribution_evidence_v01.py'))
parse=old['parse'];sha=old['sha'];req=old['req'];base_raw=old['base_bytes']
schema=json.loads((ROOT/'connector.contribution-message.v0.2.schema.json').read_text())
Draft202012Validator.check_schema(schema);new=Draft202012Validator(schema)
old_message=Draft202012Validator(old['message'])
answer_text=old['fixture']['account']['answer']['artifact']['text']
review_text=(ROOT/'contribution_content_review_v02.fixture.json').read_text()
def validate(text,base_bytes=base_raw,answer=answer_text,plan=None):
    req(len(text.encode('utf-8'))<=262144,'message byte bound')
    v=parse(text);new.validate(v)
    req(v['kind']=='manager_review' and v['disposition']=='reviewed_content_only','content-only kind')
    req(plan is None and v['plan_sha256'] is None,'no plan or automatic promotion')
    b=parse(base_bytes.decode());old['base_validator'].validate(b);old['base_semantics'](b)
    a=parse(answer);Draft202012Validator(old['message']['$defs']['answer']).validate(a)
    req(a['account_sha256']==sha(base_bytes) and a['question_id']==b['question']['id'],'answer subject')
    req(v['account_sha256']==sha(base_bytes) and v['question_id']==b['question']['id'],'review subject')
    req(v['answer_sha256']==sha(answer),'exact answer bytes')
    gaps={f'/gaps/{i}' for i in range(len(b['gaps']))};conflicts={x['contradiction_id'] for x in b['contradictions']}
    for body in (a,v):req(set(body['retained_gap_pointers'])==gaps and set(body['retained_contradiction_ids'])==conflicts,'carried limitations')
    claims={c['claim_id']:c for c in a['claims']};req(len(claims)==len(a['claims']),'unique answer claims')
    for c in claims.values():
        req(bool(c['base_claim_ids'] or c['fact_ids'] or c['comparison_ids']),'uncited answer claim')
        for key,collection,identity in [('base_claim_ids','claims','claim_id'),('fact_ids','facts','fact_id'),('comparison_ids','comparisons','comparison_id')]:
            req(set(c[key]) <= {x[identity] for x in b[collection]},'unknown support')
    ids=[x['claim_id'] for x in v['claim_findings']]
    req(len(ids)==len(set(ids)) and set(ids)==set(claims),'exact finding coverage')
    return v

def dumped(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
checks=[]
def reject(name,fn):
    try:fn()
    except (ValueError,ValidationError):checks.append(name);return
    raise AssertionError('accepted negative: '+name)
v=validate(review_text);checks.append('valid constructed content-only message')
reject('old message0.1 refuses new enum',lambda:old_message.validate(v))
for name,mut in [
 ('fake plan',lambda x:x.update(plan_sha256='a'*64)),
 ('changed answer hash',lambda x:x.update(answer_sha256='a'*64)),
 ('wrong base',lambda x:x.update(account_sha256='a'*64)),
 ('wrong question',lambda x:x.update(question_id='other')),
 ('omitted gap',lambda x:x.update(retained_gap_pointers=[])),
 ('unknown contradiction',lambda x:x.update(retained_contradiction_ids=['unknown'])),
 ('missing finding',lambda x:x.update(claim_findings=[])),
 ('extra finding',lambda x:x['claim_findings'].append({'claim_id':'unknown','finding':'unrelated'})),
 ('duplicate claim finding',lambda x:x['claim_findings'].append({'claim_id':x['claim_findings'][0]['claim_id'],'finding':'different prose same ID'})),
 ('cannot_assess substitution',lambda x:x.update(disposition='cannot_assess')),
 ('integration promotion',lambda x:x.update(disposition='reviewed_for_integration')),
 ('human act field',lambda x:x.update(accepted_by_person=True)),
 ('grant field',lambda x:x.update(direct_grant=True)),
]:
 x=copy.deepcopy(v);mut(x);reject(name,lambda x=x:validate(dumped(x)))
reject('answer whitespace changes exact binding',lambda:validate(review_text,answer=answer_text+' '))
reject('later plan cannot promote existing review',lambda:validate(review_text,plan={'sha256':'a'*64}))
reject('duplicate JSON keys',lambda:validate(review_text.strip()[:-1]+',"kind":"manager_review"}'))
a=parse(answer_text);a['claims'][0]['fact_ids']=['unknown'];x=copy.deepcopy(v);x['answer_sha256']=sha(dumped(a));reject('unknown support despite matching revised answer hash',lambda:validate(dumped(x),answer=dumped(a)))
# Old account embeds opaque message text; demonstrate shape acceptance is NOT semantic compatibility.
account=copy.deepcopy(old['fixture']['account']);account['integration']=None;account['plan']=None
account['review']['artifact']={'text':review_text,'sha256':sha(review_text),'byte_length':len(review_text.encode())}
account['review']['receipt']['content_sha256']=sha(review_text)
old['validator'].validate(account);checks.append('old account shape alone accepts opaque text: not compatibility')
reject('old account semantic reader refuses new meaning',lambda:old['validate'](account))
# Legacy payloads keep their existing meaning under the separate successor schema.
for kind in ('answer','review'):
    new.validate(parse(old['fixture']['account'][kind]['artifact']['text']));checks.append('legacy '+kind+' shape supported in new schema')
print(json.dumps({'standing':'definition-only; no actual manager emission, authority or adopted carrier','count':len(checks),'checks':checks},indent=2))
