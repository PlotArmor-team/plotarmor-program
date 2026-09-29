# security.txt placeholders replaced (commit 14815bb)

Run 2026-09-29 UTC. Not deployed, not extended, not pushed.

## 1. Values and prerequisites
- https://plotarmor.io responds: HTTP/2 200, served by Cloudflare, final URL
  https://plotarmor.io/ (01).
- solana-security-txt 1.1.3 accepts free text for `policy`. Its README.md:147 says:
  "`policy` | link/text (required) | Either a link or a text document describing the
  project's security policy." The macro (src/lib.rs:19-28) concatenates
  `stringify!($name), "\0", $value, "\0"` with no validation. The parser (src/parser.rs:217-219)
  only requires that the field is present and stores it as a `String`. The one real constraint
  is that a value must not contain a NUL byte, and this text has none (02).
- lib.rs `security_txt!` now reads: name "PlotArmor", project_url "https://plotarmor.io",
  contacts "email:info@plotarmor.io", policy exactly as supplied, source_code "private".
- SECURITY.md was added at the repo root with the same policy text and contact.
- Commit 14815bb touches ONLY programs/plotarmor/src/lib.rs and SECURITY.md.

**Beyond the literal brief:** the comment directly above the block said "WARNING ...
UNRESOLVED PLACEHOLDERS ... Do NOT deploy until Milan supplies both values" and "project_url
... intentionally private". Both would have been false next to the new values, so that
comment was rewritten in the same lib.rs edit. It is comment only, but it does appear in
the diff below.

## 2. Two cold builds, pinned v1.52 (03a, 03b)
Each build started from its own fresh `git archive 14815bb` extract, with an empty target
directory, and ran scripts/build.sh. Both took 4m46s.

| build | file bytes | trimmed bytes | trimmed SHA-256 |
|---|---|---|---|
| a | 472,440 | 472,425 | bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2 |
| b | 472,440 | 472,425 | bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2 |

The two builds are identical. Full-file SHA-256 of both:
97880b057e52f474f20bb209f586e708eaf96d5608bcc52403ca62bc396916b7.

The repo's own target/deploy/plotarmor.so, which the tests below ran against, has the same
hash before and after anchor test (04a, 04c).

(The `platform-tools v1.53` line in the logs is `cargo build-sbf --version` reporting its
default. build.sh passes `--tools-version v1.52`, as the "pin: v1.52" line shows.)

A first attempt at these builds never ran because of a variable-name bug in the driver
script: `$x_cold_build_` was parsed as one variable. The builds were rerun; nothing from the
failed attempt is counted.

## 3. Tests
| suite | result |
|---|---|
| cargo test (devnet build, bcea64bb...) | 55 passed, 0 failed (1 + 11 + 35 + 8), EXIT=0 (04a) |
| cargo test --features mainnet (mainnet .so 79a7d1cd..., 472,944 bytes) | 55 passed, 0 failed, EXIT=0 (04b) |
| anchor test --skip-build (Surfpool 1.3.1, anchor-cli 1.0.1) | 34 passing, EXIT=0 (04c) |

`--skip-build` was used so that anchor test deployed exactly the hashed binary.

## 4. Program diff since 7c267e9 (05)
Only two files changed:
- sign_contract.rs: the earlier comment-only fix (7a3dc0b).
- lib.rs: the security_txt values and the comment above them.

No logic lines changed.

## 5. Size vs devnet (06)
- The new binary is 472,440 bytes (472,425 trimmed).
- Live ProgramData capacity is 471,960 bytes (read 2026-09-29).
- **Shortfall: 480 bytes** (465 trimmed). `solana program deploy` writes the whole file, so
  plan for 480.
- The exact minimal command would be
  `solana program extend 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 480`. It was NOT run.
- Rent: `solana rent` on devnet gives 2,400,874,040 lamports for the needed 472,485-byte
  ProgramData account. The account already holds 3,286,045,680 lamports, so it appears to
  cover the larger size without a top-up. This is inferred and has not been checked by
  running an extend.
- CLAUDE.md (line 660) calls the 2026-07-03 +10,240-byte extend an "ExtendProgram minimum
  increment". Nothing in `solana program extend --help` for CLI 4.0.1 states a minimum.
  Treat that claim as unverified.
- `solana program deploy` auto-extends unless `--no-auto-extend` is passed. The
  `write-buffer` + `upgrade` path does not auto-extend.

## Verification count
- The binary builds reproducibly: 2 independent cold builds match.
- The tests pass once each on this commit.
- No independent re-audit and no live devnet check have run on 14815bb. By the CLAUDE.md
  standard, the deployable binary is verified once or twice, not four times.
