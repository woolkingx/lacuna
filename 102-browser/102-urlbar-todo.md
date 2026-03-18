---
number: 102
directory: browser
module: urlbar
status: no_patch_needed
last_updated: 2026-03-18T00:00:00
security_audit: 2026-01-03
---

# 102-browser-urlbar

## Conclusion

- Patch: none
- Prefs: none
- All urlbar network requests route through MerinoClient. Setting `browser.urlbar.merino.endpointURL = ""` blocks all requests. Weather disabled by default (featureGate: false). Geolocation depends on Merino, no independent requests. Native prefs sufficient.

## Note

Initial audit (2026-01-03) incorrectly assumed native prefs sufficient while missing UrlbarSearchTermsPersistence RemoteSettings dependency. Re-analysis (2026-01-17) confirmed prefs are indeed sufficient after tracing MerinoClient as single network exit point.
