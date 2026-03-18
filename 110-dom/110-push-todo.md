---
feature: dom.push (Web Push API)
category: dom
directory: 110-dom
patch_file: N/A (no patch needed)
config_file: 110-dom-dom-prefs.json
security_audit: 2026-01-03
audit_result: no_patch_needed
status: completed
priority: high
last_updated: 2026-01-11
---

# TODO: dom.push (Web Push API)

## Summary

Web Push API provides website push notifications via persistent WebSocket connection to Mozilla's push server. While this creates CRITICAL network exposure when enabled, native Firefox controls provide complete protection without requiring additional patches.
**Audit Conclusion**: ✅ **NO PATCH NEEDED** - Native controls sufficient
---
- patch: 無
- prefs: 無
