"""Run-specific read-only constructed carrier comparison; no production storage.
python3 compare_c3_r2_carriers.py /path/to/chirality
Uses installed offline definition validators. Writes only stdout JSON.
"""
import contextlib,copy,hashlib,io,json,runpy,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();d=next(root.glob('projects/chirality-app-v4/execution/PKG-07*/1_Working/DEL-07-02*/Design'))
with contextlib.redirect_stdout(io.StringIO()):o=runpy.run_path(str(d/'check_content_review_v02.py'))
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda v:json.dumps(v,ensure_ascii=False,separators=(',',':')).encode('utf-8')
base=o['base_raw'];answer=o['answer_text'].encode();review=o['review_text'].encode()
def corpus_case(name,b=base,a=answer,v=review):
    o['validate'](v.decode(),base_bytes=b,answer=a.decode())
    return name,{'base':b,'answer':a,'review':v}
corpus=[corpus_case('normal')]
for label,space in [('space',b' '),('LF',b'\n')]:
    b=base+space*(1048576-len(base));a=json.loads(answer);a['account_sha256']=sha(b);a=encode(a)
    v=json.loads(review);v.update(account_sha256=sha(b),answer_sha256=sha(a));corpus.append(corpus_case('1MiB_'+label+'_base_rebound',b,a,encode(v)))
for label,char in [('ASCII','x'),('quote','"'),('LF','\n')]:
    v=json.loads(review);v['review_text']=char*65536;corpus.append(corpus_case(label+'_review65536',v=encode(v)))
v=json.loads(review);v['review_text']='\U0001f600'*65536;negative=encode(v);o['new'].validate(v)
try:o['validate'](negative.decode());raise AssertionError('Unicode negative accepted')
except ValueError as e:negative_reason=str(e)
# Illustrative immutable-reference namespace is in-memory only, not a path/store API.
def build(artifacts,mode):
    entries={};pool={}
    for kind,raw in artifacts.items():
        digest=sha(raw);entry={'sha256':digest,'utf8_bytes':len(raw)}
        inline=mode=='inline' or mode=='hybrid_base_reference' and kind!='base'
        if inline:entry['text']=raw.decode('utf-8')
        else:
            key='demo:sha256:'+digest;entry['ref']=key
            assert key not in pool or pool[key]==raw
            pool[key]=raw
        entries[kind]=entry
    return {'demonstration':'exact-artifacts-v1','encoding':mode,'artifacts':entries},pool
checks=[]
def resolve(snapshot,pool,expected):
    assert set(snapshot['artifacts'])==set(expected)
    out={}
    for kind,e in snapshot['artifacts'].items():
        assert set(e) in ({'sha256','utf8_bytes','text'},{'sha256','utf8_bytes','ref'})
        if 'text' in e:raw=e['text'].encode('utf-8')
        else:
            assert e['ref']=='demo:sha256:'+e['sha256'],'mutable/non-content reference'
            assert e['ref'] in pool,'missing immutable artifact'
            raw=pool[e['ref']]
        assert len(raw)==e['utf8_bytes'] and sha(raw)==e['sha256'],'reference bytes rebound'
        assert raw==expected[kind],'changed original subject'
        out[kind]=raw
    return out
def reject(label,fn):
    try:fn()
    except (AssertionError,KeyError,UnicodeError):checks.append(label);return
    raise AssertionError('accepted negative '+label)
rows=[];union_pools={m:{} for m in ['inline','immutable_references','hybrid_base_reference']}
for name,artifacts in corpus:
    for mode in union_pools:
        snapshot,pool=build(artifacts,mode);raw=encode(snapshot)
        assert resolve(json.loads(raw),pool,artifacts)==artifacts;checks.append(name+'/'+mode+'/exact roundtrip')
        retained=sum(map(len,pool.values()));union_pools[mode].update(pool)
        rows.append({'case':name,'encoding':mode,'raw_artifacts':{k:{'sha256':sha(v),'utf8_bytes':len(v)} for k,v in artifacts.items()},'snapshot_utf8_bytes':len(raw),'retained_unique_external_artifact_bytes':retained,'one_current_logical_bytes':len(raw)+retained,'two_identical_slots_shared_artifacts_logical_bytes':2*len(raw)+retained,'external_artifact_count':len(pool)})
        if pool:
            key=next(iter(pool));bad=dict(pool);del bad[key];reject(name+'/'+mode+'/missing',lambda:resolve(snapshot,bad,artifacts))
            bad=dict(pool);bad[key]=bad[key]+b' ';reject(name+'/'+mode+'/rebound bytes',lambda:resolve(snapshot,bad,artifacts))
            bad=copy.deepcopy(snapshot);kind=next(k for k,e in bad['artifacts'].items() if 'ref' in e);bad['artifacts'][kind]['ref']='mutable:slot/current';reject(name+'/'+mode+'/mutable locator',lambda:resolve(bad,pool,artifacts))
            bad=copy.deepcopy(snapshot);foreign=b'{}';digest=sha(foreign);bad['artifacts'][kind]={'sha256':digest,'utf8_bytes':len(foreign),'ref':'demo:sha256:'+digest};foreign_pool=dict(pool);foreign_pool['demo:sha256:'+digest]=foreign;reject(name+'/'+mode+'/selfconsistent changed subject',lambda:resolve(bad,foreign_pool,artifacts))
