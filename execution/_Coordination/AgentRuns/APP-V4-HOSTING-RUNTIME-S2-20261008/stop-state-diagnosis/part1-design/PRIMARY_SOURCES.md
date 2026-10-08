# Process-group source lookup limits

HELP_HUMAN supplied POSIX group lifetime/reuse basis at https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap03.html and https://pubs.opengroup.org/onlinepubs/009696699/basedefs/xbd_chap04.html . Manager browser fetches returned403; these are parent-reported sources, not manager-retrieved proof.

Manager retrieved Apple archived killpg manual https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/killpg.2.html : it specifies signalling the group identified numerically and permission/error behavior. It does not supply a persistent original-group capability. This archive is not a proof that the proposed wait/reap protocol works on the current host.

Parent requires source-backed current-group ownership before post-reap signalling; a cached PID/PGID, past H5 or later successful numeric probe is insufficient. No source proof is claimed yet.
