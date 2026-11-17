// Web Clinic, vídeo 3: "Aguarde na linha" v3 PREMIUM (Reels 1080x1920, 30 fps, 33,6 s). Áudio aprovado (trilha.mp3).
// v2 reprovada no movimento ("não está premium"): interface chapada em tela cheia, cortes secos com "soco" de zoom,
// texto parado, selos de adesivo.
// v3: um celular 3D flutuando num espaço escuro com luz azul, câmera contínua com curvas suaves (entra no teclado,
// recua, gira), profundidade de campo, desfoque de movimento real (@remotion/motion-blur), números de contador
// mecânico (odômetro), o cronômetro sai do celular para a frente da câmera na espera, o celular cai quando a
// ligação cai, transição por círculo de luz azul, tipografia revelada por máscara. Legenda em faixa fixa com véu escuro.
import React from 'react';
import {AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender, random, spring} from 'remotion';
import {CameraMotionBlur} from '@remotion/motion-blur';
import FALAS from './falas.json';
import ENV from './envelope.json';

if (typeof document !== 'undefined') {
  const h = delayRender('fontes');
  const fs = [300, 400, 500, 600, 700].map((w) => new FontFace('Poppins', `url(${staticFile(`fonts/poppins-${w}.woff2`)}) format('woff2')`, {weight: String(w)}));
  fs.push(new FontFace('Serif', `url(${staticFile('fonts/instrument-serif-italic.woff2')}) format('woff2')`, {style: 'italic'}));
  Promise.all(fs.map((ff) => { document.fonts.add(ff); return ff.load(); })).then(() => continueRender(h)).catch(() => continueRender(h));
}

const FPS = 30;
const A = '#2D7FF0', N = '#0B1F3A', L = '#5AA2FF', M = '#CFE6F7', G = '#EEF5FC', R = '#FA5F6D';
export const DURACAO = Math.round(33.6 * FPS);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const eOut = Easing.bezier(0.16, 1, 0.3, 1); // expo out
const eIO = Easing.bezier(0.65, 0, 0.35, 1); // in-out suave
const io = (t: number, a: number, b: number, x: number, y: number, e = eOut) => interpolate(t, [a, b], [x, y], {...clamp, easing: e});
const SER: React.CSSProperties = {fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400};
type W = {texto: string; inicio: number; fim: number};
const F = FALAS as Record<string, W[]>;

// ---------- tempo ----------
const TRECHOS: [string, number, number, number][] = [
  ['ura', 0.0, 2.74, 1.8], ['ura', 6.8, 9.19, 4.7], ['ura', 11.0, 15.67, 7.5], ['ura', 3.25, 5.79, 12.6],
  ['paciente', 2.0, 3.2, 15.3], ['ura', 16.5, 19.28, 16.8], ['paciente', 3.6, 6.26, 20.4],
];
const TROCA: Record<string, string> = {'clínica': 'Clínica', 'bem': 'Bem', '-estar.': 'Estar.', '1.': 'um.'};
const DESTAQUE = ['importante', 'ocupados.', 'aguarde', 'tecle', 'um.'];
const linhas = TRECHOS.map(([voz, a, b, pos]) => ({voz, pos, fim: pos + (b - a),
  ws: F[voz].filter((w) => w.inicio >= a - 0.05 && w.inicio < b).map((w) => ({t: TROCA[w.texto] ?? w.texto, at: pos + (w.inicio - a)}))}));
const ATENDE = 1.8, TEC0 = 4.6, TEC1 = 7.45, ESPERA = 12.2, CAI = 19.8, VIRA = 23.0, SITE = 25.7, FIM = 29.9;
const segundos = (t: number) => (t < ATENDE ? 0 : t < ESPERA ? t - ATENDE : t < CAI ? interpolate(t, [ESPERA, CAI - 0.4], [ESPERA - ATENDE, 277], {...clamp, easing: Easing.bezier(0.5, 0, 0.9, 0.6)}) : 277);

