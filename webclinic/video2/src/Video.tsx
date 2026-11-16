// Web Clinic, vídeo 2: "A Cláudia não dá conta" (Reels 1080x1920, 30 fps). v2 EDITORIAL.
// Direção aprovada (quadros-chave): revista impressa. Cabeçalho de edição (logo + fio + "Nº 02 · seção"),
// títulos gigantes Poppins + Instrument Serif itálico, legendas de foto ("Fig. 01"), papel com fibras, rasgo com borda
// fibrosa, fotos com retícula e borda de papel cortado, fita, carimbo com tinta. Sem emoji, pouca coisa por quadro.
// Movimento em stop-motion (12 qps: tempo quantizado de 2 em 2 quadros + leve "tremida" de papel).
// Sons gerados no ElevenLabs (public/sfx): página, folha deslizando, fita, recado, carimbo, relógio, telefone, notificação.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender, random} from 'remotion';
import AUD from './audio.json';

if (typeof document !== 'undefined') {
  const h = delayRender('fontes');
  const fs = [300, 400, 500, 600, 700].map((w) => new FontFace('Poppins', `url(${staticFile(`fonts/poppins-${w}.woff2`)}) format('woff2')`, {weight: String(w)}));
  fs.push(new FontFace('Serif', `url(${staticFile('fonts/instrument-serif-italic.woff2')}) format('woff2')`, {style: 'italic'}));
  Promise.all(fs.map((ff) => { document.fonts.add(ff); return ff.load(); })).then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
}

const FPS = 30;
const A = '#2D7FF0', N = '#0B1F3A', M = '#CFE6F7', C = '#5E6B7E';
const P = AUD as {texto: string; inicio: number; fim: number}[];
const fr = (s: number) => Math.round(s * FPS);
const W = (i: number) => fr(P[i].inicio);
const FINAL = fr(P[P.length - 1].fim) + 10; // encerramento "boom" depois da voz
const BOOM = FINAL + 30; // pancada da folha azul com o logo
export const DURACAO = BOOM + fr(2.8);
const ABRE = [0, 4, 15, 26, 30, 41, 49, 58, 74, 86];
const CUT = [...ABRE.map((i, k) => (k === 0 ? 0 : W(i) - 5)), FINAL, DURACAO];

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const q = (f: number) => Math.floor(f / 2) * 2; // stop-motion: 12 qps
const io = (f: number, a: number, b: number, x: number, y: number, e = Easing.out(Easing.cubic)) => interpolate(q(f), [a, b], [x, y], {...clamp, easing: e});
// entrada de papel: chega de longe, passa um tiquinho e assenta (em degraus)
const chega = (f: number, at: number, dur = 8) => {
  const t = interpolate(q(f), [at, at + dur], [0, 1], clamp);
  return t < 1 ? Easing.out(Easing.back(1.4))(t) : 1;
};
const tremida = (f: number, seed: string, amp = 1) => ({r: (random(`${seed}r${q(f)}`) - 0.5) * 0.5 * amp, x: (random(`${seed}x${q(f)}`) - 0.5) * 2 * amp, y: (random(`${seed}y${q(f)}`) - 0.5) * 2 * amp});
const bg = (n: string) => `url(${staticFile(`papel-${n}.jpg`)})`;
const SOMBRA = 'drop-shadow(0 2px 1px rgba(11,31,58,.25)) drop-shadow(0 28px 34px rgba(11,31,58,.28))';
const SOMBRA_BOX = '0 1px 1px rgba(11,31,58,.18), 0 18px 30px -12px rgba(11,31,58,.38)';
const SER: React.CSSProperties = {fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400, letterSpacing: '-0.01em'};
const LBL: React.CSSProperties = {fontSize: 27, fontWeight: 600, letterSpacing: '.22em', textTransform: 'uppercase'};

