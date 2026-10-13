#!/usr/bin/env python3
"""Verify Chirality BagIt bytes with Python's standard library, without the App.

Usage: python3 verify.py /path/to/bag
This checks inventories and SHA-256, including the recorded chain-head tag.
It does not authenticate the unsigned package or interpret human-act evidence.
"""
import hashlib
import re
import sys
from pathlib import Path, PurePosixPath

TAGS = {"bagit.txt", "bag-info.txt", "manifest-sha256.txt", "records-chain-heads.json", "verify.py"}


def digest(path):
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            checksum.update(block)
    return checksum.hexdigest()


def members(root):
    result = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("linked package member")
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
        elif not path.is_dir():
            raise ValueError("nonregular package member")
    return result


def manifest(root, name, payload):
    seen = set()
    lines = (root / name).read_text(encoding="utf-8").split("\n")
    if lines[-1] == "":
        lines.pop()
    for line in lines:
        checksum, encoded = line.split("  ", 1)
        if not re.fullmatch(r"[0-9a-fA-F]{64}", checksum):
            raise ValueError("invalid SHA-256")
        if re.search(r"%(?!25|0A|0D)", encoded):
            raise ValueError("invalid path escape")
        path = re.sub(r"%(25|0A|0D)", lambda m: {"25": "%", "0A": "\n", "0D": "\r"}[m[1]], encoded)
        parts = path.split("/")
        if not parts or any(p in {"", ".", ".."} for p in parts) or PurePosixPath(path).is_absolute():
            raise ValueError("unsafe manifest path")
        if path.startswith("data/") != payload or (not payload and path.startswith("tagmanifest-")):
            raise ValueError("wrong manifest member class")
        if path in seen:
            raise ValueError("duplicate manifest member")
        seen.add(path)
        member = root / path
        if not member.is_file() or member.is_symlink() or digest(member) != checksum.lower():
            raise ValueError("missing member or checksum mismatch")
    return seen


def verify(root):
    if root.is_symlink():
        raise ValueError("linked bag folder")
    if not (root / "data").is_dir() or (root / "data").is_symlink():
        raise ValueError("missing or linked payload directory")
    all_files = members(root)
    if (root / "bagit.txt").read_bytes() != b"BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n":
        raise ValueError("unsupported bag declaration")
    tags = manifest(root, "tagmanifest-sha256.txt", False)
    if tags != TAGS:
        raise ValueError("incomplete export tags")
    payload = manifest(root, "manifest-sha256.txt", True)
    if all_files != payload | tags | {"tagmanifest-sha256.txt"}:
        raise ValueError("package inventory differs from manifests")
    return len(payload)


if __name__ == "__main__":
    try:
        count = verify(Path(sys.argv[1]))
        print(f"Verified {count} payload files and export tags, including the recorded chain-head tag.")
        print("Unsigned: this verifies package bytes, not origin, chain semantics or human acts.")
    except (OSError, ValueError, IndexError) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        sys.exit(1)
