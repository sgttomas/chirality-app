"""Bundle every workflow of the selected Chirality Library release into the App.

The release archive is the only source. It is read whole, refused unless its
size and SHA-256 equal the project's reference record of the selected release,
and its own method index decides which folders are workflows. Nothing is read
from an extracted folder and nothing is fetched.

    python3 -m tools.library_workflows generate --archive <release .tar>
    python3 -m tools.library_workflows compare  --archive <release .tar>
    python3 -m tools.library_workflows verify

`generate` writes the bundled tree and its manifest. `compare` reports every
difference between the committed tree and the release without writing.
`verify` needs no archive: it checks the committed tree against its manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import posixpath
import re
import struct
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# The selected edition. Changing it is a deliberate App change (AGENTS.md).
SELECTION = "reference/library-v3.4.0/MANIFEST.json"
OUTPUT = "app/src-tauri/resources/production_workflows"
MANIFEST_NAME = "MANIFEST.json"
INDEX_PATH = "workflows/index.json"
INDEX_SCHEMA = "chirality-method-index/v1"
LICENSE_PATH = "LICENSE.md"
STANDING = "production bundle candidate; not a published release"
# DEL-02-01's revision method, restated here so that this tool imports no
# product code: a digest computed here is an independent reading of the bytes.
REVISION_METHOD = "chirality.app.workflow-package.sha256/v1"
PACKAGE_MAX_FILES = 1000
PACKAGE_MAX_BYTES = 16 * 1024 * 1024
OS_ENTRIES = {
    ".DS_Store", "Thumbs.db", "desktop.ini", "Icon\r", ".localized",
    ".Spotlight-V100", ".Trashes", ".fseventsd", "__MACOSX",
}


# Where a path written from the Library's root may point: its tools, skills,
# role files and documents. A path written as a relative link is resolved from
# the file that names it and may point anywhere in the release.
LIBRARY_ROOTS = ("tools/", ".agents/skills/", "agents/", "docs/")
PATH_TOKEN = re.compile(r"[A-Za-z0-9_.\-/]+")


class BundleError(Exception):
    """The release or the tree is not what the bundle may be built from."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def revision(files: dict[str, bytes]) -> str:
    """The package revision: every regular file, ordered by its path's bytes."""
    digest = hashlib.sha256()
    digest.update(REVISION_METHOD.encode("ascii") + b"\0")
    digest.update(struct.pack(">Q", len(files)))
    for path in sorted(files, key=lambda p: p.encode("utf-8")):
        name = path.encode("utf-8")
        digest.update(struct.pack(">Q", len(name)) + name)
        digest.update(struct.pack(">Q", len(files[path])))
        digest.update(files[path])
    return digest.hexdigest()


def valid_name(name: str) -> bool:
    parts = name.split("-")
    return 0 < len(name) <= 64 and all(
        part and all(c.isascii() and (c.islower() or c.isdigit()) for c in part)
        for part in parts
    )


def check_package(name: str, files: dict[str, bytes]) -> None:
    """The App's own package rules (DEL-02-02 review hygiene), applied here so
    that a release the App would refuse never reaches the tree."""
    if not valid_name(name):
        raise BundleError(f"{name}: not a workflow name the App admits")
    if "WORKFLOW.md" not in files:
        raise BundleError(f"{name}: no WORKFLOW.md")
    try:
        files["WORKFLOW.md"].decode("utf-8")
    except UnicodeDecodeError:
        raise BundleError(f"{name}: WORKFLOW.md is not UTF-8") from None
    if len(files) > PACKAGE_MAX_FILES or sum(map(len, files.values())) > PACKAGE_MAX_BYTES:
        raise BundleError(f"{name}: package exceeds 1000 files or 16 MiB")
    for path in files:
        parts = path.split("/")
        if not path or any(part in ("", ".", "..") for part in parts) or "\\" in path:
            raise BundleError(f"{name}: path not package-relative: {path!r}")
        if any(part in OS_ENTRIES or part.startswith("._") for part in parts):
            raise BundleError(f"{name}: operating-system entry {path!r}")


