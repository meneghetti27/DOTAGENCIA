// Web Clinic, vídeo 3: "Aguarde na linha" v2 (Reels 1080x1920, 30 fps, ~33 s).
// v1 reprovada ("amador, escrita por cima, não prende"): 28 s da mesma tela parada, 7 s sem nada no começo,
// legenda pequena em itálico no meio da interface, UI em tamanho de celular, virada fraca.
// v2: gancho "POV" em 0 s, edição em planos (chamada → close no teclado → cronômetro gigante → tela vermelha →
// azul da marca → celular com o site → assinatura), empurrão de câmera em cada plano, legenda grande numa faixa
// fixa (nada fica por baixo), interface ampliada para a escala do vídeo.
import React from 'react';
import {AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, Easing, delayRender, continueRender, random, spring} from 'remotion';
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
const io = (t: number, a: number, b: number, x: number, y: number, e = Easing.out(Easing.cubic)) => interpolate(t, [a, b], [x, y], {...clamp, easing: e});
const SER: React.CSSProperties = {fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400};
type W = {texto: string; inicio: number; fim: number};
const F = FALAS as Record<string, W[]>;

// trechos de fala na trilha: [voz, início no arquivo, fim no arquivo, posição no vídeo]
const TRECHOS: [string, number, number, number][] = [
  ['ura', 0.0, 2.74, 1.8], ['ura', 6.8, 9.19, 4.7], ['ura', 11.0, 15.67, 7.5], ['ura', 3.25, 5.79, 12.6],
  ['paciente', 2.0, 3.2, 15.3], ['ura', 16.5, 19.28, 16.8], ['paciente', 3.6, 6.26, 20.4],
];
const TROCA: Record<string, string> = {'clínica': 'Clínica', 'bem': 'Bem', '-estar.': 'Estar.', '1.': 'um.'};
const DESTAQUE = ['importante', 'ocupados.', 'aguarde', 'Sério?', 'Caiu?', 'tecle'];
const linhas = TRECHOS.map(([voz, a, b, pos]) => ({voz, pos, fim: pos + (b - a),
  ws: F[voz].filter((w) => w.inicio >= a - 0.05 && w.inicio < b).map((w) => ({t: TROCA[w.texto] ?? w.texto, at: pos + (w.inicio - a)}))}));

// marcos
const ATENDE = 1.8, TECLADO = [4.6, 7.45], ESPERA = 12.2, CAI = 19.8, VIRA = 23.0, SITE = 25.7, FIM = 29.9;
const segundos = (t: number) => (t < ATENDE ? 0 : t < ESPERA ? t - ATENDE : t < CAI ? interpolate(t, [ESPERA, CAI - 0.3], [ESPERA - ATENDE, 277], {...clamp, easing: Easing.in(Easing.quad)}) : 277);
const mmss = (x: number) => `${String(Math.floor(x / 60)).padStart(2, '0')}:${String(Math.floor(x % 60)).padStart(2, '0')}`;

