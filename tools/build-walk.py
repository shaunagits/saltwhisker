"""Build Walter's walking layers in art/ from Shauna's walk painting.

The walk painting (walter-walk-a.png, the cat mid-stride on magenta) is keyed like the other
sprites, then cut into same-size layers: body (head, hat, coat, torso), tail, and the four legs.
The legs swing around hip and shoulder pivots in code, the tail sways, so one painting gives a
walk cycle. Leg and tail roots are copied into the body too, so nothing opens up when a piece
turns. Layers are scaled so the hat is the same width as the sitting puppet's.

Usage:
  python3 tools/key-magenta.py --sprite _private/art-src/walter-walk-a.png work/walk.png
  python3 tools/build-walk.py work/walk.png work/cat.png art
    (work/cat.png is the keyed sitting cat, used only to match the hat size)

Prints the pivots, feet row and hat centre in layer px for WALKP in index.html. The cut shapes
below are in the keyed walk image's pixels; if the painting changes, redraw them (a grid helps).
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

walk_path, cat_path, dst = sys.argv[1], sys.argv[2], sys.argv[3]
OUT_H = 336

# cut shapes, keyed walk image pixels (1120 x 932 for the 2026-10-12 painting)
LEG_BACK_NEAR = [(130, 600), (340, 600), (340, 660), (280, 760), (190, 932), (20, 932), (20, 860), (90, 760)]
LEG_BACK_FAR = [(380, 640), (560, 640), (600, 780), (600, 932), (380, 932)]
LEG_FRONT_NEAR = [(700, 715), (850, 715), (1120, 850), (1120, 932), (960, 932), (850, 860), (770, 800), (700, 780)]
LEG_FRONT_FAR = [(610, 690), (760, 690), (790, 760), (770, 932), (620, 932), (600, 820)]
TAIL = [(0, 0), (330, 0), (330, 340), (390, 430), (330, 560), (180, 560), (180, 480), (0, 420)]
# roots stay in the body as well, so a turned piece never shows a hole
ROOTS = [[(200, 590), (345, 590), (345, 700), (200, 700)], [(380, 630), (570, 630), (570, 720), (380, 720)],
         [(690, 700), (860, 700), (860, 790), (690, 790)], [(600, 680), (770, 680), (770, 770), (600, 770)],
         [(260, 420), (400, 420), (400, 600), (260, 600)]]
PIVOTS = {'legBN': (280, 640), 'legBF': (470, 660), 'legFN': (770, 725), 'legFF': (690, 710), 'tail': (340, 520)}


def load(p):
    return np.asarray(Image.open(p).convert('RGBA')).astype(float)


def hat_width(a):
    r, g, b, al = (a[..., i] for i in range(4))
    yel = (r > 165) & (g > 125) & (b < 125) & (r - b > 70) & (al > 128)
    ys, xs = np.where(yel)
    top = ys < a.shape[0] * 0.33
    return xs[top].max() - xs[top].min(), (xs[top].mean(), ys[top].mean())


def poly_mask(shape, pts):
    m = Image.new('L', (shape[1], shape[0]), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return np.asarray(m).astype(float) / 255


walk = load(walk_path)
cat = load(cat_path)
shape = walk.shape[:2]
a = walk[..., 3]
r, g, b = walk[..., 0], walk[..., 1], walk[..., 2]
fur = 1 - ((r > 165) & (g > 125) & (b < 125) & (r - b > 70)).astype(float)   # the coat stays with the body
legBN = poly_mask(shape, LEG_BACK_NEAR) * fur
legFN = poly_mask(shape, LEG_FRONT_NEAR) * fur
legBF = poly_mask(shape, LEG_BACK_FAR) * (1 - legBN) * fur
legFF = poly_mask(shape, LEG_FRONT_FAR) * (1 - legFN) * fur
tail = poly_mask(shape, TAIL) * fur
roots = np.clip(sum(poly_mask(shape, r) for r in ROOTS), 0, 1)
body = np.clip(1 - legBN - legFN - legBF - legFF - tail + roots, 0, 1)


def save(mask, name):
    out = walk.copy()
    out[..., 3] = a * mask
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA')
    im = im.resize((round(im.width * OUT_H / im.height), OUT_H), Image.LANCZOS)
    im.save(f'{dst}/{name}.webp', 'WEBP', quality=88, method=6)
    return im.size


size = save(body, 'walk-body')
save(tail, 'walk-tail')
save(legBN, 'walk-leg-back-near')
save(legBF, 'walk-leg-back-far')
save(legFN, 'walk-leg-front-near')
save(legFF, 'walk-leg-front-far')

k = OUT_H / shape[0]
hw_walk, hc = hat_width(walk)
hw_cat, _ = hat_width(cat)
ys = np.where((a > 127).sum(axis=1) > 0)[0]
P = lambda xy: (round(xy[0] * k), round(xy[1] * k))
print('walk layers', size, '| scale from keyed image', round(k, 4))
# the sitting puppet is 16 world px for its keyed height; match the hat width to find the walk scale
world_per_layer = 16 / cat.shape[0] * (hw_cat / hw_walk) / k
print('  WALKP.k (world px per layer px)', round(world_per_layer, 5), '| hat ratio sitting/walk', round(hw_cat / hw_walk, 4))
print('  pivots in layer px:', {n: P(p) for n, p in PIVOTS.items()}, '| feet row', round(ys.max() * k), '| hat centre', P(hc))
