---
number: 124
directory: toolkit
module: urlformatter
status: patch_created
patch_file: 124-toolkit-urlformatter.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 124-toolkit-urlformatter

## Conclusion

- Patch: 124-toolkit-urlformatter.patch
- Prefs: 124-toolkit-urlformatter-prefs.json
- Firefox embeds system fingerprinting data (OS version, CPU, RAM, channel, region, build ID) into URL template variables (`%OS_VERSION%`, `%SYSTEM_CAPABILITIES%`, etc.) for all outgoing service requests. Patch neutralizes 15 template variables across URLFormatter.sys.mjs (8 guards) and UpdateUtils.sys.mjs (7 guards) to return generic values. Pref: `patch.privacy.urlformatter.enabled` (default: false).

## Changelog

### 2026-03-12 - Initial creation

- 15 pref guard insertion points across 2 files
- Neutralized variables: OS_VERSION, OS, CHANNEL, DISTRIBUTION, DISTRIBUTION_VERSION, PLATFORMBUILDID, REGION, SYSTEM_CAPABILITIES
