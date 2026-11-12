#!/usr/bin/env python3
"""Verify a Chirality records BagIt package with Python's standard library, without the App.

Usage: python3 verify.py /path/to/bag
This checks the inventories and every SHA-256, including the recorded chain-head
tag, and recomputes each payload log's chain from its lines: every line's link
must name the SHA-256 of the line before it, and the chain must end at the head
the package records.

What that shows, and what it does not. A line that was changed, removed or
reordered is found where the link of the line after it was left as written, and
a change to a log's last line or lines removed from its end is found by the
head and line count the package records. A chain that was already broken in the
store when the package was exported is carried as it stood: the package records
the lines where it was broken, and when the breaks found are exactly those the
package bytes are consistent and that log's integrity is limited, which are
reported as two separate statements. The package is unsigned, so all of
this compares the package with itself: a package whose records, manifests and
recorded chain heads were replaced together still verifies. It does not show
who produced the package, and it shows no human act.

Outcomes. The output always makes two separate statements, "Package bytes:" and
"Log integrity:", and neither stands for the other.
  exit status 0  the package bytes are consistent and no chain is broken (or
                 the package carries no chained log, which is said as such).
  exit status 2  the package bytes are consistent, and the integrity of a log is
                 limited: the package records that its chain was already broken
                 (or could not be read) in the store at export, and the lines
                 agree; or the package's legacy profile records no head for a
                 log, so its chain was not checked. Each such log and line is
                 named. The package is not refused, and its logs are not whole.
                 A log that was not checked is never counted as unbroken.
  exit status 1  failed: something disagrees. A member, a checksum, an
                 inventory, or a chain that does not match what the package
                 records for it, in either direction.

The verifier validates no record schema. A line that is a JSON object is
examined for its link even where the App's reader would refuse the line as
nonconformant, so for such a line this may report a broken chain where the App
reports an invalid line.
"""
import hashlib
import json
import os
import stat
from contextlib import contextmanager
import re
import sys
from pathlib import Path, PurePosixPath

TAGS = {"bagit.txt", "bag-info.txt", "manifest-sha256.txt", "records-chain-heads.json", "verify.py"}
HEADS = "records-chain-heads.json"
# The chain method, the label of a torn line W-0 terminated and the logs the
# export records a head for (record_lines.rs, records.rs, records_export.rs).
METHOD = "chirality.rs.line.sha256/v1"
PARTIAL = "partial entry not recovered"
REGISTERED_COPY = "legacy/coordination.rs.jsonl"
ROLE_LOG = "role-supply/observations.jsonl"
WHITESPACE = frozenset(b" \t\n\x0c\r")


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
    """The manifest's members and their verified SHA-256, by path."""
    seen = {}
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
        member = root / path
        if not member.is_file() or member.is_symlink() or digest(member) != checksum.lower():
            raise ValueError("missing member or checksum mismatch")
        seen[path] = checksum.lower()
    return seen


def decoded(raw):
    """The JSON object a line holds, read as the App reads it (UTF-8 only, no
    NaN or Infinity), or None when the line is not a JSON object."""
    def refuse(constant):
        raise ValueError(f"not JSON: {constant}")
    try:
        value = json.loads(raw.decode("utf-8"), parse_constant=refuse)
    except (UnicodeError, ValueError, RecursionError):
        return None
    return value if isinstance(value, dict) else None


