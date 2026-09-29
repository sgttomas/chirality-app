# Grounding of each row under the project's accepted extraction rule
# (_COORDINATION.md: "Agent-proposed candidates derive from local SoWs and
# accepted interfaces"). DRAFT Design files corroborate but do not ground.
# G = C1 SoW correction(s) that put the relationship in the host SoW
# (applied through scope-of-work REVISE), or 'SOW-NOW' (current SoW text).
# P1 = needs new or refreshed SoW wording from P1; fallback: human declaration.
# Overrides: (ground, disp, route, why)
OPT = 'Optional supplier-side mirror. No C1 SoW correction or current SoW sentence states this receiver, so it cannot be extracted under the accepted rule (local SoWs and accepted interfaces; the Design files are DRAFT). The consumer\'s row already represents the arc. Defer, or the owner declares it (O-3).'
G = {
 # DEL-04-01
 'R-04-01-a':('SC-04-01-2',None,None,None),'R-04-01-b':('SC-04-01-2',None,None,None),'R-04-01-c':('SC-04-01-2',None,None,None),
 'R-04-01-d':('SC-04-01-2',None,None,None),'R-04-01-e':('SC-04-01-2',None,None,None),'R-04-01-f':('SC-04-01-2',None,None,None),
 'DEP-04-01-017':('SC-04-01-8',None,None,None),'DEP-04-01-018':('SC-04-01-9',None,None,None),
 'R-04-01-h':('SC-04-01-8',None,None,None),'R-04-01-i':('SC-04-01-10 (P1 refresh for DECISION-4)',None,None,None),
 # DEL-04-02
 'R-04-02-a':('SC-04-02-2',None,None,None),'R-04-02-b':(None,'DEFER','NONE',OPT),
 'R-04-02-c':('SC-04-02-2 (its direct-consumption option)',None,None,None),'R-04-02-d':('SC-04-02-2 (P1 refresh for R8-1)',None,None,None),
 'R-04-02-e':('SC-04-02-2',None,None,None),'R-04-02-f':('SC-04-02-2',None,None,None),'R-04-02-g':('SC-04-02-2',None,None,None),
 'R-04-02-h':('SC-04-02-2',None,None,None),'R-04-02-i':('SC-04-02-2',None,None,None),
 'DEP-04-02-011/-012':('C1-A SC-04-02 OI pointer corrections',None,None,None),'R-04-02-l':('C1-A SC-04-02 OI pointer corrections',None,None,None),
 'R-04-02-m':('C1-A SC-04-02 D6 wording (P1 refresh for DECISION-4)',None,None,None),
 'R8-AS-1':('P1',None,'EXTRACT*',None),
 # DEL-04-03
 'R-04-03-a':('SC-04-03-1',None,None,None),'R-04-03-b':('SC-04-03-1',None,None,None),'R-04-03-c':('SC-04-03-1',None,None,None),
 'R-04-03-d':(None,'DEFER','NONE','Package-level only in the SoW (DEP-04-03-011 → PKG-02). '+OPT),
 'R-04-03-e':(None,'DEFER','NONE','Package-level only in the SoW (DEP-04-03-011 → PKG-02). '+OPT),
 'R-04-03-f':('SC-04-03-2',None,None,None),'R-04-03-g':('SC-04-03-2',None,None,None),'R-04-03-h':('SC-04-03-2',None,None,None),
 'R-04-03-i':('SC-04-03-2','KEEP','EXTRACT','SC-04-03-2 names DEL-09-09 as a consumer of the record meaning, so the mirror is grounded.'),
 'R-04-03-j':(None,'DEFER','NONE',OPT),
 'R-04-03-k':('SC-04-03-1',None,None,None),'R-04-03-l':('SC-04-03-1 (P1 refresh for R8-1)',None,None,None),
 'R-04-03-m':('SC-04-03-1',None,None,None),'R-04-03-n':('SC-04-03-1',None,None,None),
 'R-04-03-o':('P1',None,'EXTRACT*','N-11 has no grounded row on either side. SC-04-03-2 keeps "PKG-03 basis/receipts" at package level.'),
 'DEP-04-03-012':('SOW-NOW',None,None,None),'DEP-04-03-019':('SC-04-03-4',None,None,None),
 'R8-RS-1':('P1',None,'EXTRACT*',None),
 # DEL-02-01
 'R-02-01-a':(None,'DEFER','NONE',OPT),'R-02-01-b':(None,'DEFER','NONE',OPT),'R-02-01-c':(None,'DEFER','NONE',OPT),
 'R-02-01-d':(None,'DEFER','NONE',OPT),'R-02-01-e':(None,'DEFER','NONE',OPT),'R-02-01-f':(None,'DEFER','NONE',OPT),
 'R-02-01-g':('SC-02-01-1, SC-02-01-2',None,None,None),'R-02-01-h':('P1 (SC-02-01-6 refreshed to state consumption of DEL-02-03)',None,'EXTRACT*',None),
 'R-02-01-i':('SC-02-01-1, SC-02-01-3',None,None,None),
 'R-02-01-j':(None,'DEFER','NONE',OPT+' The representative row (DEL-09-06, R9-6-1a) is grounded by S9-6-3.'),
 'R-02-01-k':('P1 (SC-02-01-1 must name DEL-03-03 as a receiver, not as a supplier)',None,'EXTRACT*','As C1 words it, SC-02-01-1 ("DEL-03-03 carries constraints on the external channel") would be extracted from CLM-002 as an UPSTREAM input. That is the unevidenced reverse arc DEL-02-01 → DEL-03-03.'),
 'R-02-01-k2':('P1',None,'EXTRACT*','Supplier side of N-B3. Neither SoW grounds N-B3 today.'),
 'R-02-01-l':('SC-02-01-5',None,None,None),'R-02-01-m':('SC-02-01-6 (P1 refresh for DECISION-4)',None,None,None),'R-02-01-n':('SOW-NOW',None,None,None),
 # DEL-02-03
 'R-02-03-a':(None,'DEFER','NONE',OPT),'R-02-03-c':(None,'DEFER','NONE',OPT),
 'R-02-03-d':('SC-02-03-4',None,None,None),'R-02-03-e':('P1',None,'EXTRACT*','N-22 has no grounded row. The current CLM-003 ownership sentence about DEL-05-01 was not extracted as an input in DAG-001.'),
 'R-02-03-f':('SC-02-03-4',None,None,None),'R-02-03-g':('SC-02-03-4',None,None,None),'R-02-03-h':('SC-02-03-4',None,None,None),
 'R-02-03-i':(None,'DEFER','NONE',OPT),'R-02-03-j':(None,'DEFER','NONE',OPT),'R-02-03-k':(None,'DEFER','NONE',OPT),'R-02-03-l':(None,'DEFER','NONE',OPT),
 'R-02-03-n':('P1',None,'EXTRACT*','Supplier side of N-27; N-27 has no grounded row today.'),
 'DEP-02-03-015/-016':('SC-02-03-5',None,None,None),'R-02-03-o':('SC-02-03-1, SC-02-03-3 (P1 refresh for DECISION-4)',None,None,None),
 'X-1':('SC-02-03-4',None,None,None),
 # DEL-03-01
 **{k:(None,'DEFER','NONE',OPT) for k in ['M-01-1','M-01-2','M-01-3','M-01-4','M-01-5','M-01-6','M-01-7','M-01-8','N-01-mir','N-10-mir']},
 'M-01-3-pkg':('SOW-NOW',None,None,None),'DEP-03-01-024':('S-01-2',None,None,None),
 'N-B1':('P1',None,'EXTRACT*','N-11 has no grounded row on either side. The current SoW names DEL-04-03 only as an owner, which DAG-001 extraction did not treat as an input.'),
 # DEL-03-02
 **{k:(None,'DEFER','NONE',OPT) for k in ['M-02-1','M-02-2','M-02-3','N-18/N-21-mir','N-21-mir']},
 'DEP-03-02-017':('S-02-1',None,None,None),
 'N-B2':(None,'DEFER','NONE','Consumer-side representative of N-05. No C1 SoW correction for DEL-03-02 states consumption of DEL-04-02 (its SoW names DEL-04-02 only as an owner, which was extracted DOWNSTREAM as DEP-03-02-018). N-05 is established by the grounded supplier row R-04-02-g (SC-04-02-2). Add later if P1 adds the sentence.'),
 'N-B3':('P1',None,'EXTRACT*','Neither SoW grounds N-B3.'),
 # DEL-03-03
 **{k:(None,'DEFER','NONE',OPT) for k in ['M-03-1','N-14-mir','N-24-mir']},
 'DEP-03-03-008':('S-03-1',None,None,None),
 'N-B4':('P1',None,'EXTRACT*','Neither the DEL-03-03 nor the DEL-01-01 C1 SoW corrections name the other deliverable.'),
 'N-B5':(None,'DEFER','NONE','Consumer-side representative of N-06. No DEL-03-03 SoW correction; N-06 is established by the grounded supplier row R-04-02-h (SC-04-02-2).'),
 'N-B6':('P1',None,'EXTRACT*','N-20 has no grounded row today (see R-02-01-k).'),
 'N-B7':('P1 (S-03-4 refreshed for R8-1 and naming DEL-02-03)',None,'EXTRACT*','S-03-4 cites "EXEC §3.6" without the deliverable ID, and R8-1 supersedes its hold wording.'),
 # DEL-03-04
 'DEP-03-04-011':('C1-B S-04 OI pointer correction',None,None,None),
 'N-B9':('S-04-6',None,None,None),'N-B10':('S-04-6',None,None,None),'N-B11':('S-04-6',None,None,None),
 # DEL-01-01
 'M-11-1':(None,'DEFER','NONE',OPT),'DEP-01-01-017':('S-11-2',None,None,None),'DEP-01-01-018':('S-11-2',None,None,None),
 # DEL-05-01
 'R5-1-1':('S5-1-1',None,None,None),'R5-1-3':('S5-1-4',None,None,None),'R5-1-5':('S5-1-4',None,None,None),
 'R8-LOOP-1':('P1 (DECISION-5 wording)',None,'EXTRACT*',None),
 # DEL-05-02
 'R5-2-1':('S5-2-2',None,None,None),'R5-2-2':('S5-2-3 (main option; P1 refresh for R8-1)',None,None,None),
 'R5-2-3':('S5-2-1',None,None,None),'R5-2-4':('SOW-NOW',None,None,None),'R5-2-5':('S5-2-5',None,None,None),'R5-2-6':('C1-C S5-2 relay wording',None,None,None),
 # DEL-09-06
 **{k:('S9-6-3',None,None,None) for k in ['R9-6-1a','R9-6-1b','R9-6-2a','R9-6-2b','R9-6-2c','R9-6-3a','R9-6-3b','R9-6-3c']},
 'R9-6-1-pkg':('SOW-NOW',None,None,None),'R9-6-4':(None,'DEFER','NONE',OPT),'R9-6-5':(None,'DEFER','NONE',OPT),
 'R9-6-6':('S9-6-1',None,None,None),'R9-6-7':('SOW-NOW (OUT-004)',None,None,None),
 # DEL-09-09
 'R9-9-1':('S9-9-4',None,None,None),'R9-9-2':('S9-9-4',None,None,None),'R9-9-3':('S9-9-4 (P1 refresh for R8-1)',None,None,None),
 'R9-9-4':(None,'DEFER','NONE',OPT),'R9-9-5':('C1-C S9-9 relay wording',None,None,None),'R9-9-6':('C1-C S9-9 A13 wording',None,None,None),
}
# One row per ungrounded arc (on the side with a natural P1 hook); the other side is an optional mirror.
G['R-04-03-o']=(None,'DEFER','NONE','Supplier side of N-11. One row per ungrounded arc is enough; the consumer row N-B1 carries it. If instead P1 refines SC-04-03-2\'s "PKG-03 basis/receipts" to name DEL-03-01, extraction yields this DOWNSTREAM row, which also establishes N-11. It also partly resolves package row DEP-04-03-012.')
G['R-02-01-k2']=(None,'DEFER','NONE','Supplier side of N-B3; optional. The consumer row N-B3 carries the arc if P1 grounds it.')
G['R-02-03-n']=(None,'DEFER','NONE','Supplier side of N-27; optional. The consumer row N-B7 carries the arc if P1 grounds it.')
G['N-B6']=(None,'DEFER','NONE','Consumer side of N-20; optional. N-20 is carried by the supplier row R-02-01-k once P1 words SC-02-01-1 with DEL-03-03 as a receiver.')
G['DEP-04-02-011/-012']=('SC-04-02-5',None,None,None)
G['R-04-02-l']=('SC-04-02-5',None,None,None)
G['R-04-02-m']=('SC-04-02-6 (P1 refresh for DECISION-4)',None,None,None)
G['DEP-03-04-011']=('S-04-1',None,None,None)
G['R5-2-6']=('Notes refresh (no SoW change needed)',None,None,None)
G['R9-9-5']=('S9-9-5 (P1 refresh: SQ answers)',None,None,None)
G['R9-9-6']=('Statement refresh (no SoW change needed)',None,None,None)
