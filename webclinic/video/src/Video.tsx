// Web Clinic: vídeo "sobre nós" para o post fixado (Reels 1080x1920, 30 fps). v2: gancho + profundidade.
// Narração ElevenLabs eleven_v4 (voz Moutella) com tags de emoção por frase (roteiro.txt); tempo por palavra em audio.json.
// Sem música: só efeitos sonoros. Vetores e logo exportados do gerador Python (exportar.py).
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, Easing, delayRender, continueRender} from 'remotion';
import AUD from './audio.json';
import VET from './vetores.json';

// Poppins local (public/fonts): o navegador do render não confia no proxy para baixar do Google Fonts
const fontFamily = 'Poppins';
if (typeof document !== 'undefined') {
  const h = delayRender('fontes');
  Promise.all([300, 400, 500, 600, 700].map((w) => {
    const ff = new FontFace('Poppins', `url(${staticFile(`fonts/poppins-${w}.woff2`)}) format('woff2')`, {weight: String(w)});
    document.fonts.add(ff);
    return ff.load();
  })).then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
}

const FPS = 30;
const A = '#2D7FF0', N = '#0B1F3A', L = '#5AA2FF', M = '#CFE6F7', G = '#EEF5FC', C = '#6B7A90', R = '#FA5F6D';
const P = AUD as {texto: string; inicio: number; fim: number}[];
const V = (VET as any).V as Record<string, string>;
const LOGO = ((VET as any).logo as string).replace('width="240" height="240"', 'width="100%" height="100%"');
const CUR = (VET as any).cur as string;

const fr = (s: number) => Math.round(s * FPS);
const W = (i: number) => fr(P[i].inicio);
const FIM_VOZ = fr(P[P.length - 1].fim);
export const DURACAO = FIM_VOZ + fr(2.8);
// cortes: palavra que abre cada cena
const GAT = [12, 20, 28, 36, 46, 59, 66, 70, 74, 85];
const CUT = [0, ...GAT.map((i) => W(i) - 4), DURACAO];

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const io = (f: number, a: number, b: number, x: number, y: number, e = ease) => interpolate(f, [a, b], [x, y], {...clamp, easing: e});
const sp = (f: number, at: number, damping = 13) => spring({frame: f - at, fps: FPS, config: {damping, mass: 0.7, stiffness: 140}});

// ---------- estilo ----------
const SOMBRA = '0 70px 120px -30px rgba(11,31,58,.55), 0 24px 48px -18px rgba(45,127,240,.45)';
const SOMBRA_LEVE = '0 40px 70px -24px rgba(11,31,58,.40), 0 12px 26px -12px rgba(45,127,240,.35)';
const VIDRO: React.CSSProperties = {background: 'linear-gradient(160deg, rgba(255,255,255,.26), rgba(255,255,255,.06))', border: '2px solid rgba(255,255,255,.55)',
  boxShadow: 'inset 0 2px 0 rgba(255,255,255,.6), inset 0 -20px 40px rgba(45,127,240,.18), 0 40px 80px -20px rgba(0,0,0,.45)', backdropFilter: 'blur(14px)'};
