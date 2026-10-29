# Guarded-bootstrap API basis (2026-10-29)

This is a bounded implementation obstacle, not proof that all Windows bootstrap
designs are impossible. No guard is weakened and no compiler is admitted by it.

## Why the proposed sharing guard is insufficient

Microsoft's [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
`dwShareMode` definition states: "Access requests to attributes or extended
attributes are not affected by this flag." Share modes persist until handle
close and can refuse conflicting preexisting data-write/delete handles, but
that is not a refusal of every preexisting mutation capability.

[MS-FSA 2.1.5.10.37, FSCTL_SET_REPARSE_POINT](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-fsa/4aeefef8-92c3-4abc-af7a-a610caf8a165)
phase 1 specifies:

```
If (Open.GrantedAccess & (FILE_WRITE_DATA | FILE_WRITE_ATTRIBUTES)) == 0,
the operation MUST be failed with STATUS_ACCESS_DENIED.
```

Thus FILE_WRITE_ATTRIBUTES is a documented alternative to FILE_WRITE_DATA for
this access test. Denying FILE_SHARE_WRITE does not establish exclusion of that
capability. An identity/file-ID check also does not detect a future mutation on
the very same object. A later pathname check cannot close that race.

Other phase-1 checks still apply: symlink access, nonempty directories, nonzero
data-file size for symlink tags, valid buffers/tags, volume support and EA state.
This account does **not** assert a demonstrated guest exploit, that every tag
redirects access, or that attribute access alone satisfies every check. It
establishes why sharing alone is no proof of the required no-reparse guarantee.
The public [FSCTL page](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ni-winioctl-fsctl_set_reparse_point)
also states a privilege requirement. No privilege experiment or change is made.
The guarantee is task-namespace redirection, not arbitrary administrator or
same-user memory-writing defense.

The [NtCreateFile](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntcreatefile)
relative RootDirectory/FILE_CREATE route is a promising atomic creation basis.
[OBJ_DONT_REPARSE](https://learn.microsoft.com/en-us/windows/win32/api/ntdef/ns-ntdef-_object_attributes)
can refuse reparses encountered during that individual parse. Neither is a
standing restriction on later compiler pathname opens. A nonempty pinned child
may help stabilize a directory; that does not establish all compiler output and
temporary-leaf states. No unsupported directory-option combination is used here.

The restrictive output variant has a separate, simple conflict: a guard that
omits FILE_SHARE_WRITE refuses a pathname open requesting write/overwrite.
Permitting FILE_SHARE_WRITE lets the compiler write but does not give it unique
writer identity or establish metadata/reparse exclusion. `/noconfig`, explicit
framework references and TEMP/TMP reduce ambient inputs but do not change those
sharing rules. The exact installed csc open/disposition/temp behavior has **not**
been observed or source-verified. No claim is made that it requires replacement.

## Candidate alternative and actual prerequisite question

Roslyn [Compilation.Emit](https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.compilation.emit)
accepts a caller-owned PE stream. This could avoid the compiler's independent
output pathname open while keeping an exclusively owned output HANDLE. It is
not an available implementation merely because the API is documented: exact
installed assemblies/runtime compatibility, metadata/reference loading, all
temporary accesses, output-to-launch identity and lifecycle still need proof.
The authorized execution basis is the installed framework csc, not acquisition
of another compiler. The bounded bootstrap check examines only the two exact
Roslyn assembly names beside that compiler, without a filesystem census.

## Inspection of the actual independent design return

Type2 `codex-hub/gpt-6.1-terra`, xhigh/priority, reviewed input ebf71ce7 read-only.
Its actual return rejected the proposed guard as unestablished, confirmed the
write-sharing conflict, warned that attribute access bypasses sharing, and
distinguished this from universal impossibility. It also flagged unknown csc
temp/replacement behavior and the directory-compatible-options question for
FILE_OPEN_REPARSE_POINT. It proposed caller-stream emission as an alternative
direction, expressly without claiming its prerequisite was available. No guest
contact occurred. The manager retained those qualifications in this account.

The first controller contribution supplied only layouts/imports and a launch
refusal. The manager inspected that actual return and completed a separate
emitted watchdog/creation/cleanup source path locally; the contribution's
refusal was not treated as a supported-API impossibility. Exact executable
review and actual in-memory attempt are recorded separately.
