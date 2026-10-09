"""Offline CC-REC-GEN encoding checks; no supplier/network/product launch."""
from generation_ref import generation_ref, generation_tuple
from itertools import product

strings = ["s", "a:b", "a/b", "h:n:1", "雪", "é", "e\u0301", "\x00", "😀"]
refs = set()
for session, home, counter in product(strings, strings, [1, 2, 10, 18446744073709551615]):
    ref = generation_ref(session, home, counter)
    assert generation_tuple(ref) == {"appSession": session, "home": home, "spawnCounter": counter}
    assert ref not in refs
    refs.add(ref)
for args in [("", "h", 1), ("s", "", 1), ("s", "h", 0), ("s", "h", -1), ("s", "h", True), ("s", "h", None), ("\ud800", "h", 1)]:
    try: generation_ref(*args)
    except (ValueError, UnicodeError): pass
    else: raise AssertionError(args)
for ref in ["1", "sess-1/H-acct/g1", "gen:v1:s:73:h:68:n:01", "gen:v1:s:7:h:68:n:1", "gen:v1:s:ff:h:68:n:1", "gen:v1:s:73:h:68:n:1\n"]:
    try: generation_tuple(ref)
    except ValueError: pass
    else: raise AssertionError(ref)
print("CC-REC-GEN: %d distinct tuple roundtrips; invalid/noncanonical/absent-spawn cases rejected" % len(refs))
