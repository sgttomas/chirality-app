#!/bin/sh
# Owner-run evidence helper for SIGNED_CANDIDATE_OWNER_WITNESS.md (proposal).
# Run ONLY inside the dedicated test user's own Terminal, after owner approval.
#   prepare        : create the private output root and invented fixtures; refuses if present
#   c1 DMG         : pre-launch gate (DMG, mounted App, installed App); read-only; nonzero = STOP
#   manifest APP   : print the content-structure manifest digest of APP (preparation aid)
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
PROFILE_SHA=5eccea61c989e499f738376cd843fe55c0c6ba6a6ad5ca86af074acdef965165
CONTENT=ae04bcaaba7c3eb7ec77248cd2302d5449c3421f2e2b353e1b4e2d7e69b14f6a
ENTITLEMENTS='<dict><key>com.apple.application-identifier</key><string>8A7JL35U4S.com.chirality.app</string><key>com.apple.developer.team-identifier</key><string>8A7JL35U4S</string></dict>'

die() { echo "refused: $*" >&2; exit 2; }
NL=$(printf '\n_'); NL=${NL%_}
statf() { if [ -e "$1" ] || [ -L "$1" ]; then stat -f '%N type=%HT mode=%Sp inode=%i links=%l size=%z mtime=%Sm' -t '%Y-%m-%dT%H:%M:%S%z' "$1"; else echo "$1 absent"; fi; }
nolink() { # refuse a symlink at $1 or any ancestor up to $HOME
  _nl=$1
  while :; do
    [ -L "$_nl" ] && die "symlink at $_nl"
    if [ "$_nl" = "$HOME" ] || [ "$_nl" = / ]; then break; fi
    _nl=$(dirname "$_nl")
  done; }
root_ok() {
  [ -d "$OUT" ] && [ ! -L "$OUT" ] || die "output root $OUT missing; run prepare first"
  nolink "$OUT"
  [ "$(stat -f %u "$OUT")" = "$(id -u)" ] || die "output root not owned by this user"
  [ "$(stat -f %Lp "$OUT")" = 700 ] || die "output root is not mode 0700"; }
stage() { root_ok; [ ! -e "$OUT/$1" ] || die "$OUT/$1 already exists"; mkdir "$OUT/$1"; D="$OUT/$1"
  { date -u '+%Y-%m-%dT%H:%M:%SZ'; whoami; id -Gn; } > "$D/who.txt"; }
