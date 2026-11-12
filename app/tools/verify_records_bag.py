#!/usr/bin/env python3
"""Verify a Chirality records BagIt package with Python's standard library, without the App.

Usage: python3 verify.py /path/to/bag

The checks, for a package whose chain-head tag is of profile 0.3:
  1. Manifests and inventory. Every payload file and export tag has the
     SHA-256 its manifest records, and the package holds exactly those files.
  2. Exported log bytes. For each chained log of the payload, the file's exact
     length and SHA-256 equal the ones the tag (records-chain-heads.json)
     records for it. A change to any byte of any chained log, with the tag left
     unchanged, fails here whether or not the manifests were regenerated.
  3. Chains. For each chained log the package records a head for, the chain is
     recomputed from the lines (each line's link must name the SHA-256 of the
     line before it) and compared with the recorded head, line count and
     recorded breaks. Which lines are counted without their link examined
     ("set aside") and which are not counted ("torn") is taken from the
     package's own account in the tag.

Limits. After the checks, anything that limits what they show is listed under
one of three labels:
  FOUND by this verifier       a break in a recomputed chain that the package
                               records too; an unclosed final part of a log.
  STATED by the package, not checked here
                               a line the package's account says the App set
                               aside as invalid; a role supply log the package
                               says the App could not read, with the line and
                               kind it records.
  NOT CHECKED                  a log's chain that this verifier did not
                               recompute.

What is never checked here: whether a line is a record or an observation the
App accepts (this program does not hold those formats), and the package's
account itself. Verifying the package through the App checks both.

Profiles 0.1 and 0.2 of the tag record neither a log's bytes nor an account of
its lines. For a package of those profiles this program checks the manifests
and inventory only, and lists every chain as NOT CHECKED. No release exported
those profiles.

Exit status:
  0  every check this verifier makes passed, and no limit is listed. It does
     not mean the records are intact.
  2  every check this verifier makes passed, and at least one limit is listed.
  1  a check failed.

The package is unsigned. A package whose logs, tag and manifests were replaced
together passes these checks. They do not show who produced the package, and
they show no human act.
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
METHOD = "chirality.rs.line.sha256/v1"
REGISTERED_COPY = "legacy/coordination.rs.jsonl"
ROLE_LOG = "role-supply/observations.jsonl"
WHITESPACE = frozenset(b" \t\n\x0c\r")
MISSING = object()


class ChainDisagreement(ValueError):
    """A chain that does not match what the package records for it."""


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


def json_object(raw):
    """The JSON object `raw` holds, or None."""
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError, RecursionError):
        return None
    return value if isinstance(value, dict) else None


def member(value, name):
    """A member as the App indexes it: absent, or of a non-object, is null."""
    return value.get(name) if isinstance(value, dict) else None


def shown(value):
    """A JSON value as the App prints it in a chain limit."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


class Chain:
    """One log's chain as its lines are read (record_lines.rs, Chain::step). The
    reasons are the App's own words, so they can be compared with the limits the
    package records."""

    def __init__(self):
        self.last, self.lines, self.linked, self.unchained = None, 0, False, 0

    def count(self, raw):
        """A line that is counted and whose link is not examined."""
        self.last = hashlib.sha256(raw).hexdigest()
        self.lines += 1

    def step(self, raw, link):
        """Takes one complete line with its link (MISSING for none). Returns
        why the chain is broken at this line, in the App's words, or None."""
        broken = None
        if link is MISSING:
            if self.linked:
                broken = "no chain link after linked lines; never repaired"
            else:
                self.unchained += 1
        else:
            self.linked = True
            value = member(link, "value")
            if member(link, "method") != METHOD or not isinstance(member(link, "method"), str):
                broken = f"unknown chain method {shown(member(link, 'method'))}"
            elif (value if isinstance(value, str) else None) != self.last:
                if value is None and self.last is not None:
                    broken = "it starts a new chain after earlier lines; never repaired"
                elif self.last is not None:
                    broken = f"it links to {shown(value)}, but the preceding line's identity is {self.last}; never repaired"
                else:
                    broken = f"it links to {shown(value)}, but it is the first line of its log; never repaired"
        self.count(raw)
        return broken

    def unchained_limit(self, name):
        """The App's note for lines with no link (record_lines.rs, unchained_note)."""
        if not self.unchained:
            return None
        if self.linked:
            return (f"{name}: unchained (legacy): lines before the first linked line ({self.unchained}) carry no chain link; "
                    "the chain starts after them")
        return f"{name}: unchained (legacy): no line carries a chain link ({self.unchained} lines)"


