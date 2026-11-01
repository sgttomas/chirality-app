"""Exact post-i_bow2kd browser-shell metadata admission; no opaque content reads."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

VERSION='attended-retained-shell/v1'
CANDIDATE='1f67d3822b-8c83d74ae3ce'
IDENTIFIER='dev.chirality.app-v4.candidate.gvpud8q'
ASSESSMENT_PATH=Path('/Users/ryan/dev/chirality-t3/scratch/app-post-i_bow2kd-assessment-l1gpyy6f/assessment.json')
ASSESSMENT_SHA='4f0a37a714d513fc7c564b9416f399126ec5838de67b4789ad3a240322b9e9b1'

POST_J_PATH=Path('/Users/ryan/dev/chirality-t3/scratch/app-post-j580-assessment-9lgnst4_/assessment.json')
POST_J_SHA='485ae1b3d5183b667ce2ef1c3fe6630bfb5e64c6686047a4231c2bf90753ce2c'

POST_EL3_PATH=Path('/Users/ryan/dev/chirality-t3/scratch/app-post-el3-assessment-y2ps41jf/assessment.json')
POST_EL3_SHA='fdec6b5490858f043199513ed019e9e936f8c5ec9517f835f75c666230452291'

def selected_profile(path,digest):
    if digest==POST_EL3_SHA:
        require(Path(path)==POST_EL3_PATH,'retained assessment location differs')
        return 'attended-retained-shell/v3','app-attended-prepared-el3pvau4'
    require(digest in (ASSESSMENT_SHA,POST_J_SHA),'unselected future retained basis')
    if digest==ASSESSMENT_SHA:
        require(Path(path)==ASSESSMENT_PATH,'retained assessment location differs')
        return VERSION,'app-attended-prepared-i_bow2kd'
    require(Path(path)==POST_J_PATH,'retained assessment location differs')
    return 'attended-retained-shell/v2','app-attended-prepared-j58087z7'


def require(ok,reason):
    if not ok:raise RuntimeError(reason)


def roots(home):
    return {name:Path(home)/relative for name,relative in {
        'AppData':'Library/Application Support/'+IDENTIFIER,'WebKit':'Library/WebKit/'+IDENTIFIER,
        'Caches':'Library/Caches/'+IDENTIFIER,'Preferences':'Library/Preferences/'+IDENTIFIER+'.plist',
        'SavedState':'Library/Saved Application State/'+IDENTIFIER+'.savedState',
        'HTTPStorages':'Library/HTTPStorages/'+IDENTIFIER}.items()}


def metadata(home):
    out={}
    for name,root in roots(home).items():
        require(root.parent.resolve()==root.parent,'namespace ancestry alias')
        rows=[];present=os.path.lexists(root)
        if present:
            def visit(path):
                s=path.lstat()
                require(s.st_uid==os.getuid() and (stat.S_ISDIR(s.st_mode) or stat.S_ISREG(s.st_mode)),
                        'foreign, linked or unsupported namespace object')
                if stat.S_ISREG(s.st_mode):require(s.st_nlink==1,'namespace hardlink')
                rows.append({'relative':str(path.relative_to(root)),'device':s.st_dev,'inode':s.st_ino,
                    'mode':s.st_mode,'uid':s.st_uid,'nlink':s.st_nlink,'size':s.st_size,
                    'mtime_ns':s.st_mtime_ns,'ctime_ns':s.st_ctime_ns})
                require(len(rows)<=4000,'namespace metadata bound')
                if stat.S_ISDIR(s.st_mode):
                    for child in sorted(path.iterdir()):visit(child)
            visit(root)
        out[name]={'path':str(root),'present':present,'metadata':rows}
    return out


def shape(assessment,home,prior_attempt='app-attended-prepared-i_bow2kd'):
    require(assessment.get('format')=='attended-post-attempt-metadata/v1'
            and assessment.get('candidate')==CANDIDATE and assessment.get('identifier')==IDENTIFIER
            and assessment.get('prior_attempt')==prior_attempt
            and assessment.get('stable_metadata') is True,'retained-shell subject differs')
    namespaces=assessment['namespaces'];expected=roots(home)
    require(set(namespaces)==set(expected),'retained namespace set differs')
    for name,path in expected.items():
        row=namespaces[name];require(row['path']==str(path),'retained namespace path differs')
        if name not in ('WebKit','Caches'):
            require(row['present'] is False and row['metadata']==[],'operational/setup state is not absent')
    require(namespaces['WebKit']['present'] is True and len(namespaces['WebKit']['metadata'])==21
            and namespaces['Caches']['present'] is True and len(namespaces['Caches']['metadata'])==10,
            'retained browser shell shape differs')
    return namespaces


def check_snapshot(assessment,home,current,prior_attempt='app-attended-prepared-i_bow2kd'):
    expected=shape(assessment,home,prior_attempt)
    require(current==expected,'exact retained namespace metadata drift; preserve/reassess')
    return expected


def verify(path,expected_sha,executable):
    path=Path(path)
    version,prior_attempt=selected_profile(path,expected_sha)
    require(path.is_absolute() and path.resolve()==path,'retained assessment alias')
    parent=path.parent.lstat()
    require(stat.S_ISDIR(parent.st_mode) and parent.st_uid==os.getuid()
            and stat.S_IMODE(parent.st_mode)==0o700,'retained assessment parent not private0700')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        before=os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_uid==os.getuid() and before.st_nlink==1
                and stat.S_IMODE(before.st_mode)==0o600 and 0<before.st_size<=2*1024*1024,'retained assessment file invalid')
        raw=os.read(fd,2*1024*1024+1)
        require(len(raw)==before.st_size and hashlib.sha256(raw).hexdigest()==expected_sha,'retained assessment bytes differ')
        stamp=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_uid,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        require(stamp(before)==stamp(os.fstat(fd))==stamp(path.lstat()),'retained assessment changed')
    finally:os.close(fd)
    assessment=json.loads(raw);home=Path.home()
    current=metadata(home);check_snapshot(assessment,home,current,prior_attempt)
    files=[str(Path(value['path'])/row['relative']) for value in current.values()
           for row in value['metadata'] if stat.S_ISREG(row['mode'])]
    require(files,'retained opaque file metadata unavailable')
    observed=subprocess.run(['/usr/sbin/lsof','-nP','-F','pn','--',*files],capture_output=True,text=True,timeout=5)
    require(observed.returncode==1 and not observed.stdout.strip() and not observed.stderr.strip(),
            'current-user opaque file descriptor observation unavailable/nonquiescent')
    ps=subprocess.run(['/bin/ps','-axo','pid=,ppid=,comm='],capture_output=True,text=True,timeout=3)
    require(ps.returncode==0 and not any(executable in line for line in ps.stdout.splitlines()),
            'candidate process observed or census unavailable')
    check_snapshot(assessment,home,metadata(home),prior_attempt)
    return {'version':version,'assessment_path':str(path),'assessment_sha256':expected_sha,
        'namespaces':current,'listed_descriptors':0,'candidate_process_observed':False,
        'AppData':'absent','saved_A':None,'ledger':None,
        'limits':'Exact metadata only, no opaque contents/auth read. Current-user lsof/census are not atomic global exclusion, opaque-byte identity, checkpoint/corruption proof or supplier settlement.'}
