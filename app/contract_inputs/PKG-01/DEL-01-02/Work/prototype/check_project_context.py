"""Offline stdlib source/shape controls; no actual private Root or native evidence."""
import json
from pathlib import Path
from project_context import *
import run_cases as C
P=explicit_project("/explicit/App/P","configured App directory")
Q=explicit_project("/explicit/App/Q","opened App directory")
example=json.loads((Path(__file__).resolve().parent.parent/"recovery.app-ledger-entry.example.valid.json").read_text())
# Existing canonical index shape is sourced from the same declared schema; invent observations.
schema=C.SCHEMAS["app-ledger-entry"]
index={"kind":"conversation_index","session":"synthetic","at":"observation","threadId":"native-observed:fixture","home":"H-acct","project":P,"tags":[],"lastObservedExecution":{"state":"loaded-idle","at":"observation"}}
assert not C.V.errors(index,schema)
original=json.dumps(index,sort_keys=True)
for invalid in [None, ""]:
    bad=dict(index,project=invalid)
    assert C.V.errors(bad,schema)  # no nullable/default index successor silently admitted
# Unknown receiver values cannot backfill either historical association or native proof.
for current,relation in [(P,"same"),(Q,"different; no transfer"),(None,"unbound")]:
 result=bind_context(index,"submission:synthetic",current)
 assert result["historicalProject"]==P and result["relation"]==relation
 assert result["indexSnapshot"]["project"]==P
 assert not C.V.errors(result["indexSnapshot"],schema)
 assert decode_context(NIR_OWNER,result["tag"]["value"])==("submission:synthetic",current)
 assert json.dumps(index,sort_keys=True)==original
unknown=bind_context(None,"submission:unknown-history",Q)
assert unknown["historicalProject"] is None and unknown["indexSnapshot"] is None and unknown["currentSubmissionProject"]==Q and unknown["limit"]
for source in ["native cwd","temp fallback","Codex home","native projectId","WR run","renderer assertion"]:
 try:explicit_project(P,source)
 except ValueError:pass
 else:raise AssertionError(source)
for owner,value in [("DEL-02-03",encode_context("submission:x",Q)),(NIR_OWNER,'["submission:x", "Q"]'),(NIR_OWNER,'["submission:x",""]'),(NIR_OWNER,'["native-turn:x","Q"]'),(NIR_OWNER,'["submission:x",null,"extra"]')]:
 try:decode_context(owner,value)
 except (ValueError,TypeError):pass
 else:raise AssertionError(value)
print("PASS known P retained; explicit Q same/different/unbound; unknown no-row/memory-only; exact owner/codec; no inferred default/native/run context")

first=bind_context(index,"submission:fixed",Q)
again=bind_context(first["indexSnapshot"],"submission:fixed",Q)
assert again["idempotent"] and again["indexSnapshot"]==first["indexSnapshot"]
for durable,hot in [(first["indexSnapshot"],()),(None,(first["tag"],))]:
    try:bind_context(durable,"submission:fixed",P,hot)
    except ValueError:pass
    else:raise AssertionError("same submission silently retagged")
conflicting=first["indexSnapshot"].copy()
conflicting["tags"]=[first["tag"],{"owner":NIR_OWNER,"value":encode_context("submission:fixed",P),"seq":2}]
assert resolve_context(conflicting["tags"],"submission:fixed")["status"]=="ambiguous"
legacy=index.copy();legacy["tags"]=[{"owner":NIR_OWNER,"value":"unrecognized historical opaque value","seq":1}]
legacy_result=bind_context(legacy,"submission:new",Q)
assert legacy_result["indexSnapshot"]["tags"][0]==legacy["tags"][0]
print("PASS immutable same-token binding/idempotence; conflicting cold bindings ambiguous; hot unknown tag guarded; unrecognized values preserved")

# Original independent defect: known durable P with absent durable tag plus hot S->Q.
hot=bind_context(None,"submission:hot",Q)["tag"]
try:bind_context(index,"submission:hot",P,(hot,))
except ValueError:pass
else:raise AssertionError("known index ignored hot immutable binding")
same_hot=bind_context(index,"submission:hot",Q,(hot,))
assert same_hot["idempotent"] and same_hot["indexSnapshot"]==index and same_hot["limit"]
contradictory_hot={"owner":NIR_OWNER,"value":encode_context("submission:fixed",P),"seq":7}
try:bind_context(first["indexSnapshot"],"submission:fixed",Q,(contradictory_hot,))
except ValueError:pass
else:raise AssertionError("durable binding masked conflicting hot source")
assert bind_context(first["indexSnapshot"],"submission:fixed",Q,(first["tag"],))["indexSnapshot"]==first["indexSnapshot"]
print("PASS known index plus hot-only binding no-retag; hot/durable disagreement retained; identical repeated source idempotent")
