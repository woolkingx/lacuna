# Captive Portal Service - Security Audit

## Current Protection Status

### Layer 1: Native Parameter (ACTIVE)
```javascript
// all.js.patch line 5
pref("network.captive-portal-service.enabled", false);
```
Effect: Service never starts
### Layer 2: Empty URL (ACTIVE)
```javascript
// all.js.patch line 28-29
pref("captivedetect.canonicalURL", "");
pref("captivedetect.canonicalContent", "");
```
Effect: No URL to fetch even if service starts
### Layer 3: User Preference (CONFIGURABLE)
```javascript
// 127-netwerk-network-prefs.json
"patch.network.captive-portal-service.enabled": false,
"network.captive-portal-service.enabled": false
```
- patch: 無
- prefs: 無
