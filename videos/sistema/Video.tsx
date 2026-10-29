// dot. — "O sistema por trás do crescimento": recriação do anúncio de agência em tipografia cinética,
// alternando cenas claras (degradê gelo → azul, no lugar do branco → amarelo da referência) e cenas pretas com brilho azul.
// Sequência: "A maioria das agências vende [ícone] anúncio." → "constrói|" com zoom e o painel de conversão →
// pílulas Google Ads / Landing pages / Sites / Perfil no Google com os posts da dot voando → "Conectada" →
// "feita pra funcionar como uma só." → site da dot com lupa ("Nada roda isolado.") → posts passando ("achismo.") →
// tabelas de resultado do Google Ads em 3D ("Isso não é teoria") → "crescimento" gigante desfocado →
// logo em pílula + "A gente não faz um pouco de tudo. / A gente faz o que traz cliente.|".
// Narração ElevenLabs eleven_v4 (voz Moutella), um take só; tempos em audio.json.
import {loadFont as carregarTight} from '@remotion/google-fonts/InterTight';
import {loadFont as carregarInter} from '@remotion/google-fonts/Inter';
import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, random, staticFile, useCurrentFrame} from 'remotion';
import audio from './audio.json';

const {fontFamily: TIGHT} = carregarTight('normal', {weights: ['500', '600', '700', '800', '900'], subsets: ['latin']});
const {fontFamily: TIGHT_IT} = carregarTight('italic', {weights: ['600', '700', '800'], subsets: ['latin']});
const {fontFamily: INTER} = carregarInter('normal', {weights: ['500', '600', '700'], subsets: ['latin']});

export const FPS = 30;
const FIXO = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const SUAVE = Easing.bezier(0.16, 1, 0.3, 1);
const C = {fundo: '#05060D', azul: '#3D6EF5', vivo: '#2B6BFF', claro: '#8FB0FF', gelo: '#DCE6FF', marinho: '#0B1A4A', texto: '#0A1230', cinza: '#A4AAC0'};
const PASTA = 'videos/dot-sistema';
const VOZ = 6;

type P = {texto: string; quadro: number};
const palavras: P[] = audio.palavras.map((p) => ({texto: p.texto, quadro: VOZ + Math.round(p.inicio * FPS)}));
const limpa = (t: string) => t.toLowerCase().normalize('NFD').replace(/[^a-z0-9]/g, '');
const em = (t: string, n = 0) => {
  const lista = palavras.filter((p) => limpa(p.texto) === limpa(t));
  if (!lista[n]) throw new Error(`palavra não encontrada: ${t} #${n}`);
  return lista[n].quadro;
};
export const DURACAO = VOZ + Math.round(audio.duracao * FPS) + 36;
const CENAS = [0, em('a', 1) - 3, em('google') - 4, em('cada') - 3, em('feita') - 3, em('nada') - 4, em('nada', 1) - 4, em('isso') - 4, em('e', 1) - 2, em('dot') - 4];
const fimDe = (i: number) => (i + 1 < CENAS.length ? CENAS[i + 1] : DURACAO);

const entra = (frame: number, q: number, dur = 8) => (frame < q ? 0 : interpolate(frame, [q, q + dur], [0, 1], {...FIXO, easing: SUAVE}));
const img = (n: string) => staticFile(`${PASTA}/${n}.jpg`);

// ---------- Fundos ----------

