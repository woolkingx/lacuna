---
number: 102
directory: browser
module: jumplist
status: prefs_only
patch_file: none
last_updated: 2026-04-14T00:00:00
patch_created: 2026-04-14
---

# 102-browser-jumplist

## Summary

`browser/modules/WindowsJumpLists.sys.mjs` — Windows taskbar right-click menu (JumpList).

Disabled `frequent` and `recent` sub-features because they read browsing history in a
background timer and expose it to the Windows `ICustomDestinationList` API without user
interaction. Retained `tasks` (static shortcuts only, no history access).

## How It Works

```
startup()
  → _updateTimer()  repeating timer (default: refreshInSeconds interval)
  → notify() on each tick
    → update()
      → Builder.buildList()
          → checkForRemovals()      # URLs removed by user in JumpList → deleted from Places history
          → [frequent] SELECT from moz_places ORDER BY visit_count DESC
              → obtainAndCacheFaviconAsync(uri)  # local favicon DB lookup only, no network
          → populateJumpList()      # writes to Windows ICustomDestinationList API
```

## Sub-features

| Pref | Behavior | Privacy Risk |
|------|----------|--------------|
| `frequent.enabled` | Background timer reads moz_places history by visit_count, queries favicon DB | High: background history read |
| `recent.enabled` | Recently visited sites list | High: background history read |
| `tasks.enabled` | Static shortcuts: New Tab, New Window, Private Window | None: no history access |

**Master switch**: `browser.taskbar.lists.enabled = false` stops the timer entirely.

## Side Effect: Bidirectional History Access

User right-clicks a JumpList item and removes it → `_clearHistory()` → **deletes the URL
from Places browser history**. JumpList is a two-way entry point into Places history.

## Favicon Warn Spam (upstream bug)

When `frequent` is enabled and favicon DB has no match for a URL, `CacheFavicon` returns
`NS_ERROR_FAILURE` without writing a disk sentinel. Every timer tick retries the same URLs:

```
WindowsJumpLists: Failed to fetch favicon for https://github.com/ NS_ERROR_FAILURE
```

Root cause: `FetchIconPerSpec` does exact `page_url` match against `moz_pages_w_icons`.
If the page-to-icon association is missing (e.g. redirect URL mismatch, or icon stored
under a different host), both the page-URL UNION and the `/favicon.ico` host UNION miss.
No sentinel is written on miss, so every refresh retries indefinitely.

Disabling `frequent.enabled` eliminates the spam entirely.

## Security Audit

**Problem**: `frequent` / `recent` run on a repeating timer, no user trigger required.
- Reads `moz_places` history
- Writes history subset to Windows `ICustomDestinationList` API (accessible to Windows OS)
- Violates Lacuna core principle: **background automatic = opaque = disable**

**Decision**:
- `frequent.enabled = false` — disabled, background history read
- `recent.enabled = false` — disabled, background history read
- `tasks.enabled = true` — retained, static list, no history access

Master switch kept `enabled = true` to preserve static task shortcuts.

## Patch Implementation

No patch required. Native prefs are sufficient.

## Changelog

### 2026-04-14 - Initial audit and prefs

**Issue**: `WindowsJumpLists: Failed to fetch favicon NS_ERROR_FAILURE` appearing repeatedly.
Investigation revealed background timer reads history and exposes it to Windows API.

**Findings**:
- Favicon warn is an upstream bug (DB miss with no sentinel), not a network request
- Core issue: `frequent` reads history in background and writes to Windows API
- Windows OS gains access to a subset of browsing history

**Decision**: Disable `frequent` + `recent`. Retain `tasks` (static, no privacy concern).

**Added**: `102-browser-jumplist-prefs.json`
