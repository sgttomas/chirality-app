#!/usr/bin/env python3
"""DEL-01-06 PKG-v0.2 design prototype: read a Codex vendor tree (as published,
or as placed inside an App bundle) and print its per-entry identity and the
signature facts of every Mach-O file, as the `codex` part of the package
identity record (PKG §5) carries them.

Reads only. It runs `/usr/bin/codesign -d` (signature display) and hashes
files; it never executes a file from the tree and writes nothing.

    python3 read_tree.py <vendor-tree-dir>                 # per-entry JSON
    python3 read_tree.py <vendor-tree-dir> --manifest      # manifest sha256 (PKG §5.2)
    python3 read_tree.py <vendor-tree-dir> --compare <other-tree-dir>

Every entry is recorded: regular files (sha256, size, mode), symbolic links to
files or directories (target, never followed) and directories (mode). With
--compare it reports, entry by entry, whether the two trees are equal in
content, link targets and modes: the FP-1 check of PKG §7.
"""
import hashlib
import json
import os
import plistlib
import stat
import subprocess
import sys

MACHO_MAGIC = {b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"\xca\xfe\xba\xbe", b"\xce\xfa\xed\xfe"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_macho(path):
    with open(path, "rb") as f:
        return f.read(4) in MACHO_MAGIC


def signature(path):
    out = subprocess.run(["/usr/bin/codesign", "-dv", "--verbose=2", path],
                         capture_output=True, text=True).stderr
    lines = out.splitlines()
    team = next((l.split("=", 1)[1] for l in lines if l.startswith("TeamIdentifier=")), None)
    authority = next((l.split("=", 1)[1] for l in lines if l.startswith("Authority=")), None)
    flags = next((l for l in lines if "flags=" in l), "")
    ts = next((l.split("=", 1)[1] for l in lines if l.startswith("Timestamp=")), None)
    ent = subprocess.run(["/usr/bin/codesign", "-d", "--entitlements", "-", "--xml", path],
                         capture_output=True).stdout
    try:
        ents = sorted(k for k, v in plistlib.loads(ent).items() if v is True) if ent.strip() else []
    except Exception:
        ents = ["<unreadable>"]
    return {"team": team, "authority": authority, "hardened_runtime": "runtime" in flags,
            "timestamp": ts is not None, "entitlements": ents}


def read(root, signatures=True):
    entries = []
    for d, dirs, names in os.walk(root, followlinks=False):
        for n in sorted(dirs + names):
            p = os.path.join(d, n)
            rel = os.path.relpath(p, root)
            st = os.lstat(p)
            mode = oct(stat.S_IMODE(st.st_mode))
            if stat.S_ISLNK(st.st_mode):
                entries.append({"path": rel, "kind": "symlink", "target": os.readlink(p), "mode": mode})
            elif stat.S_ISDIR(st.st_mode):
                entries.append({"path": rel, "kind": "dir", "mode": mode})
            elif stat.S_ISREG(st.st_mode):
                rec = {"path": rel, "kind": "file", "sha256": sha256(p), "size": st.st_size, "mode": mode}
                if signatures and is_macho(p):
                    rec["macho"] = signature(p)
                entries.append(rec)
            else:
                entries.append({"path": rel, "kind": "other", "mode": mode})
    return sorted(entries, key=lambda r: r["path"])


def manifest(entries):
    """PKG §5.2: sha256 over the lines '<sha256>  <relative path>\\n' of every
    regular file, ordered by the relative path's UTF-8 bytes (C collation),
    each line ending with one newline, the last included. This equals
    `find . -type f | sed 's|^./||' | LC_ALL=C sort | xargs shasum -a 256 |
    shasum -a 256` run in the tree."""
    files = sorted((r for r in entries if r["kind"] == "file"), key=lambda r: r["path"].encode("utf-8"))
    return hashlib.sha256(b"".join(f"{r['sha256']}  {r['path']}\n".encode("utf-8") for r in files)).hexdigest()


def key(r):
    return (r["kind"], r.get("sha256"), r.get("target"), r["mode"])


def compare(a, b):
    ma = {r["path"]: r for r in a}
    mb = {r["path"]: r for r in b}
    differing = sorted(p for p in ma.keys() & mb.keys() if key(ma[p]) != key(mb[p]))
    missing = sorted(mb.keys() - ma.keys())
    extra = sorted(ma.keys() - mb.keys())
    return {"equal": not (differing or missing or extra), "differing": differing, "missing": missing, "extra": extra}


def main(argv):
    if len(argv) < 2 or not os.path.isdir(argv[1]):
        print(__doc__)
        return 2
    if "--compare" in argv:
        res = compare(read(argv[1], False), read(argv[argv.index("--compare") + 1], False))
        print(json.dumps(res, indent=1))
        return 0 if res["equal"] else 1
    entries = read(argv[1])
    if "--manifest" in argv:
        print(manifest(entries))
        return 0
    print(json.dumps(entries, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
