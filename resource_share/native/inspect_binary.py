"""Read-only PE inspection; reproduces upstream call heuristics, not gameplay validation."""
import sys,pathlib,struct,collections,json,bisect
root=pathlib.Path(__file__).resolve().parents[1]
# Read PE32+ sections and exception directory without third-party packages.
exe=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(r'E:\SteamLibrary\steamapps\common\Palworld\Pal\Binaries\Win64\Palworld-Win64-Shipping.exe')
raw=exe.read_bytes();nt=struct.unpack_from('<I',raw,0x3c)[0];assert raw[nt:nt+4]==b'PE\0\0'
nsec=struct.unpack_from('<H',raw,nt+6)[0];opt=nt+24
assert struct.unpack_from('<H',raw,opt)[0]==0x20b
base=struct.unpack_from('<Q',raw,opt+24)[0];size=struct.unpack_from('<I',raw,opt+56)[0]
mem=bytearray(size);headers=struct.unpack_from('<I',raw,opt+60)[0];mem[:headers]=raw[:headers]
sec=opt+struct.unpack_from('<H',raw,nt+20)[0]
for i in range(nsec):
 off=sec+i*40;name=raw[off:off+8].rstrip(b'\0');vsize,rva,rsize,rptr=struct.unpack_from('<IIII',raw,off+8)
 mem[rva:rva+rsize]=raw[rptr:rptr+rsize]
 if name==b'.text':lo,hi=rva,rva+vsize
pdata,psize=struct.unpack_from('<II',raw,opt+112+3*8)
spans=sorted((a,b) for a,b,_ in struct.iter_unpack('<III',mem[pdata:pdata+psize]) if a<b);starts=[a for a,b in spans]
def span(rva):
 i=bisect.bisect_right(starts,rva)-1
 return spans[i] if i>=0 and spans[i][0]<=rva<spans[i][1] else (0,0)
def calls(rva):
 a,b=span(rva);p=a;result=[]
 while p<b:
  p=mem.find(b'\xe8',p,b)
  if p<0 or p+5>b:break
  d=p+5+struct.unpack_from('<i',mem,p+1)[0]
  if lo<=d<hi and d not in result:result.append(d)
  p+=1
 return result
refs=collections.Counter();p=lo
while True:
 p=mem.find(b'\xe8',p,hi-4)
 if p<0:break
 d=p+5+struct.unpack_from('<i',mem,p+1)[0]
 if lo<=d<hi:refs[d]+=1
 p+=1
names=['OnReadyModuleItemStackInfo','GetItemStackCount64','GetBaseCampModelBelongTo','CountLocalPlayerInsideBaseCampItemNum64','CollectLocalPlayerControllableItemInfos']
result={}
for name in names:
 entries=[];p=0
 while True:
  p=mem.find(name.encode()+b'\0',p)
  if p<0:break
  ptr=struct.pack('<Q',base+p);j=0
  while True:
   j=mem.find(ptr,j)
   if j<0:break
   fn=struct.unpack_from('<Q',mem,j+8)[0]-base
   if lo<=fn<hi:
    entries.append({'table':hex(j),'exec':hex(fn),'calls':[(hex(c),refs[c]) for c in calls(fn)]})
   j+=1
  p+=1
 result[name]=entries
print(json.dumps(result,indent=2));(root/'build/native-sites.json').write_text(json.dumps(result,indent=2))

# Offline reproduction of the authority resolver; addresses are observations, never patch constants.
def unique(values):
 values=list(set(values));return values[0] if len(values)==1 else 0
def least(fn,minimum):
 cs=[c for c in calls(fn) if refs[c]>=minimum]
 return unique(c for c in cs if refs[c]==min(refs[v] for v in cs)) if cs else 0
stacks=[];camps=[];helpers=[]
for e in result['GetItemStackCount64']:
 hit=unique(c for c in calls(int(e['exec'],16)) if refs[c]==1)
 if hit:stacks.append(hit)
for e in result['GetBaseCampModelBelongTo']:
 hit=unique(c for c in calls(int(e['exec'],16)) if 1<=refs[c]<=500)
 if hit:camps.append(hit)
for e in result['CountLocalPlayerInsideBaseCampItemNum64']:
 hit=unique(c for c in calls(int(e['exec'],16)) if refs[c]==1)
 if hit:helpers.append(hit)
get_ids=unique(least(h,2) for h in helpers)
parents=set();p=lo
while True:
 p=mem.find(b'\xe8',p,hi-4)
 if p<0:break
 if p+5+struct.unpack_from('<i',mem,p+1)[0]==get_ids:
  a,b=span(p)
  if a:parents.add(a)
 p+=1
consume=unique(c for parent in parents for c in calls(parent) if c!=get_ids and refs[c]==2)
sites={'containers':get_ids,'camp':unique(camps),'consume':consume,'stack':unique(stacks)}
print('Authority resolver:',{k:hex(v) for k,v in sites.items()})
assert all(sites.values()),'Unresolved or ambiguous authority hook'
