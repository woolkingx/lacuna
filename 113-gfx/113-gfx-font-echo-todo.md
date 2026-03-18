---
number: 113
directory: gfx
module: font-echo
status: patch_created
patch_file: 113-gfx-font-echo.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-12
---

# 113-gfx-font-echo

## Conclusion

- Patch: 113-gfx-font-echo.patch
- Prefs: 113-gfx-font-echo-prefs.json
- Four-point font fingerprinting defense. "Echo + whitelist" strategy makes all font probe APIs return consistent, predictable results so every machine looks identical. No 27MB font bundle needed (unlike Tor Browser). Pref: `patch.privacy.font.echo.enabled` (false = echo active).

## Patch Details

| Point | Target | Strategy | File |
|-------|--------|----------|------|
| 1 | `document.fonts.check()` | Always return true | `layout/style/FontFaceSet.cpp` |
| 2 | `GetFontList()` | Return fixed 12-font list | `gfx/thebes/gfxPlatformFontList.cpp` |
| 3 | `@font-face local()` | Fall back to Arial instead of missing font | `gfx/thebes/gfxUserFontSet.cpp` |
| 4 | `font.system.whitelist` | Built-in Firefox pref (no code change) | prefs-only |

Also adds "patch" pref group to `modules/libpref/moz.build` + `StaticPrefList.yaml`.

## Changelog

### 2026-03-12 - Initial creation

- Four-point defense covering all known font fingerprinting vectors
- Zero maintenance cost, no font bundle required
