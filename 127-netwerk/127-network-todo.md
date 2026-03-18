---
number: 127
directory: netwerk
module: network
status: prefs_only
last_updated: 2026-03-18T00:00:00
---

# 127-netwerk-network

## Conclusion

- Patch: none
- Prefs: 127-network-prefs.json
- Network-level prefs (DNS, prefetch, speculative connections, IDN punycode display). Includes `network.IDN_show_punycode = true` from Betterfox Securefox.js to prevent IDN homograph attacks.

## Changelog

### 2026-03-08 - Ported Betterfox Securefox.js network prefs

- `network.IDN_show_punycode = true`
