# Independent standalone LT09 cohort verification

READY for Group B receiving review of the separately named fresh v1 cohort /private/tmp/hosting-terminal-source-lt09-3mh4mkrk. Source revision is 9af67409ed0e625fcd8e0e9a0c59975fccfcae71, whose exporter/source review is reused. No source/build changes or test rerun occurred in this read-only verification.

Verified both exchanges' exact closed v1 top-level shape, producer identity/argv/features against the receipt, actual LT09 row, successful native read projection, full event/envelope equality and generation join. Rehashed every raw publication member and selected-source member, checked exact membership, sizes, duplicate absence and no file symlinks. Selected has 17 publication and 13 source members; unselected has 4 publication members and no selected-source directory. Observed/lifecycle/transport references bind the copied raw bytes. These are standalone LT09 exchanges, not predecessor fields extracted from terminal format and not terminal evidence.

Exact SHA-256 values:

- Selected exchange: 9815b031e0295ca06c145c4ce50a840979dbf8895dfe9165bef36f5caa858552.
- Unselected exchange: 6f7c94c2768d5a3740e7f1f9b716bebc514816fe443dd57c43b0aa07ac0babb5.
- LT09 receipt: 931f688f3c6d9bae2b335ea118f6c5cb9196e474c97ca998f10d6bc30d7478e1.
- Supplied executable, passively hashed: c568f53b288c142e444f936296cee1d29477f83f0ce19b2cc2c5506139bfca58.
- LT09 execution log: 3b03f77c9a9d53d5cc4a8d4b4e4576845601bc8d9fbbe649c95acf829aed51d8; records one explicit exporter test passed.
- Original terminal receipt: 4ad0581d411bf5414c5dfc70219a185f770086a9f0d378f7835d3a1f059653a5, byte-identical to the manager-retained COMMITTED_EXPORT.json. Its original selected/unselected exchange hashes still match their files.

The supplied executable digest agrees across both receipts. Manager's clean detached-source execution/no-intervening-build statement is supplied execution provenance, not cryptographic authentication inferred from exported JSON. The original v1 exporter is unchanged at the reviewed source. No historical pin or fixture was edited by this verification. Group B owns the separate named fixed selection and independent consumer/adoption checks; no fallback or bare repinning is authorized by this report.

This establishes bounded synthetic file correspondence only. It does not authenticate application identity, native custody, installed integrity, terminal behavior, qualification, S3 or release. Terminal-format receipt and evidence remain separate and unchanged.
