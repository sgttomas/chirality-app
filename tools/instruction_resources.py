"""Derive the packaged App instruction tree from DEL-02-04 Work, offline.

Run ``python3 -m tools.instruction_resources`` after an authorized source edit;
``--check`` verifies the exact bytes, modes, file set and derivation manifest.
This does not revise historical bindings or establish adoption/qualification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

SOURCE = Path("execution/PKG-02/DEL-02-04/Work/instructions-v1")
OUTPUT = Path("app/src-tauri/resources/instructions")
DERIVATION = SOURCE.parent / "INSTRUCTION_RESOURCE_DERIVATION.json"
FILES = (
    "AGENTS.md", "ROLE_SET_SOURCE_BINDING.json", "SOURCE_MAP.json",
    "agents/AGENT_HELPS_HUMANS.md", "agents/AGENT_HELP_HUMAN.md",
    "agents/AGENT_TASK.md", "agents/AGENT_WORKING_ITEMS.md", "roles.json",
)
DIRECTORIES = ("", "agents")
MODE = 0o644
DIRECTORY_MODE = 0o755
IMPORT_REVISION = "f10e5c305f58e1c7abcf462f9c3518e35c7b6eec"


def plain_ancestry(path: Path) -> None:
    """Never traverse a symlink or non-directory ancestor for reads/writes."""
    for parent in reversed((path, *path.parents)):
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise ValueError(f"Not a plain directory: {parent}")


def file_bytes(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ValueError(f"Not an unaliased regular file: {path}")
        raw = stream.read()
        after = os.fstat(stream.fileno())
        if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
            after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns
        ):
            raise ValueError(f"File changed while reading: {path}")
        return raw


def tree(root: Path, *, missing: bool = False) -> dict[str, bytes]:
    plain_ancestry(root)
    if not root.exists():
        if missing:
            return {}
        raise ValueError(f"Instruction source missing: {root}")
    actual = {}
    def visit(folder: Path, relative: str) -> None:
        if stat.S_IMODE(folder.stat().st_mode) != DIRECTORY_MODE:
            raise ValueError(f"Instruction directory mode differs: {folder}")
        for item in sorted(folder.iterdir()):
            name = relative + item.name
            meta = item.lstat()
            if stat.S_ISDIR(meta.st_mode) and name in DIRECTORIES:
                visit(item, name + "/")
            elif stat.S_ISREG(meta.st_mode) and name in FILES:
                if stat.S_IMODE(meta.st_mode) != MODE:
                    raise ValueError(f"Instruction file mode differs: {item}")
                actual[name] = file_bytes(item)
            else:
                raise ValueError(f"Unexpected instruction entry/type: {item}")
    visit(root, "")
    if not missing and set(actual) != set(FILES):
        raise ValueError(f"Instruction file set differs: {root}")
    return actual


def manifest(source: dict[str, bytes]) -> bytes:
    entries = [{"path": path, "sha256": hashlib.sha256(source[path]).hexdigest(),
                "byteLength": len(source[path]), "mode": "0644"} for path in FILES]
    document = {
        "format": "chirality.app.instruction-resource-derivation/1",
        "owner": "DEL-02-04 App role-guidance owner",
        "sourceVersion": "instructions-v1",
        "sourceRoot": SOURCE.as_posix(),
        "generatedRoot": OUTPUT.as_posix(),
        "generationCommand": "python3 -m tools.instruction_resources",
        "checkCommand": "python3 -m tools.instruction_resources --check",
        "initialRetainedSnapshot": {"revision": IMPORT_REVISION, "path": OUTPUT.as_posix()},
        "historicalBindingStanding": "SOURCE_MAP.json and ROLE_SET_SOURCE_BINDING.json are retained records, copied unchanged, not rewritten as authoring or adoption evidence",
        "directories": [{"path": path or ".", "mode": "0755"} for path in DIRECTORIES],
        "files": entries,
        "limits": "Local authoring and byte/mode derivation only; no role migration, instruction-supply/adoption/behavior/qualification or portable distribution decision",
    }
    return (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def write_file(path: Path, raw: bytes) -> None:
    plain_ancestry(path.parent)
    # Replace only the declared ordinary output. Never write through an alias.
    if path.exists() or path.is_symlink():
        file_bytes(path)
    fd, name = tempfile.mkstemp(prefix=".instruction-resource-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            os.fchmod(stream.fileno(), MODE)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def generate(project: Path, *, check: bool = False) -> dict:
    project = Path(os.path.abspath(project))
    source_root, output_root, record = project / SOURCE, project / OUTPUT, project / DERIVATION
    source = tree(source_root)
    # Preflight the entire destination before any mutation; unknown entries are
    # never deleted/adopted. Missing declared files may be created by generation.
    output = tree(output_root, missing=not check)
    plain_ancestry(record.parent)
    current_record = file_bytes(record) if record.exists() or record.is_symlink() else None
    if current_record is not None and stat.S_IMODE(record.stat().st_mode) != MODE:
        raise ValueError("Instruction derivation manifest mode differs")
    expected = manifest(source)
    changed = [path for path in FILES if output.get(path) != source[path]]
    if current_record != expected:
        changed.append(DERIVATION.as_posix())
    if check and changed:
        raise ValueError("Generated instructions stale: " + ", ".join(changed))
    if not check:
        for directory in DIRECTORIES:
            path = output_root / directory
            plain_ancestry(path)
            if not path.exists():
                path.mkdir(mode=DIRECTORY_MODE, parents=True)
                path.chmod(DIRECTORY_MODE)
        for path in FILES:
            if output.get(path) != source[path]:
                write_file(output_root / path, source[path])
        if current_record != expected:
            write_file(record, expected)
    return {"state": "fresh" if check else "generated", "files": len(FILES),
            "derivationSha256": hashlib.sha256(expected).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(generate(args.project, check=args.check), sort_keys=True))
        return 0
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
