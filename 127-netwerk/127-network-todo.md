---
number: 127
directory: netwerk
module: network
status: prefs_created
generated: 2026-02-10
last_updated: 2026-03-08T00:00:00
---

# 127-network - Summary

## TL;DR - 核心結論

- patch: 無
- prefs: 127-network-prefs.json

## 變更記錄

### 2026-03-08 - 移植 Betterfox Securefox.js 網路 prefs

來源：https://github.com/yokoffing/Betterfox/blob/main/Securefox.js

新增 1 個 pref：

| pref | 值 | 說明 |
|---|---|---|
| `network.IDN_show_punycode` | `true` | 顯示 punycode 原始格式，防 IDN homograph attack（如用相似字元偽造域名）|
