# Mobile Framework Reference

Load this when adding mobile support to your project.

---

## Framework Selection

**Default:** Expo for Bun/Node stacks. Capacitor for Deno (wraps web apps).

| Framework | Best For | Monorepo Fit | Trade-off |
|-----------|----------|--------------|-----------|
| **Expo** | Native feel, OTA updates | Bun/Node workspaces | Requires Node tooling |
| **Capacitor** | Web-first, Deno projects | Any (wraps web build) | WebView, not truly native |
| **Flutter** | Max performance, custom UI | Separate (Dart) | Learning Dart |
| **Dioxus** | Rust full-stack, type safety | Separate (Rust/Cargo) | Learning Rust, maturing ecosystem |

---

## Quick Decision

- **Want native mobile UX?** → Use **Expo** (Bun or Node stack)
- **Already have a web app?** → Use **Capacitor** (works with Deno/Fresh)
- **Need max performance or custom UI?** → Consider **Flutter** (separate project)
- **Already using Rust or need memory safety?** → Consider **Dioxus** (emerging)

---

## Expo Essentials

| Concept | What it does |
|---------|--------------|
| **Managed workflow** | Expo handles native code (default, recommended) |
| **EAS Build** | Cloud builds for iOS/Android (30 free/month) |
| **EAS Submit** | Automated App Store/Play Store submission |
| **OTA updates** | Push JS updates without store review |

**Commands:**

```bash
# scaffold
bunx create-expo-app my-app -t expo-template-blank-typescript  # Bun
npx create-expo-app my-app -t expo-template-blank-typescript   # Node

# development
bunx expo start

# production
bunx eas build --platform all
bunx eas submit --platform all
```

---

## Capacitor (Deno/Web)

Capacitor wraps your web app as a native mobile app using WebView.

```bash
# in your web app directory
deno task build                             # build to static

# add Capacitor (one-time setup)
npm init -y && npm install @capacitor/core @capacitor/cli
npx cap init my-app com.example.myapp
npx cap add ios && npx cap add android

# sync and open
npx cap sync
npx cap open ios      # Xcode
npx cap open android  # Android Studio
```

---

## Dioxus (Rust)

> [!NOTE]
> Dioxus mobile is promising but still maturing. Mobile rendering currently uses webviews;
> native rendering (WGPU/Skia) is in development. Best for teams already invested in Rust.

| Aspect | Details |
|--------|---------|
| **Language** | Rust — memory safety, type safety, no GC |
| **Syntax** | RSX (JSX-like) — familiar to React developers |
| **Platforms** | Web, Desktop, Mobile (Android/iOS) from single codebase |
| **Mobile status** | First-class Android/iOS support, JNI/native API access |
| **Ecosystem** | Growing but smaller than React Native/Flutter |

**When to consider:**

- Team already knows Rust or plans to invest
- Backend is Rust (Axum, Actix) — shared types/logic
- Performance-critical modules where Rust shines
- Long-term bet on Rust ecosystem maturity

**When to avoid (for now):**

- New to Rust — double learning curve
- Need production-ready mobile tooling today
- Require extensive third-party library support

**Scaffolding:**

```bash
# Install Dioxus CLI
cargo install dioxus-cli

# Create new project
dx new my-app
cd my-app

# Run (desktop/web)
dx serve

# Build for mobile (requires platform SDKs)
dx build --platform android
dx build --platform ios
```

**Resources:** [dioxuslabs.com](https://dioxuslabs.com) | [GitHub](https://github.com/DioxusLabs/dioxus)
