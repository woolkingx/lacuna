---
number: 102
directory: browser
module: urlbar-formfill
status: patch_created
patch_file: 102-browser-urlbar-formfill.patch
last_updated: 2026-03-12T22:30:00
patch_created: 2026-03-12
---

# 102-browser-urlbar-formfill

Makes URL bar's `addToFormHistory()` respect `browser.formfill.enable` setting.

## 功能說明

Firefox's URL bar saves search history via `UrlbarUtils.addToFormHistory()`. This method checks for empty values, private browsing mode, and excessive string length, but does **not** check `browser.formfill.enable`. When a user disables form fill via `about:config` or Privacy settings, the URL bar continues saving search history.

### 問題

- `browser.formfill.enable = false` should prevent all form history storage
- `FormHistory.enabled` (from `FormHistory.sys.mjs`) already reads this pref
- `addToFormHistory()` skips this check, creating inconsistent behavior

### 修正

Add `!lazy.FormHistory.enabled` to the existing early-return condition in `addToFormHistory()`. This is a one-line addition to an existing if-statement.

No custom `patch.*` pref needed -- this uses the existing Firefox preference `browser.formfill.enable`.

## Patch 實作

### 修改檔案

| File | Change |
|------|--------|
| `browser/components/urlbar/UrlbarUtils.sys.mjs` | Add `!lazy.FormHistory.enabled` check to `addToFormHistory()` |

### 攔截點

- **Method**: `UrlbarUtils.addToFormHistory()` (line ~1157)
- **Layer**: Trigger point (Layer 5) -- single entry point, simple guard
- **Mechanism**: Check `lazy.FormHistory.enabled` (reads `browser.formfill.enable` pref)

### 依賴

- `FormHistory` already imported as lazy module at line 21:
  ```javascript
  FormHistory: "resource://gre/modules/FormHistory.sys.mjs",
  ```
- `FormHistory.enabled` is a getter that reads `browser.formfill.enable`

### Patch 內容

```diff
+      !lazy.FormHistory.enabled ||
```

Added between `input.isPrivate ||` and `value.length >` in the existing condition block.

## 使用場景

1. User sets `browser.formfill.enable = false` in `about:config`
2. User types search in URL bar and submits
3. **Before patch**: Search term saved to form history despite setting
4. **After patch**: Search term not saved, respecting user preference

## Security Audit

- **Risk**: None -- adds a guard, does not remove any
- **Scope**: Single method, single condition addition
- **Pref**: Existing Firefox pref, not a custom pref
- **Behavior**: Consistent with how `browser.formfill.enable` works elsewhere in Firefox

## 變更記錄

### 2026-03-12 - Initial patch creation

- Created patch to add `!lazy.FormHistory.enabled` check to `addToFormHistory()`
- No prefs.json needed (uses existing `browser.formfill.enable`)
- Verified `FormHistory` already imported as lazy module (line 21)
- Patch applies cleanly with `git apply --check`
