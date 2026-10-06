# Cutover rehearsal on a local validator (2026-10-06)

Rehearses docs/CUTOVER_2026-10.md, program 09c5bfc -> f34bfae, against a local
`solana-test-validator` seeded from devnet. NOTHING was sent to devnet. All writes went to
`http://127.0.0.1:8899`. Not committed.

Verification label per fact: [cmd] command output below, [inferred] reasoned. This rehearsal is
verification pass 2 of 4 for the cutover plan (pass 1 was the read-only on-chain/IDL/size work in
the prior session). It is a rehearsal on a different cluster, so it does not count as a live
devnet check. Pass count for the cutover: 2 of 4, pending the actual devnet run.

Local key: `~/.config/solana/id.json` is the real upgrade authority
(EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd). The authority account was cloned from devnet so it
exists locally with its devnet balance. The key file contents were never printed; only its path
appears in commands, and that path is already in the committed runbook. The validator's genesis
mint is a throwaway keypair, so it does not collide with the cloned authority account.

## Setup

Validator command (as run by a wrapper script; the 11 `--clone` addresses are one account per
account discriminator, listed in the census below):

```
solana-test-validator --reset --ledger ~/.cache/pa-rehearsal-ledger --url devnet \
  --clone-feature-set --mint <throwaway pubkey> \
  --clone-upgradeable-program 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 \
  --clone EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd \
  --clone <11 accounts> --bind-address 127.0.0.1 --rpc-port 8899
```

`--clone-feature-set` copies devnet's activated feature set, so feature gates match devnet as of
the clone. `--url devnet` is the public moniker, no API key involved.

Census of the 617 program accounts on devnet (getProgramAccounts, 8-byte dataSlice, public
devnet RPC), one account cloned per discriminator [cmd]:

| account type | discriminator | count on devnet | cloned account |
|---|---|---|---|
| AnchorRecord | 12718e0d6582cfdf | 145 | 1aAF123RsFRKBhUb2YjnYbezp5JmPrN6dFjuxR9GrJE |
| ClaimArtifactLink | ec0a24d1a4a79c45 | 94 | AfFLNFjgfuyKofq7W9rzozQAYZxiya6k8Y3FChxDoek |
| OwnerRecord | 05241145f6ec53a6 | 76 | 6oGyQzMJTmJTkTHKNZRrTSoSDBX849X3KfDHTsEQEdT |
| ContentArtifact | 5db8d72df4ad9365 | 73 | G1Tz5cydp1BbwgmsjKagAT8dqkSesc5Pxt9tfLRNigs |
| Ownership | 295465ce91af5841 | 61 | 7KS6W9sTcs91vxV9hFtfFxcoEJYCW511RCMook9f6YL |
| WorkClaim | 95e36cbe7025be2f | 61 | fcT9HJWSCgU6co6K2ic2qxVThxXhc8EPAngP99mwq16 |
| ContractArtifact | 1e25f211cc0de7d0 | 51 | RSsyr3F4yedFMiJpWxoYCxXqFHZefE3K1SkdweBFg4y |
| EvidenceAnchor | c2efdd0125861640 | 35 | NL3NCKwXJQLdc7ZiUkfLTy3kreBcyngHDaVsZbf9TZz |
| AuthorizedContractAnchor | 24dbbac078ec652e | 16 | zJooXbNk9AAwpavokVMbnyp6msk97kVtSaqSfnxEf9U |
| ContractSignature | a561926950e45741 | 4 | 3u1a1KEYrdAdpqTE5Ao1R5nZnQaBWSDxeQAfqbTgE1HS |
| RegistryConfig | 17760af6ade7f39c | 1 | BpsMTsw9uxmmgmy1iVjgwaLfoyKMGuoisyBQ8sTrxvmG |

Names were matched by sha256("account:<Name>")[0..8] against the 11 discriminators; all 11
matched, none unknown. [cmd]

## Probe on a discarded ledger: does a 480-byte extend work?

Run first on a throwaway ledger (reset afterwards, so it does not affect the rehearsal below).
The validator carried devnet's cloned feature set. Output [cmd]:

```
$ solana program extend 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 480 -u http://127.0.0.1:8899 --keypair ~/.config/solana/id.json
Extended Program Id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 by 480 bytes
[exit 0]
Data Length: 472440
```

So a 480-byte extend is ACCEPTED by this local Agave 4.0.1 validator. That does not show devnet
accepts it: devnet's validator version is unknown here, and the loader interface 6.1.1 in
Cargo.lock documents a 10 KiB minimum once SIMD-0431 is active. The runbook keeps +10,240.
[inferred]

## Rehearsal log (every command and its output)

Commands below were run through a wrapper that appends the command and its output verbatim to
this file. Any `api-key=` value is replaced with REDACTED by the wrapper. Output is verbatim,
so it includes three em-dashes inside the adversarial script's own PASS lines; they are not
prose written for this file.
### Step 0 pre-checks (runbook commands with -u http://127.0.0.1:8899 in place of -u devnet)

```
$ git rev-parse HEAD; git status --short; sha256sum target/deploy/plotarmor.so; ls -l target/deploy/plotarmor.so
1e1771f8eaf26f91ff9acfc574987230b59a3508
?? docs/evidence/
97880b057e52f474f20bb209f586e708eaf96d5608bcc52403ca62bc396916b7  target/deploy/plotarmor.so
-rwxr-xr-x 1 sucka sucka 472440 Oct  6 14:23 target/deploy/plotarmor.so
[exit 0]
```

