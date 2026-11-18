"""Exercise CI Rust cache pruning and reproduce stale workspace reuse when pruning is skipped."""
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


@pytest.fixture(scope="module", autouse=True)
def cargo_in_use(request):
    """Say which cargo these tests ran with, on a passing run too: the layout depends on it."""
    reporter = request.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is not None and shutil.which("cargo"):
        version = subprocess.run(["cargo", "--version"], capture_output=True, text=True).stdout.strip()
        reporter.write_line(f"\ntools/ci/test_rust_dep_cache.py ran with {version}")


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


def built_as(project):
    """Which cargo built, and where it put things: read in the log when a layout assertion fails."""
    version = subprocess.run(["cargo", "--version"], capture_output=True, text=True).stdout.strip()
    profile = project / "target/debug"
    shown = sorted(str(path.relative_to(profile)) for depth in ("*", "*/*", "build/*/*", "build/*/*/*")
                   for path in profile.glob(depth) if not str(path.relative_to(profile)).startswith("incremental"))
    return f"{version}: {shown}"


def units_of(profile, package):
    """A package's unit folders, wherever either known layout puts them."""
    return (list((profile / ".fingerprint").glob(f"{package}-*"))
            + list((profile / "build").glob(f"{package}-*"))
            + list((profile / "build").glob(f"{package}/*")))


def pruned_for_save(project):
    """Prune as the save step does. Report the Cargo version and output paths if pruning raises a layout or ownership error."""
    try:
        return subject.prune_after_build(project / "Cargo.toml", project / "target")
    except ValueError as refusal:
        pytest.fail(f"{refusal}; {built_as(project)}")


def third_party_kept(profile):
    """The dependency's fingerprint and its compiled library, where the layout in use puts them."""
    if (profile / ".fingerprint").is_dir():
        return (list((profile / ".fingerprint").glob("third-party-*"))
                and list((profile / "deps").glob("libthird_party-*")))
    return [unit for unit in (profile / "build/third-party").glob("*")
            if (unit / "fingerprint").is_dir() and list((unit / "out").glob("libthird_party*"))]


def test_pruning_forces_a_rebuild_of_repository_crates_only(cargo_project):
    cargo(cargo_project, "build")
    cargo(cargo_project, "test", "--no-run")
    target = cargo_project / "target"
    profile = target / "debug"
    assert units_of(profile, "own-app") and units_of(profile, "third-party"), built_as(cargo_project)
    # As the save step calls it: a build that leaves nothing to remove is an error.
    removed = pruned_for_save(cargo_project)
    assert removed, built_as(cargo_project)
    assert not units_of(profile, "own-app"), built_as(cargo_project)
    assert not list((profile / "deps").glob("own_app-*")), built_as(cargo_project)
    assert not list((profile / "deps").glob("own_integration-*")), built_as(cargo_project)
    assert third_party_kept(profile), built_as(cargo_project)
    backdate_new_source(cargo_project)
    build = cargo(cargo_project, "build")
    assert "Compiling own-app" in build.stderr
    assert "Compiling third-party" not in build.stderr
    assert binary(cargo_project).startswith("own=new")


def test_a_local_library_build_script_example_and_test_leave_nothing_behind(cargo_project):
    # The library has rlib, staticlib and cdylib crate types, as the App does. With the
    # legacy layout, a normal build of this local library can leave unhashed files in `deps`.
    manifest = cargo_project / "Cargo.toml"
    manifest.write_text(manifest.read_text().replace(
        "[dependencies]", 'build = "build.rs"\n[lib]\nname = "own_app_lib"\n'
        'crate-type = ["rlib", "staticlib", "cdylib"]\n[dependencies]'))
    (cargo_project / "build.rs").write_text("fn main() {}\n")
    (cargo_project / "src/lib.rs").write_text('pub fn value() -> &\'static str { third_party::VALUE }\n')
    (cargo_project / "src/main.rs").write_text('fn main() { println!("own=old {}", own_app_lib::value()); }\n')
    (cargo_project / "examples").mkdir()
    (cargo_project / "examples/show.rs").write_text('fn main() { println!("{}", own_app_lib::value()); }\n')
    cargo(cargo_project, "build", "--lib", "--bins", "--examples")
    cargo(cargo_project, "test", "--no-run")
    profile = cargo_project / "target/debug"
    assert pruned_for_save(cargo_project), built_as(cargo_project)
    assert not units_of(profile, "own-app"), built_as(cargo_project)
    named_for_own_crates = [entry.name for entry in profile.glob("deps/*")
                            if entry.name.removeprefix("lib").startswith(("own_app", "own_integration", "build_script_build"))]
    assert not named_for_own_crates, built_as(cargo_project)
    assert third_party_kept(profile), built_as(cargo_project)
    assert not subject.unrecognised_output(profile), built_as(cargo_project)
    backdate_new_source(cargo_project)
    build = cargo(cargo_project, "build")
    assert "Compiling own-app" in build.stderr and "Compiling third-party" not in build.stderr
    assert binary(cargo_project).startswith("own=new")


