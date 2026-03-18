#!/usr/bin/env python3
"""
generate-pref-pane.py
Parses prefs-template.js, extracts patch.* prefs, and generates:
  - 200-ui/lacuna.inc.xhtml
  - 200-ui/lacuna-l10n.ftl
  - 200-ui/lacuna.js
  - 200-ui/lacuna.css
"""

import json
import os
from datetime import datetime
from collections import OrderedDict
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "200-ui")
EXCLUDE_DIRS = {".cleanup", ".backup"}

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Section → display mapping (patch prefix → UI section)
# ---------------------------------------------------------------------------
SECTION_MAP = OrderedDict([
    ("patch.privacy.",          ("privacy",     "Privacy Protection")),
    ("patch.browser.",          ("browser",     "Browser")),
    ("patch.extensions.",       ("extensions",  "Extension Security")),
    ("patch.services.",         ("services",    "Remote Settings")),
    ("patch.telemetry.",        ("telemetry",   "Telemetry Protection")),
    ("patch.app.",              ("app",         "App Updates")),
    ("patch.search.",           ("search",      "Search")),
    ("patch.dom.",              ("dom",         "DOM")),
    ("patch.media.",            ("media",       "Media")),
    ("patch.network.",          ("network",     "Network")),
])

# Prefs to exclude from the UI (internal markers, not user-facing)
EXCLUDED_PREFS = {
    "patch.lacuna.prefs.loaded",
}

# Catch-all for prefixes not in SECTION_MAP
DEFAULT_SECTION = ("other", "Other")

# Extra non-patch.* prefs to include (pref_name → section_key)
EXTRA_PREFS = {
    "privacy.fingerprintingProtection.overrides": "privacy",
    "extensions.blocklist.enabled":              "extensions",
}

# ---------------------------------------------------------------------------
# Label generation helpers
# ---------------------------------------------------------------------------
LABEL_OVERRIDES = {
    "privacy.fingerprintingProtection.overrides":           "Fingerprinting Protection Overrides",
    "extensions.blocklist.enabled":                         "Extension Blocklist (Native Switch)",
}

# Non-patch prefs that have no description in prefs.json
TOOLTIP_OVERRIDES = {
    "privacy.fingerprintingProtection.overrides":
        "Customize which FPP targets are enabled/disabled. Format: +AllTargets,-CSSPrefersColorScheme (string pref).",
    "extensions.blocklist.enabled":
        "Native Firefox blocklist switch. Disables the entire blocklist mechanism including remote MLBF updates.",
}


def pref_to_slug(pref_name: str) -> str:
    """Convert pref name to a CSS/HTML slug."""
    return pref_name.replace(".", "-").replace("_", "-")


def pref_to_label(pref_name: str) -> str:
    if pref_name in LABEL_OVERRIDES:
        return LABEL_OVERRIDES[pref_name]
    # Strip patch. prefix and .enabled suffix, title-case words
    name = pref_name
    if name.startswith("patch."):
        name = name[len("patch."):]
    if name.endswith(".enabled"):
        name = name[: -len(".enabled")]
    parts = name.replace(".", " ").replace("_", " ").split()
    return " ".join(w.capitalize() for w in parts)


def pref_to_tooltip(pref_name: str, default_val, description: str = "") -> str:
    if description:
        return f"{description} Default: {default_val}."
    if pref_name in TOOLTIP_OVERRIDES:
        return TOOLTIP_OVERRIDES[pref_name]
    return f"Controls {pref_name}. Default: {default_val}."


def get_section(pref_name: str):
    for prefix, section in SECTION_MAP.items():
        if pref_name.startswith(prefix):
            return section
    return DEFAULT_SECTION


# ---------------------------------------------------------------------------
# Parse prefs-template.js
# ---------------------------------------------------------------------------
def parse_prefs():
    """
    Scan all *prefs.json files, extract patch.* prefs.
    Returns list of dicts:
      { name, default_value, description, section_key, section_label, is_bool }
    """
    entries = []
    seen = set()
    repo = Path(REPO_ROOT)

    files = sorted(
        f for f in repo.glob("**/*prefs.json")
        if not EXCLUDE_DIRS & set(f.parts)
    )

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  ERROR reading {path}: {e}")
            continue
        raw_prefs = data.get("preferences", {})
        for name, raw_val in raw_prefs.items():
            if not name.startswith("patch."):
                continue
            if name in seen or name in EXCLUDED_PREFS:
                continue
            seen.add(name)
            # Support dict format: {"value": ..., "description": ...}
            if isinstance(raw_val, dict) and "value" in raw_val:
                val = raw_val["value"]
                desc = raw_val.get("description", "")
            else:
                val = raw_val
                desc = ""
            section_key, section_label = get_section(name)
            entries.append({
                "name":          name,
                "default_value": val,
                "description":   desc,
                "section_key":   section_key,
                "section_label": section_label,
                "is_bool":       isinstance(val, bool),
            })

    # Append extra non-patch prefs
    for pref_name, section_key in EXTRA_PREFS.items():
        if pref_name in seen:
            continue
        seen.add(pref_name)
        section_label = next(
            (v[1] for k, v in SECTION_MAP.items() if v[0] == section_key),
            section_key.title()
        )
        entries.append({
            "name":          pref_name,
            "default_value": "",
            "description":   "",
            "section_key":   section_key,
            "section_label": section_label,
            "is_bool":       False,
        })

    return entries


