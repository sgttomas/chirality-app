"""CC-REC-GEN: collision-free reference encoding of HOSTING H5's full tuple.
Prototype only; no generation is created here, only an existing tuple encoded.
"""
import re

_PATTERN = re.compile(r"gen:v1:s:([0-9a-f]+):h:([0-9a-f]+):n:([1-9][0-9]*)\Z")


def generation_ref(app_session, home, spawn_counter):
    if not isinstance(app_session, str) or not app_session or not isinstance(home, str) or not home:
        raise ValueError("generation needs nonempty App session and home identities")
    if not isinstance(spawn_counter, int) or isinstance(spawn_counter, bool) or spawn_counter < 1:
        raise ValueError("generation exists only at an actual positive spawn counter")
    # Strict UTF-8 rejects unpaired surrogate codepoints; no Unicode normalization.
    return "gen:v1:s:%s:h:%s:n:%d" % (app_session.encode("utf-8").hex(), home.encode("utf-8").hex(), spawn_counter)


def generation_tuple(reference):
    if not isinstance(reference, str) or not (match := _PATTERN.fullmatch(reference)):
        raise ValueError("not a canonical v1 generation reference")
    try:
        session = bytes.fromhex(match[1]).decode("utf-8")
        home = bytes.fromhex(match[2]).decode("utf-8")
        counter = int(match[3])
    except (ValueError, UnicodeError) as exc:
        raise ValueError("invalid generation tuple encoding") from exc
    result = {"appSession": session, "home": home, "spawnCounter": counter}
    if generation_ref(session, home, counter) != reference:
        raise ValueError("not a canonical v1 generation reference")
    return result
