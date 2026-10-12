# Saltwhisker

A painted fishing game for the browser. Walter, a tuxedo cat in a yellow sou'wester, fishes off the end of an ocean pier and keeps a journal (the Tidebook) of everything he catches.

Play it at https://games.shauna.digital/saltwhisker/

## How a session works

1. **Read the water.** Signs come and go on the surface (`SIGNS`): bubbles mean small fry, a fin means something decent, a dark patch means something big. Landing on one brings a quicker bite and a fish that matches (`signWeight`).
2. **Cast.** Hold anywhere (or Space) to wind up. The power bar fills and falls back, so timing matters. Gold marks on the bar show where the signs are (or one sweet spot when there are none). Let go on a mark for a perfect cast: a sparkle, and the fish tends to be bigger. A short cast fishes close in, a long one far out, and some fish only live at one depth.
3. **Wait and twitch.** A quick tap twitches the bait; gentle twitches (`TUNE.twitchGap` apart) bring the fish sooner, too many in a row (`twitchSpook`) scare it off and another one takes its time. Hold to reel in and cast again. Each kind of fish nibbles its own way first (`nibbleKind`): quick flutters for small fish, short tugs, one slow heavy pull for big ones, a sideways wobble for odds and ends. Skip the small ones if you are after something big.
4. **Bite.** The bobber dips, his ears go up and his tail puffs. Tap within the bite window.
5. **Reel.** Hold to reel, let go to ease off. Keep the tension marker in the green. The green is narrower for rarer fish, drifts for the eel and fades while the ghost is gone. Too much tension snaps the line, too much slack lets the fish go. Every fish fights in its own way (`fight` in `FISH`, notes in `FIGHTS`): steady bursts, quick darts, a sardine that sulks and goes limp, groupers that grumble then lunge, a tuna that runs, an eel that wriggles, heavy ones, and a ghost that fades out mid-fight. Every fish tires as the fight goes on.
6. **Golden fish.** About 1 in 20 bites is a golden version, given away by a gold shimmer in the water. Golden catches get a star in the journal.
7. **Odds and ends.** Not everything is a fish: a message in a bottle (its note tips you off about a fish you have not caught), four torn map pieces (all four reveal a sunken chest far out, whose lucky coin doubles golden fish), a rubber duck, an empty sardine tin and a single flip-flop. They sit in the journal after the fish with an Odds and Ends tag and are counted separately.
8. **The Kraken.** A legendary that bites only at night with a long cast. The fight comes in three rounds, one per tentacle (heavy, then wriggling, then lunging), each stronger than the last. A huge shape rises under the bobber and Walter's tail stays puffed the whole time. Now and then at night one of Shauna's painted tentacles (`art/kraken-tentacle-1.webp`, `-2.webp`) rises far out at sea and sinks again (`CAMEO`); the same two paintings, as dark silhouettes, ring the shape under the bobber during the fight, and the bottle sometimes hints at him. `?debug` has a tentacle button.
9. **Jumping fish.** Strong fish leap mid-fight. Tap as they jump to set the hook (they lose line); miss and they gain a little. The fight pauses while the fish is in the air and the line follows it; tension lands mid-green with a short grace before the next lunge.
10. **Feeding frenzy.** Every few minutes in daylight, gulls dive over one spot for 30 seconds. Cast near them for quick bites.
11. **Seagull thief.** Sometimes after a catch a gull lands on the lamp. Tap it within about 3 seconds or it steals the catch, which then does not count (a new entry comes back out of the Tidebook).
12. **Catch.** A journal card shows the fish. New fish get a "NEW ENTRY" stamp, bigger ones get "NEW BEST".

**Walter's moods.** Short reactions (`mood()`, `MOOD`) move his head, ears, tail and eyes and put a little sign over his head: hearts and two hops for a catch, sparkles and three hops for a new entry, best or golden fish, a head shake and "..." for odds and ends, drooping ears and a tear for an escape, a scribble cloud for a snapped line, an angry vein when a gull steals, "!!" and a jump for the Kraken, "?" on a nibble, "!" on a bite, and he dozes off with "z z" after 30 idle seconds. Drawn in code for now; painted expression heads can replace the eye shapes later.

**Time and weather.** The clock follows your real local time, and Day 1 is the day you first played. Day, dusk and night each have their own fish. About 30% of calendar days are rainy, and they are the same days for every player (picked from the date, `weatherFor`), which brings out rain-only fish. One "fish of the day" is the same for everyone on a calendar date and is more likely to bite. One fish only appears on real-world Sundays.

## Code layout

Everything is in `index.html`: canvas plus plain JavaScript, no build step, no dependencies besides Google Fonts. Asset paths must stay relative, because the game is served both at its own domain and under `/saltwhisker` on games.shauna.digital.

Sections inside the script, in order:

