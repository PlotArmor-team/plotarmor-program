from pathlib import Path
import hashlib,subprocess
s=Path('/home/sucka/plotarmor-demo/.m2-pass4-scratch');p=s/'target/deploy/plotarmor.so';b=p.read_bytes();trim=b.rstrip(b'\0'); h=hashlib.sha256(trim).hexdigest()
print('Artifact:',p,'\nFull length:',len(b),'\nFull SHA256:',hashlib.sha256(b).hexdigest(),'\nTrim method: bytes.rstrip(b"\\0")\nTrimmed length:',len(trim),'\nTrimmed SHA256:',h)
expected='789f64d7a2f6ece13e600052877849a3fcb7d9b6637205bd997dd49dd43a4cf6'
print('Expected:',expected,'\nMATCH:',h==expected)
Path('/tmp/m2-pass4-independent/baseline.so').write_bytes(b)
for file in ['Cargo.lock','scripts/build.sh','rust-toolchain.toml','Anchor.toml','programs/plotarmor/src/instructions/sign_contract.rs']:
 orig=subprocess.check_output(['git','-C','/home/sucka/plotarmor-program','show','7c267e9:'+file]);local=(s/file).read_bytes();print(file,'equals exact commit:',local==orig,'sha256',hashlib.sha256(local).hexdigest());assert local==orig
print('SBF pin stamp:',(s/'target/.platform-tools-pin').read_text())