def library_paths_named(
    name: str, package: dict[str, bytes], release: set[str], bundled: set[str]
) -> list[str]:
    """The release paths this package's files name that are outside the App.

    A path counts only when it exists in the release archive, as a file or a
    folder, and is neither in this package nor in another bundled workflow.
    It is read two ways and no other: a relative link, resolved from the file
    that names it; and a path written from the Library's root under one of
    LIBRARY_ROOTS, after any prefix (`$INSTRUCTION_ROOT/tools/...`). A name
    that is not a path (a skill or tool named in prose, a Python module) is
    not counted, and neither is the rest of a URL. This says what the text
    names; it does not say what a run needs.
    """
    inside = set(package)
    for path in package:
        parts = path.split("/")
        inside.update("/".join(parts[:i]) for i in range(1, len(parts)))
    named: set[str] = set()

    def outside_the_app(path: str) -> bool:
        parts = path.split("/")
        in_a_package = parts[0] == "workflows" and len(parts) > 1 and parts[1] in bundled
        return path in release and not in_a_package

    for source, data in package.items():
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        folder = posixpath.dirname(f"workflows/{name}/{source}")
        for token in PATH_TOKEN.findall(text):
            if "/" not in token or token.startswith("//"):
                continue
            token = token.rstrip("./").removeprefix("./")
            if not token:
                continue
            local = posixpath.normpath(posixpath.join(posixpath.dirname(source), token))
            if token in inside or local in inside:
                continue
            if token.startswith("../"):
                target = posixpath.normpath(posixpath.join(folder, token))
                if not target.startswith("../") and "/" in target + "/" and outside_the_app(target):
                    named.add(target)
                continue
            parts = token.split("/")
            for start in range(len(parts) - 1):
                candidate = "/".join(parts[start:])
                if candidate.startswith(LIBRARY_ROOTS):
                    if outside_the_app(candidate):
                        named.add(candidate)
                    break
    return sorted(named, key=lambda p: p.encode("utf-8"))


def read_selection(root: Path = ROOT) -> dict:
    record = json.loads((root / SELECTION).read_text(encoding="utf-8"))
    archive = record["published_archive"]
    return {
        "repository": record["repository"],
        "tag": record["tag"],
        "commit": record["commit"],
        "archive": {
            "name": archive["name"],
            "bytes": archive["bytes"],
            "sha256": archive["reported_sha256"],
        },
    }


def read_release(archive: Path, selection: dict) -> dict[str, bytes]:
    """Every regular file of the selected release archive, by its path."""
    data = archive.read_bytes()
    expected = selection["archive"]
    if len(data) != expected["bytes"] or sha256(data) != expected["sha256"]:
        raise BundleError(
            f"{archive.name} is not the selected release archive: expected "
            f"{expected['bytes']} bytes with SHA-256 {expected['sha256']}, read "
            f"{len(data)} bytes with SHA-256 {sha256(data)}"
        )
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as tar:
        for member in tar:
            path = member.name.removeprefix("./").rstrip("/")
            if member.isdir():
                continue
            if not member.isfile():
                # A link or special entry anywhere the bundle reads is refused
                # below, where the package it sits in is known.
                files[path] = None  # type: ignore[assignment]
                continue
            if path in files:
                raise BundleError(f"release archive repeats {path}")
            files[path] = tar.extractfile(member).read()  # type: ignore[union-attr]
    return files


