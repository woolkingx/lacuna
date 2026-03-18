---
number: 121
directory: media
module: gmp
status: patch_created
patch_file: 121-gmp.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-01-11
security_audit: 2026-01-03
---

# 121-media-gmp

## Conclusion

- Patch: 121-gmp.patch
- Prefs: none
- GMP (Gecko Media Plugins) auto-downloads Widevine/OpenH264 from Mozilla/Google servers at startup and on timer. Native prefs can disable entirely, but patch adds granular control: users can keep DRM enabled locally while blocking network updates. Three user modes: strict privacy (all off, default), local DRM (no updates), full DRM (updates enabled).

## Changelog

### 2026-01-11 - Patch created

- Audit: automatic background downloads violate user-click principle
- Strategy: pref-gated network control in GMPProvider/GMPInstallManager
- Priority: MEDIUM-LOW (native prefs provide basic protection)
