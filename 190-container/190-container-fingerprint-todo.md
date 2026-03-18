---
number: 190
directory: container
module: fingerprint
status: prefs_only
last_updated: 2026-03-18T00:00:00
analysis_date: 2026-01-09
---

# 190-container-fingerprint

## Conclusion

- Patch: none
- Prefs: 190-container-fingerprint-prefs.json
- Firefox native mechanisms fully support container-based fingerprint isolation via 5 prefs. Different containers produce different fingerprints within the same session. After restart, all containers get new fingerprints (privacy feature). No source patch needed.
