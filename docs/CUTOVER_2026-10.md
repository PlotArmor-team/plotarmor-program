# Devnet cutover: program 09c5bfc -> f34bfae (prepared 2026-10-06, NOT EXECUTED)

Nothing in this file has been run against a cluster. Every command below is a plan.
Verification label for each fact: [cmd] command output, [idl] IDL diff, [test] test run,
[inferred] reasoned but not confirmed. Audit pass count for the cutover itself: 2 of 4
(pass 1: read-only derivation in the prior session; pass 2: local-validator rehearsal,
docs/evidence/2026-10-06-cutover-rehearsal-localnet.md). Neither pass touched devnet.

## What changes on chain

- Only `sign_contract` changes: it now takes `registry_config` as its FIRST account (read-only,
  not signer) and rejects with Paused (6008) when paused. [idl]
- The other 6 instructions: discriminators, args and account lists identical. [idl]
- All account types: field layout identical, account discriminators identical, errors,
  events and constants identical. state.rs untouched between the two commits. [idl] [cmd: git diff]
- `register_work_claim` is UNCHANGED, so the Kora sponsored script and app registration need
  no change. [idl]
- security.txt is added (.rodata only). [cmd: marker found in new .so, absent in deployed dump]
- Existing devnet accounts: 617 program-owned accounts, all 11 discriminators are the same set
  and layouts are unchanged, so nothing fails to deserialize. [cmd: getProgramAccounts, idl]
- RegistryConfig PDA `BpsMTsw9uxmmgmy1iVjgwaLfoyKMGuoisyBQ8sTrxvmG` exists, owner is the program,
  44 bytes, authority EjeeFw3F..., schema 1, enabled_anchor_modes 0, paused false. No init step
  needed. [cmd]

## Artifacts (kept outside the repo in ~/plotarmor-rollback/)

| file | sha256 (whole file) | note |
|---|---|---|
| deployed-09c5bfc-slot476301346.so | 7d43bcb2...7235 | dump of live program, 471,960 bytes. Trimmed sha256 5663e20f...3fb5 equals a fresh v1.52 build of 09c5bfc [cmd] |
| new-f34bfae.so | 97880b05...16b7 | HEAD build, 472,440 bytes, trimmed 472,425, trimmed sha256 bcea64bb...c4f2 |

Built with `scripts/build.sh --anchor` (platform-tools v1.52). The cargo-path build of HEAD was
not re-run this session, so cross-path equality at HEAD is not re-confirmed here.

## Size and cost (re-derived from command output 2026-10-06, all `-u devnet`; nothing sent)

Live rent rate is 5,080 lamports per byte (rent for N data bytes = (128 + N) * 5080). The
current ProgramData was funded at the older 6,960 rate, so it holds more than the minimum.

| item | data bytes | lamports | SOL | source |
|---|---|---|---|---|
| ProgramData now (45 header + 471,960 program) | 472,005 | 3,286,045,680 held | 3.28604568 | [cmd: solana account] |
| rent minimum, ProgramData now | 472,005 | 2,398,435,640 | 2.39843564 | [cmd: solana rent 472005] |
| rent minimum, exact fit (45 + 472,440) | 472,485 | 2,400,874,040 | 2.40087404 | [cmd: solana rent 472485; same via getMinimumBalanceForRentExemption on api.devnet.solana.com] |
| rent minimum, after extend +10,240 | 482,245 | 2,450,454,840 | 2.45045484 | [cmd: solana rent 482245] |
| upgrade buffer (37 header + 472,440) | 472,477 | 2,400,833,400 | 2.40083340 | [cmd: solana rent 472477] |

New `target/deploy/plotarmor.so` is 472,440 bytes, sha256 97880b05...16b7, identical to the
copy in ~/plotarmor-rollback/. [cmd]

### Extend: exact numbers

- Needed minimum growth is 480 bytes (472,440 - 471,960). Use **+10,240** instead.
  `solana-loader-v3-interface` 6.1.1 (the version in this repo's Cargo.lock, read from
  ~/.cargo/registry) defines `MINIMUM_EXTEND_PROGRAM_BYTES = 10_240` and documents that, once
  the SIMD-0431 feature gate is active, `additional_bytes` must be at least 10 KiB. [cmd: grep of
  source] Whether that gate is active on devnet was NOT determined: `solana feature status -u
  devnet` does not list it. So 480 may be rejected and 10,240 is valid either way. The July
  extend also used +10,240 (CLAUDE.md). [cmd] [inferred: gate status]
