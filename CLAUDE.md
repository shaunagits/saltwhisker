# Saltwhisker

A pixel-art browser fishing game. Saltwhisker, a tuxedo cat in a yellow sou'wester with ear holes, fishes off an ocean pier for his dinner and keeps a journal (the Tidebook) of every catch. Just for fun, for Shauna and her friends. Read `README.md` for how a session works and where the tuning knobs are, `_docs/PROJECT_STATUS.md` for decisions, their reasons and Shauna's open questions, `_docs/TODO.md` for the ordered queue, and `_docs/findings/` before touching the painted backdrops.

- Everything is in `index.html` (canvas plus plain JavaScript, no build step).
- Repository `shaunagits/saltwhisker` (private during development, public later for her portfolio). Every push to `main` deploys to production on Vercel.
- Players reach it at https://games.shauna.digital/saltwhisker/ through a rewrite in the `shaunagits/games` repo. Keep every asset path relative.
- Keep anything private, proprietary or licensed out of commits from day one, because the repo goes public later with its history. Use the git-ignored `_private/` folder.
- No test suite. Verify changes with a playtest bot (Playwright plus the `window.__tb` hooks), see `tools/playtest-bot.js`. Screenshot phone portrait (390 by 844), phone landscape (844 by 390) and desktop.
- Painted backdrops in `art/` are Shauna's. The cat must not get bigger on screen and the camera must not zoom in further (her call, 2026-10-11).
- Shauna draws the fish and cat illustrations herself. The game uses placeholders until her art arrives. Do not redraw the cat's design without asking.
- Sound is not added yet. Ask before adding any.
- Respect `prefers-reduced-motion`.
- No em dashes in any text. No AI or assistant credit in code, commits, or docs.
- Shauna creates new GitHub repositories herself. A session cannot.
