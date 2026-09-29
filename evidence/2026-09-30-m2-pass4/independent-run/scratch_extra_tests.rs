
// ===== PASS-4 SCRATCH TESTS (appended to a SCRATCH COPY of sign_contract_tests.rs only;
// never committed into programs/). Purpose: empirical proof for check 1, that no
// substitute RegistryConfig can be passed to sign_contract, and for check 2, that the
// paused check fires before the content_hash check.

fn pass4_sign_ix_with_config(
    registry_config: Pubkey,
    contract_artifact: Pubkey,
    signer: &Keypair,
    content_hash: [u8; 32],
) -> (Instruction, Pubkey) {
    let contract_signature = Pubkey::find_program_address(
        &[b"signature", contract_artifact.as_ref(), signer.pubkey().as_ref()],
        &plotarmor::ID,
    )
    .0;
    let instruction = Instruction::new_with_bytes(
        plotarmor::ID,
        &plotarmor::instruction::SignContract { content_hash }.data(),
        plotarmor::accounts::SignContract {
            registry_config,
            contract_artifact,
            contract_signature,
            signer: signer.pubkey(),
            system_program: system_program::ID,
        }
        .to_account_metas(None),
    );
    (instruction, contract_signature)
}

fn pass4_fixture() -> (common::TestContext, Pubkey, Pubkey, [u8; 32]) {
    let mut context = setup();
    let registry_config = initialize_registry(&mut context.svm, &context.authority);
    let raw = [91u8; 32];
    let artifact =
        create_contract_artifact(&mut context.svm, registry_config, &context.authority, raw, [92; 32]);
    (context, registry_config, artifact, raw)
}

fn pass4_assert_code(error: &litesvm::types::FailedTransactionMetadata, name: &str, code: u32) {
    let logs = error.meta.logs.join("\n");
    assert!(
        format!("{:?}", error.err).contains(&format!("Custom({code})")),
        "expected {name} {code}, got {:?}\n{logs}",
        error.err
    );
    assert!(logs.contains(name), "expected {name} in logs:\n{logs}");
    println!("PASS4 observed {name} ({code}) err={:?}", error.err);
}

// A program-owned account with VALID RegistryConfig bytes (paused = false) at a
// non-PDA address. Must be rejected by the seeds constraint.
#[test]
fn pass4_fake_config_wrong_address_rejected() {
    let (mut context, registry_config, artifact, raw) = pass4_fixture();
    let real = context.svm.get_account(&registry_config).unwrap();
    let fake = Pubkey::new_unique();
    context.svm.set_account(fake, real.clone()).unwrap();
    assert_eq!(context.svm.get_account(&fake).unwrap().owner, plotarmor::ID);
    let (ix, sig) = pass4_sign_ix_with_config(fake, artifact, &context.authority, raw);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority)
        .expect_err("fake config at non-PDA address must be rejected");
    pass4_assert_code(&err, "ConstraintSeeds", 2006);
    assert!(context.svm.get_account(&sig).is_none());
}

// The real PDA address, but owned by the System Program. Must be rejected by
// Account<T>'s owner check.
#[test]
fn pass4_config_wrong_owner_rejected() {
    let (mut context, registry_config, artifact, raw) = pass4_fixture();
    let mut acct = context.svm.get_account(&registry_config).unwrap();
    acct.owner = system_program::ID;
    context.svm.set_account(registry_config, acct).unwrap();
    let (ix, sig) = pass4_sign_ix_with_config(registry_config, artifact, &context.authority, raw);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority)
        .expect_err("wrong-owner config must be rejected");
    pass4_assert_code(&err, "AccountOwnedByWrongProgram", 3007);
    assert!(context.svm.get_account(&sig).is_none());
}

