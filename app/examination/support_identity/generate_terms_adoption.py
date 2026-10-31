#!/usr/bin/env python3
"""Re-derive only the approved terms successor cohort; never refresh other pins."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
E = 'app/examination/'
D = 'execution/PKG-09/DEL-09-01/Design/support-identity-v1/'
OLD = '5312e36e02749cd3397dc8aa71385a1f6705833528afcd7bb76039e5bdd951f1'
NEW = '151f43890c48b986bec5382a675e054f7d05821a65aeab2e216c22d149f1a7c4'
RENAMES = {
 E+'standalone/sources.json': E+'standalone/sources.terms-v1.json',
 E+'native_forms/sources.json': E+'native_forms/sources.terms-v1.json',
 E+'support_identity/canonical-pins.v1.json': E+'support_identity/canonical-pins.terms-v1.json',
 E+'standalone/pre_run_inputs.pins.json': E+'standalone/pre_run_inputs.terms-v1.pins.json',
 E+'native_forms/pre_run_form.pins.json': E+'native_forms/pre_run_form.terms-v1.pins.json',
 E+'sq_receiving/pins.json': E+'sq_receiving/pins.terms-v1.json',
 D+'binding.schema.json': D+'binding.terms-v1.schema.json',
 D+'documentary-condition.v2.json': D+'documentary-condition.v3.json',
}
CHANGED = {E+p for p in ('standalone/prepare.py','standalone/pre_run_inputs.py',
 'native_forms/native_form.py','native_forms/pre_run_form.py','support_identity/canonical.py')}
PACKAGING = 'execution/PKG-01/DEL-01-06/Design/PACKAGING_AND_DISTRIBUTION.md'


def raw(path):
    return (ROOT / path.replace('/Design/', '/Work/')).read_bytes()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(raw(path))


def write(path, value):
    (ROOT / path.replace('/Design/', '/Work/')).write_text(json.dumps(value, indent=2)+'\n')


def constant(path, digest):
    p=ROOT/path
    text=p.read_text()
    text,count=re.subn(r"PINS_SHA256 = '[0-9a-f]{64}'", "PINS_SHA256 = '"+digest+"'", text)
    assert count == 1
    p.write_text(text)


def source(path, value):
    if isinstance(value, dict):
        result=copy.deepcopy(value)
        if path == PACKAGING:
            assert result['sha256'] == OLD
            result['sha256'] = NEW
        return result
    if path in RENAMES or path in CHANGED:
        return sha(raw(RENAMES.get(path,path)))
    # Deliberately retain original frozen documentary and unrelated reader pins.
    return value


def pins(old, reader, schema=False):
    value=read(old)
    value['format']=value.get('format', 'sq-receiving-pins')+'-terms-successor-1'
    value['documentary_selection']={'method':'selected-documentary-source-condition/v3-terms',
                                  'manifest':D+'documentary-condition.v3.json',
                                  'sha256':sha(raw(D+'documentary-condition.v3.json'))}
    for key in ('schema',):
        if key in value: value[key]=RENAMES.get(value[key],value[key])
    value['sources']={RENAMES.get(path,path):source(path,digest) for path,digest in value['sources'].items()}
    if schema:
        value['sources'][E+'support_identity/terms_condition.py']=sha(raw(E+'support_identity/terms_condition.py'))
    write(RENAMES[old],value)
    constant(reader,sha(raw(RENAMES[old])))


def main():
    spec=importlib.util.spec_from_file_location('projection',ROOT/E/'documentary_condition.py')
    projection=importlib.util.module_from_spec(spec);spec.loader.exec_module(projection)
    old=read(D+'documentary-condition.v2.json');new=read(D+'documentary-condition.v3.json')
    assert old['sources'] != new['sources']
    for before,after in zip(old['sources'],new['sources'],strict=True):
        expected=copy.deepcopy(before)
        if before['path']==PACKAGING:
            assert before['sha256']==OLD
            expected['sha256']=NEW
        assert after==expected, 'unexpected documentary adoption'
        assert sha(projection.project(raw(after['path']),after['selectors']))==after['sha256'], after['path']
    for path,digest in new['terms_adoption']['artifacts'].items():
        assert sha(raw(path))==digest, 'approved terms input changed: '+path
    old=E+'standalone/sources.json';value=read(old)
    value['documentary_selection']={'method':new['method'],'manifest_sha256':sha(raw(D+'documentary-condition.v3.json'))}
    for item in value['sources']:
        if item['path']==PACKAGING:
            assert item['sha256']=='sha256:'+OLD
            item['sha256']='sha256:'+NEW
            # Original basis_file_sha256 remains the historical source identity.
        elif item['path'] in RENAMES:
            item['path'] = RENAMES[item['path']]
            item['sha256'] = 'sha256:' + sha(raw(item['path']))
    write(RENAMES[old],value)
    old=E+'native_forms/sources.json';value=read(old)
    for item in value['sources']:
        path=item['path'];item['sha256']=source(path,item['sha256']);item['path']=RENAMES.get(path,path)
    write(RENAMES[old],value)
    pins(E+'support_identity/canonical-pins.v1.json',E+'support_identity/canonical.py',True)
    pins(E+'standalone/pre_run_inputs.pins.json',E+'standalone/pre_run_inputs.py',True)
    pins(E+'native_forms/pre_run_form.pins.json',E+'native_forms/pre_run_form.py')
    pins(E+'sq_receiving/pins.json',E+'sq_receiving/receive.py',True)

if __name__=='__main__':main()
