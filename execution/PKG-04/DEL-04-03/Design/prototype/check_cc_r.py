import json
from pathlib import Path
from referencing import Registry,Resource
from jsonschema import Draft202012Validator
b=Path(__file__).resolve().parents[4];r=next(b.glob('PKG-04*/DEL-04-03*'))/'Design';e=next(b.glob('PKG-02*/DEL-02-03*'))/'Design'
paths=[r/'RS_RECORD.schema.json',e/'checkpoint-record-entries.schema.json',next(b.glob('PKG-04*/DEL-04-01*/Design/ACT_POLICY_CLASS_RECORD.schema.json')),next(b.glob('PKG-04*/DEL-04-02*/Design/AS_SETTINGS_IN.schema.json'))]
reg=Registry();schemas={}
for p in paths:
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s);schemas[p.name]=s;reg=reg.with_resource(s['$id'],Resource.from_contents(s))
v=Draft202012Validator(schemas['RS_RECORD.schema.json'],registry=reg);n=0
for p in r.glob('RS_RECORD.valid.*.jsonl'):
 for line in p.read_text().splitlines():v.validate(json.loads(line));n+=1
invalid=json.loads((r/'RS_RECORD.invalid.examples.json').read_text())
for row in invalid:assert list(v.iter_errors(row.get('instance',row))),row.get('case')
print('Standard validator by declared IDs only:',n,'valid RS entries;',len(invalid),'invalid entries rejected')
exec_s=schemas['checkpoint-record-entries.schema.json']
def subval(name,value):Draft202012Validator({'$ref':exec_s['$id']+'#/$defs/'+name},registry=reg).validate(value)
pkg=json.loads((e/'decision-package-file.example.valid.json').read_text());del pkg['scope'];subval('decisionPackageFile',pkg);print('CI4 unchanged: omitted scope remains valid; owner-selected explicit absence label at capture')
req=json.loads((e/'checkpoint-record-entries.example.decision-package.valid.json').read_text())[0]['body'];assert req['requester']=={'kind':'agent'};subval('actRequest',req)
req['requester']={'kind':'agent','identity':'thread:test-observed-writer','evidence':{'kind':'conversation item','ref':'item:test-write-matching-path-and-bytes','resolutionAtWrite':'resolved'}};subval('actRequest',req);print('CI3 absent requester identity and sourced identity shapes validate (test values only)')
entry=json.loads(next(r.glob('RS_RECORD.valid.*.jsonl')).read_text().splitlines()[0]);entry['kind']='evidence_limit';entry['body']={'label':'requester identity not established','subjectRef':'rec:test:request','detail':'package file observed; writer of the identified bytes not observed'};v.validate(entry);print('CI3 requester-identity limit validates')

# Verify handoff independently from source-record mapping; package bytes stay intact.
import importlib.util, sys
sys.path.insert(0, str(e / "prototype"))
spec = importlib.util.spec_from_file_location("cc_r_exec", e / "prototype/run_all.py")
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
for scope, expected in [(None, "not named by the package"), ("", "not named by the package"), ("named scope", "named scope")]:
    package = ex.package_file()
    if scope is None: package.pop("scope", None)
    else: package["scope"] = scope
    before = json.dumps(package, sort_keys=True)
    assert ex.decision_scope_for_capture(package) == expected
    request = ex.request_from_file(package, "project/decisions/test.json", "test:bytes", {"kind": "agent"}, "T-test")
    assert ("scope" in request) == ("scope" in package)
    if scope is not None: assert request["scope"] == scope
    assert json.dumps(package, sort_keys=True) == before
print("CI4 absent/empty/present capture scope and unchanged source-record mapping hold")
