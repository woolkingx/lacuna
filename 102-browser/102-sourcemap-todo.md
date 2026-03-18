---
number: 102
directory: browser
module: sourcemap
status: prefs_only
last_updated: 2026-03-18T00:00:00
security_audit: 2026-01-07
---

# 102-browser-sourcemap

## Conclusion

- Patch: none
- Prefs: 102-sourcemap-prefs.json
- DevTools source map service auto-connects to remote servers to fetch source maps. Audit identified need for patch, but prefs disable automatic connection. Patch deferred.
