#!/usr/bin/env python3
"""CC-ACCESS-EXPLICIT-PROJECT-CONTEXT offline source-claim controls only."""
from pathlib import Path
import json
import copy
import access_model as A
import jsonschema_subset as V


def main():
    app = A.App()
    app.configure_local("fixture")
    # Poisoned sentinel cannot become a shared unknown-project preference.
    app.last_choice[None] = ("local-provider:fixture", "fixture", "must-not-offer")
    original = copy.deepcopy(app.last_choice)
    unknown = app.new_conversation(None)
    assert unknown.offer is None and unknown.record() is None
    assert unknown.message("draft") == "refused" and unknown.refusal["reason"] == "no-model-selected"
    unknown.choose("local-provider:fixture", "fixture", "explicit-person-model")
    assert app.last_choice == original
    assert unknown.message("ordinary input") == "started" and unknown.record() is None
    assert unknown.message("next input") == "turn"
    assert app.thread_starts[-1][1] == {"modelProvider": "fixture", "model": "explicit-person-model"}
    assert unknown.view()["projectStanding"] == "not-established"
    assert unknown.view()["canonicalSelectionRecord"] is None
    assert unknown.view()["projectLastChoiceAvailable"] is False
    print("PASS unknown no-row/no offer/save; genuine explicit choice starts ordinary input, no-model guard retained")
    known = app.new_conversation("explicit-directory:P")
    known.choose("local-provider:fixture", "fixture", "known-person-model")
    assert known.message("known input") == "started"
    before = copy.deepcopy(known.record())
    view = known.view("explicit-directory:Q")
    assert view["projectAtSelection"] == "explicit-directory:P" and view["contextRelation"] == "different"
    assert known.record() == before
    assert app.last_choice["explicit-directory:P"][2] == "known-person-model"
    assert "explicit-directory:Q" not in app.last_choice
    unknown_view = unknown.view("explicit-directory:Q")
    assert unknown_view["projectAtSelection"] is None and unknown.record() is None
    assert unknown_view["contextRelation"] == "unbound"
    view["selection"]["model"] = "renderer-cannot-change-source"
    assert known.selection["model"] == "known-person-model"
    try:
        known.project = "explicit-directory:Q"
        raise AssertionError("context retagged")
    except AttributeError:
        pass
    print("PASS P stays P/current Q separate; unknown not backfilled; no choice movement/view hydration/retag")
    other = app.new_conversation("explicit-directory:Q")
    assert other.offer is None
    again = app.new_conversation("explicit-directory:P")
    assert again.offer and again.selection is None and not again.offer["applied"]
    assert again.message("offer not accepted") == "refused"
    again.accept_offer()
    assert again.message("explicitly accepted") == "started"
    print("PASS different explicit projects do not collapse; same P offer remains informational until person's acceptance")
    for bad in ("", 7, Path("/native/cwd-is-not-a-project-handle")):
        try:
            app.new_conversation(bad)
            raise AssertionError("invalid project input admitted")
        except ValueError:
            pass
    schema = json.loads((Path(__file__).resolve().parents[1] / "access.conversation-selection.schema.json").read_text())
    assert not V.errors(known.record(), schema, schema)
    malformed = copy.deepcopy(known.record())
    malformed["project"] = None
    assert V.errors(malformed, schema, schema)
    assert unknown.record() is None
    unknown.entry_changed(False)
    assert unknown.message("unavailable input") == "refused" and unknown.refusal["reason"] == "entry-unavailable"
    print("PASS known0.2 record valid; null/empty/coerced project avoided; real entry-availability guard independent")
    print("Model/source claims only; no actual Root/native/provider/cold qualification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
