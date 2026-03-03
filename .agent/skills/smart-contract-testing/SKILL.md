---
name: smart-contract-testing
description: Testing methodologies for EVM smart contracts including unit, integration, and fuzz testing.
---

# Smart Contract Testing

In Web3, testing is not optional; it is the most critical phase before deployment.

## 1. The Pyramid of Web3 Testing
- **Unit Tests**: Test individual functions and modifiers in isolation. Ensure require/revert statements work properly.
- **Integration Tests**: Test how multiple contracts interact with each other.
- **Invariant Fuzz Testing**: Define properties of the system that must ALWAYS hold true (e.g., "The total supply of tokens must never exceed the max cap") and let a fuzzer (like Foundry's Forge) bombard the contract with random inputs.

## 2. Foundry / Forge Testing Practices
- **Setup State Properly**: Use a standard `setUp()` function to deploy contracts and set initial balances.
- **Cheatcodes (vm.prank & vm.expectRevert)**: Use `vm.prank(address)` to simulate calls from specific users securely. Use `vm.expectRevert` immediately before a failing call to assert the specific custom error or string.
- **Fuzz Testing**: Write test functions that accept arguments (e.g., `testTransfer(uint256 amount)`). Forge will automatically fuzz these arguments. Use `vm.assume(amount > 0 && amount < totalSupply)` to constrain fuzzing inputs.
- **Event Testing**: Use `vm.expectEmit` to ensure crucial events are being fired on state changes.

## 3. Hardhat / Chai Testing Practices
- **Fixtures**: Use `@nomicfoundation/hardhat-network-helpers` and `loadFixture` to snapshot the blockchain state. This makes tests run significantly faster.
- **Signers**: Retrieve signers with `ethers.getSigners()` to represent different roles (owner, attacker, user).
- **Match Reverts**: Use `await expect(tx).to.be.revertedWithCustomError(...)`.
- **Time Manipulation**: Use `time.increase()` and `time.latest()` from Hardhat network helpers to test time-dependent logic (e.g., vesting or timelocks).

## 4. Coverage & Auditing
- Enforce **100% Branch Coverage**.
- Use `forge coverage` or `hardhat coverage`. Every uncovered line is an exploit waiting to happen.
- Use static analysis tools like `slither` before merging PRs.
