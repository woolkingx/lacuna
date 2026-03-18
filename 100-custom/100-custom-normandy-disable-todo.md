---
number: 100
directory: custom
module: normandy-disable
status: patch_created
patch_file: 100-custom-normandy-disable.patch
last_updated: 2026-03-12T00:00:00
patch_created: 2026-03-12
---

# 100-custom-normandy-disable

Compile-time disable of Normandy (experiment/rollout system) and Health Report data collection. Replaces the previous runtime pref-based approach with build-system-level exclusion.

## Patch Strategy

Three-file compile-time disable, following the Tor Browser approach (BB 41635):

1. **browser/moz.configure** -- Set `MOZ_NORMANDY=False` and `MOZ_SERVICES_HEALTHREPORT=False` at build configuration level. This propagates to `AppConstants.MOZ_NORMANDY` and removes Normandy/healthreport code paths at compile time.

2. **browser/components/BrowserComponents.manifest** -- Wrap `Normandy.uninit` registration with `#ifdef MOZ_NORMANDY` / `#endif`. The `Normandy.init` registration was already wrapped upstream; only the shutdown handler was missing the guard.

3. **toolkit/components/moz.build** -- Make the `normandy` build directory conditional on `CONFIG["MOZ_NORMANDY"]`. When False, the entire normandy directory is excluded from the build. The `messaging-system` directory remains unconditional.

## Related Changes

- **100-app-prefs.json**: Removed 5 Normandy runtime prefs (`app.normandy.enabled`, `app.normandy.api_url`, `app.normandy.first_run`, `app.normandy.run_interval_seconds`, `app.normandy.shieldLearnMoreUrl`). These are no longer needed since the component is excluded at compile time.

- **100-firststartup.patch**: Renamed to `.disabled`. This patch added a runtime pref check in `FirstStartup.sys.mjs` for Normandy init. With `MOZ_NORMANDY=False`, `AppConstants.MOZ_NORMANDY` is already false, so the code block is dead -- no runtime patch needed.

## Reference

- Konform reference: `konform/patches/tb/bb41635-disable-normandy.patch` (Tor Browser)
- Konform reference: `konform/patches/disable-data-reporting-at-compile-time.patch`

## Changelog

### 2026-03-12 - Initial creation: compile-time Normandy disable

- Created `100-custom-normandy-disable.patch` targeting firefox-esr 140.1.0
- Disabled `MOZ_NORMANDY` and `MOZ_SERVICES_HEALTHREPORT` in `browser/moz.configure`
- Added `#ifdef MOZ_NORMANDY` guard around `Normandy.uninit` in BrowserComponents.manifest
- Made normandy build directory conditional in `toolkit/components/moz.build`
- Removed 5 Normandy prefs from `100-app-prefs.json` (compile-time removal makes runtime prefs unnecessary)
- Disabled `100-firststartup.patch` (redundant with compile-time flag)
- Replaces previous `100-app-normandy-todo.md` approach (runtime pref control)
