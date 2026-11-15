#!/usr/bin/env python3
"""Take in a supplier release archive and generate its protocol schema (DEL-01-01 OUT-002, OUT-004).

One run for one pin of the table `PINS` below, writing into a new directory outside the
repository the files the repository keeps for that pin under `src-tauri/resources/supplier/<pin>/`:

  1. The archive's size and SHA-256 are compared with the table's, before anything is read from
     it. It is extracted without following or creating links (a member that is not a regular file
     or a directory, or whose path leaves the tree, refuses) into `vendor/`, the tree is
     inventoried, and `CANONICAL_DISTRIBUTION.json` is written. Nothing is executed.
  2. The tree is compared with that record, then the supplier's own generator is run for the
     stable and the experimental variant. `MANIFEST.sha256`, the two experimental bundles the App
     compiles in and `GENERATION.json` are written.

A refusal at either step removes the output directory.

A pin is a key of `PINS` and nothing else: the pins that have a consumer today, each with its
release archive's address, size, SHA-256 and source commit. No path is built from a caller's
text; adding a pin is a reviewed change to the table.

What the generator is given is six variables only (HOME, CODEX_HOME and TMPDIR in a fresh
scratch directory, PATH, LANG and TZ=UTC), and the entrypoint and path directory the package
metadata names are admitted only as members of the verified inventory, again immediately
before each execution. Before each execution the run refuses when configuration from outside
the fresh homes could reach the supplier: a `.git` or `.codex` entry in any ancestor of the
scratch working directory, the system folder `/etc/codex`, or a managed preference the supplier
reads. These are controls on what the supplier is given, not a sandbox. The generator's sockets
are sampled while it runs; a sample that shows a socket, or cannot be taken, refuses, and
sampling is not network isolation.

These are operator-run steps on stable inputs. They are built so that a check that was not
made or that failed cannot come out as a distribution record or a generated basis. They are
not built to withstand a writer changing the inputs during the run, nor someone with write
access forging a record.

Usage, from `app/`:
  python3 supplier_checks/intake.py --archive /absolute/file.tar.gz --pin 0.167.2 \
      --out /absolute/new-directory

Fetching an archive is not this tool's act: a download needs the owner's permission
naming the file, its source and its size.
"""
import argparse
import ctypes
import hashlib
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "packaging"))
import inventory  # noqa: E402

RECORD_FORMAT = "chirality.supplier-canonical-assessment/1"
GENERATION_FORMAT = "chirality.supplier-json-generation/1"
BUNDLES = ("codex_app_server_protocol.schemas.json", "codex_app_server_protocol.v2.schemas.json")
GENERATOR_TIMEOUT = 45


# ---------- pins, the verified tree and what the supplier is given ----------
class Refused(Exception):
    pass


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


RESOURCES = HERE.parent / "src-tauri/resources/supplier"
# The pins with a consumer today, each with the release archive the supplier publishes for this
# platform. A pin is admitted only as a key of this table, so no path is built from a caller's text.
# Adding a pin is a change to this table, reviewed with the records it brings.
PINS = {
    "0.167.0": {
        "url": "https://github.com/openai/codex/releases/download/rust-v0.167.0/"
               "codex-package-aarch64-apple-darwin.tar.gz",
        "size": 166340155,
        "sha256": "af45ed45d940d7998809622c1c0296d3098ed7d7fad695284422c228bd454517",
        "source_commit": "086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a"},
    "0.167.2": {
        "url": "https://github.com/openai/codex/releases/download/rust-v0.167.2/"
               "codex-package-aarch64-apple-darwin.tar.gz",
        "size": 166599161,
        "sha256": "e791290651bce41938fb160b5de2bd9ff8bcf3401ca3e236c73f485fca4be1bb",
        "source_commit": "ce21072c90d32c40af7a55b60b2fb35c84a43a6a"},
}


def expected_distribution(pin):
    """The committed distribution record of a pin of the table, naming the table's archive, or a refusal."""
    name = next((key for key in PINS if key == pin), None)
    if name is None:
        raise Refused("%r is not a pin of the table (%s)" % (pin, ", ".join(PINS)))
    try:
        record = json.loads((RESOURCES / name / "CANONICAL_DISTRIBUTION.json").read_bytes())
    except (OSError, ValueError):
        raise Refused("no expected distribution is committed for pin %s" % name) from None
    facts = PINS[name]
    if (not isinstance(record, dict) or record.get("pin") != name
            or (record.get("package_metadata") or {}).get("version") != name
            or record.get("archive") != {key: facts[key] for key in ("url", "size", "sha256")}
            or record.get("source_commit") != facts["source_commit"]):
        raise Refused("the committed distribution record of %s does not name the table's pin and archive" % name)
    return record


