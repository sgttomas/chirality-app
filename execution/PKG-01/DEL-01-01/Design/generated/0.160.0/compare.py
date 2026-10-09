from pathlib import Path
import json,hashlib,re,subprocess,sys
scratch=Path(sys.argv[1]);h=Path(__file__).resolve().parents[2];old=h/'generated/0.158.0/json-schema/experimental';new=scratch/'json-schema/experimental/run1'
differences=[]
def diff(a,b,p):
 if type(a)!=type(b):differences.append({'path':p,'old':a,'new':b});return
 if isinstance(a,dict):
  for k in sorted(set(a)|set(b)):
   if k not in a: differences.append({'path':p+'/'+k,'kind':'added','new':b[k]})
   elif k not in b:differences.append({'path':p+'/'+k,'kind':'removed','old':a[k]})
   else:diff(a[k],b[k],p+'/'+k)
 elif isinstance(a,list):
  if a!=b:differences.append({'path':p,'old':a,'new':b})
 elif a!=b:differences.append({'path':p,'old':a,'new':b})
for f in old.glob('*.json'):diff(json.loads(f.read_text()),json.loads((new/f.name).read_text()),f.name)
classes=set()
for d in differences:
 p=d['path']
 if 'ThreadItemsListParams/properties/cursor' in p or p.endswith('/ThreadItemsListAnchor') or p.endswith('/ThreadItemsListCursor'): kind='cursor-widening'
 elif 'ListMcpServerStatusParams/properties/serverName' in p: kind='mcp-optional-serverName'
 elif p.endswith('/properties/error/description') and d.get('new')=='Error associated with a failed or interrupted turn.':kind='turn-error-description'
 elif 'tooManyDenials' in str(d.get('new')) and 'CodexErrorInfo' in p:kind='error-enum-tooManyDenials'
 else:kind='UNCLASSIFIED'
 d['class']=kind;classes.add(kind)
assert 'UNCLASSIFIED' not in classes, differences
print('diff classes',classes,'leaves',len(differences))
if 'UNCLASSIFIED' in classes:
 for d in differences:
  if d['class']=='UNCLASSIFIED':print(json.dumps(d)[:900])
# method sets across actual stable/experimental JSON and actual TS.
method_inventory={}
for variant in ['stable','experimental']:
 for category in ['ClientRequest','ClientNotification','ServerRequest','ServerNotification']:
  doc=json.loads((scratch/f'json-schema/{variant}/run1/{category}.json').read_text());methods=[]
  for br in doc.get('oneOf',[]):methods.extend(br.get('properties',{}).get('method',{}).get('enum',[]))
  ts=(scratch/f'ts/{variant}/run1/{category}.ts').read_text();ts_methods=re.findall(r'"method": "([^\"]+)"',ts)
  method_inventory[variant+'/'+category]={'schema':methods,'typescript':ts_methods,'typescriptOnly':sorted(set(ts_methods)-set(methods))}
focus=['ThreadStartParams','ThreadStartResponse','ThreadResumeParams','ThreadResumeResponse','ThreadForkParams','TurnStartParams','TurnStartResponse','LoginAccountParams','GetAccountResponse','ModelListParams','ConfigReadParams','ConfigBatchWriteParams','ModelProviderCapabilitiesReadResponse','ServerRequest','ServerNotification']
unchanged=[];missing=[];focus_changed=[]
old_def=json.loads((old/'codex_app_server_protocol.schemas.json').read_text())['definitions'];new_def=json.loads((new/'codex_app_server_protocol.schemas.json').read_text())['definitions']
for key in focus:
 if key in old_def: a,b=old_def.get(key),new_def.get(key);name=key
 else: a,b=old_def.get('v2',{}).get(key),new_def.get('v2',{}).get(key);name='v2/'+key
 if a is None or b is None:missing.append(name)
 elif a==b:unchanged.append(name)
 else:focus_changed.append(name)
# Validate all redacted recorded wire frames available in committed spike transcripts.
import sys;sys.path.insert(0,str(h/'prototype'));import jsonschema_subset as V
root=json.loads((new/'codex_app_server_protocol.schemas.json').read_text());validated=0;fail=[]
for f in (h/'generated/0.158.0/_spike/transcripts').glob('*.jsonl'):
 for line in f.read_text().splitlines():
  e=json.loads(line)
  if e.get('kind')!='recv':continue
  try:frame=json.loads(e['raw'])
  except (ValueError,KeyError):continue
  if 'method' not in frame:continue
  ref='#/definitions/ServerRequest' if 'id' in frame else '#/definitions/ServerNotification'
  errs=V.validate_against(frame,root,ref)
  if errs:fail.append({'file':f.name,'method':frame['method'],'errors':errs})
  else:validated+=1
inventory=subprocess.check_output(['python3',str(h/'generated/0.158.0/_spike/inventory.py'),str(scratch/'json-schema/stable/run1'),str(scratch/'json-schema/experimental/run1')],text=True)
assert inventory==(h/'generated/0.158.0/_spike/inventory.txt').read_text()
envelope_provenance=[{'file':str(f.relative_to(scratch/'ts/experimental/run1')), 'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted((scratch/'ts/experimental/run1').rglob('*.ts')) if 'emittedAtMs' in f.read_text()]
report={'typescriptEmittedAtMsProvenance':envelope_provenance,'differences':differences,'methodInventory':method_inventory,'unchangedFocusDefinitions':unchanged,'focusNamesNotLocated':missing,'focusChangedUnderReportedDeltas':focus_changed,'legacyRecordedFramesValid':validated,'legacyRecordedFramesFailed':fail,'schemaInventoryByteIdenticalTo0158':True}
(scratch/'comparison.json').write_text(json.dumps(report,indent=2)+'\n');(scratch/'inventory.txt').write_text(inventory)
assert not missing and not focus_changed and not fail
print('focus unchanged',unchanged,'notlocated',missing);print('recorded valid',validated,'failed',len(fail))
