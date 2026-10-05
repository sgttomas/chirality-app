# Independent attachment producer review — 2026-10-05

**NOT READY: ATT-P1 is one blocking P2 robustness defect.** No additional major/minor semantic finding in exact-byte text framing, identities, canonical validation or immutable ordered preparation. This review covers producer only, not transport/persistence/UI/native supplier qualification.

TASK `/root/group_a_execution/hosting_contract_review`, parent `/root/group_a_execution`; no delegation. Software-code-review applied. Only this report written. Read Root/TASK/project/skill basis already recorded in preceding reviews, joined V0-ATTACHMENT-CORRELATION-R1 and its NIR/HOST meaning, exact producer/tests/assets. Parent authorized one exact-function rustc/owned FIFO scratch check with external timeout. No Cargo, product/Design/schema/Git/auth/native/model/network mutation or execution.

## Exact frozen source

| Subject | SHA-256 |
| --- | --- |
| attachments.rs | `7b68e9c9b1415a4501942a74ad947f2f521ec5205e788a75b6c4f3895afbdbaa` |
| tests/attachments.rs | `15715daba6894cdbab7f24cbcc519dafee1376016efdcc445b43c27eae55386e` |
| changes/I1-ATTACHMENT-PRODUCER.md | `08b80a0f3d850898e1eca957ed9afed8549da93396837ae6c36ec8472cdabce3` |
| accepted joined review | `406a13e04ffacb97d8e9f6051a7c426f3f91008e9a1c698614bce0ea921d513d` |
| embedded canonical supply schema | `6562b8efacb75a3814f59b5918cdac9210e968f008059544864fa234e550a8c1` |

First three seals independently computed; embedded schema/source identity is the exact declared canonical origin and full bytes examined. No moving integration source is included in this verdict.

## ATT-P1 — special source can block instead of returning a hold

**Blocking P2 robustness.** `read_snapshot` (attachments.rs:113–134) opens the native path with blocking `std::fs::File::open` then blocking `take(bound+1).read_to_end`, without guarding non-file sources through a safely opened actual descriptor. `from_native_selection` and `prepare_for_source` both reach it. An absolute Unicode `source.md` FIFO with no writer passes the path/name checks and blocks opening indefinitely. A regular selected file replaced by a FIFO before preparation triggers the same issue. The inclusive byte limit bounds allocation/read count, not waiting time; ordered preparation can consequently stall instead of returning the promised visible hold/no returned partial list. A directory negative does not cover this source type.

Actual independent reproduction: exact unchanged read_snapshot function bytes SHA `feedb96324d4417e1812ac9ab736f33b663ed53d81cc0f4887a3485a15dd454a` copied from frozen source into a rustc scratch executable. Minimal identity/hold type stubs are outside the copied function; they do not alter File::open/read and are not reached before the blocking operation. Under an owned physical temporary directory, create FIFO with no writer and invoke the helper with that path. rustc exit0; process prints entry, **does not return within 2 seconds**, external timeout kills/reaps it (exit -9). Same copied helper on an actual regular text file returns exit0. All owned scratch files removed. No full product/supplier test or arbitrary system path was used, and no Cargo slot retained.

Repair direction: fail visibly for unsuitable file sources without a blocking special-file open/read, including replacement between selection and preparation. Bind suitability checks to the actual descriptor read; a pre-open pathname metadata check alone leaves a replacement race. Preserve lossless selected path, same-buffer hash/decode, ordinary regular-file behavior and current hold semantics. This is deterministic file IO suitability, not a new project-root authority gate, new schema/store/carrier fallback or permission decision. Add initial FIFO and regular-file→FIFO replacement negatives with bounded execution, plus actual regular-file control; same-reviewer exact successor backcheck required.

## Other source assessment

Native path identity is lossless tagged platform data and separate from display. Private non-deserializable selections retain the original PathBuf and identity; exact tagged claim comparison rejects a foreign path even with equal bytes, and display-string reconstruction is refused. Absolute/supplier-representable Unicode path checks precede file IO; invalid-byte Unix name is retained in the hold's lossless identity without lossy dispatch. This producer does not prove native picker origin merely because the constructor accepts PathBuf; actual native picker/IPC adoption remains the next owner's boundary.

Each observation reads one bounded buffer; identity, byteLength and strict UTF8 text derive from those same bytes. Selection/submission identity comparison holds drift/missing source; no stale-content substitution. NUL/nonUTF8 and over262144 bytes refuse text, bound is inclusive and wrapper overhead separate. BOM/CRLF/whitespace/final newline and empty-file bytes survive. Naming path/display controls are JSON quoted, file body untouched, complete element hash names its actual UTF8 representation; native input is exact text/type/text_elements only. Image suffixes return an existing-carrier hold rather than silently becoming text. No provider/supplier read/adoption inference or native future turn ID is introduced.

SupplyValidator uses full embedded canonical schema via existing failclosed offline declared-ID compilation; complete generated records pass it, not a subset substitute. App exact-byte method and element identity designate their actual hashes. `supplyStanding: supplied` is carrier meaning only; PreparedAttachmentList explicitly says prepared/not persisted/not sent. Same immutable App submission UUID appears in every record, with fresh opaque attachment IDs and ordered source/supply refs. Private records/list cannot be rewritten through cloned JSON getters. Duplicate selection refs reject, and any ordinary failed member returns no partial list. Draft reference belongs to WR and keeps exact not-registered/not-a-run standing; ordinary attachment body supplies no role/workflow guidance or A15 proof.

Author's actual final **13/13** includes eleven producer tests plus two imported schema/clock controls. I inspected their boundary/hash/source/framing/order/schema/native-input assertions; no reviewer full rerun claimed. Initial invalid-byte filename fixture setup EPERM occurred before producer and remains historical. The successor test correctly invokes the pre-IO strict path guard using exact invalid native identity and an actual Unicode regular-file control, without skip/lossy acceptance or claiming invalid-byte file creation succeeded. That repair does not address ATT-P1. Current tests cover directory/missing/drift/nontext, not FIFO/replacement blocking.

Return to original owner for ATT-P1, preserving this original source/repro. Producer remains unwired; complete-list durable record-before-pipe/client association, cancellation/full-generation/source-pipe barrier, cold resolver/unknown-no-resend, native picker/composer, image/named carriers and actual provider/native witnesses remain specific next production obligations. Their absence is truthfully declared, not an additional producer blocker or permission to send/backfill records. No broader ROLE/WR/HOST qualification or authority expansion follows.
