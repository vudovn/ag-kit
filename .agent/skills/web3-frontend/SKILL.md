---
name: web3-frontend
description: Building modern Web3 frontends with React, Wagmi, viem, and RainbowKit.
---

# Web3 Frontend Architecture

You build intuitive, responsive, and robust Web3 decentralized applications (dApps).

## 1. Core Stack
- **RainbowKit / ConnectKit**: Used for wallet connection UI. It provides a polished out-of-the-box experience for connecting various wallets (MetaMask, WalletConnect, Coinbase Wallet, etc.).
- **Wagmi (v2+)**: Use Wagmi React Hooks for interacting with Ethereum. Wagmi v2+ requires `createConfig` instead of `configureChains` and imports ABIs and chains directly from `viem` & `@wagmi/core/chains`.
- **viem**: The low-level TypeScript interface for Ethereum. It replaces Ethers.js and web3.js with a smaller bundle size and better TypeScript support. ABIs and standard parsing utilities are imported directly from `viem`.

## 2. Wallet Connection & State
- Always check if the user is `isConnected` and on the correct `chainId` before allowing transaction submissions.
- Provide clear error messaging if a user is on an unsupported network. Use Wagmi's `useSwitchChain` to prompt them to change networks.

## 3. Reading from Contracts
- Use `useReadContract` for single calls.
- Use `useReadContracts` (multicall) when fetching multiple pieces of independent data to reduce RPC load.
- Properly handle `isLoading`, `isError`, and `data` states. Show skeletons or spinners during loading.

## 4. Writing to Contracts
- **Simulation First**: Use `useSimulateContract` before executing a transaction. This catches reverts before the wallet popup appears, saving the user gas and frustration.
- **Execution**: Pass the simulated request to `useWriteContract`.
- **Waiting for Receipts**: Use `useWaitForTransactionReceipt` to track the transaction status (pending, success, error) and show toast notifications (e.g., Sonner).

## 5. Providers & RPCs
- Do not rely solely on public RPCs in production. Configure Alchemy, Infura, or QuickNode transports in the Wagmi config.
- Implement fallback RPCs to ensure the dApp remains functional during outages.
