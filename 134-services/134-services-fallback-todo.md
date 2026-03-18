---
number: 134
directory: services
module: fallback
status: patch_created
patch_file: 134-services-fallback.patch
last_updated: 2026-03-12T00:00:00
patch_created: 2026-03-12
---

# 134-services-fallback - RS Forced Local Fallback

## TL;DR

When `patch.services.settings.fallback.enabled` is `false` (default), force RemoteSettings to always use local data:
- `fallbackToCache = true` and `fallbackToDump = true` in attachment downloads
- `LOAD_DUMPS` getter returns `true` unconditionally

This ensures Firefox uses cached/dump data for RS collections instead of fetching from remote servers.

## Patch 策略

### Konform 參考

Based on Konform `rs-local.patch` which unconditionally sets `fallbackToCache = true` and `fallbackToDump = true` in `#fetchAttachment`, and forces `LOAD_DUMPS` to `return (true || ...)`.

Firebox adaptation: pref-guarded (`patch.services.settings.fallback.enabled`) instead of unconditional, following Firebox's pref-guard pattern.

### 修改檔案

1. **`services/settings/Attachments.sys.mjs`** - `#fetchAttachment` method
   - After the `LOAD_DUMPS` check block (which may force `fallbackToDump = false`)
   - Override both `fallbackToCache` and `fallbackToDump` to `true` when pref disabled
   - Insertion point: after line 356 (`fallbackToDump = false;` block), before `const dumpInfo`

2. **`services/settings/Utils.sys.mjs`** - `LOAD_DUMPS` getter
   - At top of getter, before original logic
   - Return `true` immediately when pref disabled
   - Ensures dumps are always loaded regardless of `SERVER_URL`

### Pref

| pref | default | effect |
|------|---------|--------|
| `patch.services.settings.fallback.enabled` | `false` | When false: force local fallback. When true: use Firefox default behavior |

### 與現有 patch 的關係

- `134-utils.patch` modifies `SERVER_URL` getter and `LOAD_DUMPS` getter
- This patch also modifies `LOAD_DUMPS` -- both patches touch the same getter
- Apply order matters: if 134-utils.patch is applied first (replacing LOAD_DUMPS with unconditional `return true`), this patch's LOAD_DUMPS hunk becomes redundant but the Attachments.sys.mjs hunk remains essential
- If only this patch is applied, both hunks are needed

## 變更記錄

### 2026-03-12 - Initial creation

- Created patch for Phase 2b Konform integration
- Two-file patch: Attachments.sys.mjs + Utils.sys.mjs
- Pref-guarded forced fallback pattern
- Reference: Konform `rs-local.patch`
