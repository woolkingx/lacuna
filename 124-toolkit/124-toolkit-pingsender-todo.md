---
number: 124
directory: toolkit
module: pingsender
status: patch_created
patch_file: 124-toolkit-pingsender.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 124-toolkit-pingsender

## Conclusion

- Patch: 124-toolkit-pingsender.patch
- Prefs: 124-toolkit-pingsender-prefs.json
- Pingsender is a standalone executable spawned after browser shutdown to POST telemetry to Mozilla. No UI, no user action, pure background behavior. Three-layer defense: (1) runtime pref guard on `runPingSender()`, (2) build system removal from `DIRS`, (3) packaging removal from 4 installer manifests. Pref: `patch.telemetry.pingsender.enabled` (default: false). 6 files modified.

## Changelog

### 2026-03-12 - Initial creation

- Three-layer defense: runtime guard + build removal + packaging removal