// Claro: degradê gelo → azul brilhante, com ondas suaves (no lugar do branco → amarelo).
const Claro: React.FC<{t: number}> = ({t}) => (
  <>
    <AbsoluteFill style={{background: `linear-gradient(${150 + Math.sin(t / 40) * 8}deg, #FFFFFF 0%, #EEF3FF 32%, #B9CCFF 62%, ${C.vivo} 100%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(900px 700px at ${30 + Math.sin(t / 30) * 6}% 25%, rgba(255,255,255,0.9), rgba(255,255,255,0) 70%)`}} />
    <svg width={1080} height={1920} style={{position: 'absolute', opacity: 0.35}}>
      <path d={`M -100 ${1300 + Math.sin(t / 25) * 30} C 300 1100, 700 1500, 1200 ${1250 + Math.cos(t / 25) * 30}`} fill="none" stroke="#fff" strokeWidth={90} strokeLinecap="round" style={{filter: 'blur(30px)'}} />
    </svg>
  </>
);
// Escuro: preto com brilho azul vindo de baixo.
const Escuro: React.FC<{t: number}> = ({t}) => (
  <>
    <AbsoluteFill style={{backgroundColor: '#020308'}} />
    <AbsoluteFill style={{background: `radial-gradient(1100px 600px at 50% ${108 + Math.sin(t / 30) * 3}%, rgba(43,107,255,0.75), rgba(43,107,255,0) 70%)`}} />
    <svg width={1080} height={1920} style={{position: 'absolute', opacity: 0.6}}>
      <path d={`M -200 ${1250 + Math.sin(t / 20) * 40} C 300 900, 700 1300, 1300 ${1000 + Math.cos(t / 20) * 40}`} fill="none" stroke={C.azul} strokeWidth={6} style={{filter: 'blur(4px)'}} />
    </svg>
  </>
);
const Grao: React.FC = () => {
  const frame = useCurrentFrame();
  return <Img src={img(`grao${Math.floor(frame / 2) % 4}`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'overlay', opacity: 0.12}} />;
};

// Ícones 3D brilhantes desfocados flutuando (balões de conversa e "play").
const Bolha: React.FC<{x: number; y: number; esc: number; giro: number; desfoque: number; tipo: 'chat' | 'play'; t: number}> = ({x, y, esc, giro, desfoque, tipo, t}) => (
  <div style={{position: 'absolute', left: x, top: y + Math.sin(t / 20 + x) * 14, width: 220 * esc, height: 170 * esc, transform: `rotate(${giro + Math.sin(t / 30) * 4}deg)`, filter: `blur(${desfoque}px)`}}>
    {tipo === 'chat' ? (
      <div style={{position: 'absolute', inset: 0, borderRadius: 44 * esc, background: `linear-gradient(145deg, #CFDBFF, ${C.vivo} 70%, #1D4FE0)`, boxShadow: `inset 0 ${8 * esc}px ${16 * esc}px rgba(255,255,255,0.6), 0 ${20 * esc}px ${40 * esc}px rgba(43,107,255,0.35)`}}>
        {[0, 1, 2].map((k) => (
          <div key={k} style={{position: 'absolute', left: (50 + k * 46) * esc, top: 70 * esc, width: 28 * esc, height: 28 * esc, borderRadius: '50%', backgroundColor: '#fff'}} />
        ))}
        <div style={{position: 'absolute', left: 30 * esc, bottom: -26 * esc, width: 0, height: 0, borderLeft: `${30 * esc}px solid transparent`, borderTop: `${34 * esc}px solid ${C.vivo}`}} />
      </div>
    ) : (
      <svg width={220 * esc} height={170 * esc} viewBox="0 0 220 170">
        <defs>
          <linearGradient id={`pl${x}`} x1="0" x2="1" y1="0" y2="1">
            <stop offset="0" stopColor="#DCE6FF" />
            <stop offset="0.6" stopColor={C.vivo} />
            <stop offset="1" stopColor="#1D4FE0" />
          </linearGradient>
        </defs>
        <path d="M 50 20 Q 40 15 40 30 L 40 140 Q 40 155 52 148 L 180 92 Q 192 85 180 78 Z" fill={`url(#pl${x})`} />
      </svg>
    )}
  </div>
);

// Palavra com borrão de movimento ao entrar (como na referência).
const Palavra: React.FC<{texto: string; q: number; tam: number; peso?: number; cor?: string; italico?: boolean; de?: number}> = ({texto, q, tam, peso = 600, cor = C.texto, italico, de = 60}) => {
  const frame = useCurrentFrame();
  const e = entra(frame, q - 2, 9);
  return (
    <span style={{display: 'inline-block', fontFamily: italico ? TIGHT_IT : TIGHT, fontStyle: italico ? 'italic' : 'normal', fontWeight: peso, fontSize: tam, letterSpacing: '-0.04em', color: cor, opacity: e, transform: `translateX(${(1 - e) * de}px)`, filter: `blur(${(1 - e) * 12}px)`}}>{texto}</span>
  );
};

