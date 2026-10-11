# plotarmor-demo: merge plan for the hackathon submission

Prepared 2026-10-11. Analysis only: every merge below was run in a local scratch worktree
of `PlotArmor-team/plotarmor-demo` and nothing was pushed. Commit ids refer to that repo.

## Problem

`main` ends at `34fed7c` (2026-09-10). The hackathon work is spread over four branch tips
and no branch contains all of it. Every other feature branch (`feat/saas-ui`,
`feat/sponsored-register`, `feat/provenance-package`, `feat/film-index`, `fix/cors-open`)
is already fully contained in both `feat/release` and `feat/copilot`.

| branch | tip | unique content |
|---|---|---|
| `feat/release` | `4eec0dc` | base; 9 commits not on copilot: Settings, key export and rotation, PlotArmor key or own wallet, walletless-always, official forms per jurisdiction |
| `feat/copilot` | `3e474c0` | 7 commits not on release: PlotBot assistant, package checklist, `plotbot-chat` Edge Function |
| `feat/wallet-bindings` | `5aaff08` | session-bound wallet identity verification (Edge Function, scripts, docs) |
| `release/demo-ui` | `0c71e63` | an earlier registration progress screen |

## Recommended merge

Branch from `feat/release`, e.g. `release/hackathon`.

### Step 1: merge `feat/wallet-bindings`. Clean, no conflicts.
Adds 6 files (`docs/wallet-binding.md`, two scripts, `supabase/functions/wallet-binding/`).
Its migration `20260914164500_wallet_identity_bindings.sql` is already on `feat/release`,
byte-identical, and `docs/wallet-binding.md` records it as applied to Supabase.
No frontend code calls the `wallet-binding` function, so this adds nothing visible in the
demo. Merge it so the code matches the disclosure, but do not demo or describe it as a
user-facing feature.

### Step 2: merge `feat/copilot`. 4 files, 5 conflict hunks, resolutions below.
- `src/tests/edgeCors.test.ts`: take copilot. It is release's list plus
  `"plotbot-chat/handle.ts"`.
- `src/index.css` (1 hunk): both sides appended new CSS at the end of the file and the
  common ancestor is empty there. Keep both blocks, release first, then copilot.
- `src/features/provenance/ProvenancePackagePage.tsx` (2 hunks):
  - imports: keep both import groups (release: preferences and official forms; copilot:
    checklist, package facts, PlotBot).
  - state: take copilot's block (`linkedAgreements`, derived `agreements`,
    `coOwnerWallets`) but keep release's default:
    `useState(defaults.provenance.includeOriginal)` instead of `useState(true)`.
    Checked: after the merge nothing calls `setAgreements` any more, so the derived
    `agreements` value is safe.
- `src/SaasShell.tsx` (1 hunk): copilot restructured the navigation; release changed only
  two lines. Take copilot's file, then reapply release's two changes:
  - add `import { usePreferences } from "./settings/preferences";`
  - `const { preferences } = usePreferences();` and
    `const name = profile?.full_name || preferences.profile.displayName || user?.email || "Your account";`
  - Profile menu button: `go(\`${MODULE.PROFILE}#profile\`)` instead of `go(MODULE.PROFILE)`.

### Step 3: do NOT merge `release/demo-ui`.
It conflicts in 6 files with 38 hunks (19 in `src/vault/UploadFlow.tsx`). It is a
2026-10-05 progress screen that was superseded the next day: `feat/release` already has its
own `RegistrationProgress` component (`src/RegistrationUI.tsx`) from the SaaS UI work.
Merging would mean hand-resolving the registration flow against a newer version for no
user-visible gain, the day before the deadline.

## Results of the scratch merge (steps 1 and 2)

Same checks run on three trees in this environment (Node 22.22.0, npm 10.9.4):

| check | `feat/release` | `feat/copilot` | merged |
|---|---|---|---|
| `eslint src/` | 0 problems | 0 problems | 0 problems |
| `tsc --noEmit` | 1 error | 1 error | 1 error (the same one) |
| `vitest run` without env | 518/518, 2 files not loaded | 587/587, 3 files not loaded | 647/647, 2 files not loaded |
| `vitest run` with dummy Supabase env | 525/525, 40/40 files | not run | **654/654, 46/46 files** |
| `vite build` | ok | ok | ok |

No test file from either branch is missing in the merged tree. "Not loaded" files failed at
import with `supabaseUrl is required` because no `.env` exists here; with dummy values
(`VITE_SUPABASE_URL=http://127.0.0.1:54321`, `VITE_SUPABASE_ANON_KEY=dummy-test-key`) every
file loads and passes. No real keys were used.

Verification count: 1 pass, one local environment. Not run: Playwright e2e, any live
Supabase or devnet check, a Vercel preview.

## Already broken before the merge (on both branches)

1. `npm ci` fails: package-lock.json is out of sync with package.json (`utf-8-validate`,
   `@types/react@19.3.0` missing). Observed with npm 10.9.4; not checked with the npm
   version that wrote the lockfile. `npm install` works. Fix: run `npm install` once with the
   team's npm version and commit the lockfile.
2. `tsc --noEmit` fails: `src/WalletContext.tsx(17,6): TS2786 'ConnectionProvider' cannot be
   used as a JSX component`. Because the repo's `npm run ci` runs typecheck before tests,
   `npm run ci` fails on both branches today. `vite build` does not typecheck, so it still
   builds.
3. Two test files need Supabase env vars to load at all (see above).

## Before the demo goes live

- Check which branch Vercel builds for production; the analysis did not cover Vercel.
- PlotBot needs the `plotbot-chat` Edge Function deployed and its provider key set as a
  Supabase secret. Whether that is done is not visible from git. If not, leave PlotBot out
  of the video rather than show an error.
- Walletless registration needs `VITE_WALLETLESS_REGISTER=true` in the deployment.
- Smoke test after deploying the merged branch: sign up, register a draft, add a version,
  create a share-proof link and check a file on it in a private window, generate a
  provenance package.

## Security note found during the analysis (pre-existing, not caused by the merge)

`src/solana.ts` builds the RPC URL from `import.meta.env.VITE_HELIUS_API_KEY`, present since
`4e174f4` (2026-07-04). Vite inlines every `VITE_` variable into the public JavaScript
bundle, so if this variable is set in Vercel, the Helius key is readable by every visitor.
Whether it is set was not checked. The demo repo's own CLAUDE.md forbids exposing the Helius
key. Options: route RPC through an Edge Function, or check whether Helius lets you restrict
the key to your domains, and rotate the key once it is no longer in the bundle.