// ---------- câmera contínua (keyframes com curva suave) ----------
type K = {t: number; s: number; x: number; y: number; rx: number; ry: number; rz: number};
const CAM: K[] = [
  {t: 0.0, s: 0.78, x: 120, y: 420, rx: 16, ry: -26, rz: 4},
  {t: 1.8, s: 0.92, x: 0, y: 90, rx: 6, ry: -10, rz: 1},
  {t: 4.3, s: 0.98, x: 0, y: 40, rx: 3, ry: -5, rz: 0},
  {t: 5.3, s: 1.82, x: 0, y: -500, rx: 0, ry: 0, rz: 0}, // entra no teclado
  {t: 7.3, s: 1.9, x: 0, y: -530, rx: 0, ry: 0, rz: 0},
  {t: 8.6, s: 0.95, x: 0, y: 40, rx: 4, ry: 9, rz: -1},
  {t: 12.0, s: 1.0, x: 0, y: 20, rx: 2, ry: 4, rz: 0},
  {t: 13.2, s: 0.66, x: 0, y: 640, rx: 14, ry: 14, rz: 0}, // recua: o cronômetro vai pra frente
  {t: 19.7, s: 0.62, x: 0, y: 680, rx: 16, ry: 18, rz: 0},
];
const cam = (t: number): K => {
  let i = CAM.findIndex((k) => k.t > t);
  if (i === -1) return CAM[CAM.length - 1];
  if (i === 0) return CAM[0];
  const a = CAM[i - 1], b = CAM[i];
  const p = eIO((t - a.t) / (b.t - a.t));
  const m = (u: number, v: number) => u + (v - u) * p;
  return {t, s: m(a.s, b.s), x: m(a.x, b.x), y: m(a.y, b.y), rx: m(a.rx, b.rx), ry: m(a.ry, b.ry), rz: m(a.rz, b.rz)};
};

