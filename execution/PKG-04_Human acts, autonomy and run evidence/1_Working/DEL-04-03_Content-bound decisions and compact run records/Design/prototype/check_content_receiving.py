"""CC-CONTENT-RX: local consumer conformance, not product/atomic-snapshot evidence."""
import copy, importlib.util, json, os, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
WD = next(ROOT.glob("PKG-02*/1_Working/DEL-02-01*/Design/prototype/wdproto.py"))
ROLE = next(ROOT.glob("PKG-02*/1_Working/DEL-02-04*/Design/prototype/role_supply.py"))
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec); spec.loader.exec_module(out); return out
wd = module("rx_wd", WD); role = module("rx_role", ROLE)
from exec_to_rs import load_registry
from record_store import Reader, Writer, RS_ID
from minischema import validate
reg = load_registry()
with tempfile.TemporaryDirectory(prefix="cc-content-rx-") as temp:
    package = Path(temp)/"package"; package.mkdir()
    (package/"WORKFLOW.md").write_bytes(b"workflow\n")
    (package/"resource.bin").write_bytes(b"\x00\xff")
    revision = wd.revision(str(package))
    assert revision["method"] == "chirality.app.workflow-package.sha256/v1"
    assert revision["value"] == "0c8db7f93e14aa8b667df62e56d4f7de4e3d0eae64e80112a1f519a8d26d7767"
    exact = role.cid(b"abc")
    assert exact == {"method": "chirality.app.exact-bytes.sha256/v1", "value": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}
    assert role.cid(b"a\r\n") != role.cid(b"a\n")
    package_content = {k: revision[k] for k in ("method", "value")}
    old = [json.loads(l) for l in (HERE.parent/"RS_RECORD.valid.act-log.example.jsonl").read_text().splitlines()]
    a15 = copy.deepcopy(old[0]["body"])
    a15["boundContent"] = [package_content]
    a15["relations"]["reviewedDraft"]["content"] = copy.deepcopy(package_content)
    a4 = copy.deepcopy(old[1]["body"]); a4["boundContent"] = [exact]
    log = Path(temp)/"acts.jsonl"
    writer = Writer(str(log), reg, {"role": "App interface (capturing surface)", "identity": "writer:rx"}, {"surface": "App"})
    writer.append("human_act", a15, "rec:rx:a15")
    writer.append("human_act", a4, "rec:rx:file")
    read = Reader(reg).read_log(str(log))
    assert not read["nonconformant"] and read["entries"][0]["body"]["boundContent"] == [package_content]
    assert read["entries"][1]["body"]["boundContent"] == [exact]
    # New selected method cannot silently rewrite historical reviewed content.
    mismatched = copy.deepcopy(a15); mismatched["relations"]["reviewedDraft"]["content"] = old[0]["body"]["boundContent"][0]
    badlog = Path(temp)/"mismatch.jsonl"
    Writer(str(badlog), reg, {"role": "App interface (capturing surface)", "identity": "writer:bad"}, {"surface": "App"}).append("human_act", mismatched, "rec:rx:bad")
    assert Reader(reg).view([Reader(reg).read_log(str(badlog))])["nonconformant"]
    # EXEC/RS tuple spelling seam retains revision method and derived source unchanged.
    source = {"kind": "workflow", "origin": "project", "sourceRoot": "root:test", "name": "fixture", "revision": revision["value"], "revisionMethod": revision["method"],
              "derivedFrom": {"kind": "workflow", "origin": "host", "sourceRoot": "host:test", "name": "original", "revision": "opaque:legacy", "revisionMethod": "host:original-method"}}
    assert not validate(source, {"$ref": RS_ID+"#/$defs/workflowTuple"}, reg)
    assert source["derivedFrom"]["revisionMethod"] == "host:original-method"
    # A summary cannot narrow the package to WORKFLOW.md: the binary resource matters.
    (package/"resource.bin").write_bytes(b"\x00\xfe")
    assert wd.revision(str(package))["value"] != revision["value"]
print("PASS selected App file/A15 method roundtrip; historical-method mismatch rejected; full package/derived host tuple preserved")
