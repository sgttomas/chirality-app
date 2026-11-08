# RTD checker source location

The current RTD definition checker is an App tool. Its declarative schemas,
frozen rehearsal data and governing account remain in this deliverable.

| Original location at `109441b501edd86453d263f4207ff6199dbd9a78` | Current operational location |
|---|---|
| `execution/PKG-08/DEL-08-02/Work/prototype/check_rtd.py` | `tools/deliverable_prototypes/DEL-08-02/prototype/check_rtd.py` |

The original script's SHA-256 is `6c8c1f77cd5f29a945dc5990d1a8d7cee2b850e4fbc3efdf7a495eb2bfa8f980`. The relocated script's SHA-256
is `e0a5c5956e00a8e6a827339f9f9b453515818ec37b7baf206612e87774091190`. The only source changes import `Path` and resolve the
repository, Work and EU-D1 input locations from the tool's new directory.
The pin values, fixture construction, checks and refusal rules are unchanged.
`deliverable.yaml` names the current command source, and `prototype/README.md`
gives the repository-root invocation.

Historical references to the original prototype location in
`RESEARCH_TO_DESIGN.md`, the schema description and frozen evidence retain
their original subject. The historical RTD account, supplier selections,
schemas and EU-D1 bytes are unchanged; no pin is refreshed. Running this
checker is a definition rehearsal and establishes no actual Domains input,
human act, qualification or later-increment start.
