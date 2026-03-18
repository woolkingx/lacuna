---
number: 134
directory: services
module: remotesettings
status: prefs_only
last_updated: 2026-03-18T00:00:00
---

# 134-services-remotesettings

## Conclusion

- Patch: none (network blocking handled by 134-utils.patch and 134-services-fallback.patch)
- Prefs: 134-remotesettings-prefs.json
- RemoteSettings runtime prefs. Source-level interception done in 134-utils (SERVER_URL -> %.invalid) and 134-services-fallback (forced local dump fallback).
