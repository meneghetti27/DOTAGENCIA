import { list } from '@vercel/blob';
// Rodada atual do placar. Para começar uma nova rodada, aumente este número: as rodadas antigas continuam guardadas.
export const ROUND = 2;
const prefixOf = r => (r === 1 ? 's/' : `r${r}/`);
const b64 = s => Buffer.from(s, 'utf8').toString('base64url');
const unb64 = s => { try { return Buffer.from(s, 'base64url').toString('utf8'); } catch { return '?'; } };
export const keyFor = (name, beers, hero) => `${prefixOf(ROUND)}${String(999 - beers).padStart(3, '0')}_${Date.now()}_${hero}_${b64(name)}`;
export function cleanName(n) { return String(n || '').replace(/[\u0000-\u001f<>]/g, '').replace(/\s+/g, ' ').trim().slice(0, 18); }
async function rows(round) {
  const prefix = prefixOf(round); let cursor, all = [];
  do { const r = await list({ prefix, limit: 1000, cursor }); all.push(...r.blobs); cursor = r.cursor; } while (cursor && all.length < 5000);
  return all.map(b => { const [inv, ts, hero, nm] = b.pathname.slice(prefix.length).split('_'); return { name: unb64(nm || ''), beers: 999 - Number(inv), hero, ts: Number(ts) }; })
    .filter(r => r.name && Number.isFinite(r.beers)).sort((a, b) => b.beers - a.beers || a.ts - b.ts);
}
function best(rs, n) { const seen = new Set(), out = []; for (const r of rs) { const k = r.name.toLowerCase(); if (seen.has(k)) continue; seen.add(k); if (out.length < n) out.push(r); } return { top: out, players: seen.size }; }
const champs = {};
export async function top(n = 3) {
  const cur = best(await rows(ROUND), n);
  const past = [];
  for (let r = 1; r < ROUND; r++) { if (!champs[r]) { const b = best(await rows(r), 1).top[0]; if (b) champs[r] = b; } if (champs[r]) past.push({ round: r, ...champs[r] }); }
  return { round: ROUND, ...cur, champions: past };
}