def unclosed_end(data):
    """The length of a log's unclosed final part (a partial entry the App does
    not read), or None when the log ends with a complete line."""
    last = data.split(b"\n")[-1]
    return len(last) if last and not all(byte in WHITESPACE for byte in last) else None


def account_chain(log, data, set_aside, torn):
    """A log's chain recomputed from its lines. A line the package's account
    lists as set aside is counted and its link not examined; a torn line it
    lists is not counted; every other line that is not blank must be a JSON
    object, and its link is examined. The account is the package's own
    statement of what the App's reader did: this verifier follows it and
    relays it, and does not check it. Returns the chain and every break as
    (line, reason)."""
    chain, broken = Chain(), []
    lines = data.split(b"\n")
    lines.pop()  # the unclosed final part: a partial, never a line of the chain
    for listed in sorted(set_aside | torn):
        if listed > len(lines):
            raise ChainDisagreement(f"{log}: the package's account names line {listed}, and the log has {len(lines)} complete lines")
    for index, raw in enumerate(lines):
        no = index + 1
        if no in torn:
            continue
        if no in set_aside:
            chain.count(raw)
            continue
        if all(byte in WHITESPACE for byte in raw):
            continue
        # Any JSON object will do here: which lines are records is the
        # account's to state, and a line the App read is plain JSON.
        try:
            entry = json.loads(raw.decode("utf-8"))
        except (UnicodeError, ValueError, RecursionError):
            entry = None
        if not isinstance(entry, dict):
            raise ChainDisagreement(f"{log}: line {no} is not a JSON object, and the package's account does not list it as set aside")
        why = chain.step(raw, entry["prevLine"] if "prevLine" in entry else MISSING)
        if why:
            broken.append((no, why))
    return chain, broken


def listed_lines(log, head, name):
    """One list of the account: line numbers from 1, ascending, each once."""
    lines = head.get(name)
    if not isinstance(lines, list) or any(type(no) is not int or no < 1 for no in lines) or lines != sorted(set(lines)):
        raise ChainDisagreement(f"{log}: the package's account of its lines ({name}) is missing or malformed")
    return set(lines)


def compare_head(log, name, head, chain, broken):
    """Fails unless the head the package records for `log` is the one its lines
    give: every recorded fact this verifier can recompute, as the App compares
    them. `name` is the App's name for the log in its limits."""
    listed = head.get("broken")
    if not isinstance(listed, list):
        raise ChainDisagreement(f"{log}: the recorded head does not say whether the chain was broken at export")
    recorded = {}
    for item in listed:
        found = re.match(re.escape(name) + r": chain broken at line ([0-9]+): ", item) if isinstance(item, str) else None
        if found is None or int(found[1]) in recorded:
            raise ChainDisagreement(f"{log}: the recorded head records a broken chain this verifier cannot compare: {json.dumps(item)}")
        recorded[int(found[1])] = item
    for no, why in broken:
        if no not in recorded:
            raise ChainDisagreement(f"{log}: chain broken at line {no}: {why}; the package records no break there")
    found = {no: f"{name}: chain broken at line {no}: {why}" for no, why in broken}
    for no, item in recorded.items():
        if no not in found:
            raise ChainDisagreement(f"{log}: the package records a chain broken at line {no}, but the recomputed chain is not broken there")
        if found[no] != item:
            raise ChainDisagreement(f"{log}: the break the package records at line {no} is not the break its lines give: "
                                    f"recorded {json.dumps(item)}, recomputed {json.dumps(found[no])}")
    if head.get("method") != METHOD or head.get("head") != chain.last or type(head.get("lines")) is not int or head.get("lines") != chain.lines:
        raise ChainDisagreement(f"{log}: method, head, lines: its lines give {METHOD}, {chain.last}, {chain.lines}")
    facts = {"linked": chain.linked, "unchained": chain.unchained, "unchainedLimit": chain.unchained_limit(name)}
    for fact, value in facts.items():
        if fact not in head or type(head[fact]) is not type(value) or head[fact] != value:
            raise ChainDisagreement(f"{log}: {fact}: its lines give {json.dumps(value)}")


