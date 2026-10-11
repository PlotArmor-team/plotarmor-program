from pathlib import Path
import subprocess,hashlib,difflib
S=Path('/home/<usr>/plotarmor-demo/.m2-pass4-scratch');E=Path('/tmp/m2-pass4-independent');P=S/'programs/plotarmor/src/instructions/sign_contract.rs';T=S/'programs/plotarmor/tests/sign_contract_tests.rs'
def run(name,*cmd):
 return subprocess.call(['python3',str(E/'run.py'),name,str(S),*cmd])
original=P.read_text(); tests=T.read_text();baseline=(E/'baseline.so').read_bytes()
assert P.read_bytes()==subprocess.check_output(['git','-C','/home/<usr>/plotarmor-program','show','7c267e9:programs/plotarmor/src/instructions/sign_contract.rs'])
assert tests==subprocess.check_output(['git','-C','/home/<usr>/plotarmor-program','show','7c267e9:programs/plotarmor/tests/sign_contract_tests.rs'],text=True)
line='    require!(!ctx.accounts.registry_config.paused, PlotArmorError::Paused);\n'
assert original.count(line)==1
try:
 mutated=original.replace(line,'');P.write_text(mutated)
 diff=''.join(difflib.unified_diff(original.splitlines(True),mutated.splitlines(True),fromfile='7c267e9/sign_contract.rs',tofile='scratch-mutant/sign_contract.rs'))
 (E/'mutation.patch').write_text(diff);print(diff,flush=True)
 assert run('14_mutant_sbf_build','bash','scripts/build.sh','--','--locked','--offline')==0
 b=(S/'target/deploy/plotarmor.so').read_bytes(); print('MUTANT SO SHA256 trimmed:',hashlib.sha256(b.rstrip(b'\0')).hexdigest(),flush=True);assert b!=baseline
 rc=run('15_mutant_regression','cargo','test','--locked','--offline','--test','sign_contract_tests','paused_registry_rejects_sign_contract','--','--exact','--nocapture')
 assert rc==101,f'expected failing regression, got {rc}'
 out=(E/'logs/15_mutant_regression.txt').read_text()
 assert 'sign_contract must be rejected while the registry is paused' in out and 'FAILED' in out
 print('CONFIRMED mutation killed: regression reached expect_err but transaction succeeded.',flush=True)
finally:
 P.write_text(original)
assert run('16_restored_sbf_build','bash','scripts/build.sh','--','--locked','--offline')==0
assert (S/'target/deploy/plotarmor.so').read_bytes()==baseline
print('RESTORED SO byte-for-byte equals cold baseline; mutant overwritten.',flush=True)
assert run('17_restored_regression','cargo','test','--locked','--offline','--test','sign_contract_tests','paused_registry_rejects_sign_contract','--','--exact','--nocapture')==0
try:
 T.write_text(tests+(E/'scratch_extra_tests.rs').read_text())
 assert run('18_adversarial_tests','cargo','test','--locked','--offline','--test','sign_contract_tests','pass4_','--','--nocapture')==0
finally:
 T.write_text(tests)
print('RESTORED original scratch source and tests. Source repos never modified.',flush=True)
