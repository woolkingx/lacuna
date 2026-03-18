---
number: 154
directory: netwerk
module: useragent
status: patch_created
patch_file: 154-netwerk-useragent.patch
last_updated: 2026-03-12T22:00:00
patch_created: 2026-03-12
---

# 154-netwerk-useragent: Force User-Agent to Report as Firefox

## 功能說明

Force the User-Agent string to always report as Firefox. Two compile-time changes in `nsHttpHandler.cpp`:

1. **UA_SPARE_PLATFORM unconditionally defined** -- Previously only defined on Windows (`#ifdef XP_WIN`). Now defined on all platforms. This ensures the "spare" UA platform token behavior is available everywhere, not just Windows.

2. **isFirefox forced true** -- The variable `isFirefox` (line 956) is forced to `true` instead of checking `mAppName.EqualsLiteral("Firefox")`. This ensures the "Firefox/x.y" compatibility token is always appended to the UA string, and prevents the actual app name (e.g. "Librewolf", "Konform", or any custom branding) from leaking.

### Effect

Without this patch, a rebranded Firefox build would emit:

```
Mozilla/5.0 (...) Gecko/20100101 Firefox/128.0 CustomApp/128.0
```

With this patch, the UA is:

```
Mozilla/5.0 (...) Gecko/20100101 Firefox/128.0
```

The custom app name/version portion is suppressed because `isFirefox == true` skips the `!isFirefox` branch that appends `mAppName/mAppVersion`.

### No Pref Guard

This is a compile-time change with no runtime pref guard. Rationale:
- The UA string is built once at startup in `nsHttpHandler::BuildUserAgent()`
- A pref change at runtime would not rebuild the UA string without additional plumbing
- The privacy benefit is unconditional -- there is no scenario where leaking the real app name is desirable

## Patch 實作

**File**: `netwerk/protocol/http/nsHttpHandler.cpp`

### Change 1: UA_SPARE_PLATFORM (line 113-116)

```cpp
// Before:
#define UA_PREF_PREFIX "general.useragent."
#ifdef XP_WIN
#  define UA_SPARE_PLATFORM
#endif

// After:
#define UA_PREF_PREFIX "general.useragent."
// FIREBOX PATCH: Define UA_SPARE_PLATFORM unconditionally (not just Windows)
#define UA_SPARE_PLATFORM
```

### Change 2: isFirefox (line 956)

```cpp
// Before:
bool isFirefox = mAppName.EqualsLiteral("Firefox");

// After:
// FIREBOX PATCH: Force isFirefox true so UA always shows "Firefox/x.y"
bool isFirefox = true; // mAppName.EqualsLiteral("Firefox");
```

## 變更記錄

### 2026-03-12 - Initial patch creation

- Created `154-netwerk-useragent.patch` with two changes to `nsHttpHandler.cpp`
- Change 1: `UA_SPARE_PLATFORM` defined unconditionally (removes `#ifdef XP_WIN` guard)
- Change 2: `isFirefox` forced to `true` (prevents app name leak in UA string)
- No pref guard -- compile-time change only
- Patch verified: `git apply --check` passes cleanly
