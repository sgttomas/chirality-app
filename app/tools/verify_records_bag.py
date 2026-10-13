#!/usr/bin/env python3
"""Verify Chirality BagIt bytes with Python's standard library, without the App.

Usage: python3 verify.py /path/to/bag
This checks inventories and SHA-256, including the recorded chain-head tag.
It does not authenticate the unsigned package or interpret human-act evidence.
"""
import hashlib
import os
import stat
from contextlib import contextmanager
import re
import sys
from pathlib import Path, PurePosixPath

TAGS = {"bagit.txt", "bag-info.txt", "manifest-sha256.txt", "records-chain-heads.json", "verify.py"}


def stamp(metadata):
    return (metadata.st_dev, metadata.st_ino, metadata.st_mode,
            metadata.st_nlink, metadata.st_size, metadata.st_mtime_ns,
            metadata.st_ctime_ns)


def plain_parents(path):
    for parent in path.absolute().parents:
        if not stat.S_ISDIR(parent.lstat().st_mode):
            raise ValueError("linked or nonregular package ancestor")


@contextmanager
def opened_regular(path):
    plain_parents(path)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError("nonregular package member")
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_NONBLOCK"):
        raise ValueError("safe nonblocking package verification unavailable")
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), "rb") as stream:
        opened = os.fstat(stream.fileno())
        if not stat.S_ISREG(opened.st_mode) or stamp(opened) != stamp(before):
            raise ValueError("package member changed while opening")
        yield stream
        if stamp(os.fstat(stream.fileno())) != stamp(before) or stamp(path.lstat()) != stamp(before):
            raise ValueError("package member changed while reading")
        plain_parents(path)


def read_bytes(path):
    with opened_regular(path) as stream:
        return stream.read()


def digest(path):
    checksum = hashlib.sha256()
    with opened_regular(path) as stream:
        for block in iter(lambda: stream.read(65536), b""):
            checksum.update(block)
    return checksum.hexdigest()


def members(root):
    result = {}
    def walk(folder):
        plain_parents(folder)
        if not stat.S_ISDIR(folder.lstat().st_mode):
            raise ValueError("linked or nonregular package directory")
        for path in folder.iterdir():
            metadata = path.lstat()
            result[path.relative_to(root).as_posix()] = stamp(metadata)
            if stat.S_ISDIR(metadata.st_mode):
                walk(path)
            elif not stat.S_ISREG(metadata.st_mode):
                raise ValueError("linked or nonregular package member")
    walk(root)
    return result


def manifest(root, name, payload):
    seen = set()
    lines = read_bytes(root / name).decode("utf-8").split("\n")
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
    if read_bytes(root / "bagit.txt") != b"BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n":
        raise ValueError("unsupported bag declaration")
    tags = manifest(root, "tagmanifest-sha256.txt", False)
    if tags not in (TAGS, TAGS | {"records-administration.json"}):
        raise ValueError("incomplete export tags")
    payload = manifest(root, "manifest-sha256.txt", True)
    file_names={name for name, metadata in all_files.items() if stat.S_ISREG(metadata[2])}
    if file_names != payload | tags | {"tagmanifest-sha256.txt"}:
        raise ValueError("package inventory differs from manifests")
    if members(root) != all_files:
        raise ValueError("package changed during verification")
    return len(payload), "records-administration.json" in tags


if __name__ == "__main__":
    try:
        count, administration = verify(Path(sys.argv[1]))
        print(f"Verified {count} payload files and export tags, including the recorded chain-head tag.")
        print("Protected prior administration bytes included." if administration else "Administrative history unknown: legacy package has no retention snapshot.")
        print("Unsigned: this verifies package bytes, not origin, chain semantics or human acts.")
    except (OSError, ValueError, IndexError, UnicodeError) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        sys.exit(1)
