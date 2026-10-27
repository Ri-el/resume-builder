#!/usr/bin/env python3
"""Center-crop a user-supplied photo to 5:6 portrait (no stretching) and save a 600x720 JPEG.
Usage: python3 scripts/prepare_photo.py in.jpg out.jpg
Never generate or retouch a face. Use only a photo the candidate supplied."""
import sys
from PIL import Image, ImageOps
src, dst = sys.argv[1], sys.argv[2]
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
w, h = im.size
if w < 600:
    print(f"WARNING: photo is only {w}px wide; ask for a sharper original.", file=sys.stderr)
target = 5 / 6
if w / h > target:            # too wide: crop sides
    nw = int(h * target); x0 = (w - nw) // 2; im = im.crop((x0, 0, x0 + nw, h))
else:                         # too tall: crop top/bottom (keep upper part for faces)
    nh = int(w / target); y0 = int((h - nh) * 0.25); im = im.crop((0, y0, w, y0 + nh))
im.resize((600, 720), Image.LANCZOS).save(dst, "JPEG", quality=92)
print("saved", dst)
