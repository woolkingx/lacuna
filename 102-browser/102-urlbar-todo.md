---
number: 102
directory: browser
module: browser.urlbar
category: browser
last_updated: 2026-01-17T21:00:00
status: simplified_remotesettings_only
patch_created: 2026-01-03
patch_updated: 2026-01-17
patch_strategy: remotesettings_dump_fallback
security_audit: 2026-01-03
---

# 102-browser-browser-urlbar - Changelog

## 統一結論

**為什麼不需要 patch？**
- ✅ **統一控制點**: 所有 urlbar 網路請求都透過 MerinoClient
- ✅ **原生參數足夠**: `browser.urlbar.merino.endpointURL: ""` 可完全阻止
- ✅ Line 156-157 明確檢查 endpointURL，若為空則不發送請求
- ✅ Weather 預設已停用 (featureGate: false)
- ✅ Geolocation 無獨立網路請求，依賴 Merino
**分析過程**:
1. 搜尋 urlbar 相關模組: WeatherSuggestions, GeolocationUtils, MerinoClient
2. 追蹤網路出口: MerinoClient.sys.mjs:288 fetch(url)
3. 找到控制機制: Line 155-157 檢查 merinoEndpointURL
4. 確認 Weather: 預設 featureGate: false (已停用)
5. 確認 Geolocation: 依賴 Merino，無獨立請求
6. 檢查原生參數: firefox.js 定義所有相關 pref
7. 結論: 設定 endpointURL = "" 可統一控制所有請求
**原結論 (2026-01-03)** - ❌ **錯誤！**:
- ❌ 假設原生參數足夠
- ❌ 遺漏 UrlbarSearchTermsPersistence RemoteSettings
- ❌ 錯誤判斷觸發機制為「用戶主動」
---
- patch: 無
- prefs: 無
