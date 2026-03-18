---
number: 200
directory: ui
module: firststartup
status: disabled
patch_file: 200-firststartup.patch.disabled
last_updated: 2026-03-18T00:00:00
---

# 200-ui-firststartup

## Conclusion

- Patch: 200-firststartup.patch.disabled (obsolete)
- Prefs: none
- Originally added runtime pref check for Normandy init in FirstStartup.sys.mjs. Superseded by compile-time `MOZ_NORMANDY=False` in 100-custom-normandy-disable.patch, which makes the code path dead. Patch disabled, retained for reference only.
