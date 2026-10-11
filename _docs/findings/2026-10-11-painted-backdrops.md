# Painted backdrops: how they fit the game

2026-10-11. Read this before adding or replacing any backdrop painting.

## The question

How to put Shauna's paintings (made with an image generator from prompts) behind the pixel pier so they line up, change with the time of day, and work in portrait and landscape.

## What we settled

- **Paint only what does not move.** Sky and distant coast are images. Water, pier, cat, bobber, splashes, gulls and rain stay in code because they animate.
- **Two layers per time of day:** a full sky, and a distant coast on magenta that gets keyed out.
- **World mapping.** The game world is 200 by 200 world pixels with the sea starting at y 96. The sky image spans world x 10 to 210 (`SKY_RECT`), height from its aspect ratio, placed so 90% of the way down the image sits on y 96. The coast layer's bottom edge is the horizon and it is drawn 140 world pixels wide starting at `FAR_RECT.x` (28).
- **What each screen shows** (from the camera focus box x 78 to 150, y 52 to 124): phones in portrait see a narrow tall strip, about world x 78 to 150; phones in landscape see about x 36 to 192 and y 52 to 124. That is why the prompts ask for key elements between 40% and 60% across and below 55% down, and why the coast was moved left so the lighthouse shows in portrait.
- **Time of day.** Day painting fades out toward dusk (dusk keeps 25% of it so clouds show through the code colors), night painting fades in from dusk to night. Code stars and the code moon hide when the night painting shows. Rain lays a gray wash over whichever sky is up. Dusk coast is a tinted copy of the day coast, made once on load.
- **Day and night coasts must line up.** The generator moved the lighthouse in the night version (x 1156 instead of 1328 in a 1717 wide image, and shorter). It is aligned on the lighthouse lamp (`FAR_NIGHT_LAMP`), which keeps the fade from jumping; the village shifts slightly.

## Processing steps for a new coast image

1. Save the original into `_private/` (not committed) if you want to keep it.
2. Run `python3 tools/key-magenta.py <input.png> art/<name>.webp`. It keys, crops, fades the edges and prints the crop top and a lamp estimate.
3. Find the lighthouse lamp in the cropped image (printed estimate, or read the original and subtract the crop top). Day: `FAR_RECT.lamp`. Night: `FAR_NIGHT_LAMP`.
4. Sky images: save as JPEG quality 86 (`PIL Image.save(..., quality=86, optimize=True, progressive=True)`). About 110 to 190 KB each.
5. Screenshot portrait 390 by 844, landscape 844 by 390 and desktop at day, dusk and night (`__tb.setHour(11 | 18.2 | 22)`).

## Rejected or adjusted

- Coast at full 200 world pixel width: the lighthouse towered over the cat. Scaled to 140.
- Coast without edge fades: land stopped in a hard vertical line on wide screens.
- Pixel square sun at dusk in front of a painted sky looked wrong; with paintings loaded the code sun is a soft circle.

## The style-neutral prompts (given to Shauna 2026-10-11)

Replace [ART STYLE] with the same phrase in all six prompts of a set. Size 3000 by 1600 is ideal; any 15:8 image works (her first set was 1717 by 916). Keep the coast layout identical across day, dusk and night.

1. Day sky: "[ART STYLE] daytime sky, wide 15:8 image, 3000 x 1600 pixels, a background for a 2D game. A perfectly flat, straight ocean horizon line runs across the image 90% of the way down from the top; below that line, just continue the sky color (it will be covered by water). Clear blue sky, deeper at the top and paler and slightly misty near the horizon. Soft clouds grouped toward the upper left and upper right, leaving the middle more open. A soft sun about 66% of the way across and 50% of the way down. Keep the area from 40% to 55% across and 62% to 85% down calm, plain and low in contrast (a character stands in front of it). No land, no water, no birds, no people, no text, no border, no large areas of pure black or bright yellow."
2. Day far scenery: "[ART STYLE] distant coastline for a 2D game background, wide 15:8 image, 3000 x 1600 pixels, on a flat solid magenta background (#FF00FF) so it can be cut out. All land sits on one perfectly straight horizon line 86% of the way down from the top, with nothing at all below that line. On the left, from the left edge to about 40% across, a low hill with a small seaside village: a church tower and a cluster of houses among trees. From about 40% to 60% across, open horizon with no land. On the right, from about 60% across to the right edge, a grassy headland with rocky cliffs at the water, and a small red-and-white striped lighthouse with a little keeper's house at about 77% across. The lighthouse is about 16% of the image height. The tallest land reaches no higher than 60% of the way down. Daytime light, distant and slightly hazy, soft edges. No water, no sky, no birds, no people, no text."
3. Dusk sky: same frame as the day sky; violet to rose to apricot and gold, a large soft golden sun about 70% across half sunk into the horizon, wispy clouds lit pink and orange from below, a few faint first stars.
4. Dusk far scenery: same layout as day; a few village windows starting to glow, lighthouse lamp just switching on, land in warm plum and dusky purple lit from behind with soft rim light.
5. Night sky: same frame; deep indigo to dusky blue, scattered stars, faint Milky Way across the upper left, full moon with halo about 66% across and 48% down, thin dim clouds near the edges, cozy not spooky, no pure black.
6. Night far scenery: same layout as day; warm lit windows, lighthouse lamp glowing gold with a small halo and no beam (the beam is animated in code), land in deep blue and violet, moonlit on the top edges.

Styles suggested as best fits with the pixel foreground: flat mid-century travel poster, Japanese woodblock print, risograph print, storybook gouache (current), soft chalk pastel. Avoid photoreal, busy fantasy concept art, heavy black linework (a black cat disappears), neon or noir.

## Check before redoing

- Measure the horizon and lamp in any new image; generators drift from the requested positions.
- Keep total backdrop weight small (current four files are about 360 KB).
