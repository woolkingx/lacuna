---
number: 124
directory: toolkit
module: pingsender
status: patch_created
patch_file: 124-toolkit-pingsender.patch
last_updated: 2026-03-12T22:30:00
patch_created: 2026-03-12
---

# 124-toolkit-pingsender

## 功能說明

Pingsender 是 Firefox 的獨立執行檔，在瀏覽器關閉後仍會被 spawn 出來發送 telemetry ping 到 Mozilla 伺服器。這違反了「用戶點擊原則」：沒有用戶操作，不應發出網路連線。

### 運作流程

1. Firefox 關閉時，`TelemetrySendImpl.submitPing()` 檢查 `usePingSender` option
2. 若啟用，呼叫 `_sendWithPingSender()` 將 ping 資料寫入磁碟
3. `runPingSender()` spawn `pingsender` (或 `pingsender.exe`) 執行檔
4. pingsender 在背景 POST ping 資料到 telemetry server，然後刪除本地檔案

### 決策分析

```
功能有網路連線？ → 是
├─ 有 UI 操作入口？ → 否（自動觸發，用戶不知情）
└─ 結論：完全禁用
```

pingsender 沒有任何 UI 操作入口。它是純背景自動行為，用於在 Firefox 關閉後偷偷發送 telemetry。符合「完全禁用」條件。

## Patch 實作

### 策略：pref guard + build/packaging 移除（雙層防護）

**Layer 1 — Runtime pref guard（`TelemetrySend.sys.mjs`）**

在 `runPingSender()` 函數開頭加入 pref 檢查，預設 `false`。
當 pref 為 false 時拋出 `NS_ERROR_NOT_IMPLEMENTED`，呼叫端 `_sendWithPingSender` 已有 try/catch 處理。

**Layer 2 — Build system 移除（`moz.build`）**

從 `DIRS` 移除 `pingsender` 子目錄，使 pingsender 執行檔不被編譯。

**Layer 3 — Packaging 移除（4 files）**

從以下打包清單移除 pingsender：
- `browser/installer/package-manifest.in` — 移除 `; [ Ping Sender ]` 整個區塊
- `python/mozbuild/mozbuild/artifacts.py` — 移除 LinuxArtifactJob 和 MacArtifactJob 中的 pingsender 引用
- `browser/app/macbuild/Contents/MacOS-files.in` — 移除 `/pingsender`
- `browser/installer/windows/nsis/shared.nsh` — 移除 `Push "pingsender.exe"`

### 修改檔案列表

| 檔案 | 修改內容 |
|------|---------|
| `toolkit/components/telemetry/app/TelemetrySend.sys.mjs` | pref guard on `runPingSender()` |
| `toolkit/components/telemetry/moz.build` | 移除 `DIRS = ["pingsender"]` |
| `browser/installer/package-manifest.in` | 移除 Ping Sender packaging section |
| `python/mozbuild/mozbuild/artifacts.py` | 移除 Linux + Mac artifact patterns |
| `browser/app/macbuild/Contents/MacOS-files.in` | 移除 `/pingsender` |
| `browser/installer/windows/nsis/shared.nsh` | 移除 `Push "pingsender.exe"` |

### Pref

| pref | default | 說明 |
|------|---------|------|
| `patch.telemetry.pingsender.enabled` | `false` | 控制 pingsender 是否可被 spawn |

## 使用場景

- **正常使用**：pingsender 不被編譯、不被打包、runtime 也被 pref guard 攔截
- **除錯**：設定 `patch.telemetry.pingsender.enabled = true` 可恢復 runtime 行為（但仍需自行編譯 pingsender 執行檔）

## Security Audit

- **風險**：pingsender 在瀏覽器關閉後仍能發送資料，用戶完全不知情
- **隱私**：telemetry ping 包含 client ID、系統資訊等
- **結論**：完全禁用。三層防護確保不會有 pingsender 行為

## 變更記錄

### 2026-03-12 (1) - 初始建立

- 建立 pingsender patch：pref guard + build removal + packaging removal
- 6 個檔案修改，三層防護
- pref `patch.telemetry.pingsender.enabled` 預設 `false`
