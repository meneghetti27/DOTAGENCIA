// Renderiza a cena 3D: node shot.js "query" saida.png W H
// Sem servidor: o Playwright intercepta http://cena.local/* e entrega os arquivos desta pasta.
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const TIPOS = {'.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg'};
(async () => {
  const [, , qs, out, w, h] = process.argv; const W = +w || 1600, H = +h || 1600;
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: W, height: H}});
  p.on('pageerror', e => console.log('err:', e.message));
  await p.route('http://cena.local/**', rota => {
    const f = path.join(__dirname, decodeURIComponent(new URL(rota.request().url()).pathname));
    if (!f.startsWith(__dirname) || !fs.existsSync(f)) return rota.fulfill({status: 404});
    rota.fulfill({status: 200, body: fs.readFileSync(f), contentType: TIPOS[path.extname(f)] || 'application/octet-stream'});
  });
  await p.goto(`http://cena.local/cena.html?w=${W}&h=${H}&${qs}`);
  await p.waitForFunction('window.DONE', null, {timeout: 300000});
  await p.screenshot({path: out, omitBackground: true}); await b.close();
})();
