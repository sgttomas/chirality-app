# Store P2 physical-containment repair

The initial independent review found that lexical containment allowed two case
spellings of the same physical vendor directory. Store::open then created
runtime/distribution in the measured vendor tree and returned success. The manager
preserves the original independent failed test/log in reviews/store_initial;
STORE_FREEZE.json remains the original reviewed candidate, not this repair.

The repair compares device/inode identities of no-follow-opened ancestor chains
for vendor and prospective publication root. It rejects vendor containment even
when the new root suffix does not exist, and reverse containment when the root
already exists. This precedes both mkdir operations, with named descriptor
association checks, and is repeated on every read/publication guard. It does
not authorize symlink traversal through canonicalization or lowercase strings.

The macOS regression asserts a genuine filesystem alias, then tests equal and
ancestor vendor aliases and proves runtime was not created. Reverse containment
is checked with a case-alias publication ancestor. An at-use vendor replacement
by a symlink refuses both read and new publication without changing the stored
publication count. These address the original failure rather than merely rerun
unchanged positive tests. Same-user concurrent relocation remains bounded by
descriptor/name observations, not an atomic filesystem or execution snapshot.

Main 5d562a1f11 was integrated nonrewriting before repair checks; it adds disjoint
examination/Design/records from the previous 412cf7fa01 basis. Only the store
source and its maintained explanation changed for this repair. Original label
and first-store evidence remain intact. Full selected closure/S1 and other
implementation residuals in STORE_REVIEW.md remain open. No commit or supplier
qualification is implied by this repair packet.
