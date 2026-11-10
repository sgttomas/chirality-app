"""Prove that the CI Rust cache cannot make cargo reuse a stale repository crate."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml

from tools.ci import rust_dep_cache as subject

ROOT = Path(subject.__file__).resolve().parents[2]
CARGO_PATHS = ["app/src-tauri/target/debug/.fingerprint",
               "app/src-tauri/target/debug/build",
               "app/src-tauri/target/debug/deps"]
JOBS = ("rust-integration", "rust-lib-node", "sources-packaging", "product")


@pytest.fixture
def cargo_project(tmp_path):
    if shutil.which("cargo") is None:
        # Hosted runners have cargo; only a local machine without Rust may skip.
        if os.environ.get("CI"):
            pytest.fail("cargo is required for the stale-cache regression in CI")
        pytest.skip("cargo is not installed")
    third = tmp_path / "third-party"
    (third / "src").mkdir(parents=True)
    (third / "Cargo.toml").write_text(
        '[package]\nname = "third-party"\nversion = "0.1.0"\nedition = "2021"\n')
    (third / "src/lib.rs").write_text('pub const VALUE: &str = "third";\n')
    own = tmp_path / "own"
    (own / "src").mkdir(parents=True)
    (own / "tests").mkdir()
    (own / "Cargo.toml").write_text(
        '[package]\nname = "own-app"\nversion = "0.1.0"\nedition = "2021"\n'
        '[dependencies]\nthird-party = { path = "../third-party" }\n')
    (own / "src/main.rs").write_text('fn main() { println!("own=old {}", third_party::VALUE); }\n')
    (own / "tests/own_integration.rs").write_text("#[test]\nfn passes() {}\n")
    return own


def cargo(project, *args):
    env = {**os.environ, "CARGO_INCREMENTAL": "0", "CARGO_TARGET_DIR": str(project / "target")}
    return subprocess.run(["cargo", *args, "--offline", "--manifest-path", str(project / "Cargo.toml")],
                          capture_output=True, text=True, env=env, check=True)


def binary(project):
    return subprocess.check_output([str(project / "target/debug/own-app")], text=True).strip()


def backdate_new_source(project):
    """Change the source while keeping its file time older than the build output."""
    source = project / "src/main.rs"
    past = source.stat().st_mtime - 86400
    source.write_text(source.read_text().replace("own=old", "own=new"))
    os.utime(source, (past, past))


def test_without_pruning_cargo_trusts_an_old_file_time_and_runs_stale_code(cargo_project):
    # Control: shows the trap is real, so the next test proves something.
    cargo(cargo_project, "build")
    backdate_new_source(cargo_project)
    assert "Compiling own-app" not in cargo(cargo_project, "build").stderr
    assert binary(cargo_project).startswith("own=old")


def test_pruning_forces_a_rebuild_of_repository_crates_only(cargo_project):
    cargo(cargo_project, "build")
    cargo(cargo_project, "test", "--no-run")
    target = cargo_project / "target"
    removed = subject.prune(cargo_project / "Cargo.toml", target)
    assert removed
    profile = target / "debug"
    assert not list((profile / ".fingerprint").glob("own-app-*"))
    assert not list((profile / "build").glob("own-app-*"))
    assert not list((profile / "deps").glob("own_app-*"))
    assert not list((profile / "deps").glob("own_integration-*"))
    assert list((profile / ".fingerprint").glob("third-party-*"))
    assert list((profile / "deps").glob("libthird_party-*"))
    backdate_new_source(cargo_project)
    build = cargo(cargo_project, "build")
    assert "Compiling own-app" in build.stderr
    assert "Compiling third-party" not in build.stderr
    assert binary(cargo_project).startswith("own=new")


def test_ownership_matches_exact_crate_names_only(tmp_path):
    profile = tmp_path / "debug"
    (profile / ".fingerprint").mkdir(parents=True)
    (profile / "deps").mkdir()
    own = [profile / ".fingerprint/own-app-0123456789abcdef",
           profile / "deps/own_app-0123456789abcdef",
           profile / "deps/own_app-0123456789abcdef.d",
           profile / "deps/libown_app-0123456789abcdef.rlib",
           profile / "deps/own_app-0123456789abcdef.abc-cgu.0.rcgu.o"]
    kept = [profile / ".fingerprint/own-app-helper-0123456789abcdef",
            profile / "deps/own_app_helper-0123456789abcdef",
            profile / "deps/libown_app_helper-0123456789abcdef.rlib",
            profile / "deps/own_app.txt"]
    for path in own + kept:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("")
    found = subject.own_artifacts(profile, {"own-app"}, {"own_app"})
    assert set(found) == set(own)


@pytest.fixture
def stale_target(tmp_path):
    target = tmp_path / "target"
    fingerprint = target / "debug/.fingerprint/own-app-0123456789abcdef"
    fingerprint.mkdir(parents=True)
    (fingerprint / "bin-own-app").write_text("stale")
    (tmp_path / "Cargo.toml").write_text("[package]\n")
    return tmp_path


def test_a_miss_or_failed_restore_clears_any_partial_output(stale_target):
    target = stale_target / "target"
    report = subject.restored(stale_target / "Cargo.toml", target, "")
    assert not target.exists() and "building everything" in report
    assert "building everything" in subject.restored(stale_target / "Cargo.toml", target, "")


def test_output_that_cannot_be_cleaned_is_discarded_not_fatal(stale_target, monkeypatch):
    def refuse(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "cargo")

    monkeypatch.setattr(subject.subprocess, "check_output", refuse)
    target = stale_target / "target"
    report = subject.restored(stale_target / "Cargo.toml", target, "some-key")
    assert not target.exists() and "building everything" in report


def test_prune_refuses_when_repository_output_remains(stale_target, monkeypatch):
    monkeypatch.setattr(subject, "own_units", lambda manifest: ({"own-app"}, {"own_app"}))
    monkeypatch.setattr(subject, "remove", lambda path: None)
    with pytest.raises(ValueError, match="remain"):
        subject.prune(stale_target / "Cargo.toml", stale_target / "target")


def action(name):
    return yaml.safe_load((ROOT / f".github/actions/{name}/action.yml").read_text())


def step(steps, ident):
    return next(item for item in steps if item.get("id") == ident)


def test_restore_is_nonfatal_scoped_and_followed_by_the_cleanup():
    definition = action("app-v4-setup")
    steps = definition["runs"]["steps"]
    restore = step(steps, "rust-dependencies")
    assert restore["uses"] == "actions/cache/restore@v4"
    assert restore["continue-on-error"] is True
    assert restore["with"]["path"].split() == CARGO_PATHS
    assert "fail-on-cache-miss" not in restore["with"]
    assert restore["with"]["key"] == "${{ steps.rust-cache-key.outputs.key }}"
    assert restore["with"]["restore-keys"].strip() == "${{ steps.rust-cache-key.outputs.prefix }}"
    # Cleanup follows at once, keeps no continue-on-error, and sees the match.
    after = steps[steps.index(restore) + 1]
    assert after["run"] == 'python3 tools/ci/rust_dep_cache.py restored --matched-key "$MATCHED_KEY"'
    assert after["env"]["MATCHED_KEY"] == "${{ steps.rust-dependencies.outputs.cache-matched-key }}"
    assert "continue-on-error" not in after
    # No cargo or build command precedes the cleanup in the shared setup.
    assert not any("cargo " in item.get("run", "") for item in steps[:steps.index(after)])


def test_key_covers_platform_toolchain_lockfile_and_job():
    definition = action("app-v4-setup")
    key = step(definition["runs"]["steps"], "rust-cache-key")
    assert "rustc -vV" in key["run"]
    assert 'shasum -a 256 app/src-tauri/Cargo.lock' in key["run"]
    assert key["env"]["JOB"] == "${{ inputs.rust-cache-job }}"
    for part in ("${RUNNER_OS}", "${RUNNER_ARCH}", "${toolchain}", "${lock}", "${JOB}"):
        assert part in key["run"]
    assert definition["inputs"]["rust-cache-job"]["required"] is True


def test_save_prunes_first_and_never_fails_the_job():
    steps = action("app-v4-rust-cache-save")["runs"]["steps"]
    prune, save = step(steps, "prune"), steps[-1]
    assert prune["run"] == "python3 tools/ci/rust_dep_cache.py prune"
    assert prune["continue-on-error"] is True and save["continue-on-error"] is True
    assert steps.index(prune) < steps.index(save)
    # A failed prune must never be followed by a save.
    assert save["if"] == "steps.prune.outcome == 'success'"
    assert save["uses"] == "actions/cache/save@v4"
    assert save["with"]["path"].split() == CARGO_PATHS
    assert save["with"]["key"] == "${{ inputs.key }}"
    assert "inputs.already-cached != 'true'" in prune["if"]


def test_every_macos_job_restores_under_its_own_name_and_saves_last():
    jobs = yaml.safe_load((ROOT / ".github/workflows/app-v4.yml").read_text())["jobs"]
    for name in JOBS:
        steps = jobs[name]["steps"]
        setup = step(steps, "setup")
        assert setup["uses"] == "./.github/actions/app-v4-setup"
        assert setup["with"] == {"rust-cache-job": name}
        last = steps[-1]
        assert last["uses"] == "./.github/actions/app-v4-rust-cache-save"
        assert last["if"] == "${{ !cancelled() }}"
        assert last["with"] == {"key": "${{ steps.setup.outputs.rust-cache-key }}",
                                "already-cached": "${{ steps.setup.outputs.rust-cache-hit }}"}
        assert steps.index(setup) < len(steps) - 1


def test_fork_pull_requests_neither_restore_nor_save():
    root = Path(__file__).resolve().parents[2]
    setup = (root / '.github/actions/app-v4-setup/action.yml').read_text()
    save = (root / '.github/actions/app-v4-rust-cache-save/action.yml').read_text()
    assert "github.event.pull_request.head.repo.full_name == github.repository" in setup
    assert "if [ \"$SAME_REPOSITORY\" != 'true' ]; then" in setup
    assert 'echo "key="' in setup
    restore = setup[setup.index('id: rust-dependencies'):setup.index('actions/cache/restore@')]
    assert "if: steps.rust-cache-key.outputs.key != ''" in restore
    assert "if: inputs.key != ''" in save
