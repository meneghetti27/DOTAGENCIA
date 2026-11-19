// Painel (só logada): lê tudo e salva agenda, textos, pedidos e senha.
const crypto = require('crypto');
const { lerAgenda, gravarAgenda, lerPedidos, gravarPedidos, lerConta, gravarConta, hashSenha, confere, criaSessao, logada, corpo, json, DATA, HORA, PADRAO } = require('./_lib');
const horas = l => [...new Set((Array.isArray(l) ? l : []).filter(h => HORA.test(h)))].sort();
const txt = (s, n) => String(s == null ? '' : s).replace(/[<>]/g, '').slice(0, n);

module.exports = async (req, res) => {
  try {
    if (!(await logada(req))) return json(res, 401, { erro: 'Faça login de novo.' });
    if (req.method === 'GET') return json(res, 200, { agenda: await lerAgenda(), pedidos: await lerPedidos() });
    if (req.method !== 'POST') return json(res, 405, { erro: 'Método não aceito.' });
    const b = corpo(req);

    if (b.acao === 'agenda') {
      const a = b.agenda || {}, limpo = { semana: {}, dias: {}, ocupados: {}, site: {} };
      for (let d = 0; d <= 6; d++) { const l = horas((a.semana || {})[d]); if (l.length) limpo.semana[d] = l; }
      for (const [k, v] of Object.entries(a.dias || {})) if (DATA.test(k) && v) limpo.dias[k] = v.fechado ? { fechado: true } : { horarios: horas(v.horarios) };
      for (const [k, v] of Object.entries(a.ocupados || {})) if (DATA.test(k)) { const l = horas(v); if (l.length) limpo.ocupados[k] = l; }
      const s = a.site || {};
      limpo.site = {
        whatsapp: String(s.whatsapp || PADRAO.site.whatsapp).replace(/\D/g, '').slice(0, 15),
        meses: Math.min(12, Math.max(1, parseInt(s.meses, 10) || 2)),
        avisoTitulo: txt(s.avisoTitulo, 120), avisoTexto: txt(s.avisoTexto, 200),
        notificacao: !!s.notificacao, notifTitulo: txt(s.notifTitulo, 80), notifTexto: txt(s.notifTexto, 200)
      };
      await gravarAgenda(limpo);
      return json(res, 200, { ok: true, agenda: limpo });
    }

    if (b.acao === 'pedido') {
      const pedidos = await lerPedidos(), p = pedidos.find(x => x.id === b.id);
      if (!p) return json(res, 404, { erro: 'Pedido não encontrado.' });
      if (!['novo', 'confirmado', 'cancelado'].includes(b.status)) return json(res, 400, { erro: 'Status inválido.' });
      const ag = await lerAgenda(), lista = ag.ocupados[p.data] || [];
      if (b.status === 'cancelado' && p.status !== 'cancelado') ag.ocupados[p.data] = lista.filter(h => h !== p.hora);   // libera o horário
      if (b.status !== 'cancelado' && p.status === 'cancelado' && !lista.includes(p.hora)) ag.ocupados[p.data] = [...lista, p.hora].sort();
      if (ag.ocupados[p.data] && !ag.ocupados[p.data].length) delete ag.ocupados[p.data];
      p.status = b.status;
      await gravarAgenda(ag); await gravarPedidos(pedidos);
      return json(res, 200, { ok: true, agenda: ag, pedidos });
    }

    if (b.acao === 'apagar-pedido') {
      const pedidos = (await lerPedidos()).filter(x => x.id !== b.id);
      await gravarPedidos(pedidos);
      return json(res, 200, { ok: true, pedidos });
    }

    if (b.acao === 'senha') {
      const conta = await lerConta();
      if (!confere(b.atual || '', conta)) return json(res, 400, { erro: 'A senha atual não confere.' });
      if (String(b.nova || '').length < 8) return json(res, 400, { erro: 'A nova senha precisa ter pelo menos 8 caracteres.' });
      const salt = crypto.randomBytes(16).toString('hex'), nova = { salt, hash: hashSenha(b.nova, salt) };
      await gravarConta(nova);
      criaSessao(res, nova.hash.slice(0, 12));
      return json(res, 200, { ok: true });
    }
    json(res, 400, { erro: 'Ação desconhecida.' });
  } catch (e) { json(res, 500, { erro: 'Não foi possível salvar. Tente de novo.' }); }
};