- After extend: ProgramData account 482,245 bytes, `solana program show` Data Length 482,200.
- Lamports the extend costs: **0 for rent**, plus the 5,000 lamport signature fee (one
  signature, payer = authority). Reason: held 3,286,045,680 >= required 2,450,454,840, and the
  loader pays only `max(min_balance(new_len) - balance, 0)` (solana-bpf-loader-program 3.1.14
  `common_extend_program`, `required_payment`). [cmd: source read] [inferred: not exercised on
  chain, no simulation was run]
- Does this CLI extend automatically? Yes by default: `solana-cli 4.0.1` lists
  `--no-auto-extend` ("Don't automatically extend the program's data account size") on
  `solana program deploy`, which implies auto-extend is the default. [cmd: --help] [inferred:
  behavior not exercised]. The runbook still runs `solana program extend` explicitly, as
  requested, and passes `--no-auto-extend` to the deploy so no implicit extend can happen.

### Buffer, upgrade refund and fees

- Buffer rent: **2,400,833,400 lamports (2.40083340 SOL)**. The earlier "about 2.4 SOL" figure
  was right, now exact. [cmd]
- The upgrade does not only refund the buffer. The loader sets ProgramData to the rent minimum
  for its new length and spills everything else to the spill account (the payer, here the
  authority). With ProgramData at 482,245 bytes:
  spill = 3,286,045,680 (ProgramData) + 2,400,833,400 (buffer) - 2,450,454,840 (new minimum)
  = 3,236,424,240 lamports. Net to authority after paying the buffer: +835,590,840 lamports
  (+0.83559084 SOL), before fees. [cmd: source read, arithmetic] [inferred: not exercised on
  chain; spill address = payer is the CLI default, not confirmed]
- Fees: about 475 write transactions at 5,000 lamports (one signature each, roughly 1 KB of
  program data per write) plus buffer create, extend and upgrade, about 0.0025 SOL total.
  [inferred: chunk size not measured; no compute-unit price is set, so no priority fee]
- Peak SOL needed at once: buffer 2.40083340 + fees about 0.0025 = about 2.4034 SOL.
  Authority holds 5.400565851 SOL [cmd], so margin is about 3.0 SOL at peak. Expected balance
  after the upgrade is about 6.236 SOL (5.400565851 + 0.83559084 - fees). [inferred]
- Local key `~/.config/solana/id.json` resolves to EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd,
  the upgrade authority. [cmd: solana address -k]

## Blocking item before any real deploy

- [ ] Milan approves this plan. security.txt now carries real contact info (info@plotarmor.io)
  per f34bfae, so the old placeholder blocker is cleared. [cmd: parsed fields]

## Step 0: pre-checks (all read-only)

```bash
cd ~/plotarmor-program
git rev-parse HEAD                      # a docs-only descendant of f34bfae is fine, source must match (next line)
git diff --quiet f34bfae HEAD -- programs Cargo.toml Cargo.lock Anchor.toml scripts rust-toolchain.toml && echo "source identical to f34bfae"
git status --short                      # expect empty
solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u devnet   # Last Deployed In Slot must still be 476301346
solana address -k ~/.config/solana/id.json   # expect EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd
solana balance EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd -u devnet        # expect > 3 SOL
solana rent 482245 -u devnet            # expect 2.45045484 SOL (5,080 lamports per byte)
```

Rent re-check: devnet rent was 6,960 lamports per byte in July and 5,080 on 2026-10-06. SIMD-0437
stages 3 to 5 (2,575, 1,322 and 696 lamports per byte) were still inactive on devnet that day
(`solana feature status -u devnet`). If the `solana rent` line above prints anything other than
2.45045484 SOL, the rent rate changed: recompute "Size and cost" (extend top-up, buffer rent,
spill, balances) before going on. [cmd]

The source check replaces an earlier "HEAD must equal f34bfae" line, which stopped being true
once documentation commits landed on top. The program source, Cargo files and build script are
unchanged since f34bfae. [cmd: git diff --quiet, 2026-10-06]

### Build fresh, then gate on the artifact hash

Do not trust whatever sits in `target/deploy`. Delete it, rebuild with the pinned wrapper, and let
the guard refuse anything that is not the audited build. A warm rebuild is not a reproducibility
test (CLAUDE.md), so the hash gate is what proves the bytes, not the build log:

