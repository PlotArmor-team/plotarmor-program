# M2 independent pass 4 — FAIL

Reviewed commit: `7c267e9689c0d335194f0f73fe4388c670b8509a`.
Program: `3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2` (devnet).
Run performed **2026-09-29 UTC**, using the user-requested `2026-09-30-m2-pass4` evidence path.

**Overall verdict: FAIL for unrestricted redeployment readiness.** The M2 program behavior, regression sensitivity, current corrected client, and exact cold-build hash pass. Two release issues remain: the remote frontend branches still contain the four-account caller, and the exact verified artifact contains explicitly prohibited placeholder security contact/policy values. These are rollout/pre-existing release issues, not a discovered bypass of the M2 guard. A PASS for the program logic alone must not be read as approval to deploy this artifact into the current client fleet.

| Requested check | Result |
| --- | --- |
| 1. Config seeds, canonical bump, ownership/type | PASS; exact same read-only constraint in all six consuming instructions; adversarial runtime checks pass |
| 2. Pause placement/error/ordering | PASS for behavior, with inaccurate original comment documented below |
| 3. Regression fails when guard removed | PASS; actual mutant SBF succeeds while paused, original regression fails; restored guard passes |
| 4. Source/IDL/current clients and all old callers | Current checkout and d9da574 PASS; remote main and wallet-bindings remain on old layout; Kora has no sign_contract builder |
| 5. Cold build and required trimmed SHA-256 | PASS, exact match |
| 6. Redeploy safety | FAIL: frontend coordination unresolved and explicit security metadata deployment gate remains |

No deployment or network transaction signing/broadcast occurred. LiteSVM transactions used disposable in-process test fixtures. Source repositories were not edited. The mutation and extra tests existed only in a scratch archive. Existing uncommitted evidence in the parent directory was preserved; this independent run does not adopt its conclusions as proof. Only this new `independent-run/` directory is intended for the evidence commit.

## 1. Config cannot be substituted

All program source line references in this report are at **7c267e9**, unless marked HEAD. [Raw source and caller quotations](logs/02_source_callers.txt), [pinned Anchor implementation](logs/03_anchor_validation.txt), [additional macro quotations](logs/04_caller_detail.txt), and [structural assertions](logs/19_static_assertions.txt) preserve file:line output.

`programs/plotarmor/src/instructions/sign_contract.rs:14-18`:

```rust
#[account(
    seeds = [b"config"],
    bump,
)]
pub registry_config: Account<'info, RegistryConfig>,
```

The same five-line block appears verbatim in `add_owner.rs:9-13`, `add_version.rs:18-22`, `anchor_authorized_contract.rs:18-22`, `anchor_evidence_contract.rs:17-21`, and `register_work_claim.rs:23-27`. No `mut`, unchecked account, explicit supplied bump, or `seeds::program` override is present. Initialization necessarily has different `init/payer/space` attributes (`init_registry_config.rs:9-16`); it is not one of the five other read-only consumers.

The **locked crate version is Anchor 1.0.2** (`Cargo.lock:245-248`), although CLI pin is 1.0.1. Its `anchor-syn/src/codegen/accounts/constraints.rs:1180-1204` uses `__program_id` and `Pubkey::find_program_address` for the bare bump. Its `anchor-lang/src/accounts/account.rs:314-323` rejects an owner unequal to `T::owner()` before deserializing; `anchor-attribute-account/src/lib.rs:132-139` implements that owner as `crate::ID`. `RegistryConfig` is a normal `#[account]` (`state.rs:3-10`), so its discriminator is checked too.

[Eight additional scratch tests](logs/18_adversarial_tests.txt) passed against the restored exact baseline SBF. Relevant raw results:

