# Project status

Updated 2026-10-11.

## Where it stands

- **Live:** https://games.shauna.digital/saltwhisker/ (also https://saltwhisker.vercel.app, which needs a Vercel login). Every push to `main` deploys to production.
- **Games home page:** has a Saltwhisker card (dusk pier drawn in code, no caption by Shauna's choice). Route and card live in the `shaunagits/games` repo.
- **Gameplay, all working:** cast with a ping-pong power bar, waiting with fake nibbles, a bite window, reeling with tension, surges and fish tiring, 15 fish with cat-voice notes, the Tidebook journal, the dinner goal (4 points by 8 PM, streaks), a day and night clock (12 real minutes per game day), rain, fish of the day, a Sunday-only fish, `?debug` panel.
- **Look:** pixel pier, water and cat in front; Shauna's painted day sky, night sky, and day and night distant coast (village and lighthouse) behind. Dusk is code colors plus a tinted copy of the day coast. Lighthouse light pulses in code.
- **Not done:** cat detail pass, dusk paintings, title screen, seagull thieves, share card, sound, Shauna's fish drawings.
- **Design board** (private Claude artifact, "Saltwhisker Design Board", https://claude.ai/artifact/DFAqnAssi4nRfEHLxYccuQ): palette, fonts, art specs, the cat accessory comparison, key screens in portrait and landscape. It predates the painted backdrops, and its scene thumbnails only roughly match the game's camera.
- **Check run 2026-10-11:** careful playtest bot caught every fish tested (ids 1, 5, 7, 9, 14, 15), no page errors.

## Decisions

| Decision | Why |
| --- | --- |
| Pixel world for playing, paper and ink for the journal | Pixel art is quick to build in code. The journal is where Shauna's hand-drawn art shines. A fully hand-drawn 2D version is a later phase. |
| Hero is a cat fishing for his dinner (was a boy) | Gives every session a goal, and the cat's body gives readable cues: ears on a nibble, tail puff on a bite, crouch when the line is tight. |
| Tuxedo cat, yellow sou'wester with ear holes | Strong silhouette at 16 pixels. Yellow reads against day, dusk and night. Ear holes keep the nibble cue visible. Chosen over a neckerchief, which shrank to a stripe at phone size. |
| Name: Saltwhisker (was Tidebook) | No existing game, app or product found with that name. The journal keeps the Tidebook name. |
| Ocean pier setting | Shauna's pick. |
| Both portrait and landscape | Camera keeps a focus box (cat, rod, bobber) as large as fits and shows more world on the long side. Planned from the start so it costs little. |
| Camera zoomed in (focus box 72 world pixels) | First version showed the whole 200 pixel world and the cat was too small. Scale snaps to whole device pixels to avoid seams. Shauna (2026-10-11): do not zoom in further, fishing room is already tight. |
| Dinner: 4 points by 8 PM, 1 to 3 points per fish by size | A light daily goal. Missing dinner only resets the streak. Some fish are refused for comedy. |
| Strong fish surge and tire over time | Without surges a careful player never snapped the line. Without tiring, legendaries dragged on for 40 seconds or more. |
| Painted sky behind the pixel world (2026-10-10) | Puts Shauna's art in phase 1 without her drawing the cat. Water, pier and cat stay pixel because they animate. (Superseded in part: the night sky is now painted too, see below.) |
| Repo private during development, public later | Portfolio value. Private material lives in `_private/` and is never committed. |
| Painted night sky and day and night distant coast (2026-10-11) | Shauna made them from prompts. Coast images arrive on magenta and are keyed out, cropped and edge-faded in Python (see findings note). |
| Night coast lined up on the lighthouse, not the image edge (2026-10-11) | The night painting put the lighthouse in a different place than the day one. Aligning the lighthouse keeps the day to night fade from jumping; the village shifts a little, which reads as fine. |
| Distant coast shifted left (`FAR_RECT.x` 28) (2026-10-11) | Shauna wanted the lighthouse fully visible on phones in portrait. Done in code, no image changes. The village now sits behind the pier in portrait. |
| Distant coast scaled to 140 world pixels wide, edges faded (2026-10-11) | At full width it towered over the cat and the land stopped abruptly on wide screens. |
| Journal stays "Tidebook" (2026-10-11) | Shauna: keep for now. "The Menu" (refused fish stamped OFF THE MENU) and "Dinner Plate" were the alternatives discussed. |
| Home page card has no caption (2026-10-11) | Shauna's choice after seeing several options. |
| Background prompts kept style-neutral with an [ART STYLE] slot (2026-10-11) | Shauna wants to try several art styles. Layout rules stay fixed so any set drops in. Prompts are in the findings note. |
| Pixel stays for phase 1 because the cat must be drawn in code (2026-10-11) | Organic shapes built in code were rejected twice in 13 Beads. Fully illustrated (puppet cat in pieces animated in code) is possible and was discussed; not started. |

## Playtest numbers (bot)

Careful bot (decides every 120 ms): catches everything. Common fish about 5 to 10 seconds, legendaries 12 to 20 seconds.
Sloppy bot (every 260 ms, ignores surge cues): catches common and uncommon fish, snaps the line on most rare and legendary fish.

## Open questions for Shauna

1. Cat detail: A (same 16 pixel sprite, smarter shading) or B (half-size pixels across the whole game, cat 32 pixels in the same footprint)? Draw a before-and-after on the board first? Either way the cat must not get bigger on screen and the camera must not change.
2. Move to fully illustrated now (puppet cat, pier, water texture in one art style)? If yes, write the asset list and style-neutral prompts.
3. If several background style sets come in, add a switch to compare them in the game?
4. Phone playtest feedback: does the zoom feel right, does reeling feel fair?
5. Dusk paintings: prompts given, waiting on images.

See `_docs/TODO.md` for the ordered queue.
