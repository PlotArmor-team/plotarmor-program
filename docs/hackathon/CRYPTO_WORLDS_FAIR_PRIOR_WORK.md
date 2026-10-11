# Crypto World's Fair: prior work disclosure

Prepared 2026-10-11 from the git history of the three PlotArmor repositories. Every count
and date below was read from git, not estimated. Commit dates are author dates.

Hackathon window used here: 2026-09-14 to 2026-10-12, 11:59pm PT. This window was taken
from secondary sources; confirm it against the official rules before submitting.

## Short version (for the submission form)

PlotArmor was started before the hackathon and we are disclosing that in full.

Before 2026-09-14: the Solana Anchor program (all seven instructions, account model,
version-lineage and anti-fork checks, Rust and TypeScript test suites) was built between
June and early September 2026 and has been on devnet since June. The web app
(plotarmor-demo) existed since March 2026 with upload, client-side encryption, IPFS
storage, wallet connection, on-chain registration and contract anchoring. A Kora
fee-sponsorship deployment was scaffolded on 2026-09-10 and 2026-09-11.

During the hackathon (2026-09-14 to 2026-10-12): in the web app, 53 commits between
2026-09-14 and 2026-10-11 touching 284 files (the main release branch alone differs from
the pre-hackathon state by about 44,000 added and 11,000 removed lines): session-bound
wallet identity verification, a new SaaS interface, walletless draft registration with sponsored fees through Kora, provenance
packages with per-jurisdiction court documents, public share-proof verification links, the
Film Index, a six-language interface, PlotBot (an in-app assistant), and key management
settings. In the fee-sponsorship repo, 3 commits: a devnet rent-sponsorship spike and a
sponsored registration script with live devnet evidence. In the program repo, no
instruction or logic change: an independent re-audit of the pause fix, the real
security.txt contact values, and a prepared and locally rehearsed devnet upgrade runbook.

## Detail by repository

### plotarmor-program (Solana Anchor program)

| | before window | in window |
|---|---|---|
| commits on `main` | 81 (2026-06-08 to 2026-09-04) | 16 (2026-09-17 to 2026-10-07) |
| program source changes | all of it | 2 files, 15 lines added, 11 removed |

Before the window:
- Entire program: `init_registry_config`, `register_work_claim`, `add_version`, `add_owner`,
  `anchor_evidence_contract`, `anchor_authorized_contract`, `sign_contract`.
- LiteSVM and Mocha test suites, devnet proof scripts.
- All devnet deploys (first 2026-06-11, last 2026-07-14, binary from commit `09c5bfc`).
- Audit fix M2 (`sign_contract` honours the pause flag), commit `7c267e9`, 2026-09-04.
- `security.txt` added with placeholder values, commit `0debdaa`.

In the window:
- `14815bb`: real contact and policy in `security.txt` (placeholder replacement).
- `7a3dc0b`: comment correction in `sign_contract.rs`, no code change.
- Independent re-audit of the M2 fix with mutation testing (`bc729e9`, `b6a0d9a`,
  `evidence/2026-09-30-m2-pass4/`).
- Devnet upgrade runbook, rehearsal on a local validator seeded from devnet, and an
  independent verification of that rehearsal (`docs/CUTOVER_2026-10.md`,
  `docs/evidence/`). The upgrade itself has NOT been executed.
- Documentation corrections.

### plotarmor-demo (web app, PlotArmor-team/plotarmor-demo)

| | before window | in window |
|---|---|---|
| commits | 205 on `main` (2026-03-03 to 2026-09-10) | 53 on feature branches (2026-09-14 to 2026-10-11) |

Before the window: upload flow with client-side encryption, IPFS storage via Pinata through
a Supabase Edge Function, wallet adapter, on-chain `register_work_claim` / `add_version`,
contract generation and anchoring, contract signing, co-ownership, provenance certificate,
E-SIGN consent and legal pages, signup and landing pages.

In the window (none of it is on `main` yet; see the note below):
- Session-bound wallet identity verification (`5aaff08`, 2026-09-14 13:15 PT).
- SaaS interface: app shell, Works and Contracts tables, registration progress screen,
  brand theme.
- Walletless draft registration with network fees sponsored through Kora (devnet,
  marked provisional in the commit).
- Provenance package v2: jurisdiction profiles, court PDF, archive, verification kit, full
  draft timeline, official forms per jurisdiction (marked pending counsel review).
- Share proof: public verification link per registered draft.
- Film Index: data model, Wikidata import, PlotArmor feeding the index, poster images.
- Works: loglines and credits, signed agreements on the work page, Concepts structure.
- Six-language interface and translated provenance packages.
- PlotBot: in-app help assistant with an Edge Function backend and switchable provider.
- Settings: language, appearance, profile, export of the signing key, key rotation,
  choice between the PlotArmor key and the user's own wallet.
- Shared CORS helper for Edge Functions.

### plotarmor-kora (fee sponsorship, public)

| | before window | in window |
|---|---|---|
| commits | 6 (2026-09-10 to 2026-09-14 01:36 CEST, which is 2026-09-13 PT) | 3 (2026-09-30 to 2026-10-06) |

Before the window: pinned Kora deployment scaffolding for Render, signing probes, two
provisional live signing passes.

In the window: devnet rent-sponsorship spike with raw evidence, allowing three signatures
for sponsored registration, and the sponsored work registration script with devnet
evidence.

## Before submitting

- **The hackathon work in plotarmor-demo is not on `main`, and no single branch has all
  of it.** `main` ends at 2026-09-10. The 53 in-window commits are spread over four
  branches, and a judge opening the repository sees `main` by default:
  - `feat/release`: most of the work; the only branch with Settings (language, key export,
    key rotation, PlotArmor key or own wallet), walletless-always mode and the official
    forms per jurisdiction (9 commits not on `feat/copilot`).
  - `feat/copilot`: the only branch with PlotBot (7 commits not on `feat/release`,
    including `5c3f71a` and `3e474c0`).
  - `release/demo-ui`: the only branch with `0c71e63` (registration progress screen).
  - `feat/wallet-bindings`: the only branch with `5aaff08` (wallet identity verification).
  Merge what should be judged into one branch, test it, and link that branch, or merge
  to `main`. Otherwise do not list features that are not on the linked branch.
- Grant the judges access to private repositories as the official rules require, or
  submit the public plotarmor-kora repository and describe the others.
- The program upgrade (M2 fix and security.txt) is not deployed. Demo against the deployed
  binary `09c5bfc`; do not describe the pause fix as live.
