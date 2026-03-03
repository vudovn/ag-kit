---
name: evm-tooling
description: Principles and patterns for EVM tooling, primarily Hardhat and Foundry.
---

# EVM Tooling

You use industry-standard tools for EVM smart contract development.

## 1. Environment Choice
- **Foundry / Forge**: Preferred for blazing-fast compilation, Solidity-native testing, and fuzzing capabilities. Use when the primary focus is smart contract security, complex invariant testing, or gas optimization.
- **Hardhat**: Preferred when extensive TypeScript integrations are required, interacting heavily with JS/TS specific plugins, or when the team prefers JavaScript/TypeScript for their testing suite and deployment scripts.

## 2. Hardhat Principles
- **TypeScript First**: Always use TypeScript for configurations (`hardhat.config.ts`), tests, and deployment scripts.
- **Environment Variables**: Use `dotenv` for private keys and RPC URLs. Never hardcode them.
- **TypeChain**: Always use TypeChain to generate strict typings for smart contracts in your tests.

## 3. Foundry Principles
- **Dependencies**: Use `forge install libs/openzeppelin-contracts` for dependencies and manage them cleanly via `.gitmodules`.
- **Profiles**: Utilize `foundry.toml` to configure profiles for standard development and optimized CI runs.
- **Scripting**: Use Solidity-based scripts (`forge script`) instead of Bash or JS for deployments to ensure consistency. Use `--broadcast` and `--verify` for production deployments.

## 4. Verification & Linting
- Always configure Etherscan (or equivalent block explorers like Arbiscan, Basescan) API keys for automatic contract verification.
- Always run `solhint` or `aderyn` or `forge fmt` formats before committing.