def test_a_real_build_holding_nothing_recognised_as_the_repositorys_is_not_saved(cargo_project, monkeypatch):
    cargo(cargo_project, "build")
    target = cargo_project / "target"
    monkeypatch.setattr(subject, "own_units", lambda manifest: ({"renamed-app"}, {"renamed_app"}))
    with pytest.raises(ValueError, match="none of it was recognised"):
        subject.prune_after_build(cargo_project / "Cargo.toml", target)
    # Restore allows zero matches. The stub still hides own-app in this fixture.
    assert "removed 0" in subject.restored(cargo_project / "Cargo.toml", target, "some-key")
    assert units_of(target / "debug", "third-party"), built_as(cargo_project)


def test_workspace_target_spellings_match_and_longer_crate_names_are_kept(tmp_path):
    profile = tmp_path / "debug"
    (profile / ".fingerprint").mkdir(parents=True)
    (profile / "deps").mkdir()
    own = [profile / ".fingerprint/own-app-0123456789abcdef",
           profile / "deps/own_app-0123456789abcdef",
           profile / "deps/own_app-0123456789abcdef.d",
           profile / "deps/libown_app-0123456789abcdef.rlib",
           profile / "deps/own_app-0123456789abcdef.abc-cgu.0.rcgu.o",
           # These fixtures exercise unhashed outputs and sidecars selected by the current
           # target name.
           profile / "deps/libown_app.dylib",
           profile / "deps/libown_app.a",
           profile / "deps/libown_app.rlib",
           profile / "deps/own_app.d",
           profile / "deps/own_app.own_app.0123456789abcdef-cgu.0.rcgu.o",
           profile / "deps/own_app.txt"]
    kept = [profile / ".fingerprint/own-app-helper-0123456789abcdef",
            profile / "deps/own_app_helper-0123456789abcdef",
            profile / "deps/libown_app_helper-0123456789abcdef.rlib",
            profile / "deps/own_app_helper-0123456789abcdef.long-type-123.txt"]
    for path in own + kept:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("")
    found = subject.own_artifacts(profile, {"own-app"}, {"own_app"})
    assert set(found) == set(own)


def layout_of_cargo_1_100(profile, packages=("own-app", "own-app-helper", "third-party")):
    """Units as Cargo 1.100 lays them out: build/<package>/<hash>/ holding fingerprint and out."""
    made = [profile / "build" / package for package in packages]
    for package in made:
        for unit in ("0123456789abcdef", "fedcba9876543210"):
            (package / unit / "fingerprint").mkdir(parents=True)
            (package / unit / "fingerprint/invoked.timestamp").write_text("")
            (package / unit / "out").mkdir()
            (package / unit / "out/artifact.rlib").write_text("")
    return made[0], made[1:]


def older_layout(profile, package, crate, first="0123456789abcdef", second="fedcba9876543210"):
    """Make synthetic legacy library output and compiled and run folders for a build script."""
    made = [profile / f".fingerprint/{package}-{first}",
            profile / f"build/{package}-{first}",
            profile / f"build/{package}-{second}/out"]
    for folder in made:
        folder.mkdir(parents=True)
    (made[0] / f"lib-{crate}").write_text("")
    (made[1] / "build-script-build").write_text("")
    (profile / "deps").mkdir(exist_ok=True)
    library = profile / f"deps/lib{crate}-{first}.rlib"
    library.write_text("")
    return [made[0], made[1], made[2].parent, library]


def own_app_only(monkeypatch, packages=("own-app",), crates=("own_app",)):
    """Ownership and the lockfile as Cargo would report them, for a tree that was not built."""
    monkeypatch.setattr(subject, "own_units", lambda manifest: (set(packages), set(crates)))
    monkeypatch.setattr(subject, "lockfile", lambda manifest: next(
        (lock for lock in [manifest.parent / "Cargo.lock"] if lock.is_file()), None))


