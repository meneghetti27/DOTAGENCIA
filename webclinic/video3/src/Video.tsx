// Web Clinic, vídeo 3: "Aguarde na linha" (Reels 1080x1920, 30 fps).
// Comédia em áudio: a tela é uma ligação de verdade (escura), com cronômetro, onda da voz e legenda grande.
// URA (Fernanda, filtro de telefone), paciente (Gabriel), música de espera (ElevenLabs Music), narrador (Moutella).
// A trilha inteira é montada no ffmpeg (public/trilha.mp3); envelope.json = volume por quadro para a onda.
import React from 'react';
import {AbsoluteFill, Audio, Img, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender, random, spring} from 'remotion';
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
export const DURACAO = Math.round(43.6 * FPS);
const s = (t: number) => Math.round(t * FPS);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const io = (f: number, a: number, b: number, x: number, y: number, e = Easing.out(Easing.cubic)) => interpolate(f, [a, b], [x, y], {...clamp, easing: e});
const SER: React.CSSProperties = {fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400};
type W = {texto: string; inicio: number; fim: number};
const F = FALAS as Record<string, W[]>;

// trechos de fala na ordem da trilha: [voz, início no arquivo, fim no arquivo, posição no vídeo]
const TRECHOS: [string, number, number, number][] = [
  ['paciente', 0.0, 0.9, 0.3], ['ura', 0.0, 5.79, 7.3], ['ura', 6.8, 9.19, 13.4], ['ura', 9.95, 15.67, 16.3],
  ['paciente', 2.0, 3.2, 23.4], ['ura', 16.5, 19.28, 25.0], ['paciente', 3.6, 6.26, 29.4],
  ['narrador', 0.0, 2.48, 32.6], ['narrador', 2.85, 6.68, 35.4], ['narrador', 7.3, 9.86, 39.6],
];
const TROCA: Record<string, string> = {'clínica': 'Clínica', 'bem': 'Bem', '-estar.': 'Estar.', '1.': 'um.', '4': 'quatro', '8': 'oito', 'WebClinic,': 'Web Clinic,', 'a': 'a', 'Direct.': 'direct.'};
const linhas = TRECHOS.map(([voz, a, b, pos]) => ({voz, pos, fim: pos + (b - a),
  ws: F[voz].filter((w) => w.inicio >= a - 0.05 && w.inicio < b).map((w) => ({t: w.texto, at: pos + (w.inicio - a)}))}));

// cronômetro da ligação: conta normal; na espera acelera de 00:14 até 04:37
const atendeu = 7.3, espera = 21.8, caiu = 28.6;
const segundosLigacao = (t: number) => {
  if (t < atendeu) return 0;
  if (t < espera) return t - atendeu;
  if (t < caiu) return interpolate(t, [espera, caiu - 0.4], [espera - atendeu, 277], {...clamp, easing: Easing.in(Easing.quad)});
  return 277;
};
const mmss = (x: number) => `${String(Math.floor(x / 60)).padStart(2, '0')}:${String(Math.floor(x % 60)).padStart(2, '0')}`;

