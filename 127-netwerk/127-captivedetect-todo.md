---
number: 127
directory: netwerk
module: captivedetect
status: no_patch_needed
last_updated: 2026-03-18T00:00:00
security_audit: 2026-01-03
---

# 127-netwerk-captivedetect

## Conclusion

- Patch: none
- Prefs: 127-captivedetect-prefs.json
- Captive portal detection pings Mozilla's canonical URL to check network connectivity. Disabled via native prefs: `network.captive-portal-service.enabled = false` stops the service, `captivedetect.canonicalURL = ""` removes the target URL as defense-in-depth. No source patch needed.
