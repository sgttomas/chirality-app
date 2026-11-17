# Invented examination material.
id: DEL-001-01
name: Packing List
needs:
- from: DEL-001-02
  condition: The menu for the two days is fixed, so that the food crate's mass is known.
  gating: true
- from: DEL-001-03
  condition: The instrument count is fixed, so that the number of spare batteries is known.
  gating: true
  when: Before the battery line is final.
- from: unknown
  condition: The carrier's crate mass limit is confirmed; 25 kg is assumed until it is.
  gating: false
obligations:
- to: DEL-001-04
  direction: downstream
  condition: The packed mass of each crate, for the loading plan.
code_paths: []
