#!/bin/sh
# Owner-run evidence helper for SIGNED_CANDIDATE_OWNER_WITNESS.md (proposal).
# Run ONLY inside the dedicated test user's own Terminal, after owner approval.
#   prepare : create invented fixtures (the only write outside OUT); refuses if present
#   c1 DMG  : pre-launch facts (DMG, mounted App, installed App); read-only
#   c2      : after the pre-enrollment capture, before enrollment; read-only
#   c3      : after the sealed capture, before Quit; read-only
#   c4      : after the final Quit: allowlisted evidence copy; read-only on sources
# Never reads account-homes/ contents, the keychain, or any path outside the
# listed AppData allowlist, the fixtures and the named App/DMG paths.
set -eu
umask 022
APPDATA="$HOME/Library/Application Support/com.chirality.app"
APP="$HOME/Applications/Chirality App v4.app"
MOUNTED="/Volumes/Chirality App v4/Chirality App v4.app"
SHARED="$HOME/ChiralityV4Shared"
PROJECT="$HOME/ChiralityV4Fixtures/p1"
OUT="${CHIRALITY_WITNESS_OUT:-/Users/Shared/chirality-v4-witness-out}"

die() { echo "refused: $*" >&2; exit 2; }
stage() { # create OUT/<name>, never overwrite
  mkdir -p "$OUT"; [ ! -e "$OUT/$1" ] || die "$OUT/$1 already exists"
  mkdir "$OUT/$1"; D="$OUT/$1"
  { date -u '+%Y-%m-%dT%H:%M:%SZ'; whoami; id -Gn; } > "$D/who.txt"
}
manifest() { (cd "$D" && find . -type f ! -name MANIFEST.sha256 -print0 | xargs -0 shasum -a 256 > MANIFEST.sha256); echo "wrote $D"; }
statf() { [ -e "$1" ] && stat -f '%N mode=%Sp inode=%i links=%l size=%z mtime=%Sm' -t '%Y-%m-%dT%H:%M:%S%z' "$1" || echo "$1 absent"; }

case "${1:-}" in
prepare)
  [ "$(cd "$HOME" && pwd -P)" = "$HOME" ] || die "home path is not its real path"
  id -Gn | tr ' ' '\n' | grep -qx admin && die "this user is an administrator"
  [ ! -e "$APPDATA" ] || die "App data already exists"
  [ ! -e "$SHARED" ] && [ ! -e "$HOME/ChiralityV4Fixtures" ] || die "fixtures already exist"
  mkdir -p "$SHARED/skills" "$PROJECT"
  : > "$SHARED/config.toml"
  printf '# Invented witness guidance. No real instructions.\n' > "$SHARED/AGENTS.md"
  printf 'Invented witness file one.\n' > "$PROJECT/check-1.txt"
  printf 'Invented witness file two.\n' > "$PROJECT/check-2.txt"
  echo "Prepared. Use exactly these paths in setup:"
  echo "  Shared config.toml      $SHARED/config.toml"
  echo "  Shared AGENTS.md        $SHARED/AGENTS.md"
  echo "  Shared skills directory $SHARED/skills"
  echo "  Project directory       $PROJECT"
  echo "Do not open or edit these files before the test ends." ;;
c1)
  DMG="${2:-}"; [ -f "$DMG" ] || die "give the downloaded DMG path"
  stage c1
  { sw_vers; statf "$APPDATA"; } > "$D/system.txt" 2>&1
  { shasum -a 256 "$DMG"; xattr -p com.apple.quarantine "$DMG"; } > "$D/dmg.txt" 2>&1 || true
  { xattr -p com.apple.quarantine "$MOUNTED"; spctl -a -vv -t exec "$MOUNTED"; } > "$D/mounted.txt" 2>&1 || true
  { xattr -p com.apple.quarantine "$APP"; codesign -dvvv --entitlements - "$APP"
    codesign --verify --deep --strict --verbose=2 "$APP"; spctl -a -vv -t exec "$APP"; } > "$D/installed.txt" 2>&1 || true
  manifest ;;
c2|c3|c4)
  stage "$1"
  K="$APPDATA/capture-seal-keychain"
  { statf "$K/continuity.s1.json"; statf "$APPDATA/capture-seal"; } > "$D/marker-stat.txt"
  [ -f "$K/continuity.s1.json" ] && cp "$K/continuity.s1.json" "$D/"
  mkdir "$D/captures" "$D/acts"
  for f in "$APPDATA"/records/projects/*/captures/*.json; do [ -f "$f" ] && cp "$f" "$D/captures/"; done
  for f in "$APPDATA"/records/projects/*/acts/*.jsonl; do [ -f "$f" ] && cp "$f" "$D/acts/"; done
  if [ "$1" = c4 ]; then
    [ -f "$APPDATA/desktop-startup/request.json" ] && cp "$APPDATA/desktop-startup/request.json" "$D/"
    for s in "$APPDATA"/runtime/distribution/s1-*/.chirality-s1; do
      [ -d "$s" ] || continue; t="$D/distribution/$(basename "$(dirname "$s")")"; mkdir -p "$t"
      for n in observed installed preflight transport lifecycle; do [ -f "$s/$n.json" ] && cp "$s/$n.json" "$t/"; done
    done
    # Names/metadata only; account-homes/ itself is listed, never entered.
    (cd "$APPDATA" && find . -path ./account-homes/'*' -prune -o -print | sort | while read -r p; do statf "$p"; done) > "$D/appdata-metadata.txt"
    (cd "$HOME/ChiralityV4Fixtures" && find . -type f -print0 | xargs -0 shasum -a 256) > "$D/fixture-sha256.txt"
  fi
  manifest ;;
*) echo "usage: $0 prepare | c1 <dmg> | c2 | c3 | c4" >&2; exit 64 ;;
esac