// Texto digitado com cursor piscando.
const Digita: React.FC<{texto: string; de: number; ate: number; tam: number; peso?: number; cor?: string; cursor?: boolean}> = ({texto, de, ate, tam, peso = 600, cor = C.texto, cursor = true}) => {
  const frame = useCurrentFrame();
  const n = Math.round(interpolate(frame, [de, ate], [0, texto.length], FIXO));
  const pisca = frame < ate + 2 || Math.floor(frame / 8) % 2 === 0;
  return (
    <span style={{fontFamily: TIGHT, fontWeight: peso, fontSize: tam, letterSpacing: '-0.04em', color: cor, whiteSpace: 'pre'}}>
      {texto.slice(0, n)}
      {cursor ? <span style={{display: 'inline-block', width: tam * 0.06, height: tam * 0.95, marginLeft: tam * 0.04, verticalAlign: '-0.12em', backgroundColor: cor, opacity: pisca ? 1 : 0}} /> : null}
    </span>
  );
};

// ---------- Cenas ----------

// 1. "A maioria das agências vende [megafone] anúncio."
const Maioria: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const troca = frame >= em('vende') - 2;
  const z = interpolate(t, [0, fimDe(0) - de], [1, 1.12], FIXO);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Claro t={t} />
      <Bolha x={-60} y={520} esc={1.2} giro={-18} desfoque={8} tipo="chat" t={t} />
      <Bolha x={760} y={380} esc={0.8} giro={14} desfoque={4} tipo="chat" t={t} />
      <Bolha x={600} y={1300} esc={1.5} giro={-10} desfoque={14} tipo="chat" t={t} />
      <Bolha x={60} y={1480} esc={1.0} giro={20} desfoque={10} tipo="play" t={t} />
      <AbsoluteFill style={{transform: `scale(${z})`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {!troca ? (
          <div style={{display: 'flex', gap: 22, alignItems: 'baseline'}}>
            <Palavra texto="A maioria" q={em('maioria')} tam={88} />
            <Palavra texto="das agências" q={em('agencias')} tam={88} cor="#5A6690" />
          </div>
        ) : (
          <div style={{display: 'flex', gap: 22, alignItems: 'center'}}>
            <Palavra texto="vende" q={em('vende')} tam={92} />
            <span style={{display: 'inline-flex', width: 120, height: 120, borderRadius: 30, backgroundColor: '#0A0F22', alignItems: 'center', justifyContent: 'center', boxShadow: '0 16px 40px rgba(10,15,34,0.35)', transform: `scale(${entra(frame, em('vende') + 4, 8)})`}}>
              <svg width={64} height={64} viewBox="0 0 24 24">
                <path d="M3 10 L3 14 L7 14 L13 18 L13 6 L7 10 Z" fill={C.vivo} />
                <path d="M16 9 Q18 12 16 15" fill="none" stroke={C.claro} strokeWidth={1.8} strokeLinecap="round" />
                <path d="M18.5 7 Q22 12 18.5 17" fill="none" stroke={C.claro} strokeWidth={1.8} strokeLinecap="round" />
              </svg>
            </span>
            <Palavra texto="anúncio." q={em('anuncio')} tam={92} cor="#5A6690" />
          </div>
        )}
      </AbsoluteFill>
      <Grao />
    </AbsoluteFill>
  );
};

