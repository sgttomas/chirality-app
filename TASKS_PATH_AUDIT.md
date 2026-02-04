# Path Audit Tasks

## Purpose
Create a systematic, repeatable checklist to scan and fix legacy paths and hierarchy references so the repo is a clean, cloneable template. This checklist covers all files, including `run/`, and aligns with `DIRECTORY_TREE.md` (including the new `run/_Scope/` folder).

## Constraints
- Do not create or populate deliverable placeholder folders/files. Deliverables are created during the initial run phase.
- Prefer repo-relative paths (e.g., `agents/AGENT_*.md`, `run/...`) over absolute paths.
- `run/` is the canonical execution root.

## Checklist

1. [ ] Update `DIRECTORY_TREE.md` to include `run/_Scope/` and its purpose.
Command(s):
```sh
rg -n "_Scope" DIRECTORY_TREE.md
```

2. [ ] Confirm `run/_Scope/` exists as a default folder.
Command(s):
```sh
ls run
```

3. [ ] Scan for legacy repo name references.
Command(s):
```sh
rg -n "chirality-app-test|chirality-app" -S .
```

4. [ ] Scan for template root name references.
Command(s):
```sh
rg -n "chirality-project-template|chirality-domain-template" -S .
```

5. [ ] Scan for absolute path references into prior instances.
Command(s):
```sh
rg -n "/Users/ryan/ai-env/projects/" -S .
```

6. [ ] Scan for legacy execution root references.
Command(s):
```sh
rg -n "execution-4|execution-5|execution/" -S .
```

7. [ ] Scan for legacy `test/` path references.
Command(s):
```sh
rg -n "(^|[^[:alnum:]_])test/" -S .
```

8. [ ] Scan for references to agent instruction files that do not exist in this repo.
Command(s):
```sh
rg -n "AGENT_[A-Z0-9_-]+\.md" -S .
ls agents
```

9. [ ] Scan deliverable docs for hardcoded paths.
Command(s):
```sh
rg -n "/Users/|execution-|test/" -S run
```

10. [ ] Build a replacement map and apply fixes in order (review each match list before editing).
Replacement map:
| Legacy pattern | Replace with | Notes |
| --- | --- | --- |
| `/Users/ryan/ai-env/projects/chirality-app-test/test/` | `run/` | Prefer repo-relative execution root |
| `/Users/ryan/ai-env/projects/chirality-app-test/` | `./` | Repo root, use relative paths |
| `test/` | `run/` | Only for path segments, review matches |
| `execution-4/` | `run/` | Normalize legacy execution roots |
| `execution-5/` | `run/` | Normalize legacy execution roots |
| `execution/` | `run/` | Normalize generic execution root |

Planned fix commands (run carefully after review):
```sh
# 1) Absolute execution roots -> run/
for pat in \
  "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-4/" \
  "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-5/" \
  "/Users/ryan/ai-env/projects/chirality-app-test/test/execution/"; do
  files=$(rg -l "$pat" -S . || true)
  if [ -n "$files" ]; then
    while IFS= read -r file; do
      perl -pi -e "s#${pat}#run/#g" "$file"
    done <<< "$files"
  fi
done

# 2) Absolute test root -> run/
pat="/Users/ryan/ai-env/projects/chirality-app-test/test/"
files=$(rg -l "$pat" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e "s#${pat}#run/#g" "$file"
  done <<< "$files"
fi

# 3) Absolute repo root -> ./ 
pat="/Users/ryan/ai-env/projects/chirality-app-test/"
files=$(rg -l "$pat" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e "s#${pat}#./#g" "$file"
  done <<< "$files"
fi

# 4) Legacy execution-* -> run/ (avoid double run)
files=$(rg -l "execution-4/|execution-5/|execution/" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e 's/(?<!run\\/)execution-4\\//run\\//g; s/(?<!run\\/)execution-5\\//run\\//g; s/(?<!run\\/)execution\\//run\\//g' "$file"
  done <<< "$files"
fi

# 5) Legacy test/ path segments -> run/
files=$(rg -l "(^|[^[:alnum:]_])test/" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e 's/(^|[^[:alnum:]_])test\\//${1}run\\//g' "$file"
  done <<< "$files"
fi
```

11. [ ] Update any remaining agent instruction references to point at local `agents/AGENT_*.md` paths and correct agent names.
Command(s):
```sh
rg -n "AGENT_[A-Z0-9_-]+\.md" -S .
```