```
$ solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u http://127.0.0.1:8899

Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL
Authority: EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
Last Deployed In Slot: 0
Data Length: 471960 (0x73398) bytes
Balance: 3.28604568 SOL
[exit 0]
```

```
$ solana address -k ~/.config/solana/id.json; solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899
EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
5.400565851 SOL
[exit 0]
```

```
$ solana rent 472005 -u http://127.0.0.1:8899; solana rent 482245 -u http://127.0.0.1:8899; solana rent 472477 -u http://127.0.0.1:8899; echo "--- devnet for comparison:"; solana rent 472005 -u devnet; solana rent 482245 -u devnet; solana rent 472477 -u devnet
Rent-exempt minimum: 3.28604568 SOL

Rent-exempt minimum: 3.35731608 SOL

Rent-exempt minimum: 3.2893308 SOL

--- devnet for comparison:
Rent-exempt minimum: 2.39843564 SOL

Rent-exempt minimum: 2.45045484 SOL

Rent-exempt minimum: 2.4008334 SOL
[exit 0]
```
### Before upgrade: new-account-list sign_contract against the OLD program (expected to FAIL; this is the cutover window)

```
$ DEVNET_RPC_URL=http://127.0.0.1:8899 timeout 300 node_modules/.bin/ts-node --transpile-only scripts/devnet_sign_contract_test.ts 2>&1 | tail -n 25 | cut -c1-300
    at translateError (/home/sucka/plotarmor-program/node_modules/@coral-xyz/anchor/src/error.ts:277:35)
    at MethodsBuilder.rpc [as _rpcFn] (/home/sucka/plotarmor-program/node_modules/@coral-xyz/anchor/src/program/namespace/rpc.ts:35:29)
    at processTicksAndRejections (node:internal/process/task_queues:105:5) {
  errorLogs: [
    'Program log: AnchorError caused by account: contract_artifact. Error Code: AccountDiscriminatorMismatch. Error Number: 3002. Error Message: Account discriminator did not match what was expected.'
  ],
  logs: [
    'Program 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 invoke [1]',
    'Program log: Instruction: SignContract',
    'Program log: AnchorError caused by account: contract_artifact. Error Code: AccountDiscriminatorMismatch. Error Number: 3002. Error Message: Account discriminator did not match what was expected.',
    'Program 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 consumed 3574 of 200000 compute units',
    'Program 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 failed: custom program error: 0xbba'
  ],
  error: {
    errorCode: { code: 'AccountDiscriminatorMismatch', number: 3002 },
    errorMessage: 'Account discriminator did not match what was expected',
    comparedValues: undefined,
    origin: 'contract_artifact'
  },
  _programErrorStack: ProgramErrorStack {
    stack: [
      [PublicKey [PublicKey(3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2)]]
    ]
  }
}
[exit 0]
```
### Step 2a: extend (balance in lamports before and after)

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana account Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL -u http://127.0.0.1:8899 --output json | python3 -I -c 'import sys,json,base64;a=json.load(sys.stdin)["account"];print("ProgramData lamports",a["lamports"],"data_len",len(base64.b64decode(a["data"][0])))'
5396189971 lamports
ProgramData lamports 3286045680 data_len 472005
[exit 0]
```

```
$ solana program extend 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 10240 -u http://127.0.0.1:8899

Extended Program Id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 by 10240 bytes
[exit 0]
```

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u http://127.0.0.1:8899; solana account Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL -u http://127.0.0.1:8899 --output json | python3 -I -c 'import sys,json,base64;a=json.load(sys.stdin)["account"];print("ProgramData lamports",a["lamports"],"data_len",len(base64.b64decode(a["data"][0])))'
5324914571 lamports

Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL
Authority: EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
Last Deployed In Slot: 120
Data Length: 482200 (0x75b98) bytes
Balance: 3.35731608 SOL

ProgramData lamports 3357316080 data_len 482245
[exit 0]
```
### Step 2b: deploy (upgrade) with --no-auto-extend

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports
5324914571 lamports
[exit 0]
```

```
$ solana program deploy target/deploy/plotarmor.so --program-id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 --upgrade-authority ~/.config/solana/id.json --no-auto-extend -u http://127.0.0.1:8899
Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2

Signature: 2w5jG8n8bgo3JWZnAnxDSJEAsHso3LXvvQQ7KbC63tu9ffJgPXf4pTjBZxJ43bpWNevhV1C9MxsWaFx5REjCS2u7
[exit 0]
```
### After upgrade

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u http://127.0.0.1:8899; solana account Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL -u http://127.0.0.1:8899 --output json | python3 -I -c 'import sys,json,base64;a=json.load(sys.stdin)["account"];print("ProgramData lamports",a["lamports"],"data_len",len(base64.b64decode(a["data"][0])))'
5322564571 lamports

Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL
Authority: EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
Last Deployed In Slot: 163
Data Length: 482200 (0x75b98) bytes
Balance: 3.35731608 SOL

ProgramData lamports 3357316080 data_len 482245
[exit 0]
```
### Post-upgrade byte check and security.txt (parsed from the dumped upgraded program)

```
$ solana program dump 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/post.so -u http://127.0.0.1:8899 && python3 -I /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/verify_bytes.py /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/post.so
Wrote program to /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/post.so
dump length 482200 trimmed 472425
trimmed sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
expected       bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
begin marker at 421297 end marker at 421653
  name = PlotArmor
  project_url = https://plotarmor.io
  contacts = email:info@plotarmor.io
  policy = Please report security issues privately to info@plotarmor.io. We acknowledge reports within 5 business days. Do not test against accounts or data you do not own. This program runs on Solana devnet as a demo MVP.
  source_code = private
[exit 0]
```
### Post-check: register_work_claim (scripts/devnet_register_test.ts, pointed at localnet)

