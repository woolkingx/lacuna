---
number: 100
directory: custom
module: normandy-disable
status: patch_created
patch_file: 100-custom-normandy-disable.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 100-custom-normandy-disable

## Conclusion

- Patch: 100-custom-normandy-disable.patch
- Prefs: none (compile-time removal makes runtime prefs unnecessary)
- Normandy (experiment/rollout system) and Health Report disabled at compile time via `MOZ_NORMANDY=False` and `MOZ_SERVICES_HEALTHREPORT=False`. Follows Tor Browser approach (BB 41635). Supersedes the previous runtime pref approach (`100-app-normandy-todo.md`, now deleted).

## Patch Strategy

Three-file compile-time disable:

1. **browser/moz.configure** -- `MOZ_NORMANDY=False`, `MOZ_SERVICES_HEALTHREPORT=False`
2. **browser/components/BrowserComponents.manifest** -- `#ifdef MOZ_NORMANDY` guard on `Normandy.uninit`
3. **toolkit/components/moz.build** -- normandy build dir conditional on `CONFIG["MOZ_NORMANDY"]`

## Related Changes

- 100-app-prefs.json: removed 5 Normandy runtime prefs (no longer needed)
- 100-firststartup.patch: renamed to `.disabled` (redundant with compile-time flag)

## Reference

- `konform/patches/tb/bb41635-disable-normandy.patch`
- `konform/patches/disable-data-reporting-at-compile-time.patch`

## Changelog

### 2026-03-12 - Initial creation

- Compile-time Normandy disable targeting firefox-esr 140.1.0
- Replaces previous runtime pref approach