// ---------- peças ----------
// contador mecânico: cada dígito rola na vertical
const Digito: React.FC<{v: number; h: number; cor: string}> = ({v, h, cor}) => {
  const base = Math.floor(v), fr = v - base;
  const suave = fr > 0.85 ? (fr - 0.85) / 0.15 : 0; // só rola no fim de cada unidade
  return (
    <span style={{display: 'inline-block', height: h, overflow: 'hidden', verticalAlign: 'top', position: 'relative', width: '0.6em'}}>
      <span style={{display: 'block', transform: `translateY(${-suave * h}px)`}}>
        <span style={{display: 'block', height: h, lineHeight: `${h}px`, color: cor, textAlign: 'center'}}>{base % 10}</span>
        <span style={{display: 'block', height: h, lineHeight: `${h}px`, color: cor, textAlign: 'center'}}>{(base + 1) % 10}</span>
      </span>
    </span>
  );
};
const Odometro: React.FC<{seg: number; sz: number; cor: string; peso?: number}> = ({seg, sz, cor, peso = 300}) => {
  const h = Math.round(sz * 1.05);
  const mm = seg / 60, ss = seg % 60;
  return (
    <span style={{fontSize: sz, fontWeight: peso, letterSpacing: '-0.04em', fontVariantNumeric: 'tabular-nums', display: 'inline-flex', alignItems: 'flex-start', height: h}}>
      <Digito v={mm / 10} h={h} cor={cor} /><Digito v={mm % 10} h={h} cor={cor} />
      <span style={{lineHeight: `${h * 0.95}px`, color: cor, width: '0.26em', textAlign: 'center'}}>:</span>
      <Digito v={ss / 10} h={h} cor={cor} /><Digito v={ss % 10} h={h} cor={cor} />
    </span>
  );
};
const Onda: React.FC<{f: number; cor: string; altura: number; n?: number; larg?: number}> = ({f, cor, altura, n = 28, larg = 10}) => {
  const env = (ENV as number[])[Math.min(f, (ENV as number[]).length - 1)] ?? 0;
  return (
    <div style={{height: altura, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
      {Array.from({length: n}, (_, i) => {
        const k = 0.3 + 0.7 * Math.abs(Math.sin(i * 0.9 + f * 0.22)) * (0.75 + 0.25 * Math.sin(i * 2.3 + f * 0.13));
        return <div key={i} style={{width: larg, height: Math.max(larg, altura * env * k), borderRadius: larg / 2, background: cor, opacity: 0.35 + env * 0.65}} />;
      })}
    </div>
  );
};
const Ic: Record<string, React.ReactNode> = {
  mudo: <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"><rect x="9" y="3" width="6" height="11" rx="3" /><path d="M5 11a7 7 0 0 0 14 0M12 18v3" /></svg>,
  teclado: <svg width="46" height="46" viewBox="0 0 24 24" fill="currentColor">{[0, 1, 2].flatMap((r) => [0, 1, 2].map((c) => <circle key={`${r}${c}`} cx={6 + c * 6} cy={5 + r * 6} r="1.8" />))}</svg>,
  viva: <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"><path d="M4 9v6h4l5 4V5L8 9H4z" /><path d="M16 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12" /></svg>,
  desliga: <svg width="54" height="54" viewBox="0 0 24 24" fill="currentColor"><path d="M2.5 13.5c5.3-4.6 13.7-4.6 19 0l-2.3 2.6c-.4.4-1 .5-1.5.2l-2.6-1.6c-.4-.3-.6-.8-.5-1.3l.3-1.6c-2-.7-4.8-.7-6.8 0l.3 1.6c.1.5-.1 1-.5 1.3l-2.6 1.6c-.5.3-1.1.2-1.5-.2z" /></svg>,
};

// tela da chamada (dentro do celular, 660 x 1400)
const TelaChamada: React.FC<{t: number; f: number}> = ({t, f}) => {
  const caiu = t >= CAI;
  const status = t < 0.9 ? 'discando…' : t < ATENDE ? 'chamando…' : t < ESPERA ? 'em ligação' : t < CAI ? 'em espera ♪' : 'chamada encerrada';
  const numero = '(51) 3333-0147';
  const dig = Math.floor(io(t, 0.1, 1.0, 0, 14, Easing.linear));
  const tecladoK = io(t, TEC0 + 0.2, TEC0 + 0.6, 0, 1) * io(t, TEC1 + 0.1, TEC1 + 0.5, 1, 0);
  const timerFora = io(t, ESPERA, ESPERA + 1.0, 0, 1); // o cronômetro sai da tela
  const pulso = t >= 0.9 && t < ATENDE ? (Math.sin(t * 9) + 1) / 2 : 0;
  return (
    <div style={{position: 'absolute', inset: 0, background: caiu ? `radial-gradient(900px 700px at 50% 25%, #5A1A2E, #1A0610)` : `radial-gradient(900px 800px at 50% 18%, #1E4387, ${N} 60%, #060D20)`, color: '#fff', fontFamily: 'Poppins', overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', opacity: 1 - tecladoK}}>
        <div style={{width: 200, height: 200, borderRadius: 100, margin: '0 auto', background: caiu ? `linear-gradient(160deg, #FF8D96, ${R})` : `linear-gradient(160deg, ${L}, ${A})`, display: 'grid', placeItems: 'center',
          fontSize: 80, fontWeight: 600, letterSpacing: '-0.04em', boxShadow: `0 0 0 ${pulso * 26}px rgba(90,162,255,${0.25 * (1 - pulso)}), 0 24px 60px -18px rgba(45,127,240,.8)`}}>BE</div>
        <div style={{fontSize: 56, fontWeight: 600, letterSpacing: '-0.035em', marginTop: 34}}>Clínica Bem Estar</div>
        <div style={{fontSize: 32, color: caiu ? '#FFB3BA' : M, marginTop: 4, opacity: 0.9}}>{t < ATENDE ? (dig < 14 ? numero.slice(0, dig) : status) : status}</div>
        <div style={{marginTop: 34, height: 140, opacity: (t < ATENDE ? 0.25 : 1) * (1 - timerFora), transform: `translateY(${-timerFora * 40}px) scale(${1 + timerFora * 0.3})`, filter: `blur(${timerFora * 8}px)`}}>
          <Odometro seg={segundos(t)} sz={130} cor={caiu ? R : '#fff'} />
        </div>
      </div>
      <div style={{position: 'absolute', left: 70, right: 70, top: 720, opacity: 1 - tecladoK}}>
        {!caiu ? <Onda f={f} cor={t >= ESPERA ? M : L} altura={150} /> : null}
      </div>
      {/* teclado iOS na metade de baixo */}
      <div style={{position: 'absolute', left: 80, right: 80, top: 560, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 30, opacity: tecladoK, transform: `translateY(${(1 - tecladoK) * 60}px)`}}>
        {['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((n, i) => {
          const on = n === '1' && t >= 7.13 && t < 7.5;
          const brilho = n === '1' ? io(t, 7.13, 7.2, 0, 1) * io(t, 7.3, 7.9, 1, 0) : 0;
          return <div key={n} style={{height: 150, borderRadius: 75, background: on ? '#fff' : 'rgba(255,255,255,.13)', color: on ? N : '#fff', display: 'grid', placeItems: 'center', fontSize: 74, fontWeight: 300,
            boxShadow: `0 0 ${brilho * 90}px rgba(255,255,255,${brilho * 0.7})`, transform: `scale(${on ? 0.94 : 1}) translateY(${(1 - io(t, TEC0 + 0.2 + i * 0.03, TEC0 + 0.6 + i * 0.03, 0, 1)) * 40}px)`}}>{n}</div>;
        })}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 260, display: 'flex', justifyContent: 'center', gap: 46, opacity: (caiu ? 0.2 : 1) * (1 - tecladoK)}}>
        {['mudo', 'teclado', 'viva'].map((k) => <div key={k} style={{width: 124, height: 124, borderRadius: 62, background: k === 'teclado' && tecladoK > 0.5 ? '#fff' : 'rgba(255,255,255,.13)', color: k === 'teclado' && tecladoK > 0.5 ? N : '#fff', display: 'grid', placeItems: 'center'}}>{Ic[k]}</div>)}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 90, display: 'flex', justifyContent: 'center', opacity: caiu ? 0.2 : 1}}>
        <div style={{width: 130, height: 130, borderRadius: 65, background: R, display: 'grid', placeItems: 'center', color: '#fff'}}>{Ic.desliga}</div>
      </div>
    </div>
  );
};

