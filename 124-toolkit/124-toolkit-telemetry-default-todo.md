---
number: 124
directory: toolkit
module: telemetry-default
status: patch_created
patch_file: 124-toolkit-telemetry-default.patch
last_updated: 2026-03-12T22:00:00
patch_created: 2026-03-12
---

# 124-toolkit-telemetry-default

## 功能說明

Compile-time force telemetry default to `false`.

`modules/libpref/Preferences.cpp` contains two `TelemetryPrefValue()` functions that determine the compile-time default for `toolkit.telemetry.enabled`:

1. **Android version** (`#ifdef MOZ_WIDGET_ANDROID`) -- returns `Maybe<bool>`. Original logic checks if pref is already set, checks `MOZ_TELEMETRY_ON_BY_DEFAULT`, checks beta channel. Patched to unconditionally return `Some(false)`.

2. **Non-Android version** (`#else`) -- returns `bool`. Original logic checks channel (nightly/aurora/beta), `MOZILLA_OFFICIAL`, release candidate builds. Patched to unconditionally return `false`.

Both `SetupTelemetryPref()` callers remain unchanged -- they call `TelemetryPrefValue()` and set the default accordingly.

## Patch 實作

- **File**: `modules/libpref/Preferences.cpp`
- **Strategy**: Remove all conditional logic in both `TelemetryPrefValue()` functions, return `false` unconditionally
- **No prefs.json needed**: This is a compile-time change, not a runtime pref toggle
- **FIREBOX PATCH markers**: Added for traceability

## Security Audit

- **Risk**: None. Forces telemetry default OFF, which is strictly more private than upstream
- **Reversibility**: Removing the patch restores original channel-based logic
- **Side effects**: Extended telemetry data will not be sent on any channel by default

## 變更記錄

### 2026-03-12 - Initial patch creation

- Created `124-toolkit-telemetry-default.patch`
- Android `TelemetryPrefValue()`: removed `MOZ_TELEMETRY_ON_BY_DEFAULT` / beta channel / already-set checks, return `Some(false)`
- Non-Android `TelemetryPrefValue()`: removed nightly/aurora/beta/default/RC channel checks, return `false`
- No runtime prefs needed -- compile-time only