// 2. "A gente constrói|" com zoom atravessando + painel de conversão.
const Constroi: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const card = em('sistema') - 2;
  const zoomTexto = interpolate(frame, [de, card + 8], [1, 3.2], {...FIXO, easing: Easing.in(Easing.cubic)});
  const cardE = entra(frame, card, 14);
  const foca = interpolate(frame, [em('por'), em('crescimento') + 10], [0.9, 1.35], {...FIXO, easing: SUAVE});
  const taxa = Math.round(interpolate(frame, [card + 6, em('crescimento') + 6], [13, 26], FIXO));
  const traco = entra(frame, card + 6, 26);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Claro t={t} />
      <Bolha x={700} y={1250} esc={1.4} giro={-12} desfoque={14} tipo="play" t={t} />
      <AbsoluteFill style={{display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${zoomTexto})`, filter: `blur(${Math.max(0, zoomTexto - 1.8) * 6}px)`, opacity: interpolate(frame, [card + 4, card + 12], [1, 0], FIXO)}}>
        <Digita texto="A gente constrói" de={em('a', 1)} ate={em('constroi') + 8} tam={110} peso={700} />
      </AbsoluteFill>
      {frame >= card ? (
        <div style={{position: 'absolute', left: 140, top: 640, width: 800, height: 520, transform: `translateX(${(1 - cardE) * 700}px) scale(${foca})`, transformOrigin: '40% 40%', borderRadius: 48, background: 'linear-gradient(160deg, #10162E, #070A16)', boxShadow: '0 40px 90px rgba(5,10,40,0.45)', padding: 52, fontFamily: INTER, color: '#fff'}}>
          <div style={{fontSize: 30, color: C.cinza}}>Taxa de conversão</div>
          <div style={{display: 'flex', alignItems: 'baseline', gap: 22, marginTop: 6}}>
            <span style={{fontFamily: TIGHT, fontWeight: 800, fontSize: 96, letterSpacing: '-0.04em'}}>{taxa}%</span>
            <span style={{fontSize: 32, fontWeight: 700, color: C.claro}}>▲ 12,8%</span>
          </div>
          <svg width={700} height={170} style={{position: 'absolute', left: 50, top: 210}}>
            <path d="M 0 150 C 120 140, 180 130, 260 110 S 420 60, 520 70 S 640 20, 700 10" fill="none" stroke={C.vivo} strokeWidth={6} strokeDasharray={900} strokeDashoffset={900 * (1 - traco)} style={{filter: `drop-shadow(0 0 10px ${C.vivo})`}} />
          </svg>
          <div style={{position: 'absolute', left: 52, bottom: 60, display: 'flex', alignItems: 'flex-end', gap: 12}}>
            {[40, 64, 50, 88, 72].map((h, k) => (
              <div key={k} style={{width: 22, height: h * entra(frame, card + 10 + k * 3, 10), borderRadius: 8, backgroundColor: C.vivo}} />
            ))}
          </div>
          <div style={{position: 'absolute', left: 52, bottom: 22, fontSize: 22, color: C.cinza}}>Crescimento semanal</div>
        </div>
      ) : null}
      <Grao />
    </AbsoluteFill>
  );
};

// 3. Pílulas dos serviços no preto, com os posts da dot voando atrás.
const PILULAS = [
  {t: 'Google Ads', q: () => em('google'), tipo: 'vidro'},
  {t: 'Landing pages', q: () => em('landing'), tipo: 'vidro'},
  {t: 'Sites', q: () => em('sites'), tipo: 'busca'},
  {t: 'Perfil no Google', q: () => em('perfil'), tipo: 'mapa'},
] as const;
const Pilula: React.FC<{texto: string; tipo: string; frame: number; q: number; tam?: number}> = ({texto, tipo, frame, q, tam = 84}) => {
  const n = tipo === 'busca' ? Math.round(interpolate(frame, [q, q + 10], [0, texto.length], FIXO)) : texto.length;
  const busca = tipo === 'busca';
  return (
    <div style={{display: 'inline-flex', alignItems: 'center', gap: 20, padding: `${tam * 0.22}px ${tam * (busca ? 0.18 : 0.42)}px ${tam * 0.22}px ${tam * 0.42}px`, borderRadius: 999, background: busca ? `linear-gradient(90deg, ${C.vivo}, ${C.claro})` : 'linear-gradient(180deg, rgba(255,255,255,0.22), rgba(255,255,255,0.05))', border: '3px solid rgba(255,255,255,0.75)', boxShadow: `inset 0 6px 14px rgba(255,255,255,0.25), 0 0 40px ${busca ? 'rgba(43,107,255,0.6)' : 'rgba(255,255,255,0.15)'}`, backdropFilter: 'blur(6px)', whiteSpace: 'nowrap'}}>
      {tipo === 'mapa' ? (
        <svg width={tam * 0.6} height={tam * 0.6} viewBox="0 0 24 24">
          <path d="M12 2 C7 2 4 6 4 10 C4 16 12 22 12 22 C12 22 20 16 20 10 C20 6 17 2 12 2 Z" fill={C.vivo} />
          <circle cx={12} cy={10} r={3} fill="#fff" />
        </svg>
      ) : null}
      <span style={{fontFamily: TIGHT, fontWeight: 600, fontSize: tam, letterSpacing: '-0.03em', color: busca ? '#06102E' : '#fff', lineHeight: 1}}>
        {texto.slice(0, n)}
        {busca && n < texto.length + 1 ? <span style={{opacity: Math.floor(frame / 6) % 2 ? 1 : 0}}>|</span> : null}
      </span>
      {busca ? (
        <span style={{display: 'inline-flex', width: tam * 1.05, height: tam * 1.05, borderRadius: '50%', backgroundColor: '#06102E', alignItems: 'center', justifyContent: 'center'}}>
          <svg width={tam * 0.5} height={tam * 0.5} viewBox="0 0 24 24">
            <circle cx={10} cy={10} r={6.5} fill="none" stroke="#fff" strokeWidth={2.6} />
            <path d="M15 15 L21 21" stroke="#fff" strokeWidth={2.6} strokeLinecap="round" />
          </svg>
        </span>
      ) : null}
    </div>
  );
};
const POSTS = ['post2', 'post1', 'post6', 'post3', 'post5', 'post4'];
const Servicos: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  // Câmera desliza da pílula atual para a próxima; no fim recua e mostra a fileira inteira.
  const ESP = 820;
  const atual = PILULAS.reduce((acc, p, k) => (frame >= p.q() - 3 ? k : acc), 0);
  const prox = Math.min(PILULAS.length - 1, atual + 1);
  const qAtual = PILULAS[atual].q() - 3;
  const qProx = PILULAS[prox].q() - 3;
  const passo = prox === atual ? 1 : interpolate(frame, [qProx - 6, qProx], [0, 1], {...FIXO, easing: Easing.inOut(Easing.cubic)});
  const recua = interpolate(frame, [em('google', 1) + 4, em('google', 1) + 18], [0, 1], {...FIXO, easing: SUAVE});
  const xCam = -(atual + (prox === atual ? 0 : passo * 0)) * ESP;
  const camX = interpolate(recua, [0, 1], [xCam, -1.5 * ESP]);
  const esc = interpolate(recua, [0, 1], [1, 0.4]);
  const borrao = frame >= qAtual && frame < qAtual + 6 ? (1 - (frame - qAtual) / 6) * 14 : 0;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Escuro t={t} />
      {/* posts da dot voando em profundidade */}
      {POSTS.map((n, k) => {
        const fase = ((t * 1.4 + k * 26) % 160) / 160;
        const z = 0.25 + fase * 1.1;
        const lado = k % 2 ? 1 : -1;
        return (
          <Img key={n} src={img(n)} style={{position: 'absolute', left: 540 + lado * (120 + fase * 380) - 150 * z, top: 960 - (k % 3 - 1) * 380 * fase - 190 * z, width: 300 * z, borderRadius: 18 * z, opacity: Math.min(1, fase * 3) * (1 - Math.max(0, fase - 0.75) * 4), filter: `blur(${Math.abs(fase - 0.5) * 10}px) brightness(0.85)`, boxShadow: '0 20px 60px rgba(0,0,0,0.6)'}} />
        );
      })}
      <AbsoluteFill style={{transform: `scale(${esc})`, transformOrigin: '50% 50%'}}>
        <div style={{position: 'absolute', left: 540 + camX, top: 960, display: 'flex', filter: `blur(${borrao}px)`}}>
          {PILULAS.map((p, k) => (
            <div key={p.t} style={{position: 'absolute', left: k * ESP, top: 0, transform: 'translate(-50%, -50%)', opacity: frame >= p.q() - 4 ? 1 : 0.0}}>
              <Pilula texto={p.t} tipo={p.tipo} frame={frame} q={p.q()} />
            </div>
          ))}
        </div>
      </AbsoluteFill>
      <Grao />
    </AbsoluteFill>
  );
};

// 4. "Conectada" em pílula branca.
const Conectada: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const e = entra(frame, em('conectada') - 4, 12);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Claro t={t} />
      <AbsoluteFill style={{display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 40}}>
        <div style={{display: 'flex', gap: 18}}>
          <Palavra texto="Cada" q={em('cada')} tam={70} cor="#5A6690" />
          <Palavra texto="peça" q={em('peca')} tam={70} cor="#5A6690" />
        </div>
        <div style={{padding: '26px 64px', borderRadius: 999, backgroundColor: '#fff', boxShadow: `0 0 0 6px rgba(255,255,255,0.5), 0 20px 60px rgba(43,107,255,0.35)`, transform: `scale(${0.8 + 0.2 * e})`, opacity: e, filter: `blur(${(1 - e) * 10}px)`}}>
          <span style={{fontFamily: TIGHT, fontWeight: 700, fontSize: 110, letterSpacing: '-0.04em', color: C.texto}}>Conectada</span>
        </div>
      </AbsoluteFill>
      <Grao />
    </AbsoluteFill>
  );
};

// 5. "Feita pra funcionar como uma só." digitado pequeno.
const UmaSo: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const z = interpolate(t, [0, fimDe(4) - de], [1, 1.25], FIXO);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Claro t={t} />
      <Bolha x={-80} y={1350} esc={1.3} giro={12} desfoque={12} tipo="chat" t={t} />
      <AbsoluteFill style={{display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${z})`}}>
        <Digita texto="Feita pra funcionar como uma só." de={em('feita')} ate={em('so') + 4} tam={58} peso={600} />
      </AbsoluteFill>
      <Grao />
    </AbsoluteFill>
  );
};

