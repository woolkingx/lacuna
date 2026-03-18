---
number: 102
directory: browser
module: browser.topsites
category: browser
last_updated: 2026-01-03
status: completed
patch_created: 2026-01-03
patch_strategy: disable_centralized_collection
security_audit: 2026-01-03
---

# 102-browser-browser-topsites - Changelog

## 新結論 (2026-01-03 更新) ✅

### ✅ **需要建立 patch**
**原因**：
1. **符合集中收集定義** - RemoteSettings CDN = 固定 URL
2. **多個網路出口** - 原生參數無法覆蓋所有路徑
3. **與 region 模式一致** - 相同模式應相同處理
4. **應關閉動作而非改空 URL**
---
- patch: 102-topsites.patch
- prefs: 無
