#!/usr/bin/env python3
"""Take in a supplier release archive and generate its protocol schema (DEL-01-01 OUT-002, OUT-004).

Two steps of a pin advance, each writing the files the repository keeps per pin under
`src-tauri/resources/supplier/<pin>/`, into a new directory outside the repository:

  archive   Check the archive's size and SHA-256 against the values the supplier
            publishes, before anything is read from it; extract it without following
            or creating links (a member that is not a regular file or a directory, or
            whose path leaves the tree, refuses); inventory the extracted tree; write
            `supplier/<pin>/CANONICAL_DISTRIBUTION.json`. Nothing is executed.
  generate  Compare the vendor tree with that record, then run the supplier's own
            generator for the stable and the experimental variant, in the same
            isolated environment capture.py uses and with its socket sample; write
            `supplier/<pin>/MANIFEST.sha256`, the two experimental bundles the App
            compiles in, and `GENERATION.json`. A generator that opens any socket
            refuses.

Usage, from `app/`:
  python3 supplier_checks/intake.py archive --archive /absolute/file.tar.gz --url URL \
      --size BYTES --sha256 HEX --pin 0.167.2 --out /absolute/new-directory
  python3 supplier_checks/intake.py generate --vendor /absolute/new-directory/vendor \
      --pin 0.167.2 --expected-root /absolute/new-directory/supplier --out /absolute/another-new-directory

Fetching an archive is not this tool's act: a download needs the owner's permission
naming the file, its source and its size.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import signal
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


def distribution_record(vendor, pin, archive_facts, source_commit=None):
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
    record = {"format": RECORD_FORMAT, "pin": pin}
    if source_commit:
        record["source_commit"] = source_commit
    record.update({
        "archive": archive_facts, "package_metadata": metadata,
        "files": scanned["files"], "macho_files": scanned["macho_files"],
        "inventory": {"method": "codex-vendor-tree-v1", "algorithm": "sha-256",
                      "manifest_sha256": scanned["manifest_sha256"], "entries": entries},
        "root_mode": "The container directory is not an archive member and its mode is not compared. "
                     "All %d declared file and directory member modes are compared." % len(entries),
        "limits": ["Static intake of a size- and digest-checked archive only.",
                   "No supplier execution, signature or trust reading, installed custody, product "
                   "qualification or notice coverage is established."]})
    return record


def take_archive(archive, url, size, digest, pin, out, source_commit=None):
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise Refused("the expected SHA-256 is not 64 lowercase hexadecimal characters")
    actual_size = os.path.getsize(archive)
    if actual_size != size:
        raise Refused("the archive is %d bytes, not the published %d" % (actual_size, size))
    actual_digest = capture.sha256_file(archive)
    if actual_digest != digest:
        raise Refused("the archive's SHA-256 is %s, not the published one" % actual_digest)
    os.makedirs(out)  # must be new
    try:
        vendor = os.path.join(out, "vendor")
        os.makedirs(vendor)
        extract(archive, vendor)
        record = distribution_record(vendor, pin, {"url": url, "size": size, "sha256": digest}, source_commit)
        os.makedirs(os.path.join(out, "supplier", pin))
        write_json(os.path.join(out, "supplier", pin, "CANONICAL_DISTRIBUTION.json"), record)
    except BaseException:
        shutil.rmtree(out, ignore_errors=True)  # this call made it; a refused intake leaves no tree behind
        raise
    return record


def run_generator(argv, environment, cwd):
    """Run one generator pass; any socket of its process group refuses."""
    process = subprocess.Popen(argv, cwd=cwd, env=environment, stdin=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    group, samples, end = os.getpgid(process.pid), 0, time.monotonic() + GENERATOR_TIMEOUT
    try:
        while process.poll() is None:
            listing = subprocess.run(["/usr/sbin/lsof", "-n", "-P", "-a", "-i", "-g", str(group)],
                                     capture_output=True, text=True).stdout
            samples += 1
            if listing.splitlines()[1:]:
                raise Refused("the generator opened a socket")
            if time.monotonic() > end:
                raise Refused("the generator did not finish in %d seconds" % GENERATOR_TIMEOUT)
            time.sleep(0.1)
    finally:
        if process.poll() is None:
            os.killpg(group, signal.SIGKILL)
            process.wait()
    if process.returncode != 0:
        raise Refused("the generator exited with %d" % process.returncode)
    return samples


def generate(vendor, pin, expected_root, out):
    record, binary, codex_path = capture.verified_vendor(vendor, pin, expected_root)
    os.makedirs(out)  # must be new
    scratch = os.path.realpath(tempfile.mkdtemp(prefix="supplier-generate-"))
    try:
        environment = {"LANG": "en_US.UTF-8", "PATH": codex_path + os.pathsep + capture.SYSTEM_PATH}
        for variable, name in (("HOME", "user-home"), ("CODEX_HOME", "home"), ("TMPDIR", "tmp")):
            environment[variable] = os.path.join(scratch, name)
            os.makedirs(environment[variable])
        with open(os.path.join(environment["CODEX_HOME"], "config.toml"), "w") as handle:
            handle.write("[features]\nplugins = false\n\n[analytics]\nenabled = false\n")
        variants, lines = {}, []
        for variant, extra in (("experimental", ["--experimental"]), ("stable", [])):
            target = os.path.join(scratch, "generated", variant)
            argv = [binary, "app-server", "generate-json-schema"] + extra + ["--out", target]
            samples = run_generator(argv, environment, scratch)
            files = sorted(str(path.relative_to(target)) for path in Path(target).rglob("*") if path.is_file())
            rows = ["%s  json-schema/%s/%s\n" % (capture.sha256_file(os.path.join(target, name)), variant, name)
                    for name in files]
            lines += rows
            variants[variant] = {
                "argv": ["<vendor>/bin/codex", "app-server", "generate-json-schema"] + extra
                        + ["--out", "<output>/" + variant],
                "exit_code": 0, "timeout_seconds": GENERATOR_TIMEOUT, "files": len(files),
                "bytes": sum(os.path.getsize(os.path.join(target, name)) for name in files),
                "manifest_sha256": hashlib.sha256("".join(rows).encode("utf-8")).hexdigest(),
                "socket_samples": samples, "sockets_seen": 0}
        folder = os.path.join(out, "supplier", pin)
        os.makedirs(folder)
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
                            "network": "the generator's sockets were sampled and none was seen"},
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    archive = commands.add_parser("archive")
    for name in ("--archive", "--url", "--sha256", "--pin", "--out"):
        archive.add_argument(name, required=True)
    archive.add_argument("--size", required=True, type=int)
    archive.add_argument("--source-commit")
    generator = commands.add_parser("generate")
    for name in ("--vendor", "--pin", "--out"):
        generator.add_argument(name, required=True)
    generator.add_argument("--expected-root", help="directory holding <pin>/CANONICAL_DISTRIBUTION.json; "
                                                   "the repository's supplier resources by default")
    args = parser.parse_args(argv)
    try:
        if args.command == "archive":
            record = take_archive(args.archive, args.url, args.size, args.sha256, args.pin, args.out,
                                  args.source_commit)
            print(json.dumps({"pin": args.pin, "files": record["files"], "macho_files": record["macho_files"],
                              "manifest_sha256": record["inventory"]["manifest_sha256"]}))
        else:
            generation = generate(args.vendor, args.pin, args.expected_root, args.out)
            print(json.dumps({"pin": args.pin, "manifest_sha256": generation["manifest_sha256"],
                              "bundles": generation["compiled_experimental_bundles"]}))
        return 0
    except FileExistsError:
        sys.stderr.write("refused: the output directory already exists\n")
    except Refused as refusal:
        sys.stderr.write("refused: %s\n" % refusal)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
