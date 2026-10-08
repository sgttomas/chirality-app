# Independent committed-source export verification

READY for Group B receiving review of /private/tmp/lt12-committed-exports-achyuhbn, source 938d20ef4bf0d07a7cc706d575e74f844d8caccf. Reused the exact committed-source implementation review. No rebuild or producer rerun was performed.

Independently verified both receipt hashes: LT09 739c05d3bc96128cdde6964279dbb258ae5e89abae0d3d16516a9184834ad956; terminal e3580b2acf79897a8416895bff4013189936d61e6eeab14a2cdf8a66126c2cd7. Passively hashed the supplied executable: 69d418bb91d6734f3da46812982e6a858369839aeed4532ff86299038abb8bea, matching both receipts and all four producer records. Actual recorded argv/features agree. Rehashed all 114 SOURCE_MEMBERS entries against exact Git commit bytes. Build log records compilation from manager checkout; each explicit unchanged exporter log records one pass. Clean-before/after and execution ordering remain supplied manager provenance, not cryptographically authenticated history.

All 93 raw output files match receipt membership, digests and sizes; file symlinks and undeclared files were absent. Checked actual event/envelope equality, successful read state and H5 equality across event, reference, observation and verification envelope. Terminal pairs have LT09 then LT23 with increasing sequence and unchanged raw observation/reference; unselected source is null with no directory. No LT12 event is exported. The unchanged producer implementations and prior independent review supply the remaining closed-format/live-capability checks; this is bounded exported-byte verification, not a new semantic reader.

Exact exchange SHA-256:

- LT09 selected: e5bea1191123a34aaadaa185ebb75bfb9fc430a767a02baa0ba0a982089ae15f.
- LT09 unselected: e39c2e9046ae7134d5da67e233e52a0941c48e3aaaef0e0e8090c870abe7ff8f.
- Terminal selected: 0f4fceb10409d01ea17f37cec84b0ff7684b279e3eeaf283519617b9b941329c.
- Terminal unselected: 8318a49275a2e0859c91196d4539ac2d3ddcae90e6a60b02fb6b140fb3e1e37d.

Producer source now supports LT12, but these cohorts remain standalone LT09 and LT09+LT23 only. Source adoption must preserve those row/format boundaries. Serialized references do not restore native capabilities; same-H5 correspondence does not establish current integrity, descendant certainty, installed custody, authenticated App/build identity, S3, SEAL-2 or qualification. No source changes, native App/supplier actions or downloads occurred in this verification. B owns independent named adoption and final joined validation.
