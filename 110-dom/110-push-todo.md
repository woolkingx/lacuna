---
number: 110
directory: dom
module: push
status: no_patch_needed
last_updated: 2026-03-18T00:00:00
security_audit: 2026-01-03
---

# 110-dom-push

## Conclusion

- Patch: none
- Prefs: none
- Web Push API maintains persistent WebSocket to Mozilla push server. Critical network exposure when enabled, but native controls (`dom.push.enabled = false`) provide complete protection. No patch needed.