const Celular: React.FC<{children: React.ReactNode; claro?: boolean}> = ({children, claro}) => (
  <div style={{width: 700, height: 1440, borderRadius: 118, padding: 20, position: 'relative',
    background: claro ? 'linear-gradient(150deg, #2B3B57, #0B1424 60%, #1D2B44)' : 'linear-gradient(150deg, #3A4A66, #0A1120 55%, #24324D)',
    boxShadow: '0 0 0 2px rgba(255,255,255,.08) inset, 0 120px 160px -60px rgba(0,0,0,.85), 0 40px 80px -30px rgba(45,127,240,.35)'}}>
    <div style={{position: 'absolute', inset: 20, borderRadius: 98, overflow: 'hidden', background: '#000'}}>
      {children}
      {/* reflexo de vidro */}
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,0) 32%, rgba(255,255,255,0) 70%, rgba(255,255,255,.05) 100%)', pointerEvents: 'none'}} />
      <div style={{position: 'absolute', top: 26, left: '50%', width: 190, height: 52, marginLeft: -95, borderRadius: 26, background: '#000'}} />
    </div>
  </div>
);

// legenda: faixa fixa embaixo, palavras subindo dentro de uma máscara, véu escuro por trás
const Legenda: React.FC<{t: number}> = ({t}) => {
  const l = linhas.find((x) => t >= x.pos - 0.08 && t < x.fim + 0.3);
  if (!l) return null;
  const pac = l.voz === 'paciente';
  const sai = io(t, l.fim + 0.12, l.fim + 0.3, 0, 1, Easing.in(Easing.cubic));
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top: 1450, height: 260, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: 'Poppins', zIndex: 40, opacity: 1 - sai, filter: `blur(${sai * 8}px)`}}>
      <div style={{fontSize: pac ? 92 : 62, fontWeight: pac ? 700 : 500, lineHeight: 1.16, letterSpacing: '-0.03em', color: '#fff'}}>
        {l.ws.map((w, i) => {
          const p = io(t, w.at - 0.06, w.at + 0.22, 0, 1);
          const dest = pac || DESTAQUE.includes(w.t);
          return (
            <span key={i} style={{display: 'inline-block', overflow: 'hidden', verticalAlign: 'bottom', marginRight: '0.24em', paddingBottom: 6}}>
              <span style={{display: 'inline-block', transform: `translateY(${(1 - p) * 110}%)`, color: dest ? L : '#fff', ...(dest && !pac ? {fontWeight: 600} : {})}}>{w.t}</span>
            </span>
          );
        })}
      </div>
    </div>
  );
};

