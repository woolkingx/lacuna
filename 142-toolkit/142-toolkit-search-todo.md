---
number: 142
directory: toolkit
module: search
status: patch_created
patch_file: 142-toolkit-search.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 142-toolkit-search

## Conclusion

- Patch: 142-toolkit-search.patch
- Prefs: 142-toolkit-search-prefs.json
- Filters search engine config to DuckDuckGo only when `patch.search.engines.enabled = false` (default). Three interception points in SearchEngineSelector.sys.mjs: (1) filter `_configuration` array to DDG + metadata records, (2) block `_onConfigurationUpdated`, (3) block `_onConfigurationOverridesUpdated`. Works with 134-utils.patch (blocks RS URLs) and 134-services-fallback.patch (forces local dumps). Users can still add custom engines via OpenSearch or extensions.

## Changelog

### 2026-03-12 - Initial creation (Konform integration)

- DDG-only filtering in SearchEngineSelector.sys.mjs
- Reference: Konform `bb43525-no-rs-searchengines.patch`
