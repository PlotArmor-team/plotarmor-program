# Technical demo video script (3:00 max)

For the Crypto World's Fair submission. Every on-screen step below exists in the merged
demo branch described in `DEMO_MERGE_PLAN.md`; each was checked against the code on
2026-10-11, not against a running deployment. Do a full dry run on the deployed app before
recording, and cut any scene that does not work live rather than fake it.

Network: Solana devnet. Program `3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2`.

## Prepare before recording

- Two small files: `draft_v1.pdf` and `draft_v2.pdf` (a real edit of v1), plus
  `draft_v1_tampered.pdf` (v1 with one changed word).
- A logged-in demo account with walletless registration on
  (`VITE_WALLETLESS_REGISTER=true`).
- A private browser window for the share-proof scene (proves no account is needed).
- Solana Explorer tab on devnet.
- Do not show `.env` files, the Supabase dashboard, or any URL containing `api-key=`.

## Script

### 0:00 to 0:15 Problem and claim
Screen: app home.
> "Writers send scripts to producers and contests with no proof of what they wrote and
> when. PlotArmor registers a fingerprint of each draft on Solana. The file stays
> encrypted and private; the chain holds the evidence."

### 0:15 to 1:00 Register a draft, no wallet needed
Screen: Works, Register a draft. Drop `draft_v1.pdf`, fill details, Register. Let the
progress steps play ("Encrypting on your device...", "Storing your encrypted file
securely...", "Recording your registration...").
> "The file is hashed and encrypted in the browser. Only the encrypted blob goes to IPFS.
> The writer never sees a wallet: a per-user signing key signs the claim, Kora pays the
> network fee and a PlotArmor rent wallet funds the accounts, so the writer needs no SOL.
> One transaction calls register_work_claim and creates the content artifact, the claim,
> the ownership record, the first version link and an anchor record."

Open "Verify independently" and show the SHA-256 fingerprint.

### 1:00 to 1:25 The transaction on Explorer
Screen: click the transaction link, Solana Explorer, devnet.
> "Here is the transaction: our program, register_work_claim, and the accounts it created.
> The timestamp comes from the chain clock, not from us."

### 1:25 to 1:50 Add a version, without forking history
Screen: open the work, register `draft_v2.pdf` as a new draft.
> "A new draft calls add_version. The client must name the current head of the chain;
> if two submissions race, the second one fails with StaleLineageHead instead of silently
> forking the history. Retries reuse the same intent nonces, so a retry cannot create a
> duplicate record."

### 1:50 to 2:30 Public proof, checked against the chain
Screen: Share proof of draft, Create and copy link. Paste into the private window.
> "Anyone can open this link without an account. The page reads the Solana transaction
> itself and shows the time and fingerprint from the chain, not from our database."

Check a file: drop `draft_v1.pdf`, show the match. Drop `draft_v1_tampered.pdf`, show
"Does not match".
> "The visitor's file is hashed on their own device and compared with the on-chain
> fingerprint. One changed word and it no longer matches."

### 2:30 to 2:50 Contracts and the provenance package
Screen: Contracts, a signed agreement linked to the work; then the work's provenance
package with transaction signatures.
> "Agreements are anchored the same way and signed with sign_contract. The provenance
> package collects drafts, agreements and transaction signatures into one document a
> lawyer can verify independently."

If the jurisdiction forms are shown, do not claim legal validity: they are marked pending
counsel review in the code.

### 2:50 to 3:00 What the chain proves
Screen: README section "What the chain proves, and what it does not", or one slide.
> "We are precise about it: the chain proves that a key registered this exact file at this
> time, and in what order versions followed. It does not prove who wrote it. Seven Anchor
> instructions, open test suites, devnet today."

## Do not say or show

- "Proves authorship" or "proves ownership". It proves registration by a key at a time.
- "Multi-signature" or "threshold approval". Thresholds are recorded, not enforced.
- That the pause fix or security.txt is live. The deployed program is `09c5bfc`.
- "Mainnet", "audited", "court-approved".
- `/vault/verify` as an on-chain check: it compares against the PlotArmor database. Use
  the share-proof page, which reads the chain.
- The PlotBot assistant, unless the `plotbot-chat` Edge Function is confirmed deployed.
