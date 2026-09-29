# M2 pass 4 (independent re-audit) of commit 7c267e9

Run 2026-09-29 UTC by a Claude Code session (Opus 5.5) that did not write the change.
Evidence path uses the requested 2026-09-30 name. No source edited, nothing deployed,
no transaction signed or broadcast to devnet. All mutations ran in a scratch extract of
7c267e9 outside the repo, since deleted.

## Verdict

**The M2 code change: PASS.** Checks 1 to 5 all pass on the 7c267e9 source and binary.

**Redeploy readiness: FAIL.** Check 6 found three blockers, none of which is a defect in
the M2 logic itself:

1. The 7c267e9 binary contains the security.txt placeholders
   `email:UNSET-PLACEHOLDER-DO-NOT-DEPLOY@example.invalid` and
   `UNSET-PLACEHOLDER-DO-NOT-DEPLOY` (lib.rs:52-53). CLAUDE.md says this binary must not be
   deployed until a real contact and policy URL exist. No SECURITY.md exists. Filling
   them in changes the bytes, so the pinned hash 789f64d7... can never be the deployed
   hash.
2. plotarmor-demo `main`, `origin/main`, `feat/wallet-bindings` and
   `origin/feat/wallet-bindings` still use the 4-account call
   (src/ContractsApp.tsx:1198) and the old IDL. d9da574 exists on no remote branch.
   A redeploy breaks sign_contract for any frontend built from main.
3. The binary is 472,280 bytes. The devnet ProgramData program capacity is 471,960, a
   320-byte shortfall (305 even trimmed). `solana program deploy` auto-extends by
   default (`--no-auto-extend` exists), but a `write-buffer` + `upgrade` flow does not.
   CLAUDE.md's statement that security.txt "fits ... with roughly 17KB spare" does not
   hold for this build.

## Per check

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | registry_config constraint, no fake config | PASS | 01_02, 03d |
| 2 | Pause placement, error code, ordering | PASS (commit message inaccurate) | 01_02, 03d, 03e |
| 3 | Regression test non-vacuous | PASS | 03e, 03f |
| 4 | IDL order and every caller | PASS for program repo, d9da574 and kora. Old order remains on demo main and wallet-bindings | 04a to 04e |
| 5 | Pinned cold build hash | PASS, exact match | 03a, 05a, 05c |
| 6 | Other redeploy risks | FAIL, see above | 05d, 06a to 06c |

### 1. Config constraint
sign_contract.rs:14-18 is `#[account(seeds = [b"config"], bump,)] pub registry_config:
Account<'info, RegistryConfig>`. It is identical in add_owner.rs:9-13, add_version.rs:18-22,
anchor_authorized_contract.rs:18-22, anchor_evidence_contract.rs:17-21 and
register_work_claim.rs:23-27. Checked at runtime against the pinned 7c267e9 binary, with
six scratch LiteSVM tests (03d):
- valid config bytes at a non-PDA, program-owned address: ConstraintSeeds 2006
- real PDA owned by the System Program: AccountOwnedByWrongProgram 3007
- real PDA with the ContractArtifact type tag: AccountDiscriminatorMismatch 3002
- ContractArtifact passed as the config: AccountDiscriminatorMismatch 3002
- config missing: AccountNotInitialized 3012

No signature account was created in any of these cases.

Live devnet config BpsMTsw9uxmmgmy1iVjgwaLfoyKMGuoisyBQ8sTrxvmG: owned by the program,
correct type tag, paused = 0 (06a). The fix does not depend on paused being settable.
Known limitation C (no setter) stands.

