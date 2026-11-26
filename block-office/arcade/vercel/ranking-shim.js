// Na Vercel não existe window.claude: imita claude.use("db") só para a coleção "ranking", usando /api/ranking.
(function(){ if (window.claude && window.claude.use) return;
  const q = { orderBy(){return q}, limit(){return q}, async get(){ const r = await fetch('/api/ranking',{cache:'no-store'}); const a = r.ok ? await r.json() : []; return { docs: a.map(d=>({id:d.id, data:()=>d})) }; } };
  const col = Object.assign(Object.create(q), { async add(doc){ const r = await fetch('/api/ranking',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(doc)}); if(!r.ok) throw new Error('ranking'); return await r.json(); } });
  window.claude = { use: async n => n==='db' ? { collection: () => col } : null };
})();
