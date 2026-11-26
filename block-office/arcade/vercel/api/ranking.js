// Ranking público do HARD × BLOCK: um JSON no Vercel Blob com o TOP 100.
const { put, list } = require('@vercel/blob');
const NOME = 'ranking/top.json';
async function ler() {
  const { blobs } = await list({ prefix: 'ranking/' });
  const b = blobs.find(x => x.pathname === NOME);
  if (!b) return [];
  const r = await fetch(b.url + '?v=' + Date.now(), { cache: 'no-store' });
  return r.ok ? r.json() : [];
}
module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  try {
    if (req.method === 'GET') return res.status(200).json((await ler()).slice(0, 10));
    if (req.method === 'POST') {
      let b = req.body; if (typeof b === 'string') b = JSON.parse(b || '{}');
      const arroba = String(b.arroba || '').trim();
      const pontos = Math.floor(Number(b.pontos));
      const fase = Math.floor(Number(b.fase)) || 1;
      if (!/^@[A-Za-z0-9._]{1,30}$/.test(arroba) || !(pontos >= 0 && pontos < 1e6)) return res.status(400).json({ erro: 'dados inválidos' });
      const doc = { id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), arroba, pontos, fase, quando: Date.now() };
      const lista = (await ler()).concat(doc).sort((a, c) => c.pontos - a.pontos).slice(0, 100);
      await put(NOME, JSON.stringify(lista), { access: 'public', addRandomSuffix: false, allowOverwrite: true, contentType: 'application/json', cacheControlMaxAge: 0 });
      return res.status(200).json({ id: doc.id });
    }
    res.status(405).end();
  } catch (e) { res.status(500).json({ erro: 'falhou' }); }
};
