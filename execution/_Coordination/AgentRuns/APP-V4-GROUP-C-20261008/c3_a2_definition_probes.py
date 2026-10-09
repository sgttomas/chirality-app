import runpy,copy,json,hashlib,sys
from pathlib import Path
r=Path(sys.argv[1]);m=runpy.run_path(str(r/'check_contribution_evidence_v01.py'));validate=m['validate'];fixture=m['fixture']['account'];sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
def rebind(a,key,body):
 t=json.dumps(body,separators=(',',':'),ensure_ascii=False);a[key]['artifact']={'text':t,'sha256':sha(t),'byte_length':len(t.encode())};a[key]['receipt']['content_sha256']=sha(t)
def review_only():
 a=copy.deepcopy(fixture);a['integration']=None;a['plan']=None;b=json.loads(a['review']['artifact']['text']);b['disposition']='cannot_assess';b['plan_sha256']=None;b['review_text']='Cannot assess the answer on this constructed evidence; integration remains outstanding.';rebind(a,'review',b);return a
rows=[]
def check(name,a,expected):
 try:validate(a);actual='accept cold consistency only'
 except Exception as e:actual='reject';reason=('schema refusal' if len(str(e))>500 else str(e).splitlines()[0])
 assert (actual!='reject')==expected,(name,actual)
 rows.append({'case':name,'result':actual,**({'reason':reason} if actual=='reject' else {})})
a=review_only();check('representable nonintegration cannot_assess',a,True)
a=review_only();a['review']=None;check('answer only',a,True)
a=review_only();a['answer']['receipt']['liveness_at_recording']='historical_after_source_close';check('historical answer plus current review recorded shape',a,True)
a=review_only();b=json.loads(a['review']['artifact']['text']);b['disposition']='reviewed_for_integration';rebind(a,'review',b);check('positive integration disposition without plan',a,False)
a=review_only();t=a['answer']['artifact']['text']+' ';a['answer']['artifact'].update(text=t,sha256=sha(t),byte_length=len(t.encode()));a['answer']['receipt']['content_sha256']=sha(t);check('exact answer whitespace changed with stale review',a,False)
a=review_only();b=json.loads(a['answer']['artifact']['text']);b['retained_gap_pointers']=[];rebind(a,'answer',b);check('omitted base gap',a,False)
a=review_only();b=json.loads(a['answer']['artifact']['text']);b['claims'][0]['fact_ids']=['unknown'];rebind(a,'answer',b);check('invented support identity',a,False)
a=review_only();a['review']['receipt']['thread_id']=a['answer']['receipt']['thread_id'];check('same role conversation promoted to manager',a,False)
a=review_only();a['review']['receipt']['request_reference']=a['answer']['receipt']['request_reference'];a['review']['receipt']['sources'][0]['identity']=a['answer']['receipt']['request_reference'];check('same request reused as separate review',a,False)
a=review_only();a['review']['receipt']['sources'][0]['method']='sha256:wire_bytes';check('parsed frame mislabeled wire bytes',a,False)
print(json.dumps({'standing':'Invented cold fixtures only; accepts do not establish emission/capability/lifecycle. No production code modified.','results':rows},indent=2))