const gradTexto = (a: string, b: string): React.CSSProperties => ({background: `linear-gradient(100deg, ${a}, ${b})`, WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent'});

// ---------- fundos ----------
const Escuro: React.FC<{t: number; tom?: string}> = ({t, tom = A}) => (
  <>
    <AbsoluteFill style={{background: 'linear-gradient(180deg, #050B1C 0%, #071433 55%, #0B1F3A 100%)'}} />
    <AbsoluteFill style={{background: `radial-gradient(1200px 700px at 50% ${106 + Math.sin(t / 30) * 3}%, ${tom}cc, ${tom}00 70%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(700px 500px at ${15 + Math.sin(t / 45) * 5}% 12%, rgba(90,162,255,.22), rgba(90,162,255,0) 70%)`}} />
    <svg width={1080} height={1920} style={{position: 'absolute', opacity: 0.55}}>
      <path d={`M -200 ${1380 + Math.sin(t / 22) * 40} C 300 1060, 700 1480, 1300 ${1150 + Math.cos(t / 22) * 40}`} fill="none" stroke={L} strokeWidth={5} style={{filter: 'blur(3px)'}} />
    </svg>
  </>
);
const Claro: React.FC<{t: number}> = ({t}) => (
  <>
    <AbsoluteFill style={{background: `linear-gradient(${155 + Math.sin(t / 40) * 6}deg, #FFFFFF 0%, ${G} 34%, ${M} 66%, #7DB5FF 100%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(900px 700px at ${28 + Math.sin(t / 30) * 6}% 22%, rgba(255,255,255,.95), rgba(255,255,255,0) 70%)`}} />
    <svg width={1080} height={1920} style={{position: 'absolute', opacity: 0.45}}>
      <path d={`M -100 ${1420 + Math.sin(t / 25) * 30} C 300 1220, 700 1620, 1200 ${1380 + Math.cos(t / 25) * 30}`} fill="none" stroke="#fff" strokeWidth={110} strokeLinecap="round" style={{filter: 'blur(36px)'}} />
    </svg>
  </>
);
const Azul: React.FC<{t: number}> = ({t}) => (
  <>
    <AbsoluteFill style={{background: `linear-gradient(${165 + Math.sin(t / 40) * 6}deg, #3D8CFF 0%, ${A} 45%, #1A56C4 100%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(900px 800px at ${70 + Math.sin(t / 30) * 6}% 20%, rgba(255,255,255,.35), rgba(255,255,255,0) 70%)`}} />
    <AbsoluteFill style={{background: 'radial-gradient(1100px 700px at 50% 110%, rgba(11,31,58,.55), rgba(11,31,58,0) 70%)'}} />
  </>
);
const Grao: React.FC<{f: number}> = ({f}) => (
  <Img src={staticFile(`grao${Math.floor(f / 2) % 4}.jpg`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'overlay', opacity: 0.1, zIndex: 40}} />
);
const Vinheta: React.FC = () => <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(5,11,28,.35) 100%)', zIndex: 39}} />;

// ---------- peças ----------
const Ico: React.FC<{n: string; s: number}> = ({n, s}) => <svg width={s} height={s} viewBox="0 0 200 200" dangerouslySetInnerHTML={{__html: V[n]}} />;
const Logo: React.FC<{s: number}> = ({s}) => <div style={{width: s, height: s}} dangerouslySetInnerHTML={{__html: LOGO}} />;
// ícone em "bloco 3D": degradê, brilho interno e sombra; desfoque = profundidade de campo
const Bloco: React.FC<{n: string; s: number; x: number; y: number; t: number; rot?: number; blur?: number; k?: number}> = ({n, s, x, y, t, rot = 0, blur = 0, k = 1}) => (
  <div style={{position: 'absolute', left: x, top: y + Math.sin(t / 22 + x / 90) * 14, width: s, height: s, borderRadius: s * 0.28,
    background: 'linear-gradient(150deg, #FFFFFF 0%, #EEF5FC 55%, #CFE6F7 100%)', display: 'grid', placeItems: 'center',
    boxShadow: `inset 0 ${s * 0.04}px ${s * 0.06}px rgba(255,255,255,.9), inset 0 -${s * 0.05}px ${s * 0.1}px rgba(45,127,240,.18), 0 ${s * 0.22}px ${s * 0.4}px -${s * 0.1}px rgba(11,31,58,.45)`,
    transform: `rotate(${rot + Math.sin(t / 30 + x) * 3}deg) scale(${k})`, filter: blur ? `blur(${blur}px)` : undefined, opacity: Math.min(1, k * 1.4), zIndex: blur > 6 ? 25 : 3}}>
    <Ico n={n} s={s * 0.64} />
  </div>
);
const Cursor: React.FC<{x: number; y: number; k?: number; press?: number}> = ({x, y, k = 2.3, press = 0}) => (
  <svg style={{position: 'absolute', left: x, top: y, zIndex: 30, filter: 'drop-shadow(0 14px 16px rgba(11,31,58,.35))', transform: `scale(${1 - press * 0.15})`, transformOrigin: '0 0'}}
    width={36 * k} height={50 * k} viewBox="-3 -3 33 46"><path d={CUR} fill={N} stroke="#fff" strokeWidth={2.5} strokeLinejoin="round" /></svg>
);
const Chip: React.FC<{icon: string; t: string; sub: string; x: number; y: number; k: number; rot?: number; z?: number}> = ({icon, t, sub, x, y, k, rot = 0, z = 15}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', alignItems: 'center', gap: 20, background: 'linear-gradient(160deg,#fff,#F3F8FE)', border: '2px solid #E2EAF4', borderRadius: 32,
    padding: '22px 32px', boxShadow: SOMBRA, transform: `rotate(${rot}deg) scale(${k})`, opacity: Math.min(1, k * 1.5), transformOrigin: 'left center', zIndex: z}}>
    <div style={{width: 76, height: 76, borderRadius: 22, background: G, display: 'grid', placeItems: 'center'}}><Ico n={icon} s={50} /></div>
    <div style={{fontSize: 34, fontWeight: 600, color: N, lineHeight: 1.15, whiteSpace: 'nowrap'}}>{t}<div style={{fontSize: 24, fontWeight: 400, color: C}}>{sub}</div></div>
  </div>
);
const Bar: React.FC<{url: string}> = ({url}) => (
  <div style={{height: 76, background: G, display: 'flex', alignItems: 'center', gap: 12, padding: '0 28px', borderBottom: '2px solid #E2EAF4'}}>
    {['#FA5F6D', '#F5B83D', '#3CC48A'].map((c, i) => <i key={i} style={{width: 16, height: 16, borderRadius: 9, background: c}} />)}
    <div style={{marginLeft: 18, flex: 1, height: 44, borderRadius: 99, background: '#fff', border: '2px solid #E2EAF4', fontSize: 22, color: C, display: 'flex', alignItems: 'center', padding: '0 20px'}}>{url}</div>
  </div>
);
const Btn: React.FC<{t: string; sz?: number; on?: number}> = ({t, sz = 34, on = 0}) => (
  <span style={{display: 'inline-block', background: `linear-gradient(180deg, ${L}, ${A})`, color: '#fff', fontWeight: 600, fontSize: sz, borderRadius: 99, padding: `${sz * 0.6}px ${sz * 1.3}px`, whiteSpace: 'nowrap',
    boxShadow: `0 14px 30px -10px rgba(45,127,240,.7), 0 0 0 ${on * 22}px rgba(45,127,240,${0.3 * (1 - on)})`}}>{t}</span>
);
const Site: React.FC<{tag: string; a: string; b: string; url: string; ic: string; on?: number; w?: number}> = ({tag, a, b, url, ic, on = 0, w = 920}) => (
  <div style={{width: w, background: '#fff', borderRadius: 36, overflow: 'hidden', boxShadow: SOMBRA, border: '2px solid #E2EAF4'}}>
    <Bar url={url} />
    <div style={{padding: '44px 50px', display: 'flex', gap: 34}}>
      <div style={{flex: 1}}>
        <div style={{fontSize: 20, fontWeight: 600, letterSpacing: '.22em', color: A}}>{tag}</div>
        <div style={{fontSize: Math.round(w * 0.059), lineHeight: 1.04, letterSpacing: '-0.035em', margin: '14px 0 24px', color: N}}><b>{a}</b> <span style={{fontWeight: 300}}>{b}</span></div>
        {[92, 70].map((p, i) => <div key={i} style={{height: 14, borderRadius: 9, background: G, width: `${p}%`, marginBottom: 12}} />)}
        <div style={{marginTop: 28}}><Btn t="Agendar consulta" sz={Math.round(w * 0.035)} on={on} /></div>
      </div>
      <div style={{width: w * 0.27, borderRadius: 28, background: `linear-gradient(160deg, ${G}, ${M})`, display: 'grid', placeItems: 'center'}}><Ico n={ic} s={w * 0.17} /></div>
    </div>
  </div>
);
const Pulse: React.FC<{y: number; p: number; c?: string; sw?: number; glow?: boolean}> = ({y, p, c = A, sw = 6, glow}) => (
  <svg style={{position: 'absolute', left: -40, top: y, filter: glow ? `drop-shadow(0 0 14px ${c})` : undefined}} width={1160} height={290} viewBox="0 0 400 100">
    <path d="M4 50H150L166 18L190 86L210 32L222 50H396" fill="none" stroke={c} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
  </svg>
);
// faixa de luz que atravessa um cartão
const Brilho: React.FC<{f: number; at: number; dur?: number}> = ({f, at, dur = 22}) => {
  const x = io(f, at, at + dur, -60, 160, Easing.inOut(Easing.cubic));
  return <div style={{position: 'absolute', inset: 0, background: `linear-gradient(105deg, rgba(255,255,255,0) ${x - 20}%, rgba(255,255,255,.55) ${x}%, rgba(255,255,255,0) ${x + 20}%)`, pointerEvents: 'none', zIndex: 5}} />;
};

