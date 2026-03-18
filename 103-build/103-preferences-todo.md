---
number: 103
directory: build
module: preferences
status: patch_created
patch_file: 103-preferences.patch
last_updated: 2026-03-18T00:00:00
---

# 103-build-preferences

## Conclusion

- Patch: 103-preferences.patch
- Prefs: none
- Auto-copies `prefs-template.js` to new profiles as `prefs.js` on first launch. Inserts logic in `Preferences::ReadSavedPrefs()` to detect missing prefs.js, then copies from `<exe_dir>/prefs-template.js`.

## Changelog

### 2026-03-18 - Split patch: removed telemetry-default hunks

- Telemetry `TelemetryPrefValue()` hunks moved to `124-toolkit-telemetry-default.patch` (was duplicated)
- This patch now only contains the prefs-template auto-copy logic (ReadSavedPrefs hunk)
