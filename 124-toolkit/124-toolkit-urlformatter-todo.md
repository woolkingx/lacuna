---
number: 124
directory: toolkit
module: urlformatter
status: patch_created
patch_file: 124-toolkit-urlformatter.patch
last_updated: 2026-03-12T22:30:00
patch_created: 2026-03-12
---

# 124-toolkit-urlformatter: URL Template Variable Fingerprinting Reduction

## 功能說明

Firefox's `nsURLFormatterService` and `UpdateUtils` replace `%VARIABLE%` placeholders in URLs with system-specific values (OS version, CPU instruction set, RAM size, distribution ID, channel, etc.). These template variables leak detailed system fingerprinting information in outgoing HTTP requests.

### 原始行為

Every URL formatted through `nsURLFormatterService.formatURL()` or `UpdateUtils.formatUpdateURL()` embeds real system data:
- `%OS_VERSION%` → actual OS name + version + secondary library
- `%OS%` → actual OS identifier (e.g. `Windows_NT`, `Darwin`)
- `%CHANNEL%` → actual update channel
- `%DISTRIBUTION%` / `%DISTRIBUTION_VERSION%` → distribution prefs
- `%PLATFORMBUILDID%` → exact build timestamp
- `%SYSTEM_CAPABILITIES%` → CPU instruction set + RAM size
- `%REGION%` → geoip region code

### 修改後行為

When `patch.privacy.urlformatter.enabled` is `false` (default), all template variables return generic/neutral values:

| Variable | Neutralized Value |
|----------|-------------------|
| `%OS_VERSION%` | `encodeURIComponent("default")` (URLFormatter) / `encodeURIComponent("Linux 6.12.1-1")` (UpdateUtils) |
| `%OS%` | `"Linux"` |
| `%CHANNEL%` | `"esr"` |
| `%DISTRIBUTION%` | `"default"` |
| `%DISTRIBUTION_VERSION%` | `"default"` |
| `%PLATFORMBUILDID%` | `""` |
| `%REGION%` | `"ZZ"` |
| `%SYSTEM_CAPABILITIES%` | `"ISET:unknown,MEM:unknown"` |

Setting pref to `true` restores original behavior (all real system data in URLs).

### 技術細節

- **Pref**: `patch.privacy.urlformatter.enabled` (default: `false`)
- **Files modified**: 2
  - `toolkit/components/urlformatter/URLFormatter.sys.mjs` — 8 insertion points
  - `toolkit/modules/UpdateUtils.sys.mjs` — 7 insertion points
- **Layer**: Runtime pref guard (each getter/method checks pref independently)
- **Pattern**: Early-return with generic value before real system data collection

## Patch 實作

### URLFormatter.sys.mjs (8 guards)

1. **`OSVersion` lazy getter** — returns `encodeURIComponent("default")`
2. **`distribution` lazy getter** — returns `{ id: "default", version: "default" }`
3. **`REGION()` method** — returns `"ZZ"`
4. **`PLATFORMBUILDID()` method** — returns `""`
5. **`OS()` method** — returns `"Linux"`
6. **`CHANNEL` (converted from arrow to method)** — returns `"esr"`
7. **`DISTRIBUTION()` method** — returns `"default"`
8. **`DISTRIBUTION_VERSION()` method** — returns `"default"`

### UpdateUtils.sys.mjs (7 guards)

1. **`formatUpdateURL` switch `"CHANNEL"`** — sets `replacement = "esr"`
2. **`formatUpdateURL` switch `"DISTRIBUTION"`** — sets `replacement = "default"`
3. **`formatUpdateURL` switch `"DISTRIBUTION_VERSION"`** — sets `replacement = "default"`
4. **`getDistributionPrefValue()` function** — returns `"default"`
5. **`getMemoryMB()` function** — returns `"unknown"`
6. **`gInstructionSet` lazy getter** — returns `"unknown"`
7. **`UpdateUtils.OSVersion` lazy getter** — returns `encodeURIComponent("Linux 6.12.1-1")`

### 設計決策

- **Why guard each method individually?** The `_defaults` object methods are called independently via `formatURL()` string replacement. Each variable needs its own guard because URLs may contain any subset of variables.
- **Why convert CHANNEL from arrow to method?** Arrow functions cannot contain early-return pref checks. Converting to a regular method allows the standard Firebox pref guard pattern.
- **Why duplicate guards in UpdateUtils?** `UpdateUtils.formatUpdateURL()` is a separate code path from `nsURLFormatterService.formatURL()`. Both format URLs with the same variable names but through independent implementations.

## 影響範圍

- All URLs formatted through `nsURLFormatterService` (most Mozilla service URLs)
- All URLs formatted through `UpdateUtils.formatUpdateURL()` (update check URLs)
- Does NOT affect: `%LOCALE%`, `%VENDOR%`, `%NAME%`, `%ID%`, `%VERSION%`, `%MAJOR_VERSION%`, `%APPBUILDID%`, `%PLATFORMVERSION%`, `%APP%`, `%XPCOMABI%`, `%BUILD_TARGET%`, `%MOZILLA_API_KEY%`, `%GOOGLE_*_API_KEY%`, `%BING_*%`

## Security Audit

- **Risk**: Low. Generic values may cause server-side logic to return less-specific responses (e.g., update server might return generic update packages). This is acceptable for a privacy-focused build.
- **Reversibility**: Set `patch.privacy.urlformatter.enabled` to `true` in about:config to restore all original system information.

## 變更記錄

### 2026-03-12 - Initial patch creation

- Created patch covering URLFormatter.sys.mjs (8 guards) and UpdateUtils.sys.mjs (7 guards)
- Total 15 pref guard insertion points
- Single controlling pref: `patch.privacy.urlformatter.enabled` (default: false)
- Verified patch applies cleanly with `git apply --check`
