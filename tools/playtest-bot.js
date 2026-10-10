// Playtest bot for Saltwhisker: plays rounds with a human-like reel controller and reports
// catches, snaps and escapes per fish. Usage: node tools/playtest-bot.js index.html
const { chromium } = require('playwright');
const path = require('path');
const file = 'file://' + path.resolve(process.argv[2]);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message)); page.on('console', m => console.log(m.text()));
  await page.goto(file);
  await page.waitForTimeout(500);

  const results = await page.evaluate(async () => {
    const tb = window.__tb, S = tb.S;
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const ids = (window.__ids || [1, 5, 7, 9, 14, 15]);
    const res = {};
    for (const id of ids) {
      res[id] = { caught: 0, snap: 0, escape: 0, time: [] };
      for (let round = 0; round < 3; round++) {
        tb.closeCard();
        await sleep(100);
        const target = 0.2 + Math.random() * 0.75;
        tb.press();
        while (S.power < target || S.t < 0.05) await sleep(16);
        tb.release();
        while (S.state !== 'waiting') await sleep(20);
        S.fish = tb.FISH.find(f => f.id === id);
        S.waitAt = S.t + 0.5; S.nibbles = [];
        while (S.state !== 'bite') await sleep(20);
        await sleep(250);                       // human reaction
        tb.press(); tb.release();
        const t0 = performance.now();
        const before = { c: S.catches, s: S.snaps, e: S.escapes };
        while (S.state === 'reeling') {
          // human-ish: decide every 120 ms
          if (S.tension < 0.48) tb.press(); else tb.release();
          await sleep(120);
          if (performance.now() - t0 > 40000) break;
        }
        tb.release();
        const dt = (performance.now() - t0) / 1000;
        if (S.catches > before.c) { res[id].caught++; res[id].time.push(+dt.toFixed(1)); }
        else if (S.snaps > before.s) { res[id].snap++; res[id].time.push('snap' + dt.toFixed(0)); }
        else if (S.escapes > before.e) { res[id].escape++; res[id].time.push('esc' + dt.toFixed(0)); }
        else { res[id].time.push('timeout d' + S.dist.toFixed(0)); tb.closeCard(); }
        console.log(id, round, JSON.stringify(res[id]));
        while (S.state === 'message') await sleep(50);
      }
    }
    return res;
  });
  console.log(JSON.stringify(results, null, 1));
  console.log('errors:', errors);
  await browser.close();
})();
