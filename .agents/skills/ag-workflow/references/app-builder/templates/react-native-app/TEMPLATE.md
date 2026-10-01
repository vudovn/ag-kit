---
name: react-native-app
description: React Native mobile app template principles. Expo, TypeScript, navigation.
---

# React Native App Template (2026 Edition)

> Modern mobile app, optimized for New Architecture and React 19. Versions reflect the latest stable line verified 2026-05; NativeWind v5 is pre-release — pin deliberately when scaffolding.

## Tech Stack

| Component | Technology | Version / Notes |
|-----------|------------|-----------------|
| Core | React Native + Expo | SDK 56+ (New Architecture Enabled) |
| Language | TypeScript | v5+ (Strict Mode) |
| UI Logic | React | v19 (React Compiler, auto-memoization) |
| Navigation | Expo Router | File-based, Universal Links |
| Styling | NativeWind | v5 (pre-release, Tailwind v4 CSS-first) |
| State | Zustand + React Query | v5+ (Async State Management) |
| Storage | Expo SecureStore | Encrypted local storage |

---

## Directory Structure

Expo Router keeps `app/` for routes only; everything else lives under `src/` with the `@/*` alias.

```
project-name/
├── src/
│   ├── app/             # Expo Router (file-based routing ONLY)
│   │   ├── _layout.tsx  # Root Layout (Stack/Tabs config)
│   │   ├── index.tsx    # Main Screen
│   │   ├── (tabs)/      # Route Group for Tab Bar
│   │   │   ├── _layout.tsx
│   │   │   ├── home.tsx
│   │   │   └── profile.tsx
│   │   ├── +not-found.tsx
│   │   └── [id].tsx     # Dynamic Route (Typed)
│   ├── components/
│   │   ├── ui/          # Primitive Components (Button, Text)
│   │   └── features/    # Complex Components
│   ├── hooks/           # Custom Hooks
│   ├── lib/
│   │   ├── api.ts       # Axios/Fetch client
│   │   └── storage.ts   # SecureStore wrapper
│   ├── store/           # Zustand stores
│   └── constants/       # Colors, Theme config
├── assets/              # Fonts, Images
├── global.css           # NativeWind v5 entry: @import "tailwindcss"
├── babel.config.js      # NativeWind Babel preset
├── metro.config.js      # withNativeWind wrapper
└── app.json             # Expo Config
```

---

## Navigation Patterns (Expo Router)

| Pattern | Description | Implement |
|---------|-------------|-----------|
| Stack | Hierarchical navigation (Push/Pop) | `<Stack />` in `_layout.tsx` |
| Tabs | Bottom navigation bar | `<Tabs />` in `(tabs)/_layout.tsx` |
| Drawer | Side slide-out menu | `expo-router/drawer` |
| Modals | Overlay screens | `presentation: 'modal'` in Stack screen |

---

## Key Packages & Purpose

| Package | Purpose |
|---------|---------|
| expo-router | File-based routing (Next.js like) |
| nativewind | Use Tailwind CSS classes in React Native |
| react-native-reanimated | Smooth animations (runs on UI thread) |
| @tanstack/react-query | Server state management, caching, pre-fetching |
| zustand | Global state management (lighter than Redux) |
| expo-image | Optimized image rendering for performance |

---

## Setup Steps (2026 Standard)

1. Initialize Project:
   ```bash
   npx create-expo-app@latest my-app --template default
   cd my-app
   ```

2. Install Core Dependencies:
   ```bash
   npx expo install expo-router react-native-safe-area-context react-native-screens expo-link expo-constants expo-status-bar
   ```

3. Install NativeWind v5 (pre-release, Tailwind v4 CSS-first):
   ```bash
   npm install nativewind@next tailwindcss react-native-reanimated
   ```

4. Configure NativeWind (Babel, Metro & CSS):
   - Add the preset to `babel.config.js`: `presets: [["babel-preset-expo", { jsxImportSource: "nativewind" }], "nativewind/babel"]`.
   - Wrap Metro: `withNativeWind(config, { input: './global.css' })` in `metro.config.js`.
   - Create `global.css` with `@import "tailwindcss";` (theme via `@theme`, no `tailwind.config.js`).
   - Import `global.css` in `src/app/_layout.tsx`.

5. Run Project:
   ```bash
   npx expo start -c
   # Press 'i' for iOS simulator or 'a' for Android emulator
   ```

---

## Best Practices (Updated)

- **New Architecture**: Ensure `newArchEnabled: true` in `app.json` to leverage TurboModules and Fabric Renderer.
- **Typed Routes**: Use Expo Router's "Typed Routes" feature for type-safe routing (e.g., `router.push('/path')`).
- **React 19**: Reduce usage of `useMemo` or `useCallback` thanks to React Compiler (if enabled).
- **Components**: Build UI primitives (Box, Text) with NativeWind className for reusability.
- **Assets**: Use `expo-image` instead of default `<Image />` for better caching and performance.
- **API**: Always wrap API calls with TanStack Query, avoid direct calls in `useEffect`.