// 6. Site da dot com lupa: "Nada roda isolado."
const Isolado: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const e = entra(frame, de + 2, 14);
  const rola = interpolate(t, [0, 40], [0, -520], {...FIXO, easing: Easing.inOut(Easing.quad)});
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Claro t={t} />
      <div style={{position: 'absolute', left: 70, top: 660, width: 940, height: 600, borderRadius: 28, overflow: 'hidden', border: '10px solid #0A0F22', boxShadow: '0 40px 90px rgba(5,10,40,0.45)', transform: `translateY(${(1 - e) * 200}px) perspective(1600px) rotateY(${(1 - e) * -20}deg)`, opacity: e, backgroundColor: '#05060D'}}>
        <div style={{position: 'absolute', left: 0, top: rola, width: 920}}>
          <Img src={img('site1')} style={{width: 920, display: 'block'}} />
          <Img src={img('site2')} style={{width: 920, display: 'block'}} />
        </div>
      </div>
      <svg width={180} height={180} viewBox="0 0 24 24" style={{position: 'absolute', left: 90 + Math.sin(t / 8) * 20, top: 1150 + Math.cos(t / 8) * 14, filter: 'drop-shadow(0 10px 20px rgba(43,107,255,0.5))'}}>
        <circle cx={10} cy={10} r={6.5} fill="rgba(255,255,255,0.35)" stroke={C.vivo} strokeWidth={2.4} />
        <path d="M15 15 L21 21" stroke={C.vivo} strokeWidth={3} strokeLinecap="round" />
      </svg>
      <div style={{position: 'absolute', left: 90, top: 540, display: 'flex', gap: 18}}>
        <Palavra texto="Nada" q={em('nada')} tam={90} peso={800} italico />
        <Palavra texto="roda" q={em('roda')} tam={90} peso={800} italico />
      </div>
      <div style={{position: 'absolute', right: 90, top: 1290}}>
        <Palavra texto="isolado." q={em('isolado')} tam={90} peso={800} italico cor={C.vivo} />
      </div>
      <Grao />
    </AbsoluteFill>
  );
};

