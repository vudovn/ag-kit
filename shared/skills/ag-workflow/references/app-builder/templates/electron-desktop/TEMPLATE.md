---
name: electron-desktop
description: Electron desktop app template principles. Cross-platform, React, TypeScript.
---

# Electron Desktop App Template

> Versions reflect the latest stable line verified 2026-05. Pin to the current stable when scaffolding.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Electron 42+ |
| UI | React 19 |
| Language | TypeScript |
| Styling | Tailwind CSS v4 |
| Bundler | electron-vite + electron-builder |
| IPC | Type-safe communication (contextBridge) |

---

## Directory Structure

> electron-vite layout: main / preload / renderer separation is the 2026 standard.

```
project-name/
├── src/
│   ├── main/            # Main process (lifecycle, windows, IPC handlers)
│   │   └── index.ts
│   ├── preload/         # contextBridge — type-safe IPC surface
│   │   ├── index.ts
│   │   └── index.d.ts   # Ambient types shared with renderer
│   └── renderer/        # React app
│       ├── index.html
│       └── src/
│           ├── main.tsx
│           ├── App.tsx
│           └── components/
├── resources/           # App icons / static (build-time)
├── build/               # Builder assets (entitlements, icons)
├── electron.vite.config.ts
├── electron-builder.yml
└── package.json         # scripts: electron-vite dev | build | preview
```

---

## Process Model

| Process | Role |
|---------|------|
| Main | Node.js, system access |
| Renderer | Chromium, React UI |
| Preload | Bridge, context isolation |

---

## Key Concepts

| Concept | Purpose |
|---------|---------|
| contextBridge | Safe API exposure |
| ipcMain/ipcRenderer | Process communication |
| nodeIntegration: false | Security |
| contextIsolation: true | Security |

---

## Setup Steps

1. `npm create @quick-start/electron@latest {{name}} -- --template react-ts`
2. `cd {{name}} && npm install`
3. Add Tailwind v4: `npm install tailwindcss @tailwindcss/vite`
4. Define IPC types in `src/preload/index.d.ts`
5. `npm run dev`

---

## Build Targets

| Platform | Output |
|----------|--------|
| Windows | NSIS, Portable |
| macOS | DMG, ZIP |
| Linux | AppImage, DEB |

---

## Best Practices

- `contextIsolation: true` (default v12+), `sandbox: true` (default v20+), `nodeIntegration: false` (default v5+) — never enable Node for remote content
- Expose a narrow API via `contextBridge.exposeInMainWorld`, never raw `ipcRenderer`
- Validate IPC `sender` against an allowlist; set a restrictive CSP (`script-src 'self'`)
- Type-safe IPC: share types from `preload/index.d.ts` into the renderer
- Auto-updates with electron-updater
