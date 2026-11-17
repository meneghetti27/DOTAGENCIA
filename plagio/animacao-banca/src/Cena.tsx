import React from 'react';
import SP from './sprites.json';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, Easing, Audio} from 'remotion';

export const FPS = 24;
export const DURACAO = 14 * FPS;

// posições medidas no cenário (ajustar por cena)
export const P = {telhadoX: 640, telhadoY: 588, chaoY: 1560, escala: 1};

const INK = '#141018';
const pass = (f: number) => Math.floor(f / 2) * 2; // tudo anda a 12 quadros/s, como desenho animado

// "boil": o traço treme a cada 2 quadros (3 desenhos que se alternam)
const Boil: React.FC<{id: string; f: number; forca?: number; children: React.ReactNode}> = ({id, f, forca = 2.2, children}) => {
  const k = Math.floor(f / 2) % 3;
  return (
    <g filter={`url(#${id}${k})`}>
      {children}
    </g>
  );
};
const Filtros: React.FC<{id: string; forca: number; freq: number}> = ({id, forca, freq}) => (
  <defs>
    {[0, 1, 2].map((k) => (
      <filter id={`${id}${k}`} key={k} x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency={freq} numOctaves={2} seed={k * 7 + 3} />
        <feDisplacementMap in="SourceGraphic" scale={forca} />
      </filter>
    ))}
  </defs>
);

// ---------- personagens gerados (recortes) ----------
type S = {w: number; h: number; cx: number; base: number; corpo?: number};
const sp = (n: string) => (SP as Record<string, S>)[n];

// ----- linha do tempo (s) -----
export const T = {entra: 1.0, sai: 9.4, orelha: 2.6, acorda: 3.0, curte: 3.8, para: 10.8, dorme: 11.5};
export const BATIDA = 2 * 0.418; // balanço a cada 2 tempos do beat (143,5 bpm), 1º tempo em 3,0 s
const fora = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const xCara = (t: number) => interpolate(t, [T.entra, T.sai], [-220, 1320], fora);

const Gato: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const fase = (((t - 3.0) / BATIDA) + 0.5 + 100) % 1;
  const noRitmo = t > T.curte && t < T.para;
  const bop = noRitmo ? (fase < 0.5 ? fase * 2 : (1 - fase) * 2) : 0;
  const nome = t < T.acorda ? 'gato-1' : t < T.curte ? 'gato-2' : t < T.para ? 'gato-3' : t < T.dorme ? 'gato-2' : 'gato-1';
  const s = sp(nome);
  const esc = 0.72;
  const resp = nome === 'gato-1' ? Math.sin(t * 2.2) * 0.02 : 0;
  const pulo = t > T.orelha && t < T.orelha + 0.25 ? Math.sin((t - T.orelha) / 0.25 * Math.PI) * 0.06 : 0;
  // olha pros lados quando a música acaba
  const olha = t > T.para && t < T.dorme ? Math.sin((t - T.para) * 9) * 4 : 0;
  const sy = 1 + resp + pulo + bop * 0.05, sx = 1 - bop * 0.025;
  return (
    <g transform={`translate(${P.telhadoX},${P.telhadoY}) scale(${esc}) rotate(${bop * 4 - 2 * (noRitmo ? 1 : 0) + olha}) scale(${sx},${sy})`}>
      <image href={staticFile(nome + '.png')} x={-s.cx} y={-(s.corpo as number)} width={s.w} height={s.h} />
    </g>
  );
};

const CICLO = ['trap-1', 'trap-2', 'trap-3', 'trap-4'];
const ESC_CARA = 1.3;
const Passante: React.FC<{f: number}> = ({f}) => {
  const quadro = Math.floor(f / 4); // 6 desenhos por segundo
  const t = (quadro * 4) / FPS;
  const nome = CICLO[quadro % 4];
  const s = sp(nome);
  return (
    <g transform={`translate(${xCara(t)},${P.chaoY}) scale(${ESC_CARA})`}>
      <ellipse cx={0} cy={0} rx={110} ry={16} fill="#000" opacity={0.22} />
      <image href={staticFile(nome + '.png')} x={-s.cx} y={-s.base} width={s.w} height={s.h} />
    </g>
  );
};

