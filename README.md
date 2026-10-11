# PlotArmor Anchor Program

On-chain evidence layer for PlotArmor: creators register a hash of their work (screenplays,
treatments, scores, contracts) on Solana and get a timestamped, tamper-evident record of
who claimed what, when, and how each version follows from the last. The file itself never
goes on-chain; only its SHA-256 hash and an optional IPFS CID digest do.

**Status: devnet prototype. Not deployed to mainnet. Not externally audited.**

| | |
|---|---|
| Program ID (devnet) | `3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2` |
| Explorer | https://explorer.solana.com/address/3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2?cluster=devnet |
| Framework | Anchor 1.0.1, Rust, platform-tools v1.52 (pinned) |
| Deployed binary | built from commit `09c5bfc`, last upgrade 2026-07-14 |
| Product app | `PlotArmor-team/plotarmor-demo` (web vault that calls this program) |
| Fee sponsorship | `MJ-Frictionless-NTWRK/plotarmor-kora` (Kora relayer, devnet) |

## What the program does

Seven instructions. Four of them create an `AnchorRecord`, the uniform "this happened at
this time" receipt that an indexer can follow.

| Instruction | Creates | Who may call |
|---|---|---|
| `init_registry_config` | `RegistryConfig` singleton | program upgrade authority only |
| `register_work_claim` | `ContentArtifact`, `WorkClaim`, `Ownership`, first `OwnerRecord`, root `ClaimArtifactLink`, `AnchorRecord` | any wallet (becomes claimant) |
| `add_version` | new `ContentArtifact` (if new bytes), `ClaimArtifactLink`, `AnchorRecord` | the claimant |
| `add_owner` | `OwnerRecord` | the `Ownership.admin` |
| `anchor_evidence_contract` | `ContractArtifact`, `EvidenceAnchor`, `AnchorRecord` | any wallet (unilateral) |
| `anchor_authorized_contract` | `ContractArtifact`, `AuthorizedContractAnchor`, `AnchorRecord` | the `Ownership.admin` |
| `sign_contract` | `ContractSignature` | any wallet |

### Design points worth reviewing

- **Content addressing.** `ContentArtifact` is seeded by `SHA-256("plotarmor:raw:v1\n" || bytes)`.
  Two people registering identical bytes converge on one artifact but get separate
  `WorkClaim`s, so the chain shows both claims and their order.
- **Version lineage without forks.** Each version is a `ClaimArtifactLink` pointing at the
  previous link. `add_version` must be given the link the client believes is the current
  head and reverts with `StaleLineageHead` (6001) if it is not. This blocks silent forks
  from concurrent or replayed submissions, and it still allows reverting to an earlier
  file, because the same artifact may appear twice in one chain.
- **Idempotent retries.** `link_nonce` and `anchor_nonce` are client intent nonces,
  generated once per user action and reused on retry, so a resubmitted transaction cannot
  create a duplicate record.
- **`init_if_needed` hardening.** Shared artifacts carry an explicit `is_initialized` flag so
  a second call can never overwrite fields.
- **Environment binding.** Every record stores an `anchor_mode`. Mainnet builds (Cargo
  feature `mainnet`) reject `Simulated` and `AttestedDevnet` in compiled code; devnet
  builds reject `AttestedMainnet`. No config account can turn this off.
- **Program-captured time.** Timestamps and slots come from `Clock`, never from arguments.
- **No close instruction** exists for any account. Records are permanent by design.
- **On-chain `security.txt`** in source (added in `0debdaa`, real contact values since
  `14815bb`; not yet in the deployed binary, see Deployment state).

## What the chain proves, and what it does not

This matters more than any feature, because the records may end up in front of a court.

| Record | Proves | Does NOT prove |
|---|---|---|
| `WorkClaim` | this wallet registered this hash at this time | that the wallet holder wrote the work |
| `ContractSignature` | this wallet signed this contract hash | that a contract party signed; any funded wallet may sign |
| `Ownership.threshold_shares`, `OwnerRecord.share` | what the parties stated | any enforcement; no instruction reads these to authorize anything |
| `EvidenceAnchor.asserted_work_claim` | that the anchorer asserted a link | that the link is real; the referenced work is never loaded or checked |
| `AuthorizedContractAnchor` | the work's `Ownership.admin` approved it | multi-party approval; it is a single admin key today |

Known v1 limitations are listed with reasoning in `AUDITOR_BRIEF.md` and `CLAUDE.md`
(items A to I). The most important: authorization is single-key (claimant or admin);
threshold governance is deferred pending a custody-model decision with counsel.
`add_version` AnchorRecords are content-scoped, so a front-runner can force a retry with a
fresh nonce (documented griefing vector, recoverable, pinned by a test).

## Deployment state (devnet)

- The deployed binary is commit `09c5bfc`. Rebuilding that commit with
  `--tools-version v1.52` from a clean target directory reproduced the deployed bytes
  exactly (recorded 2026-09-03 in `CLAUDE.md`).
- Source on `main` is ahead of the deployment by two changes: `sign_contract` now honours
  the registry pause flag (audit finding M2), and `security.txt` was added. The upgrade is
  prepared and rehearsed on a local validator (`docs/CUTOVER_2026-10.md`,
  `docs/evidence/`) but has **not** been executed on devnet.
- Not verifiable through `solana-verify` yet: the source repository is private and remote
  verification is mainnet-only.

## Tests

Two layers, both in this repository:

- **Rust / LiteSVM** (`programs/plotarmor/tests/`): `happy_paths.rs`, `security_tests.rs`,
  `sign_contract_tests.rs`. 56 `#[test]` functions, some feature-gated so devnet and
  mainnet builds each run their own environment checks. Last recorded run: 55 passing per
  build, 2026-10-06.
- **TypeScript / Mocha on a local validator** (`tests/plotarmor.ts`): 34 tests covering every
  instruction and every reachable error code. Last recorded run: 34/34, 2026-09-17.
- **Live devnet scripts** (`scripts/`): `measure_devnet.ts` (24 scenarios including
  adversarial ones), `devnet_ext_ref_hash_test.ts`, `devnet_sign_contract*_test.ts`.

Results above are as recorded in `CLAUDE.md` and `evidence/` on the stated dates. Rerun
them rather than trusting this file.

```bash
yarn install
scripts/build.sh            # devnet build, pins platform-tools v1.52
cargo test                  # Rust / LiteSVM
anchor test                 # TypeScript on a local validator (Surfpool by default)
```

`cargo test --features mainnet` additionally needs a mainnet build in
`target/deploy-mainnet/` (`scripts/build.sh --mainnet`).

## Repository map

| Path | Content |
|---|---|
| `programs/plotarmor/src/` | program source: `state.rs` accounts, `instructions/` handlers, `helpers.rs` anchor-mode gate (`assert_mode_allowed`) |
| `programs/plotarmor/tests/` | LiteSVM tests |
| `tests/plotarmor.ts` | Anchor / Mocha tests |
| `scripts/` | build wrapper, devnet proof scripts, call-site checkers |
| `AUDITOR_BRIEF.md` | invariants, error codes, limitations, audit focus areas |
| `docs/CUTOVER_2026-10.md` | devnet upgrade runbook (prepared, not executed) |
| `evidence/` | raw logs from independent verification passes, with SHA256SUMS |
| `CLAUDE.md` | build canon: PDA seeds, account layouts, locked enum values, decision log |

## Security

Report issues privately to info@plotarmor.io. See `SECURITY.md`.
