---
number: 144
directory: dom
module: sendbeacon
status: patch_created
patch_file: 144-dom-sendbeacon.patch
last_updated: 2026-03-12T12:00:00
patch_created: 2026-03-12
---

# 144-sendbeacon - Mock sendBeacon to prevent analytics network leaks

## TL;DR - Core Conclusion

Navigator.sendBeacon() is used by websites to send analytics/telemetry data.
This patch inserts a pref-guarded early return in `SendBeaconInternal()` that
silently returns `true` (success) without opening any network connection.
The JS caller sees success, but no data leaves the browser.

- Pref: `patch.dom.sendbeacon.enabled` (default: `false` = blocked)
- Patch: `144-dom-sendbeacon.patch`
- Prefs: `144-dom-sendbeacon-prefs.json`

## Patch Description

### dom/base/Navigator.cpp

In `SendBeaconInternal()`, after the channel priority and class-of-service setup
(line ~1309), a StaticPrefs check is inserted. When `patch.dom.sendbeacon.enabled`
is false (default), the function returns `true` before the channel is opened,
effectively mocking a successful beacon send.

### modules/libpref/init/StaticPrefList.yaml

Adds `patch.dom.sendbeacon.enabled` as a static pref (bool, default false,
mirror: always) in the beacon section. This generates `StaticPrefs_patch.h`
with the accessor `StaticPrefs::patch_dom_sendbeacon_enabled()`.

## Security Audit

- **Risk**: None. The mock returns success to the caller, preventing JS errors.
- **User click principle**: sendBeacon is always automatic (no user interaction).
  Blocking by default is consistent with the Firebox transparency principle.
- **Reversibility**: Set `patch.dom.sendbeacon.enabled = true` in about:config
  to restore normal beacon behavior.

## Changelog

### 2026-03-12 - Initial creation (Phase 3 Konform integration)

- Created patch based on Konform reference `bug1961408-mock-sendbeacon.patch`
- Adapted to Firebox conventions: `patch.dom.sendbeacon.enabled` pref name,
  StaticPrefs access pattern, FIREBOX PATCH comment markers
- Insertion point: after `cos->AddClassFlags(nsIClassOfService::Background)`
  block in `SendBeaconInternal()`
- Added StaticPrefs_patch.h include to Navigator.cpp
- Added static pref definition in StaticPrefList.yaml beacon section