paths=[d/n for n in ['record_reconstruction_v04.fixture.json','contribution_evidence_v01.fixture.json','contribution_content_review_v02.fixture.json','connector.contribution-message.v0.2.schema.json','connector.contribution-message.v0.1.schema.json','connector.route-account.v0.4.schema.json','connector.route-account.v0.5.schema.json','connector.standing.schema.json','check_content_review_v02.py','check_contribution_evidence_v01.py','check_record_reconstruction_v04.py']]
run=root/'projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-C-20261008'
paths += [run/n for n in ['C3_R2_RESOURCE_ENVELOPE.md','C3_R2_RESOURCE_BASIS.json','C3_S4_RECONSTRUCTION_REVIEW.md','C3_CONTRIBUTION_EVIDENCE_REVIEW.md','C3_CONTENT_REVIEW_BASIS.json']]
rev=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
for p in paths:assert p.read_bytes()==subprocess.check_output(['git','-C',str(root),'show',rev+':'+str(p.relative_to(root))]),'uncommitted source'
result={'standing':'constructed byte comparison only; no production carrier/store/admission/Host custody','source_revision':rev,'script_sha256':sha(Path(__file__).read_bytes()),'sources':[{'path':str(p.relative_to(root)),'sha256':sha(p.read_bytes())} for p in paths],'encoding_definition':{'serializer':'Python json.dumps ensure_ascii=False compact separators UTF8','inline':'all three original texts with per-artifact SHA256/raw UTF8 length','immutable_references':'all three content-addressed demonstration references; original raw bytes counted in external pool','hybrid_base_reference':'fixed base reference; answer/review inline; NOT threshold selection','two_slot':'same snapshot bytes twice with one shared immutable pool; not two distinct real revisions','reference_tests':'in-memory exact bytes only, no actual filesystem/immutable store or provenance enforcement'},'rows':rows,'corpus_unique_external_bytes':{m:sum(map(len,p.values())) for m,p in union_pools.items()},'source_review_context':{'base0.4':'C3_S4_RECONSTRUCTION_REVIEW: source-only READY; no runtime/native/performed-duty implication','answer_CCE':'C3_CONTRIBUTION_EVIDENCE_REVIEW: reviewable proposal READY, implementation held at its exact candidate','message0.2':'C3_CONTENT_REVIEW_BASIS: independently reviewed message proposal,23 definition cases, no adopted durable carrier or observed emission','this_comparison':'author-run constructed checks; independent review not claimed'},'negative_excluded':{'case':'four_byteUnicode_review65536','schema_valid':True,'whole_message_utf8_bytes':len(negative),'artifact_cap':262144,'owner_validator_refusal':negative_reason},'checks':{'count':len(checks),'cases':checks},'omitted_costs':['descriptor and control','admission/reservation and shared quota','temporary/orphan/uncertain artifacts','terminal markers and identity retention','reference wrapper filesystem metadata','actual Host critical evidence','all allocation/RSS/physical disk/runtime latency'],'missing_actual_critical_set':['original Host input/role/request/response/parsed-event and terminal custody with generation/positions','actual answer and content-review emissions (fixtures only)','selected scope/treatment and controlled writer/adapter, real target pre/post/reread and original attempts','adopted combined carrier, actual immutable-store lifetime/retirement/resolution','real producer workload and independent complete critical-set review'],'limits':['references move bytes; do not make them free','logical totals only; not heap or disk measurements','source checks prove constructed consistency not authenticity','no N/S/D/T/Q, cap, threshold or product envelope selected']}
print(json.dumps(result,indent=2,ensure_ascii=False))
