# Definition supplied to the reader: offer digest `aac-offer-digest/0.1`

Verbatim excerpt of DEL-01-04/AAC-v0.3 `APP_ACT_CONTROL.md` §5.1, lines 240–255, file sha256 45b13f155a0c97949b60e0dfbe0c086fa5c9e9b1afcb0db1ef4f28f82a726057. It is supplied so that a reader can recompute an offer's `offerDigest` from the offer file alone. It is a definition, not a record: it says how the digest is computed, never what happened.

**Offer digest (AAC-v0.3; PROPOSED; from the isolated reader's finding in
run `APP-V4-DESIGN-PASS-4-20261003`, E/RR-E).** `offerDigest` is the sha-256,
in lowercase hex, of the offer **without** its `offerDigest` member,
serialized as UTF-8 JSON as follows:
- object keys sorted by code point;
- no whitespace outside strings (separators `,` and `:`);
- non-ASCII characters written as themselves, not `\u` escapes;
- JSON's own escapes otherwise.

Its method designation is `aac-offer-digest/0.1`. This is the prototype's
`nir_model.canonical()`. It is not claimed to be RFC 8785, and no
equivalence with it was checked. Any reader can recompute
the digest from the offer file alone. Until a canonicalization is selected
for the project (DEL-03-01 TBD-003; RS U-04), this is the AAC's own TEST
VALUE method. The earlier examples' digests stay labelled "illustration" and
are not recomputable.
