# Lacuna

A privacy-focused Firefox build. Windows + Linux.

Lacuna patches Firefox ESR to remove outbound network activity that happens without explicit user action. The core principle: **the browser connects to the internet when you tell it to, not on its own.**

---

## Features

- **Zero background connections** — no telemetry, no pings, no auto-sync, no region detection. Silent until you click.
- **232 privacy prefs** — every known Firefox phone-home disabled at startup via `prefs-template.js`.
- **30 source patches** — code-level blocks on telemetry, Normandy, safe browsing, ASRouter, GMP, and more.
- **Portable mode** — `data/` directory next to binary = self-contained profile. No install, no registry, fully movable.
- **Dual platform** — Windows x64 (cross-compile) + Linux x64 (native). Same patches, same prefs.
- **Bundled extensions** — uBlock Origin, Containerise, CanvasBlocker pre-installed on first launch.
- **Per-patch toggle** — every patch has an on/off switch in `about:preferences#lacuna`.
- **Unsigned extension support** — install custom or self-built extensions without Mozilla signing. `xpinstall.signatures.required` disabled by default.
- **Custom branding** — Lacuna name, icon, about dialog. No Firefox branding confusion.

---

## ========== WARNING: REQUIRED EXTENSIONS ==========

> **Lacuna WITHOUT these extensions is NOT protected.**
>
> Lacuna patches the **browser**. It does NOT patch the **web**.
> Without the extensions below, websites track you freely.

| Extension | Status | Why |
|-----------|--------|-----|
| **uBlock Origin** | **MUST INSTALL** | Blocks ads, trackers, malicious scripts. Without this, every website runs whatever JavaScript it wants against you. |
| **Containerise** | **MUST INSTALL** | Isolates sites into containers. Without this, sites share cookies and storage across domains — login tracking, cross-site profiling, all of it. |
| **CanvasBlocker** | Recommended | Canvas/WebGL fingerprint protection. Optional if `privacy.resistFingerprinting` is already enabled (default in Lacuna). |

> **Do not skip uBlock Origin and Containerise.**
> They are as important as the 232 patches. Lacuna blocks Firefox from phoning home. These extensions block websites from phoning home about you.

All three are bundled in the portable release and auto-installed on first launch.

## =================================================

---

## Philosophy

Most privacy guides focus on configuration — tweaking `about:config`, installing extensions, hoping defaults behave. Lacuna takes a different approach: patch the source.

Two rules drive every decision:

1. **No unsolicited connections.** Telemetry, remote settings sync, recommendation feeds, update checks, region detection, safe browsing pings — all disabled at the source. If Firefox initiates a network request without you clicking something, it doesn't happen.

2. **On/off over removal.** Where a feature has a UI entry point (manually check for updates, install an extension), the feature is preserved but its automatic trigger is removed. Where there's no user-facing control, the feature is removed entirely.

The result: Firefox behaves like a local application. It fetches what you ask for. Nothing else.

---

## What Lacuna patches

| Area | What's blocked |
|------|---------------|
| Telemetry | All data submission, Glean, ping sender |
| Remote Settings | Auto-sync from Mozilla CDN (manual still works) |
| ASRouter | Campaign messages, CFR recommendations, What's New |
| New Tab | Discovery Stream / Pocket feed |
| Extensions | Blocklist auto-update, system addon installs, locale triggers |
| Search | Remote engine list sync |
| GMP | Automatic media codec downloads |
| Region | IP-based region detection |
| Safe Browsing | Remote list updates |
| Updates | Background update checks and downloads |
| Normandy | Remote experiment/feature rollout system |
| Network | User-Agent simplification, addon origin headers |
| DOM | `navigator.sendBeacon` (used for tracking) |
| Fonts | Remote font fingerprint exposure |

232 preferences, 30 patches. All individually toggleable via `about:preferences#lacuna`.

---

## What Lacuna does not do

