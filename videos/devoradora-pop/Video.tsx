// dot. — "A devoradora": recriação do anúncio em colagem pop-art retrô, praticamente igual à referência.
// Mesma paleta vibrante (amarelo, rosa, laranja, arco-íris, preto, creme, vinho); só o vermelho de fundo vira o azul da dot.
// Tudo com cara de impresso: grão animado, poeira, manchas de papel e vinheta em todas as cenas (fundos inclusive),
// recortes posterizados com retícula (tratados em fx.py) e títulos em Anton com sombra dura.
// Cenas: a devoradora come o orçamento → dinheiro queimando → TVs "IGUAL." → o dedão decide → anúncio mediano
// (arco-íris) → "isso não é alcance" → cérebro (Nielsen) → o homem-câmera → trompetes → estouro com a dot.
// Narração ElevenLabs eleven_v4 (voz Moutella).
import {loadFont as carregarAnton} from '@remotion/google-fonts/Anton';
import {loadFont as carregarBangers} from '@remotion/google-fonts/Bangers';
import {loadFont as carregarInter} from '@remotion/google-fonts/Inter';
import {loadFont as carregarMono} from '@remotion/google-fonts/JetBrainsMono';
import {loadFont as carregarLora} from '@remotion/google-fonts/Lora';
import {loadFont as carregarMarker} from '@remotion/google-fonts/PermanentMarker';
import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, random, spring, staticFile, useCurrentFrame} from 'remotion';
import audio from './audio.json';

const {fontFamily: ANTON} = carregarAnton('normal', {weights: ['400'], subsets: ['latin']});
const {fontFamily: BANGERS} = carregarBangers('normal', {weights: ['400'], subsets: ['latin']});
const {fontFamily: INTER} = carregarInter('normal', {weights: ['500', '700', '900'], subsets: ['latin']});
const {fontFamily: MONO} = carregarMono('normal', {weights: ['500'], subsets: ['latin']});
const {fontFamily: LORA} = carregarLora('normal', {weights: ['700'], subsets: ['latin']});
const {fontFamily: LORA_IT} = carregarLora('italic', {weights: ['700'], subsets: ['latin']});
const {fontFamily: MARKER} = carregarMarker('normal', {weights: ['400'], subsets: ['latin']});

export const FPS = 30;
const FIXO = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const SUAVE = Easing.bezier(0.16, 1, 0.3, 1);
// Paleta da referência com o vermelho trocado pelo azul da dot.
const C = {
  azul: '#2F6BFF',
  azulRef: '#1D4FE0',
  marinho: '#0B1A4A',
  amarelo: '#FFD21F',
  rosa: '#FF5FA2',
  laranja: '#FF6A1F',
  creme: '#EFE6D6',
  preto: '#09090D',
  vinho: '#3A0E2C',
  branco: '#FFFFFF',
  claro: '#9DB4FF',
};
const PASTA = 'videos/dot-pop';
const VOZ = 6;

type P = {texto: string; quadro: number};
const palavras: P[] = audio.palavras.map((p) => ({texto: p.texto, quadro: VOZ + Math.round(p.inicio * FPS)}));
const limpa = (t: string) => t.toLowerCase().normalize('NFD').replace(/[^a-z0-9]/g, '');
// Quadro da palavra (n-ésima ocorrência).
const em = (t: string, n = 0) => {
  const lista = palavras.filter((p) => limpa(p.texto) === limpa(t));
  if (!lista[n]) throw new Error(`palavra não encontrada: ${t} #${n}`);
  return lista[n].quadro;
};

export const DURACAO = VOZ + Math.round(audio.duracao * FPS) + 45;
const CENAS = [0, em('todo'), em('mesmo'), em('voce'), em('anuncio'), em('isso'), em('nielsen') - 3, em('orcamento', 1), em('entao'), em('isso', 2)].map((q) => Math.max(0, q - 4));
const fimDe = (i: number) => (i + 1 < CENAS.length ? CENAS[i + 1] : DURACAO);

const entra = (frame: number, q: number, dur = 8) => (frame < q ? 0 : interpolate(frame, [q, q + dur], [0, 1], {...FIXO, easing: SUAVE}));
const mola = (frame: number, q: number, rigidez = 200) => (frame < q ? 0 : spring({frame: frame - q, fps: FPS, config: {damping: 11, stiffness: rigidez, mass: 0.6}}));
const img = (n: string) => staticFile(`${PASTA}/${n}.png`);
const sombra = (cor: string, d = 7) => `${d * 0.6}px ${d}px 0 ${cor}`;
const CONTORNO = (cor = '#fff', t = 6) => [0, 45, 90, 135, 180, 225, 270, 315].map((a) => `drop-shadow(${(Math.cos((a * Math.PI) / 180) * t).toFixed(1)}px ${(Math.sin((a * Math.PI) / 180) * t).toFixed(1)}px 0 ${cor})`).join(' ');

// ---------- Textura (em tudo, fundos inclusive) ----------

// Fundo de papel colorido: cor + manchas + luz no centro.
const Papel: React.FC<{cor: string; luz?: number}> = ({cor, luz = 0.12}) => (
  <>
    <AbsoluteFill style={{backgroundColor: cor}} />
    <AbsoluteFill style={{background: `radial-gradient(900px 1100px at 50% 45%, rgba(255,255,255,${luz}) 0%, rgba(255,255,255,0) 70%)`}} />
    <Img src={staticFile(`${PASTA}/manchas.jpg`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'soft-light', opacity: 0.55}} />
  </>
);

// Por cima de tudo: grão animado, poeira, riscos e vinheta.
const Textura: React.FC = () => {
  const frame = useCurrentFrame();
  const k = Math.floor(frame / 2) % 4;
  const poeira = Array.from({length: 34}, (_, i) => {
    const s = `${Math.floor(frame / 3)}-${i}`;
    return {x: random(`px${s}`) * 1080, y: random(`py${s}`) * 1920, r: 1.5 + random(`pr${s}`) * 3.5, claro: random(`pc${s}`) > 0.45};
  });
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <Img src={staticFile(`${PASTA}/grao${k}.jpg`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'overlay', opacity: 0.42}} />
      {poeira.map((p, i) => (
        <div key={i} style={{position: 'absolute', left: p.x, top: p.y, width: p.r * 2, height: p.r * 2, borderRadius: '50%', backgroundColor: p.claro ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.6)'}} />
      ))}
      {random(`risco${Math.floor(frame / 4)}`) > 0.7 ? <div style={{position: 'absolute', top: 0, bottom: 0, left: random(`rx${Math.floor(frame / 4)}`) * 1080, width: 2, backgroundColor: 'rgba(255,255,255,0.25)'}} /> : null}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse 75% 65% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.42) 100%)'}} />
    </AbsoluteFill>
  );
};

