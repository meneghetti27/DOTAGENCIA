import { list } from '@vercel/blob';
const b64 = s => Buffer.from(s, 'utf8').toString('base64url');
const unb64 = s => { try { return Buffer.from(s, 'base64url').toString('utf8'); } catch { return '?'; } };
export const keyFor = (name, beers, hero) => `s/${String(999 - beers).padStart(3, '0')}_${Date.now()}_${hero}_${b64(name)}`;
export function cleanName(n) { return String(n || '').replace(/[\u0000-\u001f<>]/g, '').replace(/\s+/g, ' ').trim().slice(0, 18); }
export async function top(n = 3) {
  const { blobs } = await list({ prefix: 's/', limit: 200 });
  const rows = blobs.map(b => { const [inv, ts, hero, nm] = b.pathname.slice(2).split('_'); return { name: unb64(nm || ''), beers: 999 - Number(inv), hero, ts: Number(ts) }; })
    .filter(r => r.name && Number.isFinite(r.beers))
    .sort((a, b) => b.beers - a.beers || a.ts - b.ts);
  const seen = new Set(), out = [];
  for (const r of rows) { const k = r.name.toLowerCase(); if (seen.has(k)) continue; seen.add(k); out.push(r); if (out.length >= n) break; }
  return { top: out, players: seen.size };
}