```bash
rm -f target/deploy/plotarmor.so
scripts/build.sh --anchor                 # platform-tools v1.52, stamps and clears stale compiler output
                                          # (a cold pinned build of 7c267e9 took 4m17s here, 2026-10-06)
scripts/guard_deploy_artifact.sh          # exit 1 and prints both hashes unless the trimmed sha256 is
                                          # bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
```

The guard script was tested 2026-10-06 against: the real artifact (passes), one appended
non-zero byte, one flipped byte, a missing file (all exit 1, and a chained deploy does not run),
and a zero-padded copy (passes, because the compare is on the trimmed hash). [test]
If the hash differs, stop. Do not edit the expected value to make it pass.

If the slot changed, someone else deployed. Stop and re-dump before doing anything.

## Step 1: stage the app (so the window is minutes)

The new account list is not backward compatible: the old program would read registry_config as
contract_artifact. There is no client that works with both. [inferred from account order]

- [ ] Rebase `d9da574` onto the new SaaS UI branch. Re-run `grep -rn "signContract"` in
      plotarmor-demo and confirm every call site passes `registryConfig` (verify_calls.py does
      NOT check account contents, see CLAUDE.md coverage gap).
- [ ] Build it as a Vercel preview, NOT promoted to production. Keep the deployment id/URL ready.
- [ ] Copy the new IDL: `cp target/idl/plotarmor.json` and `target/types/plotarmor.ts` into
      plotarmor-demo `src/anchor/` (already in the branch if d9da574 includes them; diff them).
- [ ] Do not merge to main yet. Main auto-deploys to production.

## Step 2: extend, then upgrade (this opens the window)

Use a dedicated devnet RPC for every write in this step, not the public endpoint. The deploy
sends about 470 write transactions (measured in the rehearsal: authority paid 2,350,000
lamports in fees), and a public or shared RPC can rate limit or drop some of them. Whether
the Helius plan in use tolerates 470 writes in a burst is NOT known. [inferred]

Set the URL without printing it. Never run `solana config get`, `echo "$DEVNET_RPC_URL"` or
any `-v` command in this window, because they print the RPC URL including the API key:

```bash
read -rs DEVNET_RPC_URL && export DEVNET_RPC_URL     # paste the Helius devnet URL, press Enter
```

The existing devnet scripts read the same variable name, so Step 4 reuses it.

Generate the buffer keypair BEFORE the deploy and keep it outside the repo. Passing it with
`--buffer` makes a partial upload resumable with the identical command:

```bash
umask 077
solana-keygen new -o ~/plotarmor-rollback/buffer-f34bfae.json --no-bip39-passphrase --silent   # refuses to overwrite; --silent keeps the seed phrase off the screen
solana address -k ~/plotarmor-rollback/buffer-f34bfae.json    # record the buffer address
```

Then extend, check, and deploy:

```bash
cd ~/plotarmor-program
solana program extend 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 10240 -u "$DEVNET_RPC_URL"
solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u "$DEVNET_RPC_URL"    # Data Length 482200 expected (ProgramData 482,245 bytes)
scripts/guard_deploy_artifact.sh && solana program deploy target/deploy/plotarmor.so \
  --program-id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 \
  --upgrade-authority ~/.config/solana/id.json \
  --buffer ~/plotarmor-rollback/buffer-f34bfae.json \
  --no-auto-extend --use-rpc --max-sign-attempts 20 -u "$DEVNET_RPC_URL"
```

Flags, from `solana program deploy --help` on solana-cli 4.0.1 [cmd]: `--use-rpc` sends the
write transactions to the configured RPC instead of validator TPUs. `--max-sign-attempts`
re-signs and resends transactions still unconfirmed after the blockhash expires (the value 20
is a choice, not a measured need). `--buffer` takes the buffer signer and is documented as the
way to resume a failed deploy. The `--buffer` resume, the abandon-and-close path and the
`--use-rpc` flag were rehearsed on a local validator (evidence file, Addendum 2): a killed
deploy resumed with the identical command, and close returned the buffer rent. Behaviour under
devnet or Helius rate limits was not rehearsed. [cmd]

Use 10240, not 480: see "Extend: exact numbers".

### If the deploy stops partway

