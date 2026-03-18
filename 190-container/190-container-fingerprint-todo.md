---
number: 190
directory: container-fingerprint
module: integration
status: prefs_only_no_patch_needed
prefs_file: 190-container-fingerprint-prefs.json
test_file: 190-container-fingerprint-test.md
analysis_date: 2026-01-09
---

# Container + Fingerprint Integration - Analysis & Implementation Record

## TL;DR - 核心結論

**✅ 不需要任何 patch！Firefox 原生機制已完美支持容器指紋隔離。**

只需配置 5 個 prefs 即可實現：
- 不同容器 = 不同指紋（同一 session 內）
- 重啟後 = 所有容器換新指紋（隱私特性，非 bug）

---
