"""Regenerate/check the pinned Python strip+casefold oracle; offline only."""
import argparse, hashlib, json, platform, sys, unicodedata
from pathlib import Path

def generate():
    whitespace=[]; folding={}; digest=hashlib.sha256()
    for cp in range(0x110000):
        if 0xD800 <= cp <= 0xDFFF: continue
        c=chr(cp)
        if c.isspace(): whitespace.append(c)
        if c.casefold()!=c: folding[c]=c.casefold()
        normalized=c.strip().casefold().encode("utf-8")
        digest.update(cp.to_bytes(4,"big")); digest.update(len(normalized).to_bytes(4,"big")); digest.update(normalized)
    mixed=["Straße", " STRASSE\u001c", "\u001cAlice\u001f", "\tALICE ", "İ", "i\u0307", "Σςσ", "\u2003ΣΣΣ\u2003", "ﬃ", "FFI", "", " \t\u001e", "distinct reviewer", "Author"]
    return {"format":"python-string-identity.s3", "algorithm":"python-strip-casefold-scalar-v1", "pythonImplementation":platform.python_implementation(), "pythonVersion":sys.version, "unicodeVersion":unicodedata.unidata_version, "interpreterSha256":hashlib.sha256(Path(sys.executable).resolve().read_bytes()).hexdigest(), "generatorSha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "domain":"Unicode scalar values; JSON non-scalar surrogates rejected", "whitespace":whitespace, "casefold":folding, "oracle":{"scalarSha256":digest.hexdigest(), "mixed":[[s,s.strip().casefold()] for s in mixed]}}

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); args=parser.parse_args()
    target=Path(__file__).with_name("python-string-identity.s3.json")
    raw=(json.dumps(generate(),ensure_ascii=True,sort_keys=True,indent=2)+"\n").encode()
    if args.check:
        if target.read_bytes()!=raw: raise SystemExit("pinned interpreter/table/oracle drift")
        print("PASS: every Unicode scalar + mixed-string Python oracle; exact generator/interpreter/table reproduction")
    else: target.write_bytes(raw)
