---
number: 142
directory: toolkit
module: update
status: prefs_only
last_updated: 2026-03-18T00:00:00
---

# 142-toolkit-update

## Conclusion

- Patch: none (superseded by compile-time `--disable-updater` in mozconfig)
- Prefs: 142-update-prefs.json
- Firefox auto-update connects to aus5.mozilla.org periodically. Disabled at compile time via mozconfig. Runtime prefs provide defense-in-depth.

## Changelog

### 2026-03-12 - Patch removed

- Original `142-toolkit-update.patch` obsoleted by compile-time `--disable-updater`
- Runtime prefs retained as defense-in-depth

### 2026-01-09 - Original patch created

- Intercepted UpdateService.sys.mjs (now superseded)