const Onda: React.FC<{f: number; cor: string; y: number; altura: number}> = ({f, cor, y, altura}) => {
  const env = (ENV as number[])[Math.min(f, (ENV as number[]).length - 1)] ?? 0;
  return (
    <div style={{position: 'absolute', left: 90, right: 90, top: y, height: altura, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
      {Array.from({length: 36}, (_, i) => {
        const k = 0.25 + 0.75 * Math.abs(Math.sin(i * 1.7 + f * 0.35)) * (0.6 + 0.4 * random(`b${i}${Math.floor(f / 2)}`));
        const h = Math.max(8, altura * env * k);
        return <div key={i} style={{width: 12, height: h, borderRadius: 6, background: cor, opacity: 0.35 + env * 0.65}} />;
      })}
    </div>
  );
};

const Legenda: React.FC<{t: number; y: number; claro?: boolean}> = ({t, y, claro}) => {
  const l = linhas.find((x) => t >= x.pos - 0.1 && t < x.fim + 0.6);
  if (!l || l.voz === 'narrador') return null;
  const ura = l.voz === 'ura';
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top: y, textAlign: 'center', color: ura ? '#fff' : L, fontSize: ura ? 62 : 76, lineHeight: 1.15, letterSpacing: '-0.02em', fontWeight: ura ? 400 : 700, ...(ura ? SER : {})}}>
      {l.ws.map((w, i) => {
        const o = interpolate(t, [w.at - 0.05, w.at + 0.12], [0, 1], clamp);
        const txt = `${ura && i === 0 ? '“' : ''}${TROCA[w.t] ?? w.t}${ura && i === l.ws.length - 1 ? '”' : ''}`;
        return <span key={i} style={{opacity: o, display: 'inline-block', marginRight: '0.25em', transform: `translateY(${(1 - o) * 14}px)`}}>{txt}</span>;
      })}
    </div>
  );
};

const Botao: React.FC<{cor: string; children: React.ReactNode; on?: boolean}> = ({cor, children, on}) => (
  <div style={{width: 150, height: 150, borderRadius: 75, background: on ? '#fff' : cor, display: 'grid', placeItems: 'center', color: on ? N : '#fff'}}>{children}</div>
);
const I = {
  mudo: <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><rect x="9" y="3" width="6" height="11" rx="3" /><path d="M5 11a7 7 0 0 0 14 0M12 18v3" /></svg>,
  teclado: <svg width="60" height="60" viewBox="0 0 24 24" fill="currentColor">{[0, 1, 2].flatMap((r) => [0, 1, 2].map((c) => <circle key={`${r}${c}`} cx={6 + c * 6} cy={5 + r * 6} r="1.9" />))}<circle cx="12" cy="23" r="1.9" /></svg>,
  viva: <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><path d="M4 9v6h4l5 4V5L8 9H4z" /><path d="M16 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12" /></svg>,
  desliga: <svg width="70" height="70" viewBox="0 0 24 24" fill="currentColor"><path d="M2.5 13.5c5.3-4.6 13.7-4.6 19 0l-2.3 2.6c-.4.4-1 .5-1.5.2l-2.6-1.6c-.4-.3-.6-.8-.5-1.3l.3-1.6c-2-.7-4.8-.7-6.8 0l.3 1.6c.1.5-.1 1-.5 1.3l-2.6 1.6c-.5.3-1.1.2-1.5-.2z" /></svg>,
};

