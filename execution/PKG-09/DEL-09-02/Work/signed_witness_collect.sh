#!/bin/sh
# Owner-run evidence helper for SIGNED_CANDIDATE_OWNER_WITNESS.md (proposal).
# Run ONLY inside the dedicated test user's own Terminal, after owner approval.
#   prepare        : create the private output root and invented fixtures; refuses if present
#   c1 DMG         : pre-launch gate (DMG, mounted App, installed App); read-only; nonzero = STOP
#   c2             : after the pre-enrollment capture, before enrollment; read-only
#   c3             : after the sealed capture, before Quit; read-only
#   c4             : after the final Quit: allowlisted evidence copy; read-only on sources
#   handoff ACCOUNT: owner-decided; grants that one account read access to the output root
# Output stays private (0700/0600) until handoff. Never enters account-homes/,
# never reads the keychain, never follows a symlink, never overwrites.
set -eu
umask 077
APPDATA="$HOME/Library/Application Support/com.chirality.app"
APP="$HOME/Applications/Chirality App v4.app"
MOUNTED="/Volumes/Chirality App v4/Chirality App v4.app"
SHARED="$HOME/ChiralityV4Shared"
PROJECT="$HOME/ChiralityV4Fixtures/p1"
OUT="${CHIRALITY_WITNESS_OUT:-/Users/Shared/chirality-v4-witness-out}"
DMG_SHA=34ab566132e059d3e51885c87907898238ba95421c88d1303d535d19eafcf26e
EXE_SHA=49f61681ad2b985ef98cc56b01b3f63e2ff4baaad7ec711550453976d5ae43e6
CDHASH=e1bf4644f66389011964e99cec43fc853b6b4158
IDENTITY=chirality.app.bundle-tree.sha256/v2:b3dd4145779e711a0169c08b2f1757eace19e38e08effe03a18c5bef986b5fb8
ENTITLEMENTS='<dict><key>com.apple.application-identifier</key><string>8A7JL35U4S.com.chirality.app</string><key>com.apple.developer.team-identifier</key><string>8A7JL35U4S</string></dict>'
TOOLS=$(cd "$(dirname "$0")" && pwd -P)

die() { echo "refused: $*" >&2; exit 2; }
statf() { if [ -e "$1" ] || [ -L "$1" ]; then stat -f '%N type=%HT mode=%Sp inode=%i links=%l size=%z mtime=%Sm' -t '%Y-%m-%dT%H:%M:%S%z' "$1"; else echo "$1 absent"; fi; }
nolink() { # refuse a symlink at $1 or any ancestor up to $HOME
  p=$1
  while :; do
    [ -L "$p" ] && die "symlink at $p"
    if [ "$p" = "$HOME" ] || [ "$p" = / ]; then break; fi
    p=$(dirname "$p")
  done; }
root_ok() {
  [ -d "$OUT" ] && [ ! -L "$OUT" ] || die "output root $OUT missing; run prepare first"
  [ "$(stat -f %u "$OUT")" = "$(id -u)" ] || die "output root not owned by this user"
  [ "$(stat -f %Lp "$OUT")" = 700 ] || die "output root is not mode 0700"; }
stage() { root_ok; [ ! -e "$OUT/$1" ] || die "$OUT/$1 already exists"; mkdir "$OUT/$1"; D="$OUT/$1"
  { date -u '+%Y-%m-%dT%H:%M:%SZ'; whoami; id -Gn; } > "$D/who.txt"; }