```text
PASS4 observed ConstraintSeeds (2006) err=InstructionError(0, Custom(2006))
PASS4 observed AccountOwnedByWrongProgram (3007) err=InstructionError(0, Custom(3007))
PASS4 observed AccountDiscriminatorMismatch (3002) err=InstructionError(0, Custom(3002))
PASS4 observed AccountNotInitialized (3012) err=InstructionError(0, Custom(3012))
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 8 filtered out
```

Cases include valid config bytes at a wrong program-owned address, a noncanonical but valid off-curve bump, wrong owner at the actual PDA, wrong discriminator, another program account in the config slot, and a missing config. No fake-config path was found under the checked program/runtime invariants. This does not claim resistance to a trusted upgrade authority replacing the entire program.

## 2. Pause placement and known limitation

`sign_contract.rs:76` is exactly:

```rust
require!(!ctx.accounts.registry_config.paused, PlotArmorError::Paused);
```

It precedes the content-hash check (`:79-82`), `Clock::get()` (`:84`), and signature-field assignments (`:86-91`). `error.rs:21-22` declares `#[msg("Program is paused")] Paused`; both IDLs and the runtime test confirm **6008**. The extra test with both `paused=true` and a wrong content hash returned `Paused (6008)`.

The original `sign_contract.rs:75` comment, **“First check, matching the other five instructions”**, is inaccurate. `add_owner.rs:53` also checks pause first. Four anchoring handlers check `assert_mode_allowed` first, then pause: `register_work_claim.rs:102,105`, `add_version.rs:76,79`, `anchor_authorized_contract.rs:78,81`, `anchor_evidence_contract.rs:66,69`. Current HEAD's later comment-only correction is recorded in [inventory/diff](logs/01_inventory.txt). This is not a functional defect in 7c267e9.

“First” means first **handler** check. Anchor's generated `try_accounts` runs before calling the handler (`anchor-syn/.../program/handlers.rs:121-135`), including signature-account `init` (`sign_contract.rs:39-46`). Account/initialization failures can precede `Paused`. Failed transactions roll back those changes; the regression checks that no program-owned ContractSignature remains.

**Known, not new:** `init_registry_config.rs:35` sets `paused=false`; no instruction sets it afterward. M2 safely reads the flag and does not require a setter to accept normal signing. Its operational usefulness as a pause control depends on a future way to set the flag. The test intentionally injects `paused=true` through LiteSVM, not through a production instruction. M2 adds no kill-switch activation mechanism.

## 3. Mutation proves the regression is non-vacuous

The unmodified exact-commit baseline passed **55/55** tests (1 unit + 11 happy-path + 35 security + 8 signing): [raw run](logs/13_baseline_tests_retry.txt).

`sign_contract_tests.rs:423-428` passes the correct hash, calls `expect_err("sign_contract must be rejected while the registry is paused")`, then checks `Paused, 6008`. `:430-440` checks no program-owned signature survives.

[Mutation patch](mutation.patch) removes **only** the one `require!` line in a scratch `git archive 7c267e9`. The test itself remains unchanged. We rebuilt the SBF using the pinned wrapper and recompiled the native test, which embeds the `.so` via `tests/common/mod.rs:49-51`. This avoids the false result of mutating Rust source while continuing to execute an old SBF.

[Raw mutant output](logs/15_mutant_regression.txt):

```text
thread 'paused_registry_rejects_sign_contract' ... panicked at programs/plotarmor/tests/sign_contract_tests.rs:427:10:
sign_contract must be rejected while the registry is paused: TransactionMetadata { ... }
test paused_registry_rejects_sign_contract ... FAILED
test result: FAILED. 0 passed; 1 failed; ... 7 filtered out
EXIT CODE: 101
```

The full log shows the program and system CPI both succeeded, including 14,214 compute units. The mutant trimmed hash was `3cc388f514e7da09da6662b884773bfb0a0f0547236511dc2146799b8f405e30`.

Restoring the guard and rebuilding produced **byte-for-byte equality** with the cold baseline. The [restored regression](logs/17_restored_regression.txt) passed 1/1. All 44 archived tracked files were verified restored byte-for-byte before scratch deletion. The mutant was discarded. [Driver and build logs](logs/14_mutation_driver.txt) preserve the sequence, hashes and exit codes.

