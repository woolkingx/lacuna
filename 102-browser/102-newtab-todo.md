---
number: 102
directory: browser
module: newtab
status: patch_created
patch_file: 102-newtab.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-03
---

# 102-browser-newtab

## Conclusion

- Patch: 102-newtab.patch
- Prefs: none
- New Tab page fetches remote content (Top Sites, Pocket, snippets) from Mozilla CDN on every new tab open. Patch disables centralized collection.

## Changelog

### 2026-01-03 - Initial audit and patch

- Audit result: patch needed (automatic CDN fetches without user action)
- Strategy: disable centralized collection
