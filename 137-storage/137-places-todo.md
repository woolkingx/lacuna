---
number: 137
directory: storage
module: places
status: no_patch_needed
last_updated: 2026-03-18T00:00:00
security_audit: 2026-01-03
---

# 137-storage-places

## Conclusion

- Patch: none
- Prefs: none
- Places is a local SQLite database. All network behavior is user-triggered (speculative connect on click, favicon on page load, sync on explicit login). `browser.places.speculativeConnect.enabled = false` covers the one configurable case. Taskbar favicon and sync handled by other modules. No patch needed.