manifest() { (cd "$D" && find . -type f ! -name MANIFEST.sha256 -print0 | xargs -0 shasum -a 256 > MANIFEST.sha256); echo "wrote $D"; }
copyrel() { # copyrel SRC: copy one regular file to $D/appdata/<path relative to APPDATA>
  nolink "$1"; [ -f "$1" ] || die "not a regular file: $1"
  rel=${1#"$APPDATA"/}; dst="$D/appdata/$rel"; [ ! -e "$dst" ] || die "collision at $dst"
  mkdir -p "$(dirname "$dst")"; cp "$1" "$dst"; }
copytree() { # copytree DIR: every regular file under DIR; refuses any symlink inside
  nolink "$1"; [ -z "$(find "$1" -type l -print -quit)" ] || die "symlink inside $1"
  find "$1" -type f > "$D/.list"
  while IFS= read -r f; do copyrel "$f"; done < "$D/.list"
  rm "$D/.list"; }
check() { # check NAME STATUS(0 pass)
  if [ "$2" -eq 0 ]; then echo "PASS $1" >> "$D/gate.txt"; else echo "STOP $1" >> "$D/gate.txt"; G=1; fi; }

case "${1:-}" in
prepare)
  [ "$(cd "$HOME" && pwd -P)" = "$HOME" ] || die "home path is not its real path"
  id -Gn | tr ' ' '\n' | grep -qx admin && die "this user is an administrator"
  [ ! -e "$APPDATA" ] || die "App data already exists"
  [ ! -e "$SHARED" ] && [ ! -e "$HOME/ChiralityV4Fixtures" ] || die "fixtures already exist"
  [ ! -e "$OUT" ] && [ ! -L "$OUT" ] || die "output root $OUT already exists"
  mkdir "$OUT"; mkdir "$OUT/recording"
  umask 022
  mkdir -p "$SHARED/skills" "$PROJECT"
  : > "$SHARED/config.toml"
  printf '# Invented witness guidance. No real instructions.\n' > "$SHARED/AGENTS.md"
  printf 'Invented witness file one.\n' > "$PROJECT/check-1.txt"
  printf 'Invented witness file two.\n' > "$PROJECT/check-2.txt"
  echo "Private output root: $OUT (save the screen recording into $OUT/recording)"
  echo "Use exactly these paths in setup:"
  echo "  Shared config.toml      $SHARED/config.toml"
  echo "  Shared AGENTS.md        $SHARED/AGENTS.md"
  echo "  Shared skills directory $SHARED/skills"
  echo "  Project directory       $PROJECT"
  echo "Do not open or edit these files before the test ends." ;;