class Chain:
    """One log's chain as its lines are read (record_lines.rs, Chain::step)."""

    def __init__(self):
        self.last, self.lines, self.linked, self.unchained = None, 0, False, 0

    def step(self, no, raw, entry):
        """Takes complete line `no` (from 1). `entry` is its JSON object, whose
        link is examined, or None for a line that is counted but not read.
        Returns why the chain is broken at this line, or None."""
        broken = None
        if entry is not None:
            if "prevLine" not in entry:
                if self.linked:
                    broken = "it carries no chain link after linked lines"
                else:
                    self.unchained += 1
            else:
                self.linked = True
                link = entry["prevLine"]
                link = link if isinstance(link, dict) else {}
                value = link.get("value") if isinstance(link.get("value"), str) else None
                if link.get("method") != METHOD:
                    broken = f"it names an unknown chain method {json.dumps(link.get('method'))}"
                elif value != self.last:
                    if self.last is None:
                        broken = f"it links to {json.dumps(link.get('value'))}, but it is the first line of its log"
                    elif link.get("value") is None:
                        broken = "it starts a new chain after earlier lines"
                    else:
                        broken = (f"it links to {json.dumps(link.get('value'))}, "
                                  f"but the SHA-256 of the line before it is {self.last}")
        self.last = hashlib.sha256(raw).hexdigest()
        self.lines += 1
        return broken


def torn_and_named(no, raw, following):
    """Whether complete line `no` is a torn line that the complete line after it
    names, by its exact length and SHA-256, as a partial entry not recovered.
    Such a line is not a chain link: the next line links to the line before it."""
    if not following.endswith(b"\n"):
        return False
    following = following[:-1]
    try:
        text = following.decode("utf-8")
    except UnicodeError:
        text = None
    if text is not None and "\\" not in text and PARTIAL not in text:
        return False
    limit = decoded(following)
    body = limit.get("body") if limit is not None else None
    if not isinstance(body, dict) or limit.get("kind") != "evidence_limit" or body.get("label") != PARTIAL:
        return False
    named = body.get("subjectRef") if isinstance(body.get("subjectRef"), str) else ""
    if named != f"line {no}; {len(raw)} bytes; sha256 {hashlib.sha256(raw).hexdigest()}":
        return False
    # A whole entry is read as written even when a limit names it as torn.
    return decoded(raw[:-1] if raw.endswith(b"\r") else raw) is None


def record_chain(data):
    """A record log's chain and every break in it, each as (line, reason)."""
    chain, notes, broken = Chain(), [], []
    lines = data.split(b"\n")
    lines.pop()  # the unclosed final part: a partial, never a line of the chain
    for index, raw in enumerate(lines):
        no = index + 1
        following = lines[index + 1] + b"\n" if index + 1 < len(lines) else b""
        if torn_and_named(no, raw, following):
            notes.append(f"line {no} is a torn line W-0 terminated, not a chain link")
            continue
        if all(byte in WHITESPACE for byte in raw):
            continue
        why = chain.step(no, raw, decoded(raw[:-1] if raw.endswith(b"\r") else raw))
        if why:
            broken.append((no, why))
    return chain, notes, broken


def role_chain(data):
    """The role supply log's chain: every line is a whole JSON object and linked.
    The App records a head for this log only when it read it whole, so the
    first fault ends the reading."""
    chain = Chain()
    lines = data.split(b"\n")
    if lines.pop() != b"":
        return chain, [], [(len(lines) + 1, "a torn final line")]
    for index, raw in enumerate(lines):
        entry = decoded(raw)
        if entry is None:
            return chain, [], [(index + 1, "it is not a readable observation")]
        why = chain.step(index + 1, raw, entry)
        if why:
            return chain, [], [(index + 1, why)]
    return chain, [], []


def recorded_breaks(log, head):
    """The lines at which the package's recorded head says the chain was already
    broken when it was exported (the App reports a broken chain and never
    repairs it, so a faithful package carries one as it stood)."""
    listed = head.get("broken")
    if not isinstance(listed, list):
        raise ValueError(f"{log}: the recorded head does not say whether the chain was broken at export")
    lines = []
    for item in listed:
        found = re.search(r"chain broken at line ([0-9]+):", item) if isinstance(item, str) else None
        if found is None:
            raise ValueError(f"{log}: the recorded head records a broken chain this verifier cannot compare: {json.dumps(item)}")
        lines.append(int(found[1]))
    return lines


