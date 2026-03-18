---
number: 142
directory: toolkit
module: region
status: patch_created
patch_file: 142-region.patch
last_updated: 2026-03-18T00:00:00
---

# 142-toolkit-region

## Conclusion

- Patch: 142-region.patch
- Prefs: none
- Region.sys.mjs `_fetchRegion()` connects to Mozilla's GeoIP service at startup. Patch injects hardcoded region fallback (default "US" via `patch.browser.region.hardcoded`) when `patch.browser.region.enabled = false`, skipping network detection entirely.

## Changelog

### 2026-03-14 - Fixed patch context offset for ESR 140

- ESR version added retry logic and Glean telemetry to `_fetchRegion()`, causing context mismatch
- Regenerated patch from ESR source; logic unchanged

### 2026-01-03 - Initial creation

- Hardcoded region fallback in `_fetchRegion()`