// ---------- peças ----------
const Foto: React.FC<{f: number; src: string; x: number; y: number; w: number; at?: number; de?: 'baixo' | 'dir' | 'esq'; rot?: number; op?: number; seed?: string; dx?: number}> = ({f, src, x, y, w, at = 0, de = 'baixo', rot = 0, op = 1, seed = src, dx = 0}) => {
  const k = chega(f, at, 9);
  const t = tremida(f, seed, 0.6);
  const off = (1 - k) * 900;
  const tx = de === 'dir' ? off : de === 'esq' ? -off : 0, ty = de === 'baixo' ? off : 0;
  if (f < at) return null;
  return <Img src={staticFile(src)} style={{position: 'absolute', left: x + tx + t.x + dx, top: y + ty + t.y, width: w, transform: `rotate(${rot + t.r}deg)`, filter: SOMBRA, opacity: op}} />;
};
const Recado: React.FC<{f: number; at: number; x: number; y: number; rot: number; sz?: number; fita?: boolean; op?: number; children: React.ReactNode}> = ({f, at, x, y, rot, sz = 46, fita, op = 1, children}) => {
  if (f < at) return null;
  const k = chega(f, at, 6);
  const t = tremida(f, `rec${x}${y}`, 0.5);
  return (
    <div style={{position: 'absolute', left: x + t.x, top: y - (1 - k) * 140 + t.y, transform: `rotate(${rot + t.r + (1 - k) * 8}deg) scale(${1.2 - k * 0.2})`, opacity: Math.min(1, k * 2) * op, zIndex: 10}}>
      <div style={{background: bg('branco'), padding: `${sz * 0.42}px ${sz * 0.62}px`, fontSize: sz, fontWeight: 500, color: N, letterSpacing: '-0.015em', whiteSpace: 'nowrap', boxShadow: SOMBRA_BOX}}>{children}</div>
      {fita ? <div style={{position: 'absolute', left: 24, top: -22, width: 150, height: 44, background: 'rgba(207,230,247,.8)', mixBlendMode: 'multiply', transform: 'rotate(-12deg)'}} /> : null}
    </div>
  );
};
const Fita: React.FC<{x: number; y: number; rot: number; w?: number; texto?: string; f?: number; at?: number}> = ({x, y, rot, w = 150, texto, f = 0, at = -1}) => {
  if (at >= 0 && f < at) return null;
  const k = at >= 0 ? chega(f, at, 4) : 1;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: texto ? 70 : 44, background: texto ? A : 'rgba(207,230,247,.8)', mixBlendMode: texto ? 'normal' : 'multiply',
      transform: `rotate(${rot}deg) scaleX(${k})`, transformOrigin: 'left center', display: 'grid', placeItems: 'center', color: '#fff', fontWeight: 700, fontSize: 34, letterSpacing: '.18em',
      boxShadow: texto ? '0 6px 14px -6px rgba(11,31,58,.5)' : 'none', zIndex: 12, clipPath: 'polygon(1% 4%,99% 0,100% 50%,98% 100%,2% 96%,0 50%)'}}>{texto}</div>
  );
};
const Palavras: React.FC<{f: number; de: number; ate: number; k0: number; style?: React.CSSProperties; serifIdx?: number[]; corIdx?: Record<number, string>}> = ({f, de, ate, k0, style, serifIdx = [], corIdx = {}}) => (
  <span style={style}>
    {Array.from({length: ate - de + 1}, (_, j) => de + j).map((i) => {
      const at = W(i) - k0 - 2;
      const k = chega(f, at, 4);
      return <span key={i} style={{display: 'inline-block', marginRight: '0.22em', opacity: f < at ? 0 : 1, transform: `translateY(${(1 - k) * 30}px)`, color: corIdx[i], ...(serifIdx.includes(i) ? SER : {})}}>{P[i].texto}</span>;
    })}
  </span>
);
const Masthead: React.FC<{sec: string; claro?: boolean}> = ({sec, claro}) => (
  <div style={{position: 'absolute', left: 70, right: 70, top: 150, color: claro ? '#fff' : N, zIndex: 30}}>
    <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end'}}>
      <div style={{fontWeight: 700, fontSize: 40, letterSpacing: '-0.04em'}}>web<span style={{color: claro ? M : A}}>clinic</span></div>
      <div style={{...LBL, fontSize: 25}}>Nº 02 · {sec}</div>
    </div>
    <div style={{height: 2, background: 'currentColor', marginTop: 16, opacity: 0.85}} />
  </div>
);
const Legenda: React.FC<{f: number; at: number; x: number; y: number; w: number; fig: string; titulo?: string; texto?: string; claro?: boolean}> = ({f, at, x, y, w, fig, titulo, texto, claro}) => {
  if (f < at) return null;
  const k = chega(f, at, 6);
  return (
    <div style={{position: 'absolute', left: x, top: y + (1 - k) * 40, width: w, color: claro ? '#fff' : N, opacity: Math.min(1, k * 1.5), zIndex: 20}}>
      <div style={{...LBL, color: claro ? M : A}}>{fig}</div>
      {titulo ? <div style={{...SER, fontSize: 76, lineHeight: 1, margin: '12px 0 16px'}}>{titulo}</div> : null}
      {texto ? <div style={{fontSize: 40, lineHeight: 1.32, fontWeight: 400, color: claro ? '#E8F1FD' : N}}>{texto}</div> : null}
    </div>
  );
};
const Rasgo: React.FC<{cor: string; y: number; f: number; at?: number}> = ({cor, y, f, at = 0}) => {
  const k = chega(f, at, 8);
  const yy = y + (1 - k) * 700;
  return (
    <>
      <Img src={staticFile(`rasgo-${cor}.png`)} style={{position: 'absolute', left: 0, top: yy - 60, width: 1080}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: yy + 200, height: 1920, background: bg(cor)}} />
    </>
  );
};
const Relogio: React.FC<{f: number; at: number; x: number; y: number; s: number}> = ({f, at, x, y, s}) => {
  const p = io(f, at, at + 30, 0, 1);
  return (
    <svg style={{position: 'absolute', left: x, top: y, filter: SOMBRA}} width={s} height={s} viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="96" fill="#FAFAF7" />
      <circle cx="100" cy="100" r="88" fill="none" stroke={N} strokeWidth="5" />
      {Array.from({length: 12}, (_, i) => <rect key={i} x="98" y="20" width="4" height={i % 3 ? 9 : 17} fill={N} transform={`rotate(${i * 30} 100 100)`} />)}
      <rect x="96" y="52" width="8" height="52" fill={N} transform={`rotate(${150 + p * 30} 100 100)`} />
      <rect x="98" y="28" width="4" height="76" fill={A} transform={`rotate(${-300 * (1 - p)} 100 100)`} />
      <circle cx="100" cy="100" r="7" fill={N} />
    </svg>
  );
};

