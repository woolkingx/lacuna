---
number: 137
directory: storage
module: storage.places
category: storage
last_updated: 2026-01-11
status: completed
security_audit: 2026-01-03
audit_result: no_patch_needed
decision_reason: native_parameter_sufficient
---

# 137-storage-places - Security Audit Report

## 結論

### 最終決策
✅ **不需要 patch** - 移除 `patch.places.enabled` 參數
### 理由總結
1. **本地資料庫性質**:
   - Places 是本地 SQLite 資料庫
   - 無固定的資料收集伺服器
   - 主要操作都是本地查詢和儲存
2. **網路行為符合原則**:
   - Speculative Connect 只在用戶點擊時觸發
   - Favicon 下載是網頁載入的自然結果
   - Places 同步需要用戶明確登入
   - 所有網路行為都符合「用戶點擊原則」
3. **原生參數已足夠**:
   - `browser.places.speculativeConnect.enabled: false` 可停用預測性連線
   - 不是「改空 URL」而是「停止行為」
   - 符合 Patch 設計原則的最高標準
4. **無繞過路徑**:
   - 所有網路行為都需要用戶觸發
   - 無自動連線或背景同步
   - 無需額外 patch 防禦
5. **已由其他模組處理**:
   - Taskbar favicon: `patch.browser.taskbar.previews.favicon.network`
   - Places 同步: `identity.fxaccounts.enabled`
   - 無需重複實作
### 參數配置
**移除**:
```json
// 137-storage/137-storage-places-prefs.json (移除此檔案)
{
  "preferences": {
    "patch.places.enabled": false  // ❌ 移除（不需要）
  }
}
```
**保留原生參數**:
```json
// 102-browser/102-browser-browser-prefs.json (已存在)
{
  "preferences": {
    "browser.places.speculativeConnect.enabled": false  // ✅ 保留
  }
}
```
**Patch 檔案**: ❌ 不建立 `137-storage-places.patch`
---
- patch: 無
- prefs: 無
