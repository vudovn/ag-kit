---
description: Deploy smart contracts securely using Hardhat or Foundry to any EVM network.
---

# Deploy Smart Contract Workflow

This workflow ensures secure, consistent, and verified deployments of smart contracts on EVM chains.
When the user executes `/deploy-smart-contract`, follow these steps sequentially.

## Pre-Flight Checklist
1. **Tool Check**: Ask the user if they are using Hardhat or Foundry/Forge.
2. **Network Check**: Ask which network to deploy to (e.g., Ethereum Mainnet, Sepolia, Arbitrum).
3. **Environment**: Ensure `.env` is properly configured with a `PRIVATE_KEY` and the required `RPC_URL` or network config.

// turbo
## Compilation & Testing (MANDATORY)
1. If Hardhat: Execute `npx hardhat compile` and `npx hardhat test`.
2. If Foundry: Execute `forge build` and `forge test`.
3. If tests fail, STOP and notify the user to fix the errors before proceeding.

## Deployment Execution
1. If Hardhat: Ensure there is a deployment script in the `scripts/` or `ignition/` directory. Run `npx hardhat run [script_path] --network [network_name]`.
2. If Foundry: Use `forge script script/[script_name].s.sol:DeployScript --rpc-url [network_rpc] --broadcast`. 

## Verification
1. Ensure the block explorer API key (`ETHERSCAN_API_KEY`, etc.) is set in the `.env` file.
2. If Hardhat: Run `npx hardhat verify --network [network_name] [deployed_address] [constructor_arguments]`.
3. If Foundry: Append `--verify --etherscan-api-key [key]` to the deployment script command, or use `forge verify-contract [deployed_address] [contract_name] --chain [chain_id]`.
