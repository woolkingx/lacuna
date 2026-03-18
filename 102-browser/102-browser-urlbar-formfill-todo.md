---
number: 102
directory: browser
module: urlbar-formfill
status: patch_created
patch_file: 102-browser-urlbar-formfill.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 102-browser-urlbar-formfill

## Conclusion

- Patch: 102-browser-urlbar-formfill.patch
- Prefs: none (uses existing `browser.formfill.enable`)
- URL bar's `addToFormHistory()` ignores `browser.formfill.enable`, saving search history even when user disables form fill. Patch adds `!lazy.FormHistory.enabled` guard to the existing early-return condition. One-line fix for a Firefox consistency bug.

## Patch Details

- File: `browser/components/urlbar/UrlbarUtils.sys.mjs`
- Method: `addToFormHistory()` (~line 1157)
- Change: add `!lazy.FormHistory.enabled ||` to existing condition block
- `FormHistory` already imported as lazy module (line 21)

## Changelog

### 2026-03-12 - Initial patch creation

- One-line addition, applies cleanly
- No custom pref needed; respects existing `browser.formfill.enable`