// Retícula de pontos (gradiente) para fundos.
const Pontos: React.FC<{cor: string; de?: 'baixo' | 'centro'; tam?: number; opacidade?: number}> = ({cor, de = 'baixo', tam = 26, opacidade = 0.5}) => (
  <AbsoluteFill
    style={{
      backgroundImage: `radial-gradient(${cor} 34%, transparent 38%)`,
      backgroundSize: `${tam}px ${tam}px`,
      opacity: opacidade,
      maskImage: de === 'baixo' ? 'linear-gradient(180deg, transparent 45%, #000 100%)' : 'radial-gradient(circle at 50% 50%, transparent 30%, #000 80%)',
      WebkitMaskImage: de === 'baixo' ? 'linear-gradient(180deg, transparent 45%, #000 100%)' : 'radial-gradient(circle at 50% 50%, transparent 30%, #000 80%)',
    }}
  />
);

// ---------- Peças ----------

const Estouro: React.FC<{x: number; y: number; r: number; pontas?: number; cor?: string; borda?: string; esp?: number; giro?: number; semente?: string; children?: React.ReactNode}> = ({x, y, r, pontas = 16, cor = C.amarelo, borda = C.preto, esp = 12, giro = 0, semente = 'e', children}) => {
  if (r <= 0) return null;
  const pts = Array.from({length: pontas * 2}, (_, k) => {
    const raio = k % 2 ? r * (0.6 + random(`${semente}${k}`) * 0.12) : r * (0.9 + random(`${semente}${k}`) * 0.14);
    const a = (Math.PI * k) / pontas;
    return `${(r * 1.1 + Math.cos(a) * raio).toFixed(1)},${(r * 1.1 + Math.sin(a) * raio).toFixed(1)}`;
  }).join(' ');
  return (
    <div style={{position: 'absolute', left: x - r * 1.1, top: y - r * 1.1, width: r * 2.2, height: r * 2.2, transform: `rotate(${giro}deg)`}}>
      <svg width={r * 2.2} height={r * 2.2} style={{position: 'absolute', overflow: 'visible'}}>
        <polygon points={pts} fill={cor} stroke={borda} strokeWidth={esp} strokeLinejoin="round" style={{filter: 'drop-shadow(10px 12px 0 rgba(0,0,0,0.4))'}} />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center'}}>{children}</div>
    </div>
  );
};

