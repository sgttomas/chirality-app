# Review packet — DAG-003 candidate (checkpoint C)

Written before checkpoint 2, as project-dag method Stage 4 step 4 requires
(the predecessor's V12 F2 lesson). It lists the SHA-256 of every file in the
candidate as presented. At publication, `_DAG/DAG-003/` must contain these
files byte for byte (method Stage 5 step 1), verified against this list.

- **Candidate:** `_DAG/_Candidates/DAG-003/`, assembled on the frozen basis
  `8cd783d8d7493fbfe663fb108449e4ceda04a00b` (clean tree); 33 files.
- **Independent review:** not yet performed at the time of writing. A separate
  TASK instance that did not assemble the candidate must review it (method
  Stage 4 step 3) before the package is presented. Its `INDEPENDENT_REVIEW.md`
  is added to the candidate when returned; if any file listed below changes as
  a result, this packet is re-issued with the new hashes and the changed parts
  are re-presented.
- **Strict audit:** `python3 tools/coordination/audit_dag.py --dag-dir
  projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-003 --canonical --strict
  --json-out projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-003/Evidence/dag_audit.json`,
  from the repository root: exit 0 (`Evidence/Tool_Run.json`).
- **Scope of the acceptance:** checkpoints 1 and 2 are decided in one sitting
  (method: a small successor with no SCC ruling needed; only the four held
  arcs are reopened, everything else carries forward from DAG-002). **The
  acceptance record must state that the decision covers both checkpoints.**
- **What acceptance decides:** the departure found by
  `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA002_2026-09-29_2057`: four held
  arcs added (N-18, N-21, N-24, X-1), none removed. It releases DEL-01-04,
  DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03 from `DAG pending`.
- **Not in this candidate yet:** `INDEPENDENT_REVIEW.md` (from the reviewer),
  and the publication-time files `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`
  and `MANIFEST.sha256`.

| File | SHA-256 |
|---|---|
| `ASSEMBLY_RUN.md` | `999b1a92b122962b32ae379515cd350f4e52d13c07af5d045d3f0d4530ab97e8` |
| `CandidateEdges.csv` | `07b969209e2733105b23da7cb1a10df6601f0de42a56b9f286549452fe878269` |
| `DeliverableNodes.csv` | `102eee1a6a409ae4babefa674546c5111848e90ba5fb7447dc5cc240a31b93e8` |
| `DependencyEdges.csv` | `4716ca287d23835cd5ed490e27c4b7e117c89f08ba19b826f489bf7b2be8e359` |
| `Evidence/Accounting.md` | `13b837abe7a791fa8fd2647bf5da2fb05fbf2309bb343eeaab81a0bdfc914413` |
| `Evidence/AssemblyChecks.json` | `c5e8e6fbe50fbbd2f42923e6b9f0d26c64d2e2b803dac50c86cf07949e5923ec` |
| `Evidence/DepartureAccount.csv` | `393427ad92b766d2b04652274b7933848c0c240502e87e9cb1b6b9b5956a714b` |
| `Evidence/DepartureAccount.json` | `3b4748aeed2a4402de1d98ed612094a05134093440afaf957e2208c671b17622` |
| `Evidence/MirrorAssessment.csv` | `b9d92e0c28c889e324b2aeffef329e28037cba95d917fbc4ea48a84b31cf703f` |
| `Evidence/MirrorAssessment.md` | `7ac1e23a2294a7e664054beb7cd7ee5956f6a248425fd17d002037b5a70d7ad2` |
| `Evidence/MirrorComparisons.csv` | `c336574c904e7338a5c7271add8cebd27abbb9c47eb1abce68a46685910b9d56` |
| `Evidence/NonTopologicalInputs.csv` | `b42a85987b254c78e104186c181bc780d09dc5047b53008cacebbf3b5d782bac` |
| `Evidence/RegisterAccounting.csv` | `ee11708391c9186eaa7c5f26734ed6d1f08f0f87dffb14a5ad7dbab47ca797af` |
| `Evidence/SCC_Accounting.json` | `8e030d6222f1319153895322c873bde88755d759cac2f192bcd65cfdbbd8416d` |
| `Evidence/Tool_Run.json` | `118b19be661003e1e13e5c1c7243e10bb89ce41beb6c52f9e7ea2fb0a6088985` |
| `Evidence/admissible_audit.json` | `87685be272c3d36a699aa37affd267bc946d17595728c249f75a1f63f7ef404d` |
| `Evidence/admissible_audit.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `Evidence/admissible_audit.stdout.txt` | `6e3e6d80aca1590ae052bbfe4962a703ccc833e449303443b818efebd806fede` |
| `Evidence/admissible_edges.csv` | `95fffa04335d3aeeaf8943f9ac9a10a6c036d4c16e89e0d5193218793c078c35` |
| `Evidence/all_execution_rows.csv` | `e566d0f519ed250a1232ba8e543912a1629d2b24372610b4fd502bf6838bac30` |
| `Evidence/assemble_graph.py` | `eb14621c4c01716bd0699e92c6e1dfdb8c59d90437dca47968e711b26da3de34` |
| `Evidence/candidate_audit.json` | `14a2fe2a9bac326cff62adc26ec3738135e629504827fef2e387ab2995e732b8` |
| `Evidence/candidate_audit.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `Evidence/candidate_audit.stdout.txt` | `529ccc456c6201b0951e6d37bf52bd569867a09ab0fe3deb877139efd4c00f90` |
| `Evidence/dag_audit.json` | `9318aa6a058b5fc980a8697be35bb57098806936bd620d433fd80f300d905124` |
| `Evidence/dag_audit.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `Evidence/dag_audit.stdout.txt` | `ed8f397b035324276e590ee307572e3f2d7b9931feb932c081910db3bdaa3bef` |
| `Evidence/successor_currency_precheck.json` | `e92ec3dfcba2c6e2f6209764085af5d02c5a80ce440409f4a045b939ee79222d` |
| `ExcludedRows.csv` | `26576f8cfca0c800a41cb02a3c8b4f83dbe92cd6a0f47b976c281426abd01c82` |
| `GRAPH_BASIS.md` | `f61d72993528178a5dd7daa7e3e36f9284221b061c32162efdf8d11883c506ca` |
| `PROPOSED_LATEST.md` | `380f7152adc0e26febbac39ab23b3531c964f31588c0e02f5bc94080bcf34386` |
| `SOURCE_BASIS.json` | `63492ec36b9415d572cd30df69a86af5c0cef8acb5ddc3c31f185654c39d7202` |
| `SOURCE_MANIFEST.sha256` | `d0fc611d95ee80ba64b86ea5b0eaa1a1ba90e85e461fb18459dd8162df6a40c5` |
