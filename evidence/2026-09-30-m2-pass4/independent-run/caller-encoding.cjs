const fs = require('node:fs');
const assert = require('node:assert/strict');
const {createRequire} = require('node:module');
const req=createRequire('/home/sucka/plotarmor-demo/package.json');
const {Program}=req('@coral-xyz/anchor');
const {PublicKey,Connection,SystemProgram}=req('@solana/web3.js');
const {execFileSync}=require('node:child_process');
(async()=>{
 const programId=new PublicKey('3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2');
 const raw=Buffer.alloc(32,61),signer=new PublicKey(Buffer.alloc(32,42));
 const pda=(...s)=>PublicKey.findProgramAddressSync(s,programId)[0];
 const registryConfig=pda(Buffer.from('config'));
 const contractArtifact=pda(Buffer.from('contract_artifact'),raw);
 const contractSignature=pda(Buffer.from('signature'),contractArtifact.toBuffer(),signer.toBuffer());
 const accounts={registryConfig,contractArtifact,contractSignature,signer,systemProgram:SystemProgram.programId};
 const expected=Object.values(accounts).map(k=>k.toBase58());
 const variants=[['program target',fs.readFileSync('/home/sucka/plotarmor-program/target/idl/plotarmor.json','utf8')],['demo current',fs.readFileSync('/home/sucka/plotarmor-demo/src/anchor/plotarmor.json','utf8')],['demo d9da574',execFileSync('git',['-C','/home/sucka/plotarmor-demo','show','d9da574:src/anchor/plotarmor.json'],{encoding:'utf8'})]];
 for(const [name,text] of variants){
  const idl=JSON.parse(text); const program=new Program(idl,{connection:new Connection('http://127.0.0.1:8899')});
  const ix=await program.methods.signContract([...raw]).accountsStrict(accounts).instruction();
  assert.deepEqual(ix.keys.map(k=>k.pubkey.toBase58()),expected);
  assert.deepEqual(ix.keys.map(k=>[k.isWritable,k.isSigner]),[[false,false],[false,false],[true,false],[true,true],[false,false]]);
  assert.equal(ix.data.length,40);
  console.log(name,JSON.stringify({keys:ix.keys.map((k,i)=>({name:Object.keys(accounts)[i],pubkey:k.pubkey.toBase58(),writable:k.isWritable,signer:k.isSigner})),data:ix.data.toString('hex')}));
 }
 console.log('PASS: all 3 independently encode the five-account order and exact flags. No RPC requests, wallet, signing, or broadcast.');
})().catch(e=>{console.error(e);process.exit(1)});