- **Not a Tor browser.** No traffic routing, no anonymity network. Use Tor Browser for that.
- **Not a hardened config.** Lacuna patches source code; it does not replace a carefully tuned `user.js`.

---

## Platforms

| Platform | Binary | Build method |
|----------|--------|-------------|
| Windows x64 | `lacuna.exe` | Cross-compile (`--target=x86_64-pc-windows-msvc`) |
| Linux x64 | `lacuna` | Native build |

Both builds include portable mode, bundled extensions, and 232 privacy prefs.

---

## Architecture

```
firefox-patch/          <- this repo
├── 1xx-*/              <- source patches by Firefox module
├── 200-ui/             <- Lacuna preferences pane, branding, extensions
│   ├── branding/       <- icons + about dialog assets
│   └── distribution/   <- policies.json + bundled extensions
├── scripts/
│   ├── apply_patches.py      <- full deploy to clean ESR tree
│   ├── regenerate_patches.py <- rebuild .patch files from ESR diff
│   ├── generate_pane.py      <- generate UI from prefs.json
│   └── generate_prefs.py     <- generate prefs-template.js + copy to builds
├── mozconfig               <- Windows cross-compile config
├── mozconfig.linux         <- Linux native config
└── README.md

firefox-esr/            <- Firefox ESR 140 source (build target)
```

### Deploying to a fresh ESR tree

```bash
# Apply all patches + copy UI + append l10n + generate prefs
python3 scripts/apply_patches.py

# Dry run (check only, no writes)
python3 scripts/apply_patches.py --dry

# Specific stages only
python3 scripts/apply_patches.py --stage 1,2
```

### Apply stages

| Stage | Content |
|-------|---------|
| 1 | Apply .patch files |
| 2 | Copy resources (mozconfig, branding, icons, UI) |
| 3 | Append l10n strings |
| 4 | Generate prefs-template.js + copy to builds + copy extensions |

### Build

```bash
cd firefox-esr

# Windows (cross-compile)
./mach build

# Linux (native)
MOZCONFIG=mozconfig.linux ./mach build
```

Incremental builds take 10-30 minutes. Full builds several hours.

---

## Patch conventions

Guards use a consistent pattern:

```javascript
// LACUNA PATCH: description
if (Services.prefs.getBoolPref("patch.module.name.enabled", true)) {
  return;
}
// END LACUNA PATCH
```

`true` = protection active (default). All patch prefs default to on. Toggle via `about:preferences#lacuna`.

---

## Portable mode

Lacuna includes a portable profile patch. When a `data/` directory exists next to the executable, Firefox uses it as the profile root instead of the system profile location.

**Setup:**
```
Lacuna/
├── lacuna.exe        <- (or lacuna on Linux)
├── data/             <- created automatically on first launch
│   └── (profile data written here)
└── ...
```

All profile data — settings, extensions, history, cookies — stays inside `data/`, making the entire installation self-contained and movable.

This is implemented as a source-level patch to `toolkit/xre/nsXREDirProvider.cpp`, not a wrapper script or `--profile` flag.

> **Note:** The portable patch is always active. If `data/` exists or is creatable, portable mode engages.

---

## Acknowledgements

Lacuna builds on the work of projects that mapped Firefox's privacy landscape:

- **[arkenfox user.js](https://github.com/arkenfox/user.js)** — the most thorough `user.js` reference. Lacuna's patch scope was informed by arkenfox's research.
- **[LibreWolf](https://librewolf.net/)** — a hardened Firefox fork. Demonstrated that maintaining a Firefox fork long-term is viable.
- **[Konform Browser](https://codeberg.org/konform-browser/source)** — a privacy-focused Firefox fork. Several Lacuna patches were informed by Konform's approach.

The fundamental difference: those projects configure Firefox. Lacuna patches it.

---

## Status

Based on Firefox ESR 140. Windows x64 + Linux x64.