// Selo amarelo "IGUAL." e afins: entra batendo.
const Selo: React.FC<{x: number; y: number; texto: string; q: number; giro?: number; fundo?: string; cor?: string; tam?: number; borda?: string}> = ({x, y, texto, q, giro = -4, fundo = C.amarelo, cor = C.preto, tam = 80, borda = C.preto}) => {
  const frame = useCurrentFrame();
  if (frame < q) return null;
  const m = mola(frame, q, 300);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) rotate(${giro}deg) scale(${1.7 - 0.7 * m})`, opacity: Math.min(1, m * 2), padding: '4px 22px 0', backgroundColor: fundo, color: cor, fontFamily: ANTON, fontSize: tam, lineHeight: 1.1, whiteSpace: 'nowrap', border: `5px solid ${borda}`, boxShadow: '10px 12px 0 rgba(0,0,0,0.45)'}}>
      {texto}
    </div>
  );
};

// Linhas de título em Anton com sombra dura, entrando junto com a fala.
type Linha = {t: string; q: number; cor?: string; tam?: number};
const Titulo: React.FC<{linhas: Linha[]; x?: number; y: number; tam?: number; sombraCor?: string; alinha?: 'left' | 'center'}> = ({linhas, x = 60, y, tam = 120, sombraCor = 'rgba(0,0,0,0.55)', alinha = 'left'}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: x, right: alinha === 'center' ? x : undefined, top: y, textAlign: alinha, fontFamily: ANTON, lineHeight: 1.02, textTransform: 'uppercase'}}>
      {linhas.map((l) => {
        if (frame < l.q - 2) return <div key={l.t} style={{fontSize: l.tam ?? tam, opacity: 0}}>{l.t}</div>;
        const e = mola(frame, l.q - 2, 260);
        return (
          <div key={l.t} style={{fontSize: l.tam ?? tam, color: l.cor ?? C.branco, textShadow: sombra(sombraCor, (l.tam ?? tam) * 0.06), transform: `translateY(${(1 - e) * 30}px) scale(${0.85 + 0.15 * e})`, transformOrigin: alinha === 'center' ? '50% 50%' : '0 50%'}}>
            {l.t}
          </div>
        );
      })}
    </div>
  );
};

// ---------- Cenas ----------

// 1. A devoradora (fundo azul no lugar do vermelho).
const Devoradora: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const jantar = em('jantar');
  const solta = jantar - 8;
  const cai = interpolate(frame, [solta, jantar + 4], [0, 1], {...FIXO, easing: Easing.in(Easing.quad)});
  const balanco = Math.sin(t / 8) * 6 * (1 - cai);
  const nhac = jantar + 4;
  const telaCheia = frame >= nhac + 8;
  const zoom = interpolate(t, [0, 170], [1.0, 1.07], FIXO);
  // Pinça (entre polegar e indicador) presa no chapéu do homenzinho; braço sai para cima à esquerda.
  const PINCA = {x: 330, y: 640};
  const W = 760;
  const px = (29 * W) / 900;
  const py = (149 * W) / 900;
  const BOCA = {x: 400, y: 1330};
  const fim = fimDe(0);
  const branco = interpolate(frame, [fim - 8, fim], [0, 1], FIXO);
  if (telaCheia) {
    const m = 0.55 + 0.45 * mola(frame, nhac + 8, 260);
    return (
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <Papel cor={C.amarelo} />
        <Img src={img('devoradora')} style={{position: 'absolute', left: -500, top: 100, width: 2300, transform: `scale(${1 + (frame - nhac) * 0.012})`, transformOrigin: '25% 45%'}} />
        <Estouro x={540} y={960} r={600 * m} pontas={14} cor={C.amarelo} borda={C.preto} esp={16} giro={-8 + (frame - nhac) * 0.4} semente="nhac">
          <span style={{fontFamily: BANGERS, fontSize: 300 * m, color: C.azul, WebkitTextStroke: `10px ${C.preto}`, transform: 'rotate(-8deg)', display: 'inline-block', textShadow: sombra(C.preto, 14)}}>NHAC!</span>
        </Estouro>
        {[0, 1, 2, 3, 4].map((k) => (
          <Img key={k} src={img('pilha')} style={{position: 'absolute', left: 100 + random(`nb${k}`) * 700, top: 1300 + random(`nby${k}`) * 300 - (frame - nhac) * (8 + k * 3), width: 220, transform: `rotate(${(frame - nhac) * (k % 2 ? 6 : -5)}deg)`}} />
        ))}
        <AbsoluteFill style={{backgroundColor: '#fff', opacity: branco}} />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.azul} />
      <AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: '30% 70%'}}>
        <Img src={img('devoradora')} style={{position: 'absolute', left: 80, top: 780, width: 1000}} />
        {frame >= em('anuncios') - 2 ? (
          <div style={{position: 'absolute', left: 230, top: 1110, padding: '10px 22px', backgroundColor: C.marinho, color: C.branco, fontFamily: INTER, fontWeight: 900, fontSize: 38, transform: `rotate(-14deg) scaleX(${entra(frame, em('anuncios') - 2, 6)})`, transformOrigin: '0 50%'}}>SEUS ANÚNCIOS MEDIANOS</div>
        ) : null}
        {frame >= em('anuncios') + 6 ? (
          <svg width={140} height={180} style={{position: 'absolute', left: 430, top: 1170, overflow: 'visible'}}>
            <path d="M 60 0 C 90 50, 20 80, 50 150" fill="none" stroke={C.preto} strokeWidth={6} strokeLinecap="round" strokeDasharray={200} strokeDashoffset={200 * (1 - entra(frame, em('anuncios') + 6, 10))} />
            <path d="M 30 130 L 50 152 L 72 128" fill="none" stroke={C.preto} strokeWidth={6} strokeLinecap="round" opacity={entra(frame, em('anuncios') + 14, 4)} />
          </svg>
        ) : null}
        {frame < nhac ? (
          <div style={{position: 'absolute', left: PINCA.x - 70, top: PINCA.y + 4, width: 150, transform: `translate(${(BOCA.x - PINCA.x) * cai}px, ${(BOCA.y - PINCA.y) * cai}px) rotate(${balanco + cai * 40}deg) scale(${1 - cai * 0.55})`, transformOrigin: '50% 0'}}>
            <Img src={img('homenzinho')} style={{width: 150, filter: CONTORNO('#fff', 3)}} />
            {frame >= em('orcamento') - 2 ? (
              <div style={{position: 'absolute', left: 40, top: 70, padding: '4px 12px', backgroundColor: C.branco, color: C.preto, fontFamily: INTER, fontWeight: 900, fontSize: 26, border: `3px solid ${C.preto}`, whiteSpace: 'nowrap', transform: `rotate(-6deg) scale(${mola(frame, em('orcamento') - 2)})`}}>SEU ORÇAMENTO</div>
            ) : null}
          </div>
        ) : null}
        <Img src={img('mao')} style={{position: 'absolute', left: PINCA.x - px, top: PINCA.y - py - cai * 220, width: W, transform: `rotate(${187 + balanco * 0.3}deg)`, transformOrigin: `${px}px ${py}px`}} />
      </AbsoluteFill>
      <div style={{position: 'absolute', right: 60, top: 230, textAlign: 'right', opacity: entra(frame, de + 2, 10)}}>
        <div style={{fontFamily: LORA, fontWeight: 700, fontSize: 74, color: C.marinho, letterSpacing: '0.01em'}}>ELA É UMA...</div>
        <div style={{fontFamily: LORA_IT, fontStyle: 'italic', fontWeight: 700, fontSize: 118, color: C.marinho, marginTop: -16, opacity: entra(frame, em('devoradora') - 2, 8)}}>Devoradora!</div>
      </div>
      {frame >= nhac ? (
        <Estouro x={BOCA.x - 110} y={BOCA.y + 40} r={190 * mola(frame, nhac, 320)} pontas={12} cor={C.amarelo} borda={C.preto} giro={-12} semente="ch">
          <span style={{fontFamily: BANGERS, fontSize: 96, color: C.azul, WebkitTextStroke: `4px ${C.preto}`}}>NHAC!</span>
        </Estouro>
      ) : null}
    </AbsoluteFill>
  );
};

// Chamas de desenho em camadas, tremendo.
const Chamas: React.FC<{x: number; base: number; larg: number; alt: number; t: number}> = ({x, base, larg, alt, t}) => {
  const camada = (cor: string, esc: number, sem: string, fase: number) => {
    const n = 9;
    const pts: string[] = [`${x - (larg * esc) / 2},${base}`];
    for (let k = 0; k <= n; k++) {
      const fx = x - (larg * esc) / 2 + ((larg * esc) / n) * k;
      const pico = k % 2 === 0;
      const meio = 1 - Math.abs(k - n / 2) / (n / 2);
      const h = pico ? alt * esc * (0.45 + meio * 0.6) * (0.85 + 0.15 * Math.sin(t / 3 + k * 1.7 + fase) + random(`${sem}${k}`) * 0.1) : alt * esc * 0.25 * (0.6 + meio);
      pts.push(`${fx.toFixed(1)},${(base - h).toFixed(1)}`);
    }
    pts.push(`${x + (larg * esc) / 2},${base}`);
    return <polygon key={sem} points={pts.join(' ')} fill={cor} stroke={C.preto} strokeWidth={esc === 1 ? 5 : 0} strokeLinejoin="round" />;
  };
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      {camada('#E8361C', 1, 'c1', 0)}
      {camada(C.laranja, 0.78, 'c2', 1)}
      {camada('#FFB21F', 0.55, 'c3', 2)}
      {camada('#FFF1A0', 0.3, 'c4', 3)}
    </svg>
  );
};

// 2. Dinheiro queimando.
const Queima: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const valor = Math.round(interpolate(t, [0, 25, 110, 140], [0, 10120, 46000, 48750], {...FIXO, easing: Easing.out(Easing.quad)}));
  const cresce = interpolate(t, [0, 40], [0.35, 1], {...FIXO, easing: SUAVE});
  const fim = fimDe(1);
  const glitch = frame > fim - 12;
  const flash = interpolate(t, [0, 8], [1, 0], FIXO);
  const pilhas = [
    {x: 120, y: 1500, w: 440},
    {x: 520, y: 1500, w: 440},
    {x: 300, y: 1330, w: 480},
    {x: 220, y: 1180, w: 360},
    {x: 520, y: 1180, w: 340},
    {x: 360, y: 1030, w: 360},
    {x: 0, y: 1660, w: 520},
    {x: 560, y: 1660, w: 520},
  ];
  const cena = (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.preto} luz={0.05} />
      <AbsoluteFill style={{background: 'radial-gradient(600px 700px at 50% 70%, rgba(255,106,31,0.35), rgba(0,0,0,0) 70%)'}} />
      <AbsoluteFill style={{transform: `scale(${cresce})`, transformOrigin: '50% 100%'}}>
        <Chamas x={540} base={1240} larg={820} alt={760} t={t} />
        {pilhas.map((p, k) => (
          <Img key={k} src={img('pilha')} style={{position: 'absolute', left: p.x, top: p.y, width: p.w, transform: `rotate(${(k % 3) * 4 - 4}deg)`}} />
        ))}
      </AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, top: 180, textAlign: 'center', fontFamily: INTER, fontWeight: 900, fontSize: 30, letterSpacing: '0.08em', color: C.branco}}>QUEIMADO EM ANÚNCIOS ESTE MÊS</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 215, textAlign: 'center', fontFamily: ANTON, fontSize: 150, color: C.branco, textShadow: sombra(C.azul, 10), opacity: entra(frame, de + 4, 6)}}>R$ {valor.toLocaleString('pt-BR')}</div>
      {frame >= em('mes') ? <div style={{position: 'absolute', left: 70, top: 430, fontFamily: ANTON, fontSize: 70, color: C.branco, textShadow: sombra('#000', 5), transform: `scale(${mola(frame, em('mes'))})`, transformOrigin: '0 50%'}}>TODO. MÊS.</div> : null}
      <Selo x={840} y={480} texto="VENDAS: 0" q={em('queimam')} giro={-6} fundo="transparent" cor={C.azul} borda={C.azul} tam={52} />
      <Titulo linhas={[{t: 'MILHARES', q: em('milhares'), cor: C.amarelo}]} x={0} y={520} tam={190} sombraCor={C.azul} alinha="center" />
      {frame >= em('ninguem') - 2 ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 750, textAlign: 'center', fontFamily: MARKER, fontSize: 70, color: C.branco, transform: `rotate(-4deg) scale(${mola(frame, em('ninguem') - 2)})`, textShadow: '4px 5px 0 rgba(0,0,0,0.7)'}}>NINGUÉM LEMBRA.</div>
      ) : null}
      <AbsoluteFill style={{backgroundColor: '#fff', opacity: flash}} />
    </AbsoluteFill>
  );
  if (!glitch) return cena;
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: '#000'}}>
      {Array.from({length: 10}, (_, k) => (
        <AbsoluteFill key={k} style={{clipPath: `inset(${k * 10}% 0 ${100 - (k + 1) * 10}% 0)`, transform: `translateX(${(random(`g${k}${frame}`) - 0.5) * 120}px)`, filter: k % 3 === 0 ? 'grayscale(1) contrast(1.6)' : 'none'}}>
          {cena}
        </AbsoluteFill>
      ))}
      <AbsoluteFill style={{backgroundColor: '#888', mixBlendMode: 'screen', opacity: interpolate(frame, [fim - 12, fim], [0, 0.6], FIXO)}} />
    </AbsoluteFill>
  );
};

// 3. Três TVs roxas, tudo "IGUAL.".
const TV = {larg: 640, alt: 466, tela: {x: 43, y: 39, w: 411, h: 315}};
const Tela: React.FC<{tipo: number; frame: number; chiado: boolean}> = ({tipo, frame, chiado}) => {
  if (chiado) {
    return (
      <AbsoluteFill style={{backgroundColor: '#777', overflow: 'hidden'}}>
        {Array.from({length: 36}, (_, k) => (
          <div key={k} style={{position: 'absolute', left: 0, right: 0, top: `${(k * 100) / 36}%`, height: `${100 / 36}%`, backgroundColor: random(`c${k}${frame}`) > 0.5 ? '#d8d8d8' : '#2a2a2a'}} />
        ))}
      </AbsoluteFill>
    );
  }
  if (tipo === 0) {
    return (
      <AbsoluteFill style={{background: 'linear-gradient(180deg, #CFE0FF, #7FA0E8)'}}>
        <div style={{position: 'absolute', left: 12, top: 10, padding: '2px 8px', backgroundColor: C.marinho, color: '#fff', fontFamily: INTER, fontWeight: 900, fontSize: 15}}>BANCO DE IMAGEM™</div>
        <Img src={img('executivo')} style={{position: 'absolute', left: 10, top: 40, height: 420}} />
        <Img src={img('executivo')} style={{position: 'absolute', left: 230, top: 40, height: 420, transform: 'scaleX(-1)'}} />
      </AbsoluteFill>
    );
  }
  if (tipo === 1) {
    return (
      <AbsoluteFill style={{background: `linear-gradient(160deg, #22307A, ${C.marinho})`, fontFamily: ANTON, color: '#fff', padding: '50px 30px'}}>
        <div style={{fontSize: 60, lineHeight: 1}}>QUALIDADE</div>
        <div style={{fontSize: 60, lineHeight: 1}}>PREMIUM</div>
        <div style={{fontFamily: INTER, fontWeight: 700, fontSize: 15, marginTop: 10}}>★ CONFIADO POR MILHÕES</div>
        <div style={{position: 'absolute', right: 26, top: 70, width: 90, height: 90, borderRadius: '50%', backgroundColor: C.amarelo, color: C.preto, fontFamily: ANTON, fontSize: 30, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: 'rotate(-14deg)', border: `3px solid ${C.preto}`}}>1998</div>
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{background: `linear-gradient(160deg, #3A22A0, ${C.marinho})`, fontFamily: ANTON, color: '#fff', padding: '40px 30px'}}>
      <div style={{fontSize: 70, color: C.amarelo, transform: 'rotate(-4deg)', display: 'inline-block'}}>NOVO!!!</div>
      <div style={{fontFamily: INTER, fontWeight: 700, fontSize: 18, marginTop: 8}}>MARCA™ — AGORA COM MAIS MARCA</div>
      <div style={{position: 'absolute', right: 24, bottom: 22, padding: '4px 12px', backgroundColor: '#fff', color: C.preto, fontFamily: INTER, fontWeight: 900, fontSize: 15}}>COMPRE JÁ ›</div>
    </AbsoluteFill>
  );
};
const Tvs: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const q = [em('banco'), em('qualidade'), em('pulo')];
  const chiado = frame >= em('pulo') + 8;
  const fim = fimDe(2);
  const sai = interpolate(frame, [fim - 7, fim], [0, 1], {...FIXO, easing: Easing.in(Easing.quad)});
  const cursor = em('pulo');
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.azul} />
      <AbsoluteFill style={{transform: `translateX(${-sai * 1300}px)`, filter: sai > 0 ? `blur(${sai * 40}px)` : 'none'}}>
        {[0, 1, 2].map((k) => {
          const y = 120 + k * 560;
          const e = mola(frame, de + k * 3, 180);
          const ligada = frame >= q[k] - 2;
          return (
            <div key={k} style={{position: 'absolute', left: 50, top: y, width: TV.larg, height: TV.alt, transform: `translateY(${(1 - e) * 200}px)`, opacity: Math.min(1, e * 2)}}>
              <Img src={img('tv')} style={{position: 'absolute', left: 0, top: 0, width: TV.larg}} />
              <div style={{position: 'absolute', left: TV.tela.x, top: TV.tela.y, width: TV.tela.w, height: TV.tela.h, borderRadius: 36, overflow: 'hidden', backgroundColor: '#14102E'}}>
                {ligada ? <Tela tipo={k} frame={frame} chiado={chiado} /> : null}
                <AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0 2px, transparent 2px 5px)', boxShadow: 'inset 0 0 50px rgba(0,0,0,0.7)'}} />
              </div>
            </div>
          );
        })}
        <Selo x={840} y={300} texto="IGUAL." q={em('mesmo')} giro={-5} />
        <Selo x={850} y={860} texto="IGUAL." q={em('mesma')} giro={4} />
        <Selo x={840} y={1420} texto="IGUAL." q={em('mesmo', 1)} giro={-3} />
        {frame >= cursor - 6 ? (
          <svg width={70} height={92} viewBox="0 0 24 32" style={{position: 'absolute', left: interpolate(frame, [cursor - 6, cursor + 2], [1000, 470], {...FIXO, easing: SUAVE}), top: interpolate(frame, [cursor - 6, cursor + 2], [1800, 1460], {...FIXO, easing: SUAVE}), transform: `scale(${frame >= cursor + 4 && frame < cursor + 8 ? 0.8 : 1})`, filter: 'drop-shadow(4px 5px 0 rgba(0,0,0,0.45))'}}>
            <path d="M2 2 L2 26 L8 20 L12 30 L16 28 L12 18 L20 18 Z" fill="#fff" stroke="#000" strokeWidth={2} />
          </svg>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// 4. O dedão decide: mãos roxas, estouro laranja, celular com anúncios.
const MAOS = Array.from({length: 12}, (_, k) => ({ang: (k / 12) * 360 + random(`ma${k}`) * 18, dist: 560 + random(`md${k}`) * 180, esc: 0.8 + random(`me${k}`) * 0.4}));
const CEL = {larg: 1100, tela: {x: 164, y: 63, w: 249, h: 424}};
const Dedao: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const seg = Math.max(0, interpolate(t, [8, 105], [1.7, 0.0], FIXO));
  const rola = (t * 10) % 300;
  const f = CEL.larg / 800;
  const cards = [
    {t: '50% OFF!!', f: C.amarelo, c: C.azul},
    {t: 'PREMIUM', f: C.branco, c: C.preto},
    {t: 'NOVO LANÇAMENTO', f: C.preto, c: C.amarelo},
    {t: '#1 MARCA', f: C.rosa, c: C.preto},
    {t: 'NÓS SOMOS...', f: C.azul, c: C.branco},
  ];
  const fim = fimDe(3);
  const sai = interpolate(frame, [fim - 7, fim], [0, 1], {...FIXO, easing: Easing.in(Easing.quad)});
  const entraBorrao = interpolate(t, [0, 6], [1, 0], FIXO);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.azulRef} />
      <AbsoluteFill style={{transform: `translateX(${(entraBorrao - sai) * 900}px)`, filter: entraBorrao + sai > 0.02 ? `blur(${(entraBorrao + sai) * 40}px)` : 'none'}}>
        <Estouro x={540} y={1120} r={700} pontas={18} cor={C.laranja} borda={C.laranja} esp={0} giro={t * 0.5} semente="dd" />
        <Estouro x={540} y={1120} r={470} pontas={14} cor="#FF8A3D" borda="#FF8A3D" esp={0} giro={-t * 0.7} semente="dd2" />
        {MAOS.map((m, k) => {
          const a = (m.ang * Math.PI) / 180;
          const avanca = Math.sin(t / 6 + k) * 30 + interpolate(t, [0, 110], [90, 0], FIXO);
          const x = 540 + Math.cos(a) * (m.dist + avanca);
          const y = 1120 + Math.sin(a) * (m.dist + avanca);
          return <Img key={k} src={img('agarra')} style={{position: 'absolute', left: x - 350 * m.esc, top: y - 184 * m.esc, width: 700 * m.esc, transform: `rotate(${m.ang + 180}deg)`}} />;
        })}
        <div style={{position: 'absolute', left: 540 - (CEL.tela.x + CEL.tela.w / 2) * f, top: 1140 - (CEL.tela.y + CEL.tela.h / 2) * f, width: CEL.larg}}>
          <div style={{position: 'absolute', left: CEL.tela.x * f, top: CEL.tela.y * f, width: CEL.tela.w * f, height: CEL.tela.h * f, borderRadius: 30, overflow: 'hidden', backgroundColor: '#fff'}}>
            {cards.concat(cards).map((c, k) => (
              <div key={k} style={{position: 'absolute', left: 14, right: 14, top: 18 + k * 120 - rola, height: 104, backgroundColor: c.f, color: c.c, fontFamily: ANTON, fontSize: 40, lineHeight: 1, display: 'flex', alignItems: 'center', paddingLeft: 16, border: `3px solid ${C.preto}`}}>
                {c.t}
              </div>
            ))}
          </div>
          <Img src={img('celular')} style={{position: 'absolute', left: 0, top: 0, width: CEL.larg, mixBlendMode: 'normal', clipPath: `polygon(0 0, 100% 0, 100% 100%, 0 100%, 0 0, ${(CEL.tela.x / 800) * 100}% ${(CEL.tela.y / 721) * 100}%, ${(CEL.tela.x / 800) * 100}% ${((CEL.tela.y + CEL.tela.h) / 721) * 100}%, ${((CEL.tela.x + CEL.tela.w) / 800) * 100}% ${((CEL.tela.y + CEL.tela.h) / 721) * 100}%, ${((CEL.tela.x + CEL.tela.w) / 800) * 100}% ${(CEL.tela.y / 721) * 100}%, ${(CEL.tela.x / 800) * 100}% ${(CEL.tela.y / 721) * 100}%)`}} />
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 130, textAlign: 'center'}}>
          <div style={{fontFamily: INTER, fontWeight: 900, fontSize: 36, color: C.branco, letterSpacing: '0.1em', textShadow: sombra('#000', 4)}}>VOCÊ TEM</div>
          <div style={{fontFamily: ANTON, fontSize: 250, lineHeight: 1, color: C.branco, textShadow: sombra(C.marinho, 14)}}>{seg.toFixed(1).replace('.', ',')}s</div>
          <div style={{fontFamily: INTER, fontWeight: 900, fontSize: 32, color: C.branco, letterSpacing: '0.06em', textShadow: sombra('#000', 4)}}>ANTES DO DEDÃO DECIDIR</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// 5. Anúncio mediano: arco-íris em zigue-zague, o cara posterizado, métricas e "DE NOVO.".