```
$ DEVNET_RPC_URL=http://127.0.0.1:8899 timeout 300 node_modules/.bin/ts-node --transpile-only scripts/devnet_register_test.ts 2>&1 | tail -n 40 | cut -c1-250
  ContentArtifact:  6PonvVtFvh2UtKVtVEFUa6hmTABBY8FPcpzfa2ozDU2L
  WorkClaim:        BL7BnLyW1WCCBS8RacLkwQ5k1iNG1KixaRQYRuE1rivb
  Ownership:        8giU1QYfrSYP5V1EyNiMtJQftJ393iQ6pvoB1rw82fAe
  OwnerRecord:      NWgFGDWjjThCgyCMPjZyp5dMeKLsuYZZs54GTdnxrdf
  ClaimArtifactLink: 3w4g99VWw8Na6WjB3bWw7jR4aH3iGxreARcLdd2iYn3P
  AnchorRecord:     AStZqv8Dhs3k2JteKjUTzZKMJCfPdhoYDTU1Asrg4qa5
  raw_hash (hex):   d3fbba5c01964d0e23fafd4e7ee355b7c3a0cd8787a21db35a36eeb309c408e8

Submitting register_work_claim transaction to devnet...

✓ Transaction confirmed in 256 ms
✓ Signature: 3apXdA7bGp46dEf8W3e6BU3jndHiCaFzLTpHimKAZJ9G1YSs4itne6t97HedHMkYaKQqjLjWNbcZ1AhstHgqUicx
✓ Explorer: https://explorer.solana.com/tx/3apXdA7bGp46dEf8W3e6BU3jndHiCaFzLTpHimKAZJ9G1YSs4itne6t97HedHMkYaKQqjLjWNbcZ1AhstHgqUicx?cluster=devnet

Verifying on-chain state...
✓ WorkClaim fetched from chain:
    root_artifact: 6PonvVtFvh2UtKVtVEFUa6hmTABBY8FPcpzfa2ozDU2L
    claimant:      EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
    claim_kind:    1
✓ AnchorRecord fetched from chain:
    anchor_mode:   1
    anchored_object_kind: 0
    external_ref_hash (on-chain): 5dd79657af90d86ac5a8663ab99f45d4f77eb00076209852fdce966b2a52ce16
    matches submitted value:      ✓ YES

================================================
RESULT: Step A proof SUCCESSFUL
================================================

Real data for reference:
{
  "tx_signature": "3apXdA7bGp46dEf8W3e6BU3jndHiCaFzLTpHimKAZJ9G1YSs4itne6t97HedHMkYaKQqjLjWNbcZ1AhstHgqUicx",
  "tx_signature_length": 88,
  "content_artifact_pda": "6PonvVtFvh2UtKVtVEFUa6hmTABBY8FPcpzfa2ozDU2L",
  "work_claim_pda": "BL7BnLyW1WCCBS8RacLkwQ5k1iNG1KixaRQYRuE1rivb",
  "anchor_record_pda": "AStZqv8Dhs3k2JteKjUTzZKMJCfPdhoYDTU1Asrg4qa5",
  "anchor_mode": 1,
  "external_ref_hash": "5dd79657af90d86ac5a8663ab99f45d4f77eb00076209852fdce966b2a52ce16",
  "raw_hash": "d3fbba5c01964d0e23fafd4e7ee355b7c3a0cd8787a21db35a36eeb309c408e8"
}
[exit 0]
```

NOTE: the scripts print "devnet" and explorer links with `cluster=devnet`. Every signature in this
file was produced on the LOCAL validator at 127.0.0.1:8899 and does not exist on devnet.

### Post-check: sign_contract (new account list)

```
$ DEVNET_RPC_URL=http://127.0.0.1:8899 timeout 300 node_modules/.bin/ts-node --transpile-only scripts/devnet_sign_contract_test.ts 2>&1 | tail -n 40 | cut -c1-250
Verifying on-chain state via raw getAccountInfo...
✓ Account exists on-chain
  owner: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2
  lamports: 1733040
  data length: 121 (expect 121)

Decoded fields (raw bytes, independent of Anchor client):
  contract_artifact: BbyxbsJSoad6GDmzu18PqsBDWYotM6GWzs7bzTV3GhUq
  signer:            EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
  content_hash:      bf5ead64bccfec2f1cd4cac564f69572ba00ba8afd6b7d383cb018059b8a27ab
  signed_at:         1791295676 2026-10-06T14:07:56.000Z
  slot:              238
  bump:              254

Checks:
  owner == program ID:             ✓ YES
  contract_artifact matches:       ✓ YES
  signer matches:                  ✓ YES
  content_hash matches submitted:  ✓ YES
  signed_at is plausible (>0):     ✓ YES
  slot is plausible (>0):          ✓ YES

================================================
RESULT: Devnet sign_contract proof SUCCESSFUL
================================================

Real data for reference:
{
  "upgrade_note": "verified against program 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 after devnet upgrade",
  "evidence_tx": "4YoVCeBk9phybNwCNuuQbHB4NRWjghfHwDLJh8bURnrVhiEqQrazE5kJXeTY95YcmoLmntDJG2RjbTGWqibxXBEB",
  "sign_tx": "293rNppVM3MbG2SnuNLtpLx38pZmFnjAZtacaTNr2MFxJ1n97QNnSNhgrhsx4iQPfjrDebYN1aMY1dDs9RhpSJ8p",
  "contract_artifact_pda": "BbyxbsJSoad6GDmzu18PqsBDWYotM6GWzs7bzTV3GhUq",
  "contract_signature_pda": "HcGgtAPZXJHiZfik91HurFNS7iP17Z2SyzjB3jUKiTbc",
  "raw_contract_hash": "bf5ead64bccfec2f1cd4cac564f69572ba00ba8afd6b7d383cb018059b8a27ab",
  "signed_at": "1791295676",
  "slot": "238",
  "sign_contract_cost_lamports": 1738040,
  "sign_contract_cost_sol": 0.00173804,
  "sign_contract_cost_usd_at_90": 0.1564236
}
[exit 0]
```
### Post-check: sign_contract adversarial (scripts/devnet_sign_contract_adversarial_test.ts)

