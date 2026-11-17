import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

export const FPS = 24;
const s = (x: number) => Math.round(x * FPS);
// linha do tempo (s)
const A = 0, B = 5, C = 10, D = 14.1, E = 19.1, FIM = 22.8;
export const DURACAO = s(FIM);
const fora = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const FONT = `@font-face{font-family:Poppins;font-weight:500;src:url(${staticFile('fonts/poppins-500.woff2')})}@font-face{font-family:Poppins;font-weight:700;src:url(${staticFile('fonts/poppins-700.woff2')})}@font-face{font-family:Serif;font-style:italic;src:url(${staticFile('fonts/instrument-serif-italic.woff2')})}`;

const Plano: React.FC<{src: string; de?: number; zoom?: [number, number]}> = ({src, de = 0, zoom = [1, 1]}) => {
  const f = useCurrentFrame(), {durationInFrames: d} = useVideoConfig();
  const z = interpolate(f, [0, d], zoom);
  return <AbsoluteFill style={{transform: `scale(${z})`}}><OffthreadVideo src={staticFile(src)} startFrom={s(de)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} /></AbsoluteFill>;
};

// legenda de abertura
const Abertura: React.FC = () => {
  const f = useCurrentFrame();
  const op = interpolate(f, [s(0.3), s(0.7), s(3.6), s(4.1)], [0, 1, 1, 0], fora);
  const y = interpolate(f, [s(0.3), s(0.8)], [20, 0], {...fora, easing: Easing.out(Easing.cubic)});
  return (
    <><div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 520, opacity: op, background: 'linear-gradient(rgba(0,0,0,.85), rgba(0,0,0,0))'}} /><div style={{position: 'absolute', left: 70, right: 70, top: 170, opacity: op, transform: `translateY(${y}px)`, fontFamily: 'Poppins', color: '#fff', textShadow: '0 2px 18px rgba(0,0,0,.6)'}}>
      <div style={{fontSize: 26, fontWeight: 700, letterSpacing: '.28em'}}>ENTREVISTA DE EMPREGO</div>
      <div style={{fontSize: 54, fontWeight: 700, letterSpacing: '-.02em', lineHeight: 1.05, marginTop: 10}}>Vaga: editor-chefe <span style={{fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400}}>da Plágio</span></div>
    </div></>
  );
};