const ARCO = ['#E8361C', C.laranja, C.amarelo, '#2DB34A', '#19B5E0', C.azul, '#7A3FD6', C.rosa];
const Mediano: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const anel = (r: number, k: number) => {
    const n = 26;
    const pts = Array.from({length: n * 2}, (_, j) => {
      const a = (Math.PI * j) / n + t * 0.008 * (k % 2 ? 1 : -1);
      const rr = j % 2 ? r : r * 0.9;
      return `${(540 + Math.cos(a) * rr).toFixed(1)},${(1130 + Math.sin(a) * rr).toFixed(1)}`;
    }).join(' ');
    return <polygon key={k} points={pts} fill={ARCO[k % ARCO.length]} />;
  };
  const novos = [em('novo'), em('novo', 1)];
  const fim = fimDe(4);
  const mosaico = frame > fim - 8;
  const palavrasSoltas = [
    {t: 'e de novo', x: 640, y: 300},
    {t: 'impulsionar', x: 760, y: 610},
    {t: 'frequência', x: 700, y: 760},
    {t: 'alcance?', x: 110, y: 900},
    {t: 'remarketing', x: 80, y: 1500},
  ];
  return (
    <AbsoluteFill style={{overflow: 'hidden', filter: mosaico ? `blur(${(frame - (fim - 8)) * 2}px) contrast(1.4)` : 'none'}}>
      <Papel cor="#E8361C" />
      <svg width={1080} height={1920} style={{position: 'absolute', transform: `scale(${1.05 + Math.sin(t / 10) * 0.03})`}}>
        {Array.from({length: 16}, (_, k) => 2000 - k * 120).map(anel)}
      </svg>
      {palavrasSoltas.map((p, k) => (
        <div key={k} style={{position: 'absolute', left: p.x, top: p.y, fontFamily: MONO, fontSize: 26, color: C.preto, opacity: 0.6 * entra(frame, de + 6 + k * 6, 8)}}>
          {p.t}
        </div>
      ))}
      <Img src={img('estresse')} style={{position: 'absolute', left: 40, top: 880, width: 1000}} />
      <Titulo linhas={[{t: 'ANÚNCIO MEDIANO NÃO SOBREVIVE', q: em('anuncio'), tam: 74}, {t: '2 SEGUNDOS.', q: em('dois', 1), cor: C.amarelo, tam: 130}]} x={50} y={150} sombraCor={C.preto} />
      {[
        {r: 'CTR', v: '0,3%', x: 70, y: 470, q: em('mediano')},
        {r: 'ROAS', v: '0,4x', x: 620, y: 520, q: em('sobrevive')},
        {r: 'FREQ.', v: '9,4x', x: 120, y: 600, q: em('paga')},
      ].map((c) =>
        frame >= c.q ? (
          <div key={c.r} style={{position: 'absolute', left: c.x, top: c.y, padding: '8px 18px', backgroundColor: C.preto, fontFamily: MONO, fontSize: 34, color: C.branco, transform: `scale(${mola(frame, c.q, 300)})`, border: '2px solid #fff'}}>
            {c.r} <span style={{color: C.amarelo}}>{c.v}</span>
          </div>
        ) : null,
      )}
      {novos.map((q, n) =>
        Array.from({length: n === 0 ? 3 : 8}, (_, k) => {
          const qq = q + k * 2;
          if (frame < qq) return null;
          const m = mola(frame, qq, 320);
          const desl = (random(`gl${n}${k}${Math.floor(frame / 2)}`) - 0.5) * 16;
          return (
            <div key={`${n}${k}`} style={{position: 'absolute', left: 30 + random(`nx${n}${k}`) * 520, top: 640 + random(`ny${n}${k}`) * 820, transform: `rotate(${(random(`nr${n}${k}`) - 0.5) * 28}deg) scale(${m})`, fontFamily: ANTON, fontSize: 150, color: C.branco, WebkitTextStroke: `4px ${C.preto}`, textShadow: `${desl}px 0 0 ${C.rosa}, ${-desl}px 0 0 #19B5E0, ${sombra(C.preto, 10)}`}}>
              DE NOVO.
            </div>
          );
        }),
      )}
    </AbsoluteFill>
  );
};

