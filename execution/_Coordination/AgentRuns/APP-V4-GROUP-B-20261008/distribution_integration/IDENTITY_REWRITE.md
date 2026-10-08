# Owner-directed feature-branch identity rewrite — 2026-10-08

The owner explicitly authorized re-authoring this unmerged feature branch and
pushing with `--force-with-lease`. Author and committer are now Ryan C Tufts
<ryan@chirality.ai>. Main and other-owned branches were not rewritten.

The pre-rewrite head was `87e2faab6891afae8770f10846c8a4d84cfc435b`, tree
`4caaac661d529a92f4d7233e24e753a9bfa2fafa`. Fetch found main advanced from
`99ca5d6fe6b1c0e4ff15e09f070cdd646df31114` to
`b21685c0374dc05c4eff090e71d7914d757754cb` (PR #1120 privacy cleanup).
The rewrite replayed this feature onto that current main. Its resulting head,
before this mapping note, is `553c442dbf2729f488173feb13c3a32575d953ea`, tree
`239a51ba05d408563fee36902fc1b4077d327229`. The entire binary feature diff
against respective bases was byte-identical (SHA-256
`8f6bb910031408f64609a8a8664946039caeeca815ac2b4a69871c8aaf83eaf3`).
The only replay conflict was Group B's graph; the already reviewed B3 and A-IN
rows/sections were preserved exactly. No product or evidence bytes changed
through re-authoring; this authorized mapping note is the sole follow-up content.

All pre-rewrite commit identifiers retained in existing proposal, run, check
and review records are historical observations of their named candidates, not
claims about the current branch head. Existing exact-head reviews stay scoped
to those historical heads. Use this map to locate the equivalent replayed
contributions in the current branch; final new-head review and CI are required.

| Historical feature commit | Current re-authored contribution |
|---|---|
| `bcfc31cceee926a4b32d28e59133e6c5e4e5ef03` | `b0e0b443ee8272c63aa0e264f89330bc12d800ae` |
| `2e4c9ff9cf5cee669a4762f6c72a7837926d4733` | `f34f560240a6e6e20707d688011defd40a659aec` |
| `4c5f691c82d887d943849bf15a5efb9a99eec455` | `fc5e9135a7f59c566fc20fbbb102d8d1ef07c860` |
| `2138ce0b4e59a176e9ad767555d9289cae06ee92` | `e39d5162a446bb08c061fe672454664cbba2178d` |
| `cdcba57f59a6948ec1ee516ffca022c3fa86fca3` | `8b8abcb3da16c33ae31630d8f37ed94ca1587e81` |
| `a4f1d49fb76684835082ebae3b6c20691500d2b4` | `0db4be64ddac534c24e7e73801adfcc2768c0a69` |
| `e3800f0e859743de37c44372fd92352bbce3b13c` | `d8f6ec059bb40b54229d07b5cd433cca83511577` |
| `5a50030fd3faa6efe526ced7a3f8c901032259ef` | `5718ef2348692f5e2e38bf8a93693dfd64061595` |
| `3ce2493a419469d0cb5c97ddf2cf6c5ea5e3d15a` | `b14ee78bc901ad056d6fdbcac1f3d5eaeb3ddca0` |
| `87e2faab6891afae8770f10846c8a4d84cfc435b` | `553c442dbf2729f488173feb13c3a32575d953ea` |

Original child author commits cited by run returns remain historical provenance;
the map names their integrated contributions where those were cherry-picked.
The original review-only author commit `2212ed9c851bc925573271379797b65bf01cd997`
was independently re-authored by its owner as `019c32fa` with identical tree,
as relayed by HELP_HUMAN. This branch carries the same review file in the mapped
successor of `3ce2493a41`; neither rewrite gives that review a new candidate scope.

The official `tools/validation/validate_private_terms.py` was absent from the
fetched main. Read-only fallback scanning obtains machine identifiers at runtime
without recording or printing their values; uses `<host>` for any placeholder;
and checks changed content and branch commit messages before commit/push.
No credentials, user configuration, supplier/native execution, memory writes,
qualification or owner acceptance is implied by this identity maintenance.
