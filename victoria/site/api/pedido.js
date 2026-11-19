// Público: paciente reserva um horário. O horário fica ocupado na hora para ninguém mais pegar.
const crypto = require('crypto');
const { lerAgenda, gravarAgenda, lerPedidos, gravarPedidos, corpo, json, DATA, HORA } = require('./_lib');
const TIPOS = ['Primeira consulta', 'Retorno', 'Pós-operatório'], MODOS = ['Presencial em Brasília', 'Teleconsulta'];
const limpa = (s, n) => String(s || '').replace(/[<>]/g, '').trim().slice(0, n);

module.exports = async (req, res) => {
  if (req.method !== 'POST') return json(res, 405, { erro: 'Use POST.' });
  try {
    const b = corpo(req);
    const nome = limpa(b.nome, 80), tel = limpa(b.tel, 30), data = String(b.data || ''), hora = String(b.hora || '');
    if (!nome || tel.replace(/\D/g, '').length < 10 || !DATA.test(data) || !HORA.test(hora) || !TIPOS.includes(b.tipo) || !MODOS.includes(b.modo))
      return json(res, 400, { erro: 'Confira os dados do agendamento.' });
    const ag = await lerAgenda();
    const dia = new Date(data + 'T12:00:00-03:00'), sem = dia.getUTCDay();
    const hoje = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Sao_Paulo' })); hoje.setHours(23, 59, 0, 0);
    const conf = ag.dias[data];
    const horarios = conf && conf.fechado ? [] : conf && conf.horarios ? conf.horarios : (ag.semana[sem] || []);
    if (dia <= hoje || !horarios.includes(hora)) return json(res, 409, { erro: 'Esse horário não está disponível.' });
    if ((ag.ocupados[data] || []).includes(hora)) return json(res, 409, { erro: 'Esse horário acabou de ser reservado. Escolha outro.' });
    ag.ocupados[data] = [...(ag.ocupados[data] || []), hora].sort();
    await gravarAgenda(ag);
    const pedidos = await lerPedidos();
    pedidos.unshift({ id: crypto.randomBytes(6).toString('hex'), criado: new Date().toISOString(), nome, tel, tipo: b.tipo, modo: b.modo, data, hora, status: 'novo' });
    await gravarPedidos(pedidos.slice(0, 1000));
    json(res, 200, { ok: true });
  } catch (e) { json(res, 500, { erro: 'Não foi possível reservar agora. Tente pelo WhatsApp.' }); }
};
