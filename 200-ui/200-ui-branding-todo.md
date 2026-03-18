---
number: 200
directory: ui
module: branding
status: patch_created
patch_file: 200-ui-branding.patch
last_updated: 2026-03-18T00:00:00
patch_created: 2026-03-13
---

# 200-ui-branding

## Conclusion

- Patch: 200-ui-branding.patch
- Prefs: none
- Replaces Firefox brand strings with Lacuna in `browser/branding/official/locales/en-US/`. 7 strings in brand.ftl + 3 in brand.properties = 10 total. Trademark notice cleared. Technical strings (gecko, syncBrandShortName) unchanged.

## Changelog

### 2026-03-13 - Initial creation

- brand.ftl: shorter/short/shortcut/full/product-name/vendor -> Lacuna, trademarkInfo cleared
- brand.properties: shorterName/shortName/fullName -> Lacuna
