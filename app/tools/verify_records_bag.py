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
  exit status 0  the package bytes are consistent, no chain is broken and no
                 line was set aside (or the package carries no chained log,
                 which is said as such).
  exit status 2  the package bytes are consistent, and the integrity of a log is
                 limited: the package records that its chain was already broken
                 (or could not be read) in the store at export, and the lines
                 agree; or the App set a line aside as invalid; or a recorded
                 head could not be compared with the lines (a role supply log
                 the App refused for a reason this verifier cannot see, or a
                 legacy profile that records no head for a log). Each such log
                 and line is named. The package is not refused, and its logs
                 are not whole. A log that was not checked is never counted as
                 unbroken, and a head that was not compared is never counted as
                 agreeing.
  exit status 1  failed: something disagrees. A member, a checksum, an
                 inventory, or a chain that does not match what the package
                 records for it, in either direction.

The chain-head tag, records-chain-heads.json. It lists, for each chained log
of the payload, the head the App's reader found: the SHA-256 of the log's last
counted line, the number of lines counted, whether lines carry links, how many
lines written before chaining began carry none, and each place the chain was
broken. Profile 0.3 (formatVersion "0.3") adds the reader's account of the
log's lines, so that this verifier follows the chain exactly as the App did:
  setAside  the numbers (from 1) of the lines the App counted in the chain
            without reading them as records, because it found them unreadable
            or invalid. Such a line's bytes are in the chain: the line after
            it links to them. Its own link is not examined.
  torn      the numbers of the torn lines the App closed and set aside after an
            interrupted write. Such a line is not counted; the line after it
            names its exact length and SHA-256 and is itself in the chain.
For a role supply log the App could not take, profile 0.3 also records the
line and the kind of the fault that stopped it.

What the account can and cannot do. A line the account lists as set aside
always turns the result from clean to limited, and is named. A line the
account does not list must be readable and must link, or its break must be the
one the package records; otherwise verification fails. So the account can only
add stated limits and never remove a failure. The package is unsigned: someone
who rewrites a log, its account and the manifests together is not detected.

Packages of profile 0.1 or 0.2 carry no account. For those this verifier reads
each line as nearly as it can as the App's reader does (the same JSON, the top
level of the record format, the group rules) and it cannot see a fault deeper
in a record than that: for a line whole at its top level and invalid deeper, it
examines a link the App does not, and can fail a faithfully exported package
there. It says so when it fails on a chain of such a package; verifying or
importing the package through the App settles it. No release exported those
profiles.
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
# The top level of the record format (app/src-tauri/schemas/RS_RECORD.schema.json,
# $defs entry, groupLine and chainLink), kept equal to it by
# app/tests/verify_records_bag_test.py. Nothing deeper is carried here.
ENTRY_FORMAT, GROUP_FORMAT = "chirality.rs.record", "chirality.rs.group"
ENTRY_REQUIRED = ("format", "formatVersion", "recordId", "kind", "recorder", "context", "seq", "writtenAt", "body")
ENTRY_MEMBERS = frozenset(ENTRY_REQUIRED + ("runId", "observedAt", "corrects", "correctionReason", "prevLine"))
GROUP_REQUIRED = ("format", "formatVersion", "groupId", "entries")
GROUP_MEMBERS = frozenset(GROUP_REQUIRED + ("prevLine",))
KINDS = frozenset((
    "run_opened", "settings_version", "model_turn", "operation_entry", "checkpoint_arrival", "disposition_change",
    "act_request", "human_act", "act_declined", "act_lapsed", "run_resumed", "run_ended", "evidence_limit",
    "destination_requested", "destination_grant", "destination_contacted", "destination_declined", "boundary_refusal",
    "destination_request_closed", "outside_process", "supplied_guidance", "examination_findings",
    "tool_permission_settlement", "compatibility_report_ref", "checkpoint_listed", "declaration_finding", "act_counted",
    "act_not_counted", "item_decision", "arrival_declined", "control_relation", "continued_past", "observation_lost",
    "observation_recovered", "arrival_replaced", "act_after_run_end", "role_limit_observation"))
RECORDER_ROLES = frozenset(("App writer", "App interface (capturing surface)", "host facility", "host control",
                            "host loop", "host native layer", "agent"))