```
$ DEVNET_RPC_URL=http://127.0.0.1:8899 timeout 300 node_modules/.bin/ts-node --transpile-only scripts/devnet_sign_contract_adversarial_test.ts 2>&1 | tail -n 45 | cut -c1-250
Signer: EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
Signer balance: 5.3067 SOL

Fixture setup: anchor_evidence_contract (create ContractArtifact)...
  ContractArtifact: 5e3aBCQEVySx9WeFMhZXUHd2PjVK5cKX51ZjR4kMbdXH
  tx: 5pBe3t46tVsfVLaN1wq5HeZbQdtZu4khLYXPSQNuqpiVq2ev442EfwCU2mZwpStpmwhhXyyTgR8X3QB6pjNQ6MDo
PASS  sign_contract — wrong content_hash (expect ContentHashMismatch 6011)
  first sign tx: 5Xnw7fzCaJLHkNj1V6mMQs3BCkgQTnK9wQmcfGuiDbwAaPBiYvdEwZJozY5dSezbChBPTqjW86EGFoSHRZsnfwVV
PASS  sign_contract — double-sign by same signer (expect already-in-use)
PASS  sign_contract — nonexistent ContractArtifact (expect account-validation failure)

==================================================
Results: 3 passed, 0 failed
ALL GREEN
[exit 0]
```
### Post-check: deserialize the 11 cloned accounts with the NEW IDL (target/idl/plotarmor.json)

```
$ NODE_PATH=$HOME/plotarmor-program/node_modules node_modules/.bin/ts-node --transpile-only --compiler-options '{"module":"commonjs","esModuleInterop":true}' /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/deser.ts /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/clones.json 2>&1 | cut -c1-330
OK   AnchorRecord               1aAF123RsFRKBhUb2YjnYbezp5JmPrN6dFjuxR9GrJE {"anchoredObject":"YxwaHa1bpJXysDXwJ9Ty2yDBvThAuZYwjq5a8VN4qnW","anchoredObjectKind":2,"anchorMode":1,"createdAt":"1784063650","externalRefHash":"[32 items]"}
OK   ClaimArtifactLink          AfFLNFjgfuyKofq7W9rzozQAYZxiya6k8Y3FChxDoek {"workClaim":"97Ye6jq5WHfrVGDL8X8fz1jjzgGQHoSA3mzAS1cLD8j4","contentArtifact":"6zpCKWVZfcsnc2LUuctYt6w4hniifGnFKEaXBdBjRKVb","previousLink":"Gk2KNMZr7cvYjvR6TBSoHNFUK8ajLW1XodvtELnEWaWM","createdAt":"1781621847"}
OK   OwnerRecord                6oGyQzMJTmJTkTHKNZRrTSoSDBX849X3KfDHTsEQEdT {"ownership":"J6bwjwMuFg1eQFvwSAab1sy5AL8SRW27f9VcQFQGHqUx","owner":"9VkT9u8vkVDM7mopqUi1Md8JwH698v7QcYYM9GBJf8Qf","share":30,"role":1}
OK   ContentArtifact            G1Tz5cydp1BbwgmsjKagAT8dqkSesc5Pxt9tfLRNigs {"isInitialized":true,"rawHash":"[32 items]","contentKind":2,"createdAt":"1785170352"}
OK   Ownership                  7KS6W9sTcs91vxV9hFtfFxcoEJYCW511RCMook9f6YL {"workClaim":"6w1UTFrUsM6hQBHDDud4sSg36iALGsMdmt2HdM3RRgCz","totalShares":100,"thresholdShares":100,"admin":"CHnCUvzZ7yrBkQCpnG6Y6XXqP6F1ahZM1nWH5spuX7z5","rulesVersion":0,"privacyMode":0,"commitmentRoot":"[32 items]"}
OK   WorkClaim                  fcT9HJWSCgU6co6K2ic2qxVThxXhc8EPAngP99mwq16 {"rootArtifact":"8A9vYTp7odtEZPsRtLj55iAgLm1Wy7FZ5jTW6VZ7RRkM","latestArtifact":"8A9vYTp7odtEZPsRtLj55iAgLm1Wy7FZ5jTW6VZ7RRkM","latestLink":"khZKQWP9h7aRS2Ra8rYqu96K4rJvGji3KJFNaFf5MpR","claimant":"4p5u6WvMN6BEc8jNmvBMiao1bG1gdJ4U
OK   ContractArtifact           RSsyr3F4yedFMiJpWxoYCxXqFHZefE3K1SkdweBFg4y {"isInitialized":true,"rawHash":"[32 items]","contentKind":1,"createdAt":"1782403482"}
OK   EvidenceAnchor             NL3NCKwXJQLdc7ZiUkfLTy3kreBcyngHDaVsZbf9TZz {"anchorer":"EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd","contractArtifact":"RSsyr3F4yedFMiJpWxoYCxXqFHZefE3K1SkdweBFg4y","assertedWorkClaim":"5m5aFvPtYfoPFbxFaMVBoQLPj8FMXDfvSaAMGGQXwpXr","timestamp":"1782403482"}
OK   AuthorizedContractAnchor   zJooXbNk9AAwpavokVMbnyp6msk97kVtSaqSfnxEf9U {"workClaim":"34PQCZsPRxAv65z49BkJuzcftTFprkcUrkbhgCAEWn73","contractArtifact":"7BbXVyqnnnfx3o3vBzDVx8oNTNxc9pbKkwSWBzpKpNnX","timestamp":"1781279453"}
OK   ContractSignature          3u1a1KEYrdAdpqTE5Ao1R5nZnQaBWSDxeQAfqbTgE1HS {"contractArtifact":"6urRYr3c7kdDGK3tQtMwf4nhTFghrY5AFLKPbzGvnCn6","signer":"EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd","contentHash":"[32 items]","signedAt":"1784750146","slot":"478159900","bump":255}
OK   RegistryConfig             BpsMTsw9uxmmgmy1iVjgwaLfoyKMGuoisyBQ8sTrxvmG {"authority":"EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd","schemaVersion":1,"enabledAnchorModes":0,"paused":false}
deserialized ok: 11 failed: 0
[exit 0]
```
### Rent observation (devnet, not local): rent for a 121-byte ContractSignature now vs the 2026-07-22 measurement

