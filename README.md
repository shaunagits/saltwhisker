# Saltwhisker

A painted fishing game for the browser. Saltwhisker, a tuxedo cat in a yellow sou'wester, fishes off the end of an ocean pier for his dinner and keeps a journal (the Tidebook) of everything he catches.

Play it at https://games.shauna.digital/saltwhisker/

## How a session works

1. **Cast.** Hold anywhere (or Space) to wind up. The power bar fills and falls back, so timing matters. Let go to cast. A short cast fishes close in, a long one fishes far out, and some fish only live at one depth.
2. **Wait.** A fish shadow swims toward the bobber. Saltwhisker's ears twitch on a nibble. Tapping on a nibble scares the fish off.
3. **Bite.** The bobber dips, his ears go up and his tail puffs. Tap within the bite window.
4. **Reel.** Hold to reel, let go to ease off. Keep the tension marker in the green. Too much tension snaps the line, too much slack lets the fish go. Strong fish surge (the rod jerks and the panel says "It is pulling!"), and every fish tires as the fight goes on.
5. **Catch.** A journal card shows the fish. New fish get a "NEW ENTRY" stamp, bigger ones get "NEW BEST".

**Dinner.** Each game day, Saltwhisker needs 4 dinner points before 8 PM. Bigger fish are worth more (1 to 3 points). Some fish he refuses to eat (the crab, anything wearing a hat, the legendaries). Fish caught after 8 PM are snacks. Make dinner every evening to build a streak.

**Time and weather.** One game day lasts 12 real minutes. Day, dusk and night each have their own fish. Some days it rains, which brings out rain-only fish. One "fish of the day" is the same for everyone on a calendar date and is more likely to bite. One fish only appears on real-world Sundays.

## Code layout

Everything is in `index.html`: canvas plus plain JavaScript, no build step, no dependencies besides Google Fonts. Asset paths must stay relative, because the game is served both at its own domain and under `/saltwhisker` on games.shauna.digital.

Sections inside the script, in order:

- `TUNE`: every tuning knob (clock speed, cast timing, bite window, reel and tension rates, dinner goal). Change numbers here, not in the logic.
- `FISH`: the 15 fish. Each has time of day, depth, weight (how often it bites), size range, strength, rarity, the cat's journal note, the hint shown before it's found, and optional `weather`, `sunday` or `refuse`.
- Save: local storage key `saltwhisker.save` (clock, weather, journal, dinner, streak).
- Camera: `CAM` is the focus box (cat, rod, bobber, near water). The game zooms so that box always fits and fills the rest of the screen with more world. Portrait shows more water, landscape shows more sea and sky.
- Saltwhisker sprite: `CAT_MAP` is the 16 by 16 sprite as text, one letter per color. `catPose()` and `catPixels()` add the ear, tail and crouch cues. At night a soft rim light keeps his outline readable.
- Draw, HUD, catch card, journal, debug panel, loop, playtest hooks.

## Testing

There is no test suite. Check changes with a playtest bot: Playwright plus the `window.__tb` hooks (`press`, `release`, `setHour`, `setWeather`, `reset`, `closeCard`, and the live state `S`). `tools/playtest-bot.js` plays several rounds per fish and reports catches, snaps and escapes:

```
node tools/playtest-bot.js index.html
```

Add `?debug` to the URL for a small panel to jump the clock, toggle rain, force a bite, or reset the save.

## Art

**Painted backdrops** live in `art/`, all by Shauna:

- `sky-day.jpg` and `sky-night.jpg`: full skies. Each is placed so its horizon (90% of the way down) sits on the sea. Day fades to the code's dusk colors, then the night painting fades in. Rain adds a gray wash.
- `far-day.webp` and `far-night.webp`: the distant village and lighthouse, cut out from a magenta background, cropped to their content, with soft faded side edges. The night painting has a slightly different layout, so it is lined up on the lighthouse (`FAR_NIGHT_LAMP`). Dusk uses a tinted copy of the day layer. The lighthouse light pulses in code at dusk and night.

To process a new coast image: `python3 tools/key-magenta.py input.png art/far-name.webp`. The full how-to, the screen-coverage math and the style-neutral prompts are in the local notes (`_private/findings/`, not committed). A dusk painting follows the same pattern in `drawPaintedSky` and `drawFar`.

**Painted scene pieces**, also Shauna's, each one daytime painting tinted in code for dusk and night (`P.tint`):

- `pier.webp`: one strip made of two repeats of the middle section plus the end section. Below the waterline it fades into the water.
- `lamp.webp` and `bucket.webp`: props on the deck. The lantern glows in code at dusk and night.
- `cat-body.webp`, `cat-head.webp`, `cat-ear-back.webp`, `cat-ear-front.webp`, `cat-tail-1..3.webp`: Saltwhisker as a puppet. The head tilts on the neck (looks about, glances at the water, watches the bobber, perks up on a bite, leans in to reel). Ears turn on the head for the nibble and bite cues. The tail bends at two joints in a travelling wave with an occasional flick, stands up and puffs on a bite, lashes while reeling. The body squashes when he crouches, and he blinks. A soft rim light outlines him at night.

To rebuild them from new images: key each one with `python3 tools/key-magenta.py --sprite`, then run `python3 tools/build-painted-art.py work art`. The cut shapes for the ears and tail are at the top of that script. Placement constants (`PIER`, `LAMP`, `BUCKET`, `CATP`) are in `index.html`. Water, the rod, line, bobber and fish shadows are drawn in code in soft shapes to match.

**Fish paintings** live in `art/fish/` as `fish-001-pier-perch.webp` and so on (keyed with `key-magenta.py --sprite`, then resized to 720 px wide). Add each new one to `FISH_ART` in `index.html`; fish without a painting show the dashed placeholder.

The fish and Saltwhisker drawings will be hand-drawn by Shauna and dropped in later. Specs live on the design board: 1200 by 900 px transparent PNG per fish, named like `fish-007-grumble-grouper.png`.