def test_ownership_in_the_layout_of_cargo_1_100_is_the_package_folder(tmp_path):
    profile = tmp_path / "debug"
    own, kept = layout_of_cargo_1_100(profile)
    assert subject.own_artifacts(profile, {"own-app"}, {"own_app"}) == [own]
    assert len(subject.compiled_units(profile)) == 6
    assert not subject.unrecognised_output(profile)


def test_pruning_the_layout_of_cargo_1_100_removes_every_unit_of_the_package(tmp_path, monkeypatch):
    target = tmp_path / "target"
    own, kept = layout_of_cargo_1_100(target / "debug")
    own_app_only(monkeypatch)
    assert subject.prune_after_build(tmp_path / "Cargo.toml", target) == 1
    assert not own.exists()
    assert all((package / "0123456789abcdef/out/artifact.rlib").is_file() for package in kept)
    # Pruned output is what a later restore sees: nothing left to remove, and not an error.
    assert "removed 0" in subject.restored(tmp_path / "Cargo.toml", target, "some-key")


def test_a_dependency_whose_name_ends_like_a_hash_is_kept_in_the_layout_of_cargo_1_100(tmp_path, monkeypatch):
    # `build/own-app-cafe` and `build/own-app-0123456789abcdef` are packages of their own
    # here; read as the older layout they would be units of `own-app`.
    target = tmp_path / "target"
    profile = target / "debug"
    own, kept = layout_of_cargo_1_100(profile, ("own-app", "own-app-cafe", "own-app-0123456789abcdef"))
    # The same path cannot be both, so the older layout's units take other hashes here.
    older = older_layout(profile, "own-app", "own_app", "1111111111111111", "2222222222222222")
    other = older_layout(profile, "third-party", "third_party")
    own_app_only(monkeypatch)
    assert set(subject.own_artifacts(profile, {"own-app"}, {"own_app"})) == {own, *older}
    assert not subject.unrecognised_output(profile)
    assert subject.prune_after_build(tmp_path / "Cargo.toml", target) == 5
    assert not own.exists() and not any(path.exists() for path in older)
    assert all((package / "fedcba9876543210/fingerprint/invoked.timestamp").is_file() for package in kept)
    assert all(path.exists() for path in other)


def unsupported_cases(profile):
    """Output that fits neither layout, each to be refused with valid units of both layouts beside it."""
    return {
        "a package with output and no fingerprint in any unit": profile / "build/units/0123456789abcdef/out/own_app.rlib",
        "a folder of another shape under build": profile / "build/v3/own-app/fingerprint/bin-own-app",
        "a folder named as the older layout names one, holding something else":
            profile / "build/v3-0123456789abcdef/own-app/fedcba9876543210/out/own_app.rlib",
        "a member Cargo does not put in a unit": profile / "build/third-party/fedcba9876543210/unexpected/own_app.rlib",
        "a folder inside a unit's fingerprint": profile / "build/third-party/fedcba9876543210/fingerprint/nested/own_app",
        "a file where the older layout keeps a folder": profile / ".fingerprint/own-app.json",
        "a folder inside the older layout's fingerprint": profile / ".fingerprint/third-party-0123456789abcdef/nested/own_app",
        "a hashed folder among the older layout's files": profile / "deps/units-0123456789abcdef/own_app.rlib",
    }


@pytest.mark.parametrize("case", sorted(unsupported_cases(Path("."))))
def test_output_in_a_layout_the_tool_does_not_know_is_refused_beside_valid_units(tmp_path, monkeypatch, capsys, case):
    target = tmp_path / "target"
    profile = target / "debug"
    layout_of_cargo_1_100(profile)
    older_layout(profile, "own-app", "own_app", "1111111111111111", "2222222222222222")
    older_layout(profile, "third-party", "third_party")
    own_app_only(monkeypatch)
    assert not subject.unrecognised_output(profile)
    unsupported = unsupported_cases(profile)[case]
    unsupported.parent.mkdir(parents=True, exist_ok=True)
    unsupported.write_text("stale")
    assert subject.unrecognised_output(profile)
    for prune in (subject.prune, subject.prune_after_build):
        with pytest.raises(ValueError, match="not in a layout this tool knows"):
            prune(tmp_path / "Cargo.toml", target)
    # Refused before anything is removed, and the save command exits non-zero.
    assert unsupported.is_file() and (profile / "build/own-app").is_dir()
    monkeypatch.setattr(subject.sys, "argv", ["rust_dep_cache.py", "prune", "--manifest-path",
                                              str(tmp_path / "Cargo.toml"), "--target-dir", str(target)])
    assert subject.main() == 2 and "::error::" in capsys.readouterr().out
    report = subject.restored(tmp_path / "Cargo.toml", target, "some-key")
    assert not target.exists() and "building everything" in report


