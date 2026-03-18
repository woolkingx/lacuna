---
number: 200
directory: ui
module: pref-pane
status: planning
patch_file: 200-ui-pref-pane.patch
last_updated: 2026-03-13T02:30:00
patch_created: ~
---

# 200-ui-pref-pane — Firebox Preferences Pane

## 功能說明

在 `about:preferences` 側邊欄加入 **Firebox** tab，提供所有 `patch.*` prefs 的圖形化開關，不需進入 about:config。

參考：Konform Browser 的 `pref-pane-small.patch` + `librewolf.inc.xhtml` 設計。

### 技術架構

Firefox preferences 系統三層結構：
1. **XUL 聲明**（preferences.xhtml）— 側邊欄 category + #include 模板
2. **JS 模塊**（preferences.js）— `register_module("paneFirebox", gFireboxPane)`
3. **UI 模板**（firebox.inc.xhtml）— 實際的 checkbox/input 控件

patch 只需改 6 個地方（preferences.xhtml × 3、preferences.js × 1、jar.mn × 2、preferences.css × 1）。

### UI 結構（分類式）

```
about:preferences#firebox
├── 隱私防護
│   ├── 指紋混淆（patch.privacy.font.echo.enabled）
│   ├── FPP 完整覆蓋（privacy.fingerprintingProtection.overrides）
│   └── 表單歷史（browser.formfill.enable）
├── 網路攔截
│   ├── Telemetry（patch.telemetry.pingsender.enabled）
│   ├── URL 格式化（patch.privacy.urlformatter.enabled）
│   └── Addon Origin 模式（network.http.addonOriginBehavior）
├── 遠端設定
│   ├── RemoteSettings（patch.services.settings.enabled）
│   └── RS Fallback（patch.services.settings.fallback.enabled）
├── 擴充安全
│   ├── Blocklist（patch.extensions.blocklist.enabled）
│   └── 推薦（patch.browser.aboutaddons.discovery.enabled）
└── 搜尋
    └── 搜尋引擎過濾（patch.search.engines.enabled）
```

### 包含檔案

```
200-ui/
├── 200-ui-pref-pane-todo.md          ← 本文件
├── 200-ui-pref-pane.patch            ← 修改 Firefox 源碼（6 處）
├── firebox.inc.xhtml                  ← UI 模板
├── firebox.js                         ← 邏輯層（helper functions）
├── firebox.css                        ← 樣式
├── category-firebox.svg               ← 側邊欄圖示
└── preferences.ftl                    ← 多語言字符串
```

## Patch 實作

### 修改點清單

| 檔案 | 修改內容 |
|------|---------|
| `browser/components/preferences/jar.mn` | 加入 firebox.js 資源 |
| `browser/components/preferences/preferences.js` | 加入 `register_module("paneFirebox", gFireboxPane)` |
| `browser/components/preferences/preferences.xhtml` | 加入 category richlistitem + stylesheet + #include |
| `browser/themes/shared/jar.inc.mn` | 加入 firebox.css + category-firebox.svg |
| `browser/themes/shared/preferences/preferences.css` | 加入 category-firebox icon binding |

### 關鍵 JS Pattern

```javascript
// 單 pref bool 開關
setBoolSyncListeners("firebox-X-checkbox", ["patch.X.enabled"], [false]);

// 多 pref 同步（一個開關控多個）
setBoolSyncListeners("firebox-X-checkbox",
  ["pref.A", "pref.B"],
  [false,    false   ]
);
```

## 變更記錄

### 2026-03-13 (2) - 實作 generate-pref-pane.py

- 實作 `scripts/generate-pref-pane.py`：解析 prefs-template.js → 自動生成 4 個檔案
- 解析邏輯：掃描 `patch.*` prefs（排除 `patch.firebox.prefs.loaded` marker）+ 例外 non-patch prefs
- 生成結果：
  - `200-ui/firebox.inc.xhtml` — 8 section groupbox, 18 checkboxes, 3 text inputs, 21 prefs 全覆蓋
  - `200-ui/firebox-l10n.ftl` — 所有 l10n-id + tooltiptext
  - `200-ui/firebox.js` — gFireboxPane + setBoolSyncListeners 全自動生成
  - `200-ui/firebox.css` — 參考 librewolf.css 結構
- Section 分類（8 組，按優先順序）：
  1. Privacy Protection（2 prefs）
  2. Browser（7 prefs）
  3. Extension Security（5 prefs）
  4. Remote Settings（3 prefs）
  5. App Updates（1 pref）
  6. Search（1 pref）
  7. DOM（1 pref）
  8. Media（1 pref）
- 下一步：200-ui-pref-pane.patch（改 Firefox 源碼 6 處）

### 2026-03-13 (1) - 規劃

- 建立 200-ui 目錄
- 確認 UI 分類結構（4 大類：隱私防護 / 網路攔截 / 遠端設定 / 擴充安全 / 搜尋）
- 參考 Konform pref-pane 設計，採用分類式/tree 結構
- 下一步：實作 firebox.inc.xhtml + firebox.js + patch
