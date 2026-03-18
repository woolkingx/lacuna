---
number: 121
directory: media
module: media.gmp
category: media
last_updated: 2026-01-11
status: patch_created
security_audit: 2026-01-03
audit_result: patch_needed
patch_strategy: disable_centralized_collection
patch_file: 121-media-media-gmp.patch
patch_created: 2026-01-11
---

# 121-media-media-gmp - Changelog

## 結論

### 為什麼需要 Patch？
**符合原則**:
- ✅ **集中收集定義**: 固定 URL (Google, Mozilla)
- ✅ **自動觸發**: 啟動時自動、定時更新
- ⚠️ **原生參數足夠？**: 可以「關閉動作」但無法「關閉網路同時保留功能」
- ✅ **用戶選擇優先**: Patch 提供「功能啟用 + 網路停用」選項
**最終決策**: ⚠️ **需要 Patch** (但優先度較低)
**理由**:
1. 原生參數 **可以關閉動作** (`updateEnabled: false`, `eme.enabled: false`)
2. 但 Patch 提供 **額外價值**:
   - 用戶可啟用 DRM 功能但使用本地插件 (不更新)
   - 深度防禦: 即使用戶誤啟用，網路仍受控
   - 符合三層防禦策略
**優先度**: MEDIUM-LOW
- 原生參數已提供基本防護
- Patch 提供進階控制和用戶選擇
- 不如 RemoteSettings 或 taskbartabs 緊急
### Patch 檔案
**檔案名稱**: `121-media-media-gmp.patch` (待建立)
**目標檔案**:
- `toolkit/mozapps/extensions/GMPProvider.sys.mjs` (待確認)
- `toolkit/components/gmp/GMPInstallManager.sys.mjs` (待確認)
**參數設定**:
```json
{
  "patch.media.gmp.network": false,           // 網路控制 (預設停用)
  "media.gmp-manager.updateEnabled": false,   // 原生參數 (雙重保險)
  "media.eme.enabled": false,                 // EME 停用 (用戶可啟用)
  "media.gmp-gmpopenh264.enabled": false      // OpenH264 停用
}
```
**用戶模式**:
- **嚴格隱私** (預設): 全部停用
- **本地 DRM**: `patch.media.gmp.network: false` + `media.eme.enabled: true`
- **完整 DRM**: `patch.media.gmp.network: true` + `media.eme.enabled: true`
---
- patch: 121-gmp.patch
- prefs: 無
