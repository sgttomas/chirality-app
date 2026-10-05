# Transport, steering and trace candidate validation

2026-10-05. HELP_HUMAN `/root` checked committed source
`14849f34651178c1493350dc7a21c598d58d7beb` from a complete v4 Git archive.
The 33-path slice contains attachment custody/transport, native text steering,
and examination-account import. Project-context definitions/CI-13 and held
workflow parser work are excluded.

## Actual execution

- `cargo test --offline --locked`: exit 0; 312 passed, zero failed, two ignored.
  The nonreader helper is marked ignored for ordinary discovery but is invoked
  by the supervised regression. The authenticated live-model smoke remained
  intentionally unrun. Stock Codex 0.160.0's offline scratch-home handshake ran.
- `npm test`: exit 0; three passed, zero failed or skipped, including the stock
  handshake and canonical Design schema checks of actual Rust output.
- `npm run build`: exit 0, TypeScript and Vite.
- `python3 schemas/sync.py`: exit 0; six resources match source bytes, hashes
  and declared IDs.

The approved isolated Cargo cache and already prepared node_modules were used;
no dependency download, credential use or model turn occurred. The actual archive
and raw logs remain at
`/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-v4-candidate-2xez174a`.
Comparison of every archived regular source file against the original tar after
checks found no modified tracked bytes. These are parent integration checks,
separate from the independent reviews and their attributed execution.

## Independent review and source binding

- `reviews/V2-ATTACHMENT-TRANSPORT-R3.md`: exact final Host/custody READY;
  retains the five original findings and both subsequent private-state repairs.
- `reviews/V3-I1-STEERING-INTEGRATION.md`: steering consumer READY.
- `reviews/V1-I5-TRACE-RECEIVING.md` and
  `reviews/V2-I5-TRACE-INTEGRATION.md`: receiver and shared consumer READY.
  The latter's exact inverse-delta comparison preserves the reviewed steering
  bytes outside the import addition.

The committed Host, custody, shared lib/runtime/UI and receiver hashes match
those reviewed final sources. The combined archive checks above cover the
final Host with both consumers; old passing checks are not substituted for
the original failing cases or the repaired candidate.

Origin/main advanced to `f506f3e2de` with 6,613 changed paths, all within
`projects/chirality-piping`. No App, Root governance, workflow, skill or CI path
changed. Its local integration commit is
`d9caf5c38ad4db7a10d289056c96ff32856bb53b`. Both source and integration commit
have identical App v4 tree `411792cf6415090565b63f8d9cc117d79141a11e`;
the PR diff still contains only the 33 App paths before this validation note.

Native picker/UI and live steering/attachment witnesses, project/run context,
cold native provenance, broader provider/host qualification and the remainder
of Group A remain unfinished. This slice is neither 90% acceptance nor release.
The PR record carries the final submitted and merge revisions and required CI.
