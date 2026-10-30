#!/bin/sh
# OBS-1 download watch (S-2). Prototype only; DEL-01-01, run APP-V4-DESIGN-PASS-2-20260930.
# Every second: any `lms get` process; the LM Studio models-folder listing (depth 2)
# against a baseline file; the non-loopback IP sockets of LM Studio's processes
# (numeric only: no name lookups, so the watch itself makes no network traffic).
# A `lms get` process or a new model folder is written as an "S-2" line.
# Non-loopback sockets are written as "NET" lines for review (IPs are not
# resolved; a download also shows as a new model folder).
# Usage: download_watch.sh OUT STOPFILE BASELINE
OUT="$1"; STOPFILE="$2"; BASE="$3"
while [ ! -f "$STOPFILE" ]; do
  ts=$(python3 -c 'import time;print(int(time.time()*1000))')
  g=$(ps -axo pid,command | grep -E 'lms get|lms-get| get --yes' | grep -v grep)
  now=$(cd "$HOME/.lmstudio/models" && find . -maxdepth 2 -mindepth 2 | sort)
  newdirs=$(printf '%s\n' "$now" | comm -13 "$BASE" -)
  pids=$(pgrep -f 'LM Studio|\.lmstudio' | paste -sd, -)
  net=""
  if [ -n "$pids" ]; then
    net=$(lsof -nP -a -i -p "$pids" 2>/dev/null | awk 'NR>1' | grep -vE '127\.0\.0\.1|\[::1\]|localhost|\*:' )
  fi
  if [ -n "$g$newdirs" ]; then
    echo "$ts S-2 lmsget=[$g] newdirs=[$newdirs]" >> "$OUT"
  fi
  if [ -n "$net" ]; then
    printf '%s NET %s\n' "$ts" "$(printf '%s' "$net" | tr '\n' '|')" >> "$OUT"
  fi
  [ -z "$g$newdirs$net" ] && echo "$ts ok" >> "$OUT"
  sleep 1
done