// 6. "Isso não é alcance": papel creme e a devoradora em adesivo de faixas.
const Alcance: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const risca = entra(frame, em('alcance') + 8, 8);
  const fim = fimDe(5);
  const pontos = interpolate(frame, [fim - 12, fim], [0, 1], {...FIXO, easing: Easing.in(Easing.quad)});
  const sobe = mola(frame, de, 120);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.creme} luz={0.2} />
      <div style={{position: 'absolute', left: 60, top: 150, fontFamily: ANTON, fontSize: 64, color: C.preto}}>ISSO NÃO É</div>
      <div style={{position: 'absolute', left: 60, top: 215, fontFamily: ANTON, fontSize: 180, lineHeight: 1, color: C.preto, opacity: entra(frame, em('alcance') - 2, 6)}}>
        ALCANCE.
        <div style={{position: 'absolute', left: -14, top: '50%', height: 20, width: `${risca * 104}%`, backgroundColor: C.azul, transform: 'rotate(-3deg)'}} />
      </div>
      {frame >= em('isso', 1) - 2 ? (
        <div style={{position: 'absolute', left: 60, top: 420}}>
          <div style={{fontFamily: ANTON, fontSize: 64, color: C.preto, opacity: entra(frame, em('isso', 1) - 2, 6)}}>ISSO É ALIMENTAR</div>
          <div style={{fontFamily: LORA_IT, fontStyle: 'italic', fontWeight: 700, fontSize: 100, color: C.azul, marginTop: -10, opacity: entra(frame, em('devoradora', 1) - 2, 6)}}>a devoradora.</div>
        </div>
      ) : null}
      {[0, 1, 2].map((k) => (
        <Img key={k} src={img('pilha')} style={{position: 'absolute', left: 520 + k * 150 - t * (3 + k), top: 520 + k * 60 + Math.sin(t / 6 + k) * 20, width: 130, transform: `rotate(${t * (k % 2 ? 4 : -3)}deg)`, opacity: frame >= em('alimentar') ? 1 : 0}} />
      ))}
      <Img src={img('devoradora_adesivo')} style={{position: 'absolute', left: -60, top: 760 + (1 - sobe) * 600, width: 1120, transform: `rotate(${Math.sin(t / 14) * 1.5}deg)`}} />
      <AbsoluteFill style={{backgroundImage: `radial-gradient(${C.azul} ${pontos * 72}%, transparent ${pontos * 72 + 2}%)`, backgroundSize: '64px 64px', opacity: pontos > 0 ? 1 : 0}} />
    </AbsoluteFill>
  );
};

