# Redaction record, 2026-10-11

## What changed

The local operating-system username of the machine that produced these logs was replaced
with the placeholder `<usr>` in every tracked text file. It appeared as `/home/<user>/...`
paths, `-home-<user>-...` session scratch paths, and the owner/group columns of `ls -l`
output. 55 files were touched, 558 lines changed. Nothing else was altered.

The placeholder has the same length as the original name (5 bytes), so every file kept its
exact byte size and every line number and byte offset quoted elsewhere still holds.

## Why

The username is not a credential, but it identifies the operator's machine and has no
evidentiary value. It was removed ahead of the repository being shared outside the team.

## Effect on SHA256SUMS

52 of the files covered by the three manifests changed, so their hashes changed:

| manifest | entries | changed |
|---|---|---|
| `2026-09-30-m2-pass4/SHA256SUMS` | 27 | 16 |
| `2026-09-30-m2-pass4/independent-run/SHA256SUMS` | 34 | 30 |
| `2026-09-30-security-txt/SHA256SUMS` | 10 | 6 |

Each `SHA256SUMS` now describes the redacted files. The manifest as it stood before the
redaction is kept next to it as `SHA256SUMS.pre-redaction`. Those original hashes verify
against the unredacted files at commit `6fc19bf`, which remains in git history unchanged:

```
git worktree add /tmp/pre-redaction 6fc19bf
cd /tmp/pre-redaction/evidence/2026-09-30-m2-pass4 && sha256sum -c SHA256SUMS
```

The committed binary `2026-09-30-m2-pass4/independent-run/plotarmor-7c267e9.so` did not
contain the username and is byte-identical; its hash entry is unchanged.

## How the redaction was checked

- Reverse check: substituting `<usr>` back to the original name reproduces every touched
  file byte-for-byte as it is at `6fc19bf`. `<usr>` did not occur anywhere before the
  redaction, so the substitution is unambiguous.
- No hash of any touched file is quoted anywhere in the repository outside the three
  `SHA256SUMS` files (searched by full hash and by 16-character prefix).
- All three regenerated manifests pass `sha256sum -c`.

Git history was NOT rewritten. The original username is still readable in commits up to
and including `6fc19bf`. Removing it from history would change the hash of every commit
from 2026-07-15 onward, including commits cited as evidence (`7c267e9`, `bc729e9`,
`14815bb`, `f34bfae`), and would break those references.
