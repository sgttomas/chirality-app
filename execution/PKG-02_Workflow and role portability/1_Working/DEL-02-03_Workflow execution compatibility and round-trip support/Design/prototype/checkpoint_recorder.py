"""Current-phase checkpoint recorder over scripted observations (EXEC-v0.6 §2.4).

Design prototype for DEL-02-03. Not product code. The input is a script of
observations already mapped to CE events (the native-item mapping of §2.5 is
not exercised: its MCP-path cells stay "OBS-1 pending", R13-6). The recorder
applies the §2.4.3 transition table and the SP-6 / JA-1 / lapse rules it
cites, and emits **recorder outputs** {kind, observedAt, body}: the RS entry
kind and a CE body of `checkpoint-record-entries.schema.json` (R14-1). It
writes no record container; the RS writer adds the RS header (RS §13.2) and
appends each output as an RS entry (DEL-04-03 `prototype/exec_to_rs.py`).
It never requests, pauses, interrupts, refuses or prompts: its only output
is entries (RC-4).
"""

LABELS_CLEARED_ON_PERFORMANCE = ("act lapsed at", "waiting — lapsed at", "prior act not counted")


class Arrival:
    def __init__(self, cp, ordinal, bound):
        self.cp, self.ordinal, self.bound = cp, ordinal, dict(bound)
        self.disposition, self.perf = "waiting", 0
        self.coverage = {}          # referent -> act record identity counted for it
        self.resumed = False
        self.lapsed_after_resume = set()
        self.ended = False
        self.annotations = []       # RS structured annotation objects (RS §13.3)


