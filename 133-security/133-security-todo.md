---
number: 133
directory: security
module: security
status: prefs_only
last_updated: 2026-03-18T00:00:00
---

# 133-security

## Conclusion

- Patch: none
- Prefs: 133-security-prefs.json
- TLS/SSL hardening prefs from Betterfox Securefox.js: disable 0-RTT (replay attack prevention), flag unsafe TLS negotiation as broken, disable CSP violation reporting (privacy).

## Changelog

### 2026-03-08 - Ported Betterfox Securefox.js security prefs

- `security.tls.enable_0rtt_data = false`
- `security.ssl.treat_unsafe_negotiation_as_broken = true`
- `security.csp.reporting.enabled = false`