// 7. Posts da dot passando: "Nada fica no achismo."
const Achismo: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const desliza = interpolate(t, [0, fimDe(6) - de], [300, -1500], {...FIXO, easing: Easing.inOut(Easing.cubic)});
  const vel = Math.abs(interpolate(t, [0, (fimDe(6) - de) / 2, fimDe(6) - de], [0, 1, 0], FIXO));
  const ordem = ['post2', 'post3', 'post6', 'post5', 'post1', 'post4'];
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Claro t={t} />
      <div style={{position: 'absolute', left: desliza, top: 700, display: 'flex', gap: 50, filter: `blur(${vel * 6}px)`}}>
        {ordem.map((n) => (
          <Img key={n} src={img(n)} style={{width: 480, height: 600, objectFit: 'cover', borderRadius: 26, border: '8px solid #0A0F22', boxShadow: '0 30px 70px rgba(5,10,40,0.4)'}} />
        ))}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 520, display: 'flex', justifyContent: 'center', gap: 18}}>
        <Palavra texto="Nada" q={em('nada', 1)} tam={80} peso={700} italico cor="#5A6690" />
        <Palavra texto="fica no" q={em('fica')} tam={80} peso={700} italico cor="#5A6690" />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1360, textAlign: 'center'}}>
        <Palavra texto="achismo." q={em('achismo')} tam={130} peso={800} italico cor={C.texto} />
      </div>
      <Grao />
    </AbsoluteFill>
  );
};

