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
whether a change is acceptable. The overall status is `unchanged`, exit 0, only
when nothing at all differs. Any changed, removed or added entry in any root,
the application bundle included, and any root that appeared or disappeared,
gives `differences found` and exit 1. A refusal exits 2.

`record` writes the record's content and then, last, a completion marker that binds
the SHA-256 of that content. The marker detects a record that was truncated, or edited
without recomputing the marker. It is not authentication, and it does not protect
against someone deliberately writing a consistent record. `compare` validates both records strictly before
comparing: the format, a non-empty list of roots, each root's class and state,
each entry's path, kind and mode, and each file's size and digest. Entries must
be in order with their parent directories recorded, and the content must match
its marker. A record that fails, was not completed, or that a successful
observation could not have produced is refused (exit 2). Two records over
different roots are refused too.

The private record (mode 0600) keeps paths and link targets. The shareable
summaries keep only counts, classes and digests, because names can carry
content. No record holds file content. The tool never follows a link, never
reads a socket or special file, never reads a keychain and never touches or
launches an application. It refuses a link in a root's ancestry, an existing
output or one inside a root, an unreadable entry, data that changes while being
read and a name with a line break.

Paths with a NUL or other control character, a root path that is not in normal
form, a mode beyond the permission bits, a zero-byte file whose digest is not that
of the empty input (or a non-empty file with that digest), and fields that do not
match an entry's kind are all refused as values a successful record could not hold.

## Limits

These are operator-run checks on stable inputs. They are built so that an
observation that was not made, that failed, or that is incomplete cannot come out
as success, and so that drift and mistakes are caught. They are not built to
withstand a writer changing the inputs during the run, nor someone with write
access forging a record: a completion marker is not authentication.

Its tests run on invented trees only. Whether a person can go back to v3.0.1 by
reinstalling it is a question the two records help answer; this tool does not
try to answer it.
