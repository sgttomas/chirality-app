# Prior-version data, before and after (DEL-01-06 AC-009, VER-008)

4.0.0 replaces v3.0.1 under one bundle identifier, `com.chirality.app`. Its package
installs `Chirality.app` in v3.0.1's place in the Applications folder and starts
with whatever v3.0.1 and macOS left under that identity. Nothing imports, resets
or reseals that data. `inventory.py` lets an examiner see, per root and per
entry, what installing, launching and running the package left, changed, added
or removed.

## Roots

`python3 app/packaging/prior_data/inventory.py roots` prints the default set for
the operator to confirm. It composes paths and reads none of them:

| Class | Root | Why |
| --- | --- | --- |
| `prior-data` | `~/Library/Application Support/Chirality` | v3.0.1's own data folder (`runtime/packages/cli/src/config.ts` at tag `v3.0.1`) |
| `prior-data` | `~/Library/Logs/Chirality` | v3.0.1's logs folder |
| `prior-data` | `~/Library/LaunchAgents/com.chirality.runtime.plist` | v3.0.1's runtime LaunchAgent |
| `current-data` | `~/Library/Application Support/com.chirality.app` | 4.0.0's own data folder |
| `system-per-identifier` | `~/Library/Preferences/com.chirality.app.plist`, `Saved Application State/com.chirality.app.savedState`, `Caches/com.chirality.app`, `HTTPStorages/com.chirality.app`, `WebKit/com.chirality.app` | kept by macOS per bundle identifier, so shared by both versions |
| `application-bundle` | `/Applications/Chirality.app` | the installed application; its replacement is expected and reported as such |

An absent root is recorded as absent, so a root created later reads as created.

## Use

```sh
inventory.py record --root PRIOR --current-root CURRENT --system-root SYS ... --bundle-root APP \
  --out NEW-PRIVATE-RECORD --summary NEW-SHAREABLE-SUMMARY
# install, launch and run the package
inventory.py record ...same roots... --out NEW-PRIVATE-RECORD-2 --summary NEW-SHAREABLE-SUMMARY-2
inventory.py compare RECORD RECORD-2 --report NEW-PRIVATE-REPORT
```

`compare` groups its findings by root, with each root's class, whether it was
absent before, and the counts of unchanged, changed, removed and added entries.
The private report lists the entries and what differs in each. A changed file
under a system-per-identifier root, an untouched prior-data folder and a folder
4.0.0 created stay three separate findings. The tool decides nothing about
whether a change is acceptable. It exits 1 when any recorded entry in any root
is missing or differs, the application bundle included, and 0 otherwise; 2 is a
refusal.

The private record (mode 0600) keeps paths and link targets. The shareable
summaries keep only counts, classes and digests, because names can carry
content. No record holds file content. The tool never follows a link, never
reads a socket or special file, never reads a keychain and never touches or
launches an application. It refuses a link in a root's ancestry, an existing
output or one inside a root, an unreadable entry, data that changes while being
read and a name with a line break.

Its tests run on invented trees only. Whether a person can go back to v3.0.1 by
reinstalling it is a question the two records help answer; this tool does not
try to answer it.
