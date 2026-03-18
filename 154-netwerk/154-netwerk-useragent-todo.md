---
number: 154
directory: netwerk
module: useragent
status: patch_created
patch_file: 154-netwerk-useragent.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 154-netwerk-useragent

## Conclusion

- Patch: 154-netwerk-useragent.patch
- Prefs: none (compile-time only)
- Prevents rebranded app name from leaking in User-Agent string. Two changes in `nsHttpHandler.cpp`: (1) define `UA_SPARE_PLATFORM` unconditionally (not just Windows), (2) force `isFirefox = true` to always emit "Firefox/x.y" and suppress custom app name. No runtime pref; UA string built once at startup.

## Changelog

### 2026-03-12 - Initial creation

- Two compile-time changes in nsHttpHandler.cpp
