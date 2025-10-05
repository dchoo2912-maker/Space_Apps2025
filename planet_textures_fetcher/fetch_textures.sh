#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
IMG_DIR="$ROOT/images"
MANIFEST="$ROOT/textures.json"
mkdir -p "$IMG_DIR"
command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 1; }

python3 - <<'PY'
import json, os, sys, urllib.request
from pathlib import Path
root = Path(__file__).resolve().parent
img_dir = root / "images"
manifest = root / "textures.json"
data = json.load(open(manifest, "r", encoding="utf-8"))
for name, url in data.items():
    out = img_dir / name
    print(f"Downloading {name} ...")
    with urllib.request.urlopen(url) as r, open(out, "wb") as f:
        f.write(r.read())
print("All textures downloaded to images/")
PY
echo "Done."
