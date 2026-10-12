"""Split Shauna's cloud sheet into one sprite per cloud.

The sheet is several clouds on magenta. This keys it like key-magenta.py --sprite, finds each
cloud as a connected blob (after a small blur so wispy bits stay with their cloud), crops each
one tight and saves art/cloud-1.webp, cloud-2.webp ... biggest first, each resized so its width
is at most 900 px. Prints each cloud's size. Tiny specks (under 1% of the sheet) are ignored.

Usage:
  python3 tools/build-clouds.py _private/art-src/clouds.png art
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
MAX_W = 900

im = np.asarray(Image.open(src).convert('RGB')).astype(float)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
key = np.clip(((r + b) / 2 - g - 60) / 120, 0, 1)
alpha = 1 - key
spill = np.clip(np.minimum(r, b) - g, 0, None) * key
out = im.copy()
out[..., 0] -= spill
out[..., 2] -= spill
out = np.clip(out, 0, 255)
r2, g2, b2 = out[..., 0], out[..., 1], out[..., 2]
tint = np.clip(np.minimum(r2, b2) - g2 - 12, 0, None) * (alpha < 0.98)
out[..., 0] -= tint
out[..., 2] -= tint
# The painted rim around each cloud is pink-lavender, not pure magenta, so the key leaves a
# purple halo. Clouds are white, cream and blue, never purple: fade out pinkish pixels that sit
# near the edge, and keep red from climbing far above green anywhere.
pink = np.clip(np.minimum(im[..., 0], im[..., 2]) - im[..., 1], 0, None)
edge = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(15))) < 250
alpha = alpha * np.where(edge, np.clip(1 - (pink - 2) / 24, 0, 1), 1)
# lavender at the rim (blue above green, red near green) turns into the clouds' own shadow blue,
# same brightness; white and blue pixels are left alone
lum = out.mean(axis=2, keepdims=True)
w = (np.clip((out[..., 2] - out[..., 1]) / 20, 0, 1) * np.clip((out[..., 0] - out[..., 1] + 20) / 20, 0, 1) * edge)[..., None]
out = out * (1 - w) + (lum + np.array([-30.0, -2.0, 32.0])) * w
out[..., 0] = np.minimum(out[..., 0], out[..., 1] + 10)
rgba = np.dstack([np.clip(out, 0, 255), alpha * 255]).astype(np.uint8)

solid = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))) > 40
labels, n = ndimage.label(solid)
sizes = ndimage.sum(solid, labels, range(1, n + 1))
order = np.argsort(-sizes)
k = 0
for idx in order:
    lab = idx + 1
    if sizes[idx] < solid.size * 0.01:
        continue
    ys, xs = np.where(labels == lab)
    t, b0, l, r0 = max(0, ys.min() - 8), min(solid.shape[0], ys.max() + 9), max(0, xs.min() - 8), min(solid.shape[1], xs.max() + 9)
    piece = rgba[t:b0, l:r0].copy()
    piece[..., 3] = piece[..., 3] * (labels[t:b0, l:r0] == lab)      # other clouds in the box stay out
    cloud = Image.fromarray(piece, 'RGBA')
    if cloud.width > MAX_W:
        cloud = cloud.resize((MAX_W, round(cloud.height * MAX_W / cloud.width)), Image.LANCZOS)
    k += 1
    cloud.save(f'{dst}/cloud-{k}.webp', 'WEBP', quality=86, method=6)
    print(f'cloud-{k}.webp', cloud.size)
print(k, 'clouds')