SURFACES = frozenset(("App", "host"))
RECORD_ID = re.compile(r"rec:[A-Za-z0-9._:-]+\Z")
RUN_ID = re.compile(r"run:[A-Za-z0-9._:/-]+\Z")
VERSION = re.compile(r"[0-9]+\.[0-9]+\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
# The App's JSON reader (serde_json) refuses nesting deeper than this.
MAX_DEPTH = 127
NOT_JSON, MISSING = object(), object()
CANNOT_TELL = ("This package is of a chain-head profile that carries no account of its lines (0.1 or 0.2). "
               "This verifier reads each record only as far as the top level of the record format. If the App set this "
               "line aside as invalid for a deeper reason, the App does not examine the line's link, and this package may be "
               "a faithful export: this verifier cannot tell that from an altered line, and the App can. Verify or import "
               "the package through the App to settle it.")


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


def parsed(raw):
    """The JSON value `raw` holds as the App's reader (serde_json) takes it, or
    NOT_JSON: UTF-8 only; no NaN or Infinity; no number out of range; no lone
    surrogate; nesting no deeper than the App allows. Duplicate keys keep their
    last value, as in the App."""
    def refuse(_):
        raise ValueError("not JSON")

    def real(text):
        value = float(text)
        if value in (float("inf"), float("-inf")):
            raise ValueError("number out of range")
        return value

    def whole(text):
        value = int(text)
        return value if -(2 ** 63) <= value < 2 ** 64 else real(text)

    def too_deep(text):
        depth, in_string, escaped = 0, False, False
        for ch in text:
            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
            elif ch == '"':
                in_string = True
            elif ch in "[{":
                depth += 1
                if depth > MAX_DEPTH:
                    return True
            elif ch in "]}":
                depth -= 1
        return False

    def lone_surrogate(value):
        if isinstance(value, str):
            return any("\ud800" <= ch <= "\udfff" for ch in value)
        if isinstance(value, list):
            return any(lone_surrogate(item) for item in value)
        if isinstance(value, dict):
            return any(lone_surrogate(key) or lone_surrogate(item) for key, item in value.items())
        return False

    def members(pairs):
        # Every member is examined before a repeated key keeps its last value:
        # the App's reader refuses a lone surrogate wherever it stands.
        if any(lone_surrogate(key) or lone_surrogate(item) for key, item in pairs):
            raise ValueError("lone surrogate")
        return dict(pairs)

    try:
        text = raw.decode("utf-8")
        if text.count("[") + text.count("{") > MAX_DEPTH and too_deep(text):
            return NOT_JSON
        value = json.loads(text, parse_constant=refuse, parse_int=whole, parse_float=real,
                           object_pairs_hook=members if "\\u" in text else None)
    except (UnicodeError, ValueError, RecursionError):
        return NOT_JSON
    return NOT_JSON if "\\u" in text and lone_surrogate(value) else value


def decoded(raw):
    """The JSON object `raw` holds, or None."""
    value = parsed(raw)
    return value if isinstance(value, dict) else None


def member(value, name):
    """A member as the App indexes it: absent, or of a non-object, is null."""
    return value.get(name) if isinstance(value, dict) else None


def text_of(value, pattern=None, least=0):
    return isinstance(value, str) and len(value) >= least and (pattern is None or pattern.match(value) is not None)


def link_shape(link):
    return (isinstance(link, dict) and set(link) == {"method", "value"} and link["method"] == METHOD
            and (link["value"] is None or text_of(link["value"], HEX64)))


def entry_shape(value):
    """Whether `value` has the top level of a record entry. A record that is
    invalid deeper than this (in its body, for its kind) passes: see CANNOT_TELL."""
    if not isinstance(value, dict) or not set(value) <= ENTRY_MEMBERS or any(name not in value for name in ENTRY_REQUIRED):
        return False
    recorder, context, seq = value["recorder"], value["context"], value["seq"]
    return (
        value["format"] == ENTRY_FORMAT and isinstance(value["format"], str)
        and text_of(value["formatVersion"], VERSION) and text_of(value["recordId"], RECORD_ID)
        and isinstance(value["kind"], str) and value["kind"] in KINDS
        and isinstance(recorder, dict) and set(recorder) == {"role", "identity"}
        and isinstance(recorder["role"], str) and recorder["role"] in RECORDER_ROLES and text_of(recorder["identity"], least=1)
        and isinstance(context, dict) and "surface" in context and set(context) <= {"surface", "hostIdentity"}
        and isinstance(context["surface"], str) and context["surface"] in SURFACES
        and ("hostIdentity" not in context or isinstance(context["hostIdentity"], str))
        and ((type(seq) is int) or (type(seq) is float and seq.is_integer())) and seq >= 1
        and text_of(value["writtenAt"], least=1) and isinstance(value["body"], dict)
        and ("runId" not in value or text_of(value["runId"], RUN_ID))
        and ("observedAt" not in value or isinstance(value["observedAt"], str))
        and ("corrects" not in value or (text_of(value["corrects"], RECORD_ID) and "correctionReason" in value))
        and ("correctionReason" not in value or text_of(value["correctionReason"], least=1))
        and ("prevLine" not in value or link_shape(value["prevLine"])))


def group_shape(value):
    """Whether `value` is a group line the App's reader takes whole: its top
    level, and the group rules (one run, consecutive seq, distinct identities)."""
    def u64(number):
        return number if type(number) is int and 0 <= number < 2 ** 64 else None

    if not set(value) <= GROUP_MEMBERS or any(name not in value for name in GROUP_REQUIRED):
        return False
    entries = value["entries"]
    if (value["formatVersion"] != "0.1" or not isinstance(value["formatVersion"], str)
            or not text_of(value["groupId"]) or not value["groupId"].startswith("grp:")
            or ("prevLine" in value and not link_shape(value["prevLine"]))
            or not isinstance(entries, list) or len(entries) < 2
            or not all(entry_shape(entry) and "prevLine" not in entry for entry in entries)):
        return False
    if any(entry.get("runId") != entries[0].get("runId") for entry in entries):
        return False
    for before, after in zip(entries, entries[1:]):
        following = u64(before["seq"])
        following = following + 1 if following is not None and following + 1 < 2 ** 64 else None
        if u64(after["seq"]) != following:
            return False
    return len({entry["recordId"] for entry in entries}) == len(entries)


def line_link(raw):
    """The chain link of complete line `raw` as the App's reader examines it:
    MISSING for a line with none; None for a line the reader sets aside as
    unreadable or invalid, which is counted and whose link is not examined."""
    value = parsed(raw[:-1] if raw.endswith(b"\r") else raw)
    if isinstance(value, dict) and isinstance(value.get("format"), str) and value["format"] == GROUP_FORMAT:
        conforms = group_shape(value)
    else:
        conforms = entry_shape(value)
    return (value["prevLine"] if "prevLine" in value else MISSING) if conforms else None


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


def torn_and_named(no, raw, following):
    """Whether complete line `no` is a torn line that the complete line after it
    names, by its exact length and SHA-256, as a partial entry not recovered
    (record_lines.rs, parse_reader). Such a line is not a chain link: the next
    line links to the line before it. A whole, valid line is read as written
    even when a limit names it as torn."""
    if not following.endswith(b"\n"):
        return False
    following = following[:-1]
    try:
        text = following.decode("utf-8")
    except UnicodeError:
        text = None
    if text is not None and "\\" not in text and PARTIAL not in text:
        return False
    limit = parsed(following)
    body = member(limit, "body")
    named = member(body, "subjectRef") if isinstance(member(body, "subjectRef"), str) else ""
    if member(limit, "kind") != "evidence_limit" or member(body, "label") != PARTIAL:
        return False
    if named != f"line {no}; {len(raw)} bytes; sha256 {hashlib.sha256(raw).hexdigest()}":
        return False
    return line_link(raw) is None


def record_chain(data):
    """A record log's chain: the chain, every break in it as (line, reason),
    the lines counted without their link examined, and the torn lines set aside."""
    chain, broken, unexamined, torn = Chain(), [], [], []
    lines = data.split(b"\n")
    lines.pop()  # the unclosed final part: a partial, never a line of the chain
    for index, raw in enumerate(lines):
        no = index + 1
        following = lines[index + 1] + b"\n" if index + 1 < len(lines) else b""
        if torn_and_named(no, raw, following):
            torn.append(no)
            continue
        if all(byte in WHITESPACE for byte in raw):
            continue
        link = line_link(raw)
        if link is None:
            chain.count(raw)
            unexamined.append(no)
            continue
        why = chain.step(raw, link)
        if why:
            broken.append((no, why))
    return chain, broken, unexamined, torn


def account_chain(log, data, set_aside, torn):
    """A record log's chain followed by the package's own account of it (profile
    0.3): a line the account lists as set aside is counted and its link not
    examined; a torn line it lists is not counted, and the line after it must
    name it exactly; every other line must be readable JSON and is examined.
    Returns the chain and every break as (line, reason)."""
    chain, broken = Chain(), []
    lines = data.split(b"\n")
    lines.pop()  # the unclosed final part: a partial, never a line of the chain
    for listed in sorted(set_aside | torn):
        if listed > len(lines):
            raise ChainDisagreement(f"{log}: the package's account names line {listed}, and the log has {len(lines)} complete lines")
    for index, raw in enumerate(lines):
        no = index + 1
        if no in torn:
            # The App's reader takes the naming from the complete line after,
            # whatever it then makes of that line itself (it may set it aside
            # too): either way that line's bytes are held by the chain or by
            # the line after it in turn.
            following = parsed(lines[index + 1]) if index + 1 < len(lines) else NOT_JSON
            body = member(following, "body")
            if (member(following, "kind") != "evidence_limit" or member(body, "label") != PARTIAL
                    or member(body, "subjectRef") != f"line {no}; {len(raw)} bytes; sha256 {hashlib.sha256(raw).hexdigest()}"):
                raise ChainDisagreement(f"{log}: the package's account lists line {no} as a torn line the App closed, "
                                        "and the line after it does not name it by its exact length and SHA-256")
            continue
        if no in set_aside:
            chain.count(raw)
            continue
        if all(byte in WHITESPACE for byte in raw):
            continue
        entry = decoded(raw[:-1] if raw.endswith(b"\r") else raw)
        if entry is None:
            raise ChainDisagreement(f"{log}: line {no} is not a readable record, and the package's account does not list it as set aside")
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


ROLE_KINDS = ("torn final line", "unreadable line", "invalid observation", "duplicate observation identity", "sequence", "chain")


def role_chain(data):
    """The role supply log's chain as far as this verifier can read it
    (role_observations.rs, read_lines): every line whole, JSON, with a distinct
    observation identity, in sequence and linked. Returns the chain and the
    first fault as (line, kind), or None; the kinds are the App's (ROLE_KINDS).
    The App also validates each observation's format, which this verifier
    cannot: a fault of that kind is one it does not see."""
    chain, seen = Chain(), set()
    lines = data.split(b"\n")
    # The App's reader takes the lines in order, so it meets an unclosed final
    # part only after every complete line before it passed.
    unclosed = lines.pop() != b""
    for index, raw in enumerate(lines + ([None] if unclosed else [])):
        if raw is None:
            return chain, (index + 1, "torn final line")
        row = parsed(raw)
        if row is NOT_JSON:
            return chain, (index + 1, "unreadable line")
        if not (member(row, "format") == "chirality.role.supply" and member(row, "formatVersion") == "0.2"):
            identity, seq = member(row, "observationId"), member(row, "seq")
            if not isinstance(identity, str):
                return chain, (index + 1, "invalid observation")
            if identity in seen:
                return chain, (index + 1, "duplicate observation identity")
            seen.add(identity)
            if type(seq) is not int or seq != chain.lines + 1:
                return chain, (index + 1, "sequence")
        if chain.step(raw, row["prevLine"] if isinstance(row, dict) and "prevLine" in row else MISSING):
            return chain, (index + 1, "chain")
    return chain, None


def unread_role_log(log, head, chain, fault):
    """A role supply log the package records the App could not take. Returns
    (limit, compared): the integrity limit to report, and whether the recorded
    refusal was compared with the lines and agrees. Fails where the lines
    contradict the recorded refusal. The recorded state alone is never taken
    as agreement."""
    said = f"({head['state']}: {head.get('error')})"
    if fault is None and chain.lines == 0:
        raise ChainDisagreement(f"{log}: the package records that the App could not read this log {said}, but the log is empty, which the App reads")
    line, kind = head.get("line"), head.get("kind")
    carried = "its lines are carried as they stood and no chain head is established for it"
    if type(line) is not int or kind not in ROLE_KINDS:
        # No line and kind recorded (an earlier profile, or a refusal of the
        # file and not of a line): nothing here can be compared.
        return (f"{log}: the package records that the App could not read this log's chain when it was exported {said}; "
                "it does not record where, so this verifier cannot compare that with the lines; " + carried), False
    if fault is not None and fault[0] < line:
        raise ChainDisagreement(f"{log}: the package records the App's reader stopping at line {line} ({kind}), "
                                f"but line {fault[0]} already has a fault it stops at: {fault[1]}")
    if fault is not None and fault[0] == line and fault[1] == kind:
        return (f"{log}: the App could not read this log's chain when it was exported: line {line}, {kind} {said}; "
                "this verifier finds the same fault at the same line; " + carried), True
    if kind == "invalid observation":
        # The App validates each observation's format; this verifier cannot.
        return (f"{log}: the package records that the App refused this log at line {line} as an invalid observation {said}; "
                "this verifier does not hold the observation format and cannot compare that with the lines; " + carried), False
    found = "no fault it can see" if fault is None else f"line {fault[0]}: {fault[1]}"
    raise ChainDisagreement(f"{log}: the package records the App's reader stopping at line {line} ({kind}), and this verifier finds {found}")


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
        raise ChainDisagreement(f"{log}: recomputed chain head {chain.last} after {chain.lines} lines "
                                f"differs from the recorded head {head.get('head')} after {head.get('lines')} lines")
    facts = {"linked": chain.linked, "unchained": chain.unchained, "unchainedLimit": chain.unchained_limit(name)}
    for fact, value in facts.items():
        if fact not in head or type(head[fact]) is not type(value) or head[fact] != value:
            raise ChainDisagreement(f"{log}: the package records {fact} as {json.dumps(head.get(fact))}, and its lines give {json.dumps(value)}")


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
    notes, limited, limited_logs, recomputed, not_compared = [], [], set(), 0, []
    for log in expected:
        head = recorded[log]
        data = read_bytes(root / "data" / log)
        if hashlib.sha256(data).hexdigest() != names[log]:
            raise ValueError(f"{log}: log changed after its checksum was verified")
        if log == ROLE_LOG:
            chain, fault = role_chain(data)
            if "state" in head:
                limit, compared = unread_role_log(log, head, chain, fault)
                limited.append(limit)
                limited_logs.add(log)
                if not compared:
                    not_compared.append(log)
                continue
            if fault is not None:
                raise ChainDisagreement(f"{log}: line {fault[0]}: {fault[1]}; the package records a whole chain for this log")
            if profile == "0.3" and (listed_lines(log, head, "setAside") or listed_lines(log, head, "torn")):
                raise ChainDisagreement(f"{log}: the package's account sets lines of this log aside, and the App takes this log whole or not at all")
            compare_head(log, "role supply observations", head, chain, [])
            recomputed += 1
            notes.append(f"{log}: its chain is compared; this verifier does not hold the observation format, so it does not check "
                         "that each observation is one the App accepts")
        else:
            if "state" in head:
                # A record log's copy is readable here, so a recorded "unreadable" disagrees.
                raise ChainDisagreement(f"{log}: recorded at export as {head['state']}: {head.get('error')}")
            if profile == "0.3":
                unexamined, torn = sorted(listed_lines(log, head, "setAside")), sorted(listed_lines(log, head, "torn"))
                if set(unexamined) & set(torn):
                    raise ChainDisagreement(f"{log}: the package's account lists a line both as set aside and as torn")
                chain, broken = account_chain(log, data, set(unexamined), set(torn))
            else:
                chain, broken, unexamined, torn = record_chain(data)
            compare_head(log, PurePosixPath(log).name, head, chain, broken)
            recomputed += 1
            limited.extend(f"{log}: chain broken at line {no}: {why}; the package records it broken there when exported"
                           for no, why in broken)
            # A line set aside is a limit, never part of a clean result.
            limited.extend(f"{log}: line {no} was set aside by the App as invalid: it is not read as a record, and its own link is not examined"
                           for no in unexamined)
            if broken or unexamined:
                limited_logs.add(log)
            notes.extend(f"{log}: line {no} is a torn line the App closed and set aside after an interrupted write. It is not a limit: "
                         "the line after it names its exact length and SHA-256 and is itself "
                         + ("a torn line that the line after it names in turn" if no + 1 in torn else "in the chain") for no in torn)
        if chain.unchained:
            notes.append(f"{log}: unchained (legacy): {chain.unchained} lines before the chain starts carry no link"
                         if chain.linked else f"{log}: unchained (legacy): no line carries a chain link")
    if profile == "0.1" and ROLE_LOG in names:
        # Not checked is not clean: a log this verifier could not examine is
        # an integrity limit, never part of "no chain is broken".
        limited.append(f"{ROLE_LOG}: this package's legacy chain-head profile (0.1) records no head for this log, so its chain was not checked")
        limited_logs.add(ROLE_LOG)
        not_compared.append(ROLE_LOG)
    return {"profile": profile, "logs": len(expected), "recomputed": recomputed, "limited": limited,
            "limitedLogs": len(limited_logs), "notCompared": not_compared, "notes": notes}


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
    try:
        report = chains(root, payload)
    except ChainDisagreement as error:
        # Which profile the package is in decides what a chain failure can mean.
        heads = decoded(read_bytes(root / HEADS))
        error.profile = heads.get("formatVersion") if heads is not None else None
        raise
    if members(root) != all_files:
        raise ValueError("package changed during verification")
    return len(payload), "records-administration.json" in tags, report


LIMITED = 2  # exit status: bytes consistent, and a log's integrity is limited


def report_lines(count, administration, report):
    """What a person is told for a package that agrees with what it records.
    Separate statements, never one: whether the bytes agree with the manifests;
    which recorded heads were compared with the lines; and whether any log's
    own integrity is limited."""
    logs, recomputed, limited, notes = report["logs"], report["recomputed"], report["limited"], report["notes"]
    not_compared = report["notCompared"]
    lines = [f"Package bytes: consistent. {count} payload files and the export tags agree with the manifests."]
    if logs or not_compared:
        lines.append(f"Recorded chain heads: {recomputed} of {logs} compared with the lines, and each agrees." + (
            f" NOT COMPARED: {', '.join(not_compared)}. This verifier cannot establish that such a log is the one "
            "the package describes; the App can. Each is named under log integrity." if not_compared else ""))
    if limited or not_compared:
        # A head that was not compared is never a clean result, whatever else was found.
        faults, among = len(limited), report["limitedLogs"]
        lines.append(f"Log integrity: LIMITED. {faults} limit{'' if faults == 1 else 's'} in {among} log{'' if among == 1 else 's'}. "
                     "The store's own records were already limited there when this package was exported, and the package carries them as they stood:")
        lines.extend(f"  Integrity limit: {limit}" for limit in limited)
        lines.append("  A broken chain is reported and never repaired. Consistent bytes do not make these logs whole.")
        lines.append(f"Result: package bytes consistent; log integrity limited"
                     f"{'; ' + str(len(not_compared)) + ' recorded head' + ('' if len(not_compared) == 1 else 's') + ' not compared' if not_compared else ''} (exit status {LIMITED}).")
    elif logs == 0:
        # Nothing examined is said as nothing examined, not as a clean result.
        lines.append("Log integrity: nothing to check. This package carries no chained log.")
        lines.append("Result: package bytes consistent; no chained log in the package (exit status 0).")
    else:
        lines.append("Log integrity: no chain is broken and no line was set aside. Every link this verifier examined names the line before it." + (
            f" {len(notes)} note{'' if len(notes) == 1 else 's'} below name{'s' if len(notes) == 1 else ''} what that does not cover." if notes else ""))
        lines.append("Result: package bytes consistent; no chain is broken" + ("; see the notes" if notes else "") + " (exit status 0).")
    lines.extend(f"Note: {note}" for note in notes)
    lines.append("Protected prior administration bytes included." if administration
                 else "Administrative history unknown: legacy package has no retention snapshot.")
    lines.append("Unsigned: this shows that the package agrees with its own manifests and recorded chain heads. "
                 "A package whose records, manifests and chain heads were replaced together still verifies. "
                 "It does not show who produced the package, and it shows no human act.")
    return lines


if __name__ == "__main__":
    try:
        count, administration, report = verify(Path(sys.argv[1]))
    except ChainDisagreement as error:
        print(f"Result: failed (exit status 1). Verification failed: {error}", file=sys.stderr)
        if getattr(error, "profile", None) in ("0.1", "0.2"):
            print(CANNOT_TELL, file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError, IndexError, UnicodeError) as error:
        print(f"Result: failed (exit status 1). Verification failed: {error}", file=sys.stderr)
        sys.exit(1)
    print("\n".join(report_lines(count, administration, report)))
    sys.exit(LIMITED if report["limited"] or report["notCompared"] else 0)
