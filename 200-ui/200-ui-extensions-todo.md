---
number: 200
directory: ui
module: extensions
status: prefs_only
last_updated: 2026-03-18T00:00:00
---

# 200-ui-extensions

## Conclusion

- Patch: none
- Prefs: 200-ui-extensions-prefs.json
- Force-installs 4 privacy extensions via Enterprise Policy (`distribution/policies.json`): Multi-Account Containers, uBlock Origin, CanvasBlocker, Bitwarden. Downloads from AMO on first launch (requires network). Users cannot disable these extensions. Prefs set `extensions.autoDisableScopes = 0` and `extensions.enabledScopes = 15` to ensure policy extensions activate.

## Changelog

### 2026-03-13 - Initial creation

- Created distribution/policies.json with ExtensionSettings force_installed
