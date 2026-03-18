---
number: 200
directory: ui
module: branding
status: patch_created
patch_file: 200-ui-branding.patch
last_updated: 2026-03-13T04:30:00
patch_created: 2026-03-13
---

# 200-ui-branding

## 功能說明

將 Firefox 官方品牌字串替換為 Firebox，適用於桌面版 (`browser/branding/official`)。

### 替換規則

| 原始值 | 替換值 | 說明 |
|--------|--------|------|
| `Firefox` | `Firebox` | 品牌短名稱 |
| `Mozilla Firefox` | `Firebox` | 品牌全名 |
| `Mozilla` | `Firebox` | vendor 名稱 |
| trademark notice | `{ "" }` | 清空商標聲明 |

**不替換**：技術性字串（`gecko`、`mozilla.org` URL、`syncBrandShortName=Firefox Sync`）

## Patch 實作

### 修改檔案

| 檔案 | 修改項目 |
|------|---------|
| `browser/branding/official/locales/en-US/brand.ftl` | 7 個字串替換 |
| `browser/branding/official/locales/en-US/brand.properties` | 3 個字串替換 |

### brand.ftl 修改

```
-brand-shorter-name = Firebox
-brand-short-name = Firebox
-brand-shortcut-name = Firebox
-brand-full-name = Firebox
-brand-product-name = Firebox
-vendor-short-name = Firebox
trademarkInfo = { "" }
```

### brand.properties 修改

```
brandShorterName=Firebox
brandShortName=Firebox
brandFullName=Firebox
```

## 使用場景

- 瀏覽器標題列顯示 "Firebox"
- about:dialog 顯示 Firebox
- 系統層級應用程式名稱
- 安裝程式品牌名稱

## 決策記錄

- `brand.dtd` 在 Firefox ESR 中已移除（modern locale 只用 `.ftl`）
- `syncBrandShortName=Firefox Sync` 保留不改，為技術服務名稱
- `trademarkInfo` 改為空字串 `{ "" }` 而非移除，保持 FTL key 存在避免 l10n 錯誤
- 僅修改 `official` branding，`nightly`/`unofficial`/`aurora` 不在 Firebox build 範圍

## 變更記錄

### 2026-03-13 - 建立 patch

- 建立 `200-ui-branding.patch`
- 修改 `browser/branding/official/locales/en-US/brand.ftl`：7 個字串
- 修改 `browser/branding/official/locales/en-US/brand.properties`：3 個字串
- 總計替換 10 個字串
</content>
</invoke>