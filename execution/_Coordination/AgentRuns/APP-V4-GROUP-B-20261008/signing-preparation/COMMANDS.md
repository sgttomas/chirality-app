# Actual read-only check operations

A one-time Python driver used existing maintained/prototype functions; no new
framework or reusable tool was created. Inputs are fixed by AUTHOR_BASIS.json.
The local paths were supplied by the parent and resolved directly. No network
or host names are in the evidence.

1. Import unchanged `Design/prototype/read_tree.py` and `check_pkg.py` with
   bytecode generation disabled; read retained B2 bundle using
   `read_tree.read(bundle, True)`. Compare every returned entry with prior
   BUNDLE_INVENTORY.json; recompute `read_tree.manifest` and P0 SHA-256.
2. Read approved cached development vendor and actual packaged P1 with the
   same function; run `read_tree.compare(packaged, selected)`. Compare root
   directory modes separately. Invoke `check_pkg.fp0(vendor)` and retain all
   seven returned RESULTS and selected tree entries in FP0_CACHED_VENDOR.json.
3. The existing read-tree functions invoke only read-only Apple commands:
   `/usr/bin/codesign -dv --verbose=2 <each Mach-O>` and
   `/usr/bin/codesign -d --entitlements - --xml <each Mach-O>`.
   No `--sign`, `--verify`, keychain, identity-list, notary or supplier command
   was executed. Signature metadata observation is not cryptographic verification.
4. Compare actual P2/P3 with current exact source bytes through read_tree.compare;
   verify every current canonical reader pin with SHA-256. Run
   `git diff --name-only f79317be861bb63553512de3197b22d556268198
   5d562a1f11bdad3f6794f6ff4ca25e665e9f5e06 -- app/src-tauri app/src`
   with project-prefixed paths, then hash each old/new Git blob.
5. Verify exact canonical OpenAI terms path absent, write supplied unresolved
   record, check unchanged schema through Draft202012Validator and unchanged
   `check_pkg.terms_violations(record)`. Both produced no errors.
6. Reread full retained bundle and assert it equals the initial inventory;
   no artifact writes were performed. Results are in ARTIFACT_RECHECK.json.

Source/version inspection used Git read operations and local text reads only.
Staged private-term validation is required before the preparation commit; machine
terms are held in the environment and never printed. No push is performed here.
