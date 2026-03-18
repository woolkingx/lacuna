---
number: 112
directory: extensions
module: blocklist
status: patch_created
patch_file: 112-extensions-blocklist.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-13
---

# 112-extensions-blocklist

## Conclusion

- Patch: 112-extensions-blocklist.patch
- Prefs: 112-extensions-blocklist-prefs.json
- MLBF (Multi-Level Bloom Filter) lets Mozilla silently block extensions via RemoteSettings background sync. Dual-layer patch: Layer 1 disables entire blocklist mechanism in `_init()`, Layer 2 blocks MLBF remote downloads in `_fetchMLBF()`. Local bundled dump still provides basic protection. Single pref `patch.extensions.blocklist.enabled` controls both layers.

## Patch Details

- File: `toolkit/mozapps/extensions/Blocklist.sys.mjs`
- Hunk 1: `_fetchMLBF()` -- return cached data instead of fetching remote MLBF
- Hunk 2: `_init()` -- force `extensions.blocklist.enabled = false`

## Changelog

### 2026-03-13 (2) - Dual-layer master switch

- Renamed pref: `patch.extensions.blocklist.remote.enabled` -> `patch.extensions.blocklist.enabled`
- Added Layer 1 in `_init()` for full blocklist disable
- Kept Layer 2 in `_fetchMLBF()` as defense-in-depth

### 2026-03-13 (1) - Initial single-layer implementation

- MLBF fetch guard in `_fetchMLBF()`
