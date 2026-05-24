---
description: Initialize a Web3 dApp with React, Next.js, Wagmi, viem, and RainbowKit.
---

# Setup Web3 dApp Workflow

Use this workflow when the user requests a new Web3 frontend or wants to initialize a project using `/setup-web3-dapp`.

## Step 1: Initialize Project
Ask the user for the project name.
Run the initialization command. We prefer Next.js with the App Router.
1. `npx create-next-app@latest [project-name] --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"`

## Step 2: Install Web3 Dependencies
Navigate into the project directory.
1. `npm install wagmi viem @tanstack/react-query @rainbow-me/rainbowkit`

## Step 3: Configure Providers
1. Create a file `src/app/providers.tsx`.
2. Configure Wagmi and RainbowKit in this file. Include a basic configuration with `mainnet` and `sepolia` chains from `wagmi/chains`.
3. Wrap the children in `<WagmiProvider>`, `<QueryClientProvider>`, and `<RainbowKitProvider>`.

## Step 4: Update Root Layout
1. Open `src/app/layout.tsx`.
2. Import the newly created `Providers` component.
3. Wrap the `{children}` with the `<Providers>` component.
4. Add the RainbowKit CSS import at the top of the file: `import '@rainbow-me/rainbowkit/styles.css';`

## Step 5: Add Connect Button
1. Open `src/app/page.tsx`.
2. Delete the boilerplate Next.js content.
3. Add the `<ConnectButton />` from `@rainbow-me/rainbowkit` to test the integration.

Notify the user that the setup is complete and suggest starting the development server with `npm run dev`.