// The real PDA address, program-owned, but a different account type's
// discriminator. Must be rejected by Account<T>'s discriminator check.
#[test]
fn pass4_config_wrong_discriminator_rejected() {
    let (mut context, registry_config, artifact, raw) = pass4_fixture();
    let mut acct = context.svm.get_account(&registry_config).unwrap();
    let art = context.svm.get_account(&artifact).unwrap();
    acct.data[..8].copy_from_slice(&art.data[..8]); // ContractArtifact discriminator
    context.svm.set_account(registry_config, acct).unwrap();
    let (ix, sig) = pass4_sign_ix_with_config(registry_config, artifact, &context.authority, raw);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority)
        .expect_err("wrong-discriminator config must be rejected");
    pass4_assert_code(&err, "AccountDiscriminatorMismatch", 3002);
    assert!(context.svm.get_account(&sig).is_none());
}

// Passing a DIFFERENT real program account (the ContractArtifact itself) in the
// registry_config slot. Wrong address and wrong discriminator.
#[test]
fn pass4_other_program_account_as_config_rejected() {
    let (mut context, _registry_config, artifact, raw) = pass4_fixture();
    let (ix, sig) = pass4_sign_ix_with_config(artifact, artifact, &context.authority, raw);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority)
        .expect_err("ContractArtifact in config slot must be rejected");
    pass4_assert_code(&err, "AccountDiscriminatorMismatch", 3002);
    assert!(context.svm.get_account(&sig).is_none());
}

// Config account missing entirely (PDA address, no data, system-owned).
#[test]
fn pass4_config_missing_rejected() {
    let (mut context, registry_config, artifact, raw) = pass4_fixture();
    let mut empty = context.svm.get_account(&registry_config).unwrap();
    empty.lamports = 0;
    empty.data = vec![];
    empty.owner = system_program::ID;
    context.svm.set_account(registry_config, empty).unwrap();
    let (ix, sig) = pass4_sign_ix_with_config(registry_config, artifact, &context.authority, raw);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority)
        .expect_err("missing config must be rejected");
    pass4_assert_code(&err, "AccountNotInitialized", 3012);
    assert!(context.svm.get_account(&sig).is_none());
}

// Ordering: paused AND wrong content_hash. Paused must win, proving the paused
// check runs before the ContentHashMismatch check.
#[test]
fn pass4_paused_checked_before_content_hash() {
    use anchor_lang::AccountSerialize;
    let (mut context, registry_config, artifact, _raw) = pass4_fixture();
    let mut config: RegistryConfig = read_account(&context.svm, &registry_config);
    config.paused = true;
    let mut acct = context.svm.get_account(&registry_config).unwrap();
    config.try_serialize(&mut acct.data.as_mut_slice()).unwrap();
    context.svm.set_account(registry_config, acct).unwrap();
    let (ix, sig) =
        pass4_sign_ix_with_config(registry_config, artifact, &context.authority, [0xEE; 32]);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority)
        .expect_err("paused must reject");
    pass4_assert_code(&err, "Paused", 6008);
    assert!(context.svm.get_account(&sig).is_none());
}

#[test]
fn pass4_noncanonical_bump_rejected() {
    let (mut context, registry_config, artifact, raw) = pass4_fixture();
    let canonical = Pubkey::find_program_address(&[b"config"], &plotarmor::ID).1;
    let alternate = (0..canonical).rev().find_map(|bump| {
        Pubkey::create_program_address(&[b"config", &[bump]], &plotarmor::ID).ok()
    }).expect("another valid off-curve PDA");
    let real = context.svm.get_account(&registry_config).unwrap();
    context.svm.set_account(alternate, real).unwrap();
    let (ix, sig) = pass4_sign_ix_with_config(alternate, artifact, &context.authority, raw);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority).expect_err("noncanonical bump");
    pass4_assert_code(&err, "ConstraintSeeds", 2006);
    assert!(context.svm.get_account(&sig).is_none());
}

#[test]
fn pass4_old_four_account_layout_rejected() {
    let (mut context, _registry_config, artifact, raw) = pass4_fixture();
    let (mut ix, sig) = sign_contract_instruction(artifact, &context.authority, raw);
    ix.accounts.remove(0);
    let err = send_instruction_result(&mut context.svm, ix, &context.authority).expect_err("old layout cannot work");
    println!("PASS4 old four-account layout: {:?}\n{}", err.err, err.meta.logs.join("\n"));
    assert!(context.svm.get_account(&sig).is_none());
}
