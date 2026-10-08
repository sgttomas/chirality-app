#!/usr/bin/env python3
"""Offline review and change-impact file checks; no review or route is performed."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
from referencing import Registry
from rules import impact_violations, review_violations, rule_violations

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[2]
SCHEMAS={'result':'exam.result-record.schema.json','review':'exam.review-record.schema.json','change':'exam.change-impact.schema.json'}
LIMITS=[
    'File and declared-relationship checks only; no observation, actual review, independence or authorization is verified.',
    'Joins cover only the supplied records. Other evidence, affectedness, unreadable reliance and omitted results require the examination owner.',
    'Opaque subject/from/to identities are matched to caller-selected aliases; their real-world identity is not inferred.',
    'No runner/browser/native admission, human act, qualification, acceptance or release. CI26 full support identity remains pending.',
]


def sha(data): return hashlib.sha256(data).hexdigest()


def parse(data):
    def unique(pairs):
        result={}
        for k,v in pairs:
            if k in result: raise ValueError(f'duplicate JSON key: {k}')
            result[k]=v
        return result
    def invalid(value): raise ValueError(f'non-JSON constant: {value}')
    return json.loads(data,object_pairs_hook=unique,parse_constant=invalid)


def load(path):
    data=Path(path).read_bytes()
    return parse(data),{'path':str(path),'sha256':sha(data)}


def exact_keys(value,keys,label):
    if not isinstance(value,dict) or set(value)!=set(keys):
        raise ValueError(f'{label} requires exactly: {", ".join(keys)}')


def text(value,label):
    if not isinstance(value,str) or not value.strip(): raise ValueError(f'{label} must be a nonempty string')


def basis_selection(value):
    exact_keys(value,('subject','configuration','criterion'),'result basis')
    for key in value:
        if not isinstance(value[key],dict): raise ValueError(f'basis {key} must be an object')


def same_basis(result,basis):
    return all(result[k]==basis[k] for k in ('subject','configuration','criterion'))


class Support:
    def __init__(self,project=PROJECT,manifest=HERE/'sources.json'):
        self.manifest_bytes=Path(manifest).read_bytes()
        pins=parse(self.manifest_bytes); schemas={}
        for source,pin in pins['sources'].items():
            data=(Path(project)/source).read_bytes()
            if sha(data)!=pin: raise ValueError(f'canonical source drift: {source}')
            for kind,name in SCHEMAS.items():
                if source.endswith('/'+name): schemas[kind]=parse(data)
        if set(schemas)!=set(SCHEMAS): raise ValueError('incomplete schema source lock')
        for schema in schemas.values(): Draft202012Validator.check_schema(schema)
        self.validators={k:Draft202012Validator(v,registry=Registry()) for k,v in schemas.items()}

    def validate(self,kind,record,results=None):
        errors=sorted(self.validators[kind].iter_errors(record),key=lambda e:str(list(e.path)))
        if errors: return [{'code':'SCHEMA','path':list(e.path),'message':e.message} for e in errors]
        if kind=='review': codes=review_violations(record)
        elif kind=='result': codes=rule_violations(record)
        else: codes=impact_violations(record,results or {})
        return [{'code':c} for c in sorted(set(codes))]

    def index_results(self,records):
        errors=[]; index={}
        for record in records:
            found=self.validate('result',record)
            if found: errors.extend(found); continue
            key=record['record_id']
            if key in index: errors.append({'code':'DUPLICATE-RESULT-ID','record_id':key})
            index[key]=record
        return errors,index

    def review_join(self,review,result,selection):
        exact_keys(selection,('subject_alias','reviewer_identity','author_identities','review_kind','reported_as_independent','basis'),'review selection')
        for key in ('subject_alias','reviewer_identity','review_kind'): text(selection[key],key)
        authors=selection['author_identities']
        if not isinstance(authors,list) or not authors: raise ValueError('author_identities must be a nonempty list')
        for author in authors: text(author,'author identity')
        if len(set(authors))!=len(authors): raise ValueError('selected authors must be unique')
        if type(selection['reported_as_independent']) is not bool: raise ValueError('selected independence must be boolean')
        basis_selection(selection['basis'])
        errors=self.validate('review',review)+self.validate('result',result)
        if errors: return errors,[]
        def require(test,code):
            if not test: errors.append({'code':code})
        require(result['run_basis']=='candidate' and review['subject']['kind']=='candidate','REVIEW-CANDIDATE-BASIS')
        require(review['subject']['identity']==selection['subject_alias'],'REVIEW-SUBJECT-ALIAS')
        require(same_basis(result,selection['basis']),'REVIEW-RESULT-BASIS')
        require(review['reviewer']['identity']==selection['reviewer_identity'],'REVIEW-REVIEWER')
        require(sorted(a['identity'] for a in review['authors'])==sorted(authors),'REVIEW-AUTHORS')
        require(review['review_kind']==selection['review_kind'],'REVIEW-KIND')
        require(review['reported_as_independent']==selection['reported_as_independent'],'REVIEW-INDEPENDENCE-CLAIM')
        require(result['record_id'] in review['evidence_set'],'REVIEW-RESULT-NOT-CITED')
        require(len(review['evidence_set'])==len(set(review['evidence_set'])),'REVIEW-DUPLICATE-EVIDENCE')
        ids=[f['id'] for f in review['findings']]
        require(len(ids)==len(set(ids)),'REVIEW-DUPLICATE-FINDING')
        for finding in review['findings']:
            d=finding['disposition']
            if d['state']=='repaired':
                require(d['confirmed_by']==review['reviewer']['identity'],'REVIEW-REPAIR-CONFIRMER')
        # Remaining references are not silently resolved or declared examined.
        unresolved=[ref for ref in review['evidence_set'] if ref!=result['record_id']]
        return errors,unresolved

    def change_join(self,change,before,after,selection,rerun=None):
        exact_keys(selection,('from_alias','to_alias','before_basis','rerun_basis'),'change selection')
        text(selection['from_alias'],'from_alias'); text(selection['to_alias'],'to_alias')
        basis_selection(selection['before_basis'])
        if selection['rerun_basis'] is not None: basis_selection(selection['rerun_basis'])
        errors=[]
        for r in (before,after): errors.extend(self.validate('result',r))
        if rerun is not None: errors.extend(self.validate('result',rerun))
        # Check shape before selecting a row; full EXP-R8 below has only this pair's context.
        schema_errors=list(self.validators['change'].iter_errors(change))
        if schema_errors: errors.extend({'code':'SCHEMA','message':e.message} for e in schema_errors)
        if errors: return errors,[]
        def require(test,code):
            if not test: errors.append({'code':code})
        require(before['run_basis']=='candidate','CHANGE-CANDIDATE-BASIS')
        require(same_basis(before,selection['before_basis']),'CHANGE-BEFORE-BASIS')
        require(change['from']==selection['from_alias'] and change['to']==selection['to_alias'],'CHANGE-ALIASES')
        preserved=copy.deepcopy(after); preserved['currency']=before['currency']
        require(preserved==before,'CHANGE-HISTORY-MUTATED')
        rows=[a for a in change['affected'] if a['prior_result']==before['record_id']]
        require(len(rows)==1,'CHANGE-PRIOR-ROW')
        unresolved=[a['prior_result'] for a in change['affected'] if a['prior_result']!=before['record_id']]
        if len(rows)!=1: return errors,unresolved
        row=rows[0]
        require(row['case_id']==before['case']['case_id'],'CHANGE-CASE')
        partial=copy.deepcopy(change); partial['affected']=[row]
        errors.extend({'code':c} for c in impact_violations(partial,{after['record_id']:after}))
        if rerun is None:
            require('rerun_result' not in row,'CHANGE-RERUN-MISSING')
            require(selection['rerun_basis'] is None,'CHANGE-EXPECTED-RERUN-MISSING')
            return errors,unresolved
        require(selection['rerun_basis'] is not None,'CHANGE-RERUN-BASIS-MISSING')
        if selection['rerun_basis'] is not None:
            require(same_basis(rerun,selection['rerun_basis']),'CHANGE-RERUN-BASIS')
        require(row.get('rerun_result')==rerun['record_id'],'CHANGE-RERUN-REFERENCE')
        require(rerun['record_id'] not in (before['record_id'],change['record_id']),'CHANGE-RERUN-ID')
        require(rerun['run_basis']=='candidate' and rerun['case']==before['case'],'CHANGE-RERUN-CASE')
        require(rerun['currency']=={'state':'current','change_ref':change['record_id']},'CHANGE-RERUN-CURRENCY')
        if before['criterion']['identity']!=rerun['criterion']['identity']:
            require(change['change']['kind']=='criterion_disposition'
                    and bool(change['change'].get('disposition_ref'))
                    and change['change']['disposition_ref']==rerun['criterion'].get('disposition_ref'),
                    'CHANGE-CRITERION-DISPOSITION')
        return errors,unresolved


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='command',required=True)
    val=subs.add_parser('validate'); val.add_argument('kind',choices=('review','change')); val.add_argument('record'); val.add_argument('--result',action='append',default=[])
    review=subs.add_parser('review-join')
    for field in ('review','result','selection'): review.add_argument('--'+field,required=True)
    change=subs.add_parser('change-join')
    for field in ('change','before','after','selection'): change.add_argument('--'+field,required=True)
    change.add_argument('--rerun')
    args=parser.parse_args(argv)
    inputs=[]
    def read(path):
        record,identity=load(path); inputs.append(identity); return record
    try:
        support=Support(); unresolved=[]; pending=False
        if args.command=='validate':
            record=read(args.record)
            records=[read(path) for path in args.result]
            errors,index=support.index_results(records)
            if not errors: errors=support.validate(args.kind,record,index)
        elif args.command=='review-join':
            errors,unresolved=support.review_join(read(args.review),read(args.result),read(args.selection))
        else:
            ci=read(args.change); before=read(args.before); after=read(args.after); selected=read(args.selection)
            rerun=read(args.rerun) if args.rerun else None
            errors,unresolved=support.change_join(ci,before,after,selected,rerun)
            pending=rerun is None
        report={'file_checks_passed':not errors,'errors':errors,'scope':args.command,'inputs':inputs,
                'unresolved_other_references':unresolved,'rerun_not_supplied':pending,'limits':LIMITS,
                'review_or_repair_verified':False,'route_admission':'not_established',
                'tool_sha256':sha(Path(__file__).read_bytes()),'rules_sha256':sha((HERE/'rules.py').read_bytes()),
                'source_lock_sha256':sha(support.manifest_bytes)}
        print(json.dumps(report,indent=2)); return 1 if errors else 0
    except (ValueError,OSError) as error:
        print(json.dumps({'file_checks_passed':False,'input_error':str(error),'inputs':inputs,'limits':LIMITS},indent=2)); return 2


if __name__=='__main__': sys.exit(main())
