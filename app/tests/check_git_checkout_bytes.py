#!/usr/bin/env python3
"""Exercise Git checkout conversion on committed byte-bound App inputs, offline."""

import json
import os
from pathlib import Path
import subprocess
import tempfile


SOURCES = (
    "execution/PKG-04/DEL-04-03/Work/RS_RECORD.schema.json",
    "execution/PKG-01/DEL-01-06/ScopeOfWork.md",
    "app/src-tauri/schemas/RS_RECORD.schema.json",
    "app/src-tauri/resources/instructions/AGENTS.md",
    "app/src-tauri/resources/production_workflows/coordinated-knowledge-work/WORKFLOW.md",
    "app/examination/support_identity/declaration.v1.json",
    "app/tests/fixtures/FX-DP1/MANIFEST.sha256",
    "app/packaging/sources.json",
    "reference/migration/shared-inputs.json",
    "workflows/coordinated-knowledge-work/WORKFLOW.md",
)
CRLF_CONTROL = "app/tests/fixtures/checkout-bytes/intentional-crlf.txt"
UNPROTECTED_CONTROL = "docs/checkout-bytes-unprotected.txt"


def git(directory, *arguments, env, data=None):
    return subprocess.run(
        ["git", "-C", str(directory), *arguments],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        env=env,
    ).stdout


def checkout(directory, sources, attributes, env):
    directory.mkdir()
    git(directory, "init", "--quiet", "--template=", env=env)
    git(directory, "config", "core.autocrlf", "true", env=env)
    git(directory, "config", "core.attributesFile", os.devnull, env=env)
    entries = dict(sources)
    if attributes is not None:
        entries[".gitattributes"] = attributes
    # Stage the original blobs directly: no add-time conversion or reference rewrite.
    for name, content in entries.items():
        oid = git(directory, "hash-object", "-w", "--stdin", env=env, data=content)
        git(
            directory, "update-index", "--add", "--cacheinfo",
            "100644", oid.decode().strip(), name, env=env,
        )
    git(directory, "checkout-index", "--all", "--force", env=env)
    return {name: (directory / name).read_bytes() for name in sources}


def main():
    with tempfile.TemporaryDirectory(prefix="chirality-checkout-bytes-") as scratch:
        scratch = Path(scratch)
        codex_home = scratch / "codex-home"
        codex_home.mkdir()
        env = dict(os.environ, CODEX_HOME=str(codex_home))
        env.update(
            GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
            GIT_ATTR_NOSYSTEM="1", GIT_NO_LAZY_FETCH="1",
        )
        root = Path(git(Path(__file__).parent, "rev-parse", "--show-toplevel", env=env).decode().strip())
        revision = git(root, "rev-parse", "HEAD", env=env).decode().strip()
        sources = {name: git(root, "show", f"{revision}:{name}", env=env) for name in SOURCES}
        sources[CRLF_CONTROL] = b"intentional\r\nCRLF\r\n"
        sources[UNPROTECTED_CONTROL] = b"ordinary\ntext\n"
        attributes = (root / ".gitattributes").read_bytes()
        before = checkout(scratch / "before", sources, None, env)
        after = checkout(scratch / "after", sources, attributes, env)
        protected = (*SOURCES, CRLF_CONTROL)
        changed_before = [name for name in protected if before[name] != sources[name]]
        changed_after = [name for name in protected if after[name] != sources[name]]
        if not changed_before:
            raise AssertionError("negative control did not exercise Git newline conversion")
        if changed_after:
            raise AssertionError(f"byte-bound checkout changed: {changed_after}")
        if after[UNPROTECTED_CONTROL] != b"ordinary\r\ntext\r\n":
            raise AssertionError("unprotected control did not retain ordinary Git conversion")
        print(json.dumps({
            "source_revision": revision,
            "committed_inputs": len(SOURCES),
            "protected_inputs_including_intentional_crlf": len(protected),
            "changed_without_attributes": len(changed_before),
            "changed_with_attributes": len(changed_after),
            "unprotected_control_converted": True,
            "scope": "temporary Git checkout proof; no native Windows execution",
        }, sort_keys=True))


if __name__ == "__main__":
    main()
