---
number: 100
directory: custom
module: privacy-etp
status: prefs_created
patch_file: N/A
last_updated: 2026-03-08T00:00:00
prefs_created: 2026-01-18
---

# 100-custom-privacy-etp - Enhanced Tracking Protection 禁用配置

## TL;DR - 核心結論

- patch: 無
- prefs: 100-privacy-etp-prefs.json

## 變更記錄

### 2026-03-08 - 移植 Betterfox Securefox.js 隱私 prefs

來源：https://github.com/yokoffing/Betterfox/blob/main/Securefox.js

新增 2 個 pref：

| pref | 值 | 說明 |
|---|---|---|
| `privacy.globalprivacycontrol.enabled` | `true` | 發送 GPC (Global Privacy Control) header，告知網站不要出售用戶資料 |
| `privacy.antitracking.isolateContentScriptResources` | `true` | 隔離 content script 存取的資源，防跨站 tracking |
