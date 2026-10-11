from pathlib import Path
import re,json,subprocess,base64,hashlib
S=Path('/home/<usr>/plotarmor-demo/.m2-pass4-scratch');P=Path('/home/<usr>/plotarmor-program');D=Path('/home/<usr>/plotarmor-demo');K=Path('/home/<usr>/plotarmor-kora')
pattern=r'#\[account\(\s*seeds = \[b"config"\],\s*bump,\s*\)\]\s*pub registry_config: Account<\'info, RegistryConfig>,'
for p in sorted((S/'programs/plotarmor/src/instructions').glob('*.rs')):
 if p.stem=='init_registry_config': continue
 m=re.search(pattern,p.read_text());assert m,p
 print(p.name+':'+str(p.read_text()[:m.start()].count('\n')+1),repr(m.group()),'MATCH')
expected=['registry_config','contract_artifact','contract_signature','signer','system_program']
for p in [P/'target/idl/plotarmor.json',D/'src/anchor/plotarmor.json']:
 j=json.loads(p.read_text());ix=next(i for i in j['instructions'] if i['name']=='sign_contract');assert [a['name'] for a in ix['accounts']]==expected;print(p,'ORDER',expected)
 print('Paused error:',next(e for e in j['errors'] if e['name']=='Paused'))
print('Full IDLs JSON equality:',json.loads((P/'target/idl/plotarmor.json').read_text())==json.loads((D/'src/anchor/plotarmor.json').read_text()))
for repo in [S,D,K]:
 files=subprocess.check_output(['rg','--files','--hidden','-g','!.git','-g','!node_modules','-g','!target','-g','!evidence','-g','!.m2-pass4-scratch','-g','!dist',str(repo)],text=True).splitlines()
 count=0
 for name in files:
  p=Path(name)
  if p.suffix not in ['.ts','.tsx','.js','.mjs','.cjs','.rs']:continue
  txt=p.read_text()
  for m in re.finditer(r'\.signContract\s*\(',txt):
   count+=1;line=txt[:m.start()].count('\n')+1;chunk=txt[m.start():];a=re.search(r'\.accounts(?:Strict)?\(\{([\s\S]*?)\}\)',chunk);assert a,(p,line)
   keys=re.findall(r'^\s*(\w+)\s*(?::|,|$)',a.group(1),re.M)
   print(f'{p}:{line}: accounts={keys}');assert keys==['registryConfig','contractArtifact','contractSignature','signer','systemProgram']
 print(repo,'signContract builders:',count)
# Validate RPC response using fixed offsets of RegistryConfig's four Borsh fields.
raw=Path('/tmp/m2-pass4-independent/logs/08_devnet_config.txt').read_text();j=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0];a=j['account'];b=base64.b64decode(a['data'][0]);assert len(b)==44;assert a['owner']=='3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2';assert b[:8]==hashlib.sha256(b'account:RegistryConfig').digest()[:8]
print('DEVNET CONFIG verified owner, length, discriminator; schema_version=',b[40],'enabled_anchor_modes=',int.from_bytes(b[41:43],'little'),'paused=',b[43])
# Ensure all archived tracked files are still identical, ignoring generated target.
paths=subprocess.check_output(['git','-C',str(P),'ls-tree','-r','--name-only','7c267e9'],text=True).splitlines()
for p in paths: assert (S/p).read_bytes()==subprocess.check_output(['git','-C',str(P),'show','7c267e9:'+p]),p
print('All',len(paths),'archived tracked files restored byte-for-byte to 7c267e9.')
b=(S/'target/deploy/plotarmor.so').read_bytes();assert b==Path('/tmp/m2-pass4-independent/baseline.so').read_bytes()
for term in [b'UNSET-PLACEHOLDER-DO-NOT-DEPLOY@example.invalid',b'UNSET-PLACEHOLDER-DO-NOT-DEPLOY']:
 print('COLD ARTIFACT placeholder:',term.decode(),'offset=',b.find(term));assert term in b
print('Source repositories statuses:')
for r in [P,D,K]:print(r,subprocess.check_output(['git','-C',str(r),'status','--short'],text=True))