```
$ solana rent 121 -u devnet; solana rent 121 -u http://127.0.0.1:8899; python3 -I -c "print((128+121)*5080,(128+121)*6960)"
Rent-exempt minimum: 0.00126492 SOL

Rent-exempt minimum: 0.00173304 SOL

1264920 1733040
[exit 0]
```

### Addendum: spill mechanism check (NOT part of the runbook)

Local ProgramData ended the main run exactly at its local rent minimum, so no spill was visible.
To exercise the loader's spill path, 835,590,840 lamports (the excess the devnet numbers predict:
3,286,045,680 held - 2,450,454,840 required at 482,245 bytes) are transferred into ProgramData,
then the same binary is upgraded again. Expect ProgramData to drop back to its minimum and the
excess plus the buffer rent to return to the authority, leaving only fees spent.

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana transfer Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL 0.83559084 --allow-unfunded-recipient -u http://127.0.0.1:8899; solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana account Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL -u http://127.0.0.1:8899 --output json | python3 -I -c 'import sys,json;print("ProgramData lamports",json.load(sys.stdin)["account"]["lamports"])'
5300539011 lamports

Signature: 4rneh9tw763B6jfUQJbGpHrDxju2LrGGNQugyMsJfqd7pu6zAojwsMRJ5PYz9B29VPFWNzjptaysvzqgzCWTBxN1

4464943171 lamports
ProgramData lamports 4192906920
[exit 0]
```

```
$ solana program deploy target/deploy/plotarmor.so --program-id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 --upgrade-authority ~/.config/solana/id.json --no-auto-extend -u http://127.0.0.1:8899
Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2

Signature: 4g3J7qGnqjxyMVfKPmskKW8nHGZP8AsgcBzeZJy7fcmowpvuERwk8XHMX8KTVZH19CaCNEsx5VjuvFBorvEpJ6yg
[exit 0]
```

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana account Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL -u http://127.0.0.1:8899 --output json | python3 -I -c 'import sys,json;print("ProgramData lamports",json.load(sys.stdin)["account"]["lamports"])'
5298184011 lamports
ProgramData lamports 3357316080
[exit 0]
```
### Rollback rehearsal (runbook 'Rollback' section, program part only; the Vercel/app part is not rehearsed)

```
$ sha256sum ~/plotarmor-rollback/deployed-09c5bfc-slot476301346.so; solana program deploy ~/plotarmor-rollback/deployed-09c5bfc-slot476301346.so --program-id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 --upgrade-authority ~/.config/solana/id.json -u http://127.0.0.1:8899
7d43bcb222c6e71d8cfe77db2fe3a48dc82704573873f04ef0c8d144de877235  /home/sucka/plotarmor-rollback/deployed-09c5bfc-slot476301346.so
Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2

Signature: ZiR2LivXq1TmiyUaDcR3KwYR5UBzkyVtXui6uEWJufmghrH4Qdq9Ka6QVT7LfQLfijsgK3k94zh7ny4WZZ8cnrp
[exit 0]
```

```
$ solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u http://127.0.0.1:8899; solana program dump 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/rolled.so -u http://127.0.0.1:8899 && python3 -I -c "import hashlib;b=open('/tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/rolled.so','rb').read().rstrip(b'\0');print('trimmed',len(b),hashlib.sha256(b).hexdigest());print('expect 5663e20f992914ad1a2671888fd3062a36df69ecc6ac81ee1318f9e702bc3fb5');print('security.txt marker present:', b'=======BEGIN SECURITY.TXT V1=======' in b)"

Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL
Authority: EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
Last Deployed In Slot: 410
Data Length: 482200 (0x75b98) bytes
Balance: 3.35731608 SOL

Wrote program to /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/rolled.so
trimmed 470257 5663e20f992914ad1a2671888fd3062a36df69ecc6ac81ee1318f9e702bc3fb5
expect 5663e20f992914ad1a2671888fd3062a36df69ecc6ac81ee1318f9e702bc3fb5
security.txt marker present: False
[exit 0]
```

