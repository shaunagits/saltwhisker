"""Build Walter's expression heads in art/ from Shauna's face paintings.

Each face painting is the whole cat on magenta, generated from cat-puppet.png with only the
face changed. The head is cut with the same HEAD shape as cat-head.webp (minus the ears), so
a face layer drops straight onto the body in the game and the ears and hat line up.

Usage:
  python3 tools/build-faces.py _private/art-src art
    reads cat-puppet.png (the base) and walter-face-<name>.png for every name in FACES

Each face is keyed like the base, cropped to the base's crop box (the generator's crops drift
by a pixel or two), then lined up on the base by the coat and body (which do not change) and
saved as art/cat-face-<name>.webp at the same size as cat-head.webp. The script prints the
offset it found for each face; anything over a few pixels means the generator moved the cat
and that face should be redone.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

src, dst = sys.argv[1], sys.argv[2]
FACES = ['happy', 'proud', 'surprised', 'unimpressed', 'sad', 'grumpy', 'sleepy']
CAT_H = 406                   # same as build-painted-art.py
PAD = 6                       # same tight-crop margin as key-magenta.py --sprite
# Same shapes as build-painted-art.py, in the keyed base's pixels. Keep the two in step.
EAR_BACK = [(505, 0), (640, 0), (640, 140), (600, 192), (505, 197)]
EAR_FRONT = [(645, 0), (740, 0), (740, 92), (650, 108)]
HEAD = [(370, 0), (870, 0), (870, 330), (830, 362), (800, 398), (740, 418), (650, 424), (560, 430), (470, 440), (380, 446)]


def key(path):
    """Magenta key with spill removal, as key-magenta.py --sprite does, but not cropped."""
    im = np.asarray(Image.open(path).convert('RGB')).astype(float)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    k = np.clip(((r + b) / 2 - g - 60) / 120, 0, 1)
    alpha = 1 - k
    spill = np.clip(np.minimum(r, b) - g, 0, None) * k
    out = im.copy()
    out[..., 0] -= spill
    out[..., 2] -= spill
    out = np.clip(out, 0, 255)
    r2, g2, b2 = out[..., 0], out[..., 1], out[..., 2]
    tint = np.clip(np.minimum(r2, b2) - g2 - 12, 0, None) * (alpha < 0.98)
    out[..., 0] -= tint
    out[..., 2] -= tint
    return np.dstack([np.clip(out, 0, 255), alpha * 255])


def crop_box(rgba):
    m = rgba[..., 3] > 127
    ys, xs = np.where(m)
    return (max(0, ys.min() - PAD), min(m.shape[0], ys.max() + 1 + PAD),
            max(0, xs.min() - PAD), min(m.shape[1], xs.max() + 1 + PAD))


def poly_mask(shape, pts):
    m = Image.new('L', (shape[1], shape[0]), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return np.asarray(m).astype(float) / 255


def offset(base, face, box):
    """Shift (dx, dy) that best lines the face's body up with the base's, by brute force on a
    small window, comparing the alpha and the paint inside the coat area (rows below the head)."""
    t, b, l, r = box
    ref = base[t + 480:b - 60, l + 300:l + 950]
    best = (1e18, 0, 0)
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            cand = face[t + 480 + dy:b - 60 + dy, l + 300 + dx:l + 950 + dx]
            if cand.shape != ref.shape:
                continue
            d = np.abs(cand - ref).mean()
            if d < best[0]:
                best = (d, dx, dy)
    return best[1], best[2]


base = key(f'{src}/cat-puppet.png')
box = crop_box(base)
t, b, l, r = box
shape = (b - t, r - l)
ear_b = poly_mask(shape, EAR_BACK)
ear_f = poly_mask(shape, EAR_FRONT)
head = np.clip(poly_mask(shape, HEAD) - ear_b - ear_f, 0, 1)
k = CAT_H / shape[0]
size = (round(shape[1] * k), CAT_H)

for name in FACES:
    face = key(f'{src}/walter-face-{name}.png')
    dx, dy = offset(base, face, box)
    cut = face[t + dy:b + dy, l + dx:r + dx]
    if cut.shape[:2] != shape:
        print(name, 'skipped: the cat sits too close to the image edge')
        continue
    # the ears are not in the face layer: they turn on their own, so keep the base's ear pixels out
    cut = cut.copy()
    cut[..., 3] *= head
    im = Image.fromarray(np.clip(cut, 0, 255).astype(np.uint8), 'RGBA').resize(size, Image.LANCZOS)
    im.save(f'{dst}/cat-face-{name}.webp', 'WEBP', quality=88, method=6)
    print(f'cat-face-{name}.webp', im.size, '| offset', (dx, dy))
