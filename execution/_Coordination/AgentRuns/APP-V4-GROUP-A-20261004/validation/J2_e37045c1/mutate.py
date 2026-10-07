"""Apply one mutation at a time to compatibility_report.rs, run the module tests,
record the failing tests, and always restore the exact original bytes."""
import hashlib, pathlib, subprocess, re

D = "/private/tmp/claude-501/-Users-ryan-ai-env-projects-chirality--claude-worktrees-test-ci-optimization-f6cacd/a7659cd3-fdee-45df-ac08-f767111a9f26/scratchpad/j2"
target = pathlib.Path("/Users/ryan/ai-env/projects/chirality/.claude/worktrees/agent-af2ce0ad2cee92fc1/projects/chirality-app-v4/app/src-tauri/src/compatibility_report.rs")
original = target.read_bytes()
digest = hashlib.sha256(original).hexdigest()

MUTATIONS = {
    "M8-like declared->not_established": ('                "declared"\n', '                "not_established"\n'),
    "M24-like whole-undeclared->not_established": ('        Reading::Undeclared => "undeclared",', '        Reading::Undeclared => "not_established",'),
    "M25-like category-undeclared->declared_empty": ('Some(Reading::Undeclared) | None => "undeclared",', 'Some(Reading::Undeclared) | None => "declared_empty",'),
    "M14-like invalid checkpoint->valid": ('Reading::Invalid => "invalid",', 'Reading::Invalid => "valid",'),
    "M16-like partial catalog->unreadable": (
        "CatalogCoverage::Partial(c) | CatalogCoverage::Complete(c) => (Some(true), Some(c)),",
        "CatalogCoverage::Partial(c) => (Some(false), Some(c)),\n        CatalogCoverage::Complete(c) => (Some(true), Some(c)),",
    ),
    "M27-like fallback dropped from purpose": ('format!("{purpose} (fallback: {fallback})")', 'format!("{purpose}{}", if fallback.is_empty() { "" } else { "" })'),
    "M21-like CK-3 empty earlier report accepted": ("if nonempty(Some(earlier_report)).is_some()", "if true"),
}

summary = []
try:
    for name, (old, new) in MUTATIONS.items():
        text = original.decode()
        assert text.count(old) == 1, (name, text.count(old))
        target.write_text(text.replace(old, new))
        slug = re.sub(r"[^A-Za-z0-9]+", "-", name.split()[0])
        log = f"{D}/mutation-{slug}.log"
        with open(log, "w") as fh:
            code = subprocess.run(["zsh", f"{D}/cargo.sh", "test", "--offline", "--locked", "--lib", "execution_compatibility::report::tests"], stdout=fh, stderr=subprocess.STDOUT).returncode
        failed = [l.split()[1].rsplit("::", 1)[-1] for l in open(log) if l.startswith("test ") and l.rstrip().endswith("FAILED")]
        summary.append((name, code, failed))
        target.write_bytes(original)
finally:
    target.write_bytes(original)
assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
for name, code, failed in summary:
    print(f"{name}: exit={code} failed={failed}")
print("restored", digest)
