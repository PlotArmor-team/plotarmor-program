````bash
mkdir -p .cutover-pass3/old .cutover-pass3/head; git archive 09c5bfc | tar -x -C .cutover-pass3/old; git archive HEAD | tar -x -C .cutover-pass3/head
````
````text
exit_code=0
````

````bash
date -u; git status -sb; git rev-parse HEAD 09c5bfc f34bfae; git diff f34bfae HEAD -- programs Cargo.toml Cargo.lock Anchor.toml scripts rust-toolchain.toml; solana --version; anchor --version
````
````text
Wed Oct  7 09:09:27 UTC 2026
## main...origin/main
?? .cutover-pass3/
?? docs/evidence/2026-10-07-cutover-pass3.md
45476ce24406c816f37232464c5d497f09aaed70
09c5bfca2760c5b66b76b96ec08cf54dfe03acf0
f34bfae5f20d31fabd39c1d7c73140ce9994d846
diff --git a/scripts/guard_deploy_artifact.sh b/scripts/guard_deploy_artifact.sh
new file mode 100755
index 0000000..faa56e0
--- /dev/null
+++ b/scripts/guard_deploy_artifact.sh
@@ -0,0 +1,30 @@
+#!/usr/bin/env bash
+# Refuse to continue unless the program artifact is exactly the audited build.
+#
+# Compares the sha256 of the .so with trailing zero bytes stripped (the on-chain program
+# buffer is zero padded, so only the trimmed hash is comparable across a dump and a build)
+# against the hash recorded in docs/CUTOVER_2026-10.md for commit f34bfae built with
+# platform-tools v1.52 via scripts/build.sh --anchor.
+#
+# usage: scripts/guard_deploy_artifact.sh [path-to-so]   (default target/deploy/plotarmor.so)
+# exit 0 on match, exit 1 on mismatch or a missing file. Chain the deploy after it with &&.
+# Needs python3. Update EXPECT only together with a new audited build and runbook.
+set -u
+EXPECT="bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2"
+SO="${1:-target/deploy/plotarmor.so}"
+
+if [ ! -f "$SO" ]; then
+  echo "REFUSING: $SO does not exist. Build it first: scripts/build.sh --anchor" >&2
+  exit 1
+fi
+
+GOT="$(python3 -I -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read().rstrip(b"\0")).hexdigest())' "$SO")" || exit 1
+
+if [ "$GOT" = "$EXPECT" ]; then
+  echo "artifact OK: $SO trimmed sha256 $GOT"
+  exit 0
+fi
+
+echo "REFUSING: $SO trimmed sha256 is $GOT" >&2
+echo "          expected                $EXPECT" >&2
+exit 1
solana-cli 4.0.1 (src:e4e3aa49; feat:6ff76655, client:Agave)
anchor-cli 1.0.1

exit_code=0
````

````bash
test ! -e .cutover-pass3/old/target && test ! -e .cutover-pass3/head/target && echo "Both build targets absent: cold builds"; cd .cutover-pass3/old && NO_DNA=1 anchor build
````
````text
Both build targets absent: cold builds
Error: Program ID mismatch detected for program 'plotarmor':
  Keypair file has: Aq2heixRhSusZ5x26dBh3A4gqYfDuAABQongKGVKJRwL
  Source code has:  3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2

Please run 'anchor keys sync' to update the program ID in your source code or use the '--ignore-keys' flag to skip this check.

exit_code=1
````

