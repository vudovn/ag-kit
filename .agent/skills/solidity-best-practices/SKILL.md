---
name: solidity-best-practices
description: Core principles for secure, gas-efficient Solidity development.
---

# Solidity Best Practices

You follow stringent rules for smart contract development in Solidity.

## 1. Security First
- **Checks-Effects-Interactions (CEI)**: Always implement the CEI pattern to prevent reentrancy attacks.
- **ReentrancyGuard**: Use OpenZeppelin's `nonReentrant` modifier for state-changing external functions that call other contracts.
- **Access Control**: Clearly define `onlyOwner` or generic role-based access control. Do not leave sensitive functions unprotected.
- **No `tx.origin`**: Never use `tx.origin` for authorization; use `msg.sender`.
- **Safe Math**: Avoid integer overflow/underflow. Rely on Solidity ^0.8.0 built-in checks, but be aware of unchecked blocks for gas optimization where safe.

## 2. Gas Optimization (The Modern Way)
- **Custom Errors**: Use `error InvalidAmount();` instead of `require(..., "Invalid Amount");` to save deployment and runtime gas.
- **Storage vs Memory vs Transient**: Cache storage variables in memory when reading them multiple times. Use `transient` storage (`TSTORE`/`TLOAD`, EIP-1153) for data that only needs to persist for the duration of a single transaction (e.g., reentrancy locks, calculate-and-forward patterns).
- **Calldata**: Use `calldata` instead of `memory` for reference types in external function arguments.
- **Packing Variables**: Group variables of reduced sizes (like `uint128`, `uint64`) next to each other in storage to pack them into a single 256-bit slot.
- **Immutable & Constant**: Use `immutable` for variables set in the constructor and never changed. Use `constant` for fixed values.

## 3. Architecture & Standards
- **OpenZeppelin Standard**: Inherit extensively from OZ libraries (ERC20, ERC721, ERC1155, AccessControl, Pausable).
- **NatSpec**: Document ALL public/external functions, variables, and custom errors using the `@title`, `@author`, `@notice`, `@dev`, and `@param` tags.
- **Events**: Emit events for *all* critical state changes.
- **Upgradability**: If required, use UUPS or Transparent Proxies securely. Prefer immutable contracts wherever possible.

## 4. Code Style
- **Naming**: `CamelCase` for contracts, `camelCase` for functions/variables, `UPPER_CASE_WITH_UNDERSCORES` for constants.
- **Modifers**: Keep modifiers simple. Avoid heavy state changes inside them.
- **Layout**: Follow standard layout constraints: State variables, events, errors, modifiers, constructor, functions (external, public, internal, private).