def vendor_differences(vendor, inventory):
    """Every difference between the tree at `vendor` and the expected member inventory."""
    expected = {entry["path"]: entry for entry in inventory["entries"]}
    differences, seen = [], set()
    for folder, directories, files in os.walk(vendor, followlinks=False):
        for name in directories + files:
            path = os.path.join(folder, name)
            relative = os.path.relpath(path, vendor)
            seen.add(relative)
            entry, status = expected.get(relative), os.lstat(path)
            if entry is None:
                differences.append("extra: " + relative)
            elif stat.S_ISLNK(status.st_mode) or not (
                    stat.S_ISDIR(status.st_mode) if entry["kind"] == "dir" else stat.S_ISREG(status.st_mode)):
                differences.append("type: " + relative)
            elif stat.S_IMODE(status.st_mode) != entry["mode"]:
                differences.append("mode: " + relative)
            elif entry["kind"] == "file" and (status.st_size != entry["size"]
                                              or sha256_file(path) != entry["sha256"]):
                differences.append("content: " + relative)
    differences += ["missing: " + path for path in expected if path not in seen]
    return sorted(differences)


METADATA_MEMBERS = {"entrypoint": "file", "execServer": "file", "pathDir": "dir", "resourcesDir": "dir"}
def metadata_members(record):
    """The package metadata's paths, each admitted only as a member of the record's own inventory.

    Returns {field: relative path}. A path that is absolute, has a `.` or `..` part, or is not an
    inventory member of the expected kind refuses, so nothing the metadata says can name a path
    outside the tree the inventory describes.
    """
    members = {entry["path"]: entry for entry in record["inventory"]["entries"]}
    admitted = {}
    for field, kind in METADATA_MEMBERS.items():
        value = record["package_metadata"].get(field)
        if value is None and field not in ("entrypoint", "pathDir"):
            continue
        parts = value.split("/") if isinstance(value, str) else [""]
        entry = members.get(value) if isinstance(value, str) else None
        if (not isinstance(value, str) or value.startswith("/") or any(part in ("", ".", "..") for part in parts)
                or os.pathsep in value or "\x00" in value or entry is None or entry["kind"] != kind):
            raise Refused("package metadata %s %r is not a %s of the verified inventory" % (field, value, kind))
        if field == "entrypoint" and not entry["mode"] & 0o100:
            raise Refused("package metadata entrypoint %r is not executable in the inventory" % value)
        admitted[field] = value
    return admitted


def admitted_path(vendor, record, field):
    """Resolve one metadata path at the moment of use, or refuse.

    The path must still be a member of the inventory, every component beneath the vendor root must
    be a real directory or file and not a link, the result must lie inside the vendor root, and a
    file's bytes must still equal the inventory's digest.
    """
    relative = metadata_members(record)[field]
    root = os.path.realpath(vendor)
    path = root
    for part in relative.split("/"):
        path = os.path.join(path, part)
        if os.path.islink(path):
            raise Refused("%s passes through a link: %s" % (field, relative))
    if os.path.realpath(path) != path or os.path.commonpath([root, path]) != root or path == root:
        raise Refused("%s does not resolve inside the verified tree: %s" % (field, relative))
    entry = next(entry for entry in record["inventory"]["entries"] if entry["path"] == relative)
    status = os.lstat(path)
    if entry["kind"] == "dir":
        if not stat.S_ISDIR(status.st_mode):
            raise Refused("%s is no longer a directory: %s" % (field, relative))
    elif (not stat.S_ISREG(status.st_mode) or stat.S_IMODE(status.st_mode) != entry["mode"]
          or status.st_size != entry["size"] or sha256_file(path) != entry["sha256"]):
        raise Refused("%s no longer equals the verified inventory: %s" % (field, relative))
    return path