// ---------- página: cada cena é uma folha que entra deslizando por cima da anterior (stop-motion) ----------
const Pagina: React.FC<{k: number; papel: string; children: (f: number) => React.ReactNode}> = ({k, papel, children}) => {
  const g = useCurrentFrame();
  const a = CUT[k], b = CUT[k + 1];
  if (g < a || g >= b + 8) return null; // a folha fica embaixo enquanto a próxima entra
  const f = g - a;
  const e = k === 0 ? 1 : interpolate(q(f), [0, 8], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const x = (1 - e) * 1100;
  const rot = (1 - e) * 4;
  return (
    <AbsoluteFill style={{transform: `translateX(${x}px) rotate(${rot}deg)`, transformOrigin: '0% 100%', boxShadow: e < 1 ? '-30px 0 60px rgba(11,31,58,.35)' : 'none', overflow: 'hidden', fontFamily: 'Poppins', zIndex: k}}>
      <AbsoluteFill style={{background: bg(papel)}} />
      {children(f)}
    </AbsoluteFill>
  );
};


// ---------- encerramento ----------
const FOLHAS: {papel: string; rot: number; x: number; y: number; at: number; el: React.ReactNode}[] = [
  {papel: 'gelo', rot: -7, x: 140, y: 380, at: 0, el: <div style={{fontWeight: 700, fontSize: 300, color: A, letterSpacing: '-0.07em', lineHeight: 0.85}}>Cláu-<br />dia.</div>},
  {papel: 'azul', rot: 6, x: 170, y: 420, at: 6, el: <div style={{fontWeight: 700, fontSize: 520, color: N, letterSpacing: '-0.09em', lineHeight: 0.8}}>47</div>},
  {papel: 'branco', rot: -4, x: 120, y: 360, at: 14, el: <div style={{background: A, color: '#fff', fontWeight: 700, fontSize: 78, letterSpacing: '.16em', padding: '20px 30px', transform: 'rotate(-10deg)', marginTop: 200}}>DESISTIU</div>},
  {papel: 'navy', rot: 8, x: 160, y: 400, at: 19, el: <div style={{fontWeight: 300, fontSize: 230, color: '#fff', letterSpacing: '-0.07em'}}>22:47</div>},
  {papel: 'gelo', rot: -9, x: 150, y: 390, at: 24, el: <div style={{border: `9px solid ${A}`, padding: '16px 30px', color: A, fontWeight: 700, fontSize: 96, lineHeight: 0.95, transform: 'rotate(-8deg)', marginTop: 160}}>CONSULTA<br />MARCADA</div>},
];
const Final: React.FC = () => {
  const g = useCurrentFrame();
  if (g < FINAL) return null;
  const f = g - FINAL, b = g - BOOM;
  const tremor = b >= 0 && b < 14 ? (14 - b) / 14 : 0;
  const sx = (random(`sx${q(g)}`) - 0.5) * 36 * tremor, sy = (random(`sy${q(g)}`) - 0.5) * 36 * tremor;
  const bate = b >= 0 ? Math.max(1, 1.45 - Math.floor(b / 2) * 0.15) : 1.45;
  const p = io(g, BOOM + 6, BOOM + 26, 0, 1, Easing.inOut(Easing.cubic));
  return (
    <AbsoluteFill style={{zIndex: 50, background: bg('navy'), fontFamily: 'Poppins', transform: `translate(${sx}px, ${sy}px)`, overflow: 'hidden'}}>
      {FOLHAS.map((s, i) => {
        if (f < s.at) return null;
        const k = chega(f, s.at, 4);
        return (
          <div key={i} style={{position: 'absolute', left: s.x, top: s.y - (1 - k) * 1300, width: 780, height: 1060, background: bg(s.papel), transform: `rotate(${s.rot}deg) scale(${1.1 - k * 0.1})`,
            boxShadow: '0 40px 70px -20px rgba(0,0,0,.55)', padding: 60, display: 'grid', placeItems: 'center', textAlign: 'center'}}>{s.el}</div>
        );
      })}
      {b >= 0 ? (
        <>
          <AbsoluteFill style={{background: bg('azul'), transform: `scale(${bate}) rotate(${b < 6 ? -2 : 0}deg)`, boxShadow: '0 0 0 2000px rgba(11,31,58,.35)'}}>
            <div style={{position: 'absolute', left: 70, right: 70, top: 150, height: 2, background: '#fff', opacity: 0.85}} />
            <div style={{position: 'absolute', left: 70, top: 176, ...LBL, color: M, fontSize: 25}}>Nº 02 · Fim</div>
            <div style={{position: 'absolute', left: 90, right: 90, top: 600}}>
              <svg width="100%" viewBox="26 86 190 100">
                <text x="120" y="124" textAnchor="middle" fontFamily="Poppins" fontWeight={700} fontSize={40} letterSpacing={-1.8}><tspan fill="#fff">web</tspan><tspan fill={M}>clinic</tspan></text>
                <path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke="#fff" strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
              </svg>
            </div>
            <div style={{position: 'absolute', left: 0, right: 0, top: 1080, textAlign: 'center', color: '#fff', fontSize: 60, letterSpacing: '-0.03em', opacity: b >= 10 ? 1 : 0}}>
              Sites que viram<br /><span style={{...SER, fontSize: 84}}>consulta marcada.</span>
            </div>
            <Recado f={b} at={22} x={210} y={1360} rot={-3} sz={50} fita>Manda <b>SITE</b> no direct</Recado>
          </AbsoluteFill>
          {/* estouro: pedaços de papel voando a partir do centro */}
          {Array.from({length: 18}, (_, i) => {
            const ang = (i / 18) * Math.PI * 2 + random(`a${i}`) * 0.4;
            const vel = 40 + random(`v${i}`) * 50;
            const t = q(b);
            const x = 540 + Math.cos(ang) * vel * t, y = 960 + Math.sin(ang) * vel * t + 2.2 * t * t;
            if (t > 26) return null;
            return <div key={i} style={{position: 'absolute', left: x, top: y, width: 26 + random(`w${i}`) * 40, height: 18 + random(`h${i}`) * 26, background: [M, '#fff', N][i % 3],
              transform: `rotate(${random(`r${i}`) * 360 + t * 25}deg)`, boxShadow: '0 6px 10px rgba(0,0,0,.25)', opacity: t > 20 ? (26 - t) / 6 : 1}} />;
          })}
          {b < 3 ? <AbsoluteFill style={{background: '#fff', opacity: b === 0 ? 0.85 : 0.35}} /> : null}
        </>
      ) : null}
    </AbsoluteFill>
  );
};

export const Video: React.FC = () => {
  const e = (k: number, i: number) => W(i) - CUT[k];
  return (
    <AbsoluteFill style={{background: N}}>
      {/* 1. capa: "Essa é a Cláudia." */}
      <Pagina k={0} papel="gelo">
        {(f) => (
          <>
            <Masthead sec="Recepção" />
            <div style={{position: 'absolute', left: 58, top: 255, fontWeight: 700, fontSize: 322, lineHeight: 0.8, letterSpacing: '-0.07em', color: A, transform: `scale(${1.12 - chega(f, 0, 6) * 0.12})`, transformOrigin: '0 0'}}>Cláu-<br />dia.</div>
            <Rasgo cor="azul" y={1180} f={f} at={2} />
            <Foto f={f} src="claudia-base-imp.png" x={400} y={560} w={900} at={4} />
            <Legenda f={f} at={e(0, 2)} x={70} y={1340} w={330} fig="Fig. 01" titulo="Essa é a Cláudia." claro />
          </>
        )}
      </Pagina>

      {/* 2. telefone, WhatsApp, porta, Instagram: índice de revista */}
      <Pagina k={1} papel="gelo">
        {(f) => {
          const itens: [number, string, string][] = [[7, '01', 'Telefone'], [9, '02', 'WhatsApp'], [11, '03', 'A porta'], [14, '04', 'Instagram']];
          const t = tremida(f, 'fone', f >= e(1, 7) && f < e(1, 7) + 24 ? 7 : 0.5);
          return (
            <>
              <Masthead sec="Recepção" />
              <div style={{position: 'absolute', left: 70, top: 270, color: N}}>
                <div style={{...LBL, color: A}}>O dia da Cláudia</div>
                <div style={{fontWeight: 300, fontSize: 88, letterSpacing: '-0.05em', lineHeight: 1.05, marginTop: 14}}>Ela <b style={{fontWeight: 700}}>atende</b></div>
              </div>
              {itens.map(([i, n, t2], j) => {
                const at = e(1, i) - 2;
                if (f < at) return null;
                const k = chega(f, at, 6);
                return (
                  <div key={n} style={{position: 'absolute', left: 70 - (1 - k) * 500, top: 520 + j * 170, display: 'flex', alignItems: 'baseline', gap: 26, color: N}}>
                    <span style={{...SER, fontSize: 64, color: A, width: 70}}>{n}</span>
                    <span style={{fontWeight: 700, fontSize: 96, letterSpacing: '-0.05em'}}>{t2}</span>
                  </div>
                );
              })}
              <div style={{position: 'absolute', left: 70, right: 70, top: 1220, height: 2, background: N, opacity: 0.25}} />
              <Foto f={f} src="claudia-base-imp.png" x={600} y={1000} w={600} at={2} de="dir" />
              {f >= e(1, 7) - 4 ? <Img src={staticFile('telefone-imp.png')} style={{position: 'absolute', left: 60 + t.x, top: 1300 + t.y, width: 520, transform: `rotate(${-7 + t.r * 4}deg)`, filter: SOMBRA}} /> : null}
              <Legenda f={f} at={e(1, 14) + 4} x={70} y={1250} w={480} fig="Ao mesmo tempo" />
            </>
          );
        }}
      </Pagina>

      {/* 3. perguntas repetidas */}
      <Pagina k={2} papel="azul">
        {(f) => {
          const big = e(2, 23);
          const apaga = f >= big ? 0.45 : 1;
          return (
            <>
              <Masthead sec="O problema" claro />
              <Recado f={f} at={e(2, 15) - 2} x={80} y={330} rot={-4} fita op={apaga}>Qual o valor?</Recado>
              <Recado f={f} at={e(2, 18) - 2} x={380} y={560} rot={5} op={apaga}>Atende convênio?</Recado>
              <Recado f={f} at={e(2, 20) - 2} x={110} y={790} rot={-2} fita op={apaga}>Tem horário hoje?</Recado>
              <Recado f={f} at={e(2, 18) + 4} x={620} y={1010} rot={-6} sz={34} op={apaga}>Aceita Pix?</Recado>
              <Recado f={f} at={e(2, 20) + 4} x={90} y={1040} rot={4} sz={34} op={apaga}>Pode encaixar?</Recado>
              {f >= big - 2 ? (
                <div style={{position: 'absolute', left: 60, right: 40, top: 1150, color: '#fff', transform: `scale(${1.15 - chega(f, big - 2, 5) * 0.15})`, transformOrigin: '0 50%'}}>
                  <div style={{...LBL, color: M}}>De novo</div>
                  <div style={{...SER, fontSize: 196, lineHeight: 0.9, marginTop: 6}}>Qual o</div>
                  <div style={{fontWeight: 700, fontSize: 200, letterSpacing: '-0.06em', lineHeight: 0.9}}>valor?</div>
                </div>
              ) : null}
            </>
          );
        }}
      </Pagina>

      {/* 4. 47 vezes por dia */}
      <Pagina k={3} papel="azul">
        {(f) => {
          const n = Math.round(interpolate(q(f), [0, 14], [1, 47], {...clamp, easing: Easing.out(Easing.cubic)}));
          return (
            <>
              <Masthead sec="O problema" claro />
              <div style={{position: 'absolute', left: 30, top: 270, fontWeight: 700, fontSize: 820, lineHeight: 0.78, letterSpacing: '-0.09em', color: N}}>{n}</div>
              <div style={{position: 'absolute', left: 610, top: 930, color: '#fff'}}>
                {f >= e(3, 27) - 2 ? <div style={{...SER, fontSize: 104, lineHeight: 0.9}}>vezes.</div> : null}
                {f >= e(3, 28) - 2 ? <div style={{fontWeight: 700, fontSize: 104, letterSpacing: '-0.05em', lineHeight: 1}}>Por dia.</div> : null}
              </div>
              <Foto f={f} src="claudia-estresse-imp.png" x={-80} y={1130} w={1000} at={2} />
              <Recado f={f} at={6} x={690} y={1330} rot={-3} sz={34}>Qual o valor?</Recado>
            </>
          );
        }}
      </Pagina>

      {/* 5. três desistem e marcam no concorrente */}
      <Pagina k={4} papel="branco">
        {(f) => {
          const des = e(4, 35);
          return (
            <>
              <Masthead sec="O problema" />
              <div style={{position: 'absolute', left: 70, right: 70, top: 270, color: N, fontSize: 92, lineHeight: 1.04, letterSpacing: '-0.05em'}}>
                <Palavras f={f} de={30} ate={34} k0={CUT[4]} style={{fontWeight: 300}} />
                <br />
                <Palavras f={f} de={35} ate={36} k0={CUT[4]} style={{fontWeight: 700}} serifIdx={[35]} corIdx={{35: A}} />
              </div>
              {[0, 1, 2].map((i) => {
                const at = 4 + i * 2;
                if (f < at) return null;
                const k = chega(f, at, 7);
                const morto = f >= des + i * 4;
                const t = tremida(f, `pac${i}`, 0.5);
                return (
                  <div key={i} style={{position: 'absolute', left: 70 + i * 320 + t.x, top: 640 + (1 - k) * 900 + (i === 1 ? 30 : 0), width: 300, transform: `rotate(${[-3, 2, -1.5][i] + t.r}deg)`}}>
                    <div style={{background: bg('gelo'), padding: 14, boxShadow: SOMBRA_BOX, height: 520, overflow: 'hidden', position: 'relative'}}>
                      <Img src={staticFile(`paciente${i}-imp.png`)} style={{position: 'absolute', left: '50%', bottom: -120, height: 620, transform: 'translateX(-50%)', opacity: morto ? 0.45 : 1}} />
                    </div>
                    <div style={{...LBL, fontSize: 25, color: C, marginTop: 14}}>Paciente 0{i + 1}</div>
                    <Fita x={-10} y={230} rot={-14 + i * 6} w={320} texto="DESISTIU" f={f} at={des + i * 4} />
                  </div>
                );
              })}
              {f >= e(4, 37) - 2 ? (
                <div style={{position: 'absolute', left: 70, right: 70, top: 1290, color: N, opacity: Math.min(1, chega(f, e(4, 37) - 2, 6) * 1.5)}}>
                  <div style={{height: 2, background: N, opacity: 0.25, marginBottom: 26}} />
                  <div style={{fontSize: 64, lineHeight: 1.05, letterSpacing: '-0.04em'}}><span style={SER}>e marcam</span> <b style={{fontWeight: 700}}>no concorrente.</b></div>
                </div>
              ) : null}
            </>
          );
        }}
      </Pagina>

      {/* 6. às seis a Cláudia vai pra casa. Merecido. */}
      <Pagina k={5} papel="gelo">
        {(f) => {
          const anda = io(f, e(5, 44), e(5, 47) + 12, 0, 1, Easing.inOut(Easing.cubic));
          return (
            <>
              <Masthead sec="18:00" />
              <Relogio f={f} at={0} x={70} y={290} s={380} />
              <div style={{position: 'absolute', left: 70, top: 730, color: N}}>
                {f >= e(5, 41) - 2 ? <div style={{fontWeight: 700, fontSize: 150, letterSpacing: '-0.06em', lineHeight: 0.95}}>Às seis,</div> : null}
                <div style={{fontSize: 64, fontWeight: 300, letterSpacing: '-0.04em', lineHeight: 1.1, marginTop: 10, width: 520}}><Palavras f={f} de={43} ate={47} k0={CUT[5]} /></div>
              </div>
              <Foto f={f} src="claudia-tchau-imp.png" x={560} y={430} w={470} at={2} de="dir" dx={anda * 160} />
              {f >= e(5, 48) - 2 ? (
                <div style={{position: 'absolute', left: 70, top: 1230, color: A, transform: `scale(${1.1 - chega(f, e(5, 48) - 2, 5) * 0.1})`, transformOrigin: '0 50%'}}>
                  <div style={{...LBL, color: N}}>Fig. 02</div>
                  <div style={{...SER, fontSize: 170, lineHeight: 1}}>Merecido.</div>
                </div>
              ) : null}
            </>
          );
        }}
      </Pagina>

      {/* 7. às dez da noite tem paciente querendo marcar */}
      <Pagina k={6} papel="navy">
        {(f) => {
          const msg = e(6, 54) - 2;
          return (
            <>
              <Masthead sec="Domingo" claro />
              <div style={{position: 'absolute', left: 60, top: 260, color: '#fff', fontWeight: 300, fontSize: 290, letterSpacing: '-0.07em', lineHeight: 1}}>22:47</div>
              <div style={{position: 'absolute', left: 70, top: 600, color: M, fontSize: 60, lineHeight: 1.1, letterSpacing: '-0.03em', width: 900}}>
                <Palavras f={f} de={49} ate={53} k0={CUT[6]} style={{fontWeight: 300}} serifIdx={[49]} />
              </div>
              {f >= msg ? (
                <div style={{position: 'absolute', left: 120, top: 860 - (1 - chega(f, msg, 7)) * 200, width: 840, transform: `rotate(-2deg)`, opacity: Math.min(1, chega(f, msg, 7) * 2)}}>
                  <div style={{background: bg('branco'), padding: '34px 40px', boxShadow: '0 30px 60px -20px rgba(0,0,0,.6)'}}>
                    <div style={{...LBL, color: A}}>WhatsApp · Clínica</div>
                    <div style={{fontSize: 56, fontWeight: 500, color: N, letterSpacing: '-0.03em', margin: '16px 0 18px'}}>Oi! Tem horário amanhã?</div>
                    <div style={{fontSize: 32, color: C}}>Enviada às 22:47 · sem resposta</div>
                  </div>
                </div>
              ) : null}
              <Legenda f={f} at={e(6, 55)} x={70} y={1260} w={900} fig="Fig. 03" texto="A recepção está fechada. O paciente, não." claro />
            </>
          );
        }}
      </Pagina>

      {/* 8. com a Web Clinic o site responde, mostra os horários e marca. Sozinho. */}
      <Pagina k={7} papel="gelo">
        {(f) => {
          const hor = e(7, 68) - 2, marca = e(7, 70), carimbo = e(7, 72) - 1;
          const slots = ['09:00', '10:30', '14:30', '16:00', '17:30', '19:00'];
          const ck = chega(f, carimbo, 3);
          return (
            <>
              <Masthead sec="A solução" />
              <div style={{position: 'absolute', left: 70, top: 270, color: N, fontSize: 96, letterSpacing: '-0.05em', lineHeight: 1.04}}>
                <Palavras f={f} de={58} ate={59} k0={CUT[7]} style={{fontWeight: 300}} /><br />
                <Palavras f={f} de={60} ate={61} k0={CUT[7]} style={{fontWeight: 700}} corIdx={{61: A}} />
              </div>
              {f >= 4 ? (
                <div style={{position: 'absolute', left: 110, top: 600 + (1 - chega(f, 4, 9)) * 1200, width: 860, transform: 'rotate(-3deg)', background: bg('branco'), padding: '36px 42px 42px', boxShadow: SOMBRA_BOX}}>
                  <div style={{display: 'flex', justifyContent: 'space-between'}}><div style={{...LBL, color: A}}>Agenda online · 24h</div><div style={{...LBL, fontSize: 20, color: '#9AA6B6'}}>suaclinica.com.br</div></div>
                  <div style={{fontSize: 56, letterSpacing: '-0.04em', color: N, margin: '20px 0 26px'}}><b>Escolha</b> <span style={{fontWeight: 300}}>um horário</span></div>
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 14}}>
                    {slots.map((s, i) => {
                      const on = i === 2 && f >= marca;
                      return <div key={s} style={{height: 92, display: 'grid', placeItems: 'center', fontSize: 36, fontWeight: 600, border: `2px solid ${on ? A : '#DDE4EC'}`, background: on ? A : 'transparent',
                        color: on ? '#fff' : N, opacity: f >= hor + i ? 1 : 0.15}}>{s}</div>;
                    })}
                  </div>
                  <div style={{marginTop: 24, height: 96, background: N, color: '#fff', display: 'grid', placeItems: 'center', fontSize: 38, fontWeight: 600, transform: `scale(${f >= marca && f < marca + 4 ? 0.97 : 1})`}}>Agendar consulta</div>
                </div>
              ) : null}
              {f >= e(7, 64) ? <Recado f={f} at={e(7, 64)} x={330} y={1150} rot={4} sz={36}>"R$ 350 · aceita convênio"</Recado> : null}
              {f >= carimbo ? (
                <div style={{position: 'absolute', left: 140, top: 1240, transform: `rotate(-11deg) scale(${1.6 - ck * 0.6})`, opacity: Math.min(1, ck * 2), mixBlendMode: 'multiply', zIndex: 15}}>
                  <div style={{border: `9px solid ${A}`, padding: '16px 34px', color: A, fontWeight: 700, fontSize: 92, letterSpacing: '.01em', lineHeight: 0.95,
                    WebkitMaskImage: `${bg('gelo')}`, WebkitMaskSize: '260px'}}>CONSULTA<br />MARCADA</div>
                </div>
              ) : null}
              {f >= e(7, 73) - 2 ? <div style={{position: 'absolute', left: 620, top: 1500, ...SER, fontSize: 120, color: N, transform: `scale(${1.1 - chega(f, e(7, 73) - 2, 5) * 0.1})`}}>Sozinho.</div> : null}
            </>
          );
        }}
      </Pagina>

      {/* 9. a Cláudia cuida de quem chega; o site, de quem procura */}
      <Pagina k={8} papel="gelo">
        {(f) => (
          <>
            <Masthead sec="A solução" />
            <div style={{position: 'absolute', left: 70, right: 70, top: 270, color: N, letterSpacing: '-0.05em', lineHeight: 1.04}}>
              <div style={{fontSize: 80, fontWeight: 300}}><Palavras f={f} de={74} ate={79} k0={CUT[8]} /></div>
              <div style={{height: 2, background: N, opacity: 0.25, margin: '30px 0'}} />
              <div style={{fontSize: 92}}><Palavras f={f} de={80} ate={85} k0={CUT[8]} style={{fontWeight: 700}} serifIdx={[83, 84]} corIdx={{83: A, 84: A}} /></div>
            </div>
            <Rasgo cor="azul" y={1180} f={f} at={2} />
            {f >= 3 ? (() => {
              const k = chega(f, 3, 9);
              const t = tremida(f, 'cafe', 0.6);
              return (
                <div style={{position: 'absolute', left: 80 + t.x, top: 930 + (1 - k) * 900 + t.y, width: 560, transform: `rotate(${-3 + t.r}deg)`, zIndex: 6}}>
                  <div style={{background: bg('branco'), padding: '18px 18px 0', boxShadow: SOMBRA_BOX}}>
                    <div style={{height: 740, background: bg('gelo'), overflow: 'hidden', position: 'relative'}}>
                      <Img src={staticFile('claudia-cafe-imp.png')} style={{position: 'absolute', left: '50%', bottom: 0, width: 450, transform: 'translateX(-50%)'}} />
                    </div>
                    <div style={{...LBL, fontSize: 24, color: C, padding: '18px 4px 20px'}}>Cláudia · 15:00</div>
                  </div>
                  <div style={{position: 'absolute', left: 190, top: -22, width: 180, height: 46, background: 'rgba(207,230,247,.8)', mixBlendMode: 'multiply', transform: 'rotate(4deg)'}} />
                </div>
              );
            })() : null}
            <Legenda f={f} at={e(8, 80)} x={680} y={1300} w={340} fig="Fig. 04" texto="Ela atende quem está na recepção. O resto, o site resolve." claro />
          </>
        )}
      </Pagina>

      {/* 10. assinatura */}
      <Pagina k={9} papel="azul">
        {(f) => {
          const p = io(f, 6, 26, 0, 1, Easing.inOut(Easing.cubic));
          return (
            <>
              <div style={{position: 'absolute', left: 70, right: 70, top: 150, height: 2, background: '#fff', opacity: 0.85}} />
              <div style={{position: 'absolute', left: 120, right: 120, top: 560, transform: `scale(${1.08 - chega(f, 0, 6) * 0.08})`}}>
                <svg width="100%" viewBox="26 86 190 100">
                  <text x="120" y="124" textAnchor="middle" fontFamily="Poppins" fontWeight={700} fontSize={40} letterSpacing={-1.8}><tspan fill="#fff">web</tspan><tspan fill={M}>clinic</tspan></text>
                  <path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke="#fff" strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
                </svg>
              </div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 1000, textAlign: 'center', color: '#fff', fontSize: 52, letterSpacing: '-0.03em', opacity: f >= 10 ? 1 : 0}}>
                Sites que viram <span style={SER}>consulta marcada.</span>
              </div>
              <Recado f={f} at={e(9, 88) - 2} x={190} y={1220} rot={-3} sz={58} fita>Manda <b>SITE</b> no direct</Recado>
            </>
          );
        }}
      </Pagina>

      {/* 11. encerramento "boom": as páginas do vídeo caem uma sobre a outra e a folha azul do logo bate por cima */}
      <Final />

      {/* ---------- som ---------- */}
      <Audio src={staticFile('voz.mp3')} />
      {CUT.slice(1, -1).map((c, i) => <Sequence key={`pg${i}`} from={c} durationInFrames={40}><Audio src={staticFile(i === 2 ? 'sfx/rasgo.mp3' : 'sfx/pagina.mp3')} volume={0.55} /></Sequence>)}
      <Sequence from={2} durationInFrames={40}><Audio src={staticFile('sfx/desliza.mp3')} volume={0.5} /></Sequence>
      <Sequence from={W(7) - 3} durationInFrames={78}><Audio src={staticFile('sfx/telefone.mp3')} volume={0.32} /></Sequence>
      {[[1, 7], [1, 9], [1, 11], [1, 14]].map(([k, i]) => <Sequence key={`l${i}`} from={W(i) - 2} durationInFrames={30}><Audio src={staticFile('sfx/desliza.mp3')} volume={0.3} /></Sequence>)}
      {[15, 18, 20].map((i) => <Sequence key={`r${i}`} from={W(i) - 2} durationInFrames={30}><Audio src={staticFile('sfx/papelzinho.mp3')} volume={0.6} /></Sequence>)}
      <Sequence from={W(15) + 2} durationInFrames={30}><Audio src={staticFile('sfx/fita.mp3')} volume={0.4} /></Sequence>
      <Sequence from={W(23) - 2} durationInFrames={40}><Audio src={staticFile('sfx/desliza.mp3')} volume={0.6} /></Sequence>
      {[0, 1, 2].map((i) => <Sequence key={`d${i}`} from={W(35) + i * 4} durationInFrames={30}><Audio src={staticFile('sfx/fita.mp3')} volume={0.45} /></Sequence>)}
      <Sequence from={CUT[5]} durationInFrames={80}><Audio src={staticFile('sfx/relogio.mp3')} volume={0.4} /></Sequence>
      <Sequence from={W(54) - 2} durationInFrames={60}><Audio src={staticFile('sfx/notificacao.mp3')} volume={0.45} /></Sequence>
      <Sequence from={W(64)} durationInFrames={30}><Audio src={staticFile('sfx/papelzinho.mp3')} volume={0.5} /></Sequence>
      <Sequence from={W(72) - 1} durationInFrames={60}><Audio src={staticFile('sfx/carimbo.mp3')} volume={0.75} /></Sequence>
      <Sequence from={W(88) - 2} durationInFrames={30}><Audio src={staticFile('sfx/fita.mp3')} volume={0.45} /></Sequence>
      <Sequence from={FINAL} durationInFrames={32}><Audio src={staticFile('sfx/pilha.mp3')} volume={0.7} /></Sequence>
      <Sequence from={BOOM - 1} durationInFrames={150}><Audio src={staticFile('sfx/boom.mp3')} volume={0.95} /></Sequence>
      <Sequence from={BOOM + 22} durationInFrames={40}><Audio src={staticFile('sfx/fita.mp3')} volume={0.4} /></Sequence>
    </AbsoluteFill>
  );
};
