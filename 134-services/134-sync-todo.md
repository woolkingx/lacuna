---
number: 134
directory: services
module: sync
status: no_patch_needed
last_updated: 2026-03-18T00:00:00
security_audit: 2026-01-03
---

# 134-services-sync

## Conclusion

- Patch: none
- Prefs: none (controlled via FxAccounts disable)
- Sync depends entirely on FxAccounts. Disabling `identity.fxaccounts.enabled` blocks all Sync paths. Requires explicit user login; zero background activity when disabled. No patch needed.
