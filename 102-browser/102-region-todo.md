---
number: 102
directory: browser
module: region
status: completed
last_updated: 2026-03-18T00:00:00
---

# 102-browser-region

## Conclusion

- Patch: none (handled by 142-region.patch in 142-toolkit/)
- Prefs: none
- Browser region detection delegates to toolkit Region.sys.mjs. Patched there with hardcoded region fallback. See 142-toolkit/142-region-todo.md.
