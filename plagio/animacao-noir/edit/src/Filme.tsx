import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

export const FPS = 24;
const s = (x: number) => Math.round(x * FPS);
// linha do tempo (s)
const A = 0, B = 5, C = 10, D = 11.4, E = 14.6, F = 19.6, FIM = 23.2;
export const DURACAO = s(FIM);
const fora = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const VERM = '#d42424';
const FONT = `@font-face{font-family:Poppins;font-weight:500;src:url(${staticFile('fonts/poppins-500.woff2')})}@font-face{font-family:Poppins;font-weight:700;src:url(${staticFile('fonts/poppins-700.woff2')})}@font-face{font-family:Serif;font-style:italic;src:url(${staticFile('fonts/instrument-serif-italic.woff2')})}`;

const Plano: React.FC<{src: string; som?: boolean; vol?: number; zoom?: [number, number]; origem?: string}> = ({src, som = false, vol = 1, zoom = [1, 1], origem = '50% 50%'}) => {
  const f = useCurrentFrame(), {durationInFrames: d} = useVideoConfig();
  const z = interpolate(f, [0, d], zoom, {easing: Easing.inOut(Easing.sin)});
  return <AbsoluteFill style={{transform: `scale(${z})`, transformOrigin: origem}}><OffthreadVideo src={staticFile(src)} muted={!som} volume={vol} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></AbsoluteFill>;
};

// passagem: persiana fecha (listras pretas crescem) e abre no plano seguinte
const Persiana: React.FC<{dur?: number}> = ({dur = 0.5}) => {
  const f = useCurrentFrame();
  const meio = s(dur / 2);
  const k = f < meio ? interpolate(f, [0, meio], [0, 1], {...fora, easing: Easing.in(Easing.cubic)}) : interpolate(f, [meio, s(dur)], [1, 0], {...fora, easing: Easing.out(Easing.cubic)});
  const N = 14, h = 1920 / N;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {Array.from({length: N}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: 0, right: 0, top: i * h, height: h * k + 1, background: '#0b0b0b', transformOrigin: 'top'}} />
      ))}
    </AbsoluteFill>
  );
};

// letreiro chapado (fala virando cartela de jazz)
const Cartela: React.FC<{l1: string; l2: string}> = ({l1, l2}) => {
  const f = useCurrentFrame(), {fps} = useVideoConfig();
  const a = spring({frame: f, fps, config: {damping: 13, stiffness: 180}});
  const b = spring({frame: f - 6, fps, config: {damping: 11, stiffness: 200}});
  return (
    <AbsoluteFill style={{background: '#0b0b0b', overflow: 'hidden'}}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        <polygon points="0,1180 1080,880 1080,1300 0,1560" fill="#1d1d1d" />
        <polygon points="-40,620 520,300 760,560 180,900" fill="#e9e6df" opacity={0.08} />
      </svg>
      <div style={{position: 'absolute', width: '100%', top: 700, textAlign: 'center', fontFamily: 'Poppins', fontWeight: 700, color: '#efece6', letterSpacing: '-.03em'}}>
        <div style={{fontSize: 120, transform: `translateY(${(1 - a) * 60}px) rotate(-3deg)`, opacity: a}}>{l1}</div>
        <div style={{display: 'inline-block', marginTop: 20, fontSize: 190, background: VERM, color: '#0b0b0b', padding: '0 34px', transform: `scale(${0.6 + b * 0.4}) rotate(2deg)`, opacity: b}}>{l2}</div>
      </div>
    </AbsoluteFill>
  );
};