def chain_logs(payload, roles):
    """The payload logs whose chain head the export records (records_export.rs)."""
    return sorted(p for p in payload if p.endswith(".jsonl") and (
        p.startswith("runs/") or p.startswith("acts/") or p == REGISTERED_COPY or (roles and p == ROLE_LOG)))


def chains(root, payload):
    """Checks 2 and 3. Returns what was checked, as counts, and the limits by
    kind. Raises on any disagreement."""
    heads = json_object(read_bytes(root / HEADS))
    if heads is None or heads.get("format") != "chirality.records-export-chain-heads" or heads.get("method") != METHOD:
        raise ValueError("unsupported chain-head tag")
    profile = heads.get("formatVersion")
    if profile not in ("0.1", "0.2", "0.3"):
        raise ValueError("unsupported chain-head tag profile")
    recorded = {}
    for item in heads.get("logs") if isinstance(heads.get("logs"), list) else [None]:
        if not isinstance(item, dict) or not isinstance(item.get("log"), str) or not isinstance(item.get("chain"), dict):
            raise ValueError("malformed chain-head tag entry")
        if item["log"] in recorded:
            raise ValueError(f"{item['log']}: chain head recorded twice")
        recorded[item["log"]] = item["chain"]
    names = {path[len("data/"):]: checksum for path, checksum in payload.items()}
    expected = chain_logs(names, profile != "0.1")
    for log in expected:
        if log not in recorded:
            raise ValueError(f"{log}: payload log has no recorded chain head")
    for log in recorded:
        if log not in names:
            raise ValueError(f"{log}: recorded chain head names no payload log")
        if log not in expected:
            raise ValueError(f"{log}: recorded chain head for a file that is not a chained log")
    report = {"profile": profile, "logs": len(expected), "pinned": 0, "recomputed": 0,
              "found": [], "stated": [], "notChecked": [], "notes": []}
    if profile != "0.3":
        # No account and no pin on a log's bytes: nothing here follows a chain.
        logs = sorted(expected + ([ROLE_LOG] if profile == "0.1" and ROLE_LOG in names else []))
        report["logs"] = len(logs)
        report["notChecked"] = [f"{log}: its chain" for log in logs]
        return report
    for log in expected:
        head = recorded[log]
        data = read_bytes(root / "data" / log)
        if hashlib.sha256(data).hexdigest() != names[log]:
            raise ValueError(f"{log}: log changed after its checksum was verified")
        # Check 2, an equality, before anything is made of the lines.
        if type(head.get("bytes")) is not int or head.get("bytes") != len(data) or head.get("sha256") != names[log]:
            raise ChainDisagreement(f"{log}: its bytes ({len(data)} bytes, SHA-256 {names[log]}) are not the ones the package's "
                                    f"chain-head tag records ({json.dumps(head.get('bytes'))} bytes, SHA-256 {json.dumps(head.get('sha256'))})")
        report["pinned"] += 1
        role = log == ROLE_LOG
        if "state" in head:
            if not role:
                # A record log's copy is readable here, so a recorded "unreadable" disagrees.
                raise ChainDisagreement(f"{log}: recorded at export as {head['state']}: {head.get('error')}")
            line, kind = head.get("line"), head.get("kind")
            where = f" at line {line} ({kind})" if type(line) is int and isinstance(kind, str) else ""
            report["stated"].append(f"{log}: the App could not read this log's chain{where} ({head['state']}: {head.get('error')})")
            report["notChecked"].append(f"{log}: its chain")
            continue
        set_aside, torn = sorted(listed_lines(log, head, "setAside")), sorted(listed_lines(log, head, "torn"))
        if set(set_aside) & set(torn):
            raise ChainDisagreement(f"{log}: the package's account lists a line both as set aside and as torn")
        if role and (set_aside or torn):
            raise ChainDisagreement(f"{log}: the package's account sets lines of this log aside, and the App takes this log whole or not at all")
        chain, broken = account_chain(log, data, set(set_aside), set(torn))
        unclosed, stated = unclosed_end(data), head.get("unclosedEnd")
        if "unclosedEnd" not in head or (stated is not None and type(stated) is not int) or stated != unclosed:
            raise ChainDisagreement(f"{log}: unclosedEnd: the log has {json.dumps(unclosed)}")
        # Check 3.
        compare_head(log, "role supply observations" if role else PurePosixPath(log).name, head, chain, broken)
        report["recomputed"] += 1
        report["found"].extend(f"{log}: chain broken at line {no}: {why} (the package records the same break)" for no, why in broken)
        if unclosed is not None:
            report["found"].append(f"{log}: partial entry at end (not read): {unclosed} bytes after the last complete line")
        report["stated"].extend(f"{log}: line {no} was set aside by the App as invalid: it is not read as a record, and its own link is not examined"
                                for no in set_aside)
        # Not limits: what the chain recomputed here does not include.
        report["notes"].extend(f"STATED by the package, not checked here: {log}: line {no} is a torn line the App closed after an interrupted "
                               "write; it is not counted in the chain" for no in torn)
        if chain.unchained and chain.linked:
            report["notes"].append(f"FOUND by this verifier: {log}: {chain.unchained} lines before the chain starts carry no link")
    return report


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