// 8. "Isso não é teoria": tabelas de resultado do Google Ads empilhadas em 3D.
const LINHAS_ADS = [
  ['Cliques', '1.054', 'CPC', 'R$ 1,92', 'Conversões', '87'],
  ['Cliques', '2.318', 'CPC', 'R$ 1,64', 'Conversões', '163'],
  ['Cliques', '3.902', 'CPC', 'R$ 1,41', 'Conversões', '298'],
  ['Cliques', '1.770', 'CPC', 'R$ 1,73', 'Conversões', '121'],
  ['Cliques', '940', 'CPC', 'R$ 2,05', 'Conversões', '64'],
];
const Teoria: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const giro = interpolate(t, [0, 50], [55, 18], {...FIXO, easing: SUAVE});
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Escuro t={t} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 480, display: 'flex', justifyContent: 'center', gap: 16}}>
        <Palavra texto="Isso" q={em('isso')} tam={78} peso={600} cor="#fff" />
        <Palavra texto="não é" q={em('nao')} tam={78} peso={500} cor="#C9D3F0" italico />
        <Palavra texto="teoria" q={em('teoria')} tam={78} peso={800} cor="#fff" italico />
      </div>
      <div style={{position: 'absolute', left: 140, top: 640, width: 800, perspective: 1400}}>
        <div style={{transform: `rotateX(${giro}deg)`, transformOrigin: '50% 50%'}}>
          {LINHAS_ADS.map((l, k) => {
            const e = entra(frame, de + 4 + k * 3, 10);
            const destaque = k === 2;
            return (
              <div key={k} style={{display: 'flex', justifyContent: 'space-between', margin: '0 auto 22px', width: destaque ? 800 : 720 - Math.abs(k - 2) * 40, padding: '22px 30px', borderRadius: 14, backgroundColor: destaque ? '#F4F6FB' : '#B9BFCF', opacity: e * (destaque ? 1 : 0.75), transform: `translateY(${(1 - e) * 60}px)`, filter: destaque ? 'none' : 'blur(1px)', boxShadow: destaque ? `0 0 50px rgba(61,110,245,0.5)` : 'none', fontFamily: INTER}}>
                {[0, 2, 4].map((i) => (
                  <div key={i}>
                    <div style={{fontSize: 20, color: '#5A6690', fontWeight: 600}}>{l[i]} ⇅</div>
                    <div style={{fontSize: destaque ? 36 : 30, color: i === 4 && destaque ? C.vivo : '#0A1230', fontWeight: 700}}>{l[i + 1]}</div>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </div>
      <Grao />
    </AbsoluteFill>
  );
};

// 9. "crescimento" gigante passando pela câmera + "não fica por conta da sorte|".
const Sorte: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const q = em('crescimento', 1);
  const z = interpolate(frame, [q - 10, q + 34], [0.5, 4.5], {...FIXO, easing: Easing.in(Easing.quad)});
  const some = interpolate(frame, [q + 20, q + 34], [1, 0], FIXO);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Escuro t={t} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: TIGHT, fontWeight: 700, fontSize: 64, letterSpacing: '-0.04em', color: '#C9D3F0', opacity: entra(frame, em('acontece') - 2, 8) * (1 - entra(frame, q - 4, 6))}}>
        É o que acontece quando o
      </div>
      <AbsoluteFill style={{display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${z})`, opacity: frame >= q - 6 ? some : 0, filter: `blur(${Math.max(0, z - 1.6) * 3}px)`}}>
        <span style={{fontFamily: TIGHT, fontWeight: 800, fontSize: 200, letterSpacing: '-0.05em', color: '#fff', textShadow: '0 0 40px rgba(143,176,255,0.6)'}}>crescimento</span>
      </AbsoluteFill>
      <AbsoluteFill style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {frame >= em('nao', 1) - 2 ? <Digita texto="não fica por conta da sorte." de={em('nao', 1) - 2} ate={em('sorte') + 6} tam={64} peso={700} cor="#fff" /> : null}
      </AbsoluteFill>
      <Grao />
    </AbsoluteFill>
  );
};

// 10. Logo em pílula + manifesto digitado.
const Fecho: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const e = entra(frame, em('dot') - 3, 12);
  const frase1 = em('a', 2);
  const frase2 = em('a', 3);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Claro t={t} />
      <Bolha x={760} y={1380} esc={1.2} giro={-14} desfoque={12} tipo="chat" t={t} />
      <Bolha x={-40} y={420} esc={0.9} giro={16} desfoque={8} tipo="play" t={t} />
      <AbsoluteFill style={{display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 46}}>
        <div style={{display: 'flex', alignItems: 'flex-end', padding: '24px 56px 30px', borderRadius: 999, backgroundColor: 'rgba(255,255,255,0.55)', border: '3px solid #fff', boxShadow: '0 20px 60px rgba(43,107,255,0.35)', transform: `scale(${0.85 + 0.15 * e})`, opacity: e, filter: `blur(${(1 - e) * 10}px)`}}>
          <span style={{fontFamily: INTER, fontWeight: 900, fontSize: 150, letterSpacing: '-0.05em', lineHeight: 1, color: C.texto}}>dot</span>
          <span style={{display: 'inline-block', width: 40, height: 40, borderRadius: '50%', backgroundColor: C.vivo, marginLeft: 4, marginBottom: 17, boxShadow: `0 0 20px ${C.vivo}`}} />
        </div>
        <div style={{height: 64, opacity: frame >= frase2 - 2 ? 0.55 : 1}}>{frame >= frase1 - 2 ? <Digita texto="A gente não faz um pouco de tudo." de={frase1 - 2} ate={em('tudo') + 4} tam={50} peso={600} cursor={frame < frase2 - 2} /> : null}</div>
        <div style={{height: 70}}>{frame >= frase2 - 2 ? <Digita texto="A gente faz o que traz cliente." de={frase2 - 2} ate={em('cliente') + 6} tam={58} peso={700} /> : null}</div>
      </AbsoluteFill>
      <Grao />
    </AbsoluteFill>
  );
};

const Som: React.FC<{nome: string; q: number; volume: number}> = ({nome, q, volume}) => (
  <Sequence from={Math.max(0, q)} layout="none">
    <Audio src={staticFile(`sons/${nome}.mp3`)} volume={volume} />
  </Sequence>
);

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  let i = 0;
  while (i + 1 < CENAS.length && frame >= CENAS[i + 1]) i++;
  const de = CENAS[i];
  const cenas = [Maioria, Constroi, Servicos, Conectada, UmaSo, Isolado, Achismo, Teoria, Sorte, Fecho];
  const Cena = cenas[i];
  // Corte com borrão de movimento rápido, como na referência.
  const corte = interpolate(frame - de, [0, 6], [1, 0], FIXO);
  return (
    <AbsoluteFill style={{backgroundColor: '#020308'}}>
      <AbsoluteFill style={{transform: `scale(${1 + corte * 0.08})`, filter: corte > 0.05 ? `blur(${corte * 14}px)` : 'none'}}>
        <Cena de={de} />
      </AbsoluteFill>
      <Sequence from={VOZ} layout="none">
        <Audio src={staticFile(`${PASTA}/voz.mp3`)} />
      </Sequence>
      <Audio src={staticFile('trilhas/aylex-worlds-freetouse.mp3')} volume={(f) => interpolate(f, [0, 10, DURACAO - 15, DURACAO], [0, 0.09, 0.09, 0], FIXO)} />
      {CENAS.slice(1).map((c) => (
        <Som key={c} nome="whoosh" q={c - 2} volume={0.07} />
      ))}
      {PILULAS.map((p) => (
        <Som key={p.t} nome="pop" q={p.q() - 3} volume={0.08} />
      ))}
      <Som nome="ding" q={em('dot') - 2} volume={0.1} />
    </AbsoluteFill>
  );
};
