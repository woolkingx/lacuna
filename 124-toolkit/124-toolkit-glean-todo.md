---
number: 124
directory: toolkit
module: glean
status: patch_created
patch_file: 124-toolkit-glean.patch
last_updated: 2026-03-12T22:00:00
patch_created: 2026-03-12
---

# 124-toolkit-glean: Glean Telemetry Upload Disable

## 功能說明

Compile-time disable of Glean telemetry upload by unconditionally enabling the `glean_disable_upload` Rust feature flag in `gkrust-features.mozbuild`.

### 原始行為

Firefox only sets `glean_disable_upload` for non-official builds (`if not CONFIG["MOZILLA_OFFICIAL"]`). Official/release builds have Glean upload enabled at compile time.

### 修改後行為

`glean_disable_upload` is always enabled regardless of `MOZILLA_OFFICIAL`, ensuring Glean telemetry upload is disabled at the Rust/compile level for all builds.

### 技術細節

- **File**: `toolkit/library/rust/gkrust-features.mozbuild`
- **Mechanism**: Rust feature flag `glean_disable_upload` compiled into `gkrust`
- **Layer**: Compile-time (no runtime pref needed)
- **No prefs.json**: This is a build-system change, not a runtime pref

## Patch 實作

### 修改內容

Comment out the `MOZILLA_OFFICIAL` conditional, making `glean_disable_upload` unconditional:

```python
# Before:
if not CONFIG["MOZILLA_OFFICIAL"]:
    gkrust_features += ["glean_disable_upload"]

# After:
#if not CONFIG["MOZILLA_OFFICIAL"]:
gkrust_features += ["glean_disable_upload"]
```

### 影響範圍

- Only affects the build system feature flag selection
- No runtime behavior change needed
- Requires full rebuild after applying patch

## 變更記錄

### 2026-03-12 - Initial patch creation

- Created compile-time patch to unconditionally enable `glean_disable_upload`
- No prefs.json needed (compile-time only change)
- Targets ESR 140.1.0 source
