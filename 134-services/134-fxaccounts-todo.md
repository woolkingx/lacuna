---
number: 134
directory: services
module: fxaccounts
status: no_patch_needed
last_updated: 2026-03-18T00:00:00
security_audit: 2026-01-03
---

# 134-services-fxaccounts

## Conclusion

- Patch: none
- Prefs: none (controlled via 134-identity-prefs.json)
- FxAccounts requires explicit user login; zero network activity when disabled. `identity.fxaccounts.enabled = false` shuts down the service completely, blocking all dependent services (Sync, Send Tab, Monitor). Single control point, no bypass paths. No patch needed.
