# Saltwhisker

A browser fishing game in painted cut-out art (switched from pixel art on Shauna's call, 2026-10-11). The cat is Walter (named 2026-10-11; the game is still called Saltwhisker), a charcoal-and-white tuxedo cat in a yellow sou'wester with ear holes and a yellow oilskin coat, fishes off an ocean pier for his dinner and keeps a journal (the Tidebook) of every catch. Just for fun, for Shauna and her friends. Read `README.md` for how a session works and where the tuning knobs are, `_private/PROJECT_STATUS.md` for decisions, their reasons and Shauna's open questions (local only, never committed), `_private/TODO.md` for the ordered queue, and `_private/findings/` before touching the painted art. All three are local only.

- Everything is in `index.html` (canvas plus plain JavaScript, no build step).
- Repository `shaunagits/saltwhisker` (private during development, public later for her portfolio). Every push to `main` deploys to production on Vercel.
- Players reach it at https://games.shauna.digital/saltwhisker/ through a rewrite in the `shaunagits/games` repo. Keep every asset path relative.
- Keep anything private, proprietary or licensed out of commits from day one, because the repo goes public later with its history. Use the git-ignored `_private/` folder.
- No test suite. Verify changes with a playtest bot (Playwright plus the `window.__tb` hooks), see `tools/playtest-bot.js`. Screenshot phone portrait (390 by 844), phone landscape (844 by 390) and desktop.
- Painted backdrops in `art/` are Shauna's. The cat must not get bigger on screen and the camera must not zoom in further (her call, 2026-10-11).
- Shauna makes the fish, cat and scene art (image generator first, possibly redrawn by hand later). Code drawings stand in only where a painting is missing or still loading. Do not redraw the cat's design without asking.
- Sound is synthesized in code, off until the player turns it on (approved 2026-10-12). Ask before adding sound files or new kinds of sound.
- Respect `prefers-reduced-motion`.
- No em dashes in any text. No AI or assistant credit in code, commits, or docs.
- Shauna creates new GitHub repositories herself. A session cannot.