```
$ DEVNET_RPC_URL=http://127.0.0.1:8899 timeout 300 node_modules/.bin/ts-node --transpile-only scripts/devnet_sign_contract_test.ts 2>&1 | grep -E "AccountDiscriminatorMismatch|RESULT|Error Code" | head -n 3 | cut -c1-200
Fatal error: AnchorError: AnchorError caused by account: contract_artifact. Error Code: AccountDiscriminatorMismatch. Error Number: 3002. Error Message: Account discriminator did not match what was ex
    'Program log: AnchorError caused by account: contract_artifact. Error Code: AccountDiscriminatorMismatch. Error Number: 3002. Error Message: Account discriminator did not match what was expected.'
    'Program log: AnchorError caused by account: contract_artifact. Error Code: AccountDiscriminatorMismatch. Error Number: 3002. Error Message: Account discriminator did not match what was expected.'
[exit 0]
```

## Summary of results

| check | result | label |
|---|---|---|
| Cloned program bytes equal devnet dump (trimmed sha256 5663e20f...3fb5) | yes | [cmd] |
| Old program + new sign_contract account list | fails, AccountDiscriminatorMismatch 3002 on contract_artifact | [cmd] |
| `solana program extend ... 10240` | ok, Data Length 482,200, ProgramData 482,245 bytes | [cmd] |
| `solana program deploy ... --no-auto-extend` | ok, 470 write transactions, authority paid 2,350,000 lamports in fees | [cmd] |
| Upgraded bytes: trimmed sha256 bcea64bb...c4f2 and 472,425 bytes | match the runbook | [cmd] |
| security.txt read back from the upgraded program | name PlotArmor, contacts email:info@plotarmor.io, source_code private | [cmd] |
| register_work_claim after upgrade | ok, AnchorRecord external_ref_hash round trip matches | [cmd] |
| sign_contract after upgrade (happy path) | ok, ContractSignature 121 bytes, owner = program | [cmd] |
| sign_contract adversarial (3 paths) | 3 passed, 0 failed | [cmd] |
| 11 cloned accounts (one per discriminator) deserialize with the new IDL | 11 ok, 0 failed | [cmd] |
| Spill path (addendum): excess in ProgramData returns to the authority on upgrade | yes, authority regained 833,240,840 = 835,590,840 excess - 2,350,000 fees | [cmd] |
| Rollback to the saved 09c5bfc dump | ok, trimmed sha256 equals 5663e20f...3fb5, no security.txt, new sign_contract fails again | [cmd] |

Authority balance trace in lamports for the main run [cmd]: before extend 5,396,189,971; after
extend 5,324,914,571 (-71,275,400 = 71,270,400 rent top-up + 5,000 fee); before deploy
5,324,914,571; after deploy 5,322,564,571 (-2,350,000, fees only, buffer rent refunded; no spill
because ProgramData was already at its local minimum).

## Where localnet differs from devnet (read before trusting any number above)

1. RENT RATE. Local validator: 6,960 lamports per byte (genesis default). Devnet today: 5,080,
   checked 2026-10-06 with `solana rent` on both (3.28604568 vs 2.39843564 SOL for 472,005 bytes).
   The rate is not settable on solana-test-validator 4.0.1. Consequences:
   - The extend needed a 71,270,400 lamport rent top-up here. On devnet the runbook predicts 0,
     because ProgramData holds 3.286 SOL against a 2.450 SOL minimum. NOT rehearsed at devnet rates.
   - The main-run upgrade spilled nothing here. The devnet spill (3,236,424,240 lamports spilled,
     net +835,590,840 after paying the buffer) is only supported by the addendum, which showed the
     loader spills excess on upgrade, using devnet's predicted excess amount. The arithmetic at
     devnet's exact balances was not run on chain.
   - Buffer rent was 3.2893308 SOL here against 2.4008334 on devnet. Headroom looks smaller here.
   - Devnet's rate was 6,960 per byte in July (ContractSignature, 121 bytes, measured 1,733,040
     lamports) and is 5,080 now (1,264,920). So the CLAUDE.md cost baselines are stale for new
     accounts, and sign_contract today should cost about 1,269,920 lamports on devnet [inferred].
     Local rent for 121 bytes is 1,733,040, which is why the local sign_contract script printed
     the old figure.
2. FEATURE GATES AND VALIDATOR VERSION. `--clone-feature-set` copied devnet's activated features
   at start, but the local binary is Agave 4.0.1 and devnet's validator version is unknown. The
   480-byte probe extend was accepted locally, so the 10 KiB minimum (SIMD-0431, loader
   interface 6.1.1) is not enforced here. That does not show devnet accepts 480. The runbook's
   +10,240 is valid either way. `solana feature status` on this CLI does not list SIMD-0431 on
   either cluster, so its devnet state is still undetermined.
3. NETWORK BEHAVIOUR. Local confirmations took about 250 ms with no congestion, no dropped
   transactions and no rate limits. The deploy sent 470 write transactions. Against devnet, a
   public or API-keyed RPC may rate limit or drop some of them, and the deploy can stop midway
   with the buffer funded (about 2.4 SOL locked until resumed with `--buffer` or closed). Not
   rehearsed. Consider a dedicated RPC and `--max-sign-attempts`, and have the resume and close
   commands from the runbook ready.
4. CLOCK AND SLOTS. Last Deployed In Slot was 0 on the clone, then 120, 163 and 410 locally. Devnet
   slots are around 476 million. Program-effective-next-slot timing is the same in principle but
   was not measured at devnet scale.
5. STATE COVERAGE. 11 of 617 program accounts were cloned, one per discriminator. All 11
   deserialize, but 606 other accounts were not read. The authority was cloned with its balance at
   clone time, then spent down by the scripts, so the starting balance on devnet will differ.