def chain_logs(payload, roles):
    """The payload logs whose chain head the export records (records_export.rs)."""
    return sorted(p for p in payload if p.endswith(".jsonl") and (
        p.startswith("runs/") or p.startswith("acts/") or p == REGISTERED_COPY or (roles and p == ROLE_LOG)))


def chains(root, payload):
    """Recomputes each recorded log's chain from the payload and compares its head
    with the recorded head. Returns the profile, the integrity limits the package
    carries from its store (`limited`) and the notes that limit no chain."""
    heads = decoded(read_bytes(root / HEADS))
    if heads is None or heads.get("format") != "chirality.records-export-chain-heads" or heads.get("method") != METHOD:
        raise ValueError("unsupported chain-head tag")
    profile = heads.get("formatVersion")
    if profile not in ("0.1", "0.2"):
        raise ValueError("unsupported chain-head tag profile")
    recorded = {}
    for item in heads.get("logs") if isinstance(heads.get("logs"), list) else [None]:
        if not isinstance(item, dict) or not isinstance(item.get("log"), str) or not isinstance(item.get("chain"), dict):
            raise ValueError("malformed chain-head tag entry")
        if item["log"] in recorded:
            raise ValueError(f"{item['log']}: chain head recorded twice")
        recorded[item["log"]] = item["chain"]
    names = {path[len("data/"):]: checksum for path, checksum in payload.items()}
    expected = chain_logs(names, profile == "0.2")
    for log in expected:
        if log not in recorded:
            raise ValueError(f"{log}: payload log has no recorded chain head")
    for log in recorded:
        if log not in names:
            raise ValueError(f"{log}: recorded chain head names no payload log")
        if log not in expected:
            raise ValueError(f"{log}: recorded chain head for a file that is not a chained log")
    notes, limited = [], []
    for log in expected:
        head = recorded[log]
        data = read_bytes(root / "data" / log)
        if hashlib.sha256(data).hexdigest() != names[log]:
            raise ValueError(f"{log}: log changed after its checksum was verified")
        if "state" in head:
            # No head: the App could not read this log's chain at export. For
            # the role supply log the App's own verification reads the copy
            # the same way and accepts the package, and this verifier (which
            # validates no schema) cannot tell a sound log from the one the
            # App refused, so the log is carried as a limit. A record log's
            # copy is readable here, so a recorded "unreadable" disagrees.
            if log != ROLE_LOG:
                raise ValueError(f"{log}: recorded at export as {head['state']}: {head.get('error')}")
            limited.append(f"{log}: the package records that the App could not read this log's chain when it was exported "
                           f"({head['state']}: {head.get('error')}); its lines are carried as they stood and its chain is not recomputed here")
            continue
        chain, log_notes, broken = (role_chain if log == ROLE_LOG else record_chain)(data)
        # The breaks found must be exactly the breaks the package records: one
        # found and not recorded is a line altered since the head was recorded.
        at_export = recorded_breaks(log, head)
        for no, why in broken:
            if no not in at_export:
                raise ValueError(f"{log}: chain broken at line {no}: {why}; the package records no break there")
        for no in at_export:
            if no not in [found for found, _ in broken]:
                raise ValueError(f"{log}: the package records a chain broken at line {no}, but the recomputed chain is not broken there")
        if head.get("method") != METHOD or head.get("head") != chain.last or type(head.get("lines")) is not int or head.get("lines") != chain.lines:
            raise ValueError(f"{log}: recomputed chain head {chain.last} after {chain.lines} lines "
                             f"differs from the recorded head {head.get('head')} after {head.get('lines')} lines")
        limited.extend(f"{log}: chain broken at line {no}: {why}; the package records it broken there when exported"
                       for no, why in broken)
        notes.extend(f"{log}: {note}" for note in log_notes)
        if chain.unchained:
            notes.append(f"{log}: unchained (legacy): {chain.unchained} lines before the chain starts carry no link"
                         if chain.linked else f"{log}: unchained (legacy): no line carries a chain link")
    if profile == "0.1" and ROLE_LOG in names:
        # Not checked is not clean: a log this verifier could not examine is
        # an integrity limit, never part of "no chain is broken".
        limited.append(f"{ROLE_LOG}: this package's legacy chain-head profile (0.1) records no head for this log, so its chain was not checked")
    return {"profile": profile, "logs": len(expected), "limited": limited, "notes": notes}


