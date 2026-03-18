---
number: 154
directory: netwerk
module: addon-origin
status: patch_created
patch_file: 154-netwerk-addon-origin.patch
last_updated: 2026-03-12T23:00:00
patch_created: 2026-03-12
---

# 154-netwerk-addon-origin: Addon Origin Header Behavior

## 功能說明

### 問題：moz-extension UUID 追蹤向量

Firefox 為每個 extension 安裝產生唯一的 `moz-extension://<UUID>`。當 extension 發起 HTTP 請求時，`Origin` header 會攜帶這個 UUID：

```
Origin: moz-extension://a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

此 UUID 是：
- **持久性**：同一安裝下不變（除非重裝 extension）
- **唯一性**：每個 browser profile 不同
- **跨站追蹤**：任何接收到請求的 server 都能用此 UUID 關聯同一使用者的不同請求

這是一個被忽視但嚴重的隱私洩漏，等同於在每個 extension 請求中附帶 fingerprint。

### 解決方案：`network.http.addonOriginBehavior` pref

在 `nsHttpChannel::SetOriginHeader()` 中攔截 addon 請求的 Origin header，提供 4 種行為模式：

| 值 | 模式 | 說明 | 隱私 | 相容性 |
|----|------|------|------|--------|
| **0** | null origin | 設為 `Origin: null` | 最高 | 高（多數 server 接受） |
| 1 | strip | 完全移除 Origin header | 高 | 中（某些 CORS 可能失敗） |
| 2 | keep | Firefox 預設行為，UUID 直通 | 無保護 | 最高 |
| 3 | scramble | 每次請求產生隨機 UUID | 高 | 高（格式正確但不可追蹤） |

**預設值：0（null origin）** — 最安全且相容性最好的選擇。

### 為什麼 mode 0 是最佳預設

- `Origin: null` 是 HTTP 標準中定義的合法值（RFC 6454）
- 多數 server 已經處理 null origin（例如 privacy-redirected 請求）
- 不會觸發格式錯誤（不像 strip 可能讓某些嚴格的 CORS 實作困惑）
- 完全消除 UUID 洩漏

### 各模式適用場景

- **Mode 0 (null)**：一般使用者，最大隱私保護
- **Mode 1 (strip)**：進階使用者，願意接受極少數 CORS 破壞換取最小化 header fingerprint
- **Mode 2 (keep)**：需要完全相容（例如企業環境、extension 開發除錯）
- **Mode 3 (scramble)**：需要維持 moz-extension:// 格式但不想被追蹤（某些 extension 可能檢查 Origin 格式）

## Patch 實作

### 修改檔案

`netwerk/protocol/http/nsHttpChannel.cpp` — `SetOriginHeader()` 函數

### 兩條代碼路徑

`SetOriginHeader()` 有兩條處理 Origin 的路徑：

#### Path 1：已有 Origin header（existing header path）

當請求已經攜帶 Origin header 時觸發。

改動：
1. 將 `shouldNullifyOriginHeader` lambda 重構為 `getPossiblyNullOriginURI`
   - 原本返回 `bool`（是否該 null 化）
   - 改為返回 `already_AddRefed<nsIURI>`（返回 URI 或 nullptr）
   - nullptr 表示應 null 化，非 nullptr 表示保留
   - 需要 URI 來檢查 `moz-extension` scheme
2. 在 null-origin 邏輯之後、函數 return 之前插入 addon behavior switch
3. 透過 `existingHeader` 解析出 URI，判斷是否為 moz-extension scheme

#### Path 2：新建 Origin header（new header path）

當請求沒有 Origin header，函數從 triggeringPrincipal 建構一個新的。

改動：
1. 在 `GetWebExposedOriginSerialization()` 之後、CORS 檢查之前插入 addon behavior switch
2. 直接修改 `serializedOrigin` 變數（或提前 return）

### Switch 邏輯

兩條路徑使用相同的 switch 結構：

```cpp
switch (Preferences::GetUint("network.http.addonOriginBehavior", 0)) {
  case 3: // scramble — nsID::GenerateUUID() 產生隨機 UUID
  case 2: // keep — 不做任何修改
  case 1: // strip — ClearHeader 或 return（不設 header）
  case 0: // null — SetHeader("null")
}
```

Scramble 模式使用 `nsID::GenerateUUID()` + `ToProvidedString()` 產生格式正確的隨機 UUID，
剝去花括號後拼接為 `moz-extension://<random-uuid>`。

### Pref 說明

| Pref | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `network.http.addonOriginBehavior` | uint | 0 | 不是 patch.* pref — 因為是多模式 uint 而非 boolean toggle |

## Security Audit

### 威脅模型

- **威脅**：Server-side 收集 moz-extension UUID，建立跨站使用者 profile
- **攻擊面**：任何 extension 發起的 HTTP 請求（background fetch, content script XHR, etc.）
- **影響**：持久性 cross-site tracking identifier

### 緩解效果

- Mode 0：完全消除 UUID 洩漏，server 只看到 `Origin: null`
- Mode 1：Origin header 不存在，server 無從得知 extension 來源
- Mode 3：每次 UUID 不同，server 無法關聯不同請求

### 風險評估

- CORS 預檢（preflight）依賴 Origin header — mode 0/3 保留了有效的 Origin 值，不會破壞 CORS
- Mode 1 (strip) 可能在嚴格的 CORS server 上失敗，但這是使用者明確選擇的 trade-off
- Mode 2 保留完全相容性作為 escape hatch

## 變更記錄

### 2026-03-12 (1) - 初始建立

- 建立 addon origin header behavior patch
- 參考 Konform 的 `network.http.addonOriginBehavior` pref 設計
- 修改 `nsHttpChannel::SetOriginHeader()` 的兩條代碼路徑
- 重構 `shouldNullifyOriginHeader` → `getPossiblyNullOriginURI`（返回 URI 供 scheme 檢查）
- 使用 `nsID::GenerateUUID()` 實現 scramble 模式（不需要額外 include）
- 預設 mode 0（null origin）— 最安全且相容
