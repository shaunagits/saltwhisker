"""Build the painted scene pieces in art/ from Shauna's keyed images.

Step 1, key each original (originals live in _private/, never committed):
  python3 tools/key-magenta.py --sprite cat.png      work/cat.png
  python3 tools/key-magenta.py --sprite pier-end.png work/pier-end.png
  python3 tools/key-magenta.py --sprite pier-mid.png work/pier-mid.png
  python3 tools/key-magenta.py --sprite lamp.png     work/lamp.png
  python3 tools/key-magenta.py --sprite bucket.png   work/bucket.png
Step 2:
  python3 tools/build-painted-art.py work art

The cat is split into four layers of the same size so they stack without offsets:
body, back ear, front ear and tail. Ears and tail are drawn behind the body, so their
roots hide under the hat and the rump when they rotate. The cut shapes below are in the
keyed cat image's pixels; if the cat art changes, redraw them (a grid overlay helps).

The pier is one long strip: two repeats of the middle section, then the end section,
cross-faded at the joins. Both sections share the same rail and deck rows.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

src, dst = sys.argv[1], sys.argv[2]
CAT_H = 406          # output height of the cat layers
LAMP_H = 700
BUCKET_H = 240


def load(name):
    return np.asarray(Image.open(f'{src}/{name}').convert('RGBA')).astype(float)


def poly_mask(shape, pts):
    m = Image.new('L', (shape[1], shape[0]), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return np.asarray(m).astype(float) / 255


def save(arr, path, h=None, q=88):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA')
    if h:
        im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    im.save(path, 'WEBP', quality=q, method=6)
    return im.size


# ---------- cat ----------
cat = load('cat.png')
r, g, b, a = (cat[..., i] for i in range(4))
yellow = ((r > 165) & (g > 125) & (b < 125) & (r - b > 70)).astype(float)
not_yellow = 1 - yellow

EAR_BACK = [(505, 0), (640, 0), (640, 140), (600, 192), (505, 197)]
EAR_FRONT = [(645, 0), (740, 0), (740, 92), (650, 108)]
TAIL = [(0, 380), (335, 380), (335, 860), (300, 905), (300, 950), (350, 955), (352, 1127), (0, 1127)]
TAIL_ROOT = [(330, 940), (440, 940), (440, 1115), (330, 1115)]   # copied, not removed: fills behind the body

ear_b = poly_mask(cat.shape, EAR_BACK) * not_yellow
ear_f = poly_mask(cat.shape, EAR_FRONT) * not_yellow * (1 - poly_mask(cat.shape, EAR_BACK))
tail = poly_mask(cat.shape, TAIL) * not_yellow
root = poly_mask(cat.shape, TAIL_ROOT) * not_yellow


def layer(mask):
    out = cat.copy()
    out[..., 3] = a * mask
    return out


body = layer(np.clip(1 - ear_b - ear_f - tail, 0, 1))
sizes = {}
sizes['body'] = save(body, f'{dst}/cat-body.webp', CAT_H)
save(layer(ear_b), f'{dst}/cat-ear-back.webp', CAT_H)
save(layer(ear_f), f'{dst}/cat-ear-front.webp', CAT_H)
save(layer(np.clip(tail + root, 0, 1)), f'{dst}/cat-tail.webp', CAT_H)
k = CAT_H / cat.shape[0]
print('cat layers', sizes['body'], '| scale from keyed image', round(k, 4))
print('  pivots in layer px: ear back', (round(585 * k), round(182 * k)), 'ear front', (round(690 * k), round(100 * k)),
      'tail', (round(345 * k), round(1010 * k)), 'eye', (round(735 * k), round(265 * k)), 'paw', (round(1050 * k), round(578 * k)),
      'feet', round(1120 * k))

# ---------- pier strip ----------
end = load('pier-end.png')
mid = load('pier-mid.png')
H = min(end.shape[0], mid.shape[0])
end, mid = end[:H], mid[:H]
P = 415                                   # piling spacing in the middle section
t0 = 159 + P // 2                         # start halfway between its first two pilings
tile = mid[:, t0:t0 + 3 * P]
END_CUT = 226                             # halfway between the end section's first two pilings
endp = end[:, END_CUT:]
B = 40                                    # cross-fade width at each join


def join(left, right):
    ramp = np.linspace(0, 1, B)[None, :, None]
    blend = left[:, -B:] * (1 - ramp) + right[:, :B] * ramp
    return np.concatenate([left[:, :-B], blend, right[:, B:]], axis=1)


strip = join(join(tile, tile), endp)
w = save(strip, f'{dst}/pier.webp', q=86)
print('pier strip', w, '| end section starts at strip x', strip.shape[1] - endp.shape[1],
      '| pier end at strip x', strip.shape[1] - (end.shape[1] - 1899))

# ---------- lamp and bucket ----------
print('lamp', save(load('lamp.png'), f'{dst}/lamp.webp', LAMP_H))
print('bucket', save(load('bucket.png'), f'{dst}/bucket.webp', BUCKET_H))
