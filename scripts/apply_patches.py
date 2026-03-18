#!/usr/bin/env python3
"""
apply_patches.py — Apply all Lacuna patches to a clean firefox-esr tree.

Usage:
    python3 scripts/apply_patches.py              # full apply
    python3 scripts/apply_patches.py --dry        # dry run (check only)
    python3 scripts/apply_patches.py --stage 1,2  # run specific stages

Stages:
    1. Apply .patch files
    2. Copy resource files (UI, branding, icons)
    3. Append l10n strings
    4. Generate + copy prefs-template.js
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PATCH_DIR = Path(__file__).resolve().parent.parent
ESR_DIR = PATCH_DIR.parent / "firefox-esr"
EXCLUDE_DIRS = {".cleanup", ".backup", "__pycache__"}

# ---------------------------------------------------------------------------
# Stage 1: Apply patches
# ---------------------------------------------------------------------------

def find_patches():
    """Find all .patch files, sorted by directory number."""
    patches = sorted(
        f for f in PATCH_DIR.glob("**/*.patch")
        if not EXCLUDE_DIRS & set(f.relative_to(PATCH_DIR).parts)
        and not f.name.endswith(".disabled")
    )
    return patches


def apply_patches(dry=False):
    """Apply all .patch files to firefox-esr."""
    patches = find_patches()
    print(f"  Found {len(patches)} patches")

    failed = []
    for patch in patches:
        rel = patch.relative_to(PATCH_DIR)
        cmd = ["git", "apply", "--check" if dry else None, str(patch)]
        cmd = [c for c in cmd if c is not None]

        result = subprocess.run(
            cmd, cwd=ESR_DIR, capture_output=True, text=True
        )
        if result.returncode != 0:
            # Try with --3way for fuzzy matching
            if not dry:
                result2 = subprocess.run(
                    ["git", "apply", "--3way", str(patch)],
                    cwd=ESR_DIR, capture_output=True, text=True
                )
                if result2.returncode == 0:
                    print(f"  OK (3way) {rel}")
                    continue
            failed.append((rel, result.stderr.strip()))
            print(f"  FAIL {rel}")
        else:
            print(f"  OK   {rel}")

    if failed:
        print(f"\n  {len(failed)} patches failed:")
        for rel, err in failed:
            print(f"    {rel}: {err[:120]}")
    return len(failed) == 0


# ---------------------------------------------------------------------------
# Stage 2: Copy resource files
# ---------------------------------------------------------------------------

# (source relative to PATCH_DIR, dest relative to ESR_DIR)
RESOURCE_COPIES = [
    # Build config (Windows = default, Linux = mozconfig.linux)
    ("mozconfig", ".mozconfig"),
    ("mozconfig.linux", "mozconfig.linux"),
    # Pref pane UI
    ("200-ui/lacuna.inc.xhtml",
     "browser/components/preferences/lacuna.inc.xhtml"),
    ("200-ui/lacuna.js",
     "browser/components/preferences/lacuna.js"),
    ("200-ui/lacuna.css",
     "browser/themes/shared/preferences/lacuna.css"),
    ("200-ui/category-lacuna.svg",
     "browser/themes/shared/preferences/category-lacuna.svg"),
    # Distribution
    ("200-ui/distribution/policies.json",
     "distribution/policies.json"),
]

# Extensions: 200-ui/distribution/extensions/* → distribution/extensions/*
EXTENSIONS_DIR = "200-ui/distribution/extensions"
EXTENSIONS_DEST = "distribution/extensions"

# Branding icons: 200-ui/branding/* → browser/branding/official/*
BRANDING_DIR = "200-ui/branding"
BRANDING_DEST = "browser/branding/official"

# Rename map: src filename → dst filename (build system expects original names)
BRANDING_RENAME = {
    "lacuna.ico": "firefox.ico",
    "lacuna64.ico": "firefox64.ico",
}


def copy_resources(dry=False):
    """Copy resource files to firefox-esr."""
    copied = 0

    # Fixed resource copies
    for src_rel, dst_rel in RESOURCE_COPIES:
        src = PATCH_DIR / src_rel
        dst = ESR_DIR / dst_rel
        if not src.exists():
            print(f"  SKIP {src_rel} (not found)")
            continue
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        print(f"  COPY {src_rel} -> {dst_rel}")
        copied += 1

    # Branding files (root + subdirectories like content/)
    branding_src = PATCH_DIR / BRANDING_DIR
    if branding_src.is_dir():
        for f in sorted(branding_src.rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(branding_src)
            dst_name = BRANDING_RENAME.get(f.name, f.name)
            dst = ESR_DIR / BRANDING_DEST / rel.parent / dst_name
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
            print(f"  COPY {BRANDING_DIR}/{rel} -> {BRANDING_DEST}/{rel.parent / dst_name}")
            copied += 1

    print(f"  {copied} files copied")
    return True


# ---------------------------------------------------------------------------
# Stage 3: Append l10n strings
# ---------------------------------------------------------------------------

FTL_SOURCE = "200-ui/lacuna-l10n.ftl"
FTL_TARGET = "browser/locales/en-US/browser/preferences/preferences.ftl"
FTL_MARKER = "# --- Lacuna l10n start ---"


def append_l10n(dry=False):
    """Append lacuna l10n strings to preferences.ftl."""
    src = PATCH_DIR / FTL_SOURCE
    dst = ESR_DIR / FTL_TARGET

    if not src.exists():
        print(f"  SKIP {FTL_SOURCE} (not found)")
        return True
    if not dst.exists():
        print(f"  SKIP {FTL_TARGET} (not found)")
        return False

    dst_content = dst.read_text(encoding="utf-8")
    src_content = src.read_text(encoding="utf-8")

    # Already appended?
    if FTL_MARKER in dst_content:
        # Replace existing block
        idx = dst_content.index(FTL_MARKER)
        dst_content = dst_content[:idx].rstrip() + "\n"

    block = f"\n{FTL_MARKER}\n{src_content}\n"

    if not dry:
        dst.write_text(dst_content + block, encoding="utf-8")
    print(f"  Appended {FTL_SOURCE} -> {FTL_TARGET}")
    return True


# ---------------------------------------------------------------------------
# Stage 4: Generate prefs-template.js
# ---------------------------------------------------------------------------

def generate_prefs(dry=False):
    """Run generate_prefs.py."""
    script = PATCH_DIR / "scripts" / "generate_prefs.py"
    if not script.exists():
        print(f"  ERROR: {script} not found")
        return False

    cmd = [sys.executable, str(script)]
    if dry:
        cmd.append("--dry")

    result = subprocess.run(cmd, cwd=PATCH_DIR, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        return False
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

STAGES = {
    1: ("Apply patches",       apply_patches),
    2: ("Copy resources",      copy_resources),
    3: ("Append l10n",         append_l10n),
    4: ("Generate prefs",      generate_prefs),
}


def main():
    dry = "--dry" in sys.argv

    # Parse --stage 1,2,3
    stage_filter = None
    for arg in sys.argv[1:]:
        if arg.startswith("--stage"):
            idx = sys.argv.index(arg)
            if "=" in arg:
                stage_filter = [int(s) for s in arg.split("=")[1].split(",")]
            elif idx + 1 < len(sys.argv):
                stage_filter = [int(s) for s in sys.argv[idx + 1].split(",")]

    if not ESR_DIR.exists():
        print(f"ERROR: {ESR_DIR} not found")
        sys.exit(1)

    mode = "DRY RUN" if dry else "APPLY"
    print(f"=== Lacuna Patch Apply ({mode}) ===")
    print(f"  Patch dir: {PATCH_DIR}")
    print(f"  ESR dir:   {ESR_DIR}")
    print()

    ok = True
    for num, (name, func) in STAGES.items():
        if stage_filter and num not in stage_filter:
            continue
        print(f"--- Stage {num}: {name} ---")
        if not func(dry=dry):
            ok = False
            print(f"  Stage {num} had errors")
        print()

    if ok:
        print("=== All stages complete ===")
    else:
        print("=== Completed with errors ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
