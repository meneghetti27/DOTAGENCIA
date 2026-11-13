import { top } from './_placar.js';
export default async function handler(req, res) {
  try { const data = await top(3); res.setHeader('Cache-Control', 'public, s-maxage=6, stale-while-revalidate=30'); res.status(200).json(data); }
  catch (e) { res.status(500).json({ error: 'placar indisponível' }); }
}
