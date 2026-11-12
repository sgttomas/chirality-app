#!/usr/bin/env python3
"""Take in a supplier release archive and generate its protocol schema (DEL-01-01 OUT-002, OUT-004).

One run for one pin of capture.py's table `PINS`, writing into a new directory outside the
repository the files the repository keeps for that pin under `src-tauri/resources/supplier/<pin>/`:

  1. The archive's size and SHA-256 are compared with the table's, before anything is read from
     it. It is extracted without following or creating links (a member that is not a regular file
     or a directory, or whose path leaves the tree, refuses) into `vendor/`, the tree is
     inventoried, and `CANONICAL_DISTRIBUTION.json` is written. Nothing is executed.
  2. The tree is compared with that record, then the supplier's own generator is run for the
     stable and the experimental variant in the environment capture.py gives the supplier, with
     the same refusals for outside configuration and the same socket observer. `MANIFEST.sha256`,
     the two experimental bundles the App compiles in and `GENERATION.json` are written. A sample
     that shows a socket, or cannot be taken, refuses; sampling is not isolation.

A refusal at either step removes the output directory.

Usage, from `app/`:
  python3 supplier_checks/intake.py --archive /absolute/file.tar.gz --pin 0.167.2 \
      --out /absolute/new-directory

Fetching an archive is not this tool's act: a download needs the owner's permission
naming the file, its source and its size.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "packaging"))
import capture  # noqa: E402
import inventory  # noqa: E402

RECORD_FORMAT = "chirality.supplier-canonical-assessment/1"
GENERATION_FORMAT = "chirality.supplier-json-generation/1"
BUNDLES = ("codex_app_server_protocol.schemas.json", "codex_app_server_protocol.v2.schemas.json")
GENERATOR_TIMEOUT = 45
Refused = capture.Refused


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
    """The record of an extracted tree. `facts` is a row of capture.PINS; `pin` is only compared and recorded."""
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
    capture.metadata_members(record)  # the metadata may name only members of this inventory
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
    actual_digest = capture.sha256_file(archive)
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

    The process group's sockets are sampled every 0.1 s with capture.py's own observer. A sample is
    not isolation: a connection shorter than the interval can be missed.
    """
    process = subprocess.Popen(argv, cwd=cwd, env=environment, stdin=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    group, samples, end = os.getpgid(process.pid), 0, time.monotonic() + GENERATOR_TIMEOUT
    try:
        while process.poll() is None:
            rows = capture.socket_rows(group)
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
            capture.kill_group(group)
            process.wait()
    if process.returncode != 0:
        raise Refused("the generator exited with %d" % process.returncode)
    if not samples:
        raise Refused("the socket watch took no sample of the generator")
    return samples


def generate(vendor, record, out):
    """Step 2. Writes the generated basis of the tree the record describes into the existing `out`."""
    pin = record["pin"]
    _, codex_path = capture.verified_vendor(vendor, record)
    scratch = os.path.realpath(tempfile.mkdtemp(prefix="supplier-generate-"))
    try:
        outside = capture.outside_configuration(scratch)  # the generator's working directory
        homes = [os.path.join(scratch, name) for name in ("user-home", "home", "tmp")]
        for folder in homes:
            os.makedirs(folder)
        environment = capture.supplier_environment(codex_path, vendor, *homes)
        with open(os.path.join(environment["CODEX_HOME"], "config.toml"), "w") as handle:
            handle.write("[features]\nplugins = false\n\n[analytics]\nenabled = false\n")
        variants, lines = {}, []
        for variant, extra in (("experimental", ["--experimental"]), ("stable", [])):
            target = os.path.join(scratch, "generated", variant)
            # The entrypoint and path directory are admitted again immediately before each execution.
            capture.admitted_path(vendor, record, "pathDir")
            capture.outside_configuration(scratch)
            argv = [capture.admitted_path(vendor, record, "entrypoint"), "app-server", "generate-json-schema"]
            samples = run_generator(argv + extra + ["--out", target], environment, scratch)
            files = sorted(str(path.relative_to(target)) for path in Path(target).rglob("*") if path.is_file())
            missing = [name for name in BUNDLES if variant == "experimental" and name not in files]
            if not files or missing:
                # A generator that exits cleanly without its output generated nothing to record.
                raise Refused("the %s generator pass wrote %d files%s" % (
                    variant, len(files), "; missing " + ", ".join(missing) if missing else ""))
            rows = ["%s  json-schema/%s/%s\n" % (capture.sha256_file(os.path.join(target, name)), variant, name)
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
            bundles[name] = capture.sha256_file(os.path.join(folder, name))
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
    facts = capture.PINS.get(pin) if isinstance(pin, str) else None
    if facts is None:
        raise Refused("%r is not a pin of the table (%s)" % (pin, ", ".join(capture.PINS)))
    record = take_archive(archive, facts, pin, out)
    try:
        return record, generate(os.path.join(out, "vendor"), record, out)
    except BaseException as failure:
        remove_output(out, failure)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--archive", required=True)
    parser.add_argument("--pin", required=True, choices=sorted(capture.PINS))
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