````bash
cd .cutover-pass3/old && NO_DNA=1 anchor build --ignore-keys
````
````text
   Compiling proc-macro2 v1.0.106
   Compiling quote v1.0.45
   Compiling unicode-ident v1.0.24
   Compiling serde_core v1.0.228
   Compiling hashbrown v0.17.1
   Compiling winnow v1.0.3
   Compiling equivalent v1.0.2
   Compiling toml_datetime v1.1.1+spec-1.1.0
   Compiling serde v1.0.228
   Compiling cfg_aliases v0.2.1
   Compiling once_cell v1.21.4
   Compiling borsh v1.6.1
   Compiling five8_core v1.0.0
   Compiling indexmap v2.14.0
   Compiling solana-define-syscall v4.0.1
   Compiling solana-define-syscall v5.1.0
   Compiling sha2-const-stable v0.1.0
   Compiling five8 v1.0.0
   Compiling five8_const v1.0.0
   Compiling solana-atomic-u64 v3.0.1
   Compiling solana-sanitize v3.0.1
   Compiling bs58 v0.5.1
   Compiling version_check v0.9.5
   Compiling autocfg v1.5.1
   Compiling typenum v1.20.1
   Compiling toml_parser v1.1.2+spec-1.1.0
   Compiling syn v2.0.117
   Compiling generic-array v0.14.7
   Compiling num-traits v0.2.19
   Compiling anyhow v1.0.102
   Compiling toml_edit v0.25.12+spec-1.1.0
   Compiling syn v1.0.109
   Compiling thiserror v1.0.69
   Compiling crypto-common v0.1.7
   Compiling block-buffer v0.10.4
   Compiling digest v0.10.7
   Compiling cfg-if v1.0.4
   Compiling cpufeatures v0.2.17
   Compiling proc-macro-crate v3.5.0
   Compiling unicode-segmentation v1.13.3
   Compiling heck v0.3.3
   Compiling sha2 v0.10.9
   Compiling solana-program-memory v3.1.0
   Compiling feature-probe v0.1.1
   Compiling zmij v1.0.21
   Compiling bv v0.11.1
   Compiling solana-msg v3.1.0
   Compiling serde_json v1.0.150
   Compiling memchr v2.8.1
   Compiling log v0.4.32
   Compiling itoa v1.0.18
   Compiling lazy_static v1.5.0
   Compiling serde_bytes v0.11.19
   Compiling keccak-const v0.2.0
   Compiling solana-define-syscall v3.0.0
   Compiling const-crypto v0.3.0
   Compiling solana-program-option v3.1.0
   Compiling base64 v0.21.7
   Compiling serde_derive v1.0.228
   Compiling borsh-derive v1.6.1
   Compiling bytemuck_derive v1.10.2
   Compiling thiserror-impl v1.0.69
   Compiling solana-sdk-macro v3.0.1
   Compiling anchor-derive-space v1.0.2
   Compiling anchor-attribute-access-control v1.0.2
   Compiling bytemuck v1.25.0
   Compiling solana-program-error v3.0.1
   Compiling solana-instruction-error v2.3.0
   Compiling solana-program-pack v3.1.0
   Compiling solana-hash v4.4.0
   Compiling bincode v1.3.3
   Compiling solana-fee-calculator v3.2.1
   Compiling solana-sha256-hasher v3.1.0
   Compiling solana-address v2.6.1
   Compiling anchor-syn v1.0.2
   Compiling anchor-lang-idl-spec v0.1.0
   Compiling solana-pubkey v4.2.0
   Compiling solana-sdk-ids v3.1.0
   Compiling solana-account-info v3.1.1
   Compiling solana-instruction v3.4.0
   Compiling solana-address v1.1.0
   Compiling solana-pubkey v3.0.0
   Compiling solana-sysvar-id v3.1.0
   Compiling solana-stable-layout v3.0.1
   Compiling solana-program-entrypoint v3.1.1
   Compiling solana-system-interface v2.0.0
   Compiling solana-rent v3.1.0
   Compiling solana-last-restart-slot v3.0.1
   Compiling solana-slot-hashes v3.0.2
   Compiling solana-epoch-schedule v3.1.0
   Compiling solana-epoch-rewards v3.0.2
   Compiling solana-slot-history v3.0.1
   Compiling solana-clock v3.1.0
   Compiling solana-cpi v3.1.0
   Compiling anchor-lang-idl v0.1.3
   Compiling solana-system-interface v3.2.0
   Compiling solana-sysvar v3.1.1
   Compiling solana-serialize-utils v3.1.2
   Compiling solana-invoke v0.5.0
   Compiling solana-instructions-sysvar v3.0.1
   Compiling solana-feature-gate-interface v3.1.0
   Compiling solana-stake-interface v2.0.2
   Compiling solana-loader-v3-interface v6.1.1
   Compiling anchor-attribute-error v1.0.2
   Compiling anchor-derive-serde v1.0.2
   Compiling anchor-attribute-event v1.0.2
   Compiling anchor-derive-accounts v1.0.2
   Compiling anchor-attribute-account v1.0.2
   Compiling anchor-attribute-constant v1.0.2
   Compiling anchor-attribute-program v1.0.2
   Compiling anchor-lang v1.0.2
   Compiling plotarmor v0.1.0 (/home/<usr>/plotarmor-program/.cutover-pass3/old/programs/plotarmor)
    Finished `release` profile [optimized] target(s) in 29m 50s
   Compiling proc-macro2 v1.0.106
   Compiling quote v1.0.45
   Compiling unicode-ident v1.0.24
   Compiling version_check v0.9.5
   Compiling cfg-if v1.0.4
   Compiling libc v0.2.186
   Compiling typenum v1.20.1
   Compiling subtle v2.6.1
   Compiling const-oid v0.9.6
   Compiling serde_core v1.0.228
   Compiling autocfg v1.5.1
   Compiling cpufeatures v0.2.17
   Compiling generic-array v0.14.7
   Compiling equivalent v1.0.2
   Compiling hashbrown v0.17.1
   Compiling serde v1.0.228
   Compiling winnow v1.0.3
   Compiling num-traits v0.2.19
   Compiling toml_datetime v1.1.1+spec-1.1.0
   Compiling cfg_aliases v0.2.1
   Compiling borsh v1.6.1
   Compiling once_cell v1.21.4
   Compiling five8_core v1.0.0
   Compiling indexmap v2.14.0
   Compiling solana-sanitize v3.0.1
   Compiling semver v1.0.28
   Compiling five8 v1.0.0
   Compiling rustc_version v0.4.1
   Compiling solana-atomic-u64 v3.0.1
   Compiling sha2-const-stable v0.1.0
   Compiling syn v2.0.117
   Compiling curve25519-dalek v4.1.3
   Compiling getrandom v0.2.17
   Compiling five8_const v1.0.0
   Compiling zerocopy v0.8.50
   Compiling rand_core v0.6.4
   Compiling toml_parser v1.1.2+spec-1.1.0
   Compiling bs58 v0.5.1
   Compiling num-integer v0.1.46
   Compiling either v1.16.0
   Compiling syn v1.0.109
   Compiling getrandom v0.3.4
   Compiling lazy_static v1.5.0
   Compiling arrayvec v0.7.6
   Compiling toml_edit v0.25.12+spec-1.1.0
   Compiling solana-program-memory v3.1.0
   Compiling ahash v0.8.12
   Compiling feature-probe v0.1.1
   Compiling memchr v2.8.1
   Compiling log v0.4.32
   Compiling bv v0.11.1
   Compiling proc-macro-crate v3.5.0
   Compiling thiserror v2.0.18
   Compiling solana-define-syscall v4.0.1
   Compiling base64 v0.22.1
   Compiling hybrid-array v0.4.12
   Compiling shlex v2.0.1
   Compiling find-msvc-tools v0.1.9
   Compiling serde_bytes v0.11.19
   Compiling num-bigint v0.4.6
   Compiling cc v1.2.63
   Compiling thiserror v1.0.69
   Compiling cmov v0.5.4
   Compiling solana-msg v3.1.0
   Compiling ctutils v0.4.2
   Compiling block-buffer v0.12.0
   Compiling crypto-common v0.2.2
   Compiling paste v1.0.15
   Compiling byteorder v1.5.0
   Compiling blake3 v1.8.5
   Compiling arrayref v0.3.9
   Compiling digest v0.11.3
   Compiling cpufeatures v0.3.0
   Compiling constant_time_eq v0.4.2
   Compiling solana-short-vec v3.2.2
   Compiling num-bigint v0.2.6
   Compiling bitflags v2.13.0
   Compiling num-rational v0.2.4
   Compiling num-complex v0.2.4
   Compiling void v1.0.2
   Compiling unreachable v1.0.0
   Compiling ascii v0.9.3
   Compiling solana-svm-feature-set v3.1.14
   Compiling combine v3.8.1
   Compiling hash32 v0.3.1
   Compiling itertools v0.12.1
   Compiling num-iter v0.1.45
   Compiling anyhow v1.0.102
   Compiling crunchy v0.2.4
   Compiling rustc-demangle v0.1.27
   Compiling num v0.2.1
   Compiling solana-precompile-error v3.0.0
   Compiling opaque-debug v0.3.1
   Compiling solana-fee-structure v3.0.0
   Compiling eager v0.1.0
   Compiling zmij v1.0.21
   Compiling percentage v0.1.0
   Compiling solana-svm-log-collector v3.1.14
   Compiling itertools v0.13.0
   Compiling allocator-api2 v0.2.21
   Compiling solana-svm-measure v3.1.14
   Compiling serde_json v1.0.150
   Compiling keccak v0.1.6
   Compiling hashbrown v0.15.5
   Compiling block-buffer v0.10.4
   Compiling crypto-common v0.1.7
   Compiling digest v0.9.0
   Compiling itertools v0.10.5
   Compiling winnow v0.7.15
   Compiling toml_write v0.1.2
   Compiling getrandom v0.1.16
   Compiling itoa v1.0.18
   Compiling libsecp256k1-core v0.2.2
   Compiling digest v0.10.7
   Compiling ff v0.13.1
   Compiling base16ct v0.2.0
   Compiling unicode-segmentation v1.13.3
   Compiling sha2 v0.10.9
   Compiling zeroize_derive v1.4.3
   Compiling serde_derive v1.0.228
   Compiling bytemuck_derive v1.10.2
   Compiling borsh-derive v1.6.1
   Compiling curve25519-dalek-derive v0.1.1
   Compiling solana-sdk-macro v3.0.1
   Compiling zeroize v1.8.2
   Compiling thiserror-impl v2.0.18
   Compiling thiserror-impl v1.0.69
   Compiling enum-ordinalize-derive v4.3.2
   Compiling bytemuck v1.25.0
   Compiling ppv-lite86 v0.2.21
   Compiling rand_chacha v0.3.1
   Compiling signature v2.2.0
   Compiling rand v0.8.6
   Compiling ed25519 v2.2.3
   Compiling hmac v0.12.1
   Compiling enum-iterator-derive v1.5.0
   Compiling enum-ordinalize v4.3.2
   Compiling ark-serialize-derive v0.5.0
   Compiling der v0.7.10
   Compiling educe v0.6.0
   Compiling ark-serialize-derive v0.4.2
   Compiling solana-program-error v3.0.1
   Compiling ark-std v0.5.0
   Compiling enum-iterator v1.5.0
   Compiling solana-sbpf v0.13.1
   Compiling solana-svm-type-overrides v3.1.14
   Compiling ark-serialize v0.5.0
   Compiling ark-std v0.4.0
   Compiling ark-ff-asm v0.5.0
   Compiling ark-ff-macros v0.5.0
   Compiling ark-serialize v0.4.2
   Compiling ark-ff-asm v0.4.2
   Compiling derivative v2.2.0
   Compiling solana-hash v4.4.0
   Compiling solana-instruction-error v2.3.0
   Compiling bincode v1.3.3
   Compiling solana-sha256-hasher v3.1.0
   Compiling solana-fee-calculator v3.2.1
   Compiling solana-transaction-error v3.2.1
   Compiling serde-big-array v0.5.1
   Compiling solana-hash v3.1.0
   Compiling serde_spanned v0.6.9
   Compiling toml_datetime v0.6.11
   Compiling ark-ff-macros v0.4.2
   Compiling spki v0.7.3
   Compiling sha3 v0.10.9
   Compiling toml_edit v0.22.27
   Compiling hashbrown v0.13.2
   Compiling ark-ff v0.5.0
   Compiling pkcs8 v0.10.2
   Compiling solana-address v2.6.1
   Compiling ed25519-dalek v2.2.0
   Compiling sec1 v0.7.3
   Compiling ark-ff v0.4.2
   Compiling solana-pubkey v4.2.0
   Compiling solana-sdk-ids v3.1.0
   Compiling solana-address v1.1.0
   Compiling solana-account-info v3.1.1
   Compiling solana-instruction v3.4.0
   Compiling solana-pubkey v3.0.0
   Compiling solana-sysvar-id v3.1.0
   Compiling solana-signature v3.4.1
   Compiling solana-program-entrypoint v3.1.1
   Compiling solana-epoch-schedule v3.1.0
   Compiling solana-clock v3.1.0
   Compiling solana-slot-hashes v3.0.2
   Compiling solana-rent v3.1.0
   Compiling solana-last-restart-slot v3.0.1
   Compiling solana-epoch-rewards v3.0.2
   Compiling solana-slot-history v3.0.1
   Compiling solana-signer v3.0.1
   Compiling solana-system-interface v2.0.0
   Compiling solana-serialize-utils v3.1.2
   Compiling solana-sysvar v3.1.1
   Compiling solana-instructions-sysvar v3.0.1
   Compiling solana-cpi v3.1.0
   Compiling solana-message v3.1.0
   Compiling solana-stable-layout v3.0.1
   Compiling solana-system-interface v3.2.0
   Compiling solana-account v3.4.0
   Compiling solana-loader-v3-interface v6.1.1
   Compiling solana-stake-interface v2.0.2
   Compiling solana-transaction-context v3.1.14
   Compiling solana-svm-callback v3.1.14
   Compiling solana-svm-timings v3.1.14
   Compiling solana-transaction v3.1.0
   Compiling toml v0.8.23
   Compiling pbkdf2 v0.11.0
   Compiling solana-svm-transaction v3.1.14
   Compiling crypto-bigint v0.5.5
   Compiling solana-program-runtime v3.1.14
   Compiling heck v0.3.3
   Compiling group v0.13.0
   Compiling strsim v0.11.1
   Compiling ident_case v1.0.1
   Compiling cargo_toml v0.19.2
   Compiling rand_core v0.5.1
   Compiling darling_core v0.23.0
   Compiling solana-seed-phrase v3.0.0
   Compiling rfc6979 v0.4.0
   Compiling inout v0.1.4
   Compiling elliptic-curve v0.13.8
   Compiling libsecp256k1-gen-ecmult v0.2.1
   Compiling libsecp256k1-gen-genmult v0.2.1
   Compiling num-derive v0.4.2
   Compiling anchor-syn v1.0.2
   Compiling libsecp256k1 v0.6.0
   Compiling ecdsa v0.16.9
   Compiling ark-poly v0.4.2
   Compiling cipher v0.4.4
   Compiling rand_chacha v0.2.2
   Compiling agave-feature-set v3.1.14
   Compiling solana-curve25519 v3.1.14
   Compiling block-buffer v0.9.0
   Compiling darling_macro v0.23.0
   Compiling fnv v1.0.7
   Compiling percent-encoding v2.3.2
   Compiling uriparse v0.6.4
   Compiling ark-ec v0.4.2
   Compiling darling v0.23.0
   Compiling rand v0.7.3
   Compiling qstring v0.7.2
   Compiling sha2 v0.9.9
   Compiling k256 v0.13.4
   Compiling solana-bincode v3.1.0
   Compiling universal-hash v0.5.1
   Compiling solana-packet v3.0.0
   Compiling rand_core v0.9.5
   Compiling base64 v0.12.3
   Compiling derivation-path v0.2.0
   Compiling rand_chacha v0.9.0
   Compiling solana-derivation-path v3.0.0
   Compiling ark-poly v0.5.0
   Compiling ark-bn254 v0.4.0
   Compiling polyval v0.6.2
   Compiling solana-secp256k1-recover v3.1.1
   Compiling serde_with_macros v3.21.0
   Compiling light-poseidon v0.2.0
   Compiling aes v0.8.4
   Compiling ctr v0.9.2
   Compiling solana-keccak-hasher v3.1.0
   Compiling solana-blake3-hasher v3.1.0
   Compiling aead v0.5.2
   Compiling solana-big-mod-exp v3.0.0
   Compiling aes-gcm-siv v0.11.1
   Compiling rand v0.9.4
   Compiling solana-seed-derivable v3.0.0
   Compiling ark-ec v0.5.0
   Compiling solana-loader-v4-interface v3.1.0
   Compiling solana-nonce v3.2.0
   Compiling solana-serde-varint v3.0.1
   Compiling merlin v3.0.0
   Compiling qualifier_attr v0.2.2
   Compiling cfg_eval v0.1.2
   Compiling solana-nonce-account v3.0.0
   Compiling solana-keypair v3.1.2
   Compiling aho-corasick v1.1.4
   Compiling regex-syntax v0.8.10
   Compiling serde_with v3.21.0
   Compiling solana-system-program v3.1.14
   Compiling solana-compute-budget-program v3.1.14
   Compiling anchor-lang-idl-spec v0.1.0
   Compiling ark-bn254 v0.5.0
   Compiling solana-vote-interface v4.0.4
   Compiling solana-zk-token-sdk v3.1.14
   Compiling light-poseidon v0.4.0
   Compiling solana-bn254 v3.2.1
   Compiling regex-automata v0.4.14
   Compiling solana-vote-program v3.1.14
   Compiling solana-poseidon v3.1.14
   Compiling anchor-lang-idl v0.1.3
   Compiling solana-zk-sdk v4.0.0
   Compiling solana-define-syscall v3.0.0
   Compiling keccak-const v0.2.0
   Compiling solana-invoke v0.5.0
   Compiling agave-syscalls v3.1.14
   Compiling const-crypto v0.3.0
   Compiling anchor-attribute-constant v1.0.2
   Compiling anchor-attribute-account v1.0.2
   Compiling solana-bpf-loader-program v3.1.14
   Compiling regex v1.12.3
   Compiling anchor-derive-serde v1.0.2
   Compiling anchor-attribute-program v1.0.2
   Compiling anchor-derive-accounts v1.0.2
   Compiling solana-loader-v4-program v3.1.14
   Compiling anchor-attribute-event v1.0.2
   Compiling solana-builtins-default-costs v3.1.14
   Compiling anchor-attribute-error v1.0.2
   Compiling solana-compute-budget v3.1.14
   Compiling solana-compute-budget-interface v3.0.0
   Compiling solana-feature-gate-interface v3.1.0
   Compiling solana-program-pack v3.1.0
   Compiling solana-borsh v3.0.2
   Compiling anchor-attribute-access-control v1.0.2
   Compiling anchor-derive-space v1.0.2
   Compiling solana-program-option v3.1.0
   Compiling base64 v0.21.7
   Compiling solana-compute-budget-instruction v3.1.14
   Compiling agave-reserved-account-keys v3.1.14
   Compiling solana-fee v3.1.14
   Compiling anchor-lang v1.0.2
   Compiling solana-address-lookup-table-interface v3.1.0
   Compiling itertools v0.14.0
   Compiling solana-native-token v3.0.0
   Compiling ansi_term v0.12.1
   Compiling solana-zk-elgamal-proof-program v3.1.14
   Compiling solana-zk-token-proof-program v3.1.14
   Compiling solana-builtins v3.1.14
   Compiling plotarmor v0.1.0 (/home/<usr>/plotarmor-program/.cutover-pass3/old/programs/plotarmor)
   Compiling litesvm v0.10.0
    Finished `test` profile [unoptimized + debuginfo] target(s) in 25m 47s
     Running unittests src/lib.rs (/home/<usr>/plotarmor-program/.cutover-pass3/old/target/debug/deps/plotarmor-5e8b59803e9d03e3)
     Running tests/happy_paths.rs (/home/<usr>/plotarmor-program/.cutover-pass3/old/target/debug/deps/happy_paths-128f2fa5165339af)
     Running tests/security_tests.rs (/home/<usr>/plotarmor-program/.cutover-pass3/old/target/debug/deps/security_tests-18d9b6115db5dbf1)
     Running tests/sign_contract_tests.rs (/home/<usr>/plotarmor-program/.cutover-pass3/old/target/debug/deps/sign_contract_tests-6f0d255ef284f87d)

exit_code=0
````

````bash
NO_DNA=1 solana program show 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 -u devnet --output json; NO_DNA=1 solana program dump 3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2 /tmp/pass3-live.so -u devnet
````
````text
{
  "programId": "3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2",
  "owner": "BPFLoaderUpgradeab1e11111111111111111111111",
  "programdataAddress": "Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL",
  "authority": "EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd",
  "lastDeploySlot": 476301346,
  "dataLen": 471960,
  "lamports": 3286045680
}
Wrote program to /tmp/pass3-live.so

exit_code=0
````

````bash
git diff --stat 09c5bfc HEAD -- programs Cargo.toml Cargo.lock Anchor.toml scripts; git diff 09c5bfc HEAD -- programs/plotarmor/src; git diff --exit-code 09c5bfc HEAD -- programs/plotarmor/src/instructions/register_work_claim.rs programs/plotarmor/src/instructions/add_version.rs programs/plotarmor/src/state.rs programs/plotarmor/src/utils.rs; git diff --exit-code f34bfae HEAD -- programs Cargo.toml Cargo.lock Anchor.toml scripts/build.sh; cat programs/plotarmor/src/instructions/init_registry_config.rs; rg -n "required_payment|spill|MINIMUM_EXTEND_PROGRAM_BYTES" /home/<usr>/.cargo/registry/src/*/solana-bpf-loader-program-3.1.14/src/lib.rs /home/<usr>/.cargo/registry/src/*/solana-loader-v3-interface-6.1.1/src/instruction.rs
````
````text
 Anchor.toml                                        |   2 +
 Cargo.lock                                         |   7 +
 Cargo.toml                                         |   7 +
 programs/plotarmor/Cargo.toml                      |   1 +
 .../plotarmor/src/instructions/sign_contract.rs    |  22 +-
 programs/plotarmor/src/lib.rs                      |  22 ++
 programs/plotarmor/tests/security_tests.rs         | 229 ++++++++++++++++++++
 programs/plotarmor/tests/sign_contract_tests.rs    |  65 ++++++
 scripts/build.sh                                   | 110 ++++++++++
 scripts/check_integrity.py                         |   2 +
 scripts/devnet_sign_contract_adversarial_test.ts   | 234 +++++++++++++++++++++
 scripts/devnet_sign_contract_test.ts               |  19 ++
 scripts/guard_deploy_artifact.sh                   |  30 +++
 scripts/verify_calls.py                            |   2 +
 14 files changed, 751 insertions(+), 1 deletion(-)
diff --git a/programs/plotarmor/src/instructions/sign_contract.rs b/programs/plotarmor/src/instructions/sign_contract.rs
index 8dace66..9e27aa6 100644
--- a/programs/plotarmor/src/instructions/sign_contract.rs
+++ b/programs/plotarmor/src/instructions/sign_contract.rs
@@ -1,11 +1,22 @@
 use anchor_lang::prelude::*;

 use crate::error::PlotArmorError;
