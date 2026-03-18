---
number: 144
directory: dom
module: sendbeacon
status: patch_created
patch_file: 144-dom-sendbeacon.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 144-dom-sendbeacon

## Conclusion

- Patch: 144-dom-sendbeacon.patch
- Prefs: 144-dom-sendbeacon-prefs.json
- `Navigator.sendBeacon()` sends analytics/telemetry data automatically (no user action). Patch inserts StaticPrefs guard in `SendBeaconInternal()` (Navigator.cpp) that returns `true` without opening any network connection. JS caller sees success; no data leaves the browser. Pref: `patch.dom.sendbeacon.enabled` (default: false). Also adds pref definition to StaticPrefList.yaml.

## Changelog

### 2026-03-12 - Initial creation (Konform integration)

- Reference: Konform `bug1961408-mock-sendbeacon.patch`
- Insertion point: after class-of-service setup in `SendBeaconInternal()`
