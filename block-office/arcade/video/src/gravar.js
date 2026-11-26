// Grava gameplay real do jogo (270x480) com um bot movendo a raquete.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 270, height: 480 }, deviceScaleFactor: 1,
    recordVideo: { dir: path.join(__dirname, 'rec'), size: { width: 270, height: 480 } } });
  const p = await ctx.newPage();
  await p.goto('file://' + path.resolve(__dirname, '../../game/index.html'));
  await p.waitForTimeout(1500);
  const log = async m => console.log(m, ((await p.evaluate(() => performance.now())) / 1000).toFixed(2), JSON.stringify(await p.evaluate(() => window.__hxb.state())));
  await p.evaluate(() => {
    setInterval(() => { const d = window.__hxb.dbg(); const bs = d.balls.filter(b => b.vy > 0);
      const t = (bs.length ? bs : d.balls).sort((a, b) => b.y - a.y)[0];
      if (t) window.__hxb.setX(t.x + Math.sin(performance.now() / 300) * d.pad.w * 0.3);
      if (d.st === 'playing' || d.st === 'boss' || d.st === 'intro') if (d.balls.some(b => b.preso)) window.__hxb.launch(); }, 16);
  });
  await log('start'); await p.evaluate(() => window.__hxb.launch()); await p.waitForTimeout(300); await p.evaluate(() => window.__hxb.launch());
  await p.waitForTimeout(6000); await log('pw'); await p.evaluate(() => window.__hxb.pw('largo'));
  await p.waitForTimeout(6000); await log('next'); await p.evaluate(() => window.__hxb.next());
  await p.waitForTimeout(10000); await log('boss'); await p.evaluate(() => window.__hxb.next());
  await p.waitForTimeout(7000); await log('end');
  await p.waitForTimeout(3000); await log('end2');
  await ctx.close(); await b.close();
})();
