cat > make_textures.py <<'EOF'
#!/usr/bin/env python3
# make_textures.py — downloads high-quality global maps when possible and ensures 2:1 JPGs
# Output: textures/*.jpg  (equirectangular, 2:1, sRGB)

import os, io, sys, urllib.request
# --- add these near the imports ---
from PIL import Image, ImageFile
Image.MAX_IMAGE_PIXELS = None              # allow large NASA/Wiki maps
ImageFile.LOAD_TRUNCATED_IMAGES = True     # be tolerant of partial streams

# ... keep your UA/http_open helpers the same ...

# --- replace your SOURCES dict with this one ---
SOURCES = {
    "earth.jpg": [
        "https://neo.gsfc.nasa.gov/archive/bluemarble/bmng/world_8km/world.topo.bathy.200412.3x5400x2700.jpg",
        # fallback mirrors
        "https://commons.wikimedia.org/wiki/Special:FilePath/Blue%20Marble%202002.png",
    ],
    "mars.jpg": [
        # 2k equirectangular (nice size; avoids DecompressionBomb)
        "https://commons.wikimedia.org/wiki/Special:FilePath/Solarsystemscope%20texture%202k%20mars.jpg",
        # 1 km/pixel version (still reasonable):
        "https://commons.wikimedia.org/wiki/Special:FilePath/Mars%20Viking%20MDIM21%201km%20plus%20poles.jpg",
    ],
    "moon.jpg": [
        "https://commons.wikimedia.org/wiki/Special:FilePath/LROC%20color%20poles%201k.jpg",
    ],
    "mercury.jpg": [
        "https://commons.wikimedia.org/wiki/Special:FilePath/Solarsystemscope%20texture%202k%20mercury.jpg",
        # enhanced color MDIS composite (large)
        "https://commons.wikimedia.org/wiki/Special:FilePath/Mercury%20MESSENGER%20MDIS%20Basemap%20EnhancedColor%20Mosaic%20Global%2032ppd.jpg",
    ],
    "venus.jpg": [
        # “surface” rendition (equirectangular)
        "https://commons.wikimedia.org/wiki/Special:FilePath/Solarsystemscope%20texture%208k%20venus%20surface.jpg",
        # smaller mirror if needed
        "https://commons.wikimedia.org/wiki/Special:FilePath/Venus%20magellan%20c3-mdir%20colorized%20global%20mosaic%201024.jpg",
    ],
    "jupiter.jpg": [
        "https://atmos.nmsu.edu/PDS/data/PDS4/co_iss_global-maps/browse/Browse_Cassini_ISS_Jupiter_global_map_4filters.png",
        # widely used map (large)
        "https://commons.wikimedia.org/wiki/Special:FilePath/Jupiter%20map%20by%20Askaniy.jpg",
    ],
    "saturn.jpg": [
        "https://atmos.nmsu.edu/PDS/data/PDS4/co_iss_global-maps/browse/Browse_Cassini_ISS_RGB_Saturn_global_color_map_original.png",
        "https://commons.wikimedia.org/wiki/Special:FilePath/Saturn%20map%20by%20Askaniy.png",
    ],
    "uranus.jpg": [
        "https://commons.wikimedia.org/wiki/Special:FilePath/Solarsystemscope%20texture%202k%20uranus.jpg",
    ],
    "neptune.jpg": [
        "https://commons.wikimedia.org/wiki/Special:FilePath/Solarsystemscope%20texture%202k%20neptune.jpg",
    ],
}

def download(url: str):
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            data = r.read()
        return Image.open(io.BytesIO(data)).convert("RGB")
    except Exception as e:
        print(f"  … failed {url} ({e.__class__.__name__}: {e})")
        return None

def pick_local(name: str):
    stem = os.path.splitext(name)[0]
    for ext in (".jpg",".jpeg",".png",".webp",".tif",".tiff"):
        p = os.path.join("textures_in", stem+ext)
        if os.path.isfile(p):
            try:
                im = Image.open(p).convert("RGB")
                print(f"  ✓ using local {p}")
                return im
            except Exception as e:
                print(f"  … local {p} unreadable ({e})")
    return None

def ensure_2to1(im: Image.Image) -> Image.Image:
    w, h = im.size
    target_ratio = 2.0
    ratio = w / h
    if abs(ratio - target_ratio) < 0.01:
        target_w = (w // 2) * 2
        target_h = target_w // 2
        if target_h <= h:
            x0 = (w - target_w)//2
            y0 = (h - target_h)//2
            return im.crop((x0, y0, x0+target_w, y0+target_h))
    if ratio > target_ratio:
        new_w = int(h * target_ratio)
        x0 = (w - new_w)//2
        return im.crop((x0, 0, x0+new_w, h))
    else:
        new_h = int(w / target_ratio)
        y0 = (h - new_h)//2
        return im.crop((0, y0, w, y0+new_h))

def save_jpg(im: Image.Image, out_path: str, max_w=8192, max_h=4096):
    w, h = im.size
    scale = min(max_w / w, max_h / h, 1.0)
    if scale < 1.0:
        im = im.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=92, optimize=True, progressive=True)

def main():
    made, missing = [], []
    for out_name, urls in SOURCES.items():
        print(f"* {out_name}")
        im = pick_local(out_name)
        if im is None:
            for u in urls:
                print(f"  → trying {u}")
                im = download(u)
                if im: break
        if im is None:
            print("  … no source available; drop a file into textures_in/ and re-run")
            missing.append(out_name)
            continue
        im2 = ensure_2to1(im)
        save_jpg(im2, os.path.join("textures", out_name))
        print(f"  ✓ wrote textures/{out_name}  ({im2.size[0]}×{im2.size[1]})")
        made.append(out_name)

    print("\nDone.")
    if made:   print("  Built:", ", ".join(made))
    if missing:print("  Missing:", ", ".join(missing), "\n  (place your own files in textures_in/ and re-run)")

if __name__ == "__main__":
    main()
EOF