def build(files: dict[str, bytes], selection: dict) -> dict[str, bytes]:
    """The complete bundled tree, manifest included, as path -> bytes."""
    for required in (INDEX_PATH, LICENSE_PATH):
        if files.get(required) is None:
            raise BundleError(f"release has no regular file {required}")
    index = json.loads(files[INDEX_PATH].decode("utf-8"))
    if index.get("schema") != INDEX_SCHEMA:
        raise BundleError(f"method index schema is {index.get('schema')!r}, not {INDEX_SCHEMA}")
    methods = index["methods"]
    kinds = {method["kind"] for method in methods}
    if not kinds <= {"workflow", "skill"}:
        raise BundleError(f"method index has kinds this tool does not know: {sorted(kinds)}")
    workflows = [method for method in methods if method["kind"] == "workflow"]
    names = [method["name"] for method in workflows]
    if len(set(names)) != len(names):
        raise BundleError("method index repeats a workflow name")
    # The Library's own inventory rule: the immediate subfolders of workflows/
    # that hold a WORKFLOW.md. It must agree with the index.
    folders = {
        path.split("/")[1]
        for path in files
        if path.startswith("workflows/") and path.count("/") == 2 and path.endswith("/WORKFLOW.md")
    }
    if folders != set(names):
        raise BundleError(
            "the index and the workflow folders disagree: "
            f"only in index {sorted(set(names) - folders)}, only as folders {sorted(folders - set(names))}"
        )
    # Every file and folder of the release, for the paths a package names.
    release = set(files)
    for path in files:
        parts = path.split("/")
        release.update("/".join(parts[:i]) for i in range(1, len(parts)))
    tree: dict[str, bytes] = {}
    packages = []
    for method in sorted(workflows, key=lambda m: m["name"].encode("utf-8")):
        name = method["name"]
        prefix = f"workflows/{name}/"
        package = {path[len(prefix):]: data for path, data in files.items() if path.startswith(prefix)}
        special = sorted(path for path, data in package.items() if data is None)
        if special:
            raise BundleError(f"{name}: link or special entry in the release: {special}")
        if set(package) != set(method["resources"]):
            raise BundleError(f"{name}: the index's resources are not the package's files")
        check_package(name, package)
        if method.get("source") != "bundled" or not method.get("sourceRootId"):
            raise BundleError(f"{name}: not a bundled method with a source root")
        row = {
            "name": name,
            "description": method["description"],
            "revision_method": REVISION_METHOD,
            "revision": revision(package),
            "source_root": method["sourceRootId"],
            "source_path": f"workflows/{name}",
            "central": method["central"],
            "compatibility": method["compatibility"],
            "roles": method["executionRoleIds"],
            "navigation": method["navigation"],
            # What the Library's index states for the method, in its words:
            # the package's optional execution companion, or null without one.
            # It is not the App's declared part, and an empty tool list there
            # does not mean the workflow needs none.
            "library_execution": method.get("execution"),
            # What the package's files name in the release outside the App.
            "library_paths_named": library_paths_named(name, package, release, set(names)),
            "files": [
                {"path": path, "bytes": len(package[path]), "sha256": sha256(package[path])}
                for path in sorted(package, key=lambda p: p.encode("utf-8"))
            ],
        }
        packages.append(row)
        for path, data in package.items():
            tree[f"{name}/{path}"] = data
    manifest = {
        "schema_version": 2,
        "release_subject": f"chirality-library:{selection['tag']}",
        "standing": STANDING,
        "historical_shipped_revisions": [],
        "recognize_v3": False,
        "source": {
            "repository": selection["repository"],
            "tag": selection["tag"],
            "commit": selection["commit"],
            "archive": selection["archive"],
            "index": {
                "path": INDEX_PATH,
                "schema": INDEX_SCHEMA,
                "bytes": len(files[INDEX_PATH]),
                "sha256": sha256(files[INDEX_PATH]),
            },
            "license": {
                "path": LICENSE_PATH,
                "bytes": len(files[LICENSE_PATH]),
                "sha256": sha256(files[LICENSE_PATH]),
            },
        },
        # Index entries that are not workflows are listed, so that a reader can
        # account for every entry of the index against this bundle.
        "index_entries_not_bundled": [
            {"kind": method["kind"], "name": method["name"]}
            for method in methods
            if method["kind"] != "workflow"
        ],
        "packages": packages,
    }
    tree[MANIFEST_NAME] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    return tree


