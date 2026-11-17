import React from 'react';
import SP from './sprites.json';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, Easing, Audio} from 'remotion';

export const FPS = 24;
export const DURACAO = 5 * FPS;

// posições medidas no cenário (ajustar por cena)
export const P = {telhadoX: 640, telhadoY: 590, chaoY: 1560, escala: 1};

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

const Gato: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const batida = 60 / 92;
  const fase = (t / batida) % 1;
  const noRitmo = t > 2.6 && t < 4.3;
  const bop = noRitmo ? (fase < 0.5 ? fase * 2 : (1 - fase) * 2) : 0;
  const nome = t < 2.0 ? 'gato-1' : t < 2.6 ? 'gato-2' : t < 4.3 ? 'gato-3' : t < 4.7 ? 'gato-2' : 'gato-1';
  const s = sp(nome);
  const esc = 0.98;
  const resp = nome === 'gato-1' ? Math.sin(t * 2.2) * 0.02 : 0;
  // orelhada em 1.5 s: pulinho rápido
  const pulo = t > 1.45 && t < 1.7 ? Math.sin((t - 1.45) / 0.25 * Math.PI) * 0.05 : 0;
  const sy = 1 + resp + pulo + bop * 0.04, sx = 1 - bop * 0.02;
  return (
    <g transform={`translate(${P.telhadoX},${P.telhadoY}) scale(${esc}) rotate(${bop * 3 - 1.5 * (noRitmo ? 1 : 0)}) scale(${sx},${sy})`}>
      <image href={staticFile(nome + '.png')} x={-s.cx} y={-(s.corpo as number)} width={s.w} height={s.h} />
    </g>
  );
};

const CICLO = ['cara-1', 'cara-2', 'cara-3', 'cara-4'];
export const PASSO_INI = 0.3, PASSO_FIM = 4.4;
const Passante: React.FC<{f: number}> = ({f}) => {
  const quadro = Math.floor(f / 4); // 6 desenhos por segundo
  const t = (quadro * 4) / FPS;
  const nome = CICLO[quadro % 4];
  const s = sp(nome);
  const esc = 1.3;
  const x = interpolate(t, [PASSO_INI, PASSO_FIM], [-230, 1310], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <g transform={`translate(${x},${P.chaoY}) scale(${esc})`}>
      <ellipse cx={0} cy={0} rx={110} ry={16} fill="#000" opacity={0.22} />
      <image href={staticFile(nome + '.png')} x={-s.cx} y={-s.base} width={s.w} height={s.h} />
    </g>
  );
};

// notas musicais saindo do fone
const Notas: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const x0 = interpolate(t, [PASSO_INI, PASSO_FIM], [-230, 1310], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <g>
      {[0, 1, 2, 3, 4].map((i) => {
        const nasce = 0.5 + i * 0.75;
        const v = t - nasce;
        if (v < 0 || v > 1.6) return null;
        const xn = x0 + 10 - v * 120 + Math.sin(v * 6 + i) * 18;
        const yn = P.chaoY - 600 - v * 260;
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
  const dorme = t < 1.95 || t > 4.75;
  return (
    <g>
      {[0, 1, 2].map((i) => {
        const tt = (t * 0.7 + i * 0.33) % 1;
        return (
          <text key={i} x={470 - tt * 60} y={370 - tt * 150} fontFamily="Arial Black, Arial" fontWeight={900}
            fontSize={38 + tt * 30} fill="#EDE7FF" stroke={INK} strokeWidth={5} paintOrder="stroke" opacity={dorme ? Math.sin(tt * Math.PI) : 0}>z</text>
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
          <Notas f={f} />
        </Boil>
      </svg>
      <div style={{position: 'absolute', right: 40, bottom: 34, fontFamily: 'Arial', fontWeight: 900, color: INK, opacity: 0.55, fontSize: 30, letterSpacing: 2}}>plágio.zip</div>
    </AbsoluteFill>
  );
};