6. NOT REHEARSED AT ALL: Step 1 (staging the app and the Vercel preview), Step 3 (promoting the
   app within minutes), the manual sign in the live web app, the Kora script check, and the app
   side of rollback. The cutover window length is therefore unmeasured.
7. COSMETIC SCRIPT TEXT. The devnet scripts print "devnet" and explorer links with
   `cluster=devnet`. The sign_contract script's JSON also says "verified ... after devnet
   upgrade". All of that is hard-coded script text. Every transaction here is local only.

## Findings for the runbook (not yet applied)

- The runbook is consistent with this rehearsal. No command needed changing to run.
- Add to the runbook, at the owner's choice: a dedicated RPC for the deploy, and note that
  after a rollback the program account stays extended (Data Length stays 482,200; it does not
  shrink back to 471,960), which is harmless.
- CLAUDE.md cost baselines need a re-measurement against today's devnet rent rate. Not edited.

## Pass count

Cutover plan: pass 1 was the read-only on-chain and IDL work in the prior session. This is pass 2
(a rehearsal on a local validator seeded from devnet). It is not a live devnet check. Two more
independent passes are needed before the plan or the new binary can be called verified, for
example an independent re-audit and the real devnet run with post-checks.

## Addendum 2: rehearsal of --buffer resume, abandon with close, and --use-rpc (local validator)

Fresh local validator, same seeding as above (program, authority, 11 account clones, devnet
feature set), ledger deleted afterwards. The deploy command is the one in the runbook after
commit c79fb69, with the local URL in place of `$DEVNET_RPC_URL`: guard script, `--buffer`,
`--no-auto-extend --use-rpc --max-sign-attempts 20`. The buffer keypairs are throwaway files in a
scratch directory. "Kill" means `kill -9` on the whole deploy process group shortly after the buffer
account appears on chain, to imitate a crash or a dropped connection.

LIMITS: on a local validator `--use-rpc` only proves the flag is accepted and the deploy completes
through it. It does not show behaviour under devnet rate limits or against Helius. The kill point
is timing based, so how much of the upload landed is measured, not chosen.

```
$ solana program extend 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 10240 -u http://127.0.0.1:8899; solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports

Extended Program Id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 by 10240 bytes

5329290451 lamports
[exit 0]
```

```
$ scripts/guard_deploy_artifact.sh; echo guard-exit=$?
artifact OK: target/deploy/plotarmor.so trimmed sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
guard-exit=0
[exit 0]
```
### Scenario B: partial upload, then abandon with solana program close

```
$ solana-keygen new -o /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-b.json --no-bip39-passphrase --silent && solana address -k /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-b.json
Wrote new keypair to /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-b.json
HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9
[exit 0]
```

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports
5329290451 lamports
[exit 0]
```

```
$ /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/partial.sh /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-b.json 1
buffer address: HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9
deploy killed after buffer appeared (+1s)
/tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/partial.sh: line 28: 10148 Killed                     setsid bash -c "scripts/guard_deploy_artifact.sh && solana program deploy target/deploy/plotarmor.so   --program-id $P --upgrade-authority ~/.config/solana/id.json --buffer $KEY   --no-auto-extend --use-rpc --max-sign-attempts 20 -u $L" > /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/deploy-partial.log 2>&1
--- deploy log so far:
artifact OK: target/deploy/plotarmor.so trimmed sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
[exit 0]
```

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana program show --buffers -u http://127.0.0.1:8899; solana program dump HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9 /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-b.dump -u http://127.0.0.1:8899 >/dev/null && python3 -I /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/bufstat.py /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-b.dump target/deploy/plotarmor.so; solana program show HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9 -u http://127.0.0.1:8899 2>&1 | head -n 8
2039463971 lamports

Buffer Address                               | Authority                                    | Balance
HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9 | EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd | 3.28938648 SOL

buffer dump bytes 472440 program bytes 472440
non-zero 1000-byte chunks written: 87 of 473 (18.4%)
PARTIAL upload

Buffer Address: HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9
Authority: EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
Balance: 3.28938648 SOL
Data Length: 472440 (0x73578) bytes
[exit 0]
```

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana program close HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9 -u http://127.0.0.1:8899; solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana program show --buffers -u http://127.0.0.1:8899; solana account HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9 -u http://127.0.0.1:8899 2>&1 | head -n 2
2039463971 lamports

Buffer Address                               | Authority                                    | Balance
HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9 | EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd | 3.28938648 SOL

5328845451 lamports

Buffer Address                               | Authority                                    | Balance

Error: AccountNotFound: pubkey=HSA5HWVRt8qLrvYG1qeyF1j3iQwURSVec7WXqsdKtyo9
[exit 0]
```
### Scenario A: partial upload, then resume with the identical command

```
$ solana-keygen new -o /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-a.json --no-bip39-passphrase --silent && solana address -k /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-a.json; solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports
Wrote new keypair to /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-a.json
G9KiYYVNSkoaJSFDZR32yicgsFqiDTFzyR3myBvqSJJA
5328845451 lamports
[exit 0]
```

```
$ /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/partial.sh /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-a.json 1 2>&1 | grep -v Killed
buffer address: G9KiYYVNSkoaJSFDZR32yicgsFqiDTFzyR3myBvqSJJA
deploy killed after buffer appeared (+1s)
--- deploy log so far:
artifact OK: target/deploy/plotarmor.so trimmed sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
[exit 0]
```

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana program show --buffers -u http://127.0.0.1:8899; solana program dump G9KiYYVNSkoaJSFDZR32yicgsFqiDTFzyR3myBvqSJJA /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-a.dump -u http://127.0.0.1:8899 >/dev/null && python3 -I /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/bufstat.py /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-a.dump target/deploy/plotarmor.so; solana program show  -u http://127.0.0.1:8899 2>/dev/null | grep -i -E 'slot|data length'
2038988971 lamports

Buffer Address                               | Authority                                    | Balance
G9KiYYVNSkoaJSFDZR32yicgsFqiDTFzyR3myBvqSJJA | EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd | 3.28938648 SOL

buffer dump bytes 472440 program bytes 472440
non-zero 1000-byte chunks written: 93 of 473 (19.7%)
PARTIAL upload
[exit 1]
```