// celular chapado: forma plana, mão preta, contagem e notificação
const Celular: React.FC = () => {
  const f = useCurrentFrame(), {fps} = useVideoConfig();
  const t = f / fps;
  const conta = t < 0.25 ? '' : t < 1.0 ? '3' : t < 1.75 ? '2' : t < 2.5 ? '1' : '';
  const vib = t > 2.5 && t < 2.9 ? Math.round(Math.sin(t * 90)) * 10 : 0;
  const n = spring({frame: f - s(2.5), fps, config: {damping: 13, stiffness: 170}});
  const zoom = interpolate(t, [0, 3.2], [1, 1.08]);
  const pulso = conta ? spring({frame: f - s(conta === '3' ? 0.25 : conta === '2' ? 1.0 : 1.75), fps, config: {damping: 10, stiffness: 220}}) : 0;
  return (
    <AbsoluteFill style={{background: '#efece6', overflow: 'hidden'}}>
      <svg width={1080} height={1920} style={{position: 'absolute'}}>
        {/* fundo em formas recortadas */}
        <polygon points="0,0 1080,0 1080,520 0,860" fill="#cfcac0" />
        <polygon points="760,0 1080,0 1080,1920 980,1920" fill="#0b0b0b" />
        {Array.from({length: 9}).map((_, i) => <rect key={i} x={0} y={1180 + i * 70} width={1080} height={26} fill="#0b0b0b" opacity={0.85} />)}
      </svg>
      <div style={{position: 'absolute', inset: 0, transform: `scale(${zoom}) translateX(${vib}px) rotate(-6deg)`}}>
        {/* aparelho chapado */}
        <div style={{position: 'absolute', left: 250, top: 300, width: 560, height: 1120, borderRadius: 70, background: '#0b0b0b'}}>
          <div style={{position: 'absolute', inset: 26, borderRadius: 50, background: n > 0.05 ? '#efece6' : '#1d1d1d', overflow: 'hidden'}}>
            {conta && <div style={{position: 'absolute', width: '100%', top: 300, textAlign: 'center', fontFamily: 'Poppins', fontWeight: 700, fontSize: 380, lineHeight: 1, color: VERM, transform: `scale(${0.5 + pulso * 0.5})`}}>{conta}</div>}
            <div style={{position: 'absolute', left: 26, right: 26, top: 330, transform: `translateY(${(1 - n) * -260}px)`, opacity: n}}>
              <div style={{background: '#0b0b0b', color: '#efece6', padding: '30px 28px', fontFamily: 'Poppins'}}>
                <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
                  <div style={{width: 74, height: 74, background: VERM, color: '#0b0b0b', fontWeight: 700, fontSize: 30, display: 'grid', placeItems: 'center'}}>p.z</div>
                  <div style={{fontSize: 30, fontWeight: 700}}>plagio.zip</div>
                </div>
                <div style={{fontSize: 44, fontWeight: 700, lineHeight: 1.08, marginTop: 20, letterSpacing: '-.02em'}}>publicou uma notícia nova</div>
                <div style={{fontSize: 28, marginTop: 10, color: '#bdb8ad'}}>antes de todo mundo.</div>
              </div>
            </div>
          </div>
        </div>
        {/* mão da RH (formas pretas) */}
        <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
          <polygon points="180,1500 330,1180 470,1150 520,1260 430,1330 420,1920 120,1920" fill="#0b0b0b" />
          <ellipse cx={330} cy={1240} rx={70} ry={46} fill="#0b0b0b" transform="rotate(-35 330 1240)" />
          <rect x={150} y={1560} width={300} height={22} fill={VERM} />
        </svg>
      </div>
    </AbsoluteFill>
  );
};

// carimbo "CONTRATADO" por cima do último plano
const Carimbo: React.FC = () => {
  const f = useCurrentFrame(), {fps} = useVideoConfig();
  const k = spring({frame: f, fps, config: {damping: 9, stiffness: 260}});
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: 1240, textAlign: 'center', transform: `scale(${2.2 - k * 1.2}) rotate(-9deg)`, opacity: Math.min(1, k * 1.5)}}>
      <span style={{display: 'inline-block', fontFamily: 'Poppins', fontWeight: 700, fontSize: 132, color: VERM, border: `12px solid ${VERM}`, padding: '6px 36px', letterSpacing: '.02em', background: 'rgba(239,236,230,.92)'}}>CONTRATADO.</span>
    </div>
  );
};