// fumaça saindo do baseado
const Fumaca: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const xb = xCara(Math.floor(f / 4) * 4 / FPS) + 82 * ESC_CARA, yb = P.chaoY - 520 * ESC_CARA;
  if (t < T.entra || t > T.sai + 0.5) return null;
  return (
    <g>
      {[0, 1, 2, 3, 4, 5].map((i) => {
        const v = ((t * 0.55 + i / 6) % 1);
        const x = xb - v * 180 + Math.sin(v * 7 + i) * 22; // fica pra trás porque ele anda
        const y = yb - v * 210;
        const r = 7 + v * 24;
        return <circle key={i} cx={x} cy={y} r={r} fill="#D9D3EA" stroke="#3a3346" strokeWidth={2.5} opacity={0.55 * Math.sin(v * Math.PI)} />;
      })}
    </g>
  );
};

// notas musicais saindo do fone
const Notas: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  return (
    <g>
      {Array.from({length: 11}).map((_, i) => {
        const nasce = T.entra + 0.3 + i * 0.75;
        const v = t - nasce;
        if (v < 0 || v > 1.6 || nasce > T.sai - 0.8) return null;
        const x0 = xCara(nasce);
        const xn = x0 - 20 - v * 110 + Math.sin(v * 6 + i) * 18;
        const yn = P.chaoY - 560 * ESC_CARA + 40 - v * 240;
        const op = interpolate(v, [0, 0.2, 1.2, 1.6], [0, 1, 1, 0]);
        return (
          <g key={i} transform={`translate(${xn},${yn}) rotate(${Math.sin(v * 5) * 12}) scale(${1 + v * 0.3})`} opacity={op}>
            <ellipse cx={0} cy={30} rx={18} ry={13} fill="#F5D43A" stroke={INK} strokeWidth={5} transform="rotate(-20 0 30)" />
            <path d="M16 26 L 16 -30 Q 34 -20 40 -2" fill="none" stroke={INK} strokeWidth={6} strokeLinecap="round" />
          </g>
        );
      })}
    </g>
  );
};

const Zzz: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const dorme = t < T.acorda - 0.05 || t > T.dorme + 0.3;
  return (
    <g>
      {[0, 1, 2].map((i) => {
        const tt = (t * 0.7 + i * 0.33) % 1;
        return (
          <text key={i} x={520 - tt * 60} y={420 - tt * 150} fontFamily="Arial Black, Arial" fontWeight={900}
            fontSize={34 + tt * 26} fill="#EDE7FF" stroke={INK} strokeWidth={5} paintOrder="stroke" opacity={dorme ? Math.sin(tt * Math.PI) : 0}>z</text>
        );
      })}
    </g>
  );
};

export const Cena: React.FC = () => {
  const f = useCurrentFrame();
  const k = Math.floor(f / 2) % 3;
  return (
    <AbsoluteFill style={{background: '#9aa0d8'}}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920">
        <Filtros id="bg" forca={3} freq={0.012} />
        <Filtros id="ch" forca={4} freq={0.03} />
        <g filter={`url(#bg${k})`}>
          <image href={staticFile('cenario.png')} x={0} y={0} width={1080} height={1920} preserveAspectRatio="xMidYMid slice" />
        </g>
        <Boil id="ch" f={f}>
          <Gato f={f} />
          <Zzz f={f} />
        </Boil>
        <Boil id="ch" f={f}>
          <Passante f={f} />
          <Fumaca f={f} />
          <Notas f={f} />
        </Boil>
      </svg>
      <div style={{position: 'absolute', right: 40, bottom: 34, fontFamily: 'Arial', fontWeight: 900, color: INK, opacity: 0.55, fontSize: 30, letterSpacing: 2}}>plágio.zip</div>
    </AbsoluteFill>
  );
};