// 7. O cérebro (Nielsen).
const Cerebro: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const p = Math.round(interpolate(frame, [em('quase'), em('metade') + 10], [25, 47], FIXO));
  const voa = interpolate(t, [0, 22], [0.08, 1], {...FIXO, easing: SUAVE});
  const raio = (x: number, y: number, q: number, giro: number) =>
    frame >= q && Math.floor((frame - q) / 3) % 3 !== 2 ? (
      <svg width={90} height={135} viewBox="0 0 20 30" style={{position: 'absolute', left: x, top: y, transform: `rotate(${giro}deg)`, filter: 'drop-shadow(4px 5px 0 rgba(0,0,0,0.45))'}}>
        <path d="M12 0 L2 17 L9 17 L6 30 L18 11 L11 11 Z" fill={C.amarelo} stroke={C.preto} strokeWidth={1.5} />
      </svg>
    ) : null;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.azulRef} />
      <Pontos cor="#4C7BFF" de="baixo" tam={30} opacidade={0.7} />
      <Selo x={170} y={135} texto="NIELSEN, 2017." q={em('nielsen')} giro={0} fundo={C.creme} tam={30} borda={C.preto} />
      <Selo x={860} y={135} texto="NÃO É O ORÇAMENTO." q={em('descobriu')} giro={0} fundo={C.creme} tam={30} borda={C.preto} />
      <Titulo linhas={[{t: 'CRIATIVO', q: em('criativo'), cor: C.creme}]} x={0} y={190} tam={210} sombraCor={C.marinho} alinha="center" />
      <Img src={img('cerebro')} style={{position: 'absolute', left: 150, top: 500, width: 780, transform: `scale(${voa * (1 + Math.sin(t / 8) * 0.02)}) rotate(${Math.sin(t / 12) * 2}deg)`, transformOrigin: '50% 30%', filter: 'drop-shadow(14px 18px 0 rgba(0,0,0,0.35))'}} />
      {raio(110, 520, em('criativo'), -20)}
      {raio(860, 600, em('criativo') + 4, 15)}
      {raio(140, 920, em('quase'), -10)}
      {frame >= em('quase') - 2 ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 1060, textAlign: 'center', fontFamily: ANTON, color: C.creme, textShadow: sombra(C.marinho, 14)}}>
          <div style={{fontSize: 280, lineHeight: 1}}>≈{p}%</div>
          <div style={{fontSize: 64}}>DO IMPACTO DE UM ANÚNCIO NAS VENDAS</div>
        </div>
      ) : null}
      {frame >= em('vendas') ? <div style={{position: 'absolute', left: 0, right: 0, top: 1480, textAlign: 'center', fontFamily: INTER, fontWeight: 700, fontSize: 30, color: C.creme, opacity: entra(frame, em('vendas'), 8)}}>Mais que alcance. Mais que segmentação. Mais que verba.</div> : null}
    </AbsoluteFill>
  );
};

