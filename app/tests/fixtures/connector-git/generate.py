"""Independent Python standard-library object oracle; no Git invocation."""
import hashlib, json, pathlib, zlib
result={}
for algorithm in ['sha1','sha256']:
    objects=[]
    def object(kind,data):
        full=kind.encode()+b' '+str(len(data)).encode()+b'\0'+data
        oid=hashlib.new(algorithm,full).hexdigest()
        objects.append(dict(kind=kind,oid=oid,hex=data.hex() if len(data)<4096 else None,compressed=zlib.compress(full).hex()))
        return oid
    old=object('blob','old\r\né\n'.encode());new=object('blob',b'new\n\n')
    def tree(blob):return object('tree',b'100644 literal [*].txt\0'+bytes.fromhex(blob))
    before=tree(old);after=tree(new)
    def commit(tree,parent,message):return object('commit',('tree '+tree+'\n'+('parent '+parent+'\n' if parent else '')+'author Fixture <fixture@example.invalid> 0 +0000\ncommitter Fixture <fixture@example.invalid> 0 +0000\n\n'+message+'\n').encode())
    since=commit(before,None,'since');at=commit(after,since,'at');same=commit(after,at,'same bytes different commit')
    cases={}
    def case(name,rawtree):cases[name]=commit(object('tree',rawtree),None,name)
    for name,mode in [('symlink','120000'),('gitlink','160000'),('executable','100755')]:
        case(name,mode.encode()+b' literal [*].txt\0'+bytes.fromhex(new))
    entry=b'100644 literal [*].txt\0'+bytes.fromhex(new)
    case('duplicate',entry+entry);case('truncated',entry[:-1]);case('malformed',b'not a tree')
    case('unicode',b'100644 '+ 'é.txt'.encode()+b'\0'+bytes.fromhex(new))
    case('nonutf8',b'100644 raw-\xff\0'+bytes.fromhex(new))
    for name,data in [('blob_max',b'x'*262144),('blob_over',b'x'*262145),('nul',b'x\0'),('encoding',b'\xff')]:
        cases[name]=commit(tree(object('blob',data)),None,name)
    header=('tree '+after+'\nauthor Fixture <fixture@example.invalid> 0 +0000\ncommitter Fixture <fixture@example.invalid> 0 +0000\n\n').encode()
    for name,size in [('commit_max',1048576),('commit_over',1048577)]:cases[name]=object('commit',header+b'x'*(size-len(header)))
    for name,size in [('tree_max',1048576),('tree_over',1048577)]:
        remaining=size-len(entry);count=(remaining+1023)//1024;chunks=[]
        for i in range(count):
            length=remaining//count+(i<remaining%count)
            prefix=('z%06d'%i).encode()
            chunks.append(b'100644 '+prefix+b'x'*(length-8-len(bytes.fromhex(new))-len(prefix))+b'\0'+bytes.fromhex(new))
        case(name,entry+b''.join(chunks))
    result[algorithm]=dict(objects=objects,at=at,since=since,same=same,old=old,new=new,cases=cases)
pathlib.Path(__file__).with_name('vectors.json').write_text(json.dumps(result,indent=2)+'\n')
