---
name: mobile-design
description: Mobile-first design thinking and decision-making for iOS and Android apps. Touch interaction, performance patterns, platform conventions. Teaches principles, not fixed values. Use when building React Native, Flutter, or native mobile apps.
when_to_use: "When designing mobile app interfaces for iOS/Android, React Native, or Flutter. Touch interaction and platform conventions. NOT for web apps."
allowed-tools: Read, Glob, Grep, Bash
---

# Mobile Design System

> **Philosophy:** Touch-first. Battery-conscious. Platform-respectful. Offline-capable.
> **Core Principle:** Mobile is NOT a small desktop. THINK mobile constraints, ASK platform choice.

---

## 🔧 Runtime Scripts

**Execute these for validation (don't read, just run):**

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/mobile_audit.py` | Mobile UX & Touch Audit | `python scripts/mobile_audit.py <project_path>` |

---

## 🔴 MANDATORY: Read Reference Files Before Working!

**⛔ DO NOT start development until you read the relevant files:**

### Universal (Always Read)

| File | Content | Status |
|------|---------|--------|
| **[mobile-design-thinking.md](mobile-design-thinking.md)** | **⚠️ ANTI-MEMORIZATION: Forces thinking, prevents AI defaults** | **⬜ CRITICAL FIRST** |
| **[touch-psychology.md](touch-psychology.md)** | **Fitts' Law, gestures, haptics, thumb zone** | **⬜ CRITICAL** |
| **[mobile-performance.md](mobile-performance.md)** | **RN/Flutter performance, 60fps, memory** | **⬜ CRITICAL** |
| **[mobile-backend.md](mobile-backend.md)** | **Push notifications, offline sync, mobile API** | **⬜ CRITICAL** |
| **[mobile-testing.md](mobile-testing.md)** | **Testing pyramid, E2E, platform-specific** | **⬜ CRITICAL** |
| **[mobile-debugging.md](mobile-debugging.md)** | **Native vs JS debugging, Flipper, Logcat** | **⬜ CRITICAL** |
| [mobile-navigation.md](mobile-navigation.md) | Tab/Stack/Drawer, deep linking | ⬜ Read |
| [mobile-typography.md](mobile-typography.md) | System fonts, Dynamic Type, a11y | ⬜ Read |
| [mobile-color-system.md](mobile-color-system.md) | OLED, dark mode, battery-aware | ⬜ Read |
| [decision-trees.md](decision-trees.md) | Framework/state/storage selection | ⬜ Read |

> 🧠 **mobile-design-thinking.md is PRIORITY!** This file ensures AI thinks instead of using memorized patterns.

### Platform-Specific (Read Based on Target)

| Platform | File | Content | When to Read |
|----------|------|---------|--------------|
| **iOS** | [platform-ios.md](platform-ios.md) | Human Interface Guidelines, SF Pro, SwiftUI patterns | Building for iPhone/iPad |
| **Android** | [platform-android.md](platform-android.md) | Material Design 3, Roboto, Compose patterns | Building for Android |
| **Cross-Platform** | Both above | Platform divergence points | React Native / Flutter |

> 🔴 **If building for iOS → Read platform-ios.md FIRST!**
> 🔴 **If building for Android → Read platform-android.md FIRST!**
> 🔴 **If cross-platform → Read BOTH and apply conditional platform logic!**

---

## ⚠️ CRITICAL: ASK BEFORE ASSUMING (MANDATORY)

> **STOP! If the user's request is open-ended, DO NOT default to your favorites.**

### You MUST Ask If Not Specified:

| Aspect | Ask | Why |
|--------|-----|-----|
| **Platform** | "iOS, Android, or both?" | Affects EVERY design decision |
| **Framework** | "React Native, Flutter, or native?" | Determines patterns and tools |
| **Navigation** | "Tab bar, drawer, or stack-based?" | Core UX decision |
| **State** | "What state management? (Zustand/Redux/Riverpod/BLoC?)" | Architecture foundation |
| **Offline** | "Does this need to work offline?" | Affects data strategy |
| **Target devices** | "Phone only, or tablet support?" | Layout complexity |

### ⛔ AI MOBILE ANTI-PATTERNS (YASAK LİSTESİ)

> 🚫 **These are AI default tendencies that MUST be avoided!**

#### Performance Sins

| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **ScrollView for long lists** | Renders ALL items, memory explodes | Use `FlatList` / `FlashList` / `ListView.builder` |
| **Inline renderItem function** | New function every render, all items re-render | `useCallback` + `React.memo` |
| **Missing keyExtractor** | Index-based keys cause bugs on reorder | Unique, stable ID from data |
| **Skip getItemLayout** | Async layout = janky scroll | Provide when items have fixed height |
| **setState() everywhere** | Unnecessary widget rebuilds | Targeted state, `const` constructors |
| **Native driver: false** | Animations blocked by JS thread | `useNativeDriver: true` always |
| **console.log in production** | Blocks JS thread severely | Remove before release build |
| **Skip React.memo/const** | Every item re-renders on any change | Memoize list items ALWAYS |

#### Touch/UX Sins

| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **Touch target < 44px** | Impossible to tap accurately, frustrating | Minimum 44pt (iOS) / 48dp (Android) |
| **Spacing < 8px between targets** | Accidental taps on neighbors | Minimum 8-12px gap |
| **Gesture-only interactions** | Motor impaired users excluded | Always provide button alternative |
| **No loading state** | User thinks app crashed | ALWAYS show loading feedback |
| **No error state** | User stuck, no recovery path | Show error with retry option |
| **No offline handling** | Crash/block when network lost | Graceful degradation, cached data |
| **Ignore platform conventions** | Users confused, muscle memory broken | iOS feels iOS, Android feels Android |

#### Security Sins

| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **Token in AsyncStorage** | Easily accessible, stolen on rooted device | `SecureStore` / `Keychain` / `EncryptedSharedPreferences` |
| **Hardcode API keys** | Reverse engineered from APK/IPA | Environment variables, secure storage |
| **Skip SSL pinning** | MITM attacks possible | Pin certificates in production |
| **Log sensitive data** | Logs can be extracted | Never log tokens, passwords, PII |

#### Architecture Sins

| ❌ NEVER DO | Why It's Wrong | ✅ ALWAYS DO |
|-------------|----------------|--------------|
| **Business logic in UI** | Untestable, unmaintainable | Service layer separation |
| **Global state for everything** | Unnecessary re-renders, complexity | Local state default, lift when needed |
| **Deep linking as afterthought** | Notifications, shares broken | Plan deep links from day one |
| **Skip dispose/cleanup** | Memory leaks, zombie listeners | Clean up subscriptions, timers |

---

## 📱 Platform Decision Matrix

### When to Unify vs Diverge

```
                    UNIFY (same on both)          DIVERGE (platform-specific)
                    ───────────────────           ──────────────────────────
Business Logic      ✅ Always                     -
Data Layer          ✅ Always                     -
Core Features       ✅ Always                     -
                    
Navigation          -                             ✅ iOS: edge swipe, Android: back button
Gestures            -                             ✅ Platform-native feel
Icons               -                             ✅ SF Symbols vs Material Icons
Date Pickers        -                             ✅ Native pickers feel right
Modals/Sheets       -                             ✅ iOS: bottom sheet vs Android: dialog
Typography          -                             ✅ SF Pro vs Roboto (or custom)
Error Dialogs       -                             ✅ Platform conventions for alerts
```

### Quick Reference: Platform Defaults

| Element | iOS | Android |
|---------|-----|---------|
| **Primary Font** | SF Pro / SF Compact | Roboto |
| **Min Touch Target** | 44pt × 44pt | 48dp × 48dp |
| **Back Navigation** | Edge swipe left | System back button/gesture |
| **Bottom Tab Icons** | SF Symbols | Material Symbols |
| **Action Sheet** | UIActionSheet from bottom | Bottom Sheet / Dialog |
| **Progress** | Spinner | Linear progress (Material) |
| **Pull to Refresh** | Native UIRefreshControl | SwipeRefreshLayout |

---

## 🧠 Mobile UX Psychology (Quick Reference)

### Fitts' Law for Touch

```
Desktop: Cursor is precise (1px)
Mobile:  Finger is imprecise (~7mm contact area)

→ Touch targets MUST be 44-48px minimum
→ Important actions in THUMB ZONE (bottom of screen)
→ Destructive actions AWAY from easy reach
```

### Thumb Zone (One-Handed Usage)

```
┌─────────────────────────────┐
│      HARD TO REACH          │ ← Navigation, menu, back
│        (stretch)            │
├─────────────────────────────┤
│      OK TO REACH            │ ← Secondary actions
│       (natural)             │
├─────────────────────────────┤
│      EASY TO REACH          │ ← PRIMARY CTAs, tab bar
│    (thumb's natural arc)    │ ← Main content interaction
└─────────────────────────────┘
        [  HOME  ]
```

### Mobile-Specific Cognitive Load

| Desktop | Mobile Difference |
|---------|-------------------|
| Multiple windows | ONE task at a time |
| Keyboard shortcuts | Touch gestures |
| Hover states | NO hover (tap or nothing) |
| Large viewport | Limited space, scroll vertical |
| Stable attention | Interrupted constantly |

For deep dive: [touch-psychology.md](touch-psychology.md)

---

## ⚡ Performance Principles (Quick Reference)

### React Native Critical Rules

```typescript
// ✅ CORRECT: Memoized renderItem + React.memo wrapper
const ListItem = React.memo(({ item }: { item: Item }) => (
  <View style={styles.item}>
    <Text>{item.title}</Text>
  </View>
));

const renderItem = useCallback(
  ({ item }: { item: Item }) => <ListItem item={item} />,
  []
);

// ✅ CORRECT: FlatList with all optimizations
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}  // Stable ID, NOT index
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
/>
```

### Flutter Critical Rules

```dart
// ✅ CORRECT: const constructors prevent rebuilds
class MyWidget extends StatelessWidget {
  const MyWidget({super.key}); // CONST!

  @override
  Widget build(BuildContext context) {
    return const Column( // CONST!
      children: [
        Text('Static content'),
        MyConstantWidget(),
      ],
    );
  }
}

// ✅ CORRECT: Targeted state with ValueListenableBuilder
ValueListenableBuilder<int>(
  valueListenable: counter,
  builder: (context, value, child) => Text('$value'),
  child: const ExpensiveWidget(), // Won't rebuild!
)
```

### Animation Performance

```
GPU-accelerated (FAST):     CPU-bound (SLOW):
├── transform               ├── width, height
├── opacity                 ├── top, left, right, bottom
└── (use these ONLY)        ├── margin, padding
                            └── (AVOID animating these)
```

For complete guide: [mobile-performance.md](mobile-performance.md)

---

## 📝 CHECKPOINT (MANDATORY Before Any Mobile Work)

> **Before writing ANY mobile code, you MUST complete this checkpoint:**

```
🧠 CHECKPOINT:

Platform:   [ iOS / Android / Both ]
Framework:  [ React Native / Flutter / SwiftUI / Kotlin ]
Files Read: [ List the skill files you've read ]

3 Principles I Will Apply:
1. _______________
2. _______________
3. _______________

Anti-Patterns I Will Avoid:
1. _______________
2. _______________
```

**Example:**
```
🧠 CHECKPOINT:

Platform:   iOS + Android (Cross-platform)
Framework:  React Native + Expo
Files Read: touch-psychology.md, mobile-performance.md, platform-ios.md, platform-android.md

3 Principles I Will Apply:
1. FlatList with React.memo + useCallback for all lists
2. 48px touch targets, thumb zone for primary CTAs
3. Platform-specific navigation (edge swipe iOS, back button Android)

Anti-Patterns I Will Avoid:
1. ScrollView for lists → FlatList
2. Inline renderItem → Memoized
3. AsyncStorage for tokens → SecureStore
```

> 🔴 **Can't fill the checkpoint? → GO BACK AND READ THE SKILL FILES.**

---

## 🔧 Framework Decision Tree

```
WHAT ARE YOU BUILDING?
        │
        ├── Need OTA updates + rapid iteration + web team
        │   └── ✅ React Native + Expo
        │
        ├── Need pixel-perfect custom UI + performance critical
        │   └── ✅ Flutter
        │
        ├── Deep native features + single platform focus
        │   ├── iOS only → SwiftUI
        │   └── Android only → Kotlin + Jetpack Compose
        │
        ├── Existing RN codebase + new features
        │   └── ✅ React Native (bare workflow)
        │
        └── Enterprise + existing Flutter codebase
            └── ✅ Flutter
```

For complete decision trees: [decision-trees.md](decision-trees.md)

---

## 📋 Pre-Development Checklist

### Before Starting ANY Mobile Project

- [ ] **Platform confirmed?** (iOS / Android / Both)
- [ ] **Framework chosen?** (RN / Flutter / Native)
- [ ] **Navigation pattern decided?** (Tabs / Stack / Drawer)
- [ ] **State management selected?** (Zustand / Redux / Riverpod / BLoC)
- [ ] **Offline requirements known?**
- [ ] **Deep linking planned from day one?**
- [ ] **Target devices defined?** (Phone / Tablet / Both)

### Before Every Screen

- [ ] **Touch targets ≥ 44-48px?**
- [ ] **Primary CTA in thumb zone?**
- [ ] **Loading state exists?**
- [ ] **Error state with retry exists?**
- [ ] **Offline handling considered?**
- [ ] **Platform conventions followed?**

### Before Release

- [ ] **console.log removed?**
- [ ] **SecureStore for sensitive data?**
- [ ] **SSL pinning enabled?**
- [ ] **Lists optimized (memo, keyExtractor)?**
- [ ] **Memory cleanup on unmount?**
- [ ] **Tested on low-end devices?**
- [ ] **Accessibility labels on all interactive elements?**

---

## 📚 Reference Files

For deeper guidance on specific areas:

| File | When to Use |
|------|-------------|
| [mobile-design-thinking.md](mobile-design-thinking.md) | **FIRST! Anti-memorization, forces context-based thinking** |
| [touch-psychology.md](touch-psychology.md) | Understanding touch interaction, Fitts' Law, gesture design |
| [mobile-performance.md](mobile-performance.md) | Optimizing RN/Flutter, 60fps, memory/battery |
| [platform-ios.md](platform-ios.md) | iOS-specific design, HIG compliance |
| [platform-android.md](platform-android.md) | Android-specific design, Material Design 3 |
| [mobile-navigation.md](mobile-navigation.md) | Navigation patterns, deep linking |
| [mobile-typography.md](mobile-typography.md) | Type scale, system fonts, accessibility |
| [mobile-color-system.md](mobile-color-system.md) | OLED optimization, dark mode, battery |
| [decision-trees.md](decision-trees.md) | Framework, state, storage decisions |

---

> **Remember:** Mobile users are impatient, interrupted, and using imprecise fingers on small screens. Design for the WORST conditions: bad network, one hand, bright sun, low battery. If it works there, it works everywhere.
