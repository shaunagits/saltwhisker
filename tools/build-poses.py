"""Build Walter's painted key poses in art/ from Shauna's pose paintings.

Each pose painting (walter-pose-*.png, the whole cat on magenta, painted from cat-puppet.png as
the reference) is keyed, scaled to the sitting puppet's layer size and placed so his feet land
exactly where the puppet's feet are. The game cross-fades from the puppet into a pose at the
big moments (wind-up, cast, bite, reeling, landing) and back.

Usage:
  python3 tools/key-magenta.py --sprite _private/art-src/cat-puppet.png work/k-puppet.png
  python3 tools/key-magenta.py --sprite _private/art-src/walter-pose-cast.png work/k-cast.png   (and so on)
  python3 tools/build-poses.py work art

The generator kept the puppet's scale (the width across the paws matched within a few percent
for all five, 2026-10-12), so poses are not rescaled against the puppet, only lined up on the
feet: the bottom row and the toe of the front paw. Prints each pose's offset in layer px for
POSES in index.html. The paw (where the rod sits) is read off each painting by eye, in the
keyed puppet's pixels, and listed below.
"""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
CAT_H = 406
PUPPET_H = 1127                     # keyed puppet height; the layers are this scaled to CAT_H
k = CAT_H / PUPPET_H
# the gripping paw in each pose, keyed puppet pixels (after lining up on the feet)
PAW = {'windup': (44, 157), 'cast': (1238, 260), 'startle': (1016, 285), 'reel': (850, 644), 'triumph': (962, 96)}


def feet(a):
    op = a[..., 3] > 128
    rows = np.where(op.any(1))[0]
    bottom, top = rows.max(), rows.min()
    band = op[bottom - int((bottom - top) * 0.04):bottom + 1]
    return np.where(band.any(0))[0].max(), bottom


pup = np.asarray(Image.open(f'{src}/k-puppet.png').convert('RGBA'))
px, py = feet(pup)
for name in PAW:
    im = Image.open(f'{src}/k-{name}.png').convert('RGBA')
    fx, fy = feet(np.asarray(im))
    dx, dy = px - fx, py - fy                      # pose origin in keyed puppet pixels
    out = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    out.save(f'{dst}/cat-pose-{name}.webp', 'WEBP', quality=88, method=6)
    print(f"  {name}: {{ x: {dx * k:.1f}, y: {dy * k:.1f}, paw: [{PAW[name][0] * k:.0f}, {PAW[name][1] * k:.0f}] }},  size {out.size}")