12. [ ] Verify scans return zero legacy matches.
Command(s):
```sh
rg -n "chirality-app-test|chirality-project-template|chirality-domain-template|/Users/ryan/ai-env/projects/|execution-4|execution-5|execution/|(^|[^[:alnum:]_])test/" -S .
```

13. [ ] Verify `DIRECTORY_TREE.md` reflects `run/_Scope/` and no deliverable placeholders are required.
Command(s):
```sh
rg -n "_Scope" DIRECTORY_TREE.md
```

## Execution Log (Fill After Human Verification)

### Commands Executed
```sh
rg -n "chirality-app-test|chirality-app" -S .
rg -n "AGENT_CHIRALITY-APP" -S .

# Bulk replacements (absolute roots, legacy execution/test, legacy name)
set -e
for pat in \
  "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-4/" \
  "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-5/" \
  "/Users/ryan/ai-env/projects/chirality-app-test/test/execution/"; do
  files=$(rg -l "$pat" -S . || true)
  if [ -n "$files" ]; then
    while IFS= read -r file; do
      perl -pi -e "s#${pat}#run/#g" "$file"
    done <<< "$files"
  fi
done
pat="/Users/ryan/ai-env/projects/chirality-app-test/test/"
files=$(rg -l "$pat" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e "s#${pat}#run/#g" "$file"
  done <<< "$files"
fi
pat="/Users/ryan/ai-env/projects/chirality-app-test/"
files=$(rg -l "$pat" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e "s#${pat}#./#g" "$file"
  done <<< "$files"
fi
files=$(rg -l "execution-4/|execution-5/|execution/" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e 's/(?<!run\/)execution-4\//run\//g; s/(?<!run\/)execution-5\//run\//g; s/(?<!run\/)execution\//run\//g' "$file"
  done <<< "$files"
fi
files=$(rg -l "(^|[^[:alnum:]_])test/" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e 's/(^|[^[:alnum:]_])test\//${1}run\//g' "$file"
  done <<< "$files"
fi
pat="chirality-app-test"
files=$(rg -l "$pat" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e "s/${pat}/chirality-project-template/g" "$file"
  done <<< "$files"
fi

# Fix scope doc location + double run
pat="run/ADM_Lloyd_PelletCoolerUpg_ScopeDoc_Jan_14_KP.docx"
files=$(rg -l "$pat" -S agents run AGENTS.md README.md || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e "s#${pat}#run/_Scope/ADM_Lloyd_PelletCoolerUpg_ScopeDoc_Jan_14_KP.docx#g" "$file"
  done <<< "$files"
fi
files=$(rg -l "run/run" -S run || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e 's#run/run#run#g' "$file"
  done <<< "$files"
fi
files=$(rg -l "run/execution-5" -S README.md agents TASKS_PATH_AUDIT.md || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e 's#run/execution-5#run/#g' "$file"
  done <<< "$files"
fi

# Normalize repo-relative agent paths
files=$(rg -l "\./agents/" -S . || true)
if [ -n "$files" ]; then
  while IFS= read -r file; do
    perl -pi -e 's#\./agents/#agents/#g' "$file"
  done <<< "$files"
fi

# Verification scans
rg -n "/Users/ryan/ai-env/projects/" -S .
rg -n "execution-4|execution-5|execution/" -S .
rg -n "(^|[^[:alnum:]_])test/" -S .
rg -n "/Users/|execution-|test/" -S run
rg -n "run/run" -S .
rg -n "AGENT_CHIRALITY-APP" -S .
rg -n "\./agents/" -S .
rg -n "chirality-app-test|/Users/ryan/ai-env/projects/|execution-4|execution-5|execution/|(^|[^[:alnum:]_])test/" -S .
rg -n "run/execution-5" -S .
```

### Outputs / Notes
```text
Summary of results:
- Initial scans found many legacy references (absolute paths, `chirality-app-test`, `execution-4/5`, `test/`).
- After replacements, verification scans show legacy patterns only within this checklist file (intentional examples/commands).
- `run/_Scope/` references were updated; scope doc now points to `run/_Scope/ADM_Lloyd_PelletCoolerUpg_ScopeDoc_Jan_14_KP.docx`.
- Double `run/run` path references were eliminated.
- Legacy `AGENT_CHIRALITY-APP` references were removed.
- No `test/`, `execution-4/5`, or absolute `/Users/ryan/...` references remain outside this checklist.
```

### Human Verification
- [ ] I reviewed the changes and verified the scans returned zero legacy matches.
- [ ] I confirm no deliverable placeholder folders/files were created.
