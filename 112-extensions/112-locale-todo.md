---
number: 112
directory: extensions
module: locale
status: patch_created
patch_file: 112-locale.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-11
---

# 112-extensions-locale

## Conclusion

- Patch: 112-locale.patch
- Prefs: none
- AddonManager triggers network requests on INTL_LOCALES_CHANGED events to check for locale-specific extension updates. Patch intercepts this automatic trigger.
