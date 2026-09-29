from pathlib import Path
import subprocess,json,re,hashlib
P=Path('/home/sucka/plotarmor-program');D=Path('/home/sucka/plotarmor-demo');K=Path('/home/sucka/plotarmor-kora');S=D/'.m2-pass4-scratch'
def quote(p,start=1,end=None):
 lines=p.read_text().splitlines();print('\nFILE:',p)
 for n,line in enumerate(lines,1):
  if n>=start and (end is None or n<=end):print(f'{n}: {line}')
for p in sorted((S/'programs/plotarmor/src/instructions').glob('*.rs')):quote(p)
for p in ['programs/plotarmor/src/state.rs','programs/plotarmor/src/error.rs','programs/plotarmor/src/lib.rs','programs/plotarmor/tests/common/mod.rs']:quote(S/p)
quote(S/'programs/plotarmor/tests/sign_contract_tests.rs',382)
for pattern,a,b in [('anchor-lang-1.0.1/src/accounts/account.rs',280,340),('anchor-attribute-account-1.0.1/src/lib.rs',140,230),('anchor-syn-1.0.1/src/codegen/accounts/constraints.rs',1130,1230)]:
 for p in Path('/home/sucka/.cargo/registry/src').glob('*/'+pattern):quote(p,a,b)
print('\nIDL SIGN_CONTRACT:')
for p in [P/'target/idl/plotarmor.json',D/'src/anchor/plotarmor.json']:
 j=json.loads(p.read_text());ix=next(i for i in j['instructions'] if i['name']=='sign_contract');print(p, json.dumps(ix,indent=2));quote(p, next(n for n,l in enumerate(p.read_text().splitlines(),1) if '"sign_contract"' in l), None if False else next(n for n,l in enumerate(p.read_text().splitlines(),1) if '"sign_contract"' in l)+85)
print('IDL exact equality:',(P/'target/idl/plotarmor.json').read_bytes()==(D/'src/anchor/plotarmor.json').read_bytes())
print('\nCALL SITE SEARCH:')
for repo in [P,D,K]:
 cmd=['rg','-n','--hidden','-g','!.git','-g','!node_modules','-g','!target','-g','!evidence','-g','!.m2-pass4-scratch','-g','!dist','signContract|sign_contract|83, *120, *194, *61|registryConfig',str(repo)]
 r=subprocess.run(cmd,text=True,capture_output=True);print('ARGV',cmd,'\n',r.stdout,'EXIT',r.returncode)
quote(D/'src/ContractsApp.tsx',1170,1215)
print('\nDEMO d9da574:')
print(subprocess.check_output(['git','-C',str(D),'show','--stat','d9da574'],text=True))
for ref in ['d9da574','HEAD','main','origin/main','feat/wallet-bindings','origin/feat/wallet-bindings']:
 print('\nREF',ref)
 for name in ['src/ContractsApp.tsx','src/anchor/plotarmor.json']:
  r=subprocess.run(['git','-C',str(D),'show',ref+':'+name],capture_output=True,text=True)
  if r.returncode: print(r.stderr);continue
  if name.endswith('json'):print([a['name'] for a in next(i for i in json.loads(r.stdout)['instructions'] if i['name']=='sign_contract')['accounts']])
  else:
   lines=r.stdout.splitlines()
   for n,l in enumerate(lines):
    if '.signContract(' in l:
     for m in range(max(0,n-6),n+10):print(f'{ref}:{name}:{m+1}: {lines[m]}')
