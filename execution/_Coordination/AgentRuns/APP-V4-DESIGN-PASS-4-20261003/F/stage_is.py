"""Stage an EU-F1 input set for the reader into an empty folder, then verify it. Reads the repo; writes only <dest>.

Usage: python3 -B stage_is.py [--set 2] <empty destination folder>     (default set 1 = IS-FX-RP1-1)
       python3 -B stage_is.py [--set 2] --write-list
The answer key and every other file in F/ are NOT staged.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
SET = "1"
if ARGS[:1] == ["--set"]:
    SET, ARGS = ARGS[1], ARGS[2:]
IS_ID = "IS-FX-RP1-" + SET
V = "" if SET == "1" else ".v2"
D1103 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                      "PKG-11_Adoption and replacement continuity", "1_Working",
                                      "DEL-11-03_Owner replacement evidence packet", "Design"))
SOURCES = {  # staged path -> source path
    "READER_BRIEF%s.md" % V: os.path.join(HERE, "READER_BRIEF%s.md" % V),
    "rp.reader-account%s.schema.json" % V: os.path.join(HERE, "rp.reader-account%s.schema.json" % V),
    "legend/rp.packet-manifest.schema.json": os.path.join(D1103, "rp.packet-manifest.schema.json"),
    "legend/rp.disposition.schema.json": os.path.join(D1103, "rp.disposition.schema.json"),
}
FX = os.path.join(HERE, "fixtures", "FX-RP1" if SET == "1" else "FX-RP1-2")
for root, _, names in os.walk(FX):
    for n in names:
        p = os.path.join(root, n)
        SOURCES[os.path.relpath(p, FX)] = p


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    dest = ARGS[0]
    os.makedirs(dest, exist_ok=True)
    if os.listdir(dest):
        sys.exit("destination is not empty")
    listed = [l.split("  ", 1) for l in open(os.path.join(HERE, IS_ID + ".input-set.sha256"), encoding="utf-8").read().splitlines()]
    for h, rel in listed:
        out = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(out) or dest, exist_ok=True)
        shutil.copyfile(SOURCES[rel], out)
        if sha(out) != h:
            sys.exit("hash mismatch after staging: " + rel)
    shutil.copyfile(os.path.join(HERE, IS_ID + ".input-set.sha256"), os.path.join(dest, IS_ID + ".input-set.sha256"))
    print("staged %d files + the input-set list; all hashes match" % len(listed))


if __name__ == "__main__" and ARGS[:1] == ["--write-list"]:
    lines = sorted("%s  %s" % (sha(p), rel) for rel, p in SOURCES.items())
    with open(os.path.join(HERE, IS_ID + ".input-set.sha256"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sorted(lines, key=lambda s: s.split("  ", 1)[1])) + "\n")
    print("\n".join(sorted(lines, key=lambda s: s.split("  ", 1)[1])))
elif __name__ == "__main__":
    main()
