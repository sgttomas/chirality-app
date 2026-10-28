#!/usr/bin/env python3
"""Record or verify content digests of the Git-ignored Chirality archives.

The archives live only in the original checkout; worktrees do not carry them.
This tool reads them without modifying anything. `record` writes a digest
file; `verify` recomputes and reports every archive or subtree whose content
changed, appeared, or disappeared.

The repository is public and the archives are deliberately Git-ignored, so the
committed digest file names no file or subtree below an archive location:
subtree digests are keyed by the SHA-256 of the subtree's path. `verify`
recomputes locally and prints the real name of any changed subtree it can
still see. `record --file-list PATH` can additionally write a per-file list to
a local path of your choosing; do not commit that list.

Digest rule: a digest is the SHA-256 of the sorted lines
"<sha256-of-file>\t<size>\t<path-relative-to-archive-root>\n" for every
regular file below it (symlinks contribute "LINK\t<target>\t0\t<path>").
Skipped everywhere: .DS_Store, and directories named node_modules,
__pycache__, .pytest_cache, .next, target.

Usage:
  archive_digests.py record [--root ROOT] [--out FILE] [--file-list LOCAL_TSV]
  archive_digests.py verify [--root ROOT] [--digests FILE]
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.environ.get("CHIRALITY_ARCHIVE_ROOT", "/Users/ryan/ai-env/projects/chirality")
DEFAULT_DIGESTS = os.path.join(HERE, "archive_digests.json")

# (path relative to ROOT, depth of subtree digests below it)
ARCHIVES = [
    (".archive", 2),
    ("domains", 2),
    ("plans/.archive", 1),
    ("plans/evidence/2026-09-19_manual_theory.zip", 0),
    ("projects/chirality-app-dev/.archive", 2),
    ("projects/chirality-app-dev/chirality-app-dev.zip", 0),
    ("projects/chirality-app-dev/execution/_Decomposition/.archive", 0),
    ("projects/chirality-app-dev/frontend/.chirality", 1),
    ("projects/chirality-app-dev/frontend/artifacts", 1),
    ("projects/chirality-app-dev/frontend/dist", 1),
    ("projects/chirality-piping/.archive", 1),
    ("projects/pec/pilot-scratch", 1),
    ("projects/pec/backups", 0),
    ("exports/chirality-app/staging", 1),
    ("_harness_generated", 1),
    ("_DomainEngines/pec", 0),
    ("_DomainEngines/bridge/BRIDGE_2026-06-21_tier0-prep", 0),
    ("workflows/Software_PRD_Workflow_Draft_v1.zip", 0),
    ("skills", 0),
]
SKIP_DIRS = {"node_modules", "__pycache__", ".pytest_cache", ".next", "target"}


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def file_lines(root, rel):
    base = os.path.join(root, rel)
    if not os.path.lexists(base):
        return None
    paths = []
    if os.path.isfile(base) or os.path.islink(base):
        paths = [base]
    else:
        for dp, dns, fns in os.walk(base):
            dns[:] = sorted(d for d in dns if d not in SKIP_DIRS)
            for d in list(dns):
                if os.path.islink(os.path.join(dp, d)):
                    paths.append(os.path.join(dp, d))
            for fn in sorted(fns):
                if fn != ".DS_Store":
                    paths.append(os.path.join(dp, fn))
    out = []
    for fp in sorted(paths):
        r = os.path.relpath(fp, root)
        if os.path.islink(fp):
            out.append(f"LINK\t{os.readlink(fp)}\t0\t{r}")
            continue
        h = hashlib.sha256()
        with open(fp, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        out.append(f"{h.hexdigest()}\t{os.path.getsize(fp)}\t{r}")
    return out


def digest(lines):
    h = hashlib.sha256()
    for ln in sorted(lines):
        h.update((ln + "\n").encode())
    return h.hexdigest()


def path_of(line):
    return line.rsplit("\t", 1)[1]


def size_of(line):
    parts = line.split("\t")
    return int(parts[-2]) if parts[0] != "LINK" else 0


def summarize(root):
    """Return ({location: entry}, {subtree_key: real_name}, all_lines)."""
    result, names, all_lines = {}, {}, []
    for rel, depth in ARCHIVES:
        lines = file_lines(root, rel)
        if lines is None:
            result[rel] = {"missing": True}
            continue
        all_lines.extend(lines)
        entry = {"files": len(lines), "bytes": sum(size_of(l) for l in lines), "digest": digest(lines)}
        if depth:
            groups = {}
            for ln in lines:
                # Group by the file's directory, truncated to `depth` levels below the location.
                dirparts = path_of(ln)[len(rel) + 1:].split("/")[:-1]
                name = "/".join([rel] + dirparts[:depth]) if dirparts else rel + "/(files)"
                groups.setdefault(name, []).append(ln)
            subtrees = {}
            for name, grp in groups.items():
                key = sha(name)
                names[key] = name
                subtrees[key] = {"files": len(grp), "bytes": sum(size_of(l) for l in grp), "digest": digest(grp)}
            entry["subtrees"] = dict(sorted(subtrees.items()))
        result[rel] = entry
    return result, names, all_lines


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["record", "verify"])
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--out", default=DEFAULT_DIGESTS)
    ap.add_argument("--digests", default=DEFAULT_DIGESTS)
    ap.add_argument("--file-list", help="record only: also write a local per-file TSV here (do not commit it)")
    a = ap.parse_args()
    current, names, all_lines = summarize(a.root)
    if a.mode == "record":
        doc = {"schema": "chirality-v4-archive-digests/v2", "root": a.root,
               "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "subtree_keys": "sha256 of the subtree path relative to root",
               "skip_dirs": sorted(SKIP_DIRS), "archives": current}
        with open(a.out, "w") as f:
            json.dump(doc, f, indent=1, sort_keys=True)
            f.write("\n")
        if a.file_list:
            with open(a.file_list, "w") as f:
                f.write("\n".join(sorted(all_lines, key=path_of)) + "\n")
        for rel, e in current.items():
            print(f"{rel}\t{'MISSING' if e.get('missing') else str(e['files']) + ' files'}")
        print(f"total\t{sum(e.get('files', 0) for e in current.values())} files")
        return 0
    with open(a.digests) as f:
        recorded = json.load(f)["archives"]
    changed = 0
    for rel, old in recorded.items():
        new = current.get(rel, {"missing": True})
        if old.get("missing") or new.get("missing"):
            if old.get("missing") != new.get("missing"):
                changed += 1
                print(f"CHANGED {rel}: {'now missing' if new.get('missing') else 'now present'}")
            continue
        if old["digest"] == new["digest"]:
            print(f"OK      {rel} ({new['files']} files)")
            continue
        changed += 1
        print(f"CHANGED {rel}: files {old['files']} -> {new['files']}, bytes {old['bytes']} -> {new['bytes']}")
        osub, nsub = old.get("subtrees", {}), new.get("subtrees", {})
        for k in sorted(set(osub) | set(nsub)):
            o, n = osub.get(k), nsub.get(k)
            if o is None:
                print(f"          subtree added: {names.get(k, k)}")
            elif n is None:
                print(f"          subtree removed (no longer present; key {k[:16]})")
            elif o["digest"] != n["digest"]:
                print(f"          subtree changed: {names.get(k, k)} (files {o['files']} -> {n['files']})")
    print(f"{changed} archive location(s) changed" if changed else "All recorded archives unchanged.")
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