const Grao: React.FC<{f: number}> = ({f}) => (
  <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, opacity: 0.09, mixBlendMode: 'overlay', pointerEvents: 'none'}}>
    <filter id={`g${f % 6}`}><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={f % 6} /><feColorMatrix type="saturate" values="0" /></filter>
    <rect width="100%" height="100%" filter={`url(#g${f % 6})`} />
  </svg>
);

// ---------- cena principal (dentro do desfoque de movimento) ----------
const Cena: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const c = cam(t);
  // queda do celular
  const q = Math.max(0, t - CAI);
  const quedaY = q > 0 ? 260 * q + 2600 * q * q : 0;
  const quedaR = q > 0 ? 40 * q * q * 10 : 0;
  const someCel = t >= CAI + 0.9;
  // cronômetro grande na frente (espera)
  const big = io(t, ESPERA + 0.2, ESPERA + 1.2, 0, 1);
  const bigVermelho = t >= CAI;
  const dof = big * 7; // celular desfoca quando o cronômetro vem pra frente
  const sec = segundos(t);
  const tag = sec >= 240 ? 'quatro minutos depois' : sec >= 120 ? 'dois minutos depois' : sec >= 60 ? 'um minuto depois' : '';
  const tagAt = sec >= 240 ? 0 : 1;
  const somePalco = io(t, VIRA - 0.05, VIRA + 0.5, 1, 0, Easing.in(Easing.cubic));
  if (t >= VIRA + 0.6) return null;
  return (
    <AbsoluteFill style={{background: `radial-gradient(1400px 1100px at 50% 30%, ${bigVermelho ? '#3A1022' : '#13306A'}, ${bigVermelho ? '#14060C' : '#060D20'} 62%, #02050D)`, fontFamily: 'Poppins', overflow: 'hidden'}}>
      {/* luzes */}
      <div style={{position: 'absolute', left: -300 + Math.sin(t * 0.5) * 80, top: 200, width: 900, height: 900, borderRadius: '50%', background: bigVermelho ? 'rgba(250,95,109,.18)' : 'rgba(45,127,240,.22)', filter: 'blur(120px)'}} />
      <div style={{position: 'absolute', right: -280 + Math.cos(t * 0.4) * 60, top: 900, width: 800, height: 800, borderRadius: '50%', background: 'rgba(90,162,255,.14)', filter: 'blur(120px)'}} />

      {/* gancho POV */}
      {t < ATENDE + 0.6 ? (
        <div style={{position: 'absolute', left: 80, top: 250, color: '#fff', zIndex: 5, opacity: io(t, ATENDE, ATENDE + 0.5, 1, 0, Easing.in(Easing.cubic)), transform: `translateY(${io(t, ATENDE, ATENDE + 0.5, 0, -80, Easing.in(Easing.cubic))}px)`}}>
          {[['POV:', 0.0, 64, 600, L], ['você tenta', 0.12, 116, 700, '#fff'], ['marcar uma', 0.24, 116, 700, '#fff'], ['consulta.', 0.36, 132, 400, M]].map(([txt, at, sz, w, cor], i) => (
            <div key={i} style={{overflow: 'hidden', lineHeight: 1.02}}>
              <div style={{fontSize: sz as number, fontWeight: w as number, color: cor as string, letterSpacing: '-0.05em', transform: `translateY(${(1 - io(t, at as number, (at as number) + 0.5, 0, 1)) * 110}%)`, ...(i === 3 ? SER : {})}}>{txt}</div>
            </div>
          ))}
        </div>
      ) : null}

      {/* palco 3D do celular */}
      {!someCel ? (
        <AbsoluteFill style={{perspective: 2600, perspectiveOrigin: '50% 45%', opacity: somePalco}}>
          <div style={{position: 'absolute', left: 190, top: 210, width: 700, height: 1440,
            transform: `translate(${c.x}px, ${c.y + quedaY}px) scale(${c.s}) rotateX(${c.rx}deg) rotateY(${c.ry}deg) rotateZ(${c.rz + quedaR}deg)`, transformOrigin: '50% 50%', transformStyle: 'preserve-3d',
            filter: `blur(${dof}px)`, opacity: 1 - big * 0.45}}>
            <Celular><TelaChamada t={t} f={f} /></Celular>
          </div>
        </AbsoluteFill>
      ) : null}

      {/* cronômetro gigante na frente da câmera */}
      {t >= ESPERA + 0.2 ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center', zIndex: 10, opacity: somePalco,
          transform: `scale(${0.6 + big * 0.4 + (bigVermelho ? io(t, CAI, CAI + 0.5, 0.08, 0) : 0)})`, filter: `blur(${(1 - big) * 10}px)`}}>
          <div style={{fontSize: 40, fontWeight: 600, letterSpacing: '.24em', color: bigVermelho ? '#FFB3BA' : M, marginBottom: 16, opacity: big}}>{bigVermelho ? 'CHAMADA ENCERRADA' : 'EM ESPERA'}</div>
          <Odometro seg={sec} sz={300} cor={bigVermelho ? R : '#fff'} peso={600} />
          <div style={{height: 90, marginTop: 10, overflow: 'hidden'}}>
            {!bigVermelho && tag ? <div key={tag} style={{...SER, fontSize: 66, color: L}}>{tag}…</div> : null}
            {bigVermelho ? <div style={{fontSize: 60, color: '#fff', letterSpacing: '-0.02em', opacity: io(t, CAI + 0.5, CAI + 0.8, 0, 1)}}>de espera. <span style={{...SER, fontSize: 74, color: '#FFB3BA'}}>Pra nada.</span></div> : null}
          </div>
        </div>
      ) : null}

      {/* véu da legenda e legenda */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 1300, bottom: 0, background: 'linear-gradient(180deg, rgba(2,5,13,0), rgba(2,5,13,.88) 30%, rgba(2,5,13,.95))', zIndex: 30, opacity: t >= ATENDE - 0.2 ? 1 : 0}} />
      {t >= ATENDE ? <Legenda t={t} /> : null}
      {t >= CAI && t < CAI + 0.1 ? <AbsoluteFill style={{background: R, opacity: 0.45, zIndex: 50}} /> : null}
    </AbsoluteFill>
  );
};

