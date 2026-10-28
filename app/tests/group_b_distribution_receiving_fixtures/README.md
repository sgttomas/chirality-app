# Synthetic Host exports and invented consumer records

The `selected/` and `unselected/` directories preserve actual cfg(test) Host
exports byte-for-byte. Their producer is the maintained Host fixture using a
synthetic child, its actual LT09 event, publication and live native-held reader.
They are not installed supplier, S3, native App, package or qualification
observations. All raw scratch paths are historical data; receivers must never
dereference them. Export provenance is recorded in `provenance.json`.

`records.py` adapts the existing maintained invented EXP/PKG record fixtures to
`INVENTED-S4-APP-REVISION` / `INVENTED-S4-APP-BUILD`, preserving the required
before/after/rerun distinction and existing gaps. It uses the actual canonical
binding checker. These records describe no real examination, actor review,
change or packaged build, and do not establish that Host used their support
basis. The matching candidate is an explicit test declaration separate from
producer source revision and executable digest.

A replay proves correspondence of these exact exported files and the invented
consumer cohort. It does not authenticate serialized readback history or
restore the live native reference. Regenerate exports only using the named
Host test, retain exact bytes, renew explicit source pins/provenance and rerun
the receiving tests; never silently normalize paths or rehash historical data.