The buffer is funded (about 2.4 SOL, 2,400,833,400 lamports) and stays locked until it is
resumed or closed. The program is NOT changed until the final upgrade instruction lands, so
the live app keeps working on the old program meanwhile.

```bash
solana program show --buffers -u "$DEVNET_RPC_URL"     # lists buffers whose authority is the default keypair
```

- Resume: run the SAME `solana program deploy ...` command again, with the same `--buffer`
  keypair. It continues the upload into that buffer and skips chunks already written. [cmd:
  local rehearsal, resume cost 1,880,000 lamports against 2,350,000 for a full run]
- Abandon: `solana program close <BUFFER_ADDRESS> -u "$DEVNET_RPC_URL"` returns the buffer rent
  to the default keypair (the authority). Confirm the balance afterwards. [cmd: local rehearsal]
- Never run `solana program close --buffers` casually: it closes every buffer matching the
  authority, including any unrelated one.

## Step 3: close the window immediately

Window = time between the deploy confirming and the app going live. Only `sign_contract` is
broken in the live app during it. Registration, add_version and anchors keep working. [idl]

- [ ] Merge the app branch to main, or promote the staged Vercel deployment (instant, no rebuild).
      Target: under 5 minutes. Promote first, merge after, to avoid a rebuild delay. [inferred]
- [ ] Have the Kora script owner confirm no change is required (register_work_claim unchanged).

## Step 4: post-checks

```bash
solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u devnet   # new slot, authority unchanged, length 482200; ProgramData balance 2.45045484 SOL; authority about 6.236 SOL
solana program dump 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 /tmp/post.so -u devnet
python3 -I -c "import hashlib;print(hashlib.sha256(open('/tmp/post.so','rb').read().rstrip(b'\0')).hexdigest())"
# expect bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
```

- [ ] Read security.txt back from the dumped bytes (marker `=======BEGIN SECURITY.TXT V1=======`),
      expect name PlotArmor, contacts email:info@plotarmor.io, source_code private.
- [ ] Live register: `node_modules/.bin/ts-node --transpile-only scripts/devnet_register_test.ts`
- [ ] Live sign_contract: `scripts/devnet_sign_contract_test.ts`, then the adversarial one
      `scripts/devnet_sign_contract_adversarial_test.ts` (both already use the new account list).
- [ ] One manual sign in the live web app.
- [ ] Update CLAUDE.md deploy history and the "REDEPLOY PENDING" note. Do this in a separate
      approved commit.

Pass count after a clean run of this section: 1 live check. Do not call it verified until 4.

## Rollback

Program (restores the exact 09c5bfc bytes; the dump is padded, deploy accepts a file smaller
than the allocation):

```bash
solana-keygen new -o ~/plotarmor-rollback/buffer-rollback.json --no-bip39-passphrase --silent
echo "7d43bcb222c6e71d8cfe77db2fe3a48dc82704573873f04ef0c8d144de877235  $HOME/plotarmor-rollback/deployed-09c5bfc-slot476301346.so" | sha256sum -c - && \
solana program deploy ~/plotarmor-rollback/deployed-09c5bfc-slot476301346.so \
  --program-id 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 \
  --upgrade-authority ~/.config/solana/id.json \
  --buffer ~/plotarmor-rollback/buffer-rollback.json \
  --no-auto-extend --use-rpc --max-sign-attempts 20 -u "$DEVNET_RPC_URL"
```

The same partial-upload recovery as in Step 2 applies, with the rollback buffer keypair.

After a rollback the program account stays extended: `solana program show` reports Data Length
482,200, not the original 471,960, because ProgramData does not shrink. This is harmless. The
rollback restores the exact 09c5bfc bytes (trimmed sha256 5663e20f...3fb5), and the extra
space is simply unused. [cmd: local rehearsal, docs/evidence/2026-10-06-cutover-rehearsal-localnet.md]

Then revert the app: instant-rollback the Vercel deployment to the previous production build,
and revert the merge commit on plotarmor-demo main. Program and app must be rolled back together
for the same reason they must be cut over together. After rollback, security.txt disappears and
sign_contract returns to the old four-account list.

## Notes

- Verified build badge: `anchor build --verifiable` was NOT run. Docker is not installed here
  and solana-verify is not installed. [cmd: command not found] Remote verification is mainnet-only
  and needs a public repo, so it is not started.
- No Rust was changed in this task, so program_autofixer was not needed.
