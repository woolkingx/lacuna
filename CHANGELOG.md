# Changelog

All notable changes to Lacuna are documented here.

## [1.0.0] - 2026-03-18

First public release. Based on Firefox ESR 140.

### Core
- 232 privacy prefs blocking all known Firefox background connections
- 30 source patches across 7 module groups (browser, toolkit, services, dom, netwerk, security, custom)
- All patches toggleable via `about:preferences#lacuna`
- Portable mode: `data/` directory next to binary = self-contained profile

### Platforms
- Windows x64 (cross-compile via `--target=x86_64-pc-windows-msvc`)
- Linux x64 (native build)

### Branding
- Custom name, icon, about dialog (Lacuna Browser, fork of Firefox)
- New tab page wordmark

### Bundled Extensions
- uBlock Origin 1.70.0
- Containerise 3.9.0
- CanvasBlocker 1.12

### Build System
- `apply_patches.py` — 4-stage deploy (patches, resources, l10n, prefs+extensions)
- `generate_prefs.py` — aggregate *-prefs.json into prefs-template.js, auto-copy to obj-*/dist/bin/
- `regenerate_patches.py` — rebuild .patch files from ESR diff
- `generate_pane.py` — generate preferences UI from prefs.json
- Dual mozconfig: `mozconfig` (Windows), `mozconfig.linux` (Linux)

### Blocked Categories
- Telemetry (Glean, ping sender, data submission)
- Remote Settings (auto-sync)
- ASRouter (campaigns, CFR, What's New)
- New Tab (Discovery Stream, Pocket)
- Extensions (blocklist auto-update, system addon installs)
- Search (remote engine sync)
- GMP (automatic codec downloads)
- Region detection (IP-based)
- Safe Browsing (remote list updates)
- Updates (background checks)
- Normandy (remote experiments)
- Network (User-Agent, addon origin headers)
- DOM (navigator.sendBeacon)
- Fonts (remote fingerprint exposure)