// insert do celular: contagem e notificação
const Celular: React.FC = () => {
  const f = useCurrentFrame(), {fps} = useVideoConfig();
  const t = f / fps;
  const vib = t > 3.0 && t < 3.5 ? Math.sin(t * 120) * 6 : 0;
  const n = spring({frame: f - s(3.0), fps, config: {damping: 14, stiffness: 160}});
  const luz = interpolate(t, [2.95, 3.1], [0.15, 1], fora);
  const conta = t < 0.85 ? '' : t < 1.75 ? '3' : t < 2.45 ? '2' : t < 3.0 ? '1' : '';
  return (
    <AbsoluteFill style={{background: '#120d0a'}}>
      <AbsoluteFill style={{filter: 'blur(26px) brightness(.45) grayscale(1)', transform: 'scale(1.15)'}}>
        <Img src={staticFile('fundo-celular.jpg')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <div style={{position: 'absolute', left: 190, top: 330, width: 700, height: 1420, borderRadius: 96, background: '#0b0b0d', boxShadow: '0 60px 120px rgba(0,0,0,.6), inset 0 0 0 6px #2a2a30', transform: `translateX(${vib}px) rotate(${-3 + vib * 0.2}deg)`}}>
        <div style={{position: 'absolute', inset: 22, borderRadius: 76, overflow: 'hidden', background: `radial-gradient(120% 80% at 50% 0%, rgba(160,160,160,${luz}), #050505 70%)`}}>
          <div style={{position: 'absolute', top: 40, left: '50%', width: 200, height: 56, marginLeft: -100, borderRadius: 40, background: '#000'}} />
          <div style={{position: 'absolute', top: 170, width: '100%', textAlign: 'center', fontFamily: 'Poppins', color: `rgba(255,255,255,${0.35 + luz * 0.6})`}}>
            <div style={{fontSize: 30, fontWeight: 500}}>terça-feira, 17 de novembro</div>
            <div style={{fontSize: 190, fontWeight: 500, letterSpacing: '-.03em', lineHeight: 1.05}}>21:47</div>
          </div>
          <div style={{position: 'absolute', left: 26, right: 26, top: 560, opacity: n, transform: `translateY(${(1 - n) * -80}px) scale(${0.9 + n * 0.1})`, background: 'rgba(245,245,247,.94)', borderRadius: 44, padding: '28px 30px', display: 'flex', gap: 22, alignItems: 'center', fontFamily: 'Poppins'}}>
            <div style={{width: 92, height: 92, borderRadius: 22, background: '#d11a1a', display: 'grid', placeItems: 'center', fontSize: 40, fontWeight: 700, color: '#fff', flex: 'none', letterSpacing: '-.04em'}}>p.z</div>
            <div style={{color: '#111'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 26, color: '#666'}}><b style={{color: '#111'}}>plagio.zip</b><span>agora</span></div>
              <div style={{fontSize: 31, fontWeight: 700, lineHeight: 1.2, marginTop: 4}}>publicou uma notícia nova</div>
              <div style={{fontSize: 27, lineHeight: 1.25, color: '#333'}}>Toque pra ver antes de todo mundo.</div>
            </div>
          </div>
        </div>
      </div>
      {conta && <div style={{position: 'absolute', width: '100%', top: 760, textAlign: 'center', fontFamily: 'Poppins', fontWeight: 700, fontSize: 300, color: '#fff', opacity: 0.9, textShadow: '0 10px 40px rgba(0,0,0,.6)'}}>{conta}</div>}
    </AbsoluteFill>
  );
};

// fecho: último quadro vira post da Plágio (moldura branca, P&B, gravata vermelha)
const Fecho: React.FC = () => {
  const f = useCurrentFrame(), {fps} = useVideoConfig();
  const k = spring({frame: f, fps, config: {damping: 18, stiffness: 120}});
  const pb = interpolate(f, [s(0.2), s(0.6)], [0, 1], fora);
  const txt = spring({frame: f - s(0.7), fps, config: {damping: 16}});
  // janela da foto na moldura do @plagio.zip (636x796 em 1080x1350), centralizada no 9:16
  const W = 1080 - (1080 - 636 * 1.1) * k, H = 1920 - (1920 - 796 * 1.1) * k;
  return (
    <AbsoluteFill style={{background: '#fff'}}>
      <div style={{position: 'absolute', left: (1080 - W) / 2, top: (1920 - H) / 2 - 170 * k, width: W, height: H, overflow: 'hidden'}}>
        <Img src={staticFile('fecho.jpg')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />
        <Img src={staticFile('fecho-pb.jpg')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', opacity: pb}} />
      </div>
      <div style={{position: 'absolute', width: '100%', top: 1440, textAlign: 'center', fontFamily: 'Poppins', color: '#111', opacity: txt, transform: `translateY(${(1 - txt) * 40}px)`}}>
        <div style={{fontSize: 84, fontWeight: 700, letterSpacing: '-.03em'}}>A gente sabe <span style={{fontFamily: 'Serif', fontStyle: 'italic', fontWeight: 400}}>antes.</span></div>
        <div style={{fontSize: 44, fontWeight: 500, marginTop: 18}}>@plagio.zip</div>
      </div>
    </AbsoluteFill>
  );
};

export const Filme: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <style>{FONT}</style>
    <Sequence from={s(A)} durationInFrames={s(B - A)}><Plano src="s1.mp4" /><Abertura /></Sequence>
    <Sequence from={s(B)} durationInFrames={s(C - B)}><Plano src="s2.mp4" /></Sequence>
    <Sequence from={s(C)} durationInFrames={s(D - C)}><Celular /></Sequence>
    <Sequence from={s(D)} durationInFrames={s(E - D)}><Plano src="s3.mp4" /></Sequence>
    <Sequence from={s(E)} durationInFrames={s(FIM - E)}><Fecho /></Sequence>
    {/* áudio */}
    <Sequence from={s(0.5)}><Audio src={staticFile('jazz.mp3')} volume={(f) => interpolate(f / FPS, [0, 14.8, 15, 21.8, 22.3], [0.35, 0.35, 0.8, 0.8, 0], fora)} /></Sequence>
    <Sequence from={s(0.5)} durationInFrames={s(3.7)}><Audio src={staticFile('rh.mp3')} /></Sequence>
    <Sequence from={s(5.4)} durationInFrames={s(3.6)}><Audio src={staticFile('gato.mp3')} /></Sequence>
    <Sequence from={s(8.9)} durationInFrames={s(2.1)}><Audio src={staticFile('rh.mp3')} startFrom={s(4.4)} /></Sequence>
    <Sequence from={s(C + 0.5)} durationInFrames={s(2.8)}><Audio src={staticFile('gato.mp3')} startFrom={s(4.35)} /></Sequence>
    <Sequence from={s(C + 3.0)}><Audio src={staticFile('notificacao.mp3')} /></Sequence>
    <Sequence from={s(D + 1.0)} durationInFrames={s(1.6)}><Audio src={staticFile('rh.mp3')} startFrom={s(7.6)} /></Sequence>
    <Sequence from={s(E)}><Audio src={staticFile('boom.mp3')} volume={0.6} /></Sequence>
  </AbsoluteFill>
);