# ---------------------------------------------------------------------------
# Group by section (preserving encounter order)
# ---------------------------------------------------------------------------
def group_by_section(entries):
    groups = OrderedDict()
    for e in entries:
        key = e["section_key"]
        if key not in groups:
            groups[key] = {"label": e["section_label"], "prefs": []}
        groups[key]["prefs"].append(e)
    return groups


# ---------------------------------------------------------------------------
# Generate lacuna.inc.xhtml
# ---------------------------------------------------------------------------
XHTML_HEADER = """\
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Auto-generated by scripts/generate-pref-pane.py
# {timestamp}
# DO NOT EDIT MANUALLY — re-run the script to regenerate.

<script src="chrome://browser/content/preferences/lacuna.js"/>

<html:template id="template-paneLacuna">

<hbox class="subcategory" hidden="true" data-category="paneLacuna">
  <html:h1 data-l10n-id="lacuna-header">Lacuna Privacy</html:h1>
</hbox>

"""

XHTML_FOOTER = """\

</html:template>
"""


def make_checkbox_id(pref_name: str) -> str:
    slug = pref_to_slug(pref_name)
    return f"lacuna-{slug}-checkbox"


def render_bool_row(entry) -> str:
    pref = entry["name"]
    slug = pref_to_slug(pref)
    cb_id = f"lacuna-{slug}-checkbox"
    label = pref_to_label(pref)
    tooltip = pref_to_tooltip(pref, entry["default_value"], entry.get("description", ""))
    l10n_id = f"lacuna-{slug}-checkbox"

    lines = [
        f'  <hbox>',
        f'    <checkbox id="{cb_id}"',
        f'              data-l10n-id="{l10n_id}"',
        f'              preference="{pref}"',
        f'              flex="1"',
        f'              tooltiptext="{tooltip}"/>',
        f'  </hbox>',
    ]
    return "\n".join(lines)


def render_string_row(entry) -> str:
    pref = entry["name"]
    slug = pref_to_slug(pref)
    input_id = f"lacuna-{slug}-input"
    label = pref_to_label(pref)
    tooltip = pref_to_tooltip(pref, entry["default_value"], entry.get("description", ""))
    l10n_id = f"lacuna-{slug}-input"

    lines = [
        f'  <hbox align="center">',
        f'    <label data-l10n-id="{l10n_id}-label">{label}</label>',
        f'    <html:input type="text"',
        f'                id="{input_id}"',
        f'                preference="{pref}"',
        f'                tooltiptext="{tooltip}"',
        f'                flex="1"/>',
        f'  </hbox>',
    ]
    return "\n".join(lines)


def render_section(section_key, section_info) -> str:
    group_id = f"lacuna-{section_key}-group"
    heading_l10n = f"lacuna-{section_key}-heading"
    heading_text = section_info["label"]

    rows = []
    for entry in section_info["prefs"]:
        if entry["is_bool"]:
            rows.append(render_bool_row(entry))
        else:
            rows.append(render_string_row(entry))

    rows_str = "\n\n".join(rows)

    return (
        f'<groupbox id="{group_id}" data-category="paneLacuna"\n'
        f'          class="indent" hidden="true">\n'
        f'  <label class="search-header">\n'
        f'    <html:h2 data-l10n-id="{heading_l10n}">{heading_text}</html:h2>\n'
        f'  </label>\n'
        f'  <vbox class="indent">\n\n'
        f'{rows_str}\n\n'
        f'  </vbox>\n'
        f'</groupbox>'
    )


