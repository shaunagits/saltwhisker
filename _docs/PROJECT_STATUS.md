# Project status

Updated 2026-10-10.

## Where it stands

Playable greybox. Casting, waiting with fake nibbles, the bite window, reeling with tension, surges and fish tiring, the journal, the dinner goal, a day and night clock, rain, and a fish of the day all work. Fish and cat art are placeholders until Shauna's drawings arrive.

Design board (private Claude artifact, "Saltwhisker Design Board"): palette for day, dusk and night, fonts, art specs, the chosen cat look, and key screens in portrait and landscape.

## Decisions

| Decision | Why |
| --- | --- |
| Pixel world for playing, paper and ink for the journal | Pixel art is quick to build in code. The journal is where Shauna's hand-drawn art shines. A fully hand-drawn 2D version is a later phase. |
| Hero is a cat fishing for his dinner (was a boy) | Gives every session a goal, and the cat's body gives readable cues: ears on a nibble, tail puff on a bite, crouch when the line is tight. |
| Tuxedo cat, yellow sou'wester with ear holes | Strong silhouette at 16 pixels. Yellow reads against day, dusk and night. Ear holes keep the nibble cue visible. Chosen over a neckerchief, which shrank to a stripe at phone size. |
| Name: Saltwhisker (was Tidebook) | No existing game, app or product found with that name. The journal keeps the Tidebook name. |
| Ocean pier setting | Shauna's pick. |
| Both portrait and landscape | Camera keeps a focus box (cat, rod, bobber) as large as fits and shows more world on the long side. Planned from the start so it costs little. |
| Camera zoomed in (focus box 72 world pixels) | First version showed the whole 200 pixel world and the cat was too small. Scale snaps to whole device pixels to avoid seams. |
| Dinner: 4 points by 8 PM, 1 to 3 points per fish by size | A light daily goal. Missing dinner only resets the streak. Some fish are refused for comedy. |
| Strong fish surge and tire over time | Without surges a careful player never snapped the line. Without tiring, legendaries dragged on for 40 seconds or more. |
| Repo private during development, public later | Portfolio value. Private material lives in `_private/` and is never committed. |

## Playtest numbers (bot, 2026-10-10)

Careful bot (decides every 120 ms): catches everything. Common fish 4 to 10 seconds, legendaries 12 to 20 seconds.
Sloppy bot (every 260 ms, ignores surge cues): catches common and uncommon fish, snaps the line on most rare and legendary fish.

## Next

- Shauna reviews the greybox on her phone and the design board.
- Real art pass: refine the cat sprite and add more animation frames, journal page art.
- Shauna's fish drawings, then her Saltwhisker portrait for the title and journal cover.
- Title screen, seagull thieves, share card for a journal page.
- Sound, one layer at a time, once she wants it.
