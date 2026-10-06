#!/usr/bin/env bash
# Refuse to continue unless the program artifact is exactly the audited build.
#
# Compares the sha256 of the .so with trailing zero bytes stripped (the on-chain program
# buffer is zero padded, so only the trimmed hash is comparable across a dump and a build)
# against the hash recorded in docs/CUTOVER_2026-10.md for commit f34bfae built with
# platform-tools v1.52 via scripts/build.sh --anchor.
#
# usage: scripts/guard_deploy_artifact.sh [path-to-so]   (default target/deploy/plotarmor.so)
# exit 0 on match, exit 1 on mismatch or a missing file. Chain the deploy after it with &&.
# Needs python3. Update EXPECT only together with a new audited build and runbook.
set -u
EXPECT="bcea64bb938e94abf423ff0b5d286069e28e3835660fcb077e8d40996573c4f2"
SO="${1:-target/deploy/plotarmor.so}"

if [ ! -f "$SO" ]; then
  echo "REFUSING: $SO does not exist. Build it first: scripts/build.sh --anchor" >&2
  exit 1
fi

GOT="$(python3 -I -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read().rstrip(b"\0")).hexdigest())' "$SO")" || exit 1

if [ "$GOT" = "$EXPECT" ]; then
  echo "artifact OK: $SO trimmed sha256 $GOT"
  exit 0
fi

echo "REFUSING: $SO trimmed sha256 is $GOT" >&2
echo "          expected                $EXPECT" >&2
exit 1
