---
number: 102
directory: browser
module: translations
status: module_disabled
patch_file: 102-translations.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-10
audit_completed: 2026-01-09
---

# 102-browser-translations

## Conclusion

- Patch: 102-translations.patch
- Prefs: 102-translations-prefs.json
- Firefox Translations auto-loads language model list on Settings page open, triggering network requests without explicit user action. Patch converts to lazy-load (fetch only on button click). Module disabled by default via `browser.translations.enable = false`. Patch retained for future lazy-load optimization.

## Changelog

### 2026-01-17 - Module disabled via pref

- Set `browser.translations.enable = false` as default

### 2026-01-10 - Patch created

- Target: `browser/components/preferences/main.js` initTranslations()
- Strategy: lazy-load language list on user click instead of page load