// 8. O homem-câmera apontando (o rosa vira azul, como o vermelho da referência).
const Camera: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const e = mola(frame, de + 4, 120);
  const circulo = entra(frame, em('ideia') + 4, 14);
  const cor = interpolate(t, [0, 18], [0, 1], FIXO);
  const flash = Math.max(0, Math.sin(t / 5)) ** 6;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.azul} />
      <AbsoluteFill style={{backgroundColor: C.claro, opacity: 1 - cor}} />
      <Titulo linhas={[{t: 'O ORÇAMENTO COMPRA', q: em('orcamento', 1)}, {t: 'A TELA.', q: em('tela')}]} x={60} y={170} tam={96} sombraCor="rgba(0,0,0,0.35)" />
      {frame >= em('so') - 2 ? (
        <div style={{position: 'absolute', left: 60, top: 400, width: 960}}>
          <Titulo linhas={[{t: 'SÓ A IDEIA', q: em('so')}, {t: 'COMPRA ATENÇÃO.', q: em('compra', 1)}]} x={0} y={0} tam={96} sombraCor={C.marinho} />
          <svg width={330} height={140} style={{position: 'absolute', left: 110, top: -18, overflow: 'visible'}}>
            <path d="M 20 70 C 20 10, 300 0, 310 60 C 318 120, 40 130, 30 70" fill="none" stroke={C.amarelo} strokeWidth={8} strokeLinecap="round" strokeDasharray={900} strokeDashoffset={900 * (1 - circulo)} />
          </svg>
        </div>
      ) : null}
      <div style={{position: 'absolute', left: 150, top: 760 + (1 - e) * 600, width: 940, height: 1200, opacity: Math.min(1, e * 1.5)}}>
        <Img src={img('aponta')} style={{position: 'absolute', left: 0, top: 280, width: 940, filter: CONTORNO('#fff', 7)}} />
        <Img src={img('camera')} style={{position: 'absolute', left: 250, top: -110, width: 560, transform: `rotate(${Math.sin(t / 9) * 2}deg)`, filter: CONTORNO('#fff', 7), clipPath: 'inset(0 0 33% 0)'}} />
        <svg width={220} height={220} viewBox="-50 -50 100 100" style={{position: 'absolute', left: 700, top: 20, opacity: flash, transform: `rotate(${t * 3}deg)`}}>
          {Array.from({length: 12}, (_, k) => (
            <polygon key={k} points="0,-48 4,0 -4,0" fill="#fff" transform={`rotate(${k * 30})`} />
          ))}
          <circle r={10} fill="#fff" />
        </svg>
      </div>
      <div style={{position: 'absolute', right: 60, top: 860, display: 'flex', alignItems: 'center', gap: 10, fontFamily: INTER, fontWeight: 900, fontSize: 30, color: C.branco}}>
        <div style={{width: 18, height: 18, borderRadius: '50%', backgroundColor: '#fff', opacity: Math.floor(t / 10) % 2 ? 1 : 0.25}} />
        REC
      </div>
    </AbsoluteFill>
  );
};

// 9. Trompetes rosa e amarelos no vinho.
const Trompetes: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const fase2 = frame >= em('faca') - 3;
  const fim = fimDe(8);
  const catavento = interpolate(frame, [fim - 9, fim], [0, 1], {...FIXO, easing: Easing.in(Easing.quad)});
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor="#1A0612" luz={0} />
      <AbsoluteFill style={{background: `radial-gradient(700px 900px at 65% 70%, ${C.vinho} 0%, rgba(0,0,0,0) 70%)`}} />
      {[0, 1, 2, 3, 4].map((k) => {
        const toque = Math.max(0, Math.sin((t - k * 4) / 4)) * 12;
        return (
          <div key={k} style={{position: 'absolute', left: 230 + (k % 2) * 60, top: 600 + k * 250, width: 700, height: 300, transform: `translate(${toque}px, ${-toque * 0.4}px)`}}>
            <Img src={img('trompete')} style={{position: 'absolute', left: 0, top: -120, width: 560, transform: 'rotate(28deg)', transformOrigin: '50% 50%'}} />
            {[0, 1, 2].map((j) => {
              const o = (t / 12 + j / 3 + k * 0.2) % 1;
              return <div key={j} style={{position: 'absolute', left: 560 + o * 140, top: -120 - o * 40, width: 70 + o * 90, height: 160 + o * 120, borderRadius: '50%', border: `6px solid ${j % 2 ? C.amarelo : C.rosa}`, borderLeftColor: 'transparent', borderBottomColor: 'transparent', opacity: 1 - o, transform: 'rotate(10deg)'}} />;
            })}
          </div>
        );
      })}
      {!fase2 ? (
        <Titulo
          linhas={[
            {t: 'PARA DE', q: em('para'), cor: C.amarelo},
            {t: 'ALIMENTAR', q: em('alimentar', 1)},
            {t: 'ELA.', q: em('ela'), cor: C.rosa},
          ]}
          x={60}
          y={170}
          tam={180}
          sombraCor="#000"
        />
      ) : (
        <Titulo
          linhas={[
            {t: 'FAÇA UM ANÚNCIO', q: em('faca'), tam: 120},
            {t: 'QUE NINGUÉM', q: em('ninguem', 1), tam: 120},
            {t: 'CONSIGA', q: em('consiga'), cor: C.amarelo, tam: 150},
            {t: 'PASSAR.', q: em('passar'), cor: C.rosa, tam: 150},
          ]}
          x={60}
          y={150}
          sombraCor="#000"
        />
      )}
      {catavento > 0 ? (
        <svg width={1080} height={1920} style={{position: 'absolute'}}>
          {Array.from({length: 12}, (_, k) => {
            const a = (k * 30 + catavento * 220) * (Math.PI / 180);
            const r = 1700 * catavento;
            return <polygon key={k} points={`540,960 ${540 + Math.cos(a) * r},${960 + Math.sin(a) * r} ${540 + Math.cos(a + 0.42) * r * 0.62},${960 + Math.sin(a + 0.42) * r * 0.62}`} fill={[C.azul, C.amarelo, C.rosa, '#2DB34A', C.branco, C.preto][k % 6]} stroke={C.preto} strokeWidth={4} />;
          })}
        </svg>
      ) : null}
    </AbsoluteFill>
  );
};