c1)
  DMG="${2:-}"; [ -f "$DMG" ] || die "give the downloaded DMG path"
  stage c1; G=0
  { sw_vers; statf "$APPDATA"; } > "$D/system.txt" 2>&1
  shasum -a 256 "$DMG" > "$D/dmg-sha256.txt"
  r=0; grep -q "^$DMG_SHA " "$D/dmg-sha256.txt" || r=1; check dmg-sha256 "$r"
  r=0; xattr -p com.apple.quarantine "$DMG" > "$D/dmg-quarantine.txt" 2>&1 || r=1; check dmg-quarantine "$r"
  xattr -l "$DMG" > "$D/dmg-xattr-l.txt" 2>&1 || true
  r=0; spctl -a -vv -t exec "$MOUNTED" > "$D/mounted-spctl.txt" 2>&1 || r=1; check mounted-gatekeeper "$r"
  xattr -p com.apple.quarantine "$MOUNTED" > "$D/mounted-quarantine.txt" 2>&1 || true
  nolink "$APP"
  echo "$APP" > "$D/installed-path.txt"
  r=0; xattr -p com.apple.quarantine "$APP" > "$D/installed-quarantine.txt" 2>&1 || r=1; check installed-quarantine "$r"
  xattr -l "$APP" > "$D/installed-xattr-l.txt" 2>&1 || true
  r=0; codesign --verify --deep --strict --verbose=2 "$APP" > "$D/installed-verify.txt" 2>&1 || r=1; check installed-deep-strict "$r"
  r=0; spctl -a -vv -t exec "$APP" > "$D/installed-spctl.txt" 2>&1 || r=1
  grep -q 'source=Notarized Developer ID' "$D/installed-spctl.txt" || r=1; check installed-gatekeeper-notarized "$r"
  codesign -dvvv --entitlements - "$APP" > "$D/installed-codesign.txt" 2>&1 || true
  r=0; grep -q "^CDHash=$CDHASH\$" "$D/installed-codesign.txt" || r=1; check installed-cdhash "$r"
  r=0; grep -q '^Identifier=com.chirality.app$' "$D/installed-codesign.txt" || r=1; check installed-identifier "$r"
  r=0; grep -q '^TeamIdentifier=8A7JL35U4S$' "$D/installed-codesign.txt" || r=1; check installed-team "$r"
  codesign -d --entitlements :- "$APP" > "$D/installed-entitlements.plist" 2>/dev/null || true
  r=0; tr -d '\n\t ' < "$D/installed-entitlements.plist" | grep -qF "<plistversion=\"1.0\">$ENTITLEMENTS</plist>" || r=1; check installed-entitlements-exact "$r"
  for x in bin/codex:codex bin/codex-code-mode-host:codex-code-mode-host codex-path/rg:com.openai.codex.rg codex-resources/zsh/bin/zsh:com.openai.codex.zsh; do
    f=${x%%:*}; want=${x#*:}; o="$D/supplier-$(basename "$f").txt"
    codesign -dv "$APP/Contents/Resources/codex/$f" > "$o" 2>&1 || true
    r=0; grep -qx "Identifier=$want" "$o" || r=1; check "supplier-$(basename "$f")-stock" "$r"
  done
  python3 -I "$TOOLS/identify.py" inventory "$APP" > "$D/installed-identity.json" 2>&1 || true
  r=0; grep -qF "\"build_identity\": \"$IDENTITY\"" "$D/installed-identity.json" || r=1; check installed-bundle-tree-v2 "$r"
  shasum -a 256 "$APP/Contents/MacOS/chirality-app-v4" > "$D/installed-exe-sha256.txt" 2>&1 || true
  r=0; grep -q "^$EXE_SHA " "$D/installed-exe-sha256.txt" || r=1; check installed-executable "$r"
  /usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$APP/Contents/Info.plist" > "$D/installed-version.txt" 2>&1 || true
  r=0; grep -qx '4.0.0' "$D/installed-version.txt" || r=1; check installed-version-4.0.0 "$r"
  manifest; cat "$D/gate.txt"
  [ "$G" -eq 0 ] || { echo "STOP: do not launch. Tell the agent." >&2; exit 3; }
  echo "Gate passed: eject the DMG and continue." ;;
c2|c3|c4)
  stage "$1"
  nolink "$APPDATA"
  K="$APPDATA/capture-seal-keychain"
  { statf "$K"; statf "$K/continuity.s1.json"; statf "$APPDATA/capture-seal"; } > "$D/marker-stat.txt"
  if [ -f "$K/continuity.s1.json" ] || [ -L "$K/continuity.s1.json" ]; then copyrel "$K/continuity.s1.json"; fi
  for p in "$APPDATA"/records/projects/*; do
    [ -d "$p" ] || [ -L "$p" ] || continue
    for f in "$p"/captures/*.json "$p"/acts/*.jsonl; do
      [ -f "$f" ] || [ -L "$f" ] || continue; copyrel "$f"
    done
  done
  if [ "$1" = c4 ]; then
    if [ -f "$APPDATA/desktop-startup/request.json" ]; then copyrel "$APPDATA/desktop-startup/request.json"; fi
    for s in "$APPDATA"/runtime/distribution/s1-*; do
      [ -d "$s" ] || [ -L "$s" ] || continue; copytree "$s"
    done
    # Names and metadata only. account-homes is pruned itself, so it is never read.
    (cd "$APPDATA" && { find . -path ./account-homes -prune -o -print | sort | while IFS= read -r p; do statf "$p"; done; statf ./account-homes; }) > "$D/appdata-metadata.txt"
    (cd "$HOME/ChiralityV4Fixtures" && find . -type f -print0 | xargs -0 shasum -a 256) > "$D/fixture-sha256.txt"
  fi
  manifest ;;
handoff)
  A="${2:-}"; [ -n "$A" ] && id -u "$A" >/dev/null 2>&1 || die "give the receiving account name"
  root_ok
  find "$OUT" -type d -exec chmod +a "user:$A allow list,search,readattr,readextattr,readsecurity" {} +
  find "$OUT" -type f -exec chmod +a "user:$A allow read,readattr,readextattr,readsecurity" {} +
  echo "Granted read access to $A only, on $OUT" ;;
*) echo "usage: $0 prepare | c1 <dmg> | c2 | c3 | c4 | handoff <account>" >&2; exit 64 ;;
esac
