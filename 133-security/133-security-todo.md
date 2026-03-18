---
number: 133
directory: security
module: security
status: prefs_created
generated: 2026-02-10
last_updated: 2026-03-08T00:00:00
---

# 133-security - Summary

## TL;DR - 核心結論

- patch: 無
- prefs: 133-security-prefs.json

## 變更記錄

### 2026-03-08 - 移植 Betterfox Securefox.js 安全 prefs

來源：https://github.com/yokoffing/Betterfox/blob/main/Securefox.js

新增 3 個 pref：

| pref | 值 | 說明 |
|---|---|---|
| `security.tls.enable_0rtt_data` | `false` | 停用 TLS 1.3 0-RTT，防 replay attack |
| `security.ssl.treat_unsafe_negotiation_as_broken` | `true` | 舊式不安全 TLS negotiation 顯示壞鎖頭警告 |
| `security.csp.reporting.enabled` | `false` | 停用 CSP violation report 外傳（隱私） |