Six extra test cases were copied from the pre-existing, uncommitted `../scratch_extra_tests.rs`, reviewed, and executed anew; two new cases cover a noncanonical bump and the legacy four-account layout. Their executed source is [saved here](scratch_extra_tests.rs). These eight tests supplement, rather than replace, the unchanged original regression.

## 4. Account order and callers

The exact expected order and flags are:

| Position | Account | Writable | Signer |
| --- | --- | --- | --- |
| 0 | registry_config | false | false |
| 1 | contract_artifact | false | false |
| 2 | contract_signature | true | false |
| 3 | signer | true | true |
| 4 | system_program | false | false |

Source declarations: `sign_contract.rs:18,34,46,49,51`. Program `target/idl/plotarmor.json:1081` and demo `src/anchor/plotarmor.json:734` begin the matching `sign_contract` entry; their entire parsed JSON objects are equal. Demo types have `signContract` at `src/anchor/plotarmor.ts:740`, with `registryConfig` first at `:744`. The target IDL is generated/untracked, so it was inspected independently rather than assumed to belong to the commit.

The [offline Anchor instruction construction](logs/05_encoded_callers_retry.txt) verifies actual account meta order, flags, and 40-byte instruction data for all three IDLs: program target, current demo, and demo commit d9da574. Anchor builds wire order from the IDL; JavaScript object insertion order is not itself proof.

Current demo HEAD `312c043` has one builder, `src/ContractsApp.tsx:1202`, with the canonical config derivation at `:1187` and first account at `:1204`. At **d9da574**, the corresponding builder is `:1199`, config is first at `:1201`; its IDL matches. All ten program TS call sites use the new list: `tests/plotarmor.ts:561,1103,1126,1138,1163`, `scripts/devnet_sign_contract_test.ts:155`, and `scripts/devnet_sign_contract_adversarial_test.ts:127,155,168,198`. The Rust helper includes `registry_config` first at `sign_contract_tests.rs:111`.

**Old callers still present:** demo `main` / `origin/main` at `34fed7c`, and `feat/wallet-bindings` / `origin/feat/wallet-bindings` at `5aaff08`. Each has `src/ContractsApp.tsx:1198` calling `.signContract`, with the four-account block at `:1199-1204` beginning `contractArtifact`; each corresponding `src/anchor/plotarmor.json` has the four-account IDL. These are two distinct branch implementations, with their local/remote aliases. [Fresh remote refs](logs/06_remote_refs_retry.txt) confirmed those commit IDs; the requested fix/notifications remote branch names did not exist. No merge, push, or release was performed.

The scratch legacy-layout test returned `AccountDiscriminatorMismatch (3002)` on `registry_config` against the new binary, proving that the old call will fail after upgrade. Conversely, per the supplied deployment state, a five-account caller is ahead of the currently deployed four-account binary. Coordinating the frontend release with the program upgrade is required. This audit did not establish which browser bundle is currently served, so it does not claim that the deployed frontend has been upgraded.

Kora has **no sign_contract instruction builder** in either tracked scripts or the current untracked stateful probe; no old Kora caller was found. `scripts/verify_stateful_signing.mjs:27-31` defines only add_version/add_owner/anchor_authorized_contract layouts and `:16` reads the sibling program IDL. `README.md:341` documents five accounts, and `:561-562` explicitly says sign_contract is unprobed and needs M2 alignment. Thus Kora is N/A for caller migration, not a verified live sign_contract pass. Generic transaction relaying is not an independently constructed sign_contract account list.

## 5. Exact cold build

A fresh `git archive 7c267e9` was extracted to `/home/<usr>/plotarmor-demo/.m2-pass4-scratch` with **no target directory**. Existing dependency downloads/toolchain installations were reused, but no compiled target artifacts were copied. Build command:

