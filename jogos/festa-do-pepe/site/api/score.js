import { put } from '@vercel/blob';
import { top, keyFor, cleanName } from './_placar.js';
export default async function handler(req, res) {
  if (req.method !== 'POST') { res.status(405).json({ error: 'use POST' }); return; }
  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const name = cleanName(body.name), beers = Math.floor(Number(body.beers)), hero = body.hero === 'Gael' ? 'Gael' : 'Pepe';
    if (!name) { res.status(400).json({ error: 'nome vazio' }); return; }
    if (!Number.isFinite(beers) || beers < 0 || beers > 60) { res.status(400).json({ error: 'pontuação inválida' }); return; }
    await put(keyFor(name, beers, hero), String(beers), { access: 'private', addRandomSuffix: false, contentType: 'text/plain' });
    res.setHeader('Cache-Control', 'no-store');
    res.status(200).json(await top(3));
  } catch (e) { res.status(500).json({ error: 'não deu pra salvar' }); }
}
