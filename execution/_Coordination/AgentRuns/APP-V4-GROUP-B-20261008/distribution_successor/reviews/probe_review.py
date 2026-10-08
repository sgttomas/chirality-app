"""Independent synthetic review probes; no supplier/native execution."""
import copy
import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import model
import test_model

def reject(fn):
    try:
        fn()
    except Exception:
        return True
    return False

results={}
with tempfile.TemporaryDirectory() as tmp:
    d=Path(tmp)
    o,l,p,trust,put=test_model.fixtures(d)
    results['fixture_valid']=model.lifecycle(l,d,trust)=='verified'
    results['untrusted_selection_refuses_verified']=reject(lambda:model.observed(o,d,'0'*64))
    q=copy.deepcopy(p);q['legacy_package']['app']['build_identity']='another build'
    results['foreign_build_refused']=reject(lambda:model.package(q,d,trust))
    q=copy.deepcopy(p);q.update(expected_reference=None,adoption_attestation=None,verification_artifact=None,distribution_status='unverifiable')
    results['pending_reference_representable']=model.package(q,d,None)=='unverifiable'
    dev=copy.deepcopy(o);dev.update(expected_reference=None,adoption_attestation=None,outcome='unverifiable')
    dl=copy.deepcopy(l)
    dl['legacy_event'].update(transitionId='LT-24',event='development-start-authorized',supplierStanding='unverified-development',reason='U-06 development run: unverified distribution, not the pinned supplier',verificationResult={'result':'unverifiable','reason':'reference unavailable'})
    dl['verification_artifact']=put('development.json',dev)
    results['lt24_unverifiable_representable']=model.lifecycle(dl,d,None)=='unverifiable'
    missing=copy.deepcopy(dev);missing.update(observed_label=None,raw_version_label=None)
    dl['verification_artifact']=put('no-label.json',missing)
    results['lt24_missing_label_refused']=reject(lambda:model.lifecycle(dl,d,None))
    stale=copy.deepcopy(dev);stale['phase']='pre-probe'
    dl['verification_artifact']=put('pre-probe.json',stale)
    results['lt24_without_pre_spawn_refused']=reject(lambda:model.lifecycle(dl,d,None))
    bad=copy.deepcopy(dev);bad.update(observed_label='9.9.8',raw_version_label='codex-cli 9.9.8',outcome='mismatch')
    dl['verification_artifact']=put('mismatch.json',bad)
    results['lt24_known_mismatch_refused']=reject(lambda:model.lifecycle(dl,d,None))
    original=(d/'expected.json').read_bytes();(d/'expected.json').write_bytes(original+b' ')
    results['exact_byte_tampering_refused']=reject(lambda:model.observed(o,d,trust))
print(json.dumps(results,indent=2))
raise SystemExit(0 if all(results.values()) else 1)
