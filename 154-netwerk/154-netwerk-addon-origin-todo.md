---
number: 154
directory: netwerk
module: addon-origin
status: patch_created
patch_file: 154-netwerk-addon-origin.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 154-netwerk-addon-origin

## Conclusion

- Patch: 154-netwerk-addon-origin.patch
- Prefs: 154-netwerk-addon-origin-prefs.json
- Extensions leak unique `moz-extension://<UUID>` in Origin headers, enabling cross-site tracking. Patch adds 4-mode behavior control in `nsHttpChannel::SetOriginHeader()`: mode 0 (null, default) = `Origin: null`; mode 1 (strip) = remove header; mode 2 (keep) = Firefox default; mode 3 (scramble) = random UUID per request. Pref: `network.http.addonOriginBehavior` (uint, default: 0). Covers both existing-header and new-header code paths.

## Changelog

### 2026-03-12 - Initial creation

- Four-mode addon origin header control
- Refactored `shouldNullifyOriginHeader` -> `getPossiblyNullOriginURI` for scheme detection
- Konform reference design
