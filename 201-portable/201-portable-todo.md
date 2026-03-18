---
number: 201
directory: portable
module: portable
category: portable
last_updated: 2026-03-14T00:00:00
status: patch_updated
security_audit: 2026-01-09
audit_result: patch_created
patch_created: 2026-01-11
patch_updated: 2026-01-18
patch_strategy: portable_mode_always_on
patch_file: 201-portable.patch
note: "Portable mode via GetUserDataDirectoryHome() - auto-create data/ with logging"
---

# 201-portable - Portable Mode Implementation

## TL;DR - 核心結論

- patch: 201-portable.patch
- prefs: 201-portable-prefs.json

## 變更記錄

### 2026-03-14 (1) - 修正 patch context 偏移，重建為 firefox-esr 140

**問題**: 原 patch 針對 firefox-release（已含 portable mode base code）生成 delta，
apply 到 firefox-esr 140 時 context 不匹配（行 1042 附近的 macOS FSRef 代碼）。

**原因**: 原 201-portable.patch 是 delta patch，只包含 logging printf 的增量修改，
假設目標源碼已有 portable mode 基礎邏輯。firefox-esr 為原始 Mozilla 源碼，無此基礎。

**修正**: 直接在 firefox-esr 源碼插入完整 portable mode 實作（基礎邏輯 + logging），
重新執行 `git diff > 201-portable.patch`，還原 esr 源碼後驗證 apply --check 通過。

**patch 變更**: 從 14 行 delta 擴展為 38 行完整插入，插入點 `GetUserDataDirectoryHome()`
函數開頭（`nsCOMPtr<nsIFile> localDir;` 後），邏輯內容不變。