// 10. Fecho: raios coloridos, estouro amarelo com a dot e o "manda POP".
const RAIOS = [C.azul, C.amarelo, C.rosa, '#1E8F4E', C.preto, C.creme, C.claro, C.azul, C.branco, C.rosa, C.amarelo, C.preto];
const Fecho: React.FC<{de: number}> = ({de}) => {
  const frame = useCurrentFrame();
  const t = frame - de;
  const logo = frame >= em('dot') - 3;
  const mBurst = mola(frame, de, 180);
  const mTexto = mola(frame, logo ? em('dot') - 3 : de + 2, 220);
  const cta = em('manda');
  const corre = Math.sin(t / 2.5);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Papel cor={C.creme} />
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {RAIOS.map((cor, k) => {
          const a = ((k * 30 + t * 0.4) * Math.PI) / 180;
          return <polygon key={k} points={`540,960 ${540 + Math.cos(a) * 2400},${960 + Math.sin(a) * 2400} ${540 + Math.cos(a + 0.36) * 2400},${960 + Math.sin(a + 0.36) * 2400}`} fill={cor} />;
        })}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', fontFamily: INTER, fontWeight: 700, fontSize: 32, color: C.branco, textShadow: '0 2px 8px rgba(0,0,0,0.7)'}}>@marketingdotagency</div>
      <Estouro x={540} y={940} r={430 * mBurst} pontas={16} cor={C.amarelo} borda={C.preto} esp={14} giro={-6} semente="fecho">
        {logo ? (
          <div style={{display: 'flex', alignItems: 'flex-end', transform: `scale(${mTexto}) rotate(-5deg)`}}>
            <span style={{fontFamily: INTER, fontWeight: 900, fontSize: 240, letterSpacing: '-0.05em', lineHeight: 1, color: C.preto}}>dot</span>
            <span style={{display: 'inline-block', width: 64, height: 64, borderRadius: '50%', backgroundColor: C.azul, marginLeft: 6, marginBottom: 27, border: `4px solid ${C.preto}`}} />
          </div>
        ) : (
          <span style={{fontFamily: ANTON, fontSize: 100, lineHeight: 1.05, color: C.preto, transform: `scale(${mTexto}) rotate(-6deg)`, display: 'inline-block'}}>
            É ISSO QUE
            <br />A GENTE FAZ NA...
          </span>
        )}
      </Estouro>
      <Img src={img('homenzinho')} style={{position: 'absolute', left: 760, top: 470 + Math.abs(corre) * -14, width: 150, transform: `rotate(${corre * 8 - 10}deg) scale(${mBurst})`, filter: CONTORNO('#fff', 4)}} />
      {frame >= cta - 2 ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 1460, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20}}>
          <div style={{padding: '8px 36px 0', backgroundColor: C.branco, border: `7px solid ${C.preto}`, fontFamily: ANTON, fontSize: 110, lineHeight: 1.1, color: C.preto, transform: `rotate(-4deg) scale(${mola(frame, cta - 2, 260)})`, boxShadow: '12px 14px 0 rgba(0,0,0,0.5)'}}>
            MANDA <span style={{color: C.azul}}>“POP”</span>
          </div>
          <div style={{padding: '8px 22px', backgroundColor: C.azul, border: `3px solid ${C.preto}`, fontFamily: INTER, fontWeight: 900, fontSize: 32, color: C.branco, transform: `rotate(-2deg) scale(${mola(frame, em('ganhe') - 2, 220)})`}}>E GANHE UMA IDEIA DE ANÚNCIO</div>
        </div>
      ) : null}
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
  const cenas = [Devoradora, Queima, Tvs, Dedao, Mediano, Alcance, Cerebro, Camera, Trompetes, Fecho];
  const Cena = cenas[i];
  const soco = interpolate(frame - de, [0, 7], [1.07, 1], {...FIXO, easing: SUAVE});
  const treme = frame - de < 5 ? (random(`t${frame}`) - 0.5) * 16 : 0;
  // Leve trepidação de película o tempo todo.
  const pelicula = (random(`f${Math.floor(frame / 2)}`) - 0.5) * 3;
  return (
    <AbsoluteFill style={{backgroundColor: C.preto}}>
      <AbsoluteFill style={{transform: `scale(${soco}) translate(${treme + pelicula}px, ${-treme}px)`}}>
        <Cena de={de} />
      </AbsoluteFill>
      <Textura />
      <Sequence from={VOZ} layout="none">
        <Audio src={staticFile(`${PASTA}/voz.mp3`)} />
      </Sequence>
      <Audio src={staticFile('trilhas/aylex-worlds-freetouse.mp3')} volume={(f) => interpolate(f, [0, 10, DURACAO - 50, DURACAO - 40, DURACAO - 12, DURACAO], [0, 0.05, 0.05, 0.14, 0.14, 0], FIXO)} />
      {CENAS.slice(1).map((c) => (
        <Som key={c} nome="whoosh" q={c - 2} volume={0.08} />
      ))}
      <Som nome="impacto" q={em('jantar') + 4} volume={0.3} />
      <Som nome="carimbo" q={em('mesmo')} volume={0.15} />
      <Som nome="carimbo" q={em('mesma')} volume={0.15} />
      <Som nome="carimbo" q={em('mesmo', 1)} volume={0.15} />
      <Som nome="tique" q={em('pulo') + 4} volume={0.2} />
      <Som nome="risco" q={fimDe(1) - 12} volume={0.12} />
      <Som nome="risco" q={em('pulo') + 8} volume={0.12} />
      <Som nome="pop" q={em('novo')} volume={0.12} />
      <Som nome="pop" q={em('novo', 1)} volume={0.12} />
      <Som nome="batida" q={em('alcance') + 8} volume={0.15} />
      <Som nome="ding" q={em('dot') - 3} volume={0.12} />
      <Som nome="pop" q={em('manda') - 2} volume={0.12} />
    </AbsoluteFill>
  );
};
