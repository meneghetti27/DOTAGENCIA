// Funções comuns: guardar/ler a agenda no Blob e conferir o login da Dra. Victoria.
const crypto = require('crypto');
const { put, list, del } = require('@vercel/blob');

// Senha inicial (trocar no painel em "Conta"). Guardada só como hash.
const SENHA_INICIAL = { salt: 'c546ea0203a2f44dfa91d2b79678e6aa', hash: '9e80bc91784c41a710a02b6ee1bc16354898115e65a759f3ef8f89c402325f2aad01627fb6647b4d4a73a53e56ecc90f0d0d599df3942200e0d4c9e26da0d010' };

const PADRAO = {
  semana: { 1: ['15:00', '16:30', '19:00'], 2: ['08:00', '09:30', '11:00', '14:00'], 3: ['14:00', '15:30', '17:00'], 4: ['09:00', '10:30', '16:00', '18:30'], 5: ['08:30', '10:00', '11:30'] },
  dias: {},        // "2026-12-24": { fechado: true } ou { horarios: ["09:00", ...] }
  ocupados: {},    // "2026-12-01": ["09:30"]
  site: {
    whatsapp: '5551991890776',
    meses: 2,
    avisoTitulo: 'Porto Alegre a partir de maio de 2027.',
    avisoTexto: 'A agenda para consulta online já está aberta!',
    notificacao: true,
    notifTitulo: 'Em breve em Porto Alegre ✨',
    notifTexto: 'Atendimento a partir de maio de 2027. A agenda online já está aberta.'
  }
};

async function acha(prefixo) {
  const { blobs } = await list({ prefix: prefixo });
  blobs.sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt));
  return blobs;
}
async function ler(prefixo, padrao) {
  const blobs = await acha(prefixo);
  if (!blobs.length) return JSON.parse(JSON.stringify(padrao));
  const r = await fetch(blobs[0].url + '?v=' + Date.now(), { cache: 'no-store' });
  if (!r.ok) return JSON.parse(JSON.stringify(padrao));
  return r.json();
}
// arquivos privados ganham nome aleatório (ninguém adivinha o endereço); os antigos são apagados
async function gravar(prefixo, dados, privado) {
  const antigos = await acha(prefixo);
  const nome = privado ? prefixo + '-' + crypto.randomBytes(16).toString('hex') + '.json' : prefixo;
  await put(nome, JSON.stringify(dados), { access: 'public', addRandomSuffix: false, contentType: 'application/json', cacheControlMaxAge: 60 });
  const velhos = antigos.filter(b => b.pathname !== nome).map(b => b.url);
  if (velhos.length) await del(velhos);
}

const lerAgenda = async () => {
  const a = await ler('dados/agenda.json', PADRAO);
  a.site = { ...PADRAO.site, ...(a.site || {}) };
  a.semana = a.semana || PADRAO.semana; a.dias = a.dias || {}; a.ocupados = a.ocupados || {};
  return a;
};
const gravarAgenda = a => gravar('dados/agenda.json', a, false);
const lerPedidos = () => ler('privado/pedidos', []);
const gravarPedidos = p => gravar('privado/pedidos', p, true);
const lerConta = () => ler('privado/conta', SENHA_INICIAL);
const gravarConta = c => gravar('privado/conta', c, true);

const hashSenha = (senha, salt) => crypto.scryptSync(String(senha), salt, 64).toString('hex');
const confere = (senha, conta) => {
  const h = Buffer.from(hashSenha(senha, conta.salt), 'hex'), c = Buffer.from(conta.hash, 'hex');
  return h.length === c.length && crypto.timingSafeEqual(h, c);
};

// sessão: cookie assinado, vale 30 dias
const chave = () => crypto.createHash('sha256').update('sessao-vo:' + (process.env.BLOB_READ_WRITE_TOKEN || '')).digest();
const assina = txt => crypto.createHmac('sha256', chave()).update(txt).digest('hex');
function criaSessao(res, versao) {
  const exp = Date.now() + 30 * 864e5, txt = exp + '.' + versao;
  res.setHeader('Set-Cookie', `vo_sessao=${txt}.${assina(txt)}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${30 * 86400}`);
}
function apagaSessao(res) { res.setHeader('Set-Cookie', 'vo_sessao=; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=0'); }
async function logada(req) {
  const m = /(?:^|;\s*)vo_sessao=([^;]+)/.exec(req.headers.cookie || '');
  if (!m) return false;
  const [exp, versao, sig] = m[1].split('.');
  if (!sig || +exp < Date.now()) return false;
  const esperado = assina(exp + '.' + versao);
  if (sig.length !== esperado.length || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(esperado))) return false;
  const conta = await lerConta();
  return versao === (conta.hash || '').slice(0, 12); // trocar a senha derruba as sessões antigas
}

const corpo = req => (typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {});
const json = (res, status, dados) => { res.status(status).setHeader('Content-Type', 'application/json; charset=utf-8'); res.end(JSON.stringify(dados)); };
const DATA = /^\d{4}-\d{2}-\d{2}$/, HORA = /^\d{2}:\d{2}$/;

module.exports = { PADRAO, lerAgenda, gravarAgenda, lerPedidos, gravarPedidos, lerConta, gravarConta, hashSenha, confere, criaSessao, apagaSessao, logada, corpo, json, DATA, HORA };
