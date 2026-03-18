---
number: 100
directory: custom
module: privacy-etp
status: prefs_only
last_updated: 2026-03-18T00:00:00
prefs_created: 2026-01-18
---

# 100-custom-privacy-etp

## Conclusion

- Patch: none
- Prefs: 100-privacy-etp-prefs.json
- Enhanced Tracking Protection and privacy prefs. Includes GPC header (`privacy.globalprivacycontrol.enabled`) and content script resource isolation. Sourced from Betterfox Securefox.js.

## Changelog

### 2026-03-08 - Ported Betterfox Securefox.js privacy prefs

- `privacy.globalprivacycontrol.enabled = true` (GPC header)
- `privacy.antitracking.isolateContentScriptResources = true`
