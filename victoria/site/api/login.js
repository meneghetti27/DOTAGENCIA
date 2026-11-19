// Login do painel da Dra. Victoria (POST entra, DELETE sai, GET diz se está logada).
const { lerConta, confere, criaSessao, apagaSessao, logada, corpo, json } = require('./_lib');
const tentativas = new Map(); // freio simples contra chute de senha
module.exports = async (req, res) => {
  try {
    if (req.method === 'GET') return json(res, 200, { logada: await logada(req) });
    if (req.method === 'DELETE') { apagaSessao(res); return json(res, 200, { ok: true }); }
    if (req.method !== 'POST') return json(res, 405, { erro: 'Método não aceito.' });
    const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0];
    const t = tentativas.get(ip) || { n: 0, ate: 0 };
    if (t.ate > Date.now()) return json(res, 429, { erro: 'Muitas tentativas. Espere um minuto.' });
    const conta = await lerConta();
    if (!confere(corpo(req).senha || '', conta)) {
      t.n++; if (t.n >= 5) { t.ate = Date.now() + 60e3; t.n = 0; } tentativas.set(ip, t);
      await new Promise(r => setTimeout(r, 600));
      return json(res, 401, { erro: 'Senha incorreta.' });
    }
    tentativas.delete(ip);
    criaSessao(res, conta.hash.slice(0, 12));
    json(res, 200, { ok: true });
  } catch (e) { json(res, 500, { erro: 'Erro ao entrar. Tente de novo.' }); }
};