def read_tree(output: Path) -> tuple[dict[str, bytes], list[str]]:
    """The committed tree as path -> bytes, and every entry that is not a
    regular file or a folder."""
    tree: dict[str, bytes] = {}
    special: list[str] = []
    if not output.is_dir():
        return tree, special
    for path in sorted(output.rglob("*")):
        relative = path.relative_to(output).as_posix()
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            special.append(relative)
        elif path.is_file():
            tree[relative] = path.read_bytes()
    return tree, special


def differences(expected: dict[str, bytes], output: Path) -> list[str]:
    actual, special = read_tree(output)
    found = [f"not a regular file: {path}" for path in special]
    found += [f"missing: {path}" for path in sorted(set(expected) - set(actual))]
    found += [f"not in the release: {path}" for path in sorted(set(actual) - set(expected))]
    found += [
        f"bytes differ: {path}"
        for path in sorted(set(expected) & set(actual))
        if expected[path] != actual[path]
    ]
    return found


def write_tree(expected: dict[str, bytes], output: Path) -> None:
    actual, special = read_tree(output)
    for relative in special:
        raise BundleError(f"{output / relative} is not a regular file; remove it by hand")
    for relative in set(actual) - set(expected):
        (output / relative).unlink()
    for relative, data in expected.items():
        target = output / relative
        if actual.get(relative) != data:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    for folder in sorted((p for p in output.rglob("*") if p.is_dir()), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()


def verify_tree(output: Path) -> list[str]:
    """The committed tree against its own manifest; no release needed."""
    tree, special = read_tree(output)
    found = [f"not a regular file: {path}" for path in special]
    if MANIFEST_NAME not in tree:
        return found + [f"missing: {MANIFEST_NAME}"]
    manifest = json.loads(tree.pop(MANIFEST_NAME).decode("utf-8"))
    listed: set[str] = set()
    for row in manifest["packages"]:
        name = row["name"]
        prefix = f"{name}/"
        package = {path[len(prefix):]: data for path, data in tree.items() if path.startswith(prefix)}
        listed.update(f"{prefix}{path}" for path in package)
        rows = [
            {"path": path, "bytes": len(package[path]), "sha256": sha256(package[path])}
            for path in sorted(package, key=lambda p: p.encode("utf-8"))
        ]
        if rows != row["files"]:
            found.append(f"{name}: files differ from the manifest")
        elif revision(package) != row["revision"] or row["revision_method"] != REVISION_METHOD:
            found.append(f"{name}: revision differs from the manifest")
        else:
            try:
                check_package(name, package)
            except BundleError as error:
                found.append(str(error))
    found += [f"not in the manifest: {path}" for path in sorted(set(tree) - listed)]
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python3 -m tools.library_workflows", description=__doc__.split("\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("generate", "compare"):
        command = commands.add_parser(name)
        command.add_argument("--archive", required=True, type=Path, help="the selected release's source archive")
    commands.add_parser("verify")
    arguments = parser.parse_args(argv)
    output = ROOT / OUTPUT
    try:
        if arguments.command == "verify":
            found = verify_tree(output)
        else:
            selection = read_selection()
            expected = build(read_release(arguments.archive, selection), selection)
            if arguments.command == "generate":
                write_tree(expected, output)
            found = differences(expected, output)
            if not found:
                manifest = json.loads(expected[MANIFEST_NAME])
                print(
                    f"{len(manifest['packages'])} workflows of {selection['tag']} "
                    f"({selection['commit'][:12]}), {len(expected) - 1} files; "
                    f"manifest SHA-256 {sha256(expected[MANIFEST_NAME])}"
                )
    except (BundleError, OSError, KeyError, ValueError, tarfile.TarError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    for line in found:
        print(line, file=sys.stderr)
    return 1 if found else 0