def verify(root):
    if root.is_symlink():
        raise ValueError("linked bag folder")
    if not (root / "data").is_dir() or (root / "data").is_symlink():
        raise ValueError("missing or linked payload directory")
    all_files = members(root)
    if read_bytes(root / "bagit.txt") != b"BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n":
        raise ValueError("unsupported bag declaration")
    tags = set(manifest(root, "tagmanifest-sha256.txt", False))
    if tags not in (TAGS, TAGS | {"records-administration.json"}):
        raise ValueError("incomplete export tags")
    payload = manifest(root, "manifest-sha256.txt", True)
    file_names={name for name, metadata in all_files.items() if stat.S_ISREG(metadata[2])}
    if file_names != set(payload) | tags | {"tagmanifest-sha256.txt"}:
        raise ValueError("package inventory differs from manifests")
    report = chains(root, payload)
    if members(root) != all_files:
        raise ValueError("package changed during verification")
    return len(payload), "records-administration.json" in tags, report


LIMITED = 2  # exit status: bytes consistent, and a log's integrity is limited


def report_lines(count, administration, report):
    """What a person is told for a package that agrees with what it records.
    Two statements, never one: whether the bytes agree with the manifests and
    recorded heads, and whether any log's own integrity is limited."""
    logs, limited = report["logs"], report["limited"]
    chains = f"{logs} log chain{'' if logs == 1 else 's'}"
    lines = [f"Package bytes: consistent. {count} payload files and the export tags agree with the manifests, "
             f"and {chains} recomputed from the payload {'ends' if logs == 1 else 'end'} at the head this package records."]
    if limited:
        lines.append(f"Log integrity: LIMITED in {len(limited)} log{'' if len(limited) == 1 else 's'}. "
                     "The store's own records were already limited there when this package was exported, and the package carries them as they stood:")
        lines.extend(f"  Integrity limit: {limit}" for limit in limited)
        lines.append("  A broken chain is reported and never repaired. Consistent bytes do not make these logs whole.")
        lines.append(f"Result: package bytes consistent; log integrity limited (exit status {LIMITED}).")
    elif logs == 0:
        # Nothing examined is said as nothing examined, not as a clean result.
        lines.append("Log integrity: nothing to check. This package carries no chained log.")
        lines.append("Result: package bytes consistent; no chained log in the package (exit status 0).")
    else:
        unlinked = sum(1 for note in report["notes"] if "unchained (legacy)" in note)
        lines.append("Log integrity: no chain is broken. Every line that carries a link names the line before it." + (
            f" {unlinked} log{' has' if unlinked == 1 else 's have'} lines with no link, written before chaining began: "
            "the chain shows nothing about those lines. They are named in the notes." if unlinked else ""))
        lines.append("Result: package bytes consistent; no log integrity limit (exit status 0).")
    lines.extend(f"Note: {note}" for note in report["notes"])
    lines.append("Protected prior administration bytes included." if administration
                 else "Administrative history unknown: legacy package has no retention snapshot.")
    lines.append("Unsigned: this shows that the package agrees with its own manifests and recorded chain heads. "
                 "A package whose records, manifests and chain heads were replaced together still verifies. "
                 "It does not show who produced the package, and it shows no human act.")
    return lines


if __name__ == "__main__":
    try:
        count, administration, report = verify(Path(sys.argv[1]))
    except (OSError, ValueError, IndexError, UnicodeError) as error:
        print(f"Result: failed (exit status 1). Verification failed: {error}", file=sys.stderr)
        sys.exit(1)
    print("\n".join(report_lines(count, administration, report)))
    sys.exit(LIMITED if report["limited"] else 0)
