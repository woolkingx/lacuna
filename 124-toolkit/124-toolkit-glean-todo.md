---
number: 124
directory: toolkit
module: glean
status: patch_created
patch_file: 124-toolkit-glean.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 124-toolkit-glean

## Conclusion

- Patch: 124-toolkit-glean.patch
- Prefs: none (compile-time only)
- Glean telemetry upload enabled by default in official Firefox builds. Patch unconditionally enables `glean_disable_upload` Rust feature flag in `gkrust-features.mozbuild`, disabling upload at compile time regardless of `MOZILLA_OFFICIAL`. Requires full rebuild.

## Changelog

### 2026-03-12 - Initial creation

- Comment out `MOZILLA_OFFICIAL` conditional, make `glean_disable_upload` unconditional
