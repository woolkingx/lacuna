---
number: 102
directory: browser
module: asrouter
status: patch_created
patch_file: 102-asrouter.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-03
---

# 102-browser-asrouter

## Conclusion

- Patch: 102-asrouter.patch
- Prefs: none
- ASRouter fetches remote messaging configs (What's New, CFR, onboarding) from Mozilla servers automatically. Patch disables centralized collection at source.

## Changelog

### 2026-01-03 - Initial audit and patch

- Audit result: patch needed (automatic background fetch of remote messages)
- Strategy: disable centralized collection
