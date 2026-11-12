#!/usr/bin/env python3
"""Admit a pin whose generated basis is byte-identical to the prior pin's (DEL-01-01 REQ-006).

This is the check a pin advance carries when the supplier's generated schema did not change at
all. It compares bytes and admits records whole; it reads no host source, interprets no schema,
takes no dispositions and has no table of exceptions.

  1. The three generated files (the manifest and the two compiled bundles) are equal byte for
     byte at the two pins. If one differs, it refuses: a changed schema needs a full comparison
     of what the App relies on, with dispositions, and no such comparison is maintained.
  2. The new pin's distribution record and generation record are admitted whole. The check does
     not look at the records field by field for plausible values: it works out what `intake.py`
     must have written from what is independently determined (the table's row for the pin, the
     three generated files, the distribution record's own inventory entries, and the fixed
     words and numbers `intake.py` writes) and requires each record to equal that exactly, as
     canonical JSON text, so that 1 and 1.0 differ and true is not 1. Keys are a closed set at
     every level.
     What nothing kept in the repository determines is admitted by its form only. That list is
     closed, is FORM_ONLY below, and is repeated in every result: the inventory entries
     themselves (path, kind, mode, and for a file its size and digest), from which the
     inventory digest and the file count are then worked out; the count of Mach-O files; the
     supplier's own package metadata beyond its pin, entrypoint and path directory; how many
     ancestors of the scratch directory were checked; how many socket samples each generator
     pass had (at least one); and each pass's byte count (for the experimental pass, at least
     the two compiled bundles' own sizes).
  3. A supplement file at either pin refuses: supplements are not handled here.

DEL-01-01 REQ-006 requires the generated schema, the supplement and the recorded exchanges of
the new pin to be compared with the prior pin's. This check is the schema part (1) and the
supplement part (3: neither pin keeps one, or it refuses). The recorded exchanges are not read
here: they are kept at each pin with a note of what they establish and checked by
test_recordings.py.

The prior pin's own records are not admitted again; only the byte equality of its generated
files with the new pin's is used. The prior pin must be one for which the repository keeps a
consumer analysis (the table ANALYSIS), because that analysis is what an identical basis
carries over.

What a result establishes: the protocol surface, as the supplier generates it, is the same
bytes at both pins, and the new pin's records are whole and bound to its release archive. What
it does not establish: that the supplier behaves the same. The only behavioural evidence at a
pin is its recorded exchanges, bounded as the note beside them says.

Usage, from `app/`:
  python3 supplier_checks/same_basis.py --from 0.167.0 --to 0.167.2

It prints the result and writes it to `supplier_checks/version_advance/<from>-to-<to>.json`.
Exit status: 0 admitted, 2 refused.

An operator-run check on stable inputs: built so that a record it did not read in full, or a
file it did not compare, cannot come out as admitted; not built to withstand a writer changing
the inputs during the run, nor someone with write access forging a consistent set of records.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import intake  # noqa: E402

FORMAT = "chirality.app-v4.same-basis.v1"
RESULTS = HERE / "version_advance"
MANIFEST = "MANIFEST.sha256"
GENERATED = (MANIFEST,) + intake.BUNDLES
SUPPLEMENT = "SUPPLEMENT.json"
# The pins whose generated basis has a committed consumer analysis, which an identical basis
# carries over. Adding a row is a reviewed decision.
ANALYSIS = {"0.167.0": ("0.160.0-to-0.167.0.json", "0.160.0-to-0.167.0.dispositions.json")}
ENVIRONMENT = ["CODEX_HOME", "HOME", "LANG", "PATH", "TMPDIR", "TZ"]
SHA = re.compile(r"[0-9a-f]{64}")
ROW = re.compile(r"([0-9a-f]{64})  (json-schema/(experimental|stable)/([^\n/][^\n]*))")
# The fixed words intake.py writes into the two records. test_same_basis.py makes records with
# intake.py itself and admits them, which is what keeps these equal to intake.py's own text.
RECORD_ROOT_MODE = ("The container directory is not an archive member and its mode is not compared. "
                    "All %d declared file and directory member modes are compared.")
RECORD_LIMITS = ["Static intake of a size- and digest-checked archive only.",
                 "No supplier execution, signature or trust reading, installed custody, product "
                 "qualification or notice coverage is established."]
GENERATION_VERIFIED = "complete vendor tree equal to the expected inventory before execution"
GENERATION_HOMES = "fresh private HOME, CODEX_HOME and TMPDIR; plugins and analytics off"
GENERATION_NETWORK = "the generator's sockets were sampled every 0.1 s and no sample showed one; a sample is not isolation"
GENERATION_OUTSIDE_NOTE = "presence checks before execution; controls on what the supplier is given, not a sandbox"
GENERATION_LIMITS = ["One generator pass per variant; determinism is not assessed.",
                     "JSON schema generation only; no TypeScript generation, session, turn, sign-in or "
                     "provider connection.",
                     "A generated basis is not qualification of the pin."]
FORM_ONLY = [
    "distribution record: each inventory entry's path, kind and mode, and a file's size and digest (the "
    "inventory digest and the file count are worked out from them and compared)",
    "distribution record: the count of Mach-O files (a whole number no greater than the file count)",
    "distribution record: the supplier's package metadata beyond its version, entrypoint and path directory",
    "generation record: how many ancestors of the scratch directory were checked (a whole number of at least one)",
    "generation record: each generator pass's socket sample count (a whole number of at least one)",
    "generation record: each generator pass's byte count (a whole number; for the experimental pass at least "
    "the sizes of the two compiled bundles)",
]
DOES_NOT_ESTABLISH = [
    "that the supplier behaves the same at the two pins: equal generated files show only that the protocol "
    "surface, as the supplier generates it, is unchanged",
    "anything about the supplier's behaviour beyond the recorded exchanges kept for a pin, which are bounded as "
    "the note beside them says",
    "that the prior pin's own records are whole: they are not admitted again here; only the byte equality of "
    "its generated files with the new pin's is used",
    "qualification of the pin (DEL-01-01 AC-011)",
]


class Refused(Exception):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    """The bytes of a regular file that is not a link, or a refusal."""
    try:
        status = os.lstat(path)
        if not stat.S_ISREG(status.st_mode):
            raise Refused("%s is not a regular file" % path.name)
        return Path(path).read_bytes()
    except OSError as error:
        raise Refused("%s could not be read (%s)" % (path.name, type(error).__name__)) from None


def strict_json(data, name):
    def pairs(items):
        keys = [key for key, _ in items]
        if len(keys) != len(set(keys)):
            raise ValueError("repeated key")
        return dict(items)
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs)
    except (ValueError, UnicodeDecodeError):
        raise Refused("%s is not JSON without a repeated key" % name) from None


def require(condition, message):
    if not condition:
        raise Refused(message)


def closed(value, keys, where):
    """`value` is an object with exactly `keys`."""
    require(isinstance(value, dict) and sorted(value) == sorted(keys),
            "%s does not have exactly the keys %s" % (where, ", ".join(sorted(keys))))
    return value


def is_count(value, least=0):
    return type(value) is int and value >= least


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def expect(actual, expected, what):
    """`actual` is exactly `expected`, as canonical JSON text: 1 is not 1.0 and true is not 1."""
    require(canonical(actual) == canonical(expected), what + " is not what intake.py writes for this pin")


def is_digest(value):
    return isinstance(value, str) and SHA.fullmatch(value) is not None


def admit_distribution(pin, data):
    """The distribution record of `pin`, equal to what intake.py writes for it, or a refusal."""
    where = "the distribution record"
    record = closed(strict_json(data, where), ["format", "pin", "source_commit", "archive", "package_metadata",
                                               "files", "macho_files", "inventory", "root_mode", "limits"], where)
    facts = intake.PINS[pin]
    inventory = closed(record["inventory"], ["method", "algorithm", "manifest_sha256", "entries"],
                       where + "'s inventory")
    # Admitted by form only: the entries, which are the facts the rest is worked out from.
    entries = inventory["entries"]
    require(isinstance(entries, list) and entries, where + " has no inventory entries")
    kinds, last = {}, None
    for entry in entries:
        require(isinstance(entry, dict) and entry.get("kind") in ("file", "dir"),
                where + " has an entry that is not a file or a directory")
        closed(entry, ["path", "kind", "mode"] + (["size", "sha256"] if entry["kind"] == "file" else []),
               where + "'s entry")
        path = entry["path"]
        require(isinstance(path, str) and path and not path.startswith("/") and "\n" not in path and "\r" not in path
                and "\x00" not in path and all(part not in ("", ".", "..") for part in path.split("/")),
                where + " has an entry whose path is not a plain relative path")
        require(last is None or path.encode("utf-8") > last, where + "'s entries are not in order without a repeat")
        last = path.encode("utf-8")
        require(type(entry["mode"]) is int and 0 <= entry["mode"] <= 0o777, where + " has an entry with no mode")
        if entry["kind"] == "file":
            require(is_count(entry["size"]) and is_digest(entry["sha256"]),
                    where + " has a file entry without its size and digest")
        parent = path.rpartition("/")[0]
        require(not parent or kinds.get(parent) == "dir", where + " has an entry outside a listed directory")
        kinds[path] = entry["kind"]
    files = [entry for entry in entries if entry["kind"] == "file"]
    rows = "".join("%s  %s\n" % (entry["sha256"], entry["path"]) for entry in files)
    # Determined: everything else of the record but the two parts named in FORM_ONLY.
    metadata = record["package_metadata"]
    require(isinstance(metadata, dict), where + "'s package metadata is not an object")
    expect({key: value for key, value in record.items() if key not in ("package_metadata", "macho_files")},
           {"format": intake.RECORD_FORMAT, "pin": pin, "source_commit": facts["source_commit"],
            "archive": {key: facts[key] for key in ("url", "size", "sha256")}, "files": len(files),
            "inventory": {"method": "codex-vendor-tree-v1", "algorithm": "sha-256",
                          "manifest_sha256": sha256(rows.encode("utf-8")), "entries": entries},
            "root_mode": RECORD_ROOT_MODE % len(entries), "limits": RECORD_LIMITS}, where)
    expect(metadata.get("version"), pin, where + "'s package metadata version")
    require(is_count(record["macho_files"]) and record["macho_files"] <= len(files),
            where + "'s count of Mach-O files is not a whole number within its file count")
    try:
        intake.metadata_members(record)
    except intake.Refused as refusal:
        raise Refused(str(refusal)) from None
    return record


def manifest_variants(data, bundles):
    """{variant: [row text]} of a generator output manifest, every line read, or a refusal."""
    where = "the generator output manifest"
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused(where + " is not UTF-8 text") from None
    require(text.endswith("\n"), where + " does not end with a line end")
    variants, seen, order = {"experimental": [], "stable": []}, {}, []
    for line in text[:-1].split("\n"):
        row = ROW.fullmatch(line)
        require(row is not None, where + " has a line that is not a digest and a json-schema path")
        require(row.group(2) not in seen, where + " names a file twice")
        seen[row.group(2)] = row.group(1)
        variants[row.group(3)].append(line + "\n")
        if not order or order[-1] != row.group(3):
            order.append(row.group(3))
    require(order == ["experimental", "stable"], where + " is not the experimental rows followed by the stable rows")
    for name, digest in bundles.items():
        require(seen.get("json-schema/experimental/" + name) == digest,
                where + " does not name the digest of the compiled bundle " + name)
    return variants


def admit_generation(pin, data, record, manifest, bundles, bundle_bytes):
    """The generation record of `pin`, equal to what intake.py writes for it, or a refusal.

    `bundles` is {name: digest} and `bundle_bytes` the two bundles' sizes together, both from the
    files as read.
    """
    where = "the generation record"
    generation = closed(strict_json(data, where), ["format", "pin", "supplier", "environment", "variants",
                                                   "compiled_experimental_bundles", "manifest_sha256", "limits"],
                        where)
    entry = next(e for e in record["inventory"]["entries"] if e["path"] == record["package_metadata"]["entrypoint"])
    rows = manifest_variants(manifest, bundles)
    environment = closed(generation["environment"], ["inherit_environment", "allowlist", "homes",
                                                     "outside_configuration", "network"], where + "'s environment")
    outside = closed(environment["outside_configuration"], ["working_directory_ancestors",
                                                            "system_configuration_folder", "managed_preferences",
                                                            "note"], where + "'s outside-configuration checks")
    variants = closed(generation["variants"], ["experimental", "stable"], where + "'s variants")
    # Admitted by form only: the three counts nothing kept in the repository determines.
    ancestors = outside["working_directory_ancestors"]
    require(isinstance(ancestors, str) and re.fullmatch(r"[1-9][0-9]* checked, none holds \.git or \.codex", ancestors),
            where + " does not state the ancestors checked for outside configuration")
    expected_variants = {}
    for name, extra in (("experimental", ["--experimental"]), ("stable", [])):
        variant = closed(variants[name], ["argv", "exit_code", "timeout_seconds", "files", "bytes", "manifest_sha256",
                                          "socket_samples", "failed_samples", "sockets_seen"],
                         where + "'s %s variant" % name)
        require(is_count(variant["socket_samples"], 1),
                where + "'s %s variant records no socket sample" % name)
        require(is_count(variant["bytes"], bundle_bytes if name == "experimental" else 1),
                where + "'s %s variant records fewer bytes than the files it generated" % name)
        expected_variants[name] = {
            "argv": ["<vendor>/bin/codex", "app-server", "generate-json-schema"] + extra + ["--out", "<output>/" + name],
            "exit_code": 0, "timeout_seconds": intake.GENERATOR_TIMEOUT, "files": len(rows[name]),
            "bytes": variant["bytes"], "manifest_sha256": sha256("".join(rows[name]).encode("utf-8")),
            "socket_samples": variant["socket_samples"], "failed_samples": 0, "sockets_seen": 0}
    # Determined: the whole record, with those three counts carried as read.
    expect(generation, {
        "format": intake.GENERATION_FORMAT, "pin": pin,
        "supplier": {"source": "official release archive " + record["archive"]["url"],
                     "archive_sha256": record["archive"]["sha256"], "main_sha256": entry["sha256"],
                     "tree_manifest_sha256": record["inventory"]["manifest_sha256"],
                     "verified": GENERATION_VERIFIED},
        "environment": {"inherit_environment": False, "allowlist": ENVIRONMENT, "homes": GENERATION_HOMES,
                        "outside_configuration": {"working_directory_ancestors": ancestors,
                                                  "system_configuration_folder": "absent",
                                                  "managed_preferences": "absent",
                                                  "note": GENERATION_OUTSIDE_NOTE},
                        "network": GENERATION_NETWORK},
        "variants": expected_variants, "compiled_experimental_bundles": bundles,
        "manifest_sha256": sha256(manifest), "limits": GENERATION_LIMITS}, where)
    return generation


def compare(from_pin, to_pin):
    """The result of admitting `to_pin` on the same generated basis as `from_pin`, or a refusal."""
    known = list(intake.PINS)
    for pin in (from_pin, to_pin):
        require(any(pin == name for name in known), "%r is not a pin of the table (%s)" % (pin, ", ".join(known)))
    require(from_pin != to_pin, "the two pins are the same")
    require(from_pin in ANALYSIS, "no consumer analysis is kept for %s, so nothing carries over from it" % from_pin)
    resources = Path(intake.RESOURCES)
    folders = {pin: resources / pin for pin in (from_pin, to_pin)}
    for pin, folder in folders.items():
        require(folder.is_dir() and not folder.is_symlink(), "the repository holds no generated schema for %s" % pin)
        require(not os.path.lexists(folder / SUPPLEMENT),
                "a supplement is kept at %s, and supplements are not handled by this check" % pin)
    generated, sizes = {}, {}
    for name in GENERATED:
        old, new = read(folders[from_pin] / name), read(folders[to_pin] / name)
        sizes[name] = len(new)
        require(old == new, "%s differs between %s and %s: a changed schema needs a full comparison of what the "
                            "App relies on, with dispositions, and none is maintained" % (name, from_pin, to_pin))
        generated[name] = sha256(new)
    distribution = read(folders[to_pin] / "CANONICAL_DISTRIBUTION.json")
    record = admit_distribution(to_pin, distribution)
    generation = read(folders[to_pin] / "GENERATION.json")
    admit_generation(to_pin, generation, record, read(folders[to_pin] / MANIFEST),
                     {name: generated[name] for name in intake.BUNDLES}, sum(sizes[name] for name in intake.BUNDLES))
    analysis = {name: sha256(read(Path(RESULTS) / name)) for name in ANALYSIS[from_pin]}
    return {
        "format": FORMAT, "from": from_pin, "to": to_pin, "result": "admitted on the same generated basis",
        "generated_files_equal_byte_for_byte": generated,
        "admitted_whole": {"CANONICAL_DISTRIBUTION.json": sha256(distribution), "GENERATION.json": sha256(generation)},
        "admitted_by_form_only_because_nothing_kept_determines_them": FORM_ONLY,
        "establishes": "the protocol surface, as the supplier generates it, is the same bytes at %s and %s, and the "
                       "distribution record and generation record of %s are whole and bound to its release archive"
                       % (from_pin, to_pin, to_pin),
        "consumer_analysis_that_carries_over": dict(
            analysis, note="made for the basis of %s; it applies to %s because the basis is the same bytes. It "
                           "is kept as evidence with the note beside it, which says what it does not establish"
                           % (from_pin, to_pin)),
        "does_not_establish": DOES_NOT_ESTABLISH,
    }


def render(result):
    return json.dumps(result, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="from_pin", required=True, choices=sorted(intake.PINS))
    parser.add_argument("--to", dest="to_pin", required=True, choices=sorted(intake.PINS))
    args = parser.parse_args(argv)
    try:
        result = compare(args.from_pin, args.to_pin)
    except Refused as refusal:
        sys.stderr.write("refused: %s\n" % refusal)
        return 2
    text = render(result)
    (Path(RESULTS) / ("%s-to-%s.json" % (args.from_pin, args.to_pin))).write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