// ---------- legenda cinética (palavra por palavra no tempo da voz, com borrão de movimento) ----------
type Linha = {de: number; ate: number; sz: number; peso?: 300 | 600 | 700; cor?: string; grad?: [string, string]; glow?: string};
const TROCA: Record<number, string> = {62: '24', 63: '', 64: ''};
const Fala: React.FC<{f: number; linhas: Linha[]; y: number; x?: number; align?: 'left' | 'center'; sair?: number}> = ({f, linhas, y, x = 80, align = 'left', sair}) => {
  const out = sair === undefined ? 1 : io(f, sair, sair + 6, 1, 0);
  return (
    <div style={{position: 'absolute', left: x, right: x, top: y, textAlign: align, letterSpacing: '-0.045em', lineHeight: 1.04, opacity: out, filter: `blur(${(1 - out) * 10}px)`, zIndex: 20}}>
      {linhas.map((l, k) => (
        <div key={k} style={{fontSize: l.sz, fontWeight: l.peso ?? 300, color: l.cor ?? N, textShadow: l.glow ? `0 0 40px ${l.glow}` : undefined}}>
          {Array.from({length: l.ate - l.de + 1}, (_, j) => l.de + j).map((i) => {
            const txt = TROCA[i] ?? P[i].texto;
            if (!txt) return null;
            const o = io(f, W(i) - 3, W(i) + 4, 0, 1);
            return (
              <span key={i} style={{display: 'inline-block', opacity: o, filter: `blur(${(1 - o) * 14}px)`, transform: `translateX(${(1 - o) * 70}px) scale(${0.96 + o * 0.04})`, marginRight: '0.24em',
                ...(l.grad ? gradTexto(l.grad[0], l.grad[1]) : {})}}>{txt}</span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
const Hdr: React.FC<{dark?: boolean}> = ({dark}) => (
  <div style={{position: 'absolute', top: 150, left: 80, display: 'flex', alignItems: 'center', gap: 16, zIndex: 35}}>
    <div style={{borderRadius: '50%', boxShadow: '0 8px 20px rgba(0,0,0,.25)'}}><Logo s={64} /></div>
    <div style={{fontSize: 28, fontWeight: 600, color: dark ? '#fff' : N}}>webclinic</div>
  </div>
);

// ---------- cena: entra vindo de trás (0,9 → 1 com desfoque) e sai "atravessando a câmera" ----------
const Cena: React.FC<{k: number; fundo: 'claro' | 'escuro' | 'azul'; tom?: string; children: (f: number, t: number) => React.ReactNode}> = ({k, fundo, tom, children}) => {
  const g = useCurrentFrame();
  const a = CUT[k], b = CUT[k + 1];
  if (g < a || g >= b) return null;
  const t = g - a;
  const ultimo = k === CUT.length - 2;
  const ent = io(t, 0, 9, 0, 1);
  const sai = ultimo ? 0 : io(g, b - 7, b, 0, 1, Easing.in(Easing.cubic));
  const z = (0.9 + ent * 0.1) * interpolate(t, [0, b - a], [1, 1.04]) * (1 + sai * 0.45);
  const bl = (1 - ent) * 16 + sai * 18;
  const dark = fundo !== 'claro';
  return (
    <AbsoluteFill style={{fontFamily, overflow: 'hidden'}}>
      {fundo === 'claro' ? <Claro t={g} /> : fundo === 'azul' ? <Azul t={g} /> : <Escuro t={g} tom={tom} />}
      <AbsoluteFill style={{transform: `scale(${z})`, filter: `blur(${bl}px)`, opacity: Math.min(1, 0.4 + ent) * (1 - sai * 0.6)}}>
        {children(g, t)}
      </AbsoluteFill>
      <Hdr dark={dark} />
      <Vinheta />
      <Grao f={g} />
    </AbsoluteFill>
  );
};

// ---------- celular ----------
const Celular: React.FC<{x: number; y: number; w: number; h: number; rot: string; children: React.ReactNode; brilho?: number}> = ({x, y, w, h, rot, children, brilho = 0}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: w * 0.14, padding: w * 0.03, transform: rot, transformStyle: 'preserve-3d',
    background: 'linear-gradient(160deg, #2A3A57, #0B1F3A 40%, #050B1C)', boxShadow: `0 80px 140px -30px rgba(0,0,0,.65), 0 0 ${120 * brilho}px rgba(90,162,255,${0.55 * brilho}), inset 0 2px 0 rgba(255,255,255,.25)`}}>
    <div style={{width: '100%', height: '100%', borderRadius: w * 0.115, background: '#fff', overflow: 'hidden', position: 'relative'}}>
      <div style={{position: 'absolute', top: 18, left: '50%', transform: 'translateX(-50%)', width: w * 0.28, height: 34, borderRadius: 20, background: N, zIndex: 9}} />
      {children}
    </div>
  </div>
);

export const Video: React.FC = () => {
  const S: [string, number, number][] = [
    ['impacto', 0, 0.35],
    ...CUT.slice(1, -1).map((c) => ['whoosh', c - 4, 0.3] as [string, number, number]),
    ...Array.from({length: 12}, (_, i) => ['tique', W(5) + i * 4, 0.25] as [string, number, number]),
    ['pop', W(19), 0.4], ['impacto', W(27), 0.5], ['ding', W(27) + 4, 0.35],
    ['impacto', W(29), 0.5],
    ['pop', W(39), 0.25], ['pop', W(39) + 6, 0.25], ['pop', W(39) + 12, 0.25],
    ['tique', W(58) - 1, 0.6], ['ding', W(58) + 3, 0.45],
    ...Array.from({length: 6}, (_, i) => ['pop', CUT[6] + 8 + i * 5, 0.15] as [string, number, number]),
    ['pop', W(69), 0.45], ['tique', W(73), 0.6], ['pop', W(73) + 6, 0.35],
    ['ding', W(81), 0.3], ['ding', W(82) + 6, 0.28], ['ding', W(84), 0.3],
    ['impacto', W(85), 0.5], ['tique', W(88) + 4, 0.5], ['pop', FIM_VOZ + 6, 0.35],
  ];
  return (
    <AbsoluteFill style={{background: '#050B1C', fontFamily}}>
      <Audio src={staticFile('voz.mp3')} />
      {S.map(([s, at, v], i) => <Sequence key={i} from={Math.max(0, at)}><Audio src={staticFile(`${s}.mp3`)} volume={v} /></Sequence>)}

      {/* 1. GANCHO: agora mesmo, alguém digita sua especialidade */}
      <Cena k={0} fundo="escuro">{(g, t) => {
        const q = 'cardiologista perto de mim';
        const n = Math.floor(io(g, W(5), W(11), 0, q.length, Easing.linear));
        const ry = interpolate(g, [0, CUT[1]], [-24, -8]), rx = interpolate(g, [0, CUT[1]], [14, 6]);
        const ph = sp(g, 2, 16);
        return <>
          <div style={{position: 'absolute', left: 80, top: 250, display: 'flex', alignItems: 'center', gap: 12, padding: '10px 22px', borderRadius: 99, background: 'rgba(250,95,109,.16)', border: '2px solid rgba(250,95,109,.5)', zIndex: 21}}>
            <i style={{width: 16, height: 16, borderRadius: 9, background: R, opacity: g % 30 < 18 ? 1 : 0.25, boxShadow: `0 0 14px ${R}`}} />
            <span style={{fontSize: 24, fontWeight: 600, letterSpacing: '.2em', color: '#FFB3BA'}}>AGORA</span>
          </div>
          <Fala f={g} y={330} linhas={[{de: 0, ate: 2, sz: 88, cor: '#fff'}, {de: 3, ate: 6, sz: 70, peso: 700, cor: '#fff'}, {de: 7, ate: 11, sz: 54, cor: '#9CC6FF'}]} />
          <Bloco n="zoom" s={170} x={-30} y={1180} t={g} rot={-12} blur={10} k={sp(g, 10)} />
          <Bloco n="pin" s={150} x={880} y={860} t={g} rot={10} blur={3} k={sp(g, 16)} />
          <div style={{position: 'absolute', left: 0, right: 0, top: 0, bottom: 0, perspective: 2200}}>
            <Celular x={250} y={800 + (1 - ph) * 500} w={580} h={1180} rot={`rotateY(${ry}deg) rotateX(${rx}deg)`} brilho={0.6}>
              <div style={{padding: '110px 34px 0'}}>
                <div style={{fontSize: 44, fontWeight: 700, color: N, letterSpacing: '-0.03em', textAlign: 'center', marginBottom: 30}}>Pesquisar</div>
                <div style={{display: 'flex', alignItems: 'center', gap: 14, borderRadius: 99, border: `3px solid ${A}`, padding: '20px 24px', fontSize: 28, color: N, boxShadow: '0 10px 30px -10px rgba(45,127,240,.5)'}}>
                  <Ico n="zoom" s={40} /><span style={{whiteSpace: 'nowrap', overflow: 'hidden'}}>{q.slice(0, n)}<span style={{display: 'inline-block', width: 3, height: 34, background: A, marginLeft: 3, verticalAlign: 'middle', opacity: g % 16 < 8 ? 1 : 0}} /></span>
                </div>
                {['cardiologista perto de mim', 'cardiologista agendar online', 'cardiologista atende hoje'].map((s, i) => (
                  <div key={i} style={{display: 'flex', alignItems: 'center', gap: 14, padding: '20px 10px', borderBottom: '2px solid #EEF2F7', fontSize: 24, color: C, opacity: io(g, W(9) + i * 3, W(9) + i * 3 + 5, 0, 1)}}>
                    <Ico n="zoom" s={30} />{s}
                  </div>
                ))}
              </div>
              <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 330, background: '#E9EEF5', padding: '22px 10px', display: 'grid', gridTemplateColumns: 'repeat(10, 1fr)', gap: 8}}>
                {'qwertyuiopasdfghjklzxcvbnm'.split('').map((c, i) => {
                  const on = q[n - 1] === c && g % 4 < 2;
                  return <div key={i} style={{height: 64, borderRadius: 10, background: on ? A : '#fff', color: on ? '#fff' : N, display: 'grid', placeItems: 'center', fontSize: 24, boxShadow: '0 2px 0 #C9D3E1', gridColumn: i === 19 ? 'span 1' : undefined}}>{c}</div>;
                })}
              </div>
            </Celular>
          </div>
        </>;
      }}</Cena>

      {/* 2. vai marcar com quem aparecer primeiro */}
      <Cena k={1} fundo="escuro">{(g) => {
        const res = [['Dr. Rafael Lima · Cardiologia', 'Agende online · aberto agora', true], ['Clínica Coração', 'Sem site · ligue', false], ['Consultório Centro', 'Só telefone', false]] as const;
        const um = sp(g, W(19) - 2, 10);
        return <>
          <div style={{position: 'absolute', right: -20, top: 520, fontSize: 680, fontWeight: 700, letterSpacing: '-0.08em', lineHeight: 1, ...gradTexto('rgba(90,162,255,.55)', 'rgba(45,127,240,.05)'), transform: `scale(${0.8 + um * 0.2})`, opacity: 0.45 + um * 0.55, filter: 'blur(1px)'}}>1º</div>
          <Fala f={g} y={330} linhas={[{de: 12, ate: 15, sz: 96, cor: '#fff'}, {de: 16, ate: 19, sz: 96, peso: 700, grad: ['#FFFFFF', L], glow: 'rgba(45,127,240,.45)'}]} />
          <div style={{position: 'absolute', left: 80, top: 800, width: 920, perspective: 2000}}>
            <div style={{transform: `rotateX(${interpolate(g, [CUT[1], CUT[2]], [24, 14])}deg) rotateY(-6deg)`, transformStyle: 'preserve-3d'}}>
              {res.map(([t, s, top], i) => {
                const k = sp(g, CUT[1] + 4 + i * 4);
                const dim = top ? 1 : 1 - um * 0.55;
                return <div key={i} style={{position: 'relative', marginTop: 28, background: '#fff', borderRadius: 32, padding: '30px 38px', boxShadow: top && um > 0.3 ? `${SOMBRA}, 0 0 0 ${um * 6}px ${A}` : SOMBRA_LEVE,
                  opacity: k * dim, transform: `translateY(${(1 - k) * 120}px) translateZ(${top ? um * 90 : -um * 40}px)`, filter: top ? undefined : `blur(${um * 3}px)`, overflow: 'hidden'}}>
                  {top && <Brilho f={g} at={W(19)} />}
                  <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
                    <div style={{width: 74, height: 74, borderRadius: 22, background: top ? `linear-gradient(160deg, ${L}, ${A})` : G, color: top ? '#fff' : C, display: 'grid', placeItems: 'center', fontSize: 34, fontWeight: 700}}>{i + 1}</div>
                    <div><div style={{fontSize: 36, fontWeight: 600, color: top ? A : N}}>{t}</div><div style={{fontSize: 24, color: C}}>{s}</div></div>
                  </div>
                </div>;
              })}
            </div>
          </div>
          <Bloco n="calendar" s={170} x={840} y={1380} t={g} rot={8} blur={9} k={sp(g, CUT[1] + 10)} />
        </>;
      }}</Cena>

      {/* 3. se não for você, é o seu concorrente */}
      <Cena k={2} fundo="escuro" tom="#3B2A6B">{(g) => {
        const voce = io(g, W(23), W(24), 0, 1), conc = sp(g, W(26) - 2, 11), ok = sp(g, W(27) + 2);
        return <>
          <Fala f={g} y={330} linhas={[{de: 20, ate: 23, sz: 104, cor: '#fff'}, {de: 24, ate: 27, sz: 100, peso: 700, grad: ['#FFC2C8', R], glow: 'rgba(250,95,109,.35)'}]} />
          <div style={{position: 'absolute', left: 0, right: 0, top: 0, bottom: 0, perspective: 2000}}>
            <div style={{position: 'absolute', left: 120, top: 780, width: 640, transform: `translateZ(${-voce * 260}px) rotateY(10deg) translateX(${-voce * 80}px)`, filter: `grayscale(${voce}) blur(${voce * 4}px)`, opacity: 1 - voce * 0.45}}>
              <div style={{background: '#fff', borderRadius: 32, padding: '34px 40px', boxShadow: SOMBRA_LEVE}}>
                <div style={{fontSize: 22, letterSpacing: '.2em', color: C, fontWeight: 600}}>VOCÊ</div>
                <div style={{fontSize: 40, fontWeight: 600, color: N, marginTop: 6}}>Seu consultório</div>
                <div style={{fontSize: 26, color: C}}>sem site · página 2</div>
              </div>
            </div>
            <div style={{position: 'absolute', left: 260, top: 1080, width: 700, transform: `translateZ(${conc * 120}px) rotateY(-10deg) translateY(${(1 - conc) * 300}px)`, opacity: conc}}>
              <div style={{position: 'relative', background: '#fff', borderRadius: 32, padding: '34px 40px', boxShadow: `${SOMBRA}, 0 0 0 4px ${R}`, overflow: 'hidden'}}>
                <Brilho f={g} at={W(27)} />
                <div style={{fontSize: 22, letterSpacing: '.2em', color: R, fontWeight: 600}}>SEU CONCORRENTE</div>
                <div style={{fontSize: 40, fontWeight: 600, color: N, marginTop: 6}}>Clínica do lado</div>
                <div style={{fontSize: 26, color: C}}>site com agenda online · 1º no Google</div>
              </div>
            </div>
          </div>
          <Chip icon="tick" t="Consulta marcada" sub="com o concorrente" x={380} y={1360} k={ok} rot={-3} z={25} />
        </>;
      }}</Cena>

      {/* 4. A Web Clinic existe pra virar esse jogo */}
      <Cena k={3} fundo="azul">{(g, t) => {
        const k = sp(g, W(29) - 2, 11);
        const flash = io(t, 0, 8, 0.85, 0);
        return <>
          <AbsoluteFill style={{background: '#fff', opacity: flash, zIndex: 30}} />
          {[0, 1, 2].map((i) => <div key={i} style={{position: 'absolute', left: 540 - 380 - i * 120, top: 720 - 380 - i * 120, width: 760 + i * 240, height: 760 + i * 240, borderRadius: '50%',
            border: '2px solid rgba(255,255,255,.25)', transform: `scale(${0.9 + k * 0.1 + Math.sin((g + i * 20) / 25) * 0.015})`, opacity: k * (0.8 - i * 0.22)}} />)}
          <div style={{position: 'absolute', left: 260, top: 440, width: 560, height: 560, borderRadius: '50%', boxShadow: '0 80px 140px -30px rgba(11,31,58,.6), 0 0 120px rgba(255,255,255,.35)', transform: `scale(${k}) rotate(${(1 - k) * -25}deg)`}}><Logo s={560} /></div>
          <Pulse y={1000} p={io(g, W(30), W(35), 0, 1)} c="#fff" sw={4} glow />
          <Bloco n="steth" s={150} x={60} y={330} t={g} rot={-10} blur={2} k={sp(g, W(31))} />
          <Bloco n="heart" s={180} x={860} y={980} t={g} rot={9} blur={8} k={sp(g, W(33))} />
          <Fala f={g} y={1300} align="center" linhas={[{de: 28, ate: 30, sz: 100, cor: '#fff'}, {de: 31, ate: 35, sz: 96, peso: 700, cor: '#fff', glow: 'rgba(11,31,58,.35)'}]} />
        </>;
      }}</Cena>

      {/* 5. sites para médicos e profissionais da saúde */}
      <Cena k={4} fundo="claro">{(g) => {
        const sites = [['DERMATOLOGIA', 'Pele saudável', 'começa aqui.', 'draanapaula.com.br', 'drop'], ['PEDIATRIA', 'Cuidado', 'desde o 1º dia.', 'drjoaoped.com.br', 'baby'], ['ODONTOLOGIA', 'Sorriso', 'sem medo.', 'clinicasorrir.com.br', 'tooth']];
        return <>
          <Fala f={g} y={330} linhas={[{de: 36, ate: 39, sz: 92}, {de: 40, ate: 41, sz: 124, peso: 700, grad: [L, A]}, {de: 42, ate: 45, sz: 60, cor: C}]} />
          <div style={{position: 'absolute', inset: 0, perspective: 2200}}>
            {sites.map(([tag, a, b, url, ic], i) => {
              const k = sp(g, W(39) + [1, 0, 2][i] * 6, 14);
              const pos = (i - 1) + interpolate(g, [CUT[4], CUT[5]], [0.12, -0.12]);
              const centro = 1 - Math.min(1, Math.abs(pos));
              return <div key={i} style={{position: 'absolute', left: 190 + pos * 470, top: 900, transformStyle: 'preserve-3d',
                transform: `translateZ(${-260 + centro * 260}px) rotateY(${-pos * 38}deg) rotateX(6deg) translateY(${(1 - k) * 700}px)`, opacity: k, zIndex: Math.round(centro * 10),
                filter: `blur(${(1 - centro) * 3}px) brightness(${0.85 + centro * 0.15})`}}>
                <Site tag={tag} a={a} b={b} url={url} ic={ic} w={700} />
              </div>;
            })}
          </div>
          <Bloco n="heart" s={200} x={-50} y={720} t={g} rot={-10} blur={12} k={sp(g, CUT[4] + 6)} />
          <Bloco n="brain" s={120} x={900} y={760} t={g} rot={12} blur={4} k={sp(g, CUT[4] + 12)} />
          <Bloco n="steth" s={220} x={820} y={1560} t={g} rot={8} blur={14} k={sp(g, W(43))} />
        </>;
      }}</Cena>

      {/* 6. não é só bonito: vira consulta marcada */}
      <Cena k={5} fundo="claro">{(g) => {
        const risco = io(g, W(51) + 6, W(51) + 14, 0, 1);
        const cx = io(g, W(54), W(57), 900, 330), cy = io(g, W(54), W(57), 1750, 1235);
        const clk = g >= W(58) - 2 ? io(g, W(58) - 2, W(58) + 12, 0, 1) : 0;
        const ch = sp(g, W(58) + 2);
        const ry = interpolate(g, [CUT[5], CUT[6]], [-16, -6]);
        return <>
          <div style={{position: 'absolute', left: 80, top: 330, width: 920, opacity: io(g, W(52) - 4, W(52) + 2, 1, 0), zIndex: 21}}>
            <Fala f={g} y={0} x={0} linhas={[{de: 46, ate: 48, sz: 100}, {de: 49, ate: 51, sz: 112, peso: 700}]} />
            <div style={{position: 'absolute', left: -10, top: 160, width: 600 * risco, height: 16, borderRadius: 9, background: R, transform: 'rotate(-4deg)', transformOrigin: 'left', boxShadow: '0 0 20px rgba(250,95,109,.6)'}} />
          </div>
          <Fala f={g} y={330} linhas={[{de: 52, ate: 55, sz: 96}, {de: 56, ate: 58, sz: 110, peso: 700, grad: [L, A]}]} />
          <div style={{position: 'absolute', inset: 0, perspective: 2200}}>
            <div style={{position: 'absolute', left: 80, top: 760, transform: `rotateY(${ry}deg) rotateX(7deg)`, transformStyle: 'preserve-3d'}}>
              <div style={{position: 'relative', borderRadius: 36, overflow: 'hidden'}}><Site tag="DERMATOLOGIA" a="Pele saudável" b="começa na consulta certa." url="draanapaula.com.br" ic="drop" on={clk} /><Brilho f={g} at={CUT[5] + 6} dur={30} /></div>
            </div>
          </div>
          {g >= W(53) && <div style={{opacity: io(g, W(53), W(53) + 6, 0, 1)}}><Cursor x={cx} y={cy} press={clk > 0 && clk < 0.4 ? 1 : 0} /></div>}
          {Array.from({length: 10}, (_, i) => {
            const p = io(g, W(58), W(58) + 18, 0, 1), an = (i / 10) * Math.PI * 2;
            return <i key={i} style={{position: 'absolute', left: 340 + Math.cos(an) * 160 * p, top: 1240 + Math.sin(an) * 160 * p, width: 16, height: 16, borderRadius: 9, background: i % 2 ? A : L, opacity: p > 0 && p < 1 ? 1 - p : 0, zIndex: 31}} />;
          })}
          <Chip icon="tick" t="Consulta marcada" sub="Qui, 13 · 14h · pelo site" x={300} y={1470} k={ch} rot={-2} z={26} />
          <Bloco n="calendar" s={210} x={850} y={640} t={g} rot={10} blur={10} k={sp(g, CUT[5] + 8)} />
        </>;
      }}</Cena>

      {/* 7. agenda online, aberta 24 horas */}
      <Cena k={6} fundo="escuro">{(g) => {
        const slots = ['08:00', '09:30', '11:00', '14:00', '16:30', '19:00', '21:00', '22:30', '23:45'];
        const c = sp(g, CUT[6] + 2, 14);
        return <>
          <div style={{position: 'absolute', left: -40, top: 560, fontSize: 560, fontWeight: 700, letterSpacing: '-0.08em', lineHeight: 1, ...gradTexto('rgba(90,162,255,.6)', 'rgba(45,127,240,.06)'), transform: `scale(${0.9 + io(g, CUT[6], CUT[7], 0, 0.1)})`, filter: 'blur(1.5px)'}}>24h</div>
          <Fala f={g} y={330} linhas={[{de: 59, ate: 60, sz: 104, cor: '#fff'}, {de: 61, ate: 65, sz: 118, peso: 700, grad: ['#FFFFFF', L], glow: 'rgba(45,127,240,.45)'}]} />
          <div style={{position: 'absolute', inset: 0, perspective: 2200}}>
            <div style={{position: 'absolute', left: 90, top: 900, width: 900, borderRadius: 44, padding: 46, ...VIDRO, transform: `translateY(${(1 - c) * 400}px) rotateX(${10 - c * 4}deg) rotateY(-6deg)`}}>
              <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                <div><div style={{fontSize: 22, letterSpacing: '.2em', color: '#9CC6FF', fontWeight: 600}}>AGENDAR CONSULTA</div><div style={{fontSize: 46, fontWeight: 700, color: '#fff', letterSpacing: '-0.02em'}}>Dra. Ana Paula</div></div>
                <Ico n="moon" s={120} />
              </div>
              <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 18, marginTop: 34}}>
                {slots.map((s, i) => {
                  const on = io(g, CUT[6] + 8 + i * 5, CUT[6] + 12 + i * 5, 0, 1);
                  return <div key={s} style={{padding: '24px 0', textAlign: 'center', borderRadius: 24, fontSize: 34, fontWeight: 600,
                    background: on > 0.5 ? `linear-gradient(180deg, ${L}, ${A})` : 'rgba(255,255,255,.08)', color: '#fff', border: `2px solid ${on > 0.5 ? L : 'rgba(255,255,255,.25)'}`,
                    boxShadow: on > 0.5 ? '0 16px 30px -10px rgba(45,127,240,.8)' : 'none', transform: `scale(${1 + Math.sin(on * Math.PI) * 0.1})`}}>{s}</div>;
                })}
              </div>
            </div>
          </div>
          <Bloco n="clock" s={180} x={830} y={1560} t={g} rot={10} blur={9} k={sp(g, CUT[6] + 10)} />
        </>;
      }}</Cena>

      {/* 8. seu consultório no Google */}
      <Cena k={7} fundo="claro">{(g) => {
        const pin = sp(g, W(69) - 3, 9);
        return <>
          <Fala f={g} y={330} linhas={[{de: 66, ate: 67, sz: 104}, {de: 68, ate: 69, sz: 126, peso: 700, grad: [L, A]}]} />
          <div style={{position: 'absolute', inset: 0, perspective: 2200}}>
            <div style={{position: 'absolute', left: 80, top: 720, width: 920, background: '#fff', borderRadius: 40, overflow: 'hidden', boxShadow: SOMBRA, transform: `rotateY(${interpolate(g, [CUT[7], CUT[8]], [14, 6])}deg) rotateX(8deg)`}}>
              <div style={{height: 540, position: 'relative', background: `linear-gradient(160deg, ${G}, #DCEBFB)`, overflow: 'hidden'}}>
                <svg width={920} height={540} style={{position: 'absolute', inset: 0}}><path d="M0 140H920M0 390H920M220 0V540M660 0V540" stroke="#fff" strokeWidth={36} /><path d="M0 530L920 40" stroke="#fff" strokeWidth={24} /><rect x="270" y="180" width="340" height="160" rx="18" fill={M} opacity=".7" /></svg>
                {[0, 1].map((i) => { const r = io(g, W(69) + 4 + i * 8, W(69) + 30 + i * 8, 0, 1); return <div key={i} style={{position: 'absolute', left: 465 - 160 * r, top: 330 - 50 * r, width: 320 * r, height: 100 * r, borderRadius: '50%', border: `4px solid ${A}`, opacity: 1 - r}} />; })}
                <div style={{position: 'absolute', left: 465 - 70, top: 318, width: 140, height: 28, borderRadius: '50%', background: 'rgba(11,31,58,.25)', filter: 'blur(6px)', transform: `scale(${pin})`}} />
                <div style={{position: 'absolute', left: 340, top: 80 - (1 - pin) * 320, opacity: pin, filter: 'drop-shadow(0 20px 20px rgba(11,31,58,.3))'}}><Ico n="pin" s={250} /></div>
              </div>
              <div style={{padding: '34px 44px', position: 'relative'}}>
                <div style={{position: 'absolute', right: 44, top: -46, padding: '14px 26px', borderRadius: 99, background: `linear-gradient(180deg, ${L}, ${A})`, color: '#fff', fontWeight: 700, fontSize: 34, boxShadow: '0 16px 30px -10px rgba(45,127,240,.8)', transform: `scale(${sp(g, W(69) + 6)})`}}>1º</div>
                <div style={{fontSize: 40, fontWeight: 700, color: N}}>Clínica Dra. Ana Paula</div>
                <div style={{fontSize: 30, color: '#F5B83D', marginTop: 4}}>★★★★★ <span style={{color: C, fontSize: 26}}>· Dermatologia · Aberto agora</span></div>
                <div style={{display: 'flex', gap: 16, marginTop: 24}}><Btn t="Agendar" sz={28} /><span style={{border: '2px solid #E2EAF4', borderRadius: 99, padding: '15px 34px', fontSize: 28, fontWeight: 600, color: N}}>Rotas</span></div>
              </div>
            </div>
          </div>
          <Bloco n="zoom" s={200} x={850} y={600} t={g} rot={10} blur={9} k={sp(g, CUT[7] + 4)} />
        </>;
      }}</Cena>

      {/* 9. WhatsApp a um toque */}
      <Cena k={8} fundo="azul">{(g) => {
        const tap = W(73), b = sp(g, tap + 5);
        return <>
          <Fala f={g} y={330} linhas={[{de: 70, ate: 70, sz: 124, cor: '#fff'}, {de: 71, ate: 73, sz: 124, peso: 700, cor: '#fff', glow: 'rgba(11,31,58,.35)'}]} />
          <div style={{position: 'absolute', inset: 0, perspective: 2200}}>
            <Celular x={250} y={700 + (1 - sp(g, CUT[8])) * 500} w={580} h={1080} rot={`rotateY(${interpolate(g, [CUT[8], CUT[9]], [16, 8])}deg) rotateX(8deg)`}>
              <div style={{padding: '96px 36px 0'}}>
                <div style={{fontSize: 18, fontWeight: 600, letterSpacing: '.2em', color: A}}>PEDIATRIA</div>
                <div style={{fontSize: 44, lineHeight: 1.05, letterSpacing: '-0.03em', margin: '10px 0 22px', color: N}}><b>Cuidado</b> <span style={{fontWeight: 300}}>desde o primeiro dia.</span></div>
                <div style={{height: 200, borderRadius: 28, background: `linear-gradient(160deg, ${G}, ${M})`, display: 'grid', placeItems: 'center'}}><Ico n="baby" s={150} /></div>
                <div style={{marginTop: 24, background: `linear-gradient(180deg, ${L}, ${A})`, color: '#fff', textAlign: 'center', fontWeight: 600, fontSize: 28, borderRadius: 99, padding: 22}}>Agendar consulta</div>
                <div style={{marginTop: 14, border: `3px solid ${g >= tap ? A : '#E2EAF4'}`, textAlign: 'center', fontWeight: 600, fontSize: 28, borderRadius: 99, padding: 20, color: N,
                  boxShadow: `0 0 0 ${io(g, tap, tap + 12, 0, 26)}px rgba(45,127,240,${io(g, tap, tap + 12, 0.35, 0)})`}}>WhatsApp</div>
              </div>
            </Celular>
          </div>
          <Cursor x={io(g, W(70), tap, 860, 610)} y={io(g, W(70), tap, 1760, 1350)} press={g >= tap && g < tap + 5 ? 1 : 0} />
          <div style={{position: 'absolute', left: 90, top: 1540, display: 'flex', alignItems: 'center', gap: 18, background: '#fff', borderRadius: '10px 36px 36px 36px', padding: '26px 32px', fontSize: 34, color: N,
            boxShadow: SOMBRA, transform: `scale(${b})`, transformOrigin: 'left top', zIndex: 26}}><Ico n="chat" s={60} />Olá! Quero agendar.</div>
          <Bloco n="chat" s={190} x={860} y={620} t={g} rot={10} blur={10} k={sp(g, CUT[8] + 4)} />
        </>;
      }}</Cena>

      {/* 10. você cuida das pessoas; a gente faz elas chegarem até você */}
      <Cena k={9} fundo="claro">{(g) => {
        const t2 = W(78);
        const notes: [number, string][] = [[W(81), 'Qui · 09h'], [W(82) + 6, 'Qui · 14h'], [W(84), 'Sex · 10h30']];
        return <>
          <div style={{opacity: io(g, t2 - 4, t2 + 2, 1, 0), filter: `blur(${io(g, t2 - 4, t2 + 2, 0, 10)}px)`}}>
            <Fala f={g} y={330} linhas={[{de: 74, ate: 75, sz: 112}, {de: 76, ate: 77, sz: 124, peso: 700, grad: [L, A]}]} />
            <div style={{position: 'absolute', left: 270, top: 800, transform: `scale(${sp(g, CUT[9] + 3)})`}}>
              <div style={{width: 540, height: 540, borderRadius: '50%', background: 'linear-gradient(150deg,#fff,#EEF5FC 60%,#CFE6F7)', display: 'grid', placeItems: 'center', boxShadow: SOMBRA}}><Ico n="steth" s={340} /></div>
            </div>
            <Bloco n="heart" s={170} x={800} y={760} t={g} rot={10} blur={2} k={sp(g, W(77))} />
          </div>
          <Fala f={g} y={330} linhas={[{de: 78, ate: 81, sz: 96}, {de: 82, ate: 84, sz: 112, peso: 700, grad: [L, A]}]} />
          <div style={{position: 'absolute', inset: 0, perspective: 1800}}>
            {notes.map(([at, s], i) => {
              const k = sp(g, at, 14);
              return <div key={i} style={{position: 'absolute', left: 0, top: 0, transform: `translateZ(${(1 - k) * -900}px)`, opacity: k}}>
                <Chip icon="calendar" t="Nova consulta marcada" sub={s} x={110 + (i % 2) * 70} y={760 + i * 220} k={1} rot={[-2, 2, -1][i]} />
              </div>;
            })}
          </div>
          <Bloco n="user" s={200} x={830} y={1500} t={g} rot={-8} blur={11} k={sp(g, t2)} />
        </>;
      }}</Cena>

      {/* 11. fecho: Web Clinic. Manda SITE no direct. */}
      <Cena k={10} fundo="escuro">{(g) => {
        const typ = Math.floor(io(g, W(88), W(88) + 10, 0, 4, Easing.linear));
        const fim = sp(g, FIM_VOZ + 4);
        const lg = sp(g, W(85) - 2, 11);
        return <>
          {[0, 1].map((i) => <div key={i} style={{position: 'absolute', left: 540 - 320 - i * 110, top: 640 - 320 - i * 110, width: 640 + i * 220, height: 640 + i * 220, borderRadius: '50%', border: `2px solid rgba(90,162,255,${0.35 - i * 0.12})`, transform: `scale(${lg})`}} />)}
          <div style={{position: 'absolute', left: 290, top: 390, width: 500, height: 500, borderRadius: '50%', boxShadow: '0 0 160px rgba(45,127,240,.7), 0 80px 140px -30px rgba(0,0,0,.6)', transform: `scale(${lg})`}}><Logo s={500} /></div>
          <Fala f={g} y={980} align="center" linhas={[{de: 85, ate: 86, sz: 124, peso: 700, grad: ['#FFFFFF', L], glow: 'rgba(45,127,240,.45)'}, {de: 87, ate: 90, sz: 80, cor: '#fff'}]} />
          <div style={{position: 'absolute', left: 80, right: 80, top: 1260, display: 'flex', alignItems: 'center', gap: 20, borderRadius: 99, padding: '18px 18px 18px 44px', fontSize: 44, color: '#fff', ...VIDRO,
            opacity: io(g, W(87), W(87) + 6, 0, 1), transform: `translateY(${io(g, W(87), W(87) + 8, 40, 0)}px)`}}>
            <span style={{flex: 1}}><b>{'SITE'.slice(0, typ)}</b><span style={{display: 'inline-block', width: 3, height: 48, background: L, marginLeft: 6, verticalAlign: 'middle', opacity: g % 20 < 10 ? 1 : 0}} /></span>
            <span style={{width: 100, height: 100, borderRadius: '50%', background: `linear-gradient(180deg, ${L}, ${A})`, display: 'grid', placeItems: 'center', boxShadow: '0 0 30px rgba(45,127,240,.8)', transform: `scale(${g >= W(88) + 12 && g < W(88) + 18 ? 0.88 : 1})`}}>
              <svg width={46} height={46} viewBox="0 0 24 24"><path d="M4 12l16-8-6 16-3-7z" fill="#fff" /></svg></span>
          </div>
          <div style={{position: 'absolute', left: 0, right: 0, top: 1440, textAlign: 'center', color: '#fff', opacity: fim, transform: `translateY(${(1 - fim) * 30}px)`}}>
            <div style={{fontSize: 52, fontWeight: 600}}>@webclinicbrasil</div>
            <div style={{fontSize: 40, color: '#9CC6FF', marginTop: 10}}>WhatsApp (51) 98906-1441</div>
          </div>
        </>;
      }}</Cena>
    </AbsoluteFill>
  );
};