def generate_xhtml(groups, timestamp) -> str:
    parts = [XHTML_HEADER.format(timestamp=timestamp)]
    for section_key, section_info in groups.items():
        parts.append(render_section(section_key, section_info))
        parts.append("")
    parts.append(XHTML_FOOTER)
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Generate lacuna-l10n.ftl
# ---------------------------------------------------------------------------
def generate_ftl(groups, timestamp) -> str:
    lines = [
        f"# Auto-generated by scripts/generate-pref-pane.py — {timestamp}",
        "# DO NOT EDIT MANUALLY.",
        "",
        "pane-lacuna-title = Lacuna",
        "lacuna-header = Lacuna Privacy Settings",
        "",
        "category-lacuna =",
        "    .tooltiptext = Lacuna Privacy & Security Settings",
        "",
    ]

    for section_key, section_info in groups.items():
        heading_l10n = f"lacuna-{section_key}-heading"
        lines.append(f"{heading_l10n} = {section_info['label']}")
        lines.append("")

        for entry in section_info["prefs"]:
            pref = entry["name"]
            slug = pref_to_slug(pref)
            label = pref_to_label(pref)
            tooltip = pref_to_tooltip(pref, entry["default_value"], entry.get("description", ""))

            if entry["is_bool"]:
                l10n_id = f"lacuna-{slug}-checkbox"
                lines.append(f"{l10n_id} =")
                lines.append(f"    .label = {label}")
                lines.append(f"    .tooltiptext = {tooltip}")
            else:
                l10n_id = f"lacuna-{slug}-input"
                lines.append(f"{l10n_id}-label = {label}")
                lines.append(f"{l10n_id} =")
                lines.append(f"    .placeholder = {pref}")
                lines.append(f"    .tooltiptext = {tooltip}")
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Generate lacuna.js
# ---------------------------------------------------------------------------
def generate_js(groups, timestamp) -> str:
    all_bool_prefs = []
    all_string_prefs = []
    for section_info in groups.values():
        for entry in section_info["prefs"]:
            if entry["is_bool"]:
                all_bool_prefs.append(entry["name"])
            else:
                all_string_prefs.append(entry["name"])

    pref_declarations = []
    for p in all_bool_prefs:
        pref_declarations.append(f'  {{ id: "{p}", type: "bool" }},')
    for p in all_string_prefs:
        pref_declarations.append(f'  {{ id: "{p}", type: "string" }},')

    pref_decl_str = "\n".join(pref_declarations)

    return f"""\
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */
//
// Auto-generated by scripts/generate-pref-pane.py — {timestamp}

/* import-globals-from preferences.js */

Preferences.addAll([
{pref_decl_str}
]);

var gLacunaPane = {{
  _pane: null,

  init() {{
    // Checkboxes use XHTML preference="" attribute for automatic
    // two-way binding. No manual sync listeners needed.
  }},
}};
"""


# ---------------------------------------------------------------------------
# Generate lacuna.css
# ---------------------------------------------------------------------------
def generate_css(timestamp) -> str:
    return f"""\
/* Auto-generated by scripts/generate-pref-pane.py — {timestamp} */
/* DO NOT EDIT MANUALLY. */

/* Lacuna pref-pane styles */

.lacuna-section-heading {{
  font-weight: bold;
  margin-block-start: 8px;
}}

/* Indent sub-items one level */
.lacuna-indent {{
  margin-inline-start: 24px;
}}

/* Warning/info labels */
.lacuna-warning {{
  display: inline;
  font-size: 0.8em;
  color: var(--text-color-deemphasized, GrayText);
}}

/* Icon for sidebar category */
#category-lacuna > .category-icon {{
  list-style-image: url("chrome://browser/skin/preferences/category-lacuna.svg");
}}
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[generate-pref-pane] Scanning *prefs.json in {REPO_ROOT}")

    entries = parse_prefs()
    groups = group_by_section(entries)

    # Stats
    print(f"[generate-pref-pane] Found {len(entries)} patch.* prefs")
    print(f"[generate-pref-pane] Sections ({len(groups)}):")
    for key, info in groups.items():
        print(f"  [{key}] {info['label']} — {len(info['prefs'])} prefs")

    # Write outputs
    outputs = {
        "lacuna.inc.xhtml":  generate_xhtml(groups, timestamp),
        "lacuna-l10n.ftl":   generate_ftl(groups, timestamp),
        "lacuna.js":         generate_js(groups, timestamp),
        "lacuna.css":        generate_css(timestamp),
    }

    for filename, content in outputs.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        with open(out_path, "w") as fh:
            fh.write(content)
        print(f"[generate-pref-pane] Wrote  {out_path}")

    # Preview first 50 lines of xhtml
    xhtml_path = os.path.join(OUTPUT_DIR, "lacuna.inc.xhtml")
    print("\n--- lacuna.inc.xhtml (first 50 lines) ---")
    with open(xhtml_path) as fh:
        for i, line in enumerate(fh, 1):
            if i > 50:
                break
            print(f"{i:3}: {line}", end="")
    print("\n--- end preview ---")


if __name__ == "__main__":
    main()
