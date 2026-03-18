---
number: 134
directory: services
module: utils
status: patch_created
patch_file: 134-utils.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-18
---

# 134-services-utils

## Conclusion

- Patch: 134-utils.patch
- Prefs: via `patch.services.settings.enabled` in 134-services-prefs.json
- Core RemoteSettings interception. `SERVER_URL` returns `"https://%.invalid"` when disabled (immediate DNS failure). `LOAD_DUMPS` returns true unconditionally. `SearchUtils.ENGINES_URLS` prod URLs blocked. Three files: Utils.sys.mjs, SearchUtils.sys.mjs. Previously named 134-services-settings-utils.

## Changelog

### 2026-03-12 - Konform integration + SearchUtils coverage

- SERVER_URL changed from `""` to `"https://%.invalid"` (Konform pattern)
- Added SearchUtils.sys.mjs ENGINES_URLS pref guard

### 2026-01-18 - Initial creation

- SERVER_URL + LOAD_DUMPS interception in Utils.sys.mjs
