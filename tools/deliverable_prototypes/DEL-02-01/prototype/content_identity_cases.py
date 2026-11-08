#!/usr/bin/env python3
"""CC-CONTENT-IDENTITY narrow App package method checks; offline temp fixtures only."""
from pathlib import Path
import hashlib
import tempfile
import os
import shutil
import wdproto


def main():
    with tempfile.TemporaryDirectory(prefix="chirality-content-id-") as tmp:
        pkg = Path(tmp) / "package"
        pkg.mkdir()
        (pkg / "WORKFLOW.md").write_bytes(b"workflow\n")
        (pkg / "resource.bin").write_bytes(b"\0\xff")
        expected_stream = (b"chirality.app.workflow-package.sha256/v1\0" + (2).to_bytes(8, "big")
                           + (11).to_bytes(8, "big") + b"WORKFLOW.md" + (9).to_bytes(8, "big") + b"workflow\n"
                           + (12).to_bytes(8, "big") + b"resource.bin" + (2).to_bytes(8, "big") + b"\0\xff")
        base = wdproto.revision(pkg)
        assert base["value"] == hashlib.sha256(expected_stream).hexdigest()
        assert base["method"] == "chirality.app.workflow-package.sha256/v1"
        assert [m["path"] for m in base["manifest"]] == ["WORKFLOW.md", "resource.bin"]
        (pkg / "empty").mkdir()
        assert wdproto.revision(pkg) == base
        clone = Path(tmp) / "clone"
        shutil.copytree(pkg, clone)
        assert wdproto.revision(clone) == base
        (pkg / "WORKFLOW.md").write_bytes(b"workflow\r\n")
        assert wdproto.revision(pkg)["value"] != base["value"]
        (pkg / "WORKFLOW.md").write_bytes(b"workflow\n")
        (pkg / ".DS_Store").write_bytes(b"system bytes are included")
        assert wdproto.revision(pkg)["value"] != base["value"]
        (pkg / ".DS_Store").unlink()
        (pkg / "resource.bin").rename(pkg / "resource\n.bin")
        assert wdproto.revision(pkg)["value"] != base["value"]
        (pkg / "resource\n.bin").rename(pkg / "resource.bin")
        os.symlink(pkg / "resource.bin", pkg / "link")
        assert wdproto.revision(pkg)["status"] == "not_established"
        (pkg / "link").unlink()
        os.symlink(pkg, Path(tmp) / "linked-root")
        assert wdproto.revision(Path(tmp) / "linked-root")["status"] == "not_established"
        os.mkfifo(pkg / "fifo")
        assert wdproto.revision(pkg)["status"] == "not_established"
        (pkg / "fifo").unlink()
        print("PASS package reference framing; all file bytes/binary bytes; empty-directory and relocation invariance; line-ending/system-file/path sensitivity; link/root-link/FIFO refusal")
        print("Package known-vector:", base["value"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