// ---------- peças ----------
// cada plano entra com um "soco" curto (1,06 → 1) e vai empurrando a câmera devagar
const Plano: React.FC<{t: number; de: number; ate: number; bg: string; zoom?: [number, number]; origem?: string; children: React.ReactNode}> = ({t, de, ate, bg, zoom = [1, 1.06], origem = '50% 40%', children}) => {
  if (t < de || t >= ate) return null;
  const soco = io(t, de, de + 0.18, 1.06, 1);
  const z = interpolate(t, [de, ate], zoom, clamp) * soco;
  return (
    <AbsoluteFill style={{background: bg, fontFamily: 'Poppins', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${z})`, transformOrigin: origem}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};
const Fundo = `radial-gradient(1300px 1000px at 50% 22%, #1A3C78, ${N} 55%, #040915 100%)`;

// legenda: faixa fixa em y 1360–1660, Poppins grande, palavra atual em azul claro
const Legenda: React.FC<{t: number}> = ({t}) => {
  const l = linhas.find((x) => t >= x.pos - 0.08 && t < x.fim + 0.35);
  if (!l) return null;
  const pac = l.voz === 'paciente';
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: 1360, height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', zIndex: 40, fontFamily: 'Poppins'}}>
      <div style={{fontSize: pac ? 96 : 66, fontWeight: pac ? 700 : 600, lineHeight: 1.12, letterSpacing: '-0.03em', color: '#fff', textShadow: '0 6px 30px rgba(0,0,0,.45)'}}>
        {l.ws.map((w, i) => {
          if (t < w.at - 0.06) return null;
          const k = spring({frame: Math.round((t - w.at + 0.06) * FPS), fps: FPS, config: {damping: 14, stiffness: 260}});
          const ativo = DESTAQUE.includes(w.t) || pac;
          return <span key={i} style={{display: 'inline-block', marginRight: '0.24em', transform: `translateY(${(1 - k) * 22}px) scale(${0.9 + k * 0.1})`, opacity: Math.min(1, k * 1.6), color: ativo ? (pac ? L : L) : '#fff'}}>{w.t}</span>;
        })}
      </div>
    </div>
  );
};

const Onda: React.FC<{f: number; cor: string; y: number; altura: number; n?: number}> = ({f, cor, y, altura, n = 30}) => {
  const env = (ENV as number[])[Math.min(f, (ENV as number[]).length - 1)] ?? 0;
  return (
    <div style={{position: 'absolute', left: 120, right: 120, top: y, height: altura, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
      {Array.from({length: n}, (_, i) => {
        const k = 0.25 + 0.75 * Math.abs(Math.sin(i * 1.7 + f * 0.35)) * (0.6 + 0.4 * random(`b${i}${Math.floor(f / 2)}`));
        return <div key={i} style={{width: 14, height: Math.max(10, altura * env * k), borderRadius: 7, background: cor, opacity: 0.4 + env * 0.6}} />;
      })}
    </div>
  );
};
const Cabecalho: React.FC<{t: number; status: string; corStatus?: string}> = ({t, status, corStatus = M}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 230, textAlign: 'center', color: '#fff'}}>
    <div style={{width: 260, height: 260, borderRadius: 130, margin: '0 auto', background: `linear-gradient(160deg, ${L}, ${A})`, display: 'grid', placeItems: 'center', fontSize: 104, fontWeight: 600, letterSpacing: '-0.04em',
      boxShadow: '0 30px 80px -20px rgba(45,127,240,.7)'}}>BE</div>
    <div style={{fontSize: 80, fontWeight: 600, letterSpacing: '-0.035em', marginTop: 40}}>Clínica Bem Estar</div>
    <div style={{fontSize: 44, color: corStatus, marginTop: 6}}>{status}</div>
  </div>
);

export const Video: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const sec = segundos(t);
  return (
    <AbsoluteFill style={{background: N}}>
      {/* 0. GANCHO: POV + discagem */}
      <Plano t={t} de={0} ate={ATENDE} bg={Fundo} zoom={[1, 1.08]}>
        <div style={{position: 'absolute', left: 80, right: 80, top: 330, color: '#fff'}}>
          <div style={{fontSize: 70, fontWeight: 700, color: L, letterSpacing: '-0.03em'}}>POV:</div>
          <div style={{fontSize: 118, fontWeight: 700, letterSpacing: '-0.055em', lineHeight: 0.98, marginTop: 10}}>você tenta<br />marcar uma<br /><span style={{...SER, fontWeight: 400, fontSize: 130, color: M}}>consulta.</span></div>
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 1150, textAlign: 'center', color: '#fff'}}>
          <div style={{fontSize: 88, fontWeight: 300, letterSpacing: '-0.03em', fontVariantNumeric: 'tabular-nums'}}>{'(51) 3333-0147'.slice(0, Math.floor(io(t, 0.15, 1.0, 0, 14, Easing.linear)))}</div>
          <div style={{fontSize: 44, color: M, marginTop: 10, opacity: t > 0.9 ? 1 : 0}}>chamando…</div>
        </div>
      </Plano>

      {/* 1. a URA atende */}
      <Plano t={t} de={ATENDE} ate={TECLADO[0]} bg={Fundo}>
        <Cabecalho t={t} status="em ligação" />
        <div style={{position: 'absolute', left: 0, right: 0, top: 860, textAlign: 'center', color: '#fff', fontSize: 190, fontWeight: 300, letterSpacing: '-0.05em', fontVariantNumeric: 'tabular-nums'}}>{mmss(sec)}</div>
        <Onda f={f} cor={L} y={1130} altura={170} />
      </Plano>

      {/* 2. close no teclado: "tecle um" */}
      <Plano t={t} de={TECLADO[0]} ate={TECLADO[1]} bg={Fundo} zoom={[1, 1.1]} origem="50% 55%">
        <div style={{position: 'absolute', left: 120, right: 120, top: 250, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 42}}>
          {['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((n) => {
            const on = n === '1' && t >= 7.15 && t < 7.45;
            return <div key={n} style={{height: 250, borderRadius: 125, background: on ? '#fff' : 'rgba(255,255,255,.12)', color: on ? N : '#fff', display: 'grid', placeItems: 'center', fontSize: 120, fontWeight: 300,
              transform: `scale(${on ? 1.08 : 1})`, boxShadow: on ? '0 0 80px rgba(255,255,255,.5)' : 'none'}}>{n}</div>;
          })}
        </div>
      </Plano>

      {/* 3. "todos os atendentes estão ocupados" — volta à chamada, câmera indo pro cronômetro */}
      <Plano t={t} de={TECLADO[1]} ate={ESPERA} bg={Fundo} zoom={[1, 1.12]} origem="50% 50%">
        <Cabecalho t={t} status="em ligação" />
        <div style={{position: 'absolute', left: 0, right: 0, top: 860, textAlign: 'center', color: '#fff', fontSize: 190, fontWeight: 300, letterSpacing: '-0.05em', fontVariantNumeric: 'tabular-nums'}}>{mmss(sec)}</div>
        <Onda f={f} cor={L} y={1130} altura={170} />
      </Plano>

      {/* 4. ESPERA: cronômetro gigante disparando */}
      <Plano t={t} de={ESPERA} ate={CAI} bg={`radial-gradient(1200px 1000px at 50% 40%, #1A3C78, ${N} 60%, #040915)`} zoom={[1, 1.05]}>
        {(() => {
          const tremor = (random(`tr${f}`) - 0.5) * 10 * io(t, ESPERA, CAI, 0, 1);
          const soco = t >= 15.3 && t < 16.4 ? io(t, 15.3, 15.6, 1.12, 1.06) : 1; // "Sério?"
          const tag = sec >= 240 ? '+4 min' : sec >= 120 ? '+2 min' : sec >= 60 ? '+1 min' : null;
          return (
            <>
              <div style={{position: 'absolute', left: 0, right: 0, top: 240, textAlign: 'center'}}>
                <span style={{display: 'inline-block', background: 'rgba(255,255,255,.12)', color: M, borderRadius: 999, padding: '18px 44px', fontSize: 46, fontWeight: 600, letterSpacing: '.12em'}}>EM ESPERA ♪</span>
              </div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 480, textAlign: 'center', color: '#fff', fontSize: 330, fontWeight: 600, letterSpacing: '-0.06em', fontVariantNumeric: 'tabular-nums',
                transform: `translateX(${tremor}px) scale(${soco})`, filter: `blur(${io(t, ESPERA + 2, CAI, 0, 1.4)}px)`}}>{mmss(sec)}</div>
              {tag ? <div key={tag} style={{position: 'absolute', right: 110, top: 880, background: R, color: '#fff', borderRadius: 18, padding: '14px 30px', fontSize: 64, fontWeight: 700, letterSpacing: '-0.02em',
                transform: 'rotate(-6deg)', boxShadow: '0 20px 40px -10px rgba(250,95,109,.6)'}}>{tag}</div> : null}
              <Onda f={f} cor={M} y={1130} altura={150} />
            </>
          );
        })()}
      </Plano>

      {/* 5. CAIU */}
      <Plano t={t} de={CAI} ate={VIRA} bg={`radial-gradient(1200px 1000px at 50% 40%, #3A1022, #12060C 70%)`} zoom={[1.04, 1]}>
        {(() => {
          const k = spring({frame: f - Math.round(CAI * FPS), fps: FPS, config: {damping: 9}});
          const glitch = t < CAI + 0.3 ? (random(`gl${f}`) - 0.5) * 70 : 0;
          return (
            <>
              <div style={{position: 'absolute', left: 0, right: 0, top: 300, textAlign: 'center', color: R, fontSize: 52, fontWeight: 600, letterSpacing: '.14em', transform: `translateX(${glitch}px)`}}>CHAMADA ENCERRADA</div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 430, textAlign: 'center', color: R, fontSize: 300, fontWeight: 700, letterSpacing: '-0.06em', transform: `translateX(${-glitch}px) scale(${1.3 - k * 0.3})`}}>04:37</div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 820, textAlign: 'center', color: '#fff', fontSize: 64, letterSpacing: '-0.02em', opacity: io(t, CAI + 0.4, CAI + 0.7, 0, 1)}}>
                de espera. <span style={{...SER, fontSize: 80, color: '#FFB3BA'}}>Pra nada.</span></div>
              {t < CAI + 0.12 ? <AbsoluteFill style={{background: R, opacity: 0.55}} /> : null}
            </>
          );
        })()}
      </Plano>

      {/* 6. VIRADA: azul da marca */}
      <Plano t={t} de={VIRA} ate={SITE} bg={A} zoom={[1, 1.06]}>
        <div style={{position: 'absolute', left: 80, right: 80, top: 520, color: '#fff', letterSpacing: '-0.055em', lineHeight: 0.98}}>
          {[['Seu paciente', 23.2, 110, 300], ['não tem', 24.0, 110, 300], ['4 minutos.', 24.35, 168, 700]].map(([txt, at, sz, w]) => (
            t >= (at as number) - 0.05 ? <div key={txt as string} style={{fontSize: sz as number, fontWeight: w as number, whiteSpace: 'nowrap', transform: `translateY(${io(t, (at as number) - 0.05, (at as number) + 0.15, 40, 0)}px)`, opacity: io(t, (at as number) - 0.05, (at as number) + 0.1, 0, 1)}}>{txt}</div> : null
          ))}
        </div>
      </Plano>

      {/* 7. o site marca em 8 segundos */}
      <Plano t={t} de={SITE} ate={FIM} bg={`linear-gradient(180deg, #fff, ${G} 55%, ${M})`} zoom={[1, 1.04]}>
        {(() => {
          const d0 = 26.0, d1 = 29.2;
          const passo = t < d0 + 0.9 ? 0 : t < d0 + 1.8 ? 1 : t < d0 + 2.6 ? 2 : 3;
          const crono = Math.min(8, Math.floor(interpolate(t, [d0, d1], [0, 8], clamp)));
          const slots = ['09:00', '10:30', '14:30', '16:00'];
          return (
            <>
              <div style={{position: 'absolute', left: 80, right: 80, top: 200, color: N, letterSpacing: '-0.05em', lineHeight: 1}}>
                <div style={{fontSize: 74, fontWeight: 300}}>No site da Web Clinic:</div>
                <div style={{fontSize: 150, fontWeight: 700, color: A, fontVariantNumeric: 'tabular-nums'}}>00:0{crono}</div>
              </div>
              <div style={{position: 'absolute', left: 170, top: 560 + io(t, SITE, SITE + 0.35, 800, 0), width: 740, height: 1240, borderRadius: 96, background: N, padding: 24, boxShadow: '0 60px 120px -30px rgba(11,31,58,.55)'}}>
                <div style={{width: '100%', height: '100%', borderRadius: 74, background: '#fff', overflow: 'hidden', position: 'relative', padding: '100px 54px 0', color: N}}>
                  <div style={{fontWeight: 700, fontSize: 40, letterSpacing: '-0.04em'}}>web<span style={{color: A}}>clinic</span></div>
                  <div style={{fontSize: 66, letterSpacing: '-0.04em', margin: '40px 0 34px', lineHeight: 1.04}}><b>Agende</b> <span style={{fontWeight: 300}}>sua consulta</span></div>
                  <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20}}>
                    {slots.map((x) => {
                      const on = passo >= 1 && x === '14:30';
                      return <div key={x} style={{height: 116, borderRadius: 26, border: `3px solid ${on ? A : '#E2EAF4'}`, background: on ? A : '#fff', color: on ? '#fff' : N, display: 'grid', placeItems: 'center', fontSize: 44, fontWeight: 600}}>{x}</div>;
                    })}
                  </div>
                  <div style={{marginTop: 30, height: 124, borderRadius: 62, background: passo >= 2 ? N : A, color: '#fff', display: 'grid', placeItems: 'center', fontSize: 44, fontWeight: 600}}>{passo >= 2 ? 'Confirmando…' : 'Agendar'}</div>
                  {passo >= 1 && passo < 3 ? <div style={{position: 'absolute', left: passo === 1 ? 250 : 420, top: passo === 1 ? 500 : 720, width: 110, height: 110, borderRadius: 55, background: 'rgba(45,127,240,.35)', border: '5px solid #fff'}} /> : null}
                  {passo >= 3 ? (
                    <div style={{position: 'absolute', inset: 0, background: '#fff', display: 'grid', placeItems: 'center', textAlign: 'center'}}>
                      <div>
                        <div style={{width: 240, height: 240, borderRadius: 120, background: A, margin: '0 auto', display: 'grid', placeItems: 'center', transform: `scale(${spring({frame: f - Math.round((d0 + 2.6) * FPS), fps: FPS, config: {damping: 8}})})`}}>
                          <svg width="130" height="130" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>
                        </div>
                        <div style={{fontSize: 68, fontWeight: 700, letterSpacing: '-0.04em', marginTop: 40}}>Consulta marcada</div>
                        <div style={{fontSize: 40, color: '#6B7A90', marginTop: 10}}>Amanhã · 14:30</div>
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            </>
          );
        })()}
      </Plano>

      {/* 8. assinatura */}
      <Plano t={t} de={FIM} ate={99} bg={A} zoom={[1, 1.04]}>
        {(() => {
          const k = spring({frame: f - Math.round(FIM * FPS), fps: FPS, config: {damping: 10}});
          const p = io(t, FIM + 0.3, FIM + 1.1, 0, 1, Easing.inOut(Easing.cubic));
          const tremor = t < FIM + 0.4 ? (random(`fx${f}`) - 0.5) * 30 * (1 - (t - FIM) / 0.4) : 0;
          return (
            <AbsoluteFill style={{transform: `translate(${tremor}px, ${tremor * 0.6}px)`, color: '#fff'}}>
              <AbsoluteFill style={{background: 'radial-gradient(900px 700px at 50% 40%, rgba(255,255,255,.22), rgba(255,255,255,0))'}} />
              <div style={{position: 'absolute', left: 110, right: 110, top: 560, transform: `scale(${1.25 - k * 0.25})`}}>
                <svg width="100%" viewBox="26 86 190 100">
                  <text x="120" y="124" textAnchor="middle" fontFamily="Poppins" fontWeight={700} fontSize={40} letterSpacing={-1.8}><tspan fill="#fff">web</tspan><tspan fill={M}>clinic</tspan></text>
                  <path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke="#fff" strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
                </svg>
              </div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 1030, textAlign: 'center', fontSize: 62, letterSpacing: '-0.03em', opacity: io(t, FIM + 0.5, FIM + 0.8, 0, 1)}}>Sites que viram <span style={{...SER, fontSize: 76}}>consulta marcada.</span></div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 1240, textAlign: 'center', opacity: io(t, FIM + 1.0, FIM + 1.3, 0, 1)}}>
                <span style={{display: 'inline-block', background: '#fff', color: N, borderRadius: 999, padding: '30px 60px', fontSize: 60, fontWeight: 600, letterSpacing: '-0.02em'}}>Manda <b>SITE</b> no direct</span>
              </div>
              {t < FIM + 0.08 ? <AbsoluteFill style={{background: '#fff', opacity: 0.8}} /> : null}
            </AbsoluteFill>
          );
        })()}
      </Plano>

      {/* legenda por cima de tudo, na faixa fixa (só nas partes da ligação) */}
      {t >= ATENDE && t < VIRA ? <Legenda t={t} /> : null}
      {/* grão leve */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 60%, rgba(0,0,0,.28) 100%)', pointerEvents: 'none'}} />
      <Audio src={staticFile('trilha.mp3')} />
    </AbsoluteFill>
  );
};
