# Source-bound N-1 blank forms

Implementation `5410dee2fcb9ff9b33032e25949bd60009b545fa` consumes the actual maintained B7 preparation API and produces all three SQ blank forms. Their actual file consumer checks pass. All59 combined Group B tests pass, including eight new tests and wrong source/case/order/candidate/observation controls.

The header and close fields follow EXP §8.2. Observation rows remain empty; expected guidance is separate. No native run, record, examination or human act occurred. Candidate remains unassigned, and CI26 remains pending. Existing canonical Designs and consumer locks are unchanged. Separate review is required before integration.
