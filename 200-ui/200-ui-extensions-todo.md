---
number: 200
directory: ui
module: extensions
status: prefs_created
patch_file: ~
last_updated: 2026-03-13T04:00:00
patch_created: 2026-03-13
---

## 功能說明

透過 Firefox Enterprise Policy (`ExtensionSettings`) 強制安裝隱私保護 extensions。

**運作流程**：
1. Firefox 啟動時讀取 `distribution/policies.json`
2. 發現 `force_installed` 項目
3. 從 AMO 下載對應的 `.xpi` 並自動安裝
4. 使用者無法停用或移除這些 extensions

**不打包 .xpi 源碼**：直接指向 AMO 的 `latest.xpi` URL，由 Firefox 自行下載最新版本。優點是自動取得更新，缺點是首次安裝需要網路連線。

**prefs 說明**：
- `extensions.autoDisableScopes: 0` — 停用自動停用邏輯，確保 policy-installed extensions 不被 Firefox 自動停用
- `extensions.enabledScopes: 15` — 啟用所有 scope（1+2+4+8），允許從所有來源安裝 extensions

## 安裝清單

| Extension | AMO ID | AMO URL |
|-----------|--------|---------|
| Multi-Account Containers | `@testpilot-containers` | `https://addons.mozilla.org/firefox/downloads/latest/multi-account-containers/latest.xpi` |
| uBlock Origin | `uBlock0@raymondhill.net` | `https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi` |
| CanvasBlocker | `CanvasBlocker@kkapsner.de` | `https://addons.mozilla.org/firefox/downloads/latest/canvasblocker/latest.xpi` |
| Bitwarden | `{446900e4-71c2-419f-a6a7-df9c091e268b}` | `https://addons.mozilla.org/firefox/downloads/latest/bitwarden-password-manager/latest.xpi` |

## 注意事項

- **首次安裝需要網路連線**：extensions 從 AMO 下載，離線環境無法安裝
- **部署方式**：`distribution/policies.json` 必須複製到 Firefox 安裝目錄的 `distribution/` 資料夾
  - Linux: `/usr/lib/firefox/distribution/policies.json`
  - Windows: `C:\Program Files\Mozilla Firefox\distribution\policies.json`
  - macOS: `/Applications/Firefox.app/Contents/Resources/distribution/policies.json`
- **無 patch 檔案**：此模組只需要 `policies.json` + `prefs.json`，不需要修改 Firefox 源碼
- **policy 優先級**：`force_installed` extensions 使用者無法停用，適合強制隱私保護場景

## 變更記錄

### 2026-03-13 (1) - 初始實作

建立 `distribution/policies.json`，透過 Enterprise Policy 強制安裝 4 個隱私保護 extensions：
- Multi-Account Containers：容器隔離
- uBlock Origin：廣告/追蹤封鎖
- CanvasBlocker：Canvas fingerprinting 防護
- Bitwarden：密碼管理

建立 `200-ui-extensions-prefs.json`，設定 `extensions.autoDisableScopes` 和 `extensions.enabledScopes` 確保 policy extensions 正常啟用。
