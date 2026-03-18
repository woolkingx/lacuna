---
number: 134
directory: services
module: settings.utils
category: services
last_updated: 2026-03-12T12:00:00
status: patch_created
security_audit: 2026-01-18
audit_result: approved
patch_created: 2026-01-18
patch_strategy: url_level_interception
patch_file: 134-utils.patch
---

# 134-services-settings-utils - RemoteSettings 核心攔截

## TL;DR - 核心結論

- patch: 134-utils.patch
- prefs: patch.services.settings.enabled (from 134-services-prefs.json)
- 攔截範圍: Utils.sys.mjs (SERVER_URL, LOAD_DUMPS) + SearchUtils.sys.mjs (ENGINES_URLS)

## Patch 實作

### Utils.sys.mjs
- **SERVER_URL getter**: When `patch.services.settings.enabled` is false, returns `"https://%.invalid"` to prevent all RemoteSettings connections
- **LOAD_DUMPS getter**: Always returns `true` to ensure local dumps are loaded regardless of server URL

### SearchUtils.sys.mjs
- **ENGINES_URLS**: Converted from static object to getter. When `patch.services.settings.enabled` is false, prod-main and prod-preview URLs return `"https://%.invalid"` to prevent remote search engine config fetching. Stage URLs left unchanged (only used in development).

## 變更記錄

### 2026-03-12 - Phase 2a: Konform integration + SearchUtils coverage

1. **SERVER_URL return value changed**: `""` -> `"https://%.invalid"` (aligns with Konform pattern; more explicit invalid URL that fails DNS resolution immediately rather than empty string which may cause different failure modes)
2. **Added SearchUtils.sys.mjs ENGINES_URLS patch**: New coverage for `toolkit/components/search/SearchUtils.sys.mjs`. Converted static `ENGINES_URLS` object to getter with pref guard. Prod-main and prod-preview URLs blocked when `patch.services.settings.enabled` is false. Reuses existing pref (no new prefs needed).
3. **Konform reference**: Aligned with `konform/patches/sed-patches/stop-undesired-requests.patch` approach but using Firebox pref-guard pattern instead of hardcoded replacement.

### 2026-01-18 - Initial patch creation

- Created 134-utils.patch with SERVER_URL and LOAD_DUMPS interception
- SERVER_URL returned `""` when disabled
- LOAD_DUMPS always returns true
