---
number: 112
directory: extensions
module: blocklist
status: patch_created
patch_file: 112-extensions-blocklist.patch
last_updated: 2026-03-13T02:30:00
patch_created: 2026-03-13
---

# 112-extensions-blocklist

## 功能說明

### MLBF（Multi-Level Bloom Filter）是什麼

MLBF 是 Firefox 的擴充套件黑名單機制，使用 Bloom Filter 資料結構儲存已知惡意或違規擴充套件的簽名。
Firefox 在啟動和 RemoteSettings 同步時會從 Mozilla 伺服器拉取最新的 MLBF 附件，並用它來判斷已安裝的擴充套件是否被封鎖。

### 運作流程

```
_updateMLBF()
  → this._client.get()        # 從 RemoteSettings 拉取 records
  → _fetchMLBF(record, ...)   # 根據 record 下載最新 MLBF 附件
      → _getMLBFData()        # 實際下載或使用快取/dump
          → attachments.download(record, { fallbackToDump: true })
```

觸發點：
- `_onUpdate()` (line 1160): RemoteSettings sync 事件觸發，呼叫 `_updateMLBF(true)`
- `getEntry()` (line 1200): 查詢擴充狀態時，若 `_stashes` 未初始化則呼叫 `_updateMLBF(false)`

### 為何禁用遠端更新

1. **Mozilla 可無聲封鎖擴充**：MLBF 遠端更新允許 Mozilla 在用戶不知情的情況下封鎖任何擴充套件。這違反了 Firebox 的透明性原則。
2. **背景自動連線**：`_onUpdate()` 由 RemoteSettings sync 事件觸發，完全在背景自動執行，沒有任何 UI 提示。
3. **政治風險**：Mozilla 的封鎖決定可能受到外部壓力（例如廣告商、政府）影響，用戶無從知悉。
4. **本地 dump 已足夠**：Firefox ESR 發行版本已包含完整的 MLBF dump（`addons-mlbf.bin`），提供基本封鎖保護，不需要持續遠端更新。

### 雙層控制設計

一個 pref `patch.extensions.blocklist.enabled` 控制兩層：

**Layer 1 — 整體機制（`_init()` 開頭）**：
- 將 `extensions.blocklist.enabled` 設為 false
- `gBlocklistEnabled = false` → 所有 blocklist 查詢（GfxBlocklist、ExtensionBlocklist）立即返回空結果
- Firefox 原生開關，影響整個 blocklist 機制

**Layer 2 — MLBF 遠端更新（`_fetchMLBF()` 開頭）**：
- 防止從 RemoteSettings 下載 MLBF 附件
- 返回現有快取資料 `{ mlbf: this._mlbfData, mlbfSoftBlocks: this._mlbfDataSoftBlocks }`
- 雙重保險：即使 Layer 1 被繞過，Layer 2 仍阻止遠端網路請求

### Fallback 行為

當 `patch.extensions.blocklist.enabled = false` 時：
- Layer 1：`extensions.blocklist.enabled` 被設為 false，整個 blocklist 機制停用
- Layer 2：`_fetchMLBF()` 立即返回現有快取，不發出網路請求
- 若 `_mlbfData` 為 null（首次啟動），返回 null → Firefox 使用 bundled dump

## Patch 實作

### 修改檔案

`toolkit/mozapps/extensions/Blocklist.sys.mjs`

### 插入點

**Hunk 1**：`_fetchMLBF()` 函數開頭（原始行 953）— MLBF 遠端更新 guard
**Hunk 2**：`_init()` 函數開頭（原始行 1462）— 整體 blocklist 機制 master switch

### Pref Guard 邏輯

**Hunk 1 — `_fetchMLBF()`**：
```javascript
// FIREBOX PATCH: Block remote MLBF updates, rely on local dump
if (!Services.prefs.getBoolPref("patch.extensions.blocklist.enabled", false)) {
  return {
    mlbf: this._mlbfData ?? null,
    mlbfSoftBlocks: this._mlbfDataSoftBlocks ?? null,
  };
}
// END FIREBOX PATCH
```