// ---------- virada, site, assinatura ----------
const Virada: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (t < VIRA - 0.05) return null;
  const raio = io(t, VIRA - 0.05, VIRA + 0.55, 0, 1500, Easing.bezier(0.7, 0, 0.2, 1));
  const linha = (txt: string, at: number, sz: number, w: number, extra: React.CSSProperties = {}) => (
    <div style={{overflow: 'hidden', lineHeight: 1}}>
      <div style={{fontSize: sz, fontWeight: w, whiteSpace: 'nowrap', transform: `translateY(${(1 - io(t, at, at + 0.55, 0, 1)) * 115}%)`, ...extra}}>{txt}</div>
    </div>
  );
  // texto sai subindo quando o celular entra
  const sobe = io(t, SITE - 0.2, SITE + 0.5, 0, 1, eIO);
  // celular do site
  const d0 = 26.0, d1 = 29.2;
  const passo = t < d0 + 0.9 ? 0 : t < d0 + 1.8 ? 1 : t < d0 + 2.6 ? 2 : 3;
  const crono = interpolate(t, [d0, d1], [0, 8], clamp);
  const celK = io(t, SITE - 0.1, SITE + 0.9, 0, 1);
  const slots = ['09:00', '10:30', '14:30', '16:00'];
  const fimK = io(t, FIM - 0.05, FIM + 0.5, 0, 1500, Easing.bezier(0.7, 0, 0.2, 1));
  return (
    <AbsoluteFill style={{clipPath: `circle(${raio}px at 50% 52%)`, fontFamily: 'Poppins', background: `linear-gradient(180deg, #3D8CFF, ${A} 50%, #1A56C4)`, overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: -200, top: -100, width: 1000, height: 1000, borderRadius: '50%', background: 'rgba(255,255,255,.18)', filter: 'blur(140px)'}} />
      {/* "Seu paciente não tem 4 minutos." */}
      <div style={{position: 'absolute', left: 80, right: 80, top: 560 - sobe * 380, color: '#fff', letterSpacing: '-0.055em', opacity: 1 - sobe * 0.0}}>
        {linha('Seu paciente', 23.2, 112, 300)}
        {linha('não tem', 23.95, 112, 300)}
        {linha('4 minutos.', 24.35, 160, 700)}
      </div>
      {/* contador dos 8 segundos */}
      <div style={{position: 'absolute', left: 80, top: 700 - sobe * 120, color: '#fff', opacity: sobe}}>
        <div style={{fontSize: 46, fontWeight: 400, letterSpacing: '-0.02em', color: M}}>no site da Web Clinic</div>
        <Odometro seg={crono} sz={150} cor="#fff" peso={600} />
      </div>
      {/* celular com o site, entrando em 3D */}
      {t >= SITE - 0.1 ? (
        <AbsoluteFill style={{perspective: 2600}}>
          <div style={{position: 'absolute', left: 560, top: 640, width: 700, height: 1440, transformOrigin: '0% 0%',
            transform: `translate(${(1 - celK) * 500}px, ${(1 - celK) * 700}px) scale(${0.62 + celK * 0.02}) rotateY(${-22 + celK * 8}deg) rotateX(${8 - celK * 4}deg) rotateZ(${4 - celK * 2}deg)`}}>
            <Celular claro>
              <div style={{position: 'absolute', inset: 0, background: '#fff', padding: '120px 56px 0', color: N}}>
                <div style={{fontWeight: 700, fontSize: 44, letterSpacing: '-0.04em'}}>web<span style={{color: A}}>clinic</span></div>
                <div style={{fontSize: 74, letterSpacing: '-0.045em', margin: '46px 0 40px', lineHeight: 1.02}}><b>Agende</b><br /><span style={{fontWeight: 300}}>sua consulta</span></div>
                <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 22}}>
                  {slots.map((x) => {
                    const on = passo >= 1 && x === '14:30';
                    return <div key={x} style={{height: 130, borderRadius: 30, border: `3px solid ${on ? A : '#E2EAF4'}`, background: on ? A : '#fff', color: on ? '#fff' : N, display: 'grid', placeItems: 'center', fontSize: 48, fontWeight: 600}}>{x}</div>;
                  })}
                </div>
                <div style={{marginTop: 34, height: 138, borderRadius: 69, background: passo >= 2 ? N : A, color: '#fff', display: 'grid', placeItems: 'center', fontSize: 48, fontWeight: 600}}>{passo >= 2 ? 'Confirmando…' : 'Agendar'}</div>
                {passo >= 3 ? (
                  <div style={{position: 'absolute', inset: 0, background: '#fff', display: 'grid', placeItems: 'center', textAlign: 'center', opacity: io(t, d0 + 2.6, d0 + 2.85, 0, 1)}}>
                    <div>
                      <div style={{width: 260, height: 260, borderRadius: 130, background: A, margin: '0 auto', display: 'grid', placeItems: 'center', transform: `scale(${spring({frame: f - Math.round((d0 + 2.6) * FPS), fps: FPS, config: {damping: 10}})})`}}>
                        <svg width="140" height="140" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>
                      </div>
                      <div style={{fontSize: 76, fontWeight: 700, letterSpacing: '-0.04em', marginTop: 44}}>Consulta marcada</div>
                      <div style={{fontSize: 44, color: '#6B7A90', marginTop: 10}}>Amanhã · 14:30</div>
                    </div>
                  </div>
                ) : null}
              </div>
            </Celular>
          </div>
        </AbsoluteFill>
      ) : null}
      {/* assinatura: círculo branco abre por cima */}
      {t >= FIM - 0.05 ? (
        <AbsoluteFill style={{clipPath: `circle(${fimK}px at 50% 50%)`, background: '#fff'}}>
          <AbsoluteFill style={{background: `radial-gradient(1000px 800px at 50% 40%, #fff, ${G})`}} />
          <div style={{position: 'absolute', left: 120, right: 120, top: 600, transform: `scale(${1.08 - io(t, FIM, FIM + 0.9, 0, 0.08)})`}}>
            <svg width="100%" viewBox="26 86 190 100">
              <text x="120" y="124" textAnchor="middle" fontFamily="Poppins" fontWeight={700} fontSize={40} letterSpacing={-1.8}><tspan fill={N}>web</tspan><tspan fill={A}>clinic</tspan></text>
              <path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke={A} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - io(t, FIM + 0.3, FIM + 1.2, 0, 1, eIO)} />
            </svg>
          </div>
          <div style={{position: 'absolute', left: 0, right: 0, top: 1050, textAlign: 'center', color: N, overflow: 'hidden'}}>
            <div style={{fontSize: 60, letterSpacing: '-0.03em', transform: `translateY(${(1 - io(t, FIM + 0.6, FIM + 1.1, 0, 1)) * 120}%)`}}>Sites que viram <span style={{...SER, fontSize: 74, color: A}}>consulta marcada.</span></div>
          </div>
          <div style={{position: 'absolute', left: 0, right: 0, top: 1250, textAlign: 'center', opacity: io(t, FIM + 1.1, FIM + 1.4, 0, 1), transform: `translateY(${io(t, FIM + 1.1, FIM + 1.5, 30, 0)}px)`}}>
            <span style={{display: 'inline-block', background: A, color: '#fff', borderRadius: 999, padding: '30px 64px', fontSize: 58, fontWeight: 600, letterSpacing: '-0.02em', boxShadow: '0 30px 60px -20px rgba(45,127,240,.6)'}}>Manda <b>SITE</b> no direct</span>
          </div>
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

const Tudo: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: '#02050D'}}>
      <Cena />
      <Virada />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 62%, rgba(0,0,0,.32) 100%)', pointerEvents: 'none'}} />
      <Grao f={f} />
    </AbsoluteFill>
  );
};

export const Video: React.FC = () => (
  <AbsoluteFill>
    <CameraMotionBlur shutterAngle={180} samples={5}>
      <Tudo />
    </CameraMotionBlur>
    <Audio src={staticFile('trilha.mp3')} />
  </AbsoluteFill>
);
