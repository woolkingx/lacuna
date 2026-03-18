---
number: 113
directory: gfx
module: font-echo
status: patch_created
patch_file: 113-gfx-font-echo.patch
last_updated: 2026-03-12T23:30:00
patch_created: 2026-03-12
---

# 113-gfx-font-echo: Font Fingerprinting Echo Defense

## 功能說明

"Echo + whitelist" 反指紋策略：讓所有字體探測 API 回傳一致、可預測的結果，
使每台機器的字體指紋相同。

### 核心邏輯：四點防禦

| Point | 攔截目標 | 策略 | 檔案 |
|-------|----------|------|------|
| 1 | `document.fonts.check()` | 永遠回傳 true (echo) | `layout/style/FontFaceSet.cpp` |
| 2 | `GetFontList()` | 回傳固定 12 字體清單 | `gfx/thebes/gfxPlatformFontList.cpp` |
| 3 | `@font-face local()` | 找不到字體時回傳 Arial 替代 | `gfx/thebes/gfxUserFontSet.cpp` |
| 4 | `font.system.whitelist` | Firefox 內建白名單 pref | prefs-only (無 code 修改) |

### 為什麼叫 "Echo"

指紋網站透過 `document.fonts.check("12px SomeFont")` 逐一測試字體是否存在。
正常行為：已安裝 = true，未安裝 = false → 產生唯一指紋。
Echo 行為：全部回傳 true → 每台機器都「有」所有字體 → 指紋一致。

### 控制 Pref

- `patch.privacy.font.echo.enabled` (default: `false`)
  - `false` = echo 防護啟用（反指紋 ON）— 符合 Firebox 慣例
  - `true` = 正常瀏覽器行為（echo 關閉）
- `font.system.whitelist` — Firefox 內建功能，限制可見字體

### 運作流程

```
網站執行 document.fonts.check("12px Wingdings")
  → Point 1: FontFaceSet::Check() 直接 return true
  → 網站認為字體存在

網站透過 CSS 枚舉字體列表
  → Point 2: GetFontList() 回傳固定 12 字體
  → 所有機器回傳相同清單

網站用 @font-face { src: local("特殊字體") } 探測
  → Point 3: local() 找不到時回傳 Arial 替代
  → 不會 fallback 到 URL 下載（節省頻寬）

瀏覽器內部字體系統
  → Point 4: font.system.whitelist 限制可用字體
  → 底層 API 也只看到白名單字體
```

### 新穎之處

- 不需要 27MB 字體套件（Tor Browser 做法）
- 零維護成本 — 不需更新字體版本
- 四層防禦互補，涵蓋所有已知指紋向量

## 固定字體清單（12 字體）

跨平台可用，涵蓋 serif / sans-serif / monospace：

| 字體 | 類型 | 平台 |
|------|------|------|
| Arial | sans-serif | Win/Mac/Linux |
| Times New Roman | serif | Win/Mac/Linux |
| Courier New | monospace | Win/Mac/Linux |
| Georgia | serif | Win/Mac/Linux |
| Verdana | sans-serif | Win/Mac/Linux |
| Trebuchet MS | sans-serif | Win/Mac/Linux |
| Liberation Sans | sans-serif | Linux |
| Liberation Serif | serif | Linux |
| Liberation Mono | monospace | Linux |
| DejaVu Sans | sans-serif | Linux |
| DejaVu Serif | serif | Linux |
| DejaVu Sans Mono | monospace | Linux |

## Patch 實作

### Point 1: FontFaceSet::Check() echo

```
檔案: layout/style/FontFaceSet.cpp
位置: FontFaceSet::Check() 函數開頭
邏輯: if (!StaticPrefs::patch_privacy_font_echo_enabled()) return true;
```

在任何字體查詢之前直接 return true，跳過 FindMatchingFontFaces 和狀態檢查。

### Point 2: GetFontList() 固定清單

```
檔案: gfx/thebes/gfxPlatformFontList.cpp
位置: GetFontList() — AutoLock 之後
邏輯: 回傳硬編碼的 12 字體清單，排序後 return
```

攔截在 lock 取得之後、SharedFontList 查詢之前。

### Point 3: local() echo

```
檔案: gfx/thebes/gfxUserFontSet.cpp
位置: eSourceType_Local 分支 — whitelist 檢查處
邏輯: echo 啟用時，用 LookupLocalFont("Arial") 替代原始字體名
      找不到 Arial 時 fallback 到 "Liberation Sans"
```

改寫原有的 `if (!pfl->IsFontFamilyWhitelistActive())` 條件分支：
- echo 啟用：用 Arial 替代 → 有效字體 entry → 不觸發 URL 下載
- echo 關閉：保留原始邏輯

### Point 4: font.system.whitelist

```
Pref: font.system.whitelist
值: "Arial Times New Roman Courier New ..."
方式: prefs-only，無 code 修改
```

Firefox 內建功能，用空格分隔的字體名列表限制可見字體。

### StaticPrefs 基礎設施

此 patch 新增 "patch" pref group：
- `modules/libpref/moz.build` — 加入 `"patch"` 到 pref_groups
- `modules/libpref/init/StaticPrefList.yaml` — 新增 patch.* section

生成的 header: `mozilla/StaticPrefs_patch.h`
C++ accessor: `mozilla::StaticPrefs::patch_privacy_font_echo_enabled()`

## Security Audit

### 指紋防護效果

- `document.fonts.check()` — 全部 true → 無法區分
- `document.fonts.forEach()` — 受 whitelist 限制
- CSS `@font-face local()` — 全部回傳 Arial → 無法區分
- `getComputedStyle` font 探測 — 受 whitelist 限制
- Canvas 字體測量 — 只有白名單字體可用，測量結果一致

### 風險

- 部分網站依賴 `check()` 返回正確結果來決定 fallback 字體
  → 影響低：瀏覽器仍用實際安裝的字體渲染
- `local()` echo 用 Arial 替代可能造成排版差異
  → 可接受：優先考慮隱私保護

## 變更記錄

### 2026-03-12 - 初始建立

- 建立四點字體指紋防禦 patch
- Point 1: FontFaceSet::Check() echo true
- Point 2: GetFontList() 固定 12 字體清單
- Point 3: @font-face local() echo with Arial fallback
- Point 4: font.system.whitelist pref (built-in)
- 新增 "patch" pref group 到 moz.build + StaticPrefList.yaml
- Pref: `patch.privacy.font.echo.enabled` (false = echo active)