```text
NO_DNA=1 bash scripts/build.sh -- --locked --offline
platform-tools pin: v1.52  (mode: devnet)
Finished `release` profile [optimized] target(s) in 6m 31s
EXIT CODE: 0
```

[Full cold compiler output](logs/10_cold_build.txt), [hash computation](logs/12_cold_hash.txt), [artifact](plotarmor-7c267e9.so), and [hash script](hash.py) are included. Pins: host Rust 1.96.0, Solana CLI 4.0.1, Anchor CLI 1.0.1, SBF platform-tools v1.52 (Rust 1.89.0 toolchain), locked Anchor crates 1.0.2. No mainnet feature was passed.

```text
Full length: 472280
Full SHA256: 27998e6f6437e7998bf35fffb65cde8a8599cf541fcb01fba509baafbc22e231
Trim method: bytes.rstrip(b"\0")
Trimmed length: 472265
Trimmed SHA256: 789f64d7a2f6ece13e600052877849a3fcb7d9b6637205bd997dd49dd43a4cf6
MATCH: True
```

The pinned wrapper, lockfile, toolchain file, Anchor config and source were checked against the commit. The initial native test compile raced the cold SBF build and failed because `target/deploy/plotarmor.so` did not yet exist; [that raw failure](logs/11_baseline_tests.txt) is retained. The full retry after the artifact existed passed 55/55. No test source was changed to obtain that pass. Previously recorded mainnet 55/55 and Anchor 34/34 are historical inputs, not newly rerun/claimed results of this pass.

## 6. Remaining release issues and bounds

**Explicit existing release gate:** `programs/plotarmor/src/lib.rs:38-41` says the security contacts/policy are unresolved and **“Do NOT deploy until Milan supplies both values.”** The compiled values at `:52-53` are:

```rust
contacts: "email:UNSET-PLACEHOLDER-DO-NOT-DEPLOY@example.invalid",
policy: "UNSET-PLACEHOLDER-DO-NOT-DEPLOY",
```

Both occur in the exact cold artifact (confirmed in [static assertions](logs/19_static_assertions.txt)). This was not introduced by M2. Replacing them changes the artifact hash and requires a new reviewed build/hash; the successful requested hash cannot also prove corrected metadata. This audit does not modify those values or waive the existing release gate.

Fresh [read-only devnet metadata](logs/07_devnet_readonly_retry.txt) reports last deploy slot 476301346, upgrade authority `EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd`, and program data length 471,960 bytes. The new full artifact is 472,280 bytes, **320 bytes larger**; the eventual upgrade must accommodate program-data extension and rent. This is a deployment prerequisite, not evidence of a protocol vulnerability or a claim that the CLI cannot extend automatically. No upgrade simulation/deployment was attempted.

The [fresh config response](logs/08_devnet_config.txt) was checked for program owner, 44-byte length, and discriminator before decoding: schema version 1, modes 0, paused false. There is no account-layout migration in the source delta. Config existence is a new sign_contract precondition, but both instructions that create ContractArtifact already require it, and this program exposes no config close instruction. No additional M2-specific authorization bypass, persistence failure, or source change beyond the reviewed delta was found in this bounded pass.

Tool/environment failures are preserved in raw logs, with successful retries where needed: DNS/RPC restrictions, Node Git subprocess EPERM, the early missing-SBF compile, and a no-match `rg` exit in inventory. A Solana MCP auto-install attempt could not launch the locally busy `claude` executable; the audit instead inspected the actual locked dependency source and official [Anchor account constraints](https://www.anchor-lang.com/docs/references/account-constraints) / [account types](https://www.anchor-lang.com/docs/references/account-types) documentation. The local versioned source and empirical runtime checks are the decisive evidence.

The next review must distinguish fixing the release blockers from the already proven M2 runtime behavior. This **FAIL** is not a request to remove registry_config or weaken the guard.
