---
number: 142
directory: toolkit
module: search
status: patch_created
patch_file: 142-toolkit-search.patch
last_updated: 2026-03-12T00:00:00
patch_created: 2026-03-12
---

# 142-toolkit-search - Search Engine Filtering (DDG Only)

## TL;DR

When `patch.search.engines.enabled` is `false` (default), filter search engine configuration to keep only DuckDuckGo. All other engines (Google, Bing, etc.) are removed from the configuration at load time. Remote configuration updates are blocked.

Users can still add custom engines manually via OpenSearch or extensions.

## Patch Strategy

### Target File

`toolkit/components/search/SearchEngineSelector.sys.mjs`

### Three Insertion Points

1. **`getEngineConfiguration()`** (after `_configuration` is loaded, before length check):
   - Filter `_configuration` array: keep only records where `recordType === "engine"` AND `identifier === "ddg"`, plus all non-engine records (`defaultEngines`, `engineOrders`, `availableLocales`)
   - Override `defaultEngines` record: set `globalDefault = "ddg"`, `globalDefaultPrivate = "ddg"`, clear `specificDefaults` (removes Baidu/China, distribution-specific defaults)

2. **`_onConfigurationUpdated()`** (at top of method):
   - Early return when pref is false, blocking remote search config updates

3. **`_onConfigurationOverridesUpdated()`** (at top of method):
   - Early return when pref is false, blocking remote override updates

### Data Flow

```
RS dump (search-config-v2.json) → _getConfiguration() → _configuration array
                                                          ↓
                                                   [FIREBOX FILTER]
                                                          ↓
                                                   DDG-only config
                                                          ↓
                                          fetchEngineConfiguration() → engines[]
```

### Pref

| pref | default | effect |
|------|---------|--------|
| `patch.search.engines.enabled` | `false` | When false: DDG only. When true: all Firefox defaults |

### Interaction with Other Patches

- **134-utils.patch**: Blocks RS `SERVER_URL` and `ENGINES_URLS` -- prevents remote fetching of search config. This patch is complementary: even if RS somehow delivered new config, both the initial load filter and the sync handlers block it.
- **134-services-fallback.patch**: Forces RS to use local dumps. The local dump (`search-config-v2.json`) contains all engines; this patch filters that dump to DDG-only.

### What Gets Kept

- `ddg` engine record (DuckDuckGo with partnerCode, suggestions URL, etc.)
- `defaultEngines` record (modified: globalDefault/globalDefaultPrivate = "ddg")
- `engineOrders` record (kept as-is; only DDG engine survives filtering anyway)
- `availableLocales` record (metadata, no network impact)

### What Gets Removed

All other engine records: google, bing, baidu, ecosia, leo-de, wikipedia, etc.

## 變更記錄

### 2026-03-12 - Initial creation (Phase 4 Konform integration)

- Created patch for DDG-only search engine filtering
- Three-point interception in SearchEngineSelector.sys.mjs
- Konform reference: `bb43525-no-rs-searchengines.patch` (Tor Browser approach replaces entire getEngineConfiguration with chrome:// JSON fetch; Firebox approach filters existing RS dump instead, preserving pref-guard reversibility)
- Verified patch applies cleanly against ESR 140.1.0