- `TUNE`: every tuning knob (clock speed, cast timing, bite window, reel and tension rates, perfect cast, signs, twitching). Change numbers here, not in the logic.
- `FISH`: the 16 fish (the Kraken is 16) plus the odds and ends (ids 101 to 106, `junk: true`). Each has time of day, depth, weight (how often it bites), size range, strength, rarity, the cat's journal note, the hint shown before it's found, and optional `weather`, `sunday` or `refuse`.
- Save: local storage key `saltwhisker.save` (clock, weather, journal, map pieces, lucky coin). Older saves may still carry unused dinner and streak fields.
- Camera: `CAM` is the focus box (cat, rod, bobber, near water). The game zooms so that box always fits and fills the rest of the screen with more world. Portrait shows more water, landscape shows more sea and sky.
- Walter's pixel stand-in (shown only while the paintings load): `CAT_MAP` is the 16 by 16 sprite as text, one letter per color. `catPose()` and `catPixels()` add the ear, tail and crouch cues. At night a soft rim light keeps his outline readable.
- Draw, HUD, catch card, journal, debug panel, loop, playtest hooks.

## Testing

There is no test suite. Check changes with a playtest bot: Playwright plus the `window.__tb` hooks (`press`, `release`, `setHour`, `setWeather`, `reset`, `closeCard`, and the live state `S`). `tools/playtest-bot.js` plays several rounds per fish and reports catches, snaps and escapes:

```
node tools/playtest-bot.js index.html
```

Sound is off until the player taps the speaker button (all synthesized in code, no sound files; `SND` and `SFX`). A title card greets each visit, with tips the first time. Add `?debug` to the URL for a small panel (it also has tentacle, frenzy and gull buttons) to jump the clock, toggle rain, force a bite, or reset the save.

## Art

**Painted backdrops** live in `art/`, all by Shauna:

- `sky-day.webp` and `sky-night.webp`: full skies. Each is placed so its horizon (90% of the way down) sits on the sea. Day fades to the code's dusk colors, then the night painting fades in. Rain adds a gray wash.
- `far-day.webp` and `far-night.webp`: the distant village and lighthouse, cut out from a magenta background, cropped to their content, with soft faded side edges. The night painting has a slightly different layout, so it is lined up on the lighthouse (`FAR_NIGHT_LAMP`). Dusk uses a tinted copy of the day layer. The lighthouse light pulses in code at dusk and night.

To process a new coast image: `python3 tools/key-magenta.py input.png art/far-name.webp`. The full how-to, the screen-coverage math and the style-neutral prompts are in the local notes (`_private/findings/`, not committed). A dusk painting follows the same pattern in `drawPaintedSky` and `drawFar`.

**Painted scene pieces**, also Shauna's, each one daytime painting tinted in code for dusk and night (`P.tint`):

- `pier.webp`: one strip made of two repeats of the middle section plus the end section. Below the waterline it fades into the water.
- `lamp.webp` and `bucket.webp`: props on the deck. The lantern glows in code at dusk and night.
- `gull-perched.webp`, `gull-flying.webp` and `gull-flying-down.webp`: the gulls, both facing left (the code flips them). The thief stands on the lamp top in the perched painting (feet at `GULL.feetX` of its width) and arrives and leaves in the flying one; the frenzy gulls use the flying one, smaller. Flying gulls flap by swapping the wings-up and wings-down frames, which share one canvas lined up on the beak (with reduced motion they glide on the wings-up frame). The tiny gull crossing the far sky is still a code stroke. Keyed with `key-magenta.py --sprite`; the perched one is 300 px tall, the flight frames 403 px on their shared canvas.
- `cat-body.webp`, `cat-head.webp`, `cat-ear-back.webp`, `cat-ear-front.webp`, `cat-tail-1..3.webp`: Walter as a puppet. The head tilts on the neck (looks about, glances at the water, watches the bobber, perks up on a bite, leans in to reel). Ears turn on the head for the nibble and bite cues. The tail bends at two joints in a travelling wave with an occasional flick, stands up and puffs on a bite, lashes while reeling. The body squashes when he crouches, and he blinks. A soft rim light outlines him at night.

To rebuild them from new images: key each one with `python3 tools/key-magenta.py --sprite`, then run `python3 tools/build-painted-art.py work art`. The cut shapes for the ears and tail are at the top of that script. Placement constants (`PIER`, `LAMP`, `BUCKET`, `CATP`) are in `index.html`. Water, the rod, line, bobber and fish shadows are drawn in code in soft shapes to match.

**Fish paintings** live in `art/fish/` as `fish-001-pier-perch.webp` and so on (keyed with `key-magenta.py --sprite`, then resized to 720 px wide). Add each new one to `FISH_ART` in `index.html`; fish without a painting show the dashed placeholder.

The fish and Walter drawings may be hand-drawn by Shauna and dropped in later. Specs live on the design board: 1200 by 900 px transparent PNG per fish, named like `fish-007-grumble-grouper.png`.