LIMITED = 2  # exit status: every check passed, and at least one limit is listed


def limits(report):
    """The limits by kind, in the order they are printed."""
    return [("FOUND by this verifier", report["found"]), ("STATED by the package, not checked here", report["stated"]),
            ("NOT CHECKED", report["notChecked"])]


def not_checked(report):
    """What this run did not check, from the same counts as the lines above it."""
    unread = report["logs"] - report["recomputed"]
    if report["profile"] != "0.3":
        return (f"Not checked by this verifier: the chain of {unread} chained log{'' if unread == 1 else 's'} (the tag's profile, "
                f"{report['profile']}, records neither a log's bytes nor an account of its lines), and whether each line is a record "
                "the App accepts. To have them checked, verify the package through the App."
                if unread else "Not checked by this verifier: whether each payload file is one the App accepts.")
    parts = ["whether each line is a record or an observation the App accepts (this verifier does not hold those formats)",
             "the package's account of which lines the App set aside or closed as torn"]
    if unread:
        parts.append(f"the chain of {unread} log{'' if unread == 1 else 's'}")
    return "Not checked by this verifier: " + "; ".join(parts) + ". To have them checked, verify the package through the App."


def report_lines(count, administration, report):
    """One line for each check, with its result; then the limits by kind; then
    what was not checked. Nothing else."""
    logs, listed = report["logs"], sum(len(items) for _, items in limits(report))
    lines = [f"Manifests and inventory: agree. {count} payload files and the export tags."]
    if report["profile"] == "0.3":
        if logs:
            lines.append(f"Exported log bytes: {report['pinned']} of {logs} chained log{'' if logs == 1 else 's'} equal the length and SHA-256 the chain-head tag records.")
            lines.append(f"Chains: {report['recomputed']} of {logs} recomputed from the lines"
                         + ("; each recomputed head equals the recorded one." if report["recomputed"] else "."))
        else:
            lines.append("Chains: the package holds no chained log.")
    elif logs:
        lines.append(f"Chains: not checked by this verifier for a package of profile {report['profile']}; verify through the App.")
    else:
        lines.append("Chains: the package holds no chained log.")
    lines.append(f"Limits: {listed}." if listed else "Limits: none.")
    for label, items in limits(report):
        lines.extend(f"  {label}: {item}" for item in items)
    lines.extend(f"Note. {note}" for note in report["notes"])
    lines.append(not_checked(report))
    lines.append("Result: every check this verifier makes passed; "
                 + (f"{listed} limit{'' if listed == 1 else 's'} listed (exit status {LIMITED})." if listed else "no limit listed (exit status 0)."))
    lines.append("Administration snapshot: included in the package." if administration
                 else "Administration snapshot: none in the package.")
    lines.append("Unsigned: a package whose logs, tag and manifests were replaced together passes these checks. "
                 "They do not show who produced the package, and they show no human act.")
    return lines


if __name__ == "__main__":
    try:
        count, administration, report = verify(Path(sys.argv[1]))
    except (OSError, ValueError, IndexError, UnicodeError) as error:
        print(f"Result: a check failed (exit status 1). {error}", file=sys.stderr)
        print("Not checked by this verifier: anything after the check that failed.", file=sys.stderr)
        sys.exit(1)
    print("\n".join(report_lines(count, administration, report)))
    sys.exit(LIMITED if any(items for _, items in limits(report)) else 0)