-use crate::state::{ContractArtifact, ContractSignature};
+use crate::state::{ContractArtifact, ContractSignature, RegistryConfig};

 #[derive(Accounts)]
 #[instruction(content_hash: [u8; 32])]
 pub struct SignContract<'info> {
+    // Added 2026-09-04 (audit M2). sign_contract was previously the ONLY instruction
+    // taking no RegistryConfig, so it could not honour the paused flag and sat outside
+    // the kill-switch surface the other five respect. Same shape as the other five:
+    // Account (not mut), const seed, paused checked in the handler. This does NOT add a
+    // pause setter; the kill switch itself stays deferred (Known v1 limitations, item C).
+    #[account(
+        seeds = [b"config"],
+        bump,
+    )]
+    pub registry_config: Account<'info, RegistryConfig>,
+
     // The contract being signed. Must already exist on-chain; ContractArtifact
     // is never init'd here (sign_contract does not stand alone -- see spec §Design decisions #3).
     // Seeds re-derived from the account's OWN stored raw_hash (not the client's
@@ -61,6 +72,15 @@ pub fn handler(
     ctx: Context<SignContract>,
     content_hash: [u8; 32],
 ) -> Result<()> {
+    // 1. Reject if paused. The account CONSTRAINT matches the other five instructions
+    // that read RegistryConfig; handler ORDERING does not, and is not meant to. The
+    // four anchoring instructions run assert_mode_allowed first and check paused
+    // second; add_owner and sign_contract take no anchor_mode_arg, so paused is
+    // simply their first check. Only the paused-vs-mode order differs, and it is
+    // unobservable here because there is no mode check to order against.
+    require!(!ctx.accounts.registry_config.paused, PlotArmorError::Paused);
+
+    // 2. The client's asserted content hash must match the on-chain artifact.
     require!(
         content_hash == ctx.accounts.contract_artifact.raw_hash,
         PlotArmorError::ContentHashMismatch
diff --git a/programs/plotarmor/src/lib.rs b/programs/plotarmor/src/lib.rs
index 7a4265a..a93f883 100644
--- a/programs/plotarmor/src/lib.rs
+++ b/programs/plotarmor/src/lib.rs
@@ -31,6 +31,28 @@ use instructions::sign_contract::__client_accounts_sign_contract;
 pub use instructions::SignContract;
 pub use state::*;

+// on-chain security.txt (solana-security-txt 1.1.3). Embedded in .rodata only;
+// adds no code. Gated off for the no-entrypoint build so dependent crates that
+// pull this program in as a library do not inherit a second copy of the blob.
+//
+// contacts and policy were supplied by Milan on 2026-09-29, replacing the
+// .invalid placeholders that previously blocked deployment. The policy text is
+// mirrored in SECURITY.md at the repo root; keep the two in sync. source_code
+// stays "private" while the source repository is private. Per the approved
+// scope, source_revision, source_release and auditors are omitted rather than
+// filled with provisional values.
+#[cfg(not(feature = "no-entrypoint"))]
+use solana_security_txt::security_txt;
+
+#[cfg(not(feature = "no-entrypoint"))]
+security_txt! {
+    name: "PlotArmor",
+    project_url: "https://plotarmor.io",
+    contacts: "email:info@plotarmor.io",
+    policy: "Please report security issues privately to info@plotarmor.io. We acknowledge reports within 5 business days. Do not test against accounts or data you do not own. This program runs on Solana devnet as a demo MVP.",
+    source_code: "private"
+}
+
 declare_id!("3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2");

 #[program]
use anchor_lang::prelude::*;

use crate::error::PlotArmorError;
use crate::program::Plotarmor;
use crate::state::RegistryConfig;

#[derive(Accounts)]
pub struct InitRegistryConfig<'info> {
    #[account(
        init,
        payer = signer,
        space = RegistryConfig::LEN,
        seeds = [b"config"],
        bump,
    )]
    pub registry_config: Account<'info, RegistryConfig>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
    #[account(
        constraint = program.programdata_address()? == Some(program_data.key()) @ PlotArmorError::Unauthorized,
    )]
    pub program: Program<'info, Plotarmor>,
    #[account(
        constraint = program_data.upgrade_authority_address == Some(signer.key()) @ PlotArmorError::Unauthorized,
    )]
    pub program_data: Account<'info, ProgramData>,
}

