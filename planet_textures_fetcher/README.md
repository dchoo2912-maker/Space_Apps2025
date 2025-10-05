
# images/ — High‑res Planet Textures (GitHub Pages Friendly)

This bundle contains an **empty `images/` folder plus ready-to-run scripts** that will download
CORS‑safe, high‑resolution JPG textures (≈2K each) from SolarSystemScope into the folder with
the exact filenames your code expects.

## Files
- `images/` (empty placeholder; textures will be downloaded here)
- `fetch_textures.sh` (macOS/Linux)
- `fetch_textures.ps1` (Windows PowerShell)
- `textures.json` (URL manifest — do not rename)

## Quick start

### macOS / Linux
```bash
chmod +x fetch_textures.sh
./fetch_textures.sh
```

### Windows (PowerShell)
Right‑click your Start button → **Windows PowerShell** and run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
./fetch_textures.ps1
```

After the script finishes, you will have:
```
images/
  mercury.jpg  venus.jpg   earth.jpg  moon.jpg  mars.jpg
  jupiter.jpg  saturn.jpg  uranus.jpg neptune.jpg
```

Commit and push this folder to GitHub and your GitHub Pages site will load same‑origin textures with no CORS issues.

## Notes
- Sources: SolarSystemScope free texture set (2K). You can swap URLs in `textures.json` if you prefer other sources.
- Keep each image under ~25 MB for smooth Git pushes (these are well under that).
