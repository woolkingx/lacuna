---
number: 134
directory: services
module: identity.fxaccounts
category: identity
last_updated: 2026-01-11
status: no_patch_needed
security_audit: 2026-01-03
audit_result: no_patch_needed
decision_reason: native_parameter_sufficient
---

# 134-services-identity-fxaccounts - Security Audit Report

## 結論

### 最終決策
✅ **不需要 patch** - `patch.identity.fxaccounts.enabled` 保留為「專案標記參數」
### 理由總結
1. **原生參數已足夠**:
   - `identity.fxaccounts.enabled: false` 可完全停用服務
   - 不是「改空 URL」而是「關閉動作」
   - 符合 Patch 設計原則的最高標準
2. **非自動觸發**:
   - 需要用戶明確登入 Firefox Account
   - 未登入時**完全無**網路活動
   - 不符合「需要 patch」的條件
3. **無繞過路徑**:
   - 所有認證功能依賴 FxAccounts 服務
   - 服務停用 = 所有路徑阻斷
   - 無需額外 patch 防禦
4. **用戶選擇優先**:
   - 保留參數讓用戶可以啟用 FxAccounts
   - 提供多種模式（停用/啟用/自建）
   - 尊重用戶的便利性需求
5. **依賴服務自動停用**:
   - FxAccounts 是認證基礎
   - 停用它 = 自動停用 Sync, Send Tab, Monitor 等
   - 單一控制點達成完整防護
### 參數配置
**現有配置** (保持不變):
```json
// 134-services/134-services-identity-prefs.json
{
  "description": "Privacy preferences for identity",
  "category": "identity",
  "directory": "134-services",
  "preferences": {
    "patch.identity.fxaccounts.enabled": false,  // ← 保留作為標記
    "identity.fxaccounts.enabled": false         // ← 原生參數控制
  }
}
```
**Patch 檔案**: ❌ 不建立 `134-services-identity-fxaccounts.patch`
---
- patch: 無
- prefs: 無
