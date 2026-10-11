"""Build the painted scene pieces in art/ from Shauna's keyed images.

Step 1, key each original (originals live in _private/, never committed):
  python3 tools/key-magenta.py --sprite cat.png      work/cat.png
  python3 tools/key-magenta.py --sprite pier-end.png work/pier-end.png
  python3 tools/key-magenta.py --sprite pier-mid.png work/pier-mid.png
  python3 tools/key-magenta.py --sprite lamp.png     work/lamp.png
  python3 tools/key-magenta.py --sprite bucket.png   work/bucket.png
Step 2:
  python3 tools/build-painted-art.py work art

The cat is split into same-size layers so they stack without offsets: body, head (with
hat), back ear, front ear and three tail pieces. Ears turn on the head, the head tilts on
the neck, and the tail bends at two joints. Tail pieces sit behind the body, ears behind
the hat, so every root stays hidden when a piece rotates. The cut shapes below are in the
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
# Head with hat (ears ride on it). Cut just above the collar; a strip of neck fur stays in
# the body too, so the head can tilt a few degrees without a gap opening under the chin.
HEAD = [(370, 0), (870, 0), (870, 330), (830, 362), (800, 398), (740, 418), (650, 424), (560, 430), (470, 440), (380, 446)]
NECK_BAND = [(560, 360), (835, 330), (835, 440), (560, 445)]
# Tail split in three along its length so it can bend: base, middle, tip. Each piece overlaps
# the one below by 20 px so the joins stay hidden while they turn.
TAIL_CUTS = (810, 620)                       # rows where base/middle and middle/tip meet

ear_b = poly_mask(cat.shape, EAR_BACK) * not_yellow
ear_f = poly_mask(cat.shape, EAR_FRONT) * not_yellow * (1 - poly_mask(cat.shape, EAR_BACK))
tail = np.clip(poly_mask(cat.shape, TAIL) * not_yellow + poly_mask(cat.shape, TAIL_ROOT) * not_yellow, 0, 1)
tail_only = poly_mask(cat.shape, TAIL) * not_yellow
head = np.clip(poly_mask(cat.shape, HEAD) - ear_b - ear_f, 0, 1)
neck = poly_mask(cat.shape, NECK_BAND) * not_yellow * head
rows = np.arange(cat.shape[0])[:, None] * np.ones((1, cat.shape[1]))


def layer(mask):
    out = cat.copy()
    out[..., 3] = a * mask
    return out


body = layer(np.clip(1 - ear_b - ear_f - tail_only - head + neck, 0, 1))
sizes = {}
sizes['body'] = save(body, f'{dst}/cat-body.webp', CAT_H)
save(layer(head), f'{dst}/cat-head.webp', CAT_H)
save(layer(ear_b), f'{dst}/cat-ear-back.webp', CAT_H)
save(layer(ear_f), f'{dst}/cat-ear-front.webp', CAT_H)
c1, c2 = TAIL_CUTS
save(layer(tail * (rows >= c1)), f'{dst}/cat-tail-1.webp', CAT_H)
save(layer(tail * (rows >= c2) * (rows < c1 + 20)), f'{dst}/cat-tail-2.webp', CAT_H)
save(layer(tail * (rows < c2 + 20)), f'{dst}/cat-tail-3.webp', CAT_H)
k = CAT_H / cat.shape[0]
P = lambda x, y: (round(x * k), round(y * k))
print('cat layers', sizes['body'], '| scale from keyed image', round(k, 4))
print('  pivots in layer px: ear back', P(585, 182), 'ear front', P(690, 100), 'head', P(650, 425),
      'tail base', P(345, 1010), 'tail joints', P(205, 810), P(225, 620), 'eye', P(735, 265), 'paw', P(1050, 578), 'feet', round(1120 * k))

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