**Hunk 2 — `_init()`**：
```javascript
// FIREBOX PATCH: Master switch - disable entire blocklist mechanism
if (!Services.prefs.getBoolPref("patch.extensions.blocklist.enabled", false)) {
  Services.prefs.setBoolPref("extensions.blocklist.enabled", false);
}
// END FIREBOX PATCH
```

### 策略選擇理由

- Layer 1 攔截 `_init()`：在 Firefox 讀取 `gBlocklistEnabled` 前強制設 false，整體停用機制
- Layer 2 攔截 `_fetchMLBF()`：雙重保護，確保即使 blocklist 機制部分活躍也不發出遠端請求
- 兩層共用同一 pref `patch.extensions.blocklist.enabled`，一個開關控制全部

### 調用鏈

```
RemoteSettings sync event
  → ExtensionBlocklistMLBF._onUpdate()           [line 1160]
      → _updateMLBF(forceUpdate=true)            [line 1162]
          → this._client.get()                   [line 1003]
          → _fetchMLBF(mlbfRecord, ...)          [line 1045] ← PATCHED HERE
              → _getMLBFData()                   [line 955]
                  → attachments.download()       [line 935]

getEntry(addon)
  → _updateMLBF(forceUpdate=false)               [line 1200]
      → ... (same as above)
```

## 使用場景

### 隱私優先用戶

不希望 Firefox 在背景自動連線 Mozilla 伺服器，但仍需要基本的擴充套件封鎖保護（使用 bundled dump）。

### 離線環境

無網路連線時，Firefox 不會因為無法更新 MLBF 而產生錯誤，直接使用本地 dump。

## Security Audit

### 決策

禁用遠端 MLBF 更新，保留本地 dump 保護。

### Trade-off

| 面向 | 影響 |
|------|------|
| 隱私 | 消除背景自動連線，符合 Firebox 透明性原則 |
| 安全 | 封鎖資料庫不會即時更新，無法阻擋新發現的惡意擴充 |
| 穩定性 | 不影響現有功能，本地 dump 仍提供基本保護 |
| 可逆性 | 用戶可將 pref 設為 true 恢復遠端更新 |

### 結論

符合 Firebox 核心原則「所有背景網路連線必須由用戶明確操作觸發」。
MLBF 遠端更新無任何 UI 入口，依照決策流程應完全禁用。

## 變更記錄

### 2026-03-13 (2) - 改為總開關模式

- **修改**: 從單層 MLBF guard 改成雙層總開關
- **pref 更名**: `patch.extensions.blocklist.remote.enabled` → `patch.extensions.blocklist.enabled`
- **新增 Layer 1**: `_init()` 開頭加入 master switch，強制 `extensions.blocklist.enabled = false`
- **保留 Layer 2**: `_fetchMLBF()` guard 保留，更新 pref 名稱，作為雙重保護
- **決策**: 單層只擋遠端 fetch，Layer 1 確保整個 blocklist 機制（包括本地查詢）完全停用
- **影響**: 停用整個 blocklist 機制（GfxBlocklist + ExtensionBlocklist），不僅是 MLBF 遠端更新
- **檔案**:
  - `toolkit/mozapps/extensions/Blocklist.sys.mjs` (patch 已還原)
  - `112-extensions/112-extensions-blocklist.patch`
  - `112-extensions/112-extensions-blocklist-prefs.json`

### 2026-03-13 (1) - 初始實作

- **修改**: 在 `_fetchMLBF()` 開頭加入 pref guard
- **pref**: `patch.extensions.blocklist.remote.enabled` (default: false)
- **原因**: MLBF 遠端更新為背景自動網路連線，違反 Firebox 透明性原則
- **影響**: 停止從 RemoteSettings 下載 MLBF 附件，使用本地 bundled dump
- **檔案**:
  - `toolkit/mozapps/extensions/Blocklist.sys.mjs` (patch 已還原)
  - `112-extensions/112-extensions-blocklist.patch`
  - `112-extensions/112-extensions-blocklist-prefs.json`
