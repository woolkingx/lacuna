---
number: 134
directory: services
module: fallback
status: patch_created
patch_file: 134-services-fallback.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 134-services-fallback

## Conclusion

- Patch: 134-services-fallback.patch
- Prefs: 134-services-fallback-prefs.json
- Forces RemoteSettings to use local cached/dump data instead of fetching from remote servers. Patches `Attachments.sys.mjs` (force `fallbackToCache = true`, `fallbackToDump = true`) and `Utils.sys.mjs` (`LOAD_DUMPS` returns true). Pref: `patch.services.settings.fallback.enabled` (default: false). Works with 134-utils.patch for complete RS network blocking.

## Changelog

### 2026-03-12 - Initial creation (Konform integration)

- Two-file patch: Attachments.sys.mjs + Utils.sys.mjs
- Reference: Konform `rs-local.patch`