const Abertura: React.FC = () => {
  const f = useCurrentFrame();
  const op = interpolate(f, [s(0.3), s(0.7), s(3.4), s(3.9)], [0, 1, 1, 0], fora);
  return (
    <>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 520, opacity: op, background: 'linear-gradient(rgba(11,11,11,.9), rgba(11,11,11,0))'}} />
      <div style={{position: 'absolute', left: 70, right: 70, top: 170, opacity: op, fontFamily: 'Poppins', color: '#efece6'}}>
        <div style={{display: 'inline-block', fontSize: 24, fontWeight: 700, letterSpacing: '.28em', background: VERM, color: '#0b0b0b', padding: '6px 14px'}}>ENTREVISTA DE EMPREGO</div>
        <div style={{fontSize: 58, fontWeight: 700, letterSpacing: '-.02em', lineHeight: 1.05, marginTop: 14}}>Vaga: editor-chefe <span style={{fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400}}>da Plágio</span></div>
      </div>
    </>
  );
};

const Fecho: React.FC = () => {
  const f = useCurrentFrame(), {fps} = useVideoConfig();
  const k = spring({frame: f, fps, config: {damping: 18, stiffness: 120}});
  const txt = spring({frame: f - s(0.6), fps, config: {damping: 16}});
  const W = 1080 - (1080 - 636 * 1.1) * k, H = 1920 - (1920 - 796 * 1.1) * k;
  return (
    <AbsoluteFill style={{background: '#fff'}}>
      <div style={{position: 'absolute', left: (1080 - W) / 2, top: (1920 - H) / 2 - 170 * k, width: W, height: H, overflow: 'hidden'}}>
        <Img src={staticFile('fecho.jpg')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />
      </div>
      <div style={{position: 'absolute', width: '100%', top: 1440, textAlign: 'center', fontFamily: 'Poppins', color: '#111', opacity: txt, transform: `translateY(${(1 - txt) * 40}px)`}}>
        <div style={{fontSize: 84, fontWeight: 700, letterSpacing: '-.03em'}}>A gente sabe <span style={{fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400}}>antes.</span></div>
        <div style={{fontSize: 44, fontWeight: 500, marginTop: 18}}>@plagio.zip</div>
      </div>
    </AbsoluteFill>
  );
};

export const Filme: React.FC = () => (
  <AbsoluteFill style={{background: '#0b0b0b'}}>
    <style>{FONT}</style>
    <Sequence from={s(A)} durationInFrames={s(B - A)}><Plano src="k1.mp4" som zoom={[1.05, 1.55]} origem="78% 34%" /><Abertura /></Sequence>
    <Sequence from={s(B)} durationInFrames={s(C - B)}><Plano src="k2.mp4" som zoom={[1.15, 1.6]} origem="22% 40%" /></Sequence>
    <Sequence from={s(C)} durationInFrames={s(D - C)}><Cartela l1="Ah, é?" l2="PROVA." /></Sequence>
    <Sequence from={s(D)} durationInFrames={s(E - D)}><Celular /></Sequence>
    <Sequence from={s(E)} durationInFrames={s(F - E)}><Plano src="s3.mp4" zoom={[1, 1.08]} /></Sequence>
    <Sequence from={s(E + 1.0)} durationInFrames={s(F - E - 1.0)}><Carimbo /></Sequence>
    <Sequence from={s(F)} durationInFrames={s(FIM - F)}><Fecho /></Sequence>
    {/* passagens de persiana */}
    {[B, C, D, E, F].map((t) => <Sequence key={t} from={s(t - 0.25)} durationInFrames={s(0.5)}><Persiana /></Sequence>)}
    {[B, C, D, E].map((t) => <Sequence key={'w' + t} from={s(t - 0.25)}><Audio src={staticFile('desliza.mp3')} volume={0.35} /></Sequence>)}
    {/* áudio */}
    <Sequence from={s(0.2)}><Audio src={staticFile('jazz.mp3')} volume={(fr) => interpolate(fr / FPS, [0, 9.6, 10.2, 21.5, 22.6], [0.22, 0.22, 0.6, 0.6, 0], fora)} /></Sequence>
    <Sequence from={s(D + 0.25)}><Audio src={staticFile('relogio.mp3')} volume={0.7} /></Sequence>
    <Sequence from={s(D + 2.5)}><Audio src={staticFile('notificacao.mp3')} /></Sequence>
    <Sequence from={s(E + 1.0)}><Audio src={staticFile('carimbo.mp3')} /></Sequence>
    <Sequence from={s(F)}><Audio src={staticFile('boom.mp3')} volume={0.5} /></Sequence>
  </AbsoluteFill>
);
