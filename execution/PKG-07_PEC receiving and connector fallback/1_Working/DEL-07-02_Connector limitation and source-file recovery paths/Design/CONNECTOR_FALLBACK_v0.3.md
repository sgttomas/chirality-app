# Connector fallback CFB-v0.3 — CI-29 successor

Status: PROPOSED source successor, subject to independent review. This named
change consists of CFB-v0.2 `CONNECTOR_FALLBACK.md` at sha256
`69c1f10eb1ed0ecb65dbf75844d3d47daaae0842697f0e41c51b072c41353f16`
plus this amendment. All provisions of that basis remain except the explicit
§4/schema additions below. The historical file and route-account format 0.1
remain unchanged and usable by consumers pinned to them. This is no automatic
consumer adoption, product acceptance or persistence authorization.

## CI-29: wholly unavailable sources

CFB §4 sources are successful reads only. Use route-account format 0.2 and
`connector.route-account.v0.2.schema.json` for this successor. Its schema ID is
`urn:chirality:app-v4:del-07-02:route-account:0.2`. Do not resolve an existing
0.1 reference to these bytes or silently upgrade a stored account.

When no source has been read successfully, `sources` and `facts` are empty,
`conclusions.supported` is empty, `gaps` is nonempty and
`conclusions.unsupported` is nonempty. Gaps identify each missing or unreadable
needed source as far as known, the affected question part/effect and its
responsible party. Unsupported conclusions identify the affected answers;
the account does not claim that the question was answered from source facts.
No path, revision, digest, fact or successful read may be invented to fill a
missing value. A failed attempt belongs in gaps, not sources or facts.

The account still records the same question, trigger, prohibited conclusions,
recorder/time and actual duties. No prepared duty becomes performed. With some
successful reads, only supported parts may have facts/conclusions; other parts
remain gaps and unsupported under CFB §§3–7. Schema validation checks shape,
not truth, completeness, source custody, actor performance or authority.

## Compatibility and point of need

The standing schema, CS-R1–R5, connector-specific derivation, duties and
prohibited conclusions are unchanged. An old format 0.1 account remains 0.1;
old evidence retains its original basis. Consumers must deliberately select
this successor and its schema before emitting/consuming format 0.2. PEC,
Domains, fleet and examination owners receive the impact account in the
Group C C3 treatment; later research-to-design also pins the historical CFB.
No sibling contract is re-pinned by this contribution.

CFB §9's O-D placement question remains open. This definition may be checked
in memory without deciding a user-project target. Persistent account writing
and its placement remain held pending the named placement treatment.

## Maintained source check

Run `python3 check_route_account_v02.py` in this Design directory (installed
jsonschema and referencing required; no downloads). Constructed positive and
negative cases check the 0.2 rule and 0.1 separation. They establish definition
behavior only, not a source recovery, App view, provider witness or duty.