// ---------- parte 1: a ligação ----------
const Ligacao: React.FC<{f: number}> = ({f}) => {
  const t = f / FPS;
  const status = t < 2.9 ? 'discando…' : t < atendeu ? 'chamando…' : t < espera ? 'em ligação' : t < caiu ? 'em espera' : 'chamada encerrada';
  const caida = t >= caiu;
  const sec = segundosLigacao(t);
  const acelerando = t >= espera && t < caiu;
  const tremor = acelerando ? (random(`tr${f}`) - 0.5) * 6 * io(t, espera, caiu, 0, 1) : 0;
  const numero = '(51) 3333-0147';
  const digitos = Math.floor(io(t, 1.0, 2.8, 0, numero.length, Easing.linear));
  const teclado = t >= 13.4 && t < 16.6;
  const um = t >= 15.8 && t < 16.2;
  const glitch = t >= caiu && t < caiu + 0.25;
  return (
    <AbsoluteFill style={{background: `radial-gradient(1200px 900px at 50% 18%, #17346A, ${N} 55%, #050B1C 100%)`, fontFamily: 'Poppins', color: '#fff', transform: `translateX(${glitch ? (random(`g${f}`) - 0.5) * 60 : 0}px)`}}>
      {/* cabeçalho da chamada */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 230, textAlign: 'center'}}>
        <div style={{width: 210, height: 210, borderRadius: 105, margin: '0 auto', background: `linear-gradient(160deg, ${L}, ${A})`, display: 'grid', placeItems: 'center', fontSize: 84, fontWeight: 600, letterSpacing: '-0.04em',
          boxShadow: t >= 2.9 && t < atendeu ? `0 0 0 ${18 + Math.sin(f / 4) * 14}px rgba(90,162,255,.18)` : 'none'}}>BE</div>
        <div style={{fontSize: 64, fontWeight: 600, letterSpacing: '-0.03em', marginTop: 34}}>Clínica Bem Estar</div>
        <div style={{fontSize: 38, color: caida ? R : M, marginTop: 8, opacity: 0.9}}>{t < 2.9 ? numero.slice(0, digitos) || ' ' : status}</div>
        <div style={{fontSize: acelerando ? 170 : 150, fontWeight: 300, letterSpacing: '-0.05em', marginTop: 30, color: caida ? R : '#fff', fontVariantNumeric: 'tabular-nums',
          transform: `translateX(${tremor}px)`, filter: acelerando ? `blur(${io(t, espera, caiu, 0, 1.5)}px)` : 'none', opacity: t < atendeu ? 0.25 : 1}}>{mmss(sec)}</div>
        {acelerando && sec >= 60 ? <div style={{...SER, fontSize: 58, color: L, marginTop: 6}}>
          {sec < 120 ? 'um minuto depois…' : sec < 240 ? 'dois minutos depois…' : 'quatro minutos depois…'}</div> : null}
      </div>
      {/* onda */}
      {!caida && !teclado ? <Onda f={f} cor={t >= espera ? M : L} y={1010} altura={180} /> : null}
      {/* legenda */}
      <Legenda t={t} y={teclado ? 900 : 1230} />
      {/* carimbo de quando cai */}
      {caida ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 1010, textAlign: 'center', transform: `scale(${1.3 - spring({frame: f - s(caiu), fps: FPS, config: {damping: 9}}) * 0.3})`}}>
          <div style={{display: 'inline-block', border: `8px solid ${R}`, color: R, padding: '16px 36px', fontWeight: 700, fontSize: 64, letterSpacing: '.02em', transform: 'rotate(-6deg)', lineHeight: 1}}>4min37s<br /><span style={{fontSize: 40, fontWeight: 600}}>de espera. Pra nada.</span></div>
        </div>
      ) : null}
      {/* botões */}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 260, display: 'flex', justifyContent: 'center', gap: 56, opacity: caida ? 0.25 : 1}}>
        <Botao cor="rgba(255,255,255,.14)">{I.mudo}</Botao>
        <Botao cor="rgba(255,255,255,.14)" on={teclado}>{I.teclado}</Botao>
        <Botao cor="rgba(255,255,255,.14)">{I.viva}</Botao>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 70, display: 'flex', justifyContent: 'center', opacity: caida ? 0.25 : 1}}><Botao cor={R}>{I.desliga}</Botao></div>
      {/* teclado numérico no "tecle um" */}
      {teclado ? (
        <div style={{position: 'absolute', left: 190, right: 190, top: 1020, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 26, opacity: io(t, 13.4, 13.7, 0, 1) * io(t, 16.3, 16.6, 1, 0)}}>
          {['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((n) => (
            <div key={n} style={{height: 130, borderRadius: 65, background: n === '1' && um ? '#fff' : 'rgba(255,255,255,.14)', color: n === '1' && um ? N : '#fff', display: 'grid', placeItems: 'center', fontSize: 64, fontWeight: 300}}>{n}</div>
          ))}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ---------- parte 2: a virada (site marcando em 8 segundos) ----------
const Virada: React.FC<{f: number}> = ({f}) => {
  const t = f / FPS;
  const t0 = 32.3;
  const ent = io(t, t0, t0 + 0.35, 0, 1);
  const demo0 = 35.4, demo1 = 38.6;
  const crono = interpolate(t, [demo0, demo1], [0, 8], clamp);
  const passo = t < demo0 + 0.9 ? 0 : t < demo0 + 1.9 ? 1 : t < demo0 + 2.8 ? 2 : 3;
  const fala = (de: number, ate: number, txt: React.ReactNode, sz = 96) => (t >= de - 0.1 ? <div style={{opacity: io(t, de - 0.1, de + 0.15, 0, 1), transform: `translateY(${io(t, de - 0.1, de + 0.2, 30, 0)}px)`}}>{txt}</div> : null);
  const slots = ['09:00', '10:30', '14:30', '16:00'];
  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, #fff, ${G} 60%, ${M})`, fontFamily: 'Poppins', color: N, clipPath: `inset(${(1 - ent) * 100}% 0 0 0)`}}>
      <div style={{position: 'absolute', left: 80, right: 80, top: 210, letterSpacing: '-0.05em', lineHeight: 1.02}}>
        {t < 35.3 && fala(32.6, 35, <div style={{fontSize: 92, fontWeight: 300}}>Seu paciente não tem<br /><b style={{fontWeight: 700, color: A}}>4 minutos.</b></div>)}
      </div>
      {/* celular com o site */}
      {t >= 34.6 ? (
        <div style={{position: 'absolute', left: 230, top: 640 + io(t, 34.6, 35.2, 900, 0), width: 620, height: 1080, borderRadius: 80, background: N, padding: 20, boxShadow: '0 60px 120px -30px rgba(11,31,58,.55)'}}>
          <div style={{width: '100%', height: '100%', borderRadius: 62, background: '#fff', overflow: 'hidden', position: 'relative', padding: '90px 44px 0'}}>
            <div style={{fontWeight: 700, fontSize: 34, letterSpacing: '-0.04em'}}>web<span style={{color: A}}>clinic</span> <span style={{fontWeight: 400, fontSize: 22, color: '#8794A8', letterSpacing: 0}}>· clinicabemestar.com.br</span></div>
            <div style={{fontSize: 54, letterSpacing: '-0.04em', margin: '34px 0 26px', lineHeight: 1.05}}><b>Agende</b> <span style={{fontWeight: 300}}>sua consulta</span></div>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16}}>
              {slots.map((x) => {
                const on = passo >= 1 && x === '14:30';
                return <div key={x} style={{height: 96, borderRadius: 22, border: `3px solid ${on ? A : '#E2EAF4'}`, background: on ? A : '#fff', color: on ? '#fff' : N, display: 'grid', placeItems: 'center', fontSize: 36, fontWeight: 600}}>{x}</div>;
              })}
            </div>
            <div style={{marginTop: 26, height: 104, borderRadius: 52, background: passo >= 2 ? N : A, color: '#fff', display: 'grid', placeItems: 'center', fontSize: 36, fontWeight: 600, transform: `scale(${passo === 2 ? 0.96 : 1})`}}>
              {passo >= 2 ? 'Confirmando…' : 'Agendar'}</div>
            {passo >= 3 ? (
              <div style={{position: 'absolute', inset: 0, background: '#fff', display: 'grid', placeItems: 'center', textAlign: 'center', opacity: io(t, demo0 + 2.8, demo0 + 3.1, 0, 1)}}>
                <div>
                  <div style={{width: 200, height: 200, borderRadius: 100, background: A, margin: '0 auto', display: 'grid', placeItems: 'center', transform: `scale(${spring({frame: f - s(demo0 + 2.8), fps: FPS, config: {damping: 8}})})`}}>
                    <svg width="110" height="110" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>
                  </div>
                  <div style={{fontSize: 56, fontWeight: 700, letterSpacing: '-0.04em', marginTop: 36}}>Consulta marcada</div>
                  <div style={{fontSize: 34, color: '#6B7A90', marginTop: 8}}>Amanhã · 14:30</div>
                </div>
              </div>
            ) : null}
            {/* dedo tocando */}
            {passo >= 1 && passo < 3 ? <div style={{position: 'absolute', left: passo === 1 ? 130 : 230, top: passo === 1 ? 400 : 560, width: 90, height: 90, borderRadius: 45, background: 'rgba(45,127,240,.35)', border: '4px solid rgba(255,255,255,.9)'}} /> : null}
          </div>
        </div>
      ) : null}
      {/* cronômetro dos 8 segundos */}
      {t >= demo0 - 0.2 ? (
        <div style={{position: 'absolute', right: 60, top: 560, background: N, color: '#fff', borderRadius: 999, padding: '20px 36px', fontSize: 64, fontWeight: 600, fontVariantNumeric: 'tabular-nums', letterSpacing: '-0.02em',
          transform: `rotate(4deg) scale(${t >= demo1 ? 1.12 : 1})`, boxShadow: '0 20px 40px -14px rgba(11,31,58,.5)'}}>00:0{Math.min(8, Math.floor(crono))}</div>
      ) : null}
      <div style={{position: 'absolute', left: 80, right: 80, top: 210, letterSpacing: '-0.05em', lineHeight: 1.02, opacity: t >= 35.3 ? 1 : 0, background: 'linear-gradient(180deg,#fff 70%, rgba(255,255,255,0))', paddingBottom: 40}}>
        {fala(35.4, 39, <div style={{fontSize: 84, fontWeight: 300}}>No site da Web Clinic,<br />ele marca em <b style={{fontWeight: 700, color: A}}>8 segundos.</b></div>)}
      </div>
    </AbsoluteFill>
  );
};

