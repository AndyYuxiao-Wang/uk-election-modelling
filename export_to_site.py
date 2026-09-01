"""
Copies this repo's pipeline/clustering outputs (web/data, web/maps) into the
site repo's app so the live election map picks up new results.

Only copies data/ and maps/ - never css/ or js/, which belong to the site
repo's own app code, not to pipeline output.

Usage:
    py export_to_site.py [path-to-site-repo]

If no path is given, defaults to ../website (this repo and the site repo
cloned as siblings).
"""
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SITE_REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT.parent / "website"
APP_DIR = SITE_REPO / "site" / "app"

if not APP_DIR.is_dir():
    sys.exit(
        f"Couldn't find {APP_DIR}\n"
        f"Pass the site repo's path explicitly: py export_to_site.py <path-to-website-repo>"
    )

for name in ("data", "maps"):
    src = REPO_ROOT / "web" / name
    dst = APP_DIR / name
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"Copied {src} -> {dst}")

print("Done. Review the diff in the site repo and commit if it looks right.")