class Recorder:
    def __init__(self, run_id, workflow, surface):
        # Run context: written by the App writer as RS run_opened (RS §14.1), not by this recorder.
        self.run = {"run_id": run_id, "workflow": workflow, "surface": surface}
        self.outputs = []
        self.checkpoints, self.arrivals, self.acts, self.current = {}, [], {}, {}

    # -- output --------------------------------------------------------------
    def _w(self, kind, t, **body):
        o = {"kind": kind, "observedAt": t, "body": body}
        self.outputs.append(o)
        return o

    @staticmethod
    def _aref(a):
        return {"checkpoint": a.cp, "arrivalOrdinal": a.ordinal}

    def _actref(self, act_id):
        a = self.acts[act_id]
        return {"recordId": act_id, "actKind": a["kind"], "capturedAt": a["t"], "capturingSurface": a["surface"]}

    def _disp(self, a, t):
        body = {"arrival": self._aref(a), "disposition": a.disposition, "annotations": [dict(x) for x in a.annotations]}
        if a.perf:
            body["performanceOrdinal"] = a.perf
        if a.coverage and a.disposition in ("performed", "lapsed"):
            body["answeredBy"] = sorted(set(a.coverage.values()))
        self._w("disposition_change", t, **body)

    @staticmethod
    def _drop(a, labels):
        a.annotations = [x for x in a.annotations if x["label"] not in labels]

    # -- observations ----------------------------------------------------------
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
            c1 = {"method": method, "value": ci} if ci is not None else "subject absent"
            state = "lapsed" if ci is not None else "lapsed (subject absent)"
            lapse = dict(act=self._actref(act_id), state=state, referents=[ref],
                         c0={"method": method, "value": c0}, c1=c1, time=t, arrival=self._aref(a))
            if a.ended:
                self._w("act_lapsed", t, **lapse, when="after run end")
                if a.disposition == "performed":
                    a.disposition = "lapsed"
                    a.annotations.append({"label": "act lapsed at", "time": t, "referents": [ref]})
                    self._disp(a, t)
                continue
            del a.coverage[ref]
            self._w("act_lapsed", t, **lapse, when="after resume" if a.resumed else "before resume")
            if ci is None:
                a.annotations.append({"label": "subject absent", "referents": [ref]})
            if a.disposition == "performed" and not a.resumed:
                a.disposition = "waiting"                      # R2-19: before resume
                a.annotations.append({"label": "waiting — lapsed at", "time": t, "referents": [ref]})
            elif a.disposition == "performed":
                a.lapsed_after_resume.add(ref)                 # R8-12 item 1: nothing says waiting
                a.annotations.append({"label": "act lapsed at", "time": t, "referents": [ref]})
            self._disp(a, t)

    def listed(self, cp, t, *, act, rw, subject_class, purpose, scope, governed=False,
               evaluability=("evaluable", "")):
        self.checkpoints[cp] = {"act": act, "subject_class": subject_class, "governed": governed}
        self._w("checkpoint_listed", t, checkpoint=cp, requiredAct=act, reachedWhenKind=rw,
                subjectClass=subject_class, governed=governed, purpose=purpose, scope=scope,
                evaluability={"status": evaluability[0], "reason": evaluability[1]})

    def act(self, act_id, kind, referents, t, surface="host_act_facility"):
        """A human-act record observed (RS §6), cited by its RS record identity; bound {referent: c0}."""
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
                    reason="another act kind", capturedBeforeArrival=before)
            if before:
                a.annotations.append({"label": "prior act not counted", "actRef": act_id, "reason": "another act kind"})
            return
        stale = [r for r in inter if act["refs"][r] != self.current.get(r)]          # SP-4
        if stale:
            self._w("act_not_counted", t, arrival=self._aref(a), act=self._actref(act_id),
                    reason="content no longer current", capturedBeforeArrival=before)
            if before:
                a.annotations.append({"label": "prior act not counted", "actRef": act_id,
                                      "reason": "content no longer current"})
            return
        for r in inter:
            a.coverage[r] = act_id
            a.lapsed_after_resume.discard(r)
        self._w("act_counted", t, arrival=self._aref(a), act=self._actref(act_id),
                relation="earlier act" if before else "after arrival", referents=inter)
        if before:
            a.annotations.append({"label": "by earlier act", "actRef": act_id, "time": act["t"], "referents": inter})

    def _maybe_performed(self, a, t):
        complete = all(r in a.coverage for r in a.bound)
        if not complete:
            return
        relapse = a.disposition == "performed" and not a.lapsed_after_resume and any(
            x["label"] == "act lapsed at" for x in a.annotations)
        if a.disposition == "waiting" or relapse:
            a.disposition = "performed"
            a.perf += 1
            a.resumed = False
            self._drop(a, LABELS_CLEARED_ON_PERFORMANCE)
            acts = sorted(set(a.coverage.values()))
            if len(acts) > 1:
                self._drop(a, ("answered by acts",))
                a.annotations.append({"label": "answered by acts", "actRefs": acts})
            self._disp(a, t)

    def arrive(self, cp, bound, t, *, event_ref, source="native_item", time_source="supplier_item_time",
               purpose, scope, limits=(), method="m-fx"):
        ordinal = 1 + sum(1 for a in self.arrivals if a.cp == cp)
        a = Arrival(cp, ordinal, bound)
        self.arrivals.append(a)
        c = self.checkpoints[cp]
        self._w("checkpoint_arrival", t, checkpoint=cp, requiredAct=c["act"], subjectClass=c["subject_class"],
                governed=c["governed"], arrivalOrdinal=ordinal,
                event={"source": source, "ref": event_ref, "evidencedTime": {"value": t, "source": time_source}},
                referents=[{"subject": r, "content": {"method": method, "value": v}} for r, v in bound.items()],
                purpose=purpose, scope=scope, limits=list(limits),
                requestObservation={"state": "not yet observed"})
        for act_id, act in list(self.acts.items()):                               # SP-6
            inter = [r for r in act["refs"] if r in a.bound]
            if inter:
                self._evaluate(a, act_id, inter, t, before=True)
        if all(r in a.coverage for r in a.bound):
            a.disposition, a.perf = "performed", 1
        self._disp(a, t)
        return a

    def request(self, form, ref, t, arrival=None, *, act_kind=None, subject=None, purpose=None):
        """RC-5: a structured request only. Kind, subject and purpose only as the request names them (R14-2)."""
        live = [a for a in self.arrivals if not a.ended and a.disposition == "waiting"]
        body = dict(requester={"kind": "agent" if form != "MCP elicitation" else "not established (MCP server or agent)"},
                    form=form, actKind=act_kind or "not named by the request",
                    subject=subject or "not named by the request", purpose=purpose or "not named by the request",
                    association="arrival association not established",
                    evidence={"kind": "conversation item", "ref": ref, "resolutionAtWrite": "resolved"}, time=t)
        if arrival is None and len(live) == 1:
            arrival = live[0]
        if arrival is not None:
            body.update(association="associated with the current arrival", arrival=self._aref(arrival))
        return self._w("act_request", t, **body)

    def action(self, ref, t, by="agent"):
        if by != "agent":
            return                                  # the person's own operation: never annotated
        for a in self.arrivals:
            if a.ended:
                continue
            if a.disposition == "performed" and not a.resumed:
                a.resumed = True
                self._w("run_resumed", t, arrival=self._aref(a), firstActionRef=ref, time=t)
            elif a.disposition == "waiting" or a.lapsed_after_resume:
                self._w("continued_past", t, arrival=self._aref(a), actionRef=ref,
                        actKind=self.checkpoints[a.cp]["act"], turnInitiator="agent")

    def end(self, t, by="the person", cause="stopped by the person"):
        waiting = [self._aref(a) for a in self.arrivals if not a.ended and a.disposition == "waiting"]
        for a in self.arrivals:
            a.ended = True
        self._w("run_ended", t, stoppedBy=by, cause=cause, waitingArrivals=waiting)

    def final(self):
        return {(a.cp, a.ordinal): (a.disposition, a.perf, dict(a.coverage)) for a in self.arrivals}
