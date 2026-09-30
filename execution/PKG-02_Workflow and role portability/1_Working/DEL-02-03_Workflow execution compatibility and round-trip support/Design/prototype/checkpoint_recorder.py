"""Current-phase checkpoint recorder over scripted observations (EXEC-v0.6 §2.4).

Design prototype for DEL-02-03. Not product code. The input is a script of
observations already mapped to CE events (the native-item mapping of §2.5 is
not exercised: its ordering at pin 0.158.0 is "OBS-1 pending"). The recorder
applies the §2.4.3 transition table and the SP-6 / JA-1 / lapse rules it
cites, and writes entries in the PROPOSED `checkpoint-record-entries`
schema. It never requests, pauses, interrupts, refuses or prompts: its only
output is entries (RC-4).
"""


class Arrival:
    def __init__(self, cp, ordinal, bound):
        self.cp, self.ordinal, self.bound = cp, ordinal, dict(bound)
        self.disposition, self.perf = "waiting", 0
        self.coverage = {}          # referent -> act_id counted for it
        self.resumed = False
        self.lapsed_after_resume = set()
        self.ended = False
        self.annotations = []


class Recorder:
    def __init__(self, run_id, workflow, surface):
        self.doc = {"format": "exec-checkpoint-record-entries/proposed-0.6", "phase": "current",
                    "run": {"run_id": run_id, "workflow": workflow, "surface": surface},
                    "entries": []}
        self.checkpoints, self.arrivals, self.acts, self.current = {}, [], {}, {}

    # -- entry writer ----------------------------------------------------
    def _w(self, kind, t, **fields):
        n = len(self.doc["entries"]) + 1
        e = {"entry_id": "e%d" % n, "order": n, "kind": kind, "observed_at": t}
        e.update(fields)
        self.doc["entries"].append(e)
        return e

    @staticmethod
    def _aref(a):
        return {"checkpoint": a.cp, "ordinal": a.ordinal}

    def _actref(self, act_id):
        a = self.acts[act_id]
        return {"record_id": act_id, "act_kind": a["kind"], "captured_at": a["t"],
                "capturing_surface": a["surface"]}

    def _disp(self, a, t):
        self._w("disposition", t, arrival=self._aref(a), disposition=a.disposition,
                performance_ordinal=a.perf, annotations=list(a.annotations))

    # -- observations ----------------------------------------------------
    def content(self, ref, ci, t, method="m-fx"):
        """A content identity observed for a referent (None = subject absent)."""
        old = self.current.get(ref)
        self.current[ref] = ci
        if old is None or old == ci:
            return
        for a in self.arrivals:
            if ref not in a.bound:
                continue
            act_id = a.coverage.get(ref)
            c0 = a.bound[ref]
            a.bound[ref] = ci if ci is not None else c0
            if act_id is None:
                continue
            c1 = {"value": ci, "method": method} if ci is not None else "subject_absent"
            if a.ended:
                self._w("act_lapsed", t, arrival=self._aref(a), act=self._actref(act_id),
                        referents=[ref], c0={"value": c0, "method": method}, c1=c1,
                        when="after_run_end")
                if a.disposition == "performed":
                    a.disposition = "lapsed"
                    a.annotations.append("lapsed: %s" % ref)
                    self._disp(a, t)
                continue
            del a.coverage[ref]
            when = "after_resume" if a.resumed else "before_resume"
            self._w("act_lapsed", t, arrival=self._aref(a), act=self._actref(act_id),
                    referents=[ref], c0={"value": c0, "method": method}, c1=c1, when=when)
            if ci is None:
                a.annotations.append("subject absent")
            if a.disposition == "performed" and not a.resumed:
                a.disposition = "waiting"                      # R2-19: before resume
                a.annotations.append("lapsed at %s" % t)
            elif a.disposition == "performed":
                a.lapsed_after_resume.add(ref)                 # R8-12 item 1: nothing says waiting
                a.annotations.append("act lapsed at %s (%s)" % (t, ref))
            self._disp(a, t)

    def listed(self, cp, t, *, act, rw, subject_class, purpose, scope, governed=False,
               evaluability=("evaluable", "")):
        self.checkpoints[cp] = {"act": act}
        self._w("checkpoint_listed", t, checkpoint=cp, required_act=act, reached_when_kind=rw,
                subject_class=subject_class, governed=governed, purpose=purpose, scope=scope,
                evaluability={"status": evaluability[0], "reason": evaluability[1]})

    def act(self, act_id, kind, referents, t, surface="host_act_facility"):
        """A human-act record observed (RS §6), bound {referent: c0}."""
        self.acts[act_id] = {"kind": kind, "refs": dict(referents), "t": t, "surface": surface}
        for a in self.arrivals:
            inter = [r for r in referents if r in a.bound]
            if not inter:
                continue
            if a.ended:
                self._w("act_after_run_end", t, arrival=self._aref(a), act=self._actref(act_id))
                continue
            self._evaluate(a, act_id, inter, t, before=False)
            self._maybe_performed(a, t)

    def _evaluate(self, a, act_id, inter, t, before):
        act = self.acts[act_id]
        if act["kind"] != self.checkpoints[a.cp]["act"]:                          # SP-1
            self._w("act_not_counted", t, arrival=self._aref(a), act=self._actref(act_id),
                    reason="other_kind", captured_before_arrival=before)
            return
        stale = [r for r in inter if act["refs"][r] != self.current.get(r)]          # SP-4
        if stale:
            self._w("act_not_counted", t, arrival=self._aref(a), act=self._actref(act_id),
                    reason="content_no_longer_current", captured_before_arrival=before)
            if before and "prior act not counted" not in a.annotations:
                a.annotations.append("prior act not counted")
            return
        for r in inter:
            a.coverage[r] = act_id
            a.lapsed_after_resume.discard(r)
        self._w("act_counted", t, arrival=self._aref(a), act=self._actref(act_id),
                relation="earlier_act" if before else "after_arrival", referents=inter)
        if before:
            a.annotations.append("by earlier act %s at %s" % (act_id, act["t"]))

    def _maybe_performed(self, a, t):
        complete = all(r in a.coverage for r in a.bound)
        if not complete:
            return
        if a.disposition == "waiting" or (a.disposition == "performed" and a.lapsed_after_resume == set()
                                           and any(x.startswith("act lapsed at") for x in a.annotations)):
            a.disposition = "performed"
            a.perf += 1
            a.resumed = False
            a.annotations = [x for x in a.annotations
                             if not x.startswith(("act lapsed at", "lapsed at", "prior act not counted"))]
            acts = sorted(set(a.coverage.values()))
            if len(acts) > 1:
                a.annotations = [x for x in a.annotations if not x.startswith("answered by")]
                a.annotations.append("answered by %d acts: %s" % (len(acts), "; ".join(
                    "%s (%s)" % (x, ", ".join(sorted(r for r, v in a.coverage.items() if v == x)))
                    for x in acts)))
            self._disp(a, t)

    def arrive(self, cp, bound, t, *, event_ref, source="native_item", time_source="supplier_item_time",
               purpose, scope, limits=(), method="m-fx"):
        ordinal = 1 + sum(1 for a in self.arrivals if a.cp == cp)
        a = Arrival(cp, ordinal, bound)
        self.arrivals.append(a)
        self._w("arrival", t, arrival=self._aref(a),
                event={"source": source, "ref": event_ref,
                       "evidenced_time": {"value": t, "source": time_source}},
                bound_subject=[{"referent_id": r, "content_identity": {"value": c, "method": method}}
                               for r, c in bound.items()],
                purpose=purpose, scope=scope, limits=list(limits))
        for act_id, act in list(self.acts.items()):                               # SP-6
            inter = [r for r in act["refs"] if r in a.bound]
            if inter:
                self._evaluate(a, act_id, inter, t, before=True)
        if all(r in a.coverage for r in a.bound):
            a.disposition, a.perf = "performed", 1
        self._disp(a, t)
        return a

    def request(self, form, ref, t, arrival=None):
        live = [a for a in self.arrivals if not a.ended and a.disposition == "waiting"]
        fields = dict(form=form, ref=ref, association="not_established")
        if arrival is None and len(live) == 1:
            arrival = live[0]
        if arrival is not None:
            fields.update(association="associated", arrival=self._aref(arrival))
        self._w("request_observed", t, **fields)

    def action(self, ref, t, by="agent"):
        if by != "agent":
            return                                  # the person's own operation: never annotated
        for a in self.arrivals:
            if a.ended:
                continue
            if a.disposition == "performed" and not a.resumed:
                a.resumed = True
                self._w("run_resumed", t, arrival=self._aref(a), first_action_ref=ref)
            elif a.disposition == "waiting" or a.lapsed_after_resume:
                self._w("continued_past", t, arrival=self._aref(a), action_ref=ref,
                        act_kind=self.checkpoints[a.cp]["act"])

    def end(self, t, by="person", cause="stopped by the person"):
        waiting = [self._aref(a) for a in self.arrivals if not a.ended and a.disposition == "waiting"]
        for a in self.arrivals:
            a.ended = True
        self._w("run_ended", t, by=by, cause=cause, waiting_arrivals=waiting)

    def final(self):
        return {(a.cp, a.ordinal): (a.disposition, a.perf, dict(a.coverage)) for a in self.arrivals}
