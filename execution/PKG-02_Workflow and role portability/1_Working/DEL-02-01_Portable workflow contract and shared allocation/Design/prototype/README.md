# DEL-02-01 design prototype — declared-part carriage and reading

**This is not product code.** It is a design aid under R12-3 of run
`APP-V4-DESIGN-PASS-2-20260930`: a small script that renders, parses and
validates the declared part of a portable workflow as WD-v0.8 proposes it. It
chooses no library, local implementation or service for the reader (R12-2;
OI-014 stays open), and passing it establishes no consumer, host or
qualification.

## What it shows

1. **Carriage (WD §3.5).** A workflow's declared part can be carried in
   `WORKFLOW.md` as one fenced block with the info string
   `workflow-declaration`, holding JSON, and be extracted and parsed with a
   language's standard library alone. `extract.mjs` is an independent second
   extractor in node; both give the same canonical JSON for E1.
2. **Schema (WD §3.6).** `../workflow-declaration.schema.json` (JSON Schema
   2020-12) accepts `../workflow-declaration.valid.example.json` (E1) and the
   E1b, E1d and E1e fixtures, and rejects
   `../workflow-declaration.invalid.example.json` with nine named errors.
3. **Reading order (WD §3.7).** The reader classifies each element as
   recognized, invalid or not established, in the order VO-1…VO-10, with the
   FB codes of WD §11, for E1, E1d, E1e, the real Root packages E5
   (`workflows/create-workflow`) and E6 (`workflows/project-dag`), and 32
   variants (WD-EX E9).
4. **Examples agree with fixtures.** The E1 and E1d `WORKFLOW.md` renderings in
   `../EXAMPLES.md` are byte-identical to what `render` produces, and its E1b
   and E1e JSON equals the fixtures.
5. **Workflow identity (WD §6.1, §3.6; RP-3 repair).** The schema's
   `$defs/workflow_identity` accepts the three valid instances of
   `fixtures/workflow-identity.examples.json` and rejects each invalid one
   with its one named error (origin `host-supplied`; derived-from as a
   string; no source root) (S-10).
6. **Name-to-group mapping (WD §4.2.5 HC-7; R14-5; RP-3 repair).** Each of
   the ten harness capability names resolves to one HOSTING §8.4 Part A
   group, and every supplier name a row cites that HOSTING places in a group
   is a member of that group (S-11). The check reads DEL-01-01's
   `HOSTING_BOUNDARY.md` from the working tree, read only.
7. **Revision file set (WD §6.1 RV-1…RV-5).** The file set and
   canonicalization give a stable value, change with any byte, and refuse a
   symbolic link. CC-CONTENT-IDENTITY selects the bounded App
   package method `chirality.app.workflow-package.sha256/v1`; historical
   proto-sha256-list-0 values are not silently upgraded. Run
   `python3 content_identity_cases.py` for framing/byte/path and refusal checks.

It does not show a run: no checkpoint arrival, act, disposition or harness
capability presence is evaluated (those need EXEC's and LOOP's test doubles).

## Files

| File | Role |
|---|---|
| `wdproto.py` | Validator (JSON Schema subset), extractor, renderer, reader, selected App package method, self-test |
| `extract.mjs` | Second, independent extractor (node standard library) |
| `fixtures/E1.prose.md`, `E1d.prose.md`, `E1e.prose.md` | Front matter and prose of the fixture packages (the declared part is appended by `render`) |
| `fixtures/E1b.declaration.json`, `E1d.declaration.json`, `E1e.declaration.json` | Declared parts (E1's is `../workflow-declaration.valid.example.json`) |
| `fixtures/workflow-identity.examples.json` | Valid and invalid instances of `$defs/workflow_identity` (RP-3 repair) |

## JSON Schema subset validated

`type`, `enum`, `const`, `pattern`, `minLength`, `maxLength`, `minItems`,
`uniqueItems`, `required`, `properties`, `additionalProperties` (false only),
`items`, local `$ref`, `allOf`, `anyOf`, `not`, `if`/`then`. Annotation
keywords are ignored. Any other keyword stops the validator with an error, so
the schema cannot silently use a keyword the prototype does not check.

## Running

```
python3 wdproto.py selftest          # all checks; exit status 1 on any failure
python3 wdproto.py read <package>    # the reading of one package, as JSON
python3 wdproto.py render <decl.json> <prose.md> <out-dir>
```

Python 3 standard library; `node` is used by check S-9 when present. No
package is installed and nothing is fetched. The self-test writes only to a
temporary directory it removes. Set `PYTHONDONTWRITEBYTECODE=1` to avoid a
`__pycache__` folder. The command, date and output of each recorded run are
in `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/B1.md`
(54 checks) and, after the RP-3 repair (outcome token `applied`, file
outputs need a path, the identity definition, the group mapping), in
`WAVE_B/RP-3.md` (62 checks).
