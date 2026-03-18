---
number: 201
directory: portable
module: portable
status: patch_created
patch_file: 201-portable.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-11
patch_updated: 2026-03-14
---

# 201-portable

## Conclusion

- Patch: 201-portable.patch
- Prefs: 201-portable-prefs.json
- Always-on portable mode: all data stored in `<exe_dir>/data/`. Patch inserts portable path logic at the top of `GetUserDataDirectoryHome()` with auto-creation and logging. No mode toggle; Lacuna is always portable.

## Changelog

### 2026-03-14 - Rebuilt patch for ESR 140

- Original delta patch assumed pre-existing portable base code (from firefox-release)
- Regenerated as complete insertion (38 lines) against clean ESR 140 source
- Logic unchanged; verified with `git apply --check`

### 2026-01-18 - Added logging

- Printf logging for portable data directory path

### 2026-01-11 - Initial creation

- Portable mode via `GetUserDataDirectoryHome()` override