def verified_vendor(vendor, record):
    """Return (entrypoint, path directory) of a tree equal to the record's inventory, or refuse.

    Nothing is executed here.
    """
    metadata_members(record)
    vendor = os.path.realpath(vendor)
    if not os.path.isdir(vendor):
        raise Refused("the vendor tree is not a directory")
    differences = vendor_differences(vendor, record["inventory"])
    if differences:
        raise Refused("the vendor tree differs from the expected %s inventory: %s%s" % (
            record["pin"], "; ".join(differences[:6]),
            "; %d more" % (len(differences) - 6) if len(differences) > 6 else ""))
    return admitted_path(vendor, record, "entrypoint"), admitted_path(vendor, record, "pathDir")


SYSTEM_CONFIGURATION = "/etc/codex"
PREFERENCE_DOMAIN, PREFERENCE_KEYS = b"com.openai.codex", (b"config_toml_base64", b"requirements_toml_base64")
def managed_preference_present():
    """Whether a managed preference the supplier reads is set. Presence only: the value is released unread.

    The same domain and keys as the App's own guard (native_local_provider.rs). A call that cannot
    be made raises OSError.
    """
    foundation = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
    foundation.CFStringCreateWithCString.restype = ctypes.c_void_p
    foundation.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
    foundation.CFPreferencesCopyAppValue.restype = ctypes.c_void_p
    foundation.CFPreferencesCopyAppValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    foundation.CFRelease.argtypes = [ctypes.c_void_p]

    def string(text):
        value = foundation.CFStringCreateWithCString(None, text, 0x08000100)
        if not value:
            raise OSError("CoreFoundation made no string")
        return value
    domain, present = string(PREFERENCE_DOMAIN), False
    try:
        for name in PREFERENCE_KEYS:
            key = string(name)
            try:
                value = foundation.CFPreferencesCopyAppValue(key, domain)
                if value:
                    foundation.CFRelease(value)
                    present = True
            finally:
                foundation.CFRelease(key)
    finally:
        foundation.CFRelease(domain)
    return present


def outside_configuration(workspace, preference=None, system=SYSTEM_CONFIGURATION):
    """Refuse when configuration from outside the fresh homes could reach the supplier; return the checks made.

    The supplier reads `.codex/config.toml` from its working directory's ancestors up to a project
    root (a `.git` entry), the system folder, and on macOS managed preferences, whatever HOME and
    CODEX_HOME say. Each is checked by presence alone and nothing is opened. A check that cannot be
    made refuses; one that does not apply on this platform is named as not checked.
    """
    def present(path):
        try:
            os.lstat(path)
        except FileNotFoundError:
            return False
        except OSError as error:
            raise Refused("%s could not be checked (%s)" % (path, type(error).__name__)) from None
        return True
    folder = os.path.realpath(workspace)
    if folder != workspace:
        raise Refused("the supplier's working directory is not a plain path")
    ancestors = 0
    while True:
        for name in (".git", ".codex"):
            if present(os.path.join(folder, name)):
                raise Refused("%s holds a %s entry, whose settings the supplier would read; "
                              "set TMPDIR outside any project" % (folder, name))
        ancestors += 1
        if os.path.dirname(folder) == folder:
            break
        folder = os.path.dirname(folder)
    if present(system):
        raise Refused("%s exists, and the supplier reads system configuration from it" % system)
    if preference is None and sys.platform != "darwin":
        managed = "not checked: the supplier reads managed preferences on macOS only"
    else:
        try:
            found = (preference or managed_preference_present)()
        except OSError as error:
            raise Refused("managed preferences could not be checked (%s)" % type(error).__name__) from None
        if found is not False:
            raise Refused("a managed preference of %s is set, and the supplier reads it" % PREFERENCE_DOMAIN.decode())
        managed = "absent"
    return {"working_directory_ancestors": "%d checked, none holds .git or .codex" % ancestors,
            "system_configuration_folder": "absent", "managed_preferences": managed,
            "note": "presence checks before execution; controls on what the supplier is given, not a sandbox"}


