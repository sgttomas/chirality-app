"""Read-only constructed fixture byte measurements; requires existing offline validators.
Usage: python3 measure_c3_r2_bytes.py /path/to/chirality
No writes, production carrier/heap/disk claims or policy selection.
"""
import contextlib,hashlib,io,json,runpy,subprocess,sys
from pathlib import Path
from jsonschema import Draft202012Validator
root=Path(sys.argv[1]).resolve()
d=next(root.glob('projects/chirality-app-v4/execution/PKG-07*/1_Working/DEL-07-02*/Design'))
with contextlib.redirect_stdout(io.StringIO()):
    owner=runpy.run_path(str(d/'check_content_review_v02.py'))
sha=lambda x:hashlib.sha256(x).hexdigest()
dump=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
base=owner['base_raw'];answer=owner['answer_text'];review=owner['review_text']
owner['validate'](review)
def row(name,text):
    raw=text.encode('utf-8');inline=dump(text).encode('utf-8')
    return {'name':name,'unicode_codepoints':len(text),'raw_utf8_bytes':len(raw),'raw_sha256':sha(raw),'json_string_utf8_bytes':len(inline),'json_string_overhead':len(inline)-len(raw),'object_text_utf8_bytes':len(dump({'text':text}).encode()),'ensure_ascii_true_string_bytes':len(json.dumps(text,ensure_ascii=True,separators=(',',':')).encode())}
rows=[row('base0.4 exact file',base.decode()),row('answer exact artifact text',answer),row('message0.2 positive review exact file',review)]
combined=dump({'base':base.decode(),'answer':answer,'review':review}).encode()
# Whitespace padding is legal JSON and changes exact subject identity.
padded=base+b' '*(1048576-len(base));b=json.loads(padded);owner['old']['base_validator'].validate(b);owner['old']['base_semantics'](b)
a=json.loads(answer);a['account_sha256']=sha(padded);new_answer=dump(a)
v=json.loads(review);v['account_sha256']=sha(padded);v['answer_sha256']=sha(new_answer.encode());new_review=dump(v)
owner['validate'](new_review,base_bytes=padded,answer=new_answer)
rows.append(row('base0.4 padded to1MiB exact bytes',padded.decode()))
padded_lf=base+b'\n'*(1048576-len(base));owner['old']['base_semantics'](json.loads(padded_lf));rows.append(row('base0.4 LF padded to1MiB exact bytes',padded_lf.decode()))
padded_combined=dump({'base':padded.decode(),'answer':new_answer,'review':new_review}).encode()
# Schema string maxLength counts Unicode code points, not serialized bytes.
schema=owner['schema'];bounds=[]
def walk(x,path='$'):
    if isinstance(x,dict):
        for k,v in x.items():
            if k in ('maxLength','maxItems'):bounds.append({'path':path+'/'+k,'value':v})
            walk(v,path+'/'+k)
    elif isinstance(x,list):
        for i,v in enumerate(x):walk(v,path+'/'+str(i))
walk(schema)
stress=[]
for label,char in [('ascii','x'),('quote','"'),('LF','\n'),('four_byte_unicode','\U0001f600')]:
    v=json.loads(review);v['review_text']=char*65536;text=dump(v)
    Draft202012Validator(schema).validate(v)
    try:owner['validate'](text);accepted=True;reason=None
    except ValueError as e:accepted=False;reason=str(e)
    stress.append({'case':label,'review_text_codepoints':len(v['review_text']),'review_text_raw_utf8_bytes':len(v['review_text'].encode()),'schema_valid':True,'whole_message_utf8_bytes':len(text.encode()),'whole_message_inline_string_bytes':len(dump(text).encode()),'owner_message_validator_accepts':accepted,'refusal':reason})
paths=['record_reconstruction_v04.fixture.json','contribution_evidence_v01.fixture.json','contribution_content_review_v02.fixture.json','connector.contribution-message.v0.2.schema.json','connector.contribution-message.v0.1.schema.json','connector.route-account.v0.4.schema.json','connector.route-account.v0.5.schema.json','connector.standing.schema.json','check_content_review_v02.py','check_contribution_evidence_v01.py','check_record_reconstruction_v04.py']
revision=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
for n in paths:
    committed=subprocess.check_output(['git','-C',str(root),'show',revision+':'+str((d/n).relative_to(root))])
    assert committed==(d/n).read_bytes(), 'Source differs from committed basis: '+n
result={'script_sha256':sha(Path(__file__).read_bytes()),'standing':'constructed definition fixtures only; no production carrier, allocation, physical disk or Host evidence','source_revision':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),'sources':[{'path':str((d/n).relative_to(root)),'sha256':sha((d/n).read_bytes())} for n in paths],'rows':rows,'illustrative_three_string_envelope':{'normal_bytes':len(combined),'padded_base_bytes':len(padded_combined),'padded_exceeds1MiB_by':len(padded_combined)-1048576,'meaning':'illustrative compact JSON object, NOT selected carrier; exact bytes retained, not parsed-and-normalized'},'padded_base':{'schema_and_owner_semantics_valid':True,'bytes':len(padded),'padding_bytes':len(padded)-len(base),'new_answer_review_bindings_valid':True,'meaning':'constructed hash rebinding only; no new authorship/review performance; original bindings would be stale'},'schema_bounds':bounds,'stress_rows':stress,'limits':{'message_artifact_utf8_cap':262144,'current_account_serialized_cap':1048576,'measurement':'Python UTF8 compact ensure_ascii=False except explicitly labeled alternative; no heap/disk multiplier inferred'}}
print(json.dumps(result,indent=2,ensure_ascii=False))
