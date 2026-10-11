"""Turn a painted distant-coast image on a magenta (#FF00FF) background into a game layer.

Keys out the magenta with soft edges, removes magenta spill from edge pixels, crops to the
land (10 px margin above, bottom edge = horizon), fades the left 8% and right 16% so the land
dissolves into haze on wide screens, and saves a small WebP with transparency.

Usage:
  python3 tools/key-magenta.py path/to/far-night.png art/far-night.webp

Prints the lighthouse lamp position in the cropped image (bright yellow pixels), which goes in
FAR_NIGHT_LAMP or FAR_RECT.lamp in index.html. For a daytime image with no glowing lamp, read
the lamp position off the image by eye and subtract the crop top it prints.
"""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(float)
r, g, b = im[..., 0], im[..., 1], im[..., 2]

key = np.clip(((r + b) / 2 - g - 60) / 120, 0, 1)   # 1 = pure magenta
alpha = 1 - key
spill = np.clip(np.minimum(r, b) - g, 0, None) * key
out = im.copy()
out[..., 0] -= spill
out[..., 2] -= spill
out = np.clip(out, 0, 255)

rows = np.where((alpha > 0.5).sum(axis=1) > 0)[0]
top, bottom = max(0, rows.min() - 10), rows.max() + 1
rgba = np.dstack([out, alpha * 255]).astype(np.uint8)[top:bottom]

w = rgba.shape[1]
ramp = np.ones(w)
fr, fl = int(w * 0.16), int(w * 0.08)
ramp[w - fr:] = np.linspace(1, 0, fr) ** 1.5
ramp[:fl] = np.linspace(0, 1, fl)
rgba[..., 3] = (rgba[..., 3] * ramp[None, :]).astype(np.uint8)

Image.fromarray(rgba, 'RGBA').save(dst, 'WEBP', quality=88)
print('original size', im.shape[1], 'x', im.shape[0], '| crop top', top, '| layer height', rgba.shape[0])

yel = (r > 200) & (g > 170) & (b < 140) & (alpha > 0.5)
ys, xs = np.where(yel[:bottom])
if len(xs):
    print('bright yellow (lamp?) centroid in cropped image:', round(xs.mean()), round(ys.mean() - top),
          '(check: windows also count, so narrow to the lighthouse if needed)')
