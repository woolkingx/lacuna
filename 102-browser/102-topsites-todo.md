---
number: 102
directory: browser
module: topsites
status: patch_created
patch_file: 102-topsites.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-03
security_audit: 2026-01-03
---

# 102-browser-topsites

## Conclusion

- Patch: 102-topsites.patch
- Prefs: none
- Top Sites fetches site data from RemoteSettings CDN (fixed URL). Native prefs cannot cover all network paths. Patch disables centralized collection at source.

## Changelog

### 2026-01-03 - Initial audit and patch

- Multiple network exit points identified; native prefs insufficient
- Strategy: disable centralized collection (consistent with region/newtab approach)