manifest() { (cd "$D" && find . -type f ! -name MANIFEST.sha256 -print0 | xargs -0 shasum -a 256 > MANIFEST.sha256); echo "wrote $D"; }
copyrel() { # copyrel SRC: copy one regular file to $D/appdata/<path relative to APPDATA>
  nolink "$1"; [ -f "$1" ] || die "not a regular file: $1"
  rel=${1#"$APPDATA"/}; dst="$D/appdata/$rel"; [ ! -e "$dst" ] || die "collision at $dst"
  mkdir -p "$(dirname "$dst")"; cp "$1" "$dst"; }
plain_tree() { # refuse symlinks, special files and newline names inside DIR (checked status)
  nolink "$1"
  _x=$(find "$1" -type l -print -quit) || die "cannot traverse $1"; [ -z "$_x" ] || die "symlink inside $1"
  _x=$(find "$1" ! -type f ! -type d -print -quit) || die "cannot traverse $1"; [ -z "$_x" ] || die "special file inside $1"
  _x=$(find "$1" -name "*$NL*" -print -quit) || die "cannot traverse $1"; [ -z "$_x" ] || die "newline in a name inside $1"; }
copytree() { # copytree DIR: every regular file under DIR
  plain_tree "$1"
  find "$1" -type f > "$D/.list" || die "cannot traverse $1"
  while IFS= read -r f; do copyrel "$f"; done < "$D/.list"
  rm "$D/.list"; }
content() { # content-structure manifest of DIR: path, type, mode, file SHA-256 or link target;
  # no owner, times or xattrs. Never follows links. Every step is checked explicitly
  # (errexit is suppressed when callers use if/||), so any failure exits 2 with no digest.
  ( nolink "$1"
    cd "$1" || exit 2
    _x=$(find . ! -type f ! -type d ! -type l -print -quit) || { echo "refused: cannot traverse $1" >&2; exit 2; }
    [ -z "$_x" ] || { echo "refused: special file in $1" >&2; exit 2; }
    _x=$(find . -name "*$NL*" -print -quit) || { echo "refused: cannot traverse $1" >&2; exit 2; }
    [ -z "$_x" ] || { echo "refused: newline in a name in $1" >&2; exit 2; }
    L=$(mktemp -d "${TMPDIR:-/tmp}/witness-manifest.XXXXXX") || exit 2
    [ -n "$L" ] && [ -d "$L" ] || exit 2
    trap 'rm -rf "$L"' EXIT
    find . > "$L/raw" || { echo "refused: cannot traverse $1" >&2; exit 2; }
    LC_ALL=C sort -o "$L/sorted" "$L/raw" || exit 2
    while IFS= read -r q; do
      m=$(stat -f %Lp "$q") || exit 2
      case $m in ''|*[!0-7]*) echo "refused: unreadable mode for $q" >&2; exit 2 ;; esac
      if [ -L "$q" ]; then t=$(readlink "$q") || exit 2; echo "l $m $q -> $t" || exit 2
      elif [ -d "$q" ]; then
        [ -r "$q" ] && [ -x "$q" ] || { echo "refused: unreadable directory $q" >&2; exit 2; }
        echo "d $m $q" || exit 2
      else
        [ -r "$q" ] || { echo "refused: unreadable $q" >&2; exit 2; }
        h=$(shasum -a 256 < "$q") || exit 2; h=${h%% *}
        case $h in *[!0-9a-f]*) h= ;; esac
        [ ${#h} -eq 64 ] || { echo "refused: hash failed for $q" >&2; exit 2; }
        echo "f $m $h $q" || exit 2
      fi
    done < "$L/sorted" || exit 2
    exit 0 ); }
check() { # check NAME STATUS(0 pass)
  if [ "$2" -eq 0 ]; then echo "PASS $1" >> "$D/gate.txt"; else echo "STOP $1" >> "$D/gate.txt"; G=1; fi; }

case "${1:-}" in
prepare)
  [ "$(cd "$HOME" && pwd -P)" = "$HOME" ] || die "home path is not its real path"
  id -Gn | tr ' ' '\n' | grep -qx admin && die "this user is an administrator"
  [ ! -e "$APPDATA" ] || die "App data already exists"
  [ ! -e "$SHARED" ] && [ ! -e "$HOME/ChiralityV4Fixtures" ] || die "fixtures already exist"
  [ ! -e "$OUT" ] && [ ! -L "$OUT" ] || die "output root $OUT already exists"
  nolink "$(dirname "$OUT")"
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
  nolink "$DMG"; nolink "$APPDATA"
  stage c1; G=0
  { sw_vers; statf "$APPDATA"; } > "$D/system.txt" 2>&1
  shasum -a 256 "$DMG" > "$D/dmg-sha256.txt"
  r=0; grep -q "^$DMG_SHA " "$D/dmg-sha256.txt" || r=1; check dmg-sha256 "$r"
  r=0; xattr -p com.apple.quarantine "$DMG" > "$D/dmg-quarantine.txt" 2>&1 || r=1; check dmg-quarantine "$r"
  xattr -l "$DMG" > "$D/dmg-xattr-l.txt" 2>&1 || true
  r=0; spctl -a -vv -t exec "$MOUNTED" > "$D/mounted-spctl.txt" 2>&1 || r=1; check mounted-gatekeeper "$r"
  xattr -p com.apple.quarantine "$MOUNTED" > "$D/mounted-quarantine.txt" 2>&1 || true
  [ -d "$APP" ] || die "installed App not found at $APP"
  plain_tree "$APP"   # no symlink, special file or odd name anywhere in the App before member reads
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
  shasum -a 256 "$APP/Contents/embedded.provisionprofile" > "$D/installed-profile-sha256.txt" 2>&1 || true
  r=0; grep -q "^$PROFILE_SHA " "$D/installed-profile-sha256.txt" || r=1; check installed-embedded-profile "$r"
  stat -f '%N owner=%Su group=%Sg mode=%Sp' "$APP" > "$D/installed-ownership.txt"
  r=0
  if content "$APP" > "$D/installed-content.txt" 2> "$D/installed-content.err"; then
    h=$(shasum -a 256 < "$D/installed-content.txt"); [ "${h%% *}" = "$CONTENT" ] || r=1
  else r=1; fi
  check installed-content-structure "$r"
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
  for x in "$K" "$APPDATA/capture-seal"; do if [ -e "$x" ] || [ -L "$x" ]; then nolink "$x"; fi; done
  { statf "$K"; statf "$K/continuity.s1.json"; statf "$APPDATA/capture-seal"; } > "$D/marker-stat.txt"
  if [ -f "$K/continuity.s1.json" ] || [ -L "$K/continuity.s1.json" ]; then copyrel "$K/continuity.s1.json"; fi
  [ -e "$APPDATA/records/projects" ] && nolink "$APPDATA/records/projects"
  for p in "$APPDATA"/records/projects/*; do
    [ -d "$p" ] || [ -L "$p" ] || continue
    nolink "$p"; for x in captures acts; do if [ -e "$p/$x" ] || [ -L "$p/$x" ]; then nolink "$p/$x"; fi; done
    for f in "$p"/captures/*.json "$p"/acts/*.jsonl; do
      [ -f "$f" ] || [ -L "$f" ] || continue; copyrel "$f"
    done
  done
  if [ "$1" = c4 ]; then
    if [ -f "$APPDATA/desktop-startup/request.json" ]; then copyrel "$APPDATA/desktop-startup/request.json"; fi
    [ -e "$APPDATA/runtime/distribution" ] && nolink "$APPDATA/runtime/distribution"
    for s in "$APPDATA"/runtime/distribution/s1-*; do
      [ -d "$s" ] || [ -L "$s" ] || continue; copytree "$s"
    done
    # Names and metadata only. account-homes is pruned itself, so it is never read.
    (cd "$APPDATA" && find . -path ./account-homes -prune -o -print) > "$D/.meta"
    LC_ALL=C sort -o "$D/.meta" "$D/.meta"
    (cd "$APPDATA" && while IFS= read -r p; do statf "$p"; done < "$D/.meta"; statf ./account-homes) > "$D/appdata-metadata.txt"
    rm "$D/.meta"
    plain_tree "$HOME/ChiralityV4Fixtures"
    content "$HOME/ChiralityV4Fixtures" > "$D/fixture-manifest.txt" || die "fixture manifest failed"
  fi
  manifest ;;
handoff)
  A="${2:-}"; [ -n "$A" ] && id -u "$A" >/dev/null 2>&1 || die "give the receiving account name"
  root_ok
  find "$OUT" -type d -exec chmod +a "user:$A allow list,search,readattr,readextattr,readsecurity" {} +
  find "$OUT" -type f -exec chmod +a "user:$A allow read,readattr,readextattr,readsecurity" {} +
  echo "Granted read access to $A only, on $OUT" ;;
manifest)
  [ -d "${2:-}" ] || die "give an App path"
  nolink "$2"
  T=$(mktemp "${TMPDIR:-/tmp}/witness-manifest-out.XXXXXX")
  content "$2" > "$T" || { rm -f "$T"; die "manifest failed"; }
  h=$(shasum -a 256 < "$T"); rm -f "$T"; echo "${h%% *}" ;;
*) echo "usage: $0 prepare | c1 <dmg> | c2 | c3 | c4 | handoff <account> | manifest <app>" >&2; exit 64 ;;
esac
