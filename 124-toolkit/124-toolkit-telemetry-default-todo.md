---
number: 124
directory: toolkit
module: telemetry-default
status: patch_created
patch_file: 124-toolkit-telemetry-default.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 124-toolkit-telemetry-default

## Conclusion

- Patch: 124-toolkit-telemetry-default.patch
- Prefs: none (compile-time only)
- Forces `TelemetryPrefValue()` in `Preferences.cpp` to return false unconditionally for both Android and non-Android builds. Removes all channel-based conditional logic (nightly/beta/release/RC). Compile-time change; no runtime pref needed.

## Changelog

### 2026-03-18 - Split from 103-preferences.patch

- Previously duplicated in 103-preferences.patch (same file, different concern)
- Now sole owner of TelemetryPrefValue() hunks in Preferences.cpp

### 2026-03-12 - Initial creation

- Both `TelemetryPrefValue()` variants (Android `Maybe<bool>`, non-Android `bool`) return false
