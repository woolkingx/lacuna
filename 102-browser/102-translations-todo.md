---
number: 102
directory: browser
module: translations
category: translations
last_updated: 2026-01-17T00:00:00
status: module_disabled
priority: MEDIUM
audit_completed: 2026-01-09
patch_created: 2026-01-10
patch_file: 102-browser-translations.patch
audit_result: disabled_via_prefs
patch_strategy: disable_translations_enable
rationale: prevent_auto_network_requests_on_settings_load
note: "Disabled browser.translations.enable. Patch retained for future Lazy Load optimization."
---

# 142-toolkit-translations - Security Audit Report

## 結論（2026-01-10 修正）

**最終判斷**: ⚠️ **需要 PATCH**
**Patch 策略**: 延遲載入（lazy load）
- Settings 頁面載入時不自動載入語言列表
- 點擊 Settings 按鈕時才載入
- 不需要 pref 開關（功能完整保留，只是改變載入時機）
**Patch 位置**:
- `browser/components/preferences/main.js` - `initTranslations()`
---
**審查完成日期**: 2026-01-10（重構）
**審查者**: security-auditor (Claude Code)
**複查狀態**: 改用延遲載入策略
**Patch 檔案**: `102-browser-translations.patch`
**下次審查**: Firefox ESR 下個大版本或 Translations 重大更新
- patch: 102-translations.patch
- prefs: 102-translations-prefs.json