SYSTEM_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
def supplier_environment(path_directory, vendor, user_home, codex_home, tmp):
    """The whole environment the supplier is given: six variables, built here and not inherited.

    PATH is the admitted path directory followed by the fixed system directories, and is checked
    after composition: exactly those entries, the first inside the vendor root.
    """
    path = path_directory + os.pathsep + SYSTEM_PATH
    entries, root = path.split(os.pathsep), os.path.realpath(vendor)
    if (entries != [path_directory] + SYSTEM_PATH.split(os.pathsep) or not os.path.isabs(path_directory)
            or os.path.commonpath([root, path_directory]) != root or path_directory == root):
        raise Refused("the supplier's PATH would name a directory other than the admitted one")
    for name, value in (("HOME", user_home), ("CODEX_HOME", codex_home), ("TMPDIR", tmp)):
        if not os.path.isabs(value) or os.pathsep in value or os.path.realpath(value) != value:
            raise Refused("the supplier's %s is not a plain private directory" % name)
    # TZ is fixed so that nothing made here depends on the clock setting of its host.
    return {"HOME": user_home, "CODEX_HOME": codex_home, "TMPDIR": tmp, "PATH": path, "LANG": "en_US.UTF-8",
            "TZ": "UTC"}


OBSERVER_TIMEOUT = 20
def kill_group(group):
    """SIGKILL a process group that may already be gone.

    A group whose members have all exited and await reaping answers EPERM on macOS, and a reaped
    one answers ESRCH; both mean there is nothing left to kill.
    """
    try:
        os.killpg(group, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def socket_rows(group, run=subprocess.run):
    """lsof's rows for the process group's internet sockets, or None when no sample could be taken.

    lsof exits 1 with no output when nothing matches, which is a taken sample with no socket. Any
    other failure, output on its error stream, or no answer in time, is not a sample.
    """
    try:
        result = run(["/usr/sbin/lsof", "-n", "-P", "-a", "-i", "-g", str(group)], capture_output=True, text=True,
                     timeout=OBSERVER_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None
    rows = result.stdout.splitlines()[1:]
    if result.stderr.strip() or result.returncode not in (0, 1) or (result.returncode == 1 and rows):
        return None
    return rows


# ---------- intake ----------

def write_json(path, value):
    with open(path, "x") as handle:
        handle.write(json.dumps(value, indent=1, ensure_ascii=False) + "\n")


def member_path(name):
    path = PurePosixPath(name)
    parts = [part for part in path.parts if part != "."]
    if path.is_absolute() or not parts or ".." in parts or any("\n" in part or "\r" in part for part in parts):
        raise Refused("archive member path is not a plain relative path: %r" % name)
    return "/".join(parts)


def extract(archive, destination):
    """Extract regular files and directories only, with their recorded modes."""
    modes, seen = {}, set()
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar:
            if not (member.isreg() or member.isdir()):
                raise Refused("archive member is not a regular file or a directory: %r" % member.name)
            relative = member_path(member.name)
            if relative in seen:
                raise Refused("archive names a member twice: %r" % relative)
            seen.add(relative)
            target = os.path.join(destination, relative)
            if member.isdir():
                os.makedirs(target, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target), exist_ok=True)
                source = tar.extractfile(member)
                with open(target, "xb") as handle:
                    shutil.copyfileobj(source, handle, 1 << 20)
            modes[target] = member.mode & 0o777
    for target, mode in sorted(modes.items(), key=lambda pair: len(pair[0]), reverse=True):
        os.chmod(target, mode)
    return len(seen)


def distribution_record(vendor, pin, facts):
    """The record of an extracted tree. `facts` is a row of PINS; `pin` is only compared and recorded."""
    scanned = inventory.scan(vendor)
    if any(entry["kind"] not in ("file", "dir") for entry in scanned["entries"]):
        raise Refused("the extracted tree holds a link or special file")
    try:
        metadata = json.loads(Path(vendor, "codex-package.json").read_bytes())
    except (OSError, ValueError):
        raise Refused("the tree has no readable codex-package.json") from None
    if metadata.get("version") != pin:
        raise Refused("the package metadata names version %r, not %s" % (metadata.get("version"), pin))
    entries = []
    for entry in scanned["entries"]:
        row = {"path": entry["path"], "kind": entry["kind"], "mode": int(entry["mode"], 8)}
        if entry["kind"] == "file":
            row.update(size=entry["size"], sha256=entry["sha256"])
        entries.append(row)
    record = {"format": RECORD_FORMAT, "pin": pin, "source_commit": facts["source_commit"]}
    record.update({
        "archive": {key: facts[key] for key in ("url", "size", "sha256")}, "package_metadata": metadata,
        "files": scanned["files"], "macho_files": scanned["macho_files"],
        "inventory": {"method": "codex-vendor-tree-v1", "algorithm": "sha-256",
                      "manifest_sha256": scanned["manifest_sha256"], "entries": entries},
        "root_mode": "The container directory is not an archive member and its mode is not compared. "
                     "All %d declared file and directory member modes are compared." % len(entries),
        "limits": ["Static intake of a size- and digest-checked archive only.",
                   "No supplier execution, signature or trust reading, installed custody, product "
                   "qualification or notice coverage is established."]})
    metadata_members(record)  # the metadata may name only members of this inventory
    return record


def remove_output(out, failure):
    """Remove an output directory this run made. Extracted directories keep the archive's modes,
    which may forbid removal, so they are made writable first."""
    for folder, _, _ in os.walk(out):
        os.chmod(folder, 0o700)
    shutil.rmtree(out, ignore_errors=True)
    if os.path.lexists(out):
        raise Refused("%s; and the partial output could not be removed: %s" % (failure, out)) from None


def take_archive(archive, facts, pin, out):
    """Step 1. Writes `out/vendor` and `out/CANONICAL_DISTRIBUTION.json`; `out` must be new."""
    if not re.fullmatch(r"[0-9a-f]{64}", facts["sha256"]):
        raise Refused("the expected SHA-256 is not 64 lowercase hexadecimal characters")
    actual_size = os.path.getsize(archive)
    if actual_size != facts["size"]:
        raise Refused("the archive is %d bytes, not the published %d" % (actual_size, facts["size"]))
    actual_digest = sha256_file(archive)
    if actual_digest != facts["sha256"]:
        raise Refused("the archive's SHA-256 is %s, not the published one" % actual_digest)
    os.makedirs(out)  # must be new
    try:
        vendor = os.path.join(out, "vendor")
        os.makedirs(vendor)
        extract(archive, vendor)
        record = distribution_record(vendor, pin, facts)
        write_json(os.path.join(out, "CANONICAL_DISTRIBUTION.json"), record)
    except BaseException as failure:
        remove_output(out, failure)  # a refused intake leaves no tree behind
        raise
    return record


def run_generator(argv, environment, cwd):
    """Run one generator pass; a sample that shows a socket, or cannot be taken, refuses.

    The process group's sockets are sampled every 0.1 s with py's own observer. A sample is
    not isolation: a connection shorter than the interval can be missed.
    """
    process = subprocess.Popen(argv, cwd=cwd, env=environment, stdin=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    group, samples, end = os.getpgid(process.pid), 0, time.monotonic() + GENERATOR_TIMEOUT
    try:
        while process.poll() is None:
            rows = socket_rows(group)
            if rows is None:
                # Every sample that could not be taken refuses, also one that coincides with the exit.
                raise Refused("the socket watch could not take a sample")
            if rows:
                raise Refused("the generator opened a socket")
            samples += 1
            if time.monotonic() > end:
                raise Refused("the generator did not finish in %d seconds" % GENERATOR_TIMEOUT)
            time.sleep(0.1)
    finally:
        if process.poll() is None:
            kill_group(group)
            process.wait()
    if process.returncode != 0:
        raise Refused("the generator exited with %d" % process.returncode)
    if not samples:
        raise Refused("the socket watch took no sample of the generator")
    return samples


def generate(vendor, record, out):
    """Step 2. Writes the generated basis of the tree the record describes into the existing `out`."""
    pin = record["pin"]
    _, codex_path = verified_vendor(vendor, record)
    scratch = os.path.realpath(tempfile.mkdtemp(prefix="supplier-generate-"))
    try:
        outside = outside_configuration(scratch)  # the generator's working directory
        homes = [os.path.join(scratch, name) for name in ("user-home", "home", "tmp")]
        for folder in homes:
            os.makedirs(folder)
        environment = supplier_environment(codex_path, vendor, *homes)
        with open(os.path.join(environment["CODEX_HOME"], "config.toml"), "w") as handle:
            handle.write("[features]\nplugins = false\n\n[analytics]\nenabled = false\n")
        variants, lines = {}, []
        for variant, extra in (("experimental", ["--experimental"]), ("stable", [])):
            target = os.path.join(scratch, "generated", variant)
            # The entrypoint and path directory are admitted again immediately before each execution.
            admitted_path(vendor, record, "pathDir")
            outside_configuration(scratch)
            argv = [admitted_path(vendor, record, "entrypoint"), "app-server", "generate-json-schema"]
            samples = run_generator(argv + extra + ["--out", target], environment, scratch)
            files = sorted(str(path.relative_to(target)) for path in Path(target).rglob("*") if path.is_file())
            missing = [name for name in BUNDLES if variant == "experimental" and name not in files]
            if not files or missing:
                # A generator that exits cleanly without its output generated nothing to record.
                raise Refused("the %s generator pass wrote %d files%s" % (
                    variant, len(files), "; missing " + ", ".join(missing) if missing else ""))
            rows = ["%s  json-schema/%s/%s\n" % (sha256_file(os.path.join(target, name)), variant, name)
                    for name in files]
            lines += rows
            variants[variant] = {
                "argv": ["<vendor>/bin/codex", "app-server", "generate-json-schema"] + extra
                        + ["--out", "<output>/" + variant],
                "exit_code": 0, "timeout_seconds": GENERATOR_TIMEOUT, "files": len(files),
                "bytes": sum(os.path.getsize(os.path.join(target, name)) for name in files),
                "manifest_sha256": hashlib.sha256("".join(rows).encode("utf-8")).hexdigest(),
                "socket_samples": samples, "failed_samples": 0, "sockets_seen": 0}
        folder = out
        manifest = "".join(lines).encode("utf-8")
        with open(os.path.join(folder, "MANIFEST.sha256"), "xb") as handle:
            handle.write(manifest)
        bundles = {}
        for name in BUNDLES:
            shutil.copyfile(os.path.join(scratch, "generated", "experimental", name), os.path.join(folder, name))
            bundles[name] = sha256_file(os.path.join(folder, name))
        main = next(entry for entry in record["inventory"]["entries"]
                    if entry["path"] == record["package_metadata"]["entrypoint"])
        generation = {
            "format": GENERATION_FORMAT, "pin": pin,
            "supplier": {"source": "official release archive " + record["archive"]["url"],
                         "archive_sha256": record["archive"]["sha256"], "main_sha256": main["sha256"],
                         "tree_manifest_sha256": record["inventory"]["manifest_sha256"],
                         "verified": "complete vendor tree equal to the expected inventory before execution"},
            "environment": {"inherit_environment": False, "allowlist": sorted(environment),
                            "homes": "fresh private HOME, CODEX_HOME and TMPDIR; plugins and analytics off",
                            "outside_configuration": outside,
                            "network": "the generator's sockets were sampled every 0.1 s and no sample showed "
                                       "one; a sample is not isolation"},
            "variants": variants, "compiled_experimental_bundles": bundles,
            "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
            "limits": ["One generator pass per variant; determinism is not assessed.",
                       "JSON schema generation only; no TypeScript generation, session, turn, sign-in or "
                       "provider connection.",
                       "A generated basis is not qualification of the pin."]}
        write_json(os.path.join(folder, "GENERATION.json"), generation)
        return generation
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def take_in(archive, pin, out):
    """Both steps for one pin of the table. Returns (record, generation); a refusal leaves no output."""
    facts = PINS.get(pin) if isinstance(pin, str) else None
    if facts is None:
        raise Refused("%r is not a pin of the table (%s)" % (pin, ", ".join(PINS)))
    record = take_archive(archive, facts, pin, out)
    try:
        return record, generate(os.path.join(out, "vendor"), record, out)
    except BaseException as failure:
        remove_output(out, failure)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--archive", required=True)
    parser.add_argument("--pin", required=True, choices=sorted(PINS))
    parser.add_argument("--out", required=True, help="a new directory outside the repository")
    args = parser.parse_args(argv)
    try:
        record, generation = take_in(args.archive, args.pin, args.out)
        print(json.dumps({"pin": args.pin, "files": record["files"], "macho_files": record["macho_files"],
                          "inventory_manifest_sha256": record["inventory"]["manifest_sha256"],
                          "generated_manifest_sha256": generation["manifest_sha256"],
                          "bundles": generation["compiled_experimental_bundles"]}))
        return 0
    except FileExistsError:
        sys.stderr.write("refused: the output directory already exists\n")
    except Refused as refusal:
        sys.stderr.write("refused: %s\n" % refusal)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