// ---------- parte 3: assinatura ----------
const Fim: React.FC<{f: number}> = ({f}) => {
  const t = f / FPS;
  const t0 = 39.45;
  if (t < t0) return null;
  const k = spring({frame: f - s(t0), fps: FPS, config: {damping: 10}});
  const p = io(t, t0 + 0.3, t0 + 1.2, 0, 1, Easing.inOut(Easing.cubic));
  const tremor = t < t0 + 0.4 ? (random(`fx${f}`) - 0.5) * 30 * (1 - (t - t0) / 0.4) : 0;
  return (
    <AbsoluteFill style={{background: A, fontFamily: 'Poppins', color: '#fff', transform: `translate(${tremor}px, ${tremor * 0.6}px)`}}>
      <AbsoluteFill style={{background: 'radial-gradient(900px 700px at 50% 40%, rgba(255,255,255,.22), rgba(255,255,255,0))'}} />
      <div style={{position: 'absolute', left: 120, right: 120, top: 600, transform: `scale(${1.25 - k * 0.25})`}}>
        <svg width="100%" viewBox="26 86 190 100">
          <text x="120" y="124" textAnchor="middle" fontFamily="Poppins" fontWeight={700} fontSize={40} letterSpacing={-1.8}><tspan fill="#fff">web</tspan><tspan fill={M}>clinic</tspan></text>
          <path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke="#fff" strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
        </svg>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1040, textAlign: 'center', fontSize: 58, letterSpacing: '-0.03em', opacity: io(t, t0 + 0.6, t0 + 0.9, 0, 1)}}>Sites que viram <span style={{...SER, fontSize: 72}}>consulta marcada.</span></div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 1260, textAlign: 'center', opacity: io(t, t0 + 1.4, t0 + 1.7, 0, 1)}}>
        <span style={{display: 'inline-block', background: '#fff', color: N, borderRadius: 999, padding: '26px 52px', fontSize: 52, fontWeight: 600, letterSpacing: '-0.02em'}}>Manda <b>SITE</b> no direct</span>
      </div>
      {t < t0 + 0.08 ? <AbsoluteFill style={{background: '#fff', opacity: 0.8}} /> : null}
    </AbsoluteFill>
  );
};

export const Video: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  return (
    <AbsoluteFill style={{background: N}}>
      {t < 32.7 ? <Ligacao f={f} /> : null}
      {t >= 32.3 && t < 39.6 ? <Virada f={f} /> : null}
      <Fim f={f} />
      <Audio src={staticFile('trilha.mp3')} />
    </AbsoluteFill>
  );
};
