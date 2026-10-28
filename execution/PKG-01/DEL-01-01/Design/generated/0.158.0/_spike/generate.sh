#!/bin/zsh
# W11 pin spike (APP-V4-FIRST-INCREMENT-20260928) — generator runs at Codex 0.158.0.
# Reproduction helper; spike evidence only, not qualification.
#
# Usage: generate.sh <scratch-root>
#   <scratch-root>/pkg        npm prefix holding @openai/codex@0.158.0
#                             (npm install --prefix <scratch-root>/pkg @openai/codex@0.158.0)
#   <scratch-root>/codex-home empty directory used as CODEX_HOME (never ~/.codex)
#   <scratch-root>/gen/<variant>/run{1,2}   outputs written here
#
# Variants: ts-stable, ts-experimental, schema-stable, schema-experimental.
# Each variant is generated twice; per-file sha256 manifests are compared.
# Prettier is not passed (-p omitted), so TS output is the generator's raw form.
set -u
S="$1"
C="$S/pkg/node_modules/.bin/codex"
export CODEX_HOME="$S/codex-home"
mkdir -p "$CODEX_HOME"
LOG="$S/gen/commands.log"
mkdir -p "$S/gen"
: > "$LOG"

run() {
  local variant="$1" n="$2"; shift 2
  local out="$S/gen/$variant/run$n"
  rm -rf "$out"; mkdir -p "$out"
  "$C" "$@" --out "$out" > "$S/gen/$variant/run$n.stdout" 2> "$S/gen/$variant/run$n.stderr"
  local rc=$?
  print -r -- "codex $* --out <scratch>/gen/$variant/run$n  EXIT=$rc" >> "$LOG"
  (cd "$out" && find . -type f | LC_ALL=C sort | xargs shasum -a 256) > "$S/gen/$variant/run$n.sha256"
}

for n in 1 2; do
  run ts-stable            $n app-server generate-ts
  run ts-experimental      $n app-server generate-ts --experimental
  run schema-stable        $n app-server generate-json-schema
  run schema-experimental  $n app-server generate-json-schema --experimental
done

for v in ts-stable ts-experimental schema-stable schema-experimental; do
  if cmp -s "$S/gen/$v/run1.sha256" "$S/gen/$v/run2.sha256"; then
    print -r -- "determinism $v: IDENTICAL ($(wc -l < "$S/gen/$v/run1.sha256" | tr -d ' ') files; manifest sha256 $(shasum -a 256 < "$S/gen/$v/run1.sha256" | cut -d' ' -f1))" >> "$LOG"
  else
    print -r -- "determinism $v: DIFFERENT" >> "$LOG"
  fi
done
cat "$LOG"