def test_these_shapes_of_ordinary_and_interrupted_output_are_accepted(tmp_path, monkeypatch):
    target = tmp_path / "target"
    profile = target / "debug"
    layout_of_cargo_1_100(profile)
    older_layout(profile, "third-party", "third_party")
    unit = profile / "build/third-party/0123456789abcdef"
    # A build script's run, its lock, artifact output, and an output folder made before its fingerprint.
    for folder in (unit / "run", unit / "artifact/bin", profile / "build/third-party/aaaaaaaaaaaaaaaa/out/generated"):
        folder.mkdir(parents=True)
    for file in (unit / "run/stdout", unit / "run/invoked.timestamp", unit / ".lock", unit / "out/nested.rs"):
        file.write_text("")
    # The older layout's build script folders, a debug-symbol bundle and a diagnostic file.
    script = profile / "build/third-party-0123456789abcdef"
    for name in ("build_script_build-0123456789abcdef", "build_script_build-0123456789abcdef.d",
                 "build-script-test-build"):
        (script / name).write_text("")
    (script / "build_script_build-0123456789abcdef.dSYM/Contents").mkdir(parents=True)
    run = profile / "build/third-party-fedcba9876543210"
    for name in ("output", "root-output", "stderr", "invoked.timestamp"):
        (run / name).write_text("")
    (run / "out/deep/er").mkdir(parents=True)
    (profile / "deps/libthird_party-0123456789abcdef.dylib.dSYM/Contents").mkdir(parents=True)
    (profile / "deps/third_party-0123456789abcdef.long-type-123.txt").write_text("")
    own_app_only(monkeypatch)
    assert subject.unrecognised_output(profile) == []
    assert subject.prune_after_build(tmp_path / "Cargo.toml", target) == 1
    assert (unit / "run/stdout").is_file() and (run / "out/deep/er").is_dir()
    assert (profile / "deps/libthird_party-0123456789abcdef.dylib.dSYM").is_dir()


def test_files_without_a_hash_in_deps_are_removed_whatever_they_are_named(tmp_path, monkeypatch):
    # A library built under a name it no longer has, saved by the tool as it was before
    # it removed such files: no fingerprint names it and the current target names do not
    # match it. A linker's temporary folder left by an interrupted build goes the same way.
    target = tmp_path / "target"
    profile = target / "debug"
    kept = older_layout(profile, "third-party", "third_party")
    stale = [profile / "deps/libold_name.dylib", profile / "deps/old_name.d",
             profile / "deps/old_name.old_name.0123456789abcdef-cgu.0.rcgu.o"]
    for file in stale:
        file.write_text("stale")
    (profile / "deps/rustcAbCdEf").mkdir()
    own_app_only(monkeypatch, packages=("own-app",), crates=("new_name",))
    assert subject.unrecognised_output(profile) == []
    # None of the four names a current package or target, so none is counted as the repository's.
    assert "removed 0" in subject.restored(tmp_path / "Cargo.toml", target, "some-key")
    assert not any(file.exists() for file in stale) and not (profile / "deps/rustcAbCdEf").exists()
    assert all(path.exists() for path in kept)
    # The same at save, with the repository's own units beside it. Only those four count.
    for file in stale:
        file.write_text("stale")
    older_layout(profile, "own-app", "new_name", "1111111111111111", "2222222222222222")
    assert subject.prune_after_build(tmp_path / "Cargo.toml", target) == 4
    assert not any(file.exists() for file in stale) and all(path.exists() for path in kept)


