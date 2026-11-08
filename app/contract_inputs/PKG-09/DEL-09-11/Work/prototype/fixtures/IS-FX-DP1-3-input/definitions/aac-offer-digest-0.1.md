# Definition supplied to the reader: offer digest `aac-offer-digest/0.1`

Verbatim excerpt of DEL-01-04 `APP_ACT_CONTROL.md` §5.1, lines 240–273, file sha256 de39976e93500c9455c000b78363ad192fe56fd8aa87c680284f78db939acf65. It is supplied so that a reader can recompute an offer's `offerDigest` from the offer file alone. It is a definition, not a record: it says how the digest is computed, never what happened.

**Offer digest (AAC-v0.3; PROPOSED; from the isolated reader's finding in
run `APP-V4-DESIGN-PASS-4-20261003`, E/RR-E, and RV E1-R4).** Method
designation `aac-offer-digest/0.1`. `offerDigest` is the sha-256, in
lowercase hex, of the UTF-8 bytes of the offer **without** its `offerDigest`
member, serialized as JSON as follows:

- **Objects.** Members are sorted by key in code-point order. The offer's keys
  are all ASCII schema names, so code-point and UTF-16 order agree.
- **Separators.** `,` and `:`, with no whitespace outside strings. Arrays keep
  their order.
- **Strings.** `"` and `\` are escaped. U+0008, U+0009, U+000A, U+000C and
  U+000D are written as `\b`, `\t`, `\n`, `\f` and `\r`. Other characters
  below U+0020 are written as `\u00xx` with lowercase hex. **Every other
  character is written as itself**, including non-ASCII, U+007F, and U+2028
  and U+2029; none is `\u`-escaped.
- **Numbers.** Only integers occur in an offer (the schema has no
  non-integer number). They are written in decimal, with `-` for a negative
  value and no `+`, leading zeros, fraction or exponent.
- **Literals.** `true`, `false` and `null`.
- **Non-integer numbers.** The method is not defined over a non-integer
  number. An offer containing one is not offered.

This is the prototype's `nir_model.canonical()`. It is not claimed to be RFC
8785, and no equivalence with it was checked. Any reader can recompute the
digest from the offer file alone.

The A16 example carries ü, ≈ and U+2028 in a consequence. The run folder's
`E/run_e.py` recomputes that digest with an implementation written from this
text (not Python's `json`), and gets the same value; it also checks integer
serialization on the A4 example's `arrivalOrdinal`.

Until a canonicalization is selected for the project (DEL-03-01 TBD-003; RS
U-04), this is the AAC's own TEST VALUE method. The earlier examples' digests
stay labelled "illustration" and are not recomputable.
