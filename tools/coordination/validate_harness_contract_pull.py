#!/usr/bin/env python3
"""Validate the Flow-A harness-contract pull and optional consumption records."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_SCHEMA = "chirality.flowA.harnessContractPull.v1"
EXPECTED_CONSUMPTION_SCHEMA = "chirality.piping.harnessContractConsumption.v1"


def run_git(repo_root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def git_blob(repo_root: Path, commit: str, repo_path: str) -> str:
    return run_git(repo_root, ["show", f"{commit}:{repo_path}"])


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_pull_contract(repo_root: Path, contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(contract.get("schemaVersion") == EXPECTED_SCHEMA, "unexpected pull-contract schema", errors)

    source = contract.get("source", {})
    package = contract.get("package", {})
    constants = contract.get("constants", {})
    exports = contract.get("exports", [])
    validation = contract.get("validation", {})

    commit = str(source.get("commitSha", ""))
    package_path = str(package.get("path", ""))
    package_json_path = f"{package_path}/package.json"

    try:
      run_git(repo_root, ["cat-file", "-e", f"{commit}^{{commit}}"])
    except subprocess.CalledProcessError as exc:
      errors.append(f"source commit is not reachable: {commit}: {exc.stderr.strip()}")
      return errors

    try:
        package_json = json.loads(git_blob(repo_root, commit, package_json_path))
    except Exception as exc:  # noqa: BLE001 - report validation context
        errors.append(f"cannot read package.json at source commit: {exc}")
        return errors

    require(package_json.get("name") == package.get("name"), "package.name mismatch", errors)
    require(package_json.get("version") == package.get("version"), "package.version mismatch", errors)
    require(package_json.get("private") is True, "package must remain private", errors)
    for dependency_key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        require(dependency_key not in package_json, f"package must not declare {dependency_key}", errors)

    package_exports = package_json.get("exports", {})
    manifest_exports = {entry.get("export"): entry for entry in exports if isinstance(entry, dict)}
    require(set(package_exports) == set(manifest_exports), "package export keys mismatch", errors)

    for export_key, target in package_exports.items():
        entry = manifest_exports.get(export_key, {})
        require(entry.get("target") == target, f"export target mismatch for {export_key}", errors)
        target_path = f"{package_path}/{str(target).removeprefix('./')}"
        try:
            content = git_blob(repo_root, commit, target_path)
        except subprocess.CalledProcessError as exc:
            errors.append(f"cannot read export target {target_path}: {exc.stderr.strip()}")
            continue
        require(entry.get("sha256") == sha256_text(content), f"sha256 mismatch for {export_key}", errors)

    sdk_version = git_blob(repo_root, commit, f"{package_path}/src/sdk-version.ts")
    tool_descriptor = git_blob(repo_root, commit, f"{package_path}/src/tool-descriptor.ts")
    require(
        f"FLOW_A_CONTRACT_VERSION = '{constants.get('flowAContractVersion')}'" in sdk_version,
        "FLOW_A_CONTRACT_VERSION mismatch",
        errors,
    )
    require(
        f"CLAUDE_AGENT_SDK_PACKAGE_VERSION = '{constants.get('claudeAgentSdkPackageVersion')}'" in sdk_version,
        "CLAUDE_AGENT_SDK_PACKAGE_VERSION mismatch",
        errors,
    )
    require(
        f"HARNESS_TOOL_REGISTRY_VERSION = '{constants.get('harnessToolRegistryVersion')}'" in tool_descriptor,
        "HARNESS_TOOL_REGISTRY_VERSION mismatch",
        errors,
    )
    require(
        "harness:validate:contract-deps" in str(validation.get("dependencyLintCommand", "")),
        "dependency lint command is missing",
        errors,
    )

    return errors


def validate_consumption_record(contract: dict[str, Any], consumption: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    require(
        consumption.get("schemaVersion") == EXPECTED_CONSUMPTION_SCHEMA,
        "unexpected consumption-record schema",
        errors,
    )
    for field in ("commitSha",):
        require(
            consumption.get("source", {}).get(field) == contract.get("source", {}).get(field),
            f"consumption source.{field} mismatch",
            errors,
        )
    for field in ("name", "path", "version"):
        require(
            consumption.get("package", {}).get(field) == contract.get("package", {}).get(field),
            f"consumption package.{field} mismatch",
            errors,
        )
    require(
        consumption.get("constants", {}).get("flowAContractVersion")
        == contract.get("constants", {}).get("flowAContractVersion"),
        "consumption Flow-A contract version mismatch",
        errors,
    )
    require(
        consumption.get("mechanism") == "D-APP-48 O-A intra-repo SHA-pinned pull",
        "unexpected consumption mechanism",
        errors,
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pull-contract", required=True)
    parser.add_argument("--consumption-record")
    args = parser.parse_args()

    repo_root = Path(run_git(Path.cwd(), ["rev-parse", "--show-toplevel"]).strip())
    contract_path = (repo_root / args.pull_contract).resolve()
    contract = read_json(contract_path)
    errors = validate_pull_contract(repo_root, contract)

    if args.consumption_record:
        consumption_path = (repo_root / args.consumption_record).resolve()
        errors.extend(validate_consumption_record(contract, read_json(consumption_path)))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("harness contract pull validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
