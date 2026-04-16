---
number: 100
directory: custom
module: privacy-etp
status: prefs_only
last_updated: 2026-04-16T09:25:00
prefs_created: 2026-01-18
---

# 100-custom-privacy-etp

## Conclusion

- Patch: none
- Prefs: 100-privacy-etp-prefs.json
- Enhanced Tracking Protection and privacy prefs. Includes GPC header (`privacy.globalprivacycontrol.enabled`) and content script resource isolation. Sourced from Betterfox Securefox.js.

## Changelog

### 2026-04-16 - Enable ETP Standard to pair with containTAB defaultContainer

- `privacy.trackingprotection.enabled = true` (ETP Standard)
- `privacy.trackingprotection.pbmode.enabled = true`
- Rationale: containTAB defaultContainer opens a fresh container per tab with an empty cookie store. An empty store is itself a fingerprint ("too clean"). ETP Standard is the most natural mitigation — no patching or cookie simulation required.
- Note: Lacuna blocks Mozilla remote settings, so the ETP blocklist cannot update. However, the bundled blocklist remains effective and enabling ETP still provides value.

### 2026-03-08 - Port Betterfox Securefox.js privacy prefs

- `privacy.globalprivacycontrol.enabled = true` (GPC header)
- `privacy.antitracking.isolateContentScriptResources = true`
