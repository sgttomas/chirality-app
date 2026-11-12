# Retained terms position

The held record of the supplier's position on distributing the App with its
current sign-in flow, which DEL-01-06 REQ-004 requires before public release.
Five files, kept byte for byte as they were recorded:

| File | What it is |
|---|---|
| `execution/PKG-01/DEL-01-06/Work/terms-position-v1/OpenAI.json` | The terms-position record: its scope, conditions, exclusions and the distribution decision, which reads `not_made` |
| `execution/PKG-01/DEL-01-06/Work/openai-app-server-publication-20261030.json` | The supplier's publication as captured, with its source, retrieval time and exact excerpts |
| `execution/PKG-01/DEL-01-06/Work/terms-position-v1/owner-disposition.json` | The disposition the owner approved, with its clauses |
| `execution/PKG-01/DEL-01-06/Work/terms-position-v1/owner-answer.json` | The owner's question and answer as captured |
| `execution/PKG-01/DEL-01-06/Work/terms-position-v1/approved-proposal.md` | The exact text the owner approved |

The files name one another by path and hash inside their own bytes, so they
keep the relative paths they were recorded under, beneath this folder as the
evidence root. Moving or editing one makes the reader refuse the set. Two of
them carry a local scratch path from the machine they were captured on; it is
part of the hashed bytes and is left as it is.

To check the set, from the repository root:

```sh
python3 app/packaging/terms/check.py \
  --record execution/PKG-01/DEL-01-06/Work/terms-position-v1/OpenAI.json \
  --evidence-root "$(pwd -P)/app/packaging/terms/retained"
```

The reader checks that the retained bytes agree with one another. It gives no
legal judgment and no release authority. Whether the position applies to the
offering and sign-in flow of a candidate is the owner's statement, read
against that candidate (DEL-01-06 AC-004).
