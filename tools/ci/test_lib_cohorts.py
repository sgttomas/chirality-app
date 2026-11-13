"""Regressions for check_lib_cohorts.py, on invented test lists and workflows."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_lib_cohorts as cohorts  # noqa: E402

FOCUSED = f'"{cohorts.PULL_REQUEST_CONDITION}"'
FULL = "\"github.event_name == 'workflow_dispatch' || inputs.full_suite\""
LOOP = 'for cohort in $LIB_COHORTS; do cargo test --locked --manifest-path src-tauri/Cargo.toml --lib "$cohort" -- --test-threads=1; done'


def workflow(lib_cohorts: str, steps: list[str] = (LOOP,), full_steps: list[str] = ()) -> str:
    def block(runs):
        return "".join(f"      - name: step {i}\n        run: '{run}'\n" for i, run in enumerate(runs)) or "      []\n"
    return (
        "jobs:\n"
        f"  shard:\n    if: {FOCUSED}\n    env:\n      LIB_COHORTS: >-\n          {lib_cohorts}\n    steps:\n{block(steps)}"
        f"  product:\n    if: {FULL}\n    steps:\n{block(full_steps)}"
    )


def listing(*tests: str) -> str:
    return "".join(f"{t}: test\n" for t in tests) + f"\n{len(tests)} tests, 0 benchmarks\n"


TESTS = listing("a::tests::one", "a::tests::two", "b::tests::three", "b::tests::deep::four", "top_level")


def test_selected_and_excluded_tests_pass():
    problems, counts = cohorts.check(
        TESTS, workflow("a::tests top_level"),
        "b::tests: full route only\nb::tests::deep: selected only with the feature\n")
    assert problems == []
    assert counts == {"tests": 5, "selected": 3, "excluded": 2, "ignored": 0}


def test_unselected_unexcluded_test_is_named():
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level"), "b::tests: full route only\n")
    assert problems == [
        "b::tests::deep::four is selected by no pull-request cohort and covered by no line of tools/ci/lib_cohort_exclusions.txt"]


def test_a_module_line_does_not_cover_a_new_submodule():
    problems, _ = cohorts.check(listing("m::tests::x", "m::tests::new::y"), workflow("other_filter_x"), "m::tests: r\n")
    assert "m::tests::new::y is selected by no pull-request cohort and covered by no line of tools/ci/lib_cohort_exclusions.txt" in problems


def test_matching_is_by_substring_as_libtest_does():
    problems, counts = cohorts.check(listing("x::fleet_view::t", "y::z_fleet_::u"), workflow("fleet_"), "")
    assert problems == [] and counts["selected"] == 2


def test_filter_selecting_nothing_fails():
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level b::tests gone_cohort"), "")
    assert problems == ["default-feature filter gone_cohort on shard / step 0 selects no test that is not ignored"]


def test_stale_exclusion_fails():
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level b::tests"), "vanished::tests: r\n")
    assert problems == ["exclusion line vanished::tests covers no test"]


def test_a_line_naming_a_selected_test_fails():
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level b::tests"), "a::tests::one: r\n")
    assert problems == ["a::tests::one is selected by a::tests and excluded by its own line"]


def test_a_module_line_whose_tests_are_all_selected_is_stale():
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level b::tests"), "a::tests: r\n")
    assert problems == ["exclusion line a::tests covers no test"]


def test_a_module_line_covers_only_the_unselected_tests_of_a_mixed_module():
    problems, counts = cohorts.check(TESTS, workflow("a::tests::one top_level b::tests"), "a::tests: r\n")
    assert problems == [] and counts == {"tests": 5, "selected": 4, "excluded": 1, "ignored": 0}


def test_a_test_line_takes_precedence_over_its_module_line():
    tests = listing("m::tests::x", "m::tests::y", "m::tests::z")
    problems, counts = cohorts.check(tests, workflow("m::tests::x"), "m::tests: full route\nm::tests::y: feature step\n")
    assert problems == [] and counts["excluded"] == 2
    # Without the module's other unselected test the module line covers nothing.
    problems, _ = cohorts.check(listing("m::tests::x", "m::tests::y"), workflow("m::tests::x"), "m::tests: r\nm::tests::y: r\n")
    assert problems == ["exclusion line m::tests covers no test"]


def test_empty_list_is_not_a_pass():
    problems, _ = cohorts.check("0 tests, 0 benchmarks\n", workflow("a"), "")
    assert "the test list holds no test" in problems


def test_no_pull_request_filter_is_not_a_pass():
    text = workflow("a::tests", steps=["npm run build"], full_steps=["cargo test --lib a::tests"])
    problems, _ = cohorts.check(TESTS, text, "")
    assert f"no pull-request default-feature cargo test --lib filter found (if: {cohorts.PULL_REQUEST_CONDITION})" in problems


def test_feature_and_full_route_filters_do_not_select():
    text = workflow(
        "a::tests top_level",
        steps=[LOOP, "cargo test --locked --manifest-path src-tauri/Cargo.toml --features distribution-successor --lib b::tests -- --test-threads=1"],
        full_steps=["cargo test --locked --manifest-path src-tauri/Cargo.toml --lib b::tests"])
    problems, _ = cohorts.check(TESTS, text, "")
    assert [p for p in problems if p.startswith("b::tests::three")]


def test_standalone_step_filter_and_exact_match():
    text = workflow("a::tests", steps=[
        LOOP,
        "cargo test --locked --manifest-path src-tauri/Cargo.toml --lib b::tests -- --test-threads=1",
        "cargo test --locked --lib top_level -- --exact",
        "cargo test --locked --manifest-path src-tauri/Cargo.toml --tests --no-run"])
    problems, counts = cohorts.check(TESTS, text, "")
    assert problems == [] and counts["selected"] == 5
    problems, _ = cohorts.check(listing("top_level", "top_level_two"), workflow("zz", steps=["cargo test --lib top_level -- --exact"]), "")
    assert problems == ["top_level_two is selected by no pull-request cohort and covered by no line of tools/ci/lib_cohort_exclusions.txt"]


def test_exclusion_without_reason_or_repeated_fails():
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level"), "b::tests\nb::tests::deep: r\nb::tests::deep: again\n")
    assert "exclusion line 1 gives no reason: b::tests" in problems
    assert "b::tests::deep is excluded twice" in problems


def test_prune_drops_only_stale_and_selected_lines_and_adds_nothing():
    text = "# kept comment\na::tests: now selected\nb::tests: kept reason\nb::tests::deep::four: selected too\ngone::tests: stale\n"
    kept, dropped = cohorts.prune(TESTS, workflow("a::tests top_level b::tests::deep"), text)
    assert kept == "# kept comment\nb::tests: kept reason\n"
    assert sorted(dropped) == ["a::tests", "b::tests::deep::four", "gone::tests"]
    kept, _ = cohorts.prune(TESTS, workflow("top_level"), "a::tests: r\n")
    assert kept == "a::tests: r\n"  # b::tests stays a failure for a person to decide
    assert cohorts.check(TESTS, workflow("top_level"), kept)[0]


def test_this_repository_workflow_yields_filters():
    workflow_text = (cohorts.ROOT / cohorts.WORKFLOW).read_text(encoding="utf-8")
    default, featured = cohorts.pull_request_filters(cohorts.read_workflow(workflow_text))
    assert len(default) > 50 and "terminal_exchange_actual_selected_and_unselected_roundtrip" in default
    assert "s2_" in featured and "s2_" not in default
    entries, problems = cohorts.parse_exclusions((cohorts.ROOT / cohorts.EXCLUSIONS).read_text(encoding="utf-8"))
    assert problems == [] and entries


def test_the_standard_library_reading_agrees_with_pyyaml_on_this_workflow():
    # The macOS job has no YAML library; this is what lets the check rely on its own reader there.
    workflow_text = (cohorts.ROOT / cohorts.WORKFLOW).read_text(encoding="utf-8")
    ours, theirs = cohorts.read_workflow(workflow_text)["jobs"], yaml.safe_load(workflow_text)["jobs"]
    assert list(ours) == list(theirs)
    for job_id, job in theirs.items():
        assert ours[job_id].get("if") == job.get("if"), job_id
        assert str((ours[job_id].get("env") or {}).get("LIB_COHORTS", "")).split() == \
            str((job.get("env") or {}).get("LIB_COHORTS", "")).split(), job_id
    ours_problems, theirs_problems = [], []
    assert cohorts.pull_request_filters(cohorts.read_workflow(workflow_text), ours_problems) == \
        cohorts.pull_request_filters(yaml.safe_load(workflow_text), theirs_problems)
    assert ours_problems == theirs_problems == []


def test_the_real_check_step_lists_and_checks_in_the_compile_job():
    jobs = yaml.safe_load((cohorts.ROOT / cohorts.WORKFLOW).read_text(encoding="utf-8"))["jobs"]
    names = [step.get("name") for step in jobs["rust-integration"]["steps"]]
    compile_at = names.index("Compile every Rust test target once")
    step = jobs["rust-integration"]["steps"][compile_at + 1]
    assert "-- --list" in step["run"] and "tools/ci/check_lib_cohorts.py" in step["run"]
    assert "pip install" not in step["run"]


def test_an_environment_prefixed_cargo_line_is_read():
    text = workflow("a::tests top_level", steps=[LOOP, "CARGO_TERM_COLOR=never cargo test --locked --lib b::tests -- --test-threads=1"])
    problems, counts = cohorts.check(TESTS, text, "")
    assert problems == [] and counts["selected"] == 5


def _jobs(*jobs):
    text = "jobs:\n"
    for name, condition, run in jobs:
        text += f"  {name}:\n" + (f"    if: {condition}\n" if condition is not None else "")
        text += f"    steps:\n      - name: s\n        run: '{run}'\n"
    return text


def test_a_job_with_an_unrecognised_condition_and_a_cargo_lib_line_fails():
    text = _jobs(("shard", FOCUSED, "cargo test --lib a::tests"),
                 ("reworded", "always()", "cargo test --lib top_level"))
    problems, _ = cohorts.check(listing("a::tests::one"), text, "")
    assert problems == [
        "job reworded has a cargo test --lib line and an if the check does not recognise: 'always()' "
        f"(pull request: {cohorts.PULL_REQUEST_CONDITION!r}; full route: {cohorts.FULL_ROUTE_CONDITION!r})"]


def test_a_job_with_an_unrecognised_condition_and_no_cargo_lib_line_is_not_a_finding():
    text = _jobs(("shard", FOCUSED, "cargo test --lib a::tests"), ("result", "always()", "test success = success"))
    assert cohorts.check(listing("a::tests::one"), text, "")[0] == []


def test_a_job_with_no_condition_counts_as_a_pull_request_job():
    text = _jobs(("unconditioned", None, "cargo test --lib a::tests"))
    assert cohorts.check(listing("a::tests::one"), text, "")[0] == []


def test_a_listing_command_selects_nothing():
    text = workflow("a::tests", steps=[LOOP, 'cargo test --locked --manifest-path src-tauri/Cargo.toml --lib -- --list > "$RUNNER_TEMP/l.txt"'])
    problems, _ = cohorts.check(listing("a::tests::one", "b::tests::two"), text, "")
    assert problems == ["b::tests::two is selected by no pull-request cohort and covered by no line of tools/ci/lib_cohort_exclusions.txt"]


IGNORED_REASON = "ignored (#[ignore]): opt-in; run by no hosted job unless someone names it"


def test_an_ignored_test_under_a_full_route_line_fails():
    # The reader's control: a "full route only" line cannot cover an ignored test.
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level"), "b::tests: full route only\nb::tests::deep: r\n",
                                listing("b::tests::three"))
    assert problems == ["b::tests::three is ignored (#[ignore]) but its line b::tests does not say so "
                        "(its reason must begin 'ignored (#[ignore])')"]


def test_an_ignored_test_is_its_own_category_and_never_selected():
    text = workflow("a::tests top_level")
    exclusions = f"a::tests::two: {IGNORED_REASON}\nb::tests: r\nb::tests::deep: r\n"
    problems, counts = cohorts.check(TESTS, text, exclusions, listing("a::tests::two"))
    assert problems == [] and counts == {"tests": 5, "selected": 2, "excluded": 2, "ignored": 1}
    problems, _ = cohorts.check(TESTS, text, "b::tests: r\nb::tests::deep: r\n", listing("a::tests::two"))
    assert problems == ["a::tests::two is ignored (#[ignore]) and covered by no line of tools/ci/lib_cohort_exclusions.txt"]


def test_an_ignored_line_cannot_cover_a_test_that_is_not_ignored():
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level"), f"b::tests: {IGNORED_REASON}\nb::tests::deep: r\n",
                                listing("b::tests::three"))
    assert problems == []
    problems, _ = cohorts.check(TESTS, workflow("a::tests top_level"), f"b::tests: r\nb::tests::deep: {IGNORED_REASON}\n", "")
    assert problems == ["b::tests::deep::four is not ignored but its line b::tests::deep says it is"]


def test_a_filter_matching_only_ignored_tests_selects_nothing():
    problems, _ = cohorts.check(listing("a::t", "b::t"), workflow("a::t b::t"), f"b::t: {IGNORED_REASON}\n", listing("b::t"))
    assert problems == ["default-feature filter b::t on shard / step 0 selects no test that is not ignored"]


def test_ignored_list_from_another_build_fails():
    problems, _ = cohorts.check(listing("a::t"), workflow("a::t"), "", listing("z::t"))
    assert "z::t is in the ignored list but not in the test list (were both listed from one build?)" in problems


def test_an_absorbed_test_is_not_detected():
    # Documented limit: removing a filter that selected a direct test of an excluded module is absorbed by the module line.
    tests = listing("m::tests::x", "m::tests::y", "u::t")
    before, c1 = cohorts.check(tests, workflow("m::tests::x u::t"), "m::tests: r\n")
    after, c2 = cohorts.check(tests, workflow("u::t"), "m::tests: r\n")
    assert before == after == [] and (c1["excluded"], c2["excluded"]) == (1, 2)


def _refusal(run_block: str, steps_yaml: str | None = None) -> list[str]:
    text = ("jobs:\n  shard:\n    if: " + FOCUSED + "\n    env:\n      LIB_COHORTS: a::tests\n    steps:\n"
            + (steps_yaml if steps_yaml is not None else f"      - name: s\n        run: {run_block}\n"))
    return [p for p in cohorts.check(TESTS, text, "")[0] if "cannot read" in p]


def test_refuses_more_than_one_filter():
    assert _refusal("cargo test --lib a::tests -- b::tests --test-threads 1") == [
        "shard / s: the check cannot read more than one test filter (the check reads one)"]


def test_refuses_skip_and_ignored_runs():
    assert _refusal("cargo test --lib a::tests -- --skip x") == ["shard / s: the check cannot read --skip (the check does not read it)"]
    assert _refusal("cargo test --lib a::tests -- --include-ignored") == [
        "shard / s: the check cannot read --ignored or --include-ignored (the check does not count runs of ignored tests)"]


def test_refuses_a_step_level_lib_cohorts():
    steps = "      - name: s\n        env:\n          LIB_COHORTS: b::tests\n        run: cargo test --lib a::tests\n"
    assert _refusal("", steps) == ["shard / s: the check cannot read a step-level LIB_COHORTS (the check reads only the job's)"]


def test_refuses_a_step_level_if_on_a_library_test_command():
    steps = "      - name: s\n        if: false\n        run: cargo test --lib a::tests\n"
    assert _refusal("", steps) == [
        "shard / s: the check cannot read a step-level if on a library test command (the check does not evaluate step conditions)"]
    assert _refusal("", "      - name: s\n        if: always()\n        run: npm test\n") == []


def test_refuses_a_folded_block_with_blank_lines():
    steps = "      - name: s\n        run: >-\n          cargo test --lib a::tests\n\n          -- --test-threads=1\n"
    assert _refusal("", steps) == ["shard / s: the check cannot read run: a folded block with blank lines"]


def test_refuses_a_quoted_run_with_a_trailing_comment():
    assert _refusal("'cargo test --lib a::tests' # note") == [
        "shard / s: the check cannot read run: a quoted scalar followed by other text (such as a comment)"]


def test_refuses_anchors_and_aliases():
    steps = "      - name: s\n        run: &cmd cargo test --lib a::tests\n      - name: t\n        run: *cmd\n"
    assert _refusal("", steps) == ["shard / s: the check cannot read run: an anchor, alias or merge key",
                                   "shard / t: the check cannot read run: an anchor, alias or merge key"]


def test_refuses_an_expression_in_a_filter():
    # The expression also splits into several words, so it is refused as more than one filter as well.
    assert "shard / s: the check cannot read a ${{ }} expression in a filter" in _refusal("cargo test --lib ${{ matrix.cohort }}")
