#!/usr/bin/env python3
"""
regenerate_patches.py — Regenerate all .patch files from current firefox-esr diff.

Reads existing patches to determine the file→patch mapping, then generates
fresh patches from `git diff HEAD` in the ESR tree.

Usage:
    python3 scripts/regenerate_patches.py          # regenerate all
    python3 scripts/regenerate_patches.py --dry     # show what would be done
"""

import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PATCH_DIR = SCRIPT_DIR.parent
ESR_DIR = PATCH_DIR.parent / "firefox-esr"
EXCLUDE_DIRS = {".cleanup", ".backup", "__pycache__"}

# Files handled by other stages (not patches)
SKIP_FILES = {
    "browser/locales/en-US/browser/preferences/preferences.ftl",
}

# Extra file→patch mappings for files not yet in any patch
EXTRA_MAPPINGS = {
    "browser/branding/official/configure.sh": "200-ui/200-ui-branding.patch",
    "config/create_rc.py": "200-ui/200-ui-branding.patch",
}

# When a file appears in multiple patches, prefer this one
PREFERRED_PATCH = {
    "modules/libpref/Preferences.cpp": "103-build/103-preferences.patch",
}

# Patches that become empty after merging shared files into preferred patch
MERGED_PATCHES = {
    "124-toolkit/124-toolkit-telemetry-default.patch",
}


def scan_existing_patches():
    """Scan existing .patch files to build file→patch mapping."""
    mapping = {}
    patches = sorted(
        f for f in PATCH_DIR.glob("**/*.patch")
        if not EXCLUDE_DIRS & set(f.relative_to(PATCH_DIR).parts)
    )

    for patch_path in patches:
        rel = str(patch_path.relative_to(PATCH_DIR))
        if rel in MERGED_PATCHES:
            continue
        content = patch_path.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'^diff --git a/(.*?) b/', content, re.MULTILINE):
            esr_file = m.group(1)
            if esr_file not in mapping:
                mapping[esr_file] = patch_path

    # Apply preferred patch overrides
    for esr_file, pref_rel in PREFERRED_PATCH.items():
        mapping[esr_file] = PATCH_DIR / pref_rel

    # Apply extra mappings
    for esr_file, patch_rel in EXTRA_MAPPINGS.items():
        if esr_file not in mapping:
            mapping[esr_file] = PATCH_DIR / patch_rel

    return mapping


def get_modified_files():
    """Get list of modified files in ESR tree."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=ESR_DIR, capture_output=True, text=True
    )
    return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]


def get_file_diff(filepath):
    """Get git diff for a single file."""
    result = subprocess.run(
        ["git", "diff", "HEAD", "--", filepath],
        cwd=ESR_DIR, capture_output=True, text=True
    )
    return result.stdout


def build_patch_contents(file_mapping, modified_files):
    """Build patch contents grouped by patch file."""
    patch_diffs = defaultdict(list)
    unmapped = []

    for esr_file in sorted(modified_files):
        if esr_file in SKIP_FILES:
            continue
        if esr_file in file_mapping:
            target = file_mapping[esr_file]
            diff = get_file_diff(esr_file)
            if diff.strip():
                patch_diffs[target].append(diff)
        else:
            unmapped.append(esr_file)

    return patch_diffs, unmapped


def main():
    dry = "--dry" in sys.argv

    if not ESR_DIR.exists():
        print(f"ERROR: {ESR_DIR} not found")
        sys.exit(1)

    print(f"=== Regenerate Patches {'(DRY RUN)' if dry else ''} ===")
    print(f"  Patch dir: {PATCH_DIR}")
    print(f"  ESR dir:   {ESR_DIR}")
    print()

    file_mapping = scan_existing_patches()
    print(f"  File mappings: {len(file_mapping)}")

    modified = get_modified_files()
    print(f"  Modified files in ESR: {len(modified)}")
    print()

    patch_diffs, unmapped = build_patch_contents(file_mapping, modified)

    written = 0
    for patch_path in sorted(patch_diffs.keys()):
        rel = patch_path.relative_to(PATCH_DIR)
        diffs = patch_diffs[patch_path]
        combined = "\n".join(diffs)

        if not dry:
            patch_path.write_text(combined, encoding="utf-8")

        file_count = len(diffs)
        print(f"  {'WOULD WRITE' if dry else 'WROTE'} {rel} ({file_count} files)")
        written += 1

    # Handle merged patches
    for merged_rel in sorted(MERGED_PATCHES):
        merged_path = PATCH_DIR / merged_rel
        if merged_path.exists():
            if not dry:
                merged_path.unlink()
            print(f"  {'WOULD DELETE' if dry else 'DELETED'} {merged_rel} (merged into preferred patch)")

    print(f"\n  {written} patches regenerated")

    if unmapped:
        print(f"\n  WARNING: {len(unmapped)} files not mapped to any patch:")
        for f in unmapped:
            print(f"    {f}")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