pub fn handler(ctx: Context<InitRegistryConfig>) -> Result<()> {
    let config = &mut ctx.accounts.registry_config;
    config.authority = ctx.accounts.signer.key();
    config.schema_version = 1;
    config.enabled_anchor_modes = 0;
    config.paused = false;
    Ok(())
}
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:18:pub const MINIMUM_EXTEND_PROGRAM_BYTES: u32 = 10_240;
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:110:    /// will be transferred to the spill account, leaving the Buffer account
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:119:    ///   3. `[writable]` The spill account.
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:154:    /// must be at least [`MINIMUM_EXTEND_PROGRAM_BYTES`] (10 KiB).
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:156:    /// within [`MINIMUM_EXTEND_PROGRAM_BYTES`] of the max permitted
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:308:    spill_address: &Pubkey,
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:318:            AccountMeta::new(*spill_address, false),
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-loader-v3-interface-6.1.1/src/instruction.rs:469:/// [`MINIMUM_EXTEND_PROGRAM_BYTES`] unless the account is near the
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:820:            // Fund ProgramData to rent-exemption, spill the rest
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:822:            let mut spill = instruction_context.try_borrow_instruction_account(3)?;
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:823:            spill.checked_add_lamports(
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:1362:    let required_payment = {
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:1374:    if required_payment > 0 {
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:1379:            system_instruction::transfer(&payer_key, &programdata_key, required_payment),
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:2331:            let spill_address = Pubkey::new_unique();
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:2377:            let spill_account = AccountSharedData::new(0, 0, &Pubkey::new_unique());
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:2388:                (spill_address, spill_account),
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:2410:                    pubkey: spill_address,
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:2549:        // Case: Buffer account and spill account alias
/home/<usr>/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana-bpf-loader-program-3.1.14/src/lib.rs:2564:        // Case: Programdata account and spill account alias

exit_code=0
````

````bash
cat /tmp/pass3-chain.cjs; node /tmp/pass3-chain.cjs
````
````text
const {PublicKey}=require('/home/<usr>/plotarmor-program/node_modules/@solana/web3.js');
const {createHash}=require('crypto');
const fs=require('fs');
const rpcUrl='https://api.devnet.solana.com';
async function rpc(method,params){const r=await fetch(rpcUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:1,method,params})});const j=await r.json();if(j.error)throw Error(JSON.stringify(j.error));return j.result;}
(async()=>{
 console.log('UTC',new Date().toISOString(),'RPC',rpcUrl,'commitment finalized');
 const program=new PublicKey('3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2');
 const [config,bump]=PublicKey.findProgramAddressSync([Buffer.from('config')],program);
 const [pd]=PublicKey.findProgramAddressSync([program.toBuffer()],new PublicKey('BPFLoaderUpgradeab1e11111111111111111111111'));
 const authority='EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd';
 const keys=[program.toBase58(),pd.toBase58(),config.toBase58(),authority,'SysvarRent111111111111111111111111111111111'];
 const result=await rpc('getMultipleAccounts',[keys,{encoding:'base64',commitment:'finalized'}]);
 console.log('snapshot slot',result.context.slot);
 const accounts=result.value.map((a,i)=>{if(!a)throw Error('missing '+keys[i]);const b=Buffer.from(a.data[0],'base64');console.log(JSON.stringify({address:keys[i],owner:a.owner,executable:a.executable,lamports:a.lamports,dataBytes:b.length}));return {a,b};});
 const {a:pa,b:pb}=accounts[1];
 if(pa.owner!=='BPFLoaderUpgradeab1e11111111111111111111111'||pb.readUInt32LE(0)!==3)throw Error('invalid ProgramData');
 console.log('ProgramData',JSON.stringify({slot:pb.readBigUInt64LE(4).toString(),authorityOption:pb[12],authority:new PublicKey(pb.subarray(13,45)).toBase58(),programCapacity:pb.length-45}));
 console.log('ProgramData payload equals CLI dump',pb.subarray(45).equals(fs.readFileSync('/tmp/pass3-live.so')));
 const {a:ca,b:cb}=accounts[2];const disc=createHash('sha256').update('account:RegistryConfig').digest().subarray(0,8);
 if(ca.owner!==program.toBase58()||cb.length!==44||!cb.subarray(0,8).equals(disc)||cb[43]>1)throw Error('invalid RegistryConfig');
 console.log('RegistryConfig',JSON.stringify({pda:config.toBase58(),bump,discriminator:[...disc],authority:new PublicKey(cb.subarray(8,40)).toBase58(),schema_version:cb[40],enabled_anchor_modes:cb.readUInt16LE(41),paused:!!cb[43],initialized:cb[40]===1}));
 const rb=accounts[4].b;console.log('Rent sysvar',JSON.stringify({lamports_per_byte_year:rb.readBigUInt64LE(0).toString(),exemption_threshold:rb.readDoubleLE(8),burn_percent:rb[16]}));
 const sizes=[0,1,472005,472485,482245,472477];const rents={};for(const n of sizes)rents[n]=await rpc('getMinimumBalanceForRentExemption',[n,{commitment:'finalized'}]);
 console.log('getMinimumBalanceForRentExemption',JSON.stringify(rents));
 const rate=rents[1]-rents[0];console.log('rent exemption lamports per added byte',rate,'overhead bytes',rents[0]/rate);
 const balance=accounts[3].a.lamports,extend=10240,newSize=472440,after=pb.length+extend,topup=Math.max(rents[after]-pa.lamports,0),buffer=rents[newSize+37],spill=pa.lamports+topup+buffer-rents[after],net=spill-buffer-topup;
 console.log('cost calculation',JSON.stringify({authorityBalanceLamports:balance,programDataBytes:pb.length,newSoBytes:newSize,minimumGrowth:newSize-(pb.length-45),runbookExtend:extend,afterProgramDataBytes:after,afterProgramCapacity:after-45,extendRentTopup:topup,bufferRent:buffer,upgradeSpill:spill,netAuthorityBeforeFees:net,authorityAfterBeforeFees:balance+net,authorityAfterWithRunbookEstimated2500000Fees:balance+net-2500000,authorityAfterWith2350000DeployFeesPlus5000Extend:balance+net-2355000}));
 const expected={472005:2398435640,472485:2400874040,482245:2450454840,472477:2400833400};for(const [n,v]of Object.entries(expected))console.log('runbook rent delta',n,rents[n]-v);
 console.log('runbook authority balance delta lamports',balance-5400565851);
 console.log('runbook ProgramData lamports delta',pa.lamports-3286045680);
 fs.writeFileSync('/tmp/pass3-chain-snapshot.json',JSON.stringify({result,rents,rate,balance,net},null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
UTC 2026-10-07T09:18:46.254Z RPC https://api.devnet.solana.com commitment finalized
snapshot slot 508406915
{"address":"3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2","owner":"BPFLoaderUpgradeab1e11111111111111111111111","executable":true,"lamports":1141440,"dataBytes":36}
{"address":"Dr8S95D7bHGBrd6gFSAommQjBNH1qcBMJpofe9ooLRpL","owner":"BPFLoaderUpgradeab1e11111111111111111111111","executable":false,"lamports":3286045680,"dataBytes":472005}
{"address":"BpsMTsw9uxmmgmy1iVjgwaLfoyKMGuoisyBQ8sTrxvmG","owner":"3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2","executable":false,"lamports":1197120,"dataBytes":44}
{"address":"EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd","owner":"11111111111111111111111111111111","executable":false,"lamports":5400565851,"dataBytes":0}
{"address":"SysvarRent111111111111111111111111111111111","owner":"Sysvar1111111111111111111111111111111111111","executable":false,"lamports":1009200,"dataBytes":17}
ProgramData {"slot":"476301346","authorityOption":1,"authority":"EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd","programCapacity":471960}
ProgramData payload equals CLI dump true
RegistryConfig {"pda":"BpsMTsw9uxmmgmy1iVjgwaLfoyKMGuoisyBQ8sTrxvmG","bump":254,"discriminator":[23,118,10,246,173,231,243,156],"authority":"EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd","schema_version":1,"enabled_anchor_modes":0,"paused":false,"initialized":true}
Rent sysvar {"lamports_per_byte_year":"5080","exemption_threshold":1,"burn_percent":50}
getMinimumBalanceForRentExemption {"0":650240,"1":655320,"472005":2398435640,"472477":2400833400,"472485":2400874040,"482245":2450454840}
rent exemption lamports per added byte 5080 overhead bytes 128
cost calculation {"authorityBalanceLamports":5400565851,"programDataBytes":472005,"newSoBytes":472440,"minimumGrowth":480,"runbookExtend":10240,"afterProgramDataBytes":482245,"afterProgramCapacity":482200,"extendRentTopup":0,"bufferRent":2400833400,"upgradeSpill":3236424240,"netAuthorityBeforeFees":835590840,"authorityAfterBeforeFees":6236156691,"authorityAfterWithRunbookEstimated2500000Fees":6233656691,"authorityAfterWith2350000DeployFeesPlus5000Extend":6233801691}
runbook rent delta 472005 0
runbook rent delta 472477 0
runbook rent delta 472485 0
runbook rent delta 482245 0
runbook authority balance delta lamports 0
runbook ProgramData lamports delta 0

exit_code=0
````

````bash
sed -n "808,836p;1356,1386p" /home/<usr>/.cargo/registry/src/*/solana-bpf-loader-program-3.1.14/src/lib.rs; sed -n "10,23p;140,166p" /home/<usr>/.cargo/registry/src/*/solana-loader-v3-interface-6.1.1/src/instruction.rs; rg -n "tools_version|platform-tools" /home/<usr>/.cargo/registry/src/*/anchor-cli-1.0.1/src/lib.rs | head -30; git diff --quiet f34bfae HEAD -- programs Cargo.toml Cargo.lock Anchor.toml scripts rust-toolchain.toml; printf "runbook_source_precheck_exit=%s\n" "$?"; git diff --name-only f34bfae HEAD -- programs Cargo.toml Cargo.lock Anchor.toml scripts rust-toolchain.toml
````
````text
                let src_slice = buffer
                    .get_data()
                    .get(buffer_data_offset..)
                    .ok_or(InstructionError::AccountDataTooSmall)?;
                dst_slice.copy_from_slice(src_slice);
            }
            programdata
                .get_data_mut()?
                .get_mut(programdata_data_offset.saturating_add(buffer_data_len)..)
                .ok_or(InstructionError::AccountDataTooSmall)?
                .fill(0);

            // Fund ProgramData to rent-exemption, spill the rest
            let mut buffer = instruction_context.try_borrow_instruction_account(2)?;
            let mut spill = instruction_context.try_borrow_instruction_account(3)?;
            spill.checked_add_lamports(
                programdata
                    .get_lamports()
                    .saturating_add(buffer_lamports)
                    .saturating_sub(programdata_balance_required),
            )?;
            buffer.set_lamports(0)?;
            programdata.set_lamports(programdata_balance_required)?;
            buffer.set_data_length(UpgradeableLoaderState::size_of_buffer(0))?;

            ic_logger_msg!(log_collector, "Upgraded program {:?}", new_program_id);
        }
        UpgradeableLoaderInstruction::SetAuthority => {
            instruction_context.check_number_of_instruction_accounts(2)?;
        upgrade_authority_address
    } else {
        ic_logger_msg!(log_collector, "ProgramData state is invalid");
        return Err(InstructionError::InvalidAccountData);
    };

    let required_payment = {
        let balance = programdata_account.get_lamports();
        let rent = invoke_context.get_sysvar_cache().get_rent()?;
        let min_balance = rent.minimum_balance(new_len).max(1);
        min_balance.saturating_sub(balance)
    };

    // Borrowed accounts need to be dropped before native_invoke
    drop(programdata_account);

    // Dereference the program ID to prevent overlapping mutable/immutable borrow of invoke context
    let program_id = *program_id;
    if required_payment > 0 {
        let payer_key =
            *instruction_context.get_key_of_instruction_account(optional_payer_account_index)?;

        invoke_context.native_invoke(
            system_instruction::transfer(&payer_key, &programdata_key, required_payment),
            &[],
        )?;
    }

    let transaction_context = &invoke_context.transaction_context;
    let instruction_context = transaction_context.get_current_instruction_context()?;
    let mut programdata_account =
};

/// Minimum number of bytes for an `ExtendProgram` instruction.
///
/// After the SIMD-0431 feature gate is activated, `ExtendProgram` will
/// reject requests smaller than this value, unless the program data
/// account is within this many bytes of the max permitted data length of
/// an account: 10 MiB.
pub const MINIMUM_EXTEND_PROGRAM_BYTES: u32 = 10_240;

#[repr(u8)]
#[cfg_attr(
    feature = "serde",
    derive(serde_derive::Deserialize, serde_derive::Serialize)
    /// # Account references
    ///   0. `[writable]` The account to close, if closing a program must be the
    ///      ProgramData account.
    ///   1. `[writable]` The account to deposit the closed account's lamports.
    ///   2. `[signer]` The account's authority, Optional, required for
    ///      initialized accounts.
    ///   3. `[writable]` The associated Program account if the account to close
    ///      is a ProgramData account.
    Close,

    /// Extend a program's ProgramData account by the specified number of bytes.
    /// Only upgradeable programs can be extended.
    ///
    /// After the SIMD-0431 feature gate is activated, `additional_bytes`
    /// must be at least [`MINIMUM_EXTEND_PROGRAM_BYTES`] (10 KiB).
    /// The minimum does not apply when the program data account is
    /// within [`MINIMUM_EXTEND_PROGRAM_BYTES`] of the max permitted
    /// data length of an account: 10 MiB.
    ///
    /// The payer account must contain sufficient lamports to fund the
    /// ProgramData account to be rent-exempt. If the ProgramData account
    /// balance is already sufficient to cover the rent exemption cost
    /// for the extended bytes, the payer account is not required.
    ///
    /// # Account references
    ///   0. `[writable]` The ProgramData account.
    ///   1. `[writable]` The ProgramData account's associated Program account.
rg: /home/<usr>/.cargo/registry/src/*/anchor-cli-1.0.1/src/lib.rs: IO error for operation on /home/<usr>/.cargo/registry/src/*/anchor-cli-1.0.1/src/lib.rs: No such file or directory (os error 2)
runbook_source_precheck_exit=1
scripts/guard_deploy_artifact.sh

exit_code=0
````

````bash
cd .cutover-pass3/head && NO_DNA=1 scripts/build.sh --anchor --ignore-keys
````
````text
platform-tools pin: v1.52  (mode: anchor)
   Compiling proc-macro2 v1.0.106
   Compiling quote v1.0.45
   Compiling unicode-ident v1.0.24
   Compiling hashbrown v0.17.1
   Compiling equivalent v1.0.2
   Compiling serde_core v1.0.228
   Compiling winnow v1.0.3
   Compiling toml_datetime v1.1.1+spec-1.1.0
   Compiling serde v1.0.228
   Compiling cfg_aliases v0.2.1
   Compiling borsh v1.6.1
   Compiling once_cell v1.21.4
   Compiling five8_core v1.0.0
   Compiling solana-define-syscall v4.0.1
   Compiling five8 v1.0.0
   Compiling sha2-const-stable v0.1.0
   Compiling solana-define-syscall v5.1.0
   Compiling five8_const v1.0.0
   Compiling solana-sanitize v3.0.1
   Compiling solana-atomic-u64 v3.0.1
   Compiling bs58 v0.5.1
   Compiling version_check v0.9.5
   Compiling typenum v1.20.1
   Compiling indexmap v2.14.0
   Compiling autocfg v1.5.1
   Compiling generic-array v0.14.7
   Compiling syn v1.0.109
   Compiling toml_parser v1.1.2+spec-1.1.0
   Compiling syn v2.0.117
   Compiling num-traits v0.2.19
   Compiling toml_edit v0.25.12+spec-1.1.0
   Compiling thiserror v1.0.69
   Compiling anyhow v1.0.102
   Compiling crypto-common v0.1.7
   Compiling block-buffer v0.10.4
   Compiling digest v0.10.7
   Compiling proc-macro-crate v3.5.0
   Compiling cfg-if v1.0.4
   Compiling cpufeatures v0.2.17
   Compiling unicode-segmentation v1.13.3
   Compiling heck v0.3.3
   Compiling sha2 v0.10.9
   Compiling solana-program-memory v3.1.0
   Compiling feature-probe v0.1.1
   Compiling zmij v1.0.21
   Compiling bv v0.11.1
   Compiling solana-msg v3.1.0
   Compiling serde_json v1.0.150
   Compiling memchr v2.8.1
   Compiling log v0.4.32
   Compiling itoa v1.0.18
   Compiling lazy_static v1.5.0
   Compiling serde_bytes v0.11.19
   Compiling keccak-const v0.2.0
   Compiling solana-define-syscall v3.0.0
   Compiling solana-program-option v3.1.0
   Compiling base64 v0.21.7
   Compiling const-crypto v0.3.0
   Compiling solana-security-txt v1.1.3
   Compiling serde_derive v1.0.228
   Compiling borsh-derive v1.6.1
   Compiling bytemuck_derive v1.10.2
   Compiling thiserror-impl v1.0.69
   Compiling solana-sdk-macro v3.0.1
   Compiling bytemuck v1.25.0
   Compiling anchor-derive-space v1.0.2
   Compiling anchor-attribute-access-control v1.0.2
   Compiling solana-program-error v3.0.1
   Compiling solana-instruction-error v2.3.0
   Compiling solana-program-pack v3.1.0
   Compiling solana-hash v4.4.0
   Compiling bincode v1.3.3
   Compiling solana-fee-calculator v3.2.1
   Compiling anchor-syn v1.0.2
   Compiling anchor-lang-idl-spec v0.1.0
   Compiling solana-sha256-hasher v3.1.0
   Compiling solana-address v2.6.1
   Compiling solana-sdk-ids v3.1.0
   Compiling solana-pubkey v4.2.0
   Compiling solana-account-info v3.1.1
   Compiling solana-sysvar-id v3.1.0
   Compiling solana-instruction v3.4.0
   Compiling solana-address v1.1.0
   Compiling solana-slot-hashes v3.0.2
   Compiling solana-last-restart-slot v3.0.1
   Compiling solana-program-entrypoint v3.1.1
   Compiling solana-pubkey v3.0.0
   Compiling solana-epoch-schedule v3.1.0
   Compiling solana-stable-layout v3.0.1
   Compiling solana-rent v3.1.0
   Compiling solana-clock v3.1.0
   Compiling solana-epoch-rewards v3.0.2
   Compiling solana-cpi v3.1.0
   Compiling solana-system-interface v2.0.0
   Compiling solana-system-interface v3.2.0
   Compiling solana-slot-history v3.0.1
   Compiling solana-serialize-utils v3.1.2
   Compiling solana-invoke v0.5.0
   Compiling solana-feature-gate-interface v3.1.0
   Compiling solana-instructions-sysvar v3.0.1
   Compiling anchor-lang-idl v0.1.3
   Compiling solana-sysvar v3.1.1
   Compiling solana-loader-v3-interface v6.1.1
   Compiling solana-stake-interface v2.0.2
   Compiling anchor-attribute-account v1.0.2
   Compiling anchor-attribute-constant v1.0.2
   Compiling anchor-attribute-event v1.0.2
   Compiling anchor-derive-serde v1.0.2
   Compiling anchor-derive-accounts v1.0.2
   Compiling anchor-attribute-error v1.0.2
   Compiling anchor-attribute-program v1.0.2
   Compiling anchor-lang v1.0.2
   Compiling plotarmor v0.1.0 (/home/<usr>/plotarmor-program/.cutover-pass3/head/programs/plotarmor)
    Finished `release` profile [optimized] target(s) in 43m 04s
   Compiling proc-macro2 v1.0.106
   Compiling quote v1.0.45
   Compiling unicode-ident v1.0.24
   Compiling version_check v0.9.5
   Compiling cfg-if v1.0.4
   Compiling libc v0.2.186
   Compiling typenum v1.20.1
   Compiling subtle v2.6.1
   Compiling const-oid v0.9.6
   Compiling serde_core v1.0.228
   Compiling autocfg v1.5.1
   Compiling cpufeatures v0.2.17
   Compiling hashbrown v0.17.1
   Compiling generic-array v0.14.7
   Compiling serde v1.0.228
   Compiling equivalent v1.0.2
   Compiling winnow v1.0.3
   Compiling num-traits v0.2.19
   Compiling toml_datetime v1.1.1+spec-1.1.0
   Compiling indexmap v2.14.0
   Compiling cfg_aliases v0.2.1
   Compiling borsh v1.6.1
   Compiling once_cell v1.21.4
   Compiling getrandom v0.2.17
   Compiling five8_core v1.0.0
   Compiling syn v2.0.117
   Compiling solana-sanitize v3.0.1
   Compiling semver v1.0.28
   Compiling five8 v1.0.0
   Compiling solana-atomic-u64 v3.0.1
   Compiling rand_core v0.6.4
   Compiling sha2-const-stable v0.1.0
   Compiling toml_parser v1.1.2+spec-1.1.0
   Compiling rustc_version v0.4.1
   Compiling five8_const v1.0.0
   Compiling zerocopy v0.8.50
   Compiling bs58 v0.5.1
   Compiling num-integer v0.1.46
   Compiling either v1.16.0
   Compiling syn v1.0.109
   Compiling curve25519-dalek v4.1.3
   Compiling toml_edit v0.25.12+spec-1.1.0
   Compiling lazy_static v1.5.0
   Compiling getrandom v0.3.4
   Compiling arrayvec v0.7.6
   Compiling solana-program-memory v3.1.0
   Compiling ahash v0.8.12
   Compiling feature-probe v0.1.1
   Compiling memchr v2.8.1
   Compiling proc-macro-crate v3.5.0
   Compiling log v0.4.32
   Compiling bv v0.11.1
   Compiling thiserror v2.0.18
   Compiling base64 v0.22.1
   Compiling solana-define-syscall v4.0.1
   Compiling hybrid-array v0.4.12
   Compiling shlex v2.0.1
   Compiling find-msvc-tools v0.1.9
   Compiling serde_bytes v0.11.19
   Compiling num-bigint v0.4.6
   Compiling cc v1.2.63
   Compiling solana-msg v3.1.0
   Compiling thiserror v1.0.69
   Compiling cmov v0.5.4
   Compiling ctutils v0.4.2
   Compiling crypto-common v0.2.2
   Compiling block-buffer v0.12.0
   Compiling paste v1.0.15
   Compiling arrayref v0.3.9
   Compiling byteorder v1.5.0
   Compiling blake3 v1.8.5
   Compiling digest v0.11.3
   Compiling cpufeatures v0.3.0
   Compiling constant_time_eq v0.4.2
   Compiling solana-short-vec v3.2.2
   Compiling num-bigint v0.2.6
   Compiling bitflags v2.13.0
   Compiling zeroize_derive v1.4.3
   Compiling serde_derive v1.0.228
   Compiling bytemuck_derive v1.10.2
   Compiling borsh-derive v1.6.1
   Compiling zeroize v1.8.2
   Compiling curve25519-dalek-derive v0.1.1
   Compiling solana-sdk-macro v3.0.1
   Compiling bytemuck v1.25.0
   Compiling crypto-common v0.1.7
   Compiling block-buffer v0.10.4
   Compiling digest v0.10.7
   Compiling ppv-lite86 v0.2.21
   Compiling thiserror-impl v2.0.18
   Compiling thiserror-impl v1.0.69
   Compiling sha2 v0.10.9
   Compiling signature v2.2.0
   Compiling ed25519 v2.2.3
   Compiling rand_chacha v0.3.1
   Compiling rand v0.8.6
   Compiling hmac v0.12.1
   Compiling num-complex v0.2.4
   Compiling num-rational v0.2.4
   Compiling void v1.0.2
   Compiling solana-hash v4.4.0
   Compiling solana-program-error v3.0.1
   Compiling bincode v1.3.3
   Compiling solana-sha256-hasher v3.1.0
   Compiling solana-instruction-error v2.3.0
   Compiling solana-fee-calculator v3.2.1
   Compiling solana-transaction-error v3.2.1
   Compiling serde-big-array v0.5.1
   Compiling solana-hash v3.1.0
   Compiling unreachable v1.0.0
   Compiling solana-svm-feature-set v3.1.14
   Compiling ascii v0.9.3
   Compiling enum-iterator-derive v1.5.0
   Compiling enum-ordinalize-derive v4.3.2
   Compiling combine v3.8.1
   Compiling hash32 v0.3.1
   Compiling num-iter v0.1.45
   Compiling itertools v0.12.1
   Compiling solana-address v2.6.1
   Compiling ed25519-dalek v2.2.0
   Compiling crunchy v0.2.4
   Compiling solana-pubkey v4.2.0
   Compiling solana-sdk-ids v3.1.0
   Compiling solana-instruction v3.4.0
   Compiling solana-address v1.1.0
   Compiling solana-pubkey v3.0.0
   Compiling solana-account-info v3.1.1
   Compiling solana-sysvar-id v3.1.0
   Compiling solana-signature v3.4.1
   Compiling solana-system-interface v2.0.0
   Compiling solana-serialize-utils v3.1.2
   Compiling solana-epoch-schedule v3.1.0
   Compiling solana-clock v3.1.0
   Compiling solana-program-entrypoint v3.1.1
   Compiling solana-rent v3.1.0
   Compiling solana-slot-hashes v3.0.2
   Compiling solana-slot-history v3.0.1
   Compiling solana-epoch-rewards v3.0.2
   Compiling solana-last-restart-slot v3.0.1
   Compiling solana-signer v3.0.1
   Compiling solana-instructions-sysvar v3.0.1
   Compiling solana-cpi v3.1.0
   Compiling solana-sysvar v3.1.1
   Compiling solana-message v3.1.0
   Compiling solana-system-interface v3.2.0
   Compiling solana-stable-layout v3.0.1
   Compiling solana-loader-v3-interface v6.1.1
   Compiling anyhow v1.0.102
   Compiling rustc-demangle v0.1.27
   Compiling enum-iterator v1.5.0
   Compiling solana-account v3.4.0
   Compiling solana-stake-interface v2.0.2
   Compiling num v0.2.1
   Compiling solana-transaction v3.1.0
   Compiling enum-ordinalize v4.3.2
   Compiling ark-std v0.5.0
   Compiling ark-serialize-derive v0.5.0
   Compiling solana-precompile-error v3.0.0
   Compiling opaque-debug v0.3.1
   Compiling eager v0.1.0
   Compiling solana-svm-transaction v3.1.14
   Compiling solana-fee-structure v3.0.0
   Compiling zmij v1.0.21
   Compiling solana-svm-callback v3.1.14
   Compiling educe v0.6.0
   Compiling percentage v0.1.0
   Compiling solana-svm-timings v3.1.14
   Compiling ark-serialize v0.5.0
   Compiling ark-std v0.4.0
   Compiling solana-svm-type-overrides v3.1.14
   Compiling ark-serialize-derive v0.4.2
   Compiling der v0.7.10
   Compiling ark-ff-asm v0.5.0
   Compiling ark-ff-macros v0.5.0
   Compiling solana-svm-log-collector v3.1.14
   Compiling itertools v0.13.0
   Compiling keccak v0.1.6
   Compiling solana-sbpf v0.13.1
   Compiling allocator-api2 v0.2.21
   Compiling serde_json v1.0.150
   Compiling solana-svm-measure v3.1.14
   Compiling ark-serialize v0.4.2
   Compiling hashbrown v0.15.5
   Compiling serde_spanned v0.6.9
   Compiling toml_datetime v0.6.11
   Compiling derivative v2.2.0
   Compiling ark-ff-asm v0.4.2
   Compiling ark-ff-macros v0.4.2
   Compiling digest v0.9.0
   Compiling itertools v0.10.5
   Compiling winnow v0.7.15
   Compiling toml_write v0.1.2
   Compiling getrandom v0.1.16
   Compiling itoa v1.0.18
   Compiling ark-ff v0.5.0
   Compiling libsecp256k1-core v0.2.2
   Compiling spki v0.7.3
   Compiling sha3 v0.10.9
   Compiling hashbrown v0.13.2
   Compiling ff v0.13.1
   Compiling unicode-segmentation v1.13.3
   Compiling base16ct v0.2.0
   Compiling ark-ff v0.4.2
   Compiling sec1 v0.7.3
   Compiling group v0.13.0
   Compiling pkcs8 v0.10.2
   Compiling heck v0.3.3
   Compiling pbkdf2 v0.11.0
   Compiling crypto-bigint v0.5.5
   Compiling ident_case v1.0.1
   Compiling solana-transaction-context v3.1.14
   Compiling strsim v0.11.1
   Compiling toml_edit v0.22.27
   Compiling darling_core v0.23.0
   Compiling rand_core v0.5.1
   Compiling solana-program-runtime v3.1.14
   Compiling solana-seed-phrase v3.0.0
   Compiling elliptic-curve v0.13.8
   Compiling libsecp256k1-gen-genmult v0.2.1
   Compiling libsecp256k1-gen-ecmult v0.2.1
   Compiling rfc6979 v0.4.0
   Compiling inout v0.1.4
   Compiling num-derive v0.4.2
   Compiling cipher v0.4.4
   Compiling ecdsa v0.16.9
   Compiling toml v0.8.23
   Compiling libsecp256k1 v0.6.0
   Compiling cargo_toml v0.19.2
   Compiling darling_macro v0.23.0
   Compiling rand_chacha v0.2.2
   Compiling agave-feature-set v3.1.14
   Compiling solana-curve25519 v3.1.14
   Compiling block-buffer v0.9.0
   Compiling percent-encoding v2.3.2
   Compiling fnv v1.0.7
   Compiling qstring v0.7.2
   Compiling uriparse v0.6.4
   Compiling sha2 v0.9.9
   Compiling darling v0.23.0
   Compiling rand v0.7.3
   Compiling anchor-syn v1.0.2
   Compiling ark-poly v0.5.0
   Compiling k256 v0.13.4
   Compiling solana-bincode v3.1.0
   Compiling universal-hash v0.5.1
   Compiling solana-packet v3.0.0
   Compiling ark-poly v0.4.2
   Compiling rand_core v0.9.5
   Compiling derivation-path v0.2.0
   Compiling base64 v0.12.3
   Compiling ark-ec v0.5.0
   Compiling solana-derivation-path v3.0.0
   Compiling rand_chacha v0.9.0
   Compiling solana-secp256k1-recover v3.1.1
   Compiling polyval v0.6.2
   Compiling serde_with_macros v3.21.0
   Compiling ctr v0.9.2
   Compiling aes v0.8.4
   Compiling ark-ec v0.4.2
   Compiling solana-keccak-hasher v3.1.0
   Compiling solana-blake3-hasher v3.1.0
   Compiling aead v0.5.2
   Compiling solana-big-mod-exp v3.0.0
   Compiling rand v0.9.4
   Compiling solana-seed-derivable v3.0.0
   Compiling aes-gcm-siv v0.11.1
   Compiling merlin v3.0.0
   Compiling solana-loader-v4-interface v3.1.0
   Compiling solana-nonce v3.2.0
   Compiling solana-serde-varint v3.0.1
   Compiling ark-bn254 v0.5.0
   Compiling cfg_eval v0.1.2
   Compiling qualifier_attr v0.2.2
   Compiling solana-keypair v3.1.2
   Compiling serde_with v3.21.0
   Compiling ark-bn254 v0.4.0
   Compiling light-poseidon v0.4.0
   Compiling solana-bn254 v3.2.1
   Compiling solana-nonce-account v3.0.0
   Compiling light-poseidon v0.2.0
   Compiling solana-vote-interface v4.0.4
   Compiling aho-corasick v1.1.4
   Compiling regex-syntax v0.8.10
   Compiling solana-system-program v3.1.14
   Compiling solana-poseidon v3.1.14
   Compiling solana-compute-budget-program v3.1.14
   Compiling solana-vote-program v3.1.14
   Compiling regex-automata v0.4.14
   Compiling anchor-lang-idl-spec v0.1.0
   Compiling solana-zk-sdk v4.0.0
   Compiling agave-syscalls v3.1.14
   Compiling solana-zk-token-sdk v3.1.14
   Compiling solana-bpf-loader-program v3.1.14
   Compiling anchor-lang-idl v0.1.3
   Compiling keccak-const v0.2.0
   Compiling solana-define-syscall v3.0.0
   Compiling solana-loader-v4-program v3.1.14
   Compiling solana-invoke v0.5.0
   Compiling const-crypto v0.3.0
   Compiling solana-builtins-default-costs v3.1.14
   Compiling anchor-derive-accounts v1.0.2
   Compiling regex v1.12.3
   Compiling anchor-attribute-account v1.0.2
   Compiling anchor-attribute-constant v1.0.2
   Compiling anchor-attribute-error v1.0.2
   Compiling anchor-derive-serde v1.0.2
   Compiling anchor-attribute-event v1.0.2
   Compiling anchor-attribute-program v1.0.2
   Compiling solana-compute-budget v3.1.14
   Compiling solana-compute-budget-interface v3.0.0
   Compiling solana-feature-gate-interface v3.1.0
   Compiling solana-program-pack v3.1.0
   Compiling solana-borsh v3.0.2
   Compiling anchor-attribute-access-control v1.0.2
   Compiling anchor-derive-space v1.0.2
   Compiling solana-program-option v3.1.0
   Compiling base64 v0.21.7
   Compiling solana-compute-budget-instruction v3.1.14
   Compiling solana-fee v3.1.14
   Compiling agave-reserved-account-keys v3.1.14
   Compiling solana-address-lookup-table-interface v3.1.0
   Compiling itertools v0.14.0
   Compiling anchor-lang v1.0.2
   Compiling solana-native-token v3.0.0
   Compiling solana-zk-elgamal-proof-program v3.1.14
   Compiling ansi_term v0.12.1
   Compiling solana-security-txt v1.1.3
   Compiling plotarmor v0.1.0 (/home/<usr>/plotarmor-program/.cutover-pass3/head/programs/plotarmor)
   Compiling solana-zk-token-proof-program v3.1.14
   Compiling solana-builtins v3.1.14
   Compiling litesvm v0.10.0
    Finished `test` profile [unoptimized + debuginfo] target(s) in 23m 31s
     Running unittests src/lib.rs (/home/<usr>/plotarmor-program/.cutover-pass3/head/target/debug/deps/plotarmor-d5140aaaa4041b11)
     Running tests/happy_paths.rs (/home/<usr>/plotarmor-program/.cutover-pass3/head/target/debug/deps/happy_paths-4beb9126c1ce0080)
     Running tests/security_tests.rs (/home/<usr>/plotarmor-program/.cutover-pass3/head/target/debug/deps/security_tests-ad5cac0c007edf49)
     Running tests/sign_contract_tests.rs (/home/<usr>/plotarmor-program/.cutover-pass3/head/target/debug/deps/sign_contract_tests-0a71df0c6bdccafb)

exit_code=0
````

````bash
python3 - <<'PY'
import pathlib,subprocess,hashlib
for rev,label in [("09c5bfc","old"),("HEAD","head")]:
 files=subprocess.check_output(["git","ls-tree","-r","--name-only",rev],text=True).splitlines()
 checked=0
 for name in files:
  if name.startswith("programs/") or name in ["Cargo.toml","Cargo.lock","Anchor.toml","scripts/build.sh"]:
   source=subprocess.check_output(["git","show",rev+":"+name]);copy=pathlib.Path(".cutover-pass3",label,name).read_bytes()
   assert source==copy,(rev,name)
   checked+=1
 print(rev,"archived tracked build/source files match commit:",checked)
 print(rev,"Cargo.lock sha256",hashlib.sha256(pathlib.Path(".cutover-pass3",label,"Cargo.lock").read_bytes()).hexdigest())
PY
````
````text
09c5bfc archived tracked build/source files match commit: 22
09c5bfc Cargo.lock sha256 17ffb5f9f88ab1f9a6f8d52254817c14e42c0c81134a4eb40e43640fcdf7e97b
HEAD archived tracked build/source files match commit: 23
HEAD Cargo.lock sha256 1944f68bcfce259ec18e9e44e909ac296fbad38d74b1f775da8992abc1a93dd9

exit_code=0
````

````bash
cat /tmp/pass3-fee.cjs; node /tmp/pass3-fee.cjs
````
````text
const {Connection,PublicKey,Transaction,SystemProgram}=require('/home/<usr>/plotarmor-program/node_modules/@solana/web3.js');
(async()=>{const c=new Connection('https://api.devnet.solana.com','finalized');const a=new PublicKey('EjeeFw3Ft856o9Ek2VWti6aAco9RXxGUyeLk96dPSWzd');const {blockhash}=await c.getLatestBlockhash();const t=new Transaction({feePayer:a,recentBlockhash:blockhash}).add(SystemProgram.transfer({fromPubkey:a,toPubkey:a,lamports:0}));const m=t.compileMessage();console.log('Unsigned message required signatures:',m.header.numRequiredSignatures);console.log('getFeeForMessage:',JSON.stringify(await c.getFeeForMessage(m,'finalized')));console.log('No signing, simulation or submission performed. Actual upgrade total fees depend on upload transactions and retries.');})().catch(e=>{console.error(e);process.exitCode=1});
Unsigned message required signatures: 1
getFeeForMessage: {"context":{"apiVersion":"4.4.0-beta.0","slot":508408291},"value":5000}
No signing, simulation or submission performed. Actual upgrade total fees depend on upload transactions and retries.

exit_code=0
````

````bash
NO_DNA=1 cargo build-sbf --version; /home/<usr>/.cache/solana/v1.52/platform-tools/rust/bin/rustc --version; readlink /home/<usr>/.rustup/toolchains/sbpf; git show 09c5bfc:programs/plotarmor/src/lib.rs | sed -n "30,160p"; sed -n "55,180p" programs/plotarmor/src/lib.rs; sed -n "50,100p" docs/CUTOVER_2026-10.md
````
````text
cargo-build-sbf 4.0.0
platform-tools v1.53
rustc 1.89.0
rustc 1.89.0-dev
use instructions::sign_contract::__client_accounts_sign_contract;
pub use instructions::SignContract;
pub use state::*;

declare_id!("3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2");

#[program]
pub mod plotarmor {
    use super::*;

    pub fn init_registry_config(ctx: Context<InitRegistryConfig>) -> Result<()> {
        instructions::init_registry_config::handler(ctx)
    }

    pub fn add_owner(
        ctx: Context<AddOwner>,
        new_share: u16,
        new_role: u8,
        new_threshold_shares: u16,
    ) -> Result<()> {
        instructions::add_owner::handler(ctx, new_share, new_role, new_threshold_shares)
    }

    pub fn anchor_authorized_contract(
        ctx: Context<AnchorAuthorizedContract>,
        raw_contract_hash: [u8; 32],
        contract_kind: u8,
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::anchor_authorized_contract::handler(
            ctx,
            raw_contract_hash,
            contract_kind,
            anchor_nonce,
            anchor_mode_arg,
            external_ref_hash,
        )
    }

    pub fn anchor_evidence_contract(
        ctx: Context<AnchorEvidenceContract>,
        raw_contract_hash: [u8; 32],
        contract_kind: u8,
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        asserted_work_claim: Pubkey,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::anchor_evidence_contract::handler(
            ctx,
            raw_contract_hash,
            contract_kind,
            anchor_nonce,
            anchor_mode_arg,
            asserted_work_claim,
            external_ref_hash,
        )
    }

    pub fn add_version(
        ctx: Context<AddVersion>,
        raw_hash: [u8; 32],
        content_kind: u8,
        link_nonce: [u8; 32],
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        expected_previous_link: Pubkey,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::add_version::handler(
            ctx,
            raw_hash,
            content_kind,
            link_nonce,
            anchor_nonce,
            anchor_mode_arg,
            expected_previous_link,
            external_ref_hash,
        )
    }

    pub fn register_work_claim(
        ctx: Context<RegisterWorkClaim>,
        raw_hash: [u8; 32],
        content_kind: u8,
        claim_kind: u8,
        total_shares: u16,
        threshold_shares: u16,
        link_nonce: [u8; 32],
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::register_work_claim::handler(
            ctx,
            raw_hash,
            content_kind,
            claim_kind,
            total_shares,
            threshold_shares,
            link_nonce,
            anchor_nonce,
            anchor_mode_arg,
            external_ref_hash,
        )
    }

    pub fn sign_contract(
        ctx: Context<SignContract>,
        content_hash: [u8; 32],
    ) -> Result<()> {
        instructions::sign_contract::handler(ctx, content_hash)
    }
}

declare_id!("3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2");

#[program]
pub mod plotarmor {
    use super::*;

    pub fn init_registry_config(ctx: Context<InitRegistryConfig>) -> Result<()> {
        instructions::init_registry_config::handler(ctx)
    }

    pub fn add_owner(
        ctx: Context<AddOwner>,
        new_share: u16,
        new_role: u8,
        new_threshold_shares: u16,
    ) -> Result<()> {
        instructions::add_owner::handler(ctx, new_share, new_role, new_threshold_shares)
    }

    pub fn anchor_authorized_contract(
        ctx: Context<AnchorAuthorizedContract>,
        raw_contract_hash: [u8; 32],
        contract_kind: u8,
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::anchor_authorized_contract::handler(
            ctx,
            raw_contract_hash,
            contract_kind,
            anchor_nonce,
            anchor_mode_arg,
            external_ref_hash,
        )
    }

    pub fn anchor_evidence_contract(
        ctx: Context<AnchorEvidenceContract>,
        raw_contract_hash: [u8; 32],
        contract_kind: u8,
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        asserted_work_claim: Pubkey,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::anchor_evidence_contract::handler(
            ctx,
            raw_contract_hash,
            contract_kind,
            anchor_nonce,
            anchor_mode_arg,
            asserted_work_claim,
            external_ref_hash,
        )
    }

    pub fn add_version(
        ctx: Context<AddVersion>,
        raw_hash: [u8; 32],
        content_kind: u8,
        link_nonce: [u8; 32],
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        expected_previous_link: Pubkey,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::add_version::handler(
            ctx,
            raw_hash,
            content_kind,
            link_nonce,
            anchor_nonce,
            anchor_mode_arg,
            expected_previous_link,
            external_ref_hash,
        )
    }

    pub fn register_work_claim(
        ctx: Context<RegisterWorkClaim>,
        raw_hash: [u8; 32],
        content_kind: u8,
        claim_kind: u8,
        total_shares: u16,
        threshold_shares: u16,
        link_nonce: [u8; 32],
        anchor_nonce: [u8; 32],
        anchor_mode_arg: u8,
        external_ref_hash: [u8; 32],
    ) -> Result<()> {
        instructions::register_work_claim::handler(
            ctx,
            raw_hash,
            content_kind,
            claim_kind,
            total_shares,
            threshold_shares,
            link_nonce,
            anchor_nonce,
            anchor_mode_arg,
            external_ref_hash,
        )
    }

    pub fn sign_contract(
        ctx: Context<SignContract>,
        content_hash: [u8; 32],
    ) -> Result<()> {
        instructions::sign_contract::handler(ctx, content_hash)
    }
}

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

exit_code=0
````

````bash
curl -fsSL https://raw.githubusercontent.com/anza-xyz/agave/v4.0.1/cli/src/program.rs -o /tmp/pass3-solana-cli-program.rs && sha256sum /tmp/pass3-solana-cli-program.rs && sed -n "2708,2727p;2970,2995p;3030,3095p" /tmp/pass3-solana-cli-program.rs
````
````text
curl: (6) Could not resolve host: raw.githubusercontent.com

exit_code=6
````

````bash
curl -fsSL https://raw.githubusercontent.com/anza-xyz/agave/v4.0.1/cli/src/program.rs -o /tmp/pass3-solana-cli-program.rs && sha256sum /tmp/pass3-solana-cli-program.rs && sed -n "2708,2727p;2970,2995p;3030,3095p" /tmp/pass3-solana-cli-program.rs
````
````text
123271ca58a98e8300c287f78c7635dd955f1e70eb1348d49b5cd74a14c7fd5c  /tmp/pass3-solana-cli-program.rs
pub fn calculate_max_chunk_size(baseline_msg: Message) -> usize {
    let tx_size = bincode::serialized_size(&Transaction {
        signatures: vec![
            Signature::default();
            baseline_msg.header.num_required_signatures as usize
        ],
        message: baseline_msg,
    })
    .unwrap() as usize;
    // add 1 byte buffer to account for shortvec encoding
    PACKET_DATA_SIZE.saturating_sub(tx_size).saturating_sub(1)
}

#[allow(clippy::too_many_arguments)]
async fn do_process_program_deploy(
    rpc_client: Arc<RpcClient>,
    config: &CliConfig<'_>,
    program_data: &[u8], // can be empty, hence we have program_len
    program_len: usize,
    program_data_max_len: usize,
async fn do_process_program_upgrade(
    rpc_client: Arc<RpcClient>,
    config: &CliConfig<'_>,
    program_data: &[u8], // can be empty, hence we have program_len
    program_len: usize,
    min_rent_exempt_program_data_balance: u64,
    fee_payer_signer: &dyn Signer,
    program_id: &Pubkey,
    upgrade_authority: &dyn Signer,
    buffer_pubkey: &Pubkey,
    buffer_signer: Option<&dyn Signer>,
    buffer_program_data: Option<Vec<u8>>,
    skip_fee_check: bool,
    compute_unit_price: Option<u64>,
    max_sign_attempts: usize,
    auto_extend: bool,
    use_rpc: bool,
) -> ProcessResult {
    let blockhash = rpc_client.get_latest_blockhash().await?;
    let compute_unit_limit = ComputeUnitLimit::Simulated;

    let (initial_message, write_messages, balance_needed) = if let Some(buffer_signer) =
        buffer_signer
    {
        let (mut initial_instructions, balance_needed, buffer_program_data) =
            if let Some(buffer_program_data) = buffer_program_data {
                &blockhash,
            ))
        } else {
            None
        };

        let buffer_signer_pubkey = buffer_signer.pubkey();
        let upgrade_authority_pubkey = upgrade_authority.pubkey();
        let create_msg = |offset: u32, bytes: Vec<u8>| {
            let instructions = vec![loader_v3_instruction::write(
                &buffer_signer_pubkey,
                &upgrade_authority_pubkey,
                offset,
                bytes,
            )]
            .with_compute_unit_config(&ComputeUnitConfig {
                compute_unit_price,
                compute_unit_limit,
            });
            Message::new_with_blockhash(&instructions, Some(&fee_payer_signer.pubkey()), &blockhash)
        };

        // Create and add write messages
        let mut write_messages = vec![];
        let chunk_size = calculate_max_chunk_size(create_msg(0, Vec::new()));
        for (chunk, i) in program_data.chunks(chunk_size).zip(0usize..) {
            let offset = i.saturating_mul(chunk_size);
            if chunk != &buffer_program_data[offset..offset.saturating_add(chunk.len())] {
                write_messages.push(create_msg(offset as u32, chunk.to_vec()));
            }
        }

        (initial_message, write_messages, balance_needed)
    } else {
        (None, vec![], 0)
    };

    // Create and add final message
    let final_instructions = vec![loader_v3_instruction::upgrade(
        program_id,
        buffer_pubkey,
        &upgrade_authority.pubkey(),
        &fee_payer_signer.pubkey(),
    )]
    .with_compute_unit_config(&ComputeUnitConfig {
        compute_unit_price,
        compute_unit_limit,
    });
    let final_message = Message::new_with_blockhash(
        &final_instructions,
        Some(&fee_payer_signer.pubkey()),
        &blockhash,
    );
    let final_message = Some(final_message);

    if !skip_fee_check {
        check_payer(
            &rpc_client,
            config,
            fee_payer_signer.pubkey(),
            balance_needed,
            &initial_message,
            &write_messages,
            &final_message,
        )
        .await?;

exit_code=0
````

````bash
python3 - <<'PY'
import pathlib,hashlib
for n,p in [("live","/tmp/pass3-live.so"),("cold 09c5bfc",".cutover-pass3/old/target/deploy/plotarmor.so")]:
 b=pathlib.Path(p).read_bytes();print(n,"bytes",len(b),"trimmed",len(b.rstrip(b"\0")),"sha256",hashlib.sha256(b).hexdigest(),"trimmed_sha256",hashlib.sha256(b.rstrip(b"\0")).hexdigest())
assert pathlib.Path("/tmp/pass3-live.so").read_bytes().rstrip(b"\0")==pathlib.Path(".cutover-pass3/old/target/deploy/plotarmor.so").read_bytes().rstrip(b"\0")
print("PASS: live bytes match cold 09c5bfc build")
PY
````
````text
live bytes 471960 trimmed 470257 sha256 7d43bcb222c6e71d8cfe77db2fe3a48dc82704573873f04ef0c8d144de877235 trimmed_sha256 5663e20f992914ad1a2671888fd3062a36df69ecc6ac81ee1318f9e702bc3fb5
cold 09c5bfc bytes 470272 trimmed 470257 sha256 bcd70bb29d6acafb9d3fab6c80fff52358decfacd52315f703719d35e6024142 trimmed_sha256 5663e20f992914ad1a2671888fd3062a36df69ecc6ac81ee1318f9e702bc3fb5
PASS: live bytes match cold 09c5bfc build

exit_code=0
````

````bash
cd .cutover-pass3/old && CARGO_TARGET_DIR=/home/<usr>/plotarmor-program/target NO_DNA=1 anchor idl build -o /tmp/pass3-old-idl.json
````
````text
   Compiling plotarmor v0.1.0 (/home/<usr>/plotarmor-program/.cutover-pass3/old/programs/plotarmor)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 6m 48s
     Running unittests src/lib.rs (/home/<usr>/plotarmor-program/target/debug/deps/plotarmor-5e8b59803e9d03e3)
     Running tests/happy_paths.rs (/home/<usr>/plotarmor-program/target/debug/deps/happy_paths-128f2fa5165339af)
     Running tests/security_tests.rs (/home/<usr>/plotarmor-program/target/debug/deps/security_tests-18d9b6115db5dbf1)
     Running tests/sign_contract_tests.rs (/home/<usr>/plotarmor-program/target/debug/deps/sign_contract_tests-6f0d255ef284f87d)

exit_code=0
````

````bash
cd .cutover-pass3/head && CARGO_TARGET_DIR=/home/<usr>/plotarmor-program/target NO_DNA=1 anchor idl build -o /tmp/pass3-head-idl.json
````
````text
    Blocking waiting for file lock on build directory
   Compiling plotarmor v0.1.0 (/home/<usr>/plotarmor-program/.cutover-pass3/head/programs/plotarmor)
error: couldn't read `programs/plotarmor/tests/common/../../../../target/deploy/plotarmor.so`: No such file or directory (os error 2)
  --> programs/plotarmor/tests/common/mod.rs:51:9
   |
51 |         include_bytes!("../../../../target/deploy/plotarmor.so");
   |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |
help: there is a file with the same name in a different directory
   |
51 |         include_bytes!("../../../../../../target/deploy/plotarmor.so");
   |                                     ++++++

error: could not compile `plotarmor` (test "sign_contract_tests") due to 1 previous error
warning: build failed, waiting for other jobs to finish...
error: could not compile `plotarmor` (test "security_tests") due to 1 previous error
error: could not compile `plotarmor` (test "happy_paths") due to 1 previous error
Error: Building IDL failed. Run `ANCHOR_LOG=true anchor idl build` to see the logs.

exit_code=1
````

````bash
cat /tmp/pass3-compare.py; python3 /tmp/pass3-compare.py; scripts/guard_deploy_artifact.sh .cutover-pass3/head/target/deploy/plotarmor.so; cat /tmp/pass3-cost.py; python3 /tmp/pass3-cost.py
````
````text
import json,pathlib,hashlib,difflib,subprocess
root=pathlib.Path('/home/<usr>/plotarmor-program')
a=json.loads((root/'.cutover-pass3/old/target/idl/plotarmor.json').read_text());b=json.loads((root/'.cutover-pass3/head/target/idl/plotarmor.json').read_text())
print('IDL whole-document unified diff:')
print(''.join(difflib.unified_diff(json.dumps(a,indent=2,sort_keys=True).splitlines(True),json.dumps(b,indent=2,sort_keys=True).splitlines(True),fromfile='09c5bfc generated IDL',tofile='HEAD generated IDL')))
for section in ['instructions','accounts','types','events','errors','constants']:
 aa={x['name']:x for x in a.get(section,[])};bb={x['name']:x for x in b.get(section,[])}
 print(section,'old_count',len(aa),'new_count',len(bb))
 for name in sorted(aa.keys()|bb.keys()):
  same=aa.get(name)==bb.get(name)
  print(' ',name,'IDENTICAL' if same else 'DIFFERENT')
  if section=='instructions':
   for label,d in [('09c5bfc',aa.get(name)),('HEAD',bb.get(name))]:
    print('  ',label,json.dumps(d,sort_keys=True))
for name in ['register_work_claim','add_version']:
 old=next(x for x in a['instructions'] if x['name']==name);new=next(x for x in b['instructions'] if x['name']==name)
 assert old==new
 path='programs/plotarmor/src/instructions/'+name+'.rs'
 oldsrc=subprocess.check_output(['git','show','09c5bfc:'+path],cwd=root);newsrc=subprocess.check_output(['git','show','HEAD:'+path],cwd=root)
 assert oldsrc==newsrc
 print(name,'IDL and entire instruction source byte-identical; source sha256',hashlib.sha256(oldsrc).hexdigest())
for label,p in [('live',pathlib.Path('/tmp/pass3-live.so')),('09c5bfc',root/'.cutover-pass3/old/target/deploy/plotarmor.so'),('HEAD',root/'.cutover-pass3/head/target/deploy/plotarmor.so')]:
 data=p.read_bytes();trim=data.rstrip(b'\0')
 print(label,'size',len(data),'sha256',hashlib.sha256(data).hexdigest(),'trimmed_size',len(trim),'trimmed_sha256',hashlib.sha256(trim).hexdigest())
live=pathlib.Path('/tmp/pass3-live.so').read_bytes().rstrip(b'\0');old=(root/'.cutover-pass3/old/target/deploy/plotarmor.so').read_bytes().rstrip(b'\0');new=(root/'.cutover-pass3/head/target/deploy/plotarmor.so').read_bytes().rstrip(b'\0')
assert live==old
assert hashlib.sha256(new).hexdigest()=='bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2'
print('PASS: live trimmed bytes equal cold 09c5bfc build; HEAD passes audited hash')
IDL whole-document unified diff:
--- 09c5bfc generated IDL
+++ HEAD generated IDL
@@ -1288,6 +1288,24 @@
     {
       "accounts": [
         {
+          "name": "registry_config",
+          "pda": {
+            "seeds": [
+              {
+                "kind": "const",
+                "value": [
+                  99,
+                  111,
+                  110,
+                  102,
+                  105,
+                  103
+                ]
+              }
+            ]
+          }
+        },
+        {
           "name": "contract_artifact",
           "pda": {
             "seeds": [

instructions old_count 7 new_count 7
  add_owner IDENTICAL
   09c5bfc {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.root_artifact"}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.claimant"}]}}, {"name": "ownership", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114, 115, 104, 105, 112]}, {"kind": "account", "path": "work_claim"}]}, "writable": true}, {"name": "new_owner_record", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114]}, {"kind": "account", "path": "ownership"}, {"kind": "account", "path": "new_owner"}]}, "writable": true}, {"name": "admin", "relations": ["ownership"], "signer": true, "writable": true}, {"name": "new_owner"}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "new_share", "type": "u16"}, {"name": "new_role", "type": "u8"}, {"name": "new_threshold_shares", "type": "u16"}], "discriminator": [211, 140, 15, 161, 64, 48, 232, 184], "name": "add_owner"}
   HEAD {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.root_artifact"}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.claimant"}]}}, {"name": "ownership", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114, 115, 104, 105, 112]}, {"kind": "account", "path": "work_claim"}]}, "writable": true}, {"name": "new_owner_record", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114]}, {"kind": "account", "path": "ownership"}, {"kind": "account", "path": "new_owner"}]}, "writable": true}, {"name": "admin", "relations": ["ownership"], "signer": true, "writable": true}, {"name": "new_owner"}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "new_share", "type": "u16"}, {"name": "new_role", "type": "u8"}, {"name": "new_threshold_shares", "type": "u16"}], "discriminator": [211, 140, 15, 161, 64, 48, 232, 184], "name": "add_owner"}
  add_version IDENTICAL
   09c5bfc {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.root_artifact"}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.claimant"}]}, "writable": true}, {"name": "content_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 101, 110, 116]}, {"kind": "arg", "path": "raw_hash"}]}, "writable": true}, {"name": "claim_artifact_link", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "account", "path": "work_claim"}, {"kind": "arg", "path": "link_nonce"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "content_artifact"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "claimant", "relations": ["work_claim"], "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_hash", "type": {"array": ["u8", 32]}}, {"name": "content_kind", "type": "u8"}, {"name": "link_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "expected_previous_link", "type": "pubkey"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [167, 42, 0, 24, 83, 109, 61, 248], "name": "add_version"}
   HEAD {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.root_artifact"}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.claimant"}]}, "writable": true}, {"name": "content_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 101, 110, 116]}, {"kind": "arg", "path": "raw_hash"}]}, "writable": true}, {"name": "claim_artifact_link", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "account", "path": "work_claim"}, {"kind": "arg", "path": "link_nonce"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "content_artifact"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "claimant", "relations": ["work_claim"], "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_hash", "type": {"array": ["u8", 32]}}, {"name": "content_kind", "type": "u8"}, {"name": "link_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "expected_previous_link", "type": "pubkey"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [167, 42, 0, 24, 83, 109, 61, 248], "name": "add_version"}
  anchor_authorized_contract IDENTICAL
   09c5bfc {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.root_artifact"}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.claimant"}]}}, {"name": "ownership", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114, 115, 104, 105, 112]}, {"kind": "account", "path": "work_claim"}]}}, {"name": "contract_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 114, 97, 99, 116, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "arg", "path": "raw_contract_hash"}]}, "writable": true}, {"name": "authorized_contract_anchor", "pda": {"seeds": [{"kind": "const", "value": [97, 117, 116, 104, 111, 114, 105, 122, 101, 100, 95, 99, 111, 110, 116, 114, 97, 99, 116]}, {"kind": "account", "path": "work_claim"}, {"kind": "account", "path": "contract_artifact"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "authorized_contract_anchor"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "admin", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_contract_hash", "type": {"array": ["u8", 32]}}, {"name": "contract_kind", "type": "u8"}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [210, 79, 150, 32, 196, 91, 92, 64], "name": "anchor_authorized_contract"}
   HEAD {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.root_artifact"}, {"account": "WorkClaim", "kind": "account", "path": "work_claim.claimant"}]}}, {"name": "ownership", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114, 115, 104, 105, 112]}, {"kind": "account", "path": "work_claim"}]}}, {"name": "contract_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 114, 97, 99, 116, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "arg", "path": "raw_contract_hash"}]}, "writable": true}, {"name": "authorized_contract_anchor", "pda": {"seeds": [{"kind": "const", "value": [97, 117, 116, 104, 111, 114, 105, 122, 101, 100, 95, 99, 111, 110, 116, 114, 97, 99, 116]}, {"kind": "account", "path": "work_claim"}, {"kind": "account", "path": "contract_artifact"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "authorized_contract_anchor"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "admin", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_contract_hash", "type": {"array": ["u8", 32]}}, {"name": "contract_kind", "type": "u8"}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [210, 79, 150, 32, 196, 91, 92, 64], "name": "anchor_authorized_contract"}
  anchor_evidence_contract IDENTICAL
   09c5bfc {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "contract_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 114, 97, 99, 116, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "arg", "path": "raw_contract_hash"}]}, "writable": true}, {"name": "evidence_anchor", "pda": {"seeds": [{"kind": "const", "value": [101, 118, 105, 100, 101, 110, 99, 101]}, {"kind": "account", "path": "anchorer"}, {"kind": "account", "path": "contract_artifact"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "evidence_anchor"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "anchorer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_contract_hash", "type": {"array": ["u8", 32]}}, {"name": "contract_kind", "type": "u8"}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "asserted_work_claim", "type": "pubkey"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [5, 43, 187, 2, 36, 176, 229, 86], "name": "anchor_evidence_contract"}
   HEAD {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "contract_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 114, 97, 99, 116, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "arg", "path": "raw_contract_hash"}]}, "writable": true}, {"name": "evidence_anchor", "pda": {"seeds": [{"kind": "const", "value": [101, 118, 105, 100, 101, 110, 99, 101]}, {"kind": "account", "path": "anchorer"}, {"kind": "account", "path": "contract_artifact"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "evidence_anchor"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "anchorer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_contract_hash", "type": {"array": ["u8", 32]}}, {"name": "contract_kind", "type": "u8"}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "asserted_work_claim", "type": "pubkey"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [5, 43, 187, 2, 36, 176, 229, 86], "name": "anchor_evidence_contract"}
  init_registry_config IDENTICAL
   09c5bfc {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}, "writable": true}, {"name": "signer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}, {"address": "3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2", "name": "program"}, {"name": "program_data"}], "args": [], "discriminator": [157, 90, 204, 184, 92, 221, 52, 86], "name": "init_registry_config"}
   HEAD {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}, "writable": true}, {"name": "signer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}, {"address": "3h9CzV9MJDeD5yjhVhdE6cupuXVRnLW1Cu6P14EJBKv2", "name": "program"}, {"name": "program_data"}], "args": [], "discriminator": [157, 90, 204, 184, 92, 221, 52, 86], "name": "init_registry_config"}
  register_work_claim IDENTICAL
   09c5bfc {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "content_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 101, 110, 116]}, {"kind": "arg", "path": "raw_hash"}]}, "writable": true}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"kind": "account", "path": "content_artifact"}, {"kind": "account", "path": "signer"}]}, "writable": true}, {"name": "ownership", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114, 115, 104, 105, 112]}, {"kind": "account", "path": "work_claim"}]}, "writable": true}, {"name": "owner_record", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114]}, {"kind": "account", "path": "ownership"}, {"kind": "account", "path": "signer"}]}, "writable": true}, {"name": "claim_artifact_link", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "account", "path": "work_claim"}, {"kind": "arg", "path": "link_nonce"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "work_claim"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "signer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_hash", "type": {"array": ["u8", 32]}}, {"name": "content_kind", "type": "u8"}, {"name": "claim_kind", "type": "u8"}, {"name": "total_shares", "type": "u16"}, {"name": "threshold_shares", "type": "u16"}, {"name": "link_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [128, 224, 48, 240, 166, 14, 119, 76], "name": "register_work_claim"}
   HEAD {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "content_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 101, 110, 116]}, {"kind": "arg", "path": "raw_hash"}]}, "writable": true}, {"name": "work_claim", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109]}, {"kind": "account", "path": "content_artifact"}, {"kind": "account", "path": "signer"}]}, "writable": true}, {"name": "ownership", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114, 115, 104, 105, 112]}, {"kind": "account", "path": "work_claim"}]}, "writable": true}, {"name": "owner_record", "pda": {"seeds": [{"kind": "const", "value": [111, 119, 110, 101, 114]}, {"kind": "account", "path": "ownership"}, {"kind": "account", "path": "signer"}]}, "writable": true}, {"name": "claim_artifact_link", "pda": {"seeds": [{"kind": "const", "value": [99, 108, 97, 105, 109, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"kind": "account", "path": "work_claim"}, {"kind": "arg", "path": "link_nonce"}]}, "writable": true}, {"name": "anchor_record", "pda": {"seeds": [{"kind": "const", "value": [97, 110, 99, 104, 111, 114]}, {"kind": "account", "path": "work_claim"}, {"kind": "arg", "path": "anchor_nonce"}]}, "writable": true}, {"name": "signer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "raw_hash", "type": {"array": ["u8", 32]}}, {"name": "content_kind", "type": "u8"}, {"name": "claim_kind", "type": "u8"}, {"name": "total_shares", "type": "u16"}, {"name": "threshold_shares", "type": "u16"}, {"name": "link_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_nonce", "type": {"array": ["u8", 32]}}, {"name": "anchor_mode_arg", "type": "u8"}, {"name": "external_ref_hash", "type": {"array": ["u8", 32]}}], "discriminator": [128, 224, 48, 240, 166, 14, 119, 76], "name": "register_work_claim"}
  sign_contract DIFFERENT
   09c5bfc {"accounts": [{"name": "contract_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 114, 97, 99, 116, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"account": "ContractArtifact", "kind": "account", "path": "contract_artifact.raw_hash"}]}}, {"name": "contract_signature", "pda": {"seeds": [{"kind": "const", "value": [115, 105, 103, 110, 97, 116, 117, 114, 101]}, {"kind": "account", "path": "contract_artifact"}, {"kind": "account", "path": "signer"}]}, "writable": true}, {"name": "signer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "content_hash", "type": {"array": ["u8", 32]}}], "discriminator": [145, 83, 234, 177, 104, 87, 183, 156], "name": "sign_contract"}
   HEAD {"accounts": [{"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}, {"name": "contract_artifact", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 116, 114, 97, 99, 116, 95, 97, 114, 116, 105, 102, 97, 99, 116]}, {"account": "ContractArtifact", "kind": "account", "path": "contract_artifact.raw_hash"}]}}, {"name": "contract_signature", "pda": {"seeds": [{"kind": "const", "value": [115, 105, 103, 110, 97, 116, 117, 114, 101]}, {"kind": "account", "path": "contract_artifact"}, {"kind": "account", "path": "signer"}]}, "writable": true}, {"name": "signer", "signer": true, "writable": true}, {"address": "11111111111111111111111111111111", "name": "system_program"}], "args": [{"name": "content_hash", "type": {"array": ["u8", 32]}}], "discriminator": [145, 83, 234, 177, 104, 87, 183, 156], "name": "sign_contract"}
accounts old_count 11 new_count 11
  AnchorRecord IDENTICAL
  AuthorizedContractAnchor IDENTICAL
  ClaimArtifactLink IDENTICAL
  ContentArtifact IDENTICAL
  ContractArtifact IDENTICAL
  ContractSignature IDENTICAL
  EvidenceAnchor IDENTICAL
  OwnerRecord IDENTICAL
  Ownership IDENTICAL
  RegistryConfig IDENTICAL
  WorkClaim IDENTICAL
types old_count 11 new_count 11
  AnchorRecord IDENTICAL
  AuthorizedContractAnchor IDENTICAL
  ClaimArtifactLink IDENTICAL
  ContentArtifact IDENTICAL
  ContractArtifact IDENTICAL
  ContractSignature IDENTICAL
  EvidenceAnchor IDENTICAL
  OwnerRecord IDENTICAL
  Ownership IDENTICAL
  RegistryConfig IDENTICAL
  WorkClaim IDENTICAL
events old_count 0 new_count 0
errors old_count 12 new_count 12
  AlreadyInitialized IDENTICAL
  AnchorModeNotAllowed IDENTICAL
  ContentHashMismatch IDENTICAL
  Paused IDENTICAL
  ReservedFieldNonZero IDENTICAL
  ShareOverflow IDENTICAL
  ShareSumMismatch IDENTICAL
  SimulatedModeRejected IDENTICAL
  StaleLineageHead IDENTICAL
  SupersededClaim IDENTICAL
  ThresholdNotMet IDENTICAL
  Unauthorized IDENTICAL
constants old_count 1 new_count 1
  SEED IDENTICAL
register_work_claim IDL and entire instruction source byte-identical; source sha256 61812a435d308c540471d72796ff860b6b8d9820520bf6fcd51b1d404fdd923f
add_version IDL and entire instruction source byte-identical; source sha256 42b37c51a70e5a985f697f148c3b66b42aba4463ebadc5e121b6ce7d1cad19df
live size 471960 sha256 7d43bcb222c6e71d8cfe77db2fe3a48dc82704573873f04ef0c8d144de877235 trimmed_size 470257 trimmed_sha256 5663e20f992914ad1a2671888fd3062a36df69ecc6ac81ee1318f9e702bc3fb5
09c5bfc size 470272 sha256 bcd70bb29d6acafb9d3fab6c80fff52358decfacd52315f703719d35e6024142 trimmed_size 470257 trimmed_sha256 5663e20f992914ad1a2671888fd3062a36df69ecc6ac81ee1318f9e702bc3fb5
HEAD size 472440 sha256 97880b057e52f474f20bb209f586e708eaf96d5608bcc52403ca62bc396916b7 trimmed_size 472425 trimmed_sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
PASS: live trimmed bytes equal cold 09c5bfc build; HEAD passes audited hash
artifact OK: .cutover-pass3/head/target/deploy/plotarmor.so trimmed sha256 bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2
import json,pathlib,re
s=json.loads(pathlib.Path('/tmp/pass3-chain-snapshot.json').read_text());runbook=pathlib.Path('docs/CUTOVER_2026-10.md').read_text();a=s['result']['value'];r=s['rents'];rate=s['rate'];held=a[1]['lamports'];balance=a[3]['lamports']
import base64
pd=len(base64.b64decode(a[1]['data'][0]));new=pathlib.Path('.cutover-pass3/head/target/deploy/plotarmor.so').stat().st_size
extend=int(re.search(r'solana program extend 3h9\S+ (\d+)',runbook)[1]);rent=lambda n:(128+n)*rate
rows=[('ProgramData bytes',pd,472005),('ProgramData lamports',held,3286045680),('New SO bytes',new,472440),('Minimum growth bytes',new-(pd-45),480),('Extend bytes',extend,10240),('Extended ProgramData bytes',pd+extend,482245),('Extended program capacity',pd+extend-45,482200),('Rent per byte lamports',rate,5080),('Current rent minimum',rent(pd),2398435640),('Exact-fit rent minimum',rent(45+new),2400874040),('Extended rent minimum',rent(pd+extend),2450454840),('Buffer rent',rent(37+new),2400833400),('Extend rent topup',max(rent(pd+extend)-held,0),0),('Authority balance',balance,5400565851)]
for name,observed,expected in rows:print(f'{name}: observed={observed}; runbook={expected}; delta={observed-expected}')
refund=held-rent(pd+extend);spill=refund+rent(37+new)
print('Upgrade spill to fee payer (CLI v4.0.1 source):',spill,'lamports')
print('Net authority gain before fees:',refund,'lamports')
print('Expected authority balance: balance + net gain - actual total fees')
print('Expected balance before fees:',f'{(balance+refund)/1e9:.9f}','SOL')
print('Expected balance using runbook 0.0025 SOL fee estimate:',f'{(balance+refund-2500000)/1e9:.9f}','SOL')
print('Difference from runbook approximately 6.236 SOL:',f'{(balance+refund-2500000)/1e9-6.236:.9f}','SOL')
print('Peak funding using runbook fee estimate:',f'{(rent(37+new)+2500000)/1e9:.9f}','SOL (runbook approximately 2.4034 SOL)')
print('Actual total transaction fees are unmeasured: no on-chain transactions sent in pass 3.')
print('Runbook difference: source precheck exits 1 because scripts/guard_deploy_artifact.sh was added after f34bfae; program source and build inputs match f34bfae.')
print('Runbook difference: approximately 6.236 SOL is the pre-fee balance; approximately 6.233657 SOL follows its 0.0025 SOL fee estimate.')
ProgramData bytes: observed=472005; runbook=472005; delta=0
ProgramData lamports: observed=3286045680; runbook=3286045680; delta=0
New SO bytes: observed=472440; runbook=472440; delta=0
Minimum growth bytes: observed=480; runbook=480; delta=0
Extend bytes: observed=10240; runbook=10240; delta=0
Extended ProgramData bytes: observed=482245; runbook=482245; delta=0
Extended program capacity: observed=482200; runbook=482200; delta=0
Rent per byte lamports: observed=5080; runbook=5080; delta=0
Current rent minimum: observed=2398435640; runbook=2398435640; delta=0
Exact-fit rent minimum: observed=2400874040; runbook=2400874040; delta=0
Extended rent minimum: observed=2450454840; runbook=2450454840; delta=0
Buffer rent: observed=2400833400; runbook=2400833400; delta=0
Extend rent topup: observed=0; runbook=0; delta=0
Authority balance: observed=5400565851; runbook=5400565851; delta=0
Upgrade spill to fee payer (CLI v4.0.1 source): 3236424240 lamports
Net authority gain before fees: 835590840 lamports
Expected authority balance: balance + net gain - actual total fees
Expected balance before fees: 6.236156691 SOL
Expected balance using runbook 0.0025 SOL fee estimate: 6.233656691 SOL
Difference from runbook approximately 6.236 SOL: -0.002343309 SOL
Peak funding using runbook fee estimate: 2.403333400 SOL (runbook approximately 2.4034 SOL)
Actual total transaction fees are unmeasured: no on-chain transactions sent in pass 3.
Runbook difference: source precheck exits 1 because scripts/guard_deploy_artifact.sh was added after f34bfae; program source and build inputs match f34bfae.
Runbook difference: approximately 6.236 SOL is the pre-fee balance; approximately 6.233657 SOL follows its 0.0025 SOL fee estimate.

exit_code=0
````

````bash
python3 - <<'PY'
import json,copy,pathlib,hashlib
p=pathlib.Path(".cutover-pass3")
a=json.loads((p/"old/target/idl/plotarmor.json").read_text());b=json.loads((p/"head/target/idl/plotarmor.json").read_text());c=copy.deepcopy(b)
s=next(i for i in c["instructions"] if i["name"]=="sign_contract");added=s["accounts"].pop(0)
assert added["name"]=="registry_config" and not added.get("signer",False) and not added.get("writable",False)
assert c==a
print("PASS: entire IDL equals 09c5bfc after removing only sign_contract.accounts[0] from HEAD")
print("Added account:",json.dumps(added,sort_keys=True))
for label in ["old","head"]:
 for name in ["target/idl/plotarmor.json","Cargo.lock"]:
  f=p/label/name; print(f,hashlib.sha256(f.read_bytes()).hexdigest())
print("PASS: generated cold-build IDLs used for the comparison; separate cached HEAD IDL attempt failed before the cold build finished and was not used")
PY
````
````text
PASS: entire IDL equals 09c5bfc after removing only sign_contract.accounts[0] from HEAD
Added account: {"name": "registry_config", "pda": {"seeds": [{"kind": "const", "value": [99, 111, 110, 102, 105, 103]}]}}
.cutover-pass3/old/target/idl/plotarmor.json eaad0eae19e808befe7c4076038ad27ffb4bf809bee5fe0835c0177021b87516
.cutover-pass3/old/Cargo.lock 17ffb5f9f88ab1f9a6f8d52254817c14e42c0c81134a4eb40e43640fcdf7e97b
.cutover-pass3/head/target/idl/plotarmor.json ccf446e8427564fbf9a815c294d40039350ee1a46c0bedd4474960f1420bfa5a
.cutover-pass3/head/Cargo.lock 1944f68bcfce259ec18e9e44e909ac296fbad38d74b1f775da8992abc1a93dd9
PASS: generated cold-build IDLs used for the comparison; separate cached HEAD IDL attempt failed before the cold build finished and was not used

exit_code=0
````
