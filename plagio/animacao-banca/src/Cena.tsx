import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, Easing, Audio} from 'remotion';

export const FPS = 24;
export const DURACAO = 5 * FPS;

// posições medidas no cenário (ajustar por cena)
export const P = {telhadoX: 640, telhadoY: 520, chaoY: 1500, escala: 0.95};

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

// ---------- o gato (preto, deitado em "pão") ----------
const Gato: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const resp = Math.sin(t * 2.2) * 0.018; // respiração
  const batida = 60 / 92; // ~92 bpm
  const noRitmo = interpolate(t, [2.4, 2.7], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fase = (t / batida) % 1;
  const bop = noRitmo * (fase < 0.5 ? fase * 2 : (1 - fase) * 2); // 0..1 triângulo na batida
  // orelha: tremidinha em 1.5s, depois no ritmo
  const tremida = t > 1.45 && t < 1.75 ? Math.sin(t * 60) * 10 : 0;
  const orelha = tremida + bop * 14;
  // olho: abre em 2.0s, fecha em 4.2s
  const abre = interpolate(t, [1.95, 2.1, 4.15, 4.35], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const rabo = Math.sin(t * 1.3) * 6 + bop * 22 - 6;
  return (
    <g transform={`translate(${P.telhadoX},${P.telhadoY}) scale(${P.escala})`}>
      {/* rabo pendurado pra fora do telhado */}
      <g transform={`translate(150,-20) rotate(${rabo})`}>
        <path d="M0 0 C 40 10, 60 60, 50 120 C 45 160, 20 175, 5 170" fill="none" stroke={INK} strokeWidth={26} strokeLinecap="round" />
      </g>
      {/* corpo */}
      <g transform={`scale(1,${1 + resp}) translate(0,${-resp * 120})`}>
        <path d="M-150 0 C -160 -90, -60 -130, 30 -125 C 120 -120, 175 -80, 170 -10 C 168 10, 140 18, 0 18 C -120 18, -148 12, -150 0 Z" fill="#1b1720" stroke={INK} strokeWidth={8} />
        {/* patinhas */}
        <ellipse cx={-95} cy={12} rx={34} ry={14} fill="#1b1720" stroke={INK} strokeWidth={7} />
        <ellipse cx={-30} cy={14} rx={30} ry={13} fill="#1b1720" stroke={INK} strokeWidth={7} />
      </g>
      {/* cabeça */}
      <g transform={`translate(-105,-85) rotate(${bop * 4})`}>
        {/* orelha de trás */}
        <path d="M30 -55 L 62 -112 L 78 -42 Z" fill="#1b1720" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
        {/* orelha da frente, que mexe */}
        <g transform={`translate(-30,-55) rotate(${-orelha})`}>
          <path d="M-20 5 L -38 -62 L 25 -12 Z" fill="#1b1720" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
          <path d="M-18 -4 L -30 -42 L 8 -12 Z" fill="#5a3a52" />
        </g>
        <ellipse cx={0} cy={0} rx={92} ry={74} fill="#1b1720" stroke={INK} strokeWidth={8} />
        {/* olho esquerdo: sempre fechado */}
        <path d="M-52 2 Q -36 14 -18 2" fill="none" stroke="#8b86a0" strokeWidth={6} strokeLinecap="round" />
        {/* olho direito: abre */}
        {abre < 0.15 ? (
          <path d="M18 2 Q 36 14 54 2" fill="none" stroke="#8b86a0" strokeWidth={6} strokeLinecap="round" />
        ) : (
          <g>
            <ellipse cx={36} cy={2} rx={20} ry={17 * abre} fill="#F5D43A" stroke={INK} strokeWidth={5} />
            <rect x={33} y={2 - 14 * abre} width={6} height={28 * abre} rx={3} fill={INK} />
            {/* pálpebra meio caída: cara de "hm" */}
            <path d={`M14 ${-17 * abre} L 58 ${-17 * abre} L 58 ${-4 * abre} Q 36 ${2 * abre} 14 ${-4 * abre} Z`} fill="#1b1720" />
            <path d={`M14 ${-4 * abre} Q 36 ${2 * abre} 58 ${-4 * abre}`} fill="none" stroke={INK} strokeWidth={5} />
          </g>
        )}
        {/* focinho e bigode */}
        <path d="M-6 26 L 6 26 L 0 33 Z" fill="#c98aa0" />
        <path d="M-20 36 L -80 30 M -20 42 L -78 48 M 20 36 L 80 30 M 20 42 L 78 48" stroke="#5c5770" strokeWidth={3} strokeLinecap="round" />
      </g>
      {/* Zzz enquanto dorme */}
      {[0, 1, 2].map((i) => {
        const tt = (t * 0.8 + i * 0.33) % 1;
        const vis = abre < 0.1 ? 1 : 0;
        return (
          <text key={i} x={-60 + tt * 70} y={-190 - tt * 120} fontFamily="Comic Neue, Arial Rounded MT Bold, Arial" fontWeight={900}
            fontSize={34 + tt * 26} fill="#EDE7FF" stroke={INK} strokeWidth={3} paintOrder="stroke" opacity={vis * Math.sin(tt * Math.PI)}>z</text>
        );
      })}
    </g>
  );
};

// ---------- o passante de fone ----------
const Passante: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const x = interpolate(t, [0.4, 4.6], [-260, 1340], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const passo = Math.sin(t * Math.PI * 2 * 1.53); // passo no ritmo
  const bob = Math.abs(passo) * -14;
  const cabeca = Math.sin(t * Math.PI * 2 * 1.53) * 5;
  const LARANJA = '#E58A2B', JEANS = '#3f4f8f', PELE = '#b07a52';
  return (
    <g transform={`translate(${x},${P.chaoY + bob})`}>
      {/* sombra */}
      <ellipse cx={0} cy={-bob + 4} rx={95} ry={16} fill="#000" opacity={0.18} />
      {/* perna de trás */}
      <g transform={`translate(-8,-260) rotate(${-passo * 24})`}>
        <path d="M-22 0 L 22 0 L 20 250 L -20 250 Z" fill="#33407a" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        <path d="M-26 240 L 52 240 Q 62 262 48 268 L -28 268 Z" fill="#e9e3d4" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
      </g>
      {/* braço de trás */}
      <g transform={`translate(-10,-520) rotate(${passo * 20})`}>
        <path d="M-20 0 L 20 0 L 16 190 L -16 190 Z" fill="#c4721f" stroke={INK} strokeWidth={7} />
        <circle cx={0} cy={198} r={20} fill={PELE} stroke={INK} strokeWidth={6} />
      </g>
      {/* tronco: moletom laranja */}
      <path d="M-80 -560 Q 0 -600 80 -560 L 70 -250 L -70 -250 Z" fill={LARANJA} stroke={INK} strokeWidth={8} strokeLinejoin="round" />
      <path d="M-40 -380 L 40 -380 L 36 -320 L -36 -320 Z" fill="none" stroke={INK} strokeWidth={5} />
      {/* perna da frente */}
      <g transform={`translate(8,-260) rotate(${passo * 24})`}>
        <path d="M-22 0 L 22 0 L 20 250 L -20 250 Z" fill={JEANS} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        <path d="M-26 240 L 52 240 Q 62 262 48 268 L -28 268 Z" fill="#fff8ea" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
      </g>
      {/* braço da frente */}
      <g transform={`translate(10,-520) rotate(${-passo * 20})`}>
        <path d="M-20 0 L 20 0 L 16 190 L -16 190 Z" fill={LARANJA} stroke={INK} strokeWidth={7} />
        <circle cx={0} cy={198} r={20} fill={PELE} stroke={INK} strokeWidth={6} />
      </g>
      {/* cabeça balançando no som */}
      <g transform={`translate(10,-620) rotate(${cabeca})`}>
        <rect x={-20} y={20} width={40} height={40} fill={PELE} stroke={INK} strokeWidth={6} />
        <ellipse cx={0} cy={-20} rx={62} ry={66} fill={PELE} stroke={INK} strokeWidth={8} />
        {/* boné pra trás */}
        <path d="M-64 -30 Q -60 -96 2 -98 Q 62 -96 64 -40 Z" fill="#2c7a4b" stroke={INK} strokeWidth={8} strokeLinejoin="round" />
        <path d="M-60 -40 L -112 -30 Q -110 -16 -62 -22 Z" fill="#2c7a4b" stroke={INK} strokeWidth={7} strokeLinejoin="round" />
        {/* olho fechado curtindo e sorriso */}
        <path d="M22 -14 Q 34 -6 46 -14" fill="none" stroke={INK} strokeWidth={6} strokeLinecap="round" />
        <path d="M30 22 Q 44 30 56 18" fill="none" stroke={INK} strokeWidth={6} strokeLinecap="round" />
        {/* fone */}
        <path d="M-50 -60 Q 0 -128 50 -60" fill="none" stroke={INK} strokeWidth={12} />
        <ellipse cx={-30} cy={-12} rx={20} ry={28} fill="#d33b3b" stroke={INK} strokeWidth={7} />
      </g>
    </g>
  );
};

// notas musicais saindo do fone
const Notas: React.FC<{f: number}> = ({f}) => {
  const t = pass(f) / FPS;
  const x0 = interpolate(t, [0.4, 4.6], [-260, 1340], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <g>
      {[0, 1, 2, 3, 4].map((i) => {
        const nasce = 0.5 + i * 0.75;
        const v = t - nasce;
        if (v < 0 || v > 1.6) return null;
        const xn = x0 - 40 - v * 120 + Math.sin(v * 6 + i) * 18;
        const yn = P.chaoY - 660 - v * 260;
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
