The scratch directory was created by extracting `git -C /home/<usr>/plotarmor-program archive 7c267e9` via Python tarfile into the previously empty `/home/<usr>/plotarmor-demo/.m2-pass4-scratch` directory. The captured setup output was:

```
Extracted exact commit 7c267e9 into /home/<usr>/plotarmor-demo/.m2-pass4-scratch ; target exists: False
```

It resides on the workspace filesystem because /tmp has only 1.8 GB total capacity. No target tree was copied. The scripts in this bundle retain the actual scratch and log paths for traceability; recreate those paths (or adjust them consistently) to repeat the commands. `run.py` records UTC time, argv, cwd, combined stdout/stderr and exit status. The SBF artifact is the unmodified devnet cold build; no keypair files are included.

Initial read-only inspection found no applicable AGENTS.md files. Existing program HEAD was 7c2b54d; program changes since 7c267e9 consist only of the handler-order comment correction, plus documentation outside programs/. Existing evidence under the requested destination was left untouched and is not included in this run's commit.

The solana-dev skill was read from /home/<usr>/.agents/skills/solana-dev/SKILL.md. Its Solana MCP installation command was attempted twice but the executable could not launch (`Text file busy (os error 26)`). No MCP configuration was changed. Official Anchor documentation was accessed at https://www.anchor-lang.com/docs/references/account-constraints and https://www.anchor-lang.com/docs/references/account-types. Exact locked local dependency sources and runtime tests substantiate the audit.
