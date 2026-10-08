# B3 F1 import isolation repair

Candidate `6acb23613a905ebd1e0339345f7a49eaf6071e44` replaces the new generic Python module names with `admission_check` and `admission_rules`. Existing Group B modules and tests are unchanged. The added regression imports B1 and B3 in both orders in fresh interpreters.

Exact combined Group B discovery passes all **51 tests**. Invented review and change joins also pass at this candidate using the renamed CLI. The attached hashes bind inputs, code and outputs; original evidence remains historical. This is offline file-check support only, with no route admission, actual reviewer observation or qualification claim. CI26 remains pending.