### 2. Pause placement
At 7c267e9, `require!(!ctx.accounts.registry_config.paused, PlotArmorError::Paused)` is at
sign_contract.rs:76, before the ContentHashMismatch check at :79. Paused is error 6008, and
the test with paused plus a wrong hash returned 6008. The four anchoring instructions call
assert_mode_allowed first and check paused second (register_work_claim.rs:102/105,
add_version.rs:76/79, anchor_authorized_contract.rs:78/81, anchor_evidence_contract.rs:66/69).
add_owner.rs:53 checks paused first. The HEAD comment (7a3dc0b) describes this accurately.
The 7c267e9 commit message ("Copied verbatim from anchor_evidence_contract.rs ... the
require! as the first check") does not. That is a documentation inaccuracy only.

Anchor validates the accounts, including the `init` of contract_signature, before the
handler runs. A paused rejection therefore rolls back an already-executed create_account
CPI atomically. Confirmed: no ContractSignature exists after a rejection.

### 3. Mutation
The mutant has the single line at sign_contract.rs:76 deleted (diff in 03e). Its binary
hash 3cc388f5... differs from the baseline, so it genuinely rebuilt.
- `paused_registry_rejects_sign_contract` FAILED: the signing transaction SUCCEEDED while
  paused.
- `pass4_paused_checked_before_content_hash` FAILED: it got 6011 instead of 6008.
- The other 12 tests still passed.

Restored (03f): the source is identical to 7c267e9, the hash is back to 789f64d7..., and
14/14 pass. The mutant was discarded with the scratch tree.

### 4. Account order and callers
target/idl/plotarmor.json order is registry_config, contract_artifact, contract_signature,
signer, system_program. This matches the struct order in the source. The demo
src/anchor/plotarmor.json is byte-identical to target/idl. The demo src/anchor/plotarmor.ts
matches target/types in content: it is prettier-formatted, and the only difference is how
one string literal is quoted.

All 11 call sites pass all five accounts (04d): tests/plotarmor.ts x5,
devnet_sign_contract_test.ts x1, devnet_sign_contract_adversarial_test.ts x4, and
plotarmor-demo ContractsApp.tsx:1202 at d9da574 (branches fix/sign-contract-registry-config
and feat/notifications). plotarmor-kora has no sign_contract caller or builder; its README
documents 5 accounts.

**Still on the old order:** plotarmor-demo main / origin/main (34fed7c) and
feat/wallet-bindings / origin/feat/wallet-bindings (5aaff08), at
src/ContractsApp.tsx:1198 (04e).

### 5. Build
A fresh extract of 7c267e9 was built with scripts/build.sh (pin v1.52) in an empty target
directory (3m49s for the counted build in 03a, and 5m34s for the first cold build in 05a, so both genuinely recompiled). The trimmed SHA-256 is
789f64d7a2f6ece13e600052877849a3fcb7d9b6637205bd997dd49dd43a4cf6. MATCH. The binary is
472,280 bytes (472,265 trimmed). It was reproduced three times in this run (05c, 03a,
03f), and the repo's existing target/deploy/plotarmor.so also matches.

HEAD 7c2b54d does NOT reproduce this hash: it builds to 33577f6b.... The two binaries
differ in exactly 2 bytes, the embedded `require!` source line numbers (76 to 81 and
79 to 84), shifted by the comment-only change in 7a3dc0b (05d). Deploy from 7c267e9 or
re-pin the expected hash. Do not build from HEAD and expect 789f64d7.

### Tests on the pinned binary
`cargo test`: 55/55 (1 + 11 + 35 + 8), EXIT=0 (03b). `cargo test --features mainnet`
against a freshly built mainnet .so (9c254990...): 55/55, EXIT=0 (03c). anchor test was
NOT re-run in this pass.

## Process notes
- The first test attempt failed with ENOSPC on the 1.8G /tmp tmpfs. That output is kept in
  00_failed_attempts_enospc/ and is not evidence of anything. The same folder records that
  a warm rebuild after `git archive | tar` silently reused a stale artifact, because the
  extracted files carry old commit timestamps. All counted runs used a fresh target
  directory, and each recorded the binary hash it tested against.
- `independent-run/` in this directory was written by a DIFFERENT agent (not this session)
  between 20:18 and 20:33 UTC. Its REPORT.md reaches the same split verdict. This session
  did not verify it and did not commit it. Its PREPARATION.md mentions a scratch extract at
  /home/sucka/plotarmor-demo/.m2-pass4-scratch. That path no longer exists (checked).
