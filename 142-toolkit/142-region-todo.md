---
number: 142
directory: toolkit
module: region
status: patch_created
patch_file: 142-region.patch
generated: 2026-02-10
last_updated: 2026-03-14T00:00:00
---

# 142-region - Summary

## TL;DR - 核心結論

- 這是依現有 patch/prefs 自動整理的結論草稿。
- 需要 patch：142-region.patch
- 待後續審查與補充原因說明。
- patch: 142-region.patch
- prefs: 無

## 變更記錄

### 2026-03-14 (1) - 修正 patch context 偏移

- **原因**: patch 無法 apply 到 firefox-esr，`toolkit/modules/Region.sys.mjs:225` context 不符
- **差異說明**: 原 patch 基於舊版源碼，`_fetchRegion()` 函數體簡短；firefox-esr 版本中該函數加入了 retry 邏輯、telemetry（`_retryCount`、`Glean.region`）和錯誤處理，導致 context 行不匹配
- **修正方式**: 在 firefox-esr 源碼對應位置手動套用 patch 邏輯（`_fetchRegion()` 開頭注入 FIREBOX PATCH block），重新 `git diff` 生成 patch，再 `git checkout` 還原源碼
- **驗證**: `git apply --check` 無錯誤輸出
- **patch 邏輯不變**: 若 `patch.browser.region.enabled=false`，設定 hardcoded region（`patch.browser.region.hardcoded`，預設 "US"）後直接 return，跳過網路偵測