```
$ scripts/guard_deploy_artifact.sh && solana program deploy target/deploy/plotarmor.so --program-id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 --upgrade-authority ~/.config/solana/id.json --buffer /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/buf-a.json --no-auto-extend --use-rpc --max-sign-attempts 20 -u http://127.0.0.1:8899
artifact OK: target/deploy/plotarmor.so trimmed sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2

Signature: qD6xYfHwjGDVAAkHmw1GBsAp7rpmS1XnxsxJGXbxPCkXKyziQhFN9tTXMkcekPsHjdWaAioJDKEa6HUrvqMfgac
[exit 0]
```

```
$ solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u http://127.0.0.1:8899 --lamports; solana program show --buffers -u http://127.0.0.1:8899; solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u http://127.0.0.1:8899; solana program dump 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/final.so -u http://127.0.0.1:8899 >/dev/null && python3 -I /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/verify_bytes.py /tmp/claude-1000/-home-sucka-plotarmor-program/df3dc9e2-961a-4750-abc1-a723e965a5da/scratchpad/final.so | head -n 4
5326495451 lamports

Buffer Address                               | Authority                                    | Balance


Program Id: 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2
Owner: BPFLoaderUpgradeab1e11111111111111111111111
ProgramData Address: Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL
Authority: EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
Last Deployed In Slot: 171
Data Length: 482200 (0x75b98) bytes
Balance: 3.35731608 SOL

dump length 482200 trimmed 472425
trimmed sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
expected       bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
begin marker at 421297 end marker at 421653
[exit 0]
```

### Addendum 2 results

| check | result | label |
|---|---|---|
| Guard script passes the audited artifact before deploy | passes, trimmed sha256 bcea64bb...c4f2 | [cmd] |
| Deploy with `--buffer`, `--no-auto-extend --use-rpc --max-sign-attempts 20` accepted by solana-cli 4.0.1 | yes, full deploy completed through it (scenario A resume) | [cmd] |
| Killed deploy leaves a funded partial buffer, listed by `solana program show --buffers` | yes: 87 of 473 non-zero chunks (18.4%) in scenario B, 93 of 473 (19.7%) in A; buffer held 3.28938648 SOL (local rent) | [cmd] |
| Program unchanged while the buffer is partial | yes, Data Length 482,200 and slot unchanged until the resume | [cmd] |
| Abandon: `solana program close <buffer>` | buffer gone, rent returned: balance +3,289,386,480 (rent) - 5,000 (fee) | [cmd] |
| Total cost of the abandoned attempt | 445,000 lamports in fees | [cmd] |
| Resume: same command, same `--buffer` keypair | completed, upgrade landed (slot 171), buffer consumed, `--buffers` list empty | [cmd] |
| Resume cost vs a full run | 1,880,000 lamports (376 transactions) against 2,350,000 (470) for the full run in the main rehearsal: chunks already written were not paid for again | [cmd] |
| Upgraded bytes after the resumed deploy | trimmed sha256 bcea64bb...c4f2, security.txt fields as before | [cmd] |

Notes:
- `solana-keygen new` prints the seed phrase unless `--silent` is given. The runbook now includes
  `--silent` for the buffer keypairs.
- The kill is timing based (kill -9 one second after the buffer appears). The same-command resume
  is shown to continue and skip written chunks, not to survive every possible interruption point
  (for example a kill during the final upgrade instruction was not tried).
- Not shown: behaviour against devnet rate limits or Helius, which is the actual reason for
  `--use-rpc`. Local confirms in about 250 ms, so no transaction expired and `--max-sign-attempts`
  never came into play.

## Addendum 3: committed binary in bc729e9 is the clean build

`evidence/2026-09-30-m2-pass4/independent-run/plotarmor-7c267e9.so` was compared with a fresh build
of 7c267e9 (git worktree at that commit, fresh CARGO_TARGET_DIR on the main disk,
`cargo build-sbf --tools-version v1.52 --manifest-path programs/plotarmor/Cargo.toml`, cold build
4m17s) [cmd]:

| file | bytes | trimmed bytes | trimmed sha256 |
|---|---|---|---|
| fresh build of 7c267e9 | 472,280 | 472,265 | 789f64d7a2f6ece13e600052877849a3fcb7d9b6637205bd997dd49dd43a4cf6 |
| committed plotarmor-7c267e9.so | 472,280 | 472,265 | 789f64d7a2f6ece13e600052877849a3fcb7d9b6637205bd997dd49dd43a4cf6 |

The whole-file sha256 of both starts 27998e6f6437e799, equal to the SHA256SUMS entry
27998e6f6437e7998bf35fffb65cde8a8599cf541fcb01fba509baafbc22e231. The worktree source contains the
pause check (`require!(!ctx.accounts.registry_config.paused, PlotArmorError::Paused)` at
sign_contract.rs line 76) that the mutation removes, so the committed binary is the CLEAN build,
not the mutant. One pass: the build is one cold build with one toolchain on one machine.
The worktree and its target directory were removed afterwards.