def test_compiler_scratch_left_in_a_build_scripts_folder_is_removed_not_refused(tmp_path, monkeypatch):
    # rustc links in a temporary directory beside its output; an interrupted link of a
    # build script leaves it in the older layout's `build/<package>-<hash>/`.
    target = tmp_path / "target"
    profile = target / "debug"
    own = older_layout(profile, "own-app", "own_app", "1111111111111111", "2222222222222222")
    kept = older_layout(profile, "third-party", "third_party")
    scratch = [own[1] / "rustcl56x0c", kept[1] / "rustcoOub7N"]
    for folder in scratch:
        (folder / "symbols.o").parent.mkdir()
        (folder / "symbols.o").write_text("")
    own_app_only(monkeypatch)
    assert subject.unrecognised_output(profile) == []
    # At save: the repository's four paths count, the dependency's scratch goes uncounted.
    assert subject.prune_after_build(tmp_path / "Cargo.toml", target) == 4
    assert not any(folder.exists() for folder in scratch)
    assert all(path.exists() for path in kept) and not any(path.exists() for path in own)
    # After a matched restore: removed again, and the restored output is kept.
    scratch[1].mkdir()
    assert "removed 0" in subject.restored(tmp_path / "Cargo.toml", target, "some-key")
    assert not scratch[1].exists() and all(path.exists() for path in kept)
    # Reject a scratch directory whose name has the wrong form.
    (kept[1] / "rustc-other").mkdir()
    with pytest.raises(ValueError, match="not in a layout this tool knows"):
        subject.prune(tmp_path / "Cargo.toml", target)
    # Reject a regular file with the scratch spelling.
    (kept[1] / "rustc-other").rmdir()
    (kept[1] / "rustcl56x0c").write_text("")
    with pytest.raises(ValueError, match="not in a layout this tool knows"):
        subject.prune(tmp_path / "Cargo.toml", target)


def test_the_older_layouts_output_with_no_fingerprint_beside_it_is_refused(tmp_path, monkeypatch):
    target = tmp_path / "target"
    (target / "debug/deps").mkdir(parents=True)
    (target / "debug/deps/libthird_party-0123456789abcdef.rlib").write_text("")
    own_app_only(monkeypatch)
    with pytest.raises(ValueError, match="not in a layout this tool knows"):
        subject.prune(tmp_path / "Cargo.toml", target)


def test_a_repository_package_name_shared_with_another_package_is_refused(tmp_path, monkeypatch):
    # Package-name matching can conflate units from different package IDs.
    target = tmp_path / "target"
    own, kept = layout_of_cargo_1_100(target / "debug")
    own_app_only(monkeypatch)
    lock = tmp_path / "Cargo.lock"
    one = '[[package]]\nname = "own-app"\nversion = "0.1.0"\n\n[[package]]\nname = "own-app-helper"\nversion = "1.0.0"\n'
    lock.write_text(one)
    assert subject.shared_names(tmp_path / "Cargo.toml", {"own-app"}) == []
    # Valid TOML that is not spelled as Cargo writes it: a comment, and the name not first.
    for other in ('\n# another source\n[[package]]\nversion = "9.0.0"\nname = "own-app"\n',
                  # A name differing only in case shares the folder on a case-insensitive disk.
                  '\n[[package]]\nname = "Own-App"\nversion = "9.0.0"\n'):
        lock.write_text(one + other)
        assert subject.shared_names(tmp_path / "Cargo.toml", {"own-app"}) == ["own-app"]
        with pytest.raises(ValueError, match="cannot be told apart"):
            subject.prune_after_build(tmp_path / "Cargo.toml", target)
        assert own.is_dir()
    report = subject.restored(tmp_path / "Cargo.toml", target, "some-key")
    assert not target.exists() and "building everything" in report


def test_a_package_folder_named_in_another_case_is_removed_with_the_repositorys(tmp_path, monkeypatch):
    target = tmp_path / "target"
    own, kept = layout_of_cargo_1_100(target / "debug", ("Own-App", "third-party"))
    own_app_only(monkeypatch)
    assert subject.prune_after_build(tmp_path / "Cargo.toml", target) == 1
    assert not own.exists() and kept[0].is_dir()


def test_the_lockfile_read_is_the_workspace_roots_not_a_nearer_one(tmp_path):
    if shutil.which("cargo") is None:
        if os.environ.get("CI"):
            pytest.fail("cargo is required to locate the workspace root in CI")
        pytest.skip("cargo is not installed")
    member = tmp_path / "member"
    (member / "src").mkdir(parents=True)
    (tmp_path / "Cargo.toml").write_text('[workspace]\nmembers = ["member"]\nresolver = "2"\n')
    (member / "Cargo.toml").write_text('[package]\nname = "own-app"\nversion = "0.1.0"\nedition = "2021"\n')
    (member / "src/lib.rs").write_text("")
    package = '[[package]]\nname = "own-app"\nversion = "{}"\n'
    # A stale lockfile beside the member names the package once; the workspace's names it twice.
    (member / "Cargo.lock").write_text(package.format("0.1.0"))
    assert subject.lockfile(member / "Cargo.toml") is None
    (tmp_path / "Cargo.lock").write_text(package.format("0.1.0") + "\n" + package.format("9.0.0"))
    assert subject.lockfile(member / "Cargo.toml") == (tmp_path / "Cargo.lock").resolve()
    assert subject.shared_names(member / "Cargo.toml", {"own-app"}) == ["own-app"]


def test_the_save_command_fails_when_a_build_left_nothing_of_the_repositorys(tmp_path, monkeypatch, capsys):
    target = tmp_path / "target"
    (target / "debug/.fingerprint/third-party-0123456789abcdef").mkdir(parents=True)
    (target / "debug/deps").mkdir()
    (target / "debug/deps/libthird_party-0123456789abcdef.rlib").write_text("")
    own_app_only(monkeypatch)
    arguments = ["rust_dep_cache.py", "prune", "--manifest-path", str(tmp_path / "Cargo.toml"),
                 "--target-dir", str(target)]
    monkeypatch.setattr(subject.sys, "argv", arguments)
    assert subject.main() == 2
    assert "::error::" in capsys.readouterr().out
    assert (target / "debug/deps/libthird_party-0123456789abcdef.rlib").is_file()
    # A save needs a match whatever the tree holds: with no target at all it is refused too.
    shutil.rmtree(target)
    assert subject.main() == 2
    assert "nothing is saved" in capsys.readouterr().out


def test_the_save_command_refuses_a_tree_holding_only_compiler_scratch(tmp_path, monkeypatch, capsys):
    # No fingerprint anywhere: only a temporary directory rustc left in deps.
    target = tmp_path / "target"
    (target / "debug/deps/rustcl56x0c").mkdir(parents=True)
    (target / "debug/deps/rustcl56x0c/symbols.o").write_text("")
    own_app_only(monkeypatch)
    arguments = ["rust_dep_cache.py", "prune", "--manifest-path", str(tmp_path / "Cargo.toml"),
                 "--target-dir", str(target)]
    monkeypatch.setattr(subject.sys, "argv", arguments)
    assert subject.main() == 2
    printed = capsys.readouterr().out
    assert "::error::" in printed and "Removed" not in printed
    # A matched restore of the same tree removes the scratch and succeeds with zero matches.
    (target / "debug/deps/rustcl56x0c").mkdir(exist_ok=True)
    assert "removed 0" in subject.restored(tmp_path / "Cargo.toml", target, "some-key")
    assert not (target / "debug/deps/rustcl56x0c").exists()


def test_the_save_command_does_not_take_removed_compiler_scratch_for_the_repositorys(tmp_path, monkeypatch, capsys):
    # A dependency's fingerprint and library, and a temporary directory rustc left in deps.
    target = tmp_path / "target"
    (target / "debug/.fingerprint/serde-0123456789abcdef").mkdir(parents=True)
    (target / "debug/deps/rustcl56x0c").mkdir(parents=True)
    (target / "debug/deps/libserde-0123456789abcdef.rlib").write_text("")
    own_app_only(monkeypatch)
    monkeypatch.setattr(subject.sys, "argv", ["rust_dep_cache.py", "prune", "--manifest-path",
                                              str(tmp_path / "Cargo.toml"), "--target-dir", str(target)])
    assert subject.main() == 2
    printed = capsys.readouterr().out
    assert "::error::" in printed and "Removed" not in printed
    assert (target / "debug/deps/libserde-0123456789abcdef.rlib").is_file()


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
    own_app_only(monkeypatch)
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
    # Exact lines, so a widened condition such as `true || ...` fails here.
    same = "github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository"
    root = Path(__file__).resolve().parents[2]
    setup = (root / '.github/actions/app-v4-setup/action.yml').read_text().splitlines()
    save = (root / '.github/actions/app-v4-rust-cache-save/action.yml').read_text()
    lines = [line.strip() for line in setup]
    assert 'SAME_REPOSITORY: ${{ ' + same + ' }}' in lines
    # The npm cache also needs the caller not to have turned it off (npm-cache: 'false'); that only narrows it.
    assert "cache: ${{ inputs.npm-cache != 'false' && (" + same + ") && 'npm' || '' }}" in lines
    assert sum(line.startswith('cache:') for line in lines) == 1
    assert "if [ \"$SAME_REPOSITORY\" != 'true' ]; then" in lines
    assert '{ echo "key="; echo "prefix="; } >> "$GITHUB_OUTPUT"' in lines
    restore = lines[lines.index('id: rust-dependencies'):lines.index('uses: actions/cache/restore@v4')]
    assert "if: steps.rust-cache-key.outputs.key != ''" in restore
    assert "if: inputs.key != '' && inputs.already-cached != 'true'" in save
