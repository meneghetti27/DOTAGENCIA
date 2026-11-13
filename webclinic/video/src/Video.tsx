// Web Clinic: vídeo "sobre nós" para o post fixado (Reels 1080x1920, 30 fps).
// Narração ElevenLabs eleven_v4 (voz Moutella), um take só; tempo por palavra em audio.json.
// Sem música: só efeitos sonoros. Vetores e logo exportados do gerador Python (exportar.py).
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, Easing, delayRender, continueRender} from 'remotion';
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
const W = (i: number) => fr(P[i].inicio);           // quadro em que a palavra i começa
const FIM_VOZ = fr(P[P.length - 1].fim);
export const DURACAO = FIM_VOZ + fr(2.6);
const CUT = [0, W(8), W(13), W(19), W(29), W(42), W(49), W(53), W(57), W(65), W(76), DURACAO].map((x, k) => (k === 0 || k === 11 ? x : x - 4));

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const io = (f: number, a: number, b: number, x: number, y: number) => interpolate(f, [a, b], [x, y], {...clamp, easing: ease});
const sp = (f: number, at: number, damping = 13) => spring({frame: f - at, fps: FPS, config: {damping, mass: 0.7, stiffness: 140}});

// ---------- peças ----------
const Ico: React.FC<{n: string; s: number}> = ({n, s}) => (
  <svg width={s} height={s} viewBox="0 0 200 200" dangerouslySetInnerHTML={{__html: V[n]}} />
);
const SH = '0 40px 80px -18px rgba(45,127,240,.28), 0 10px 22px -8px rgba(11,31,58,.12)';
const Tile: React.FC<{n: string; s: number; x: number; y: number; rot?: number; k?: number; bg?: string}> = ({n, s, x, y, rot = 0, k = 1, bg = '#fff'}) => (
  <div style={{position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: s * 0.28, background: bg, border: '2px solid #E2EAF4',
    display: 'grid', placeItems: 'center', boxShadow: SH, transform: `translateY(${Math.sin((useCurrentFrame() + x) / 18) * 8}px) rotate(${rot}deg) scale(${k})`, opacity: Math.min(1, k * 1.5)}}>
    <Ico n={n} s={s * 0.64} />
  </div>
);
const Logo: React.FC<{s: number}> = ({s}) => <div style={{width: s, height: s}} dangerouslySetInnerHTML={{__html: LOGO}} />;
const Cursor: React.FC<{x: number; y: number; k?: number; press?: number}> = ({x, y, k = 2.3, press = 0}) => (
  <svg style={{position: 'absolute', left: x, top: y, zIndex: 20, filter: 'drop-shadow(0 10px 12px rgba(11,31,58,.25))', transform: `scale(${1 - press * 0.15})`, transformOrigin: '0 0'}}
    width={36 * k} height={50 * k} viewBox="-3 -3 33 46"><path d={CUR} fill={N} stroke="#fff" strokeWidth={2.5} strokeLinejoin="round" /></svg>
);
const Chip: React.FC<{icon: string; t: string; sub: string; x: number; y: number; k: number; rot?: number}> = ({icon, t, sub, x, y, k, rot = 0}) => (
  <div style={{position: 'absolute', left: x, top: y, display: 'flex', alignItems: 'center', gap: 20, background: '#fff', border: '2px solid #E2EAF4', borderRadius: 32,
    padding: '22px 32px', boxShadow: SH, transform: `rotate(${rot}deg) scale(${k})`, opacity: Math.min(1, k * 1.5), transformOrigin: 'left center', zIndex: 15}}>
    <div style={{width: 76, height: 76, borderRadius: 22, background: G, display: 'grid', placeItems: 'center'}}><Ico n={icon} s={50} /></div>
    <div style={{fontSize: 34, fontWeight: 600, color: N, lineHeight: 1.15}}>{t}<div style={{fontSize: 24, fontWeight: 400, color: C}}>{sub}</div></div>
  </div>
);
const Bar: React.FC<{url: string}> = ({url}) => (
  <div style={{height: 76, background: G, display: 'flex', alignItems: 'center', gap: 12, padding: '0 28px', borderBottom: '2px solid #E2EAF4'}}>
    {[0, 1, 2].map((i) => <i key={i} style={{width: 16, height: 16, borderRadius: 9, background: '#C9D6E6'}} />)}
    <div style={{marginLeft: 18, flex: 1, height: 44, borderRadius: 99, background: '#fff', border: '2px solid #E2EAF4', fontSize: 22, color: C, display: 'flex', alignItems: 'center', padding: '0 20px'}}>{url}</div>
  </div>
);
const Btn: React.FC<{t: string; sz?: number; on?: number}> = ({t, sz = 34, on = 0}) => (
  <span style={{display: 'inline-block', background: A, color: '#fff', fontWeight: 600, fontSize: sz, borderRadius: 99, padding: `${sz * 0.6}px ${sz * 1.3}px`,
    boxShadow: `0 0 0 ${on * 18}px rgba(45,127,240,${0.25 * (1 - on)})`}}>{t}</span>
);
const Linhas: React.FC<{w: number}> = ({w}) => (
  <>{[92, 74].map((p, i) => <div key={i} style={{height: 16, borderRadius: 9, background: G, width: `${p}%`, marginBottom: 14}} />)}</>
);
const Blob: React.FC<{x: number; y: number; w: number; h: number; c: string; o: number}> = ({x, y, w, h, c, o}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: '50%', background: c, opacity: o, filter: 'blur(80px)'}} />
);
const Pulse: React.FC<{y: number; p: number; c?: string; sw?: number}> = ({y, p, c = A, sw = 6}) => (
  <svg style={{position: 'absolute', left: -40, top: y}} width={1160} height={290} viewBox="0 0 400 100">
    <path d="M4 50H150L166 18L190 86L210 32L222 50H396" fill="none" stroke={c} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round"
      pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
  </svg>
);

// ---------- legenda cinética: cada palavra entra no tempo da narração ----------
type Linha = {de: number; ate: number; sz: number; peso?: 300 | 700; cor?: string};
const Fala: React.FC<{f: number; linhas: Linha[]; y: number; x?: number; align?: 'left' | 'center'; sair?: number}> = ({f, linhas, y, x = 80, align = 'left', sair}) => {
  const out = sair === undefined ? 1 : io(f, sair, sair + 6, 1, 0);
  return (
    <div style={{position: 'absolute', left: x, right: x, top: y, textAlign: align, letterSpacing: '-0.045em', lineHeight: 1.02, opacity: out,
      transform: `translateY(${(1 - out) * -30}px)`, zIndex: 12}}>
      {linhas.map((l, k) => (
        <div key={k} style={{fontSize: l.sz, fontWeight: l.peso ?? 300, color: l.cor ?? N}}>
          {Array.from({length: l.ate - l.de + 1}, (_, j) => l.de + j).map((i) => {
            const a = W(i) - 2;
            const o = io(f, a, a + 5, 0, 1);
            return (
              <span key={i} style={{display: 'inline-block', opacity: o, filter: `blur(${(1 - o) * 12}px)`, transform: `translateX(${(1 - o) * 50}px)`, marginRight: '0.24em'}}>
                {P[i].texto.replace('vinte', '24').replace(/^e$/, i === 46 ? '' : 'e').replace('quatro', '')}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
const Hdr: React.FC<{dark?: boolean}> = ({dark}) => (
  <div style={{position: 'absolute', top: 150, left: 80, display: 'flex', alignItems: 'center', gap: 16, zIndex: 30}}>
    <Logo s={64} /><div style={{fontSize: 28, fontWeight: 600, color: dark ? '#fff' : N}}>webclinic</div>
  </div>
);

// ---------- cena com corte: zoom 1,08 → 1 e desfoque 14 → 0 ----------
const Cena: React.FC<{k: number; bg: string; dark?: boolean; children: (f: number) => React.ReactNode}> = ({k, bg, dark, children}) => {
  const g = useCurrentFrame();
  const a = CUT[k], b = CUT[k + 1];
  if (g < a || g >= b) return null;
  const f = g - a;
  const z = io(f, 0, 7, 1.08, 1) * interpolate(f, [0, b - a], [1, 1.035]), bl = io(f, 0, 7, 14, 0);
  return (
    <AbsoluteFill style={{background: bg, fontFamily, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${z})`, filter: `blur(${bl}px)`}}>
        {children(g)}
        <Hdr dark={dark} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- cenas ----------
const Busca: React.FC<{f: number}> = ({f}) => {
  const q = 'dermatologista perto de mim';
  const n = Math.floor(io(f, fr(0.5), W(6), 0, q.length));
  const res = [['Clínica Pele & Cia', 'site antigo · sem agenda'], ['Dra. Ana Paula · Dermatologia', 'agende online · aberto agora'], ['Consultório Centro', 'só telefone']];
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top: 780}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 22, background: '#fff', border: '2px solid #E2EAF4', borderRadius: 99, padding: '30px 40px', boxShadow: SH, fontSize: 38, color: N}}>
        <Ico n="zoom" s={64} /><span>{q.slice(0, n)}<span style={{display: 'inline-block', width: 3, height: 44, background: A, marginLeft: 4, verticalAlign: 'middle', opacity: f % 20 < 10 ? 1 : 0}} /></span>
      </div>
      {res.map(([t, s], i) => {
        const k = sp(f, W(7) + i * 4);
        return (
          <div key={i} style={{marginTop: 26, background: '#fff', border: '2px solid #E2EAF4', borderRadius: 30, padding: '28px 36px', opacity: k, transform: `translateY(${(1 - k) * 60}px)`, boxShadow: SH}}>
            <div style={{fontSize: 22, color: C}}>www.{['clinicapele', 'draanapaula', 'consultoriocentro'][i]}.com.br</div>
            <div style={{fontSize: 36, fontWeight: 600, color: i === 1 ? A : N, marginTop: 4}}>{t}</div>
            <div style={{fontSize: 24, color: C, marginTop: 2}}>{s}</div>
          </div>
        );
      })}
    </div>
  );
};

export const Video: React.FC = () => {
  const SFX: [string, number, number][] = [
    ['whoosh', 0, 0.3], ...CUT.slice(1, -1).map((c) => ['whoosh', c - 3, 0.32] as [string, number, number]),
    ['pop', W(7), 0.35], ['pop', W(7) + 4, 0.3], ['pop', W(7) + 8, 0.3],
    ['impacto', W(14), 0.55], ['ding', W(41) + 2, 0.45], ['tique', W(41) - 1, 0.6],
    ...[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => ['pop', W(21) + i * 5, 0.22] as [string, number, number]),
    ['pop', W(52), 0.4], ['tique', W(56), 0.6], ['pop', W(56) + 6, 0.35],
    ['ding', W(72), 0.35], ['ding', W(74), 0.3], ['ding', W(75) + 4, 0.3],
    ['impacto', W(76), 0.5], ['tique', W(79) + 6, 0.5], ['pop', FIM_VOZ + 6, 0.35],
  ];
  return (
    <AbsoluteFill style={{background: G, fontFamily}}>
      <Audio src={staticFile('voz.mp3')} />
      {SFX.map(([s, at, v], i) => (
        <Sequence key={i} from={Math.max(0, at)}><Audio src={staticFile(`${s}.mp3`)} volume={v} /></Sequence>
      ))}

      {/* 1. o paciente pesquisa */}
      <Cena k={0} bg={G}>{(f) => <>
        <Blob x={140} y={900} w={800} h={700} c={L} o={0.25} />
        <Fala f={f} y={330} linhas={[{de: 0, ate: 4, sz: 84}, {de: 5, ate: 7, sz: 104, peso: 700, cor: A}]} />
        <Busca f={f} />
      </>}</Cena>

      {/* 2. escolhe pelo que encontra */}
      <Cena k={1} bg={G}>{(f) => {
        const a = CUT[1], ruim = io(f, W(12), W(12) + 8, 0, 1), bom = sp(f, W(12) + 4);
        return <>
          <Fala f={f} y={330} linhas={[{de: 8, ate: 9, sz: 110}, {de: 10, ate: 12, sz: 110, peso: 700, cor: A}]} />
          <div style={{position: 'absolute', left: 90, top: 690, width: 820, transform: `rotate(-3deg) scale(${1 - ruim * 0.08})`, opacity: 1 - ruim * 0.55, filter: `grayscale(1)`}}>
            <div style={{background: '#fff', border: '2px solid #E2EAF4', borderRadius: 30, overflow: 'hidden'}}>
              <Bar url="clinicapele.com.br/home.html" />
              <div style={{padding: 36, fontFamily: 'Times New Roman, serif', fontSize: 38, color: '#555'}}>Bem-vindo ao site oficial
                <div style={{display: 'flex', gap: 12, marginTop: 20}}>{[0, 1, 2].map((i) => <div key={i} style={{flex: 1, height: 110, background: '#DADDE3'}} />)}</div></div>
            </div>
          </div>
          <div style={{position: 'absolute', left: 820, top: 640, transform: `scale(${sp(f, W(12))})`}}><Ico n="x" s={150} /></div>
          <div style={{position: 'absolute', left: 170, top: 1140, width: 820, transform: `rotate(2deg) translateY(${(1 - io(f, 0, 12, 0, 1)) * 200}px) scale(${1 + bom * 0.06})`}}>
            <div style={{background: '#fff', border: `${2 + bom * 4}px solid ${bom > 0.5 ? A : '#E2EAF4'}`, borderRadius: 30, overflow: 'hidden', boxShadow: SH}}>
              <Bar url="draanapaula.com.br" />
              <div style={{padding: '36px 44px'}}><div style={{fontSize: 48, letterSpacing: '-0.03em', color: N, lineHeight: 1.05}}><b>Pele saudável</b> <span style={{fontWeight: 300}}>começa na consulta certa.</span></div>
                <div style={{marginTop: 26}}><Btn t="Agendar consulta" sz={30} /></div></div>
            </div>
          </div>
          <div style={{position: 'absolute', left: 110, top: 1100, transform: `scale(${bom})`, zIndex: 9}}><Ico n="tick" s={150} /></div>
        </>;
      }}</Cena>

      {/* 3. A Web Clinic existe pra isso */}
      <Cena k={2} bg={N} dark>{(f) => {
        const k = sp(f, W(14) - 2, 11);
        return <>
          <Blob x={90} y={420} w={900} h={900} c={A} o={0.45} />
          <div style={{position: 'absolute', left: 240, top: 430, transform: `scale(${k}) rotate(${(1 - k) * -20}deg)`}}><Logo s={600} /></div>
          <Pulse y={1010} p={io(f, W(14), W(18), 0, 1)} c={L} sw={4} />
          <Fala f={f} y={1300} align="center" linhas={[{de: 13, ate: 15, sz: 110, cor: '#fff'}, {de: 16, ate: 18, sz: 120, peso: 700, cor: L}]} />
        </>;
      }}</Cena>

      {/* 4. sites para médicos e profissionais da saúde */}
      <Cena k={3} bg={A} dark>{(f) => <>
        <Fala f={f} y={300} linhas={[{de: 19, ate: 22, sz: 96, cor: '#fff'}, {de: 23, ate: 24, sz: 126, peso: 700, cor: '#fff'}, {de: 25, ate: 28, sz: 64, cor: '#DCEBFB'}]} />
        {['steth', 'tooth', 'apple', 'bone', 'brain', 'baby', 'drop', 'heart', 'pulse'].map((n, i) => (
          <Tile key={n} n={n} s={260} x={100 + (i % 3) * 310} y={820 + Math.floor(i / 3) * 300} rot={[-6, 4, -3, 5, -5, 3, 6, -4, 2][i]} k={sp(f, W(21) + i * 5)} />
        ))}
      </>}</Cena>

      {/* 5. não é só um site bonito: é um site que vira consulta marcada */}
      <Cena k={4} bg={G}>{(f) => {
        const risco = io(f, W(34) + 6, W(34) + 14, 0, 1);
        const cx = io(f, W(37), W(40) + 4, 860, 340), cy = io(f, W(37), W(40) + 4, 1700, 1165);
        const clk = f >= W(41) - 2 ? io(f, W(41) - 2, W(41) + 10, 0, 1) : 0;
        const ch = sp(f, W(41) + 3);
        return <>
          <div style={{position: 'absolute', left: 80, top: 330, width: 920, opacity: io(f, W(35) - 4, W(35) + 2, 1, 0)}}>
            <Fala f={f} y={0} x={0} linhas={[{de: 29, ate: 31, sz: 96}, {de: 32, ate: 34, sz: 110, peso: 700}]} />
            <div style={{position: 'absolute', left: -10, top: 150, width: 560 * risco, height: 14, borderRadius: 9, background: R, transform: 'rotate(-4deg)', transformOrigin: 'left'}} />
          </div>
          <Fala f={f} y={330} linhas={[{de: 35, ate: 38, sz: 96}, {de: 39, ate: 41, sz: 108, peso: 700, cor: A}]} />
          <Blob x={140} y={900} w={800} h={700} c={L} o={0.3} />
          <div style={{position: 'absolute', left: 80, top: 720, width: 920, transform: 'perspective(2200px) rotateY(-12deg) rotateX(6deg)', background: '#fff', border: '2px solid #E2EAF4', borderRadius: 36, overflow: 'hidden', boxShadow: SH}}>
            <Bar url="draanapaula.com.br" />
            <div style={{padding: '48px 52px'}}>
              <div style={{fontSize: 20, fontWeight: 600, letterSpacing: '.22em', color: A}}>DERMATOLOGIA</div>
              <div style={{fontSize: 60, lineHeight: 1.04, letterSpacing: '-0.035em', margin: '16px 0 26px', color: N}}><b>Pele saudável</b> <span style={{fontWeight: 300}}>começa na consulta certa.</span></div>
              <Linhas w={1} />
              <div style={{marginTop: 34}}><Btn t="Agendar consulta" sz={36} on={clk} /></div>
            </div>
          </div>
          {f >= W(36) && <div style={{opacity: io(f, W(36), W(36) + 6, 0, 1)}}><Cursor x={cx} y={cy} press={clk > 0 && clk < 0.5 ? 1 : 0} /></div>}
          <Chip icon="tick" t="Consulta marcada" sub="Qui, 13 · 14h · pelo site" x={300} y={1470} k={ch} rot={-2} />
        </>;
      }}</Cena>

      {/* 6. agenda online, aberta 24 horas */}
      <Cena k={5} bg={N} dark>{(f) => {
        const slots = ['08:00', '09:30', '11:00', '14:00', '16:30', '19:00', '21:00', '22:30', '23:45'];
        return <>
          <Blob x={90} y={700} w={900} h={900} c={A} o={0.35} />
          <Fala f={f} y={330} linhas={[{de: 42, ate: 43, sz: 104, cor: '#fff'}, {de: 44, ate: 48, sz: 116, peso: 700, cor: L}]} />
          <div style={{position: 'absolute', left: 80, top: 760, width: 920, background: '#fff', borderRadius: 40, padding: 50, transform: `translateY(${(1 - sp(f, CUT[5] + 2)) * 300}px)`}}>
            <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
              <div><div style={{fontSize: 22, letterSpacing: '.2em', color: A, fontWeight: 600}}>AGENDAR CONSULTA</div><div style={{fontSize: 46, fontWeight: 700, color: N, letterSpacing: '-0.02em'}}>Dra. Ana Paula</div></div>
              <Ico n="moon" s={120} />
            </div>
            <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 18, marginTop: 34}}>
              {slots.map((s, i) => {
                const on = io(f, CUT[5] + 8 + i * 6, CUT[5] + 12 + i * 6, 0, 1);
                return <div key={s} style={{padding: '26px 0', textAlign: 'center', borderRadius: 24, fontSize: 34, fontWeight: 500,
                  background: on > 0.5 ? A : '#fff', color: on > 0.5 ? '#fff' : N, border: `2px solid ${on > 0.5 ? A : '#E2EAF4'}`, transform: `scale(${1 + Math.sin(on * Math.PI) * 0.08})`}}>{s}</div>;
              })}
            </div>
          </div>
        </>;
      }}</Cena>

      {/* 7. seu consultório no Google */}
      <Cena k={6} bg={G}>{(f) => {
        const pin = sp(f, W(52) - 2, 9);
        return <>
          <Fala f={f} y={330} linhas={[{de: 49, ate: 50, sz: 104}, {de: 51, ate: 52, sz: 124, peso: 700, cor: A}]} />
          <div style={{position: 'absolute', left: 80, top: 720, width: 920, background: '#fff', border: '2px solid #E2EAF4', borderRadius: 40, overflow: 'hidden', boxShadow: SH, transform: 'perspective(2200px) rotateY(12deg) rotateX(6deg)'}}>
            <div style={{height: 520, position: 'relative', background: G, overflow: 'hidden'}}>
              <svg width={920} height={520} style={{position: 'absolute', inset: 0}}><path d="M0 130H920M0 370H920M220 0V520M660 0V520" stroke="#fff" strokeWidth={36} /><path d="M0 510L920 40" stroke="#fff" strokeWidth={24} /><rect x="270" y="170" width="340" height="150" rx="18" fill={M} opacity=".6" /></svg>
              <div style={{position: 'absolute', left: 340, top: 60 - (1 - pin) * 300, opacity: pin}}><Ico n="pin" s={250} /></div>
            </div>
            <div style={{padding: '34px 44px'}}>
              <div style={{fontSize: 40, fontWeight: 700, color: N}}>Clínica Dra. Ana Paula</div>
              <div style={{fontSize: 30, color: '#F5B83D', marginTop: 4}}>★★★★★ <span style={{color: C, fontSize: 26}}>· Dermatologia · Aberto agora</span></div>
              <div style={{display: 'flex', gap: 16, marginTop: 24}}><Btn t="Agendar" sz={28} /><span style={{border: '2px solid #E2EAF4', borderRadius: 99, padding: '15px 34px', fontSize: 28, fontWeight: 600, color: N}}>Rotas</span></div>
            </div>
          </div>
        </>;
      }}</Cena>

      {/* 8. WhatsApp a um toque */}
      <Cena k={7} bg={A} dark>{(f) => {
        const tap = W(56), b = sp(f, tap + 6);
        return <>
          <Fala f={f} y={330} linhas={[{de: 53, ate: 53, sz: 120, cor: '#fff'}, {de: 54, ate: 56, sz: 120, peso: 700, cor: '#fff'}]} />
          <div style={{position: 'absolute', left: 250, top: 700, width: 580, height: 1000, borderRadius: 80, background: N, padding: 18, transform: `translateY(${(1 - sp(f, CUT[7])) * 400}px)`}}>
            <div style={{width: '100%', height: '100%', borderRadius: 64, background: '#fff', overflow: 'hidden', padding: '90px 36px 0'}}>
              <div style={{fontSize: 18, fontWeight: 600, letterSpacing: '.2em', color: A}}>PEDIATRIA</div>
              <div style={{fontSize: 44, lineHeight: 1.05, letterSpacing: '-0.03em', margin: '10px 0 22px', color: N}}><b>Cuidado</b> <span style={{fontWeight: 300}}>desde o primeiro dia.</span></div>
              <div style={{height: 200, borderRadius: 28, background: G, display: 'grid', placeItems: 'center'}}><Ico n="baby" s={150} /></div>
              <div style={{marginTop: 24, background: A, color: '#fff', textAlign: 'center', fontWeight: 600, fontSize: 28, borderRadius: 99, padding: 22}}>Agendar consulta</div>
              <div style={{marginTop: 14, border: `3px solid ${f >= tap ? A : '#E2EAF4'}`, textAlign: 'center', fontWeight: 600, fontSize: 28, borderRadius: 99, padding: 20, color: N,
                boxShadow: `0 0 0 ${io(f, tap, tap + 12, 0, 26)}px rgba(45,127,240,${io(f, tap, tap + 12, 0.35, 0)})`}}>WhatsApp</div>
            </div>
          </div>
          <Cursor x={io(f, W(53), tap, 820, 560)} y={io(f, W(53), tap, 1700, 1300)} press={f >= tap && f < tap + 5 ? 1 : 0} />
          <div style={{position: 'absolute', left: 110, top: 1500, display: 'flex', alignItems: 'center', gap: 18, background: '#fff', borderRadius: '10px 36px 36px 36px', padding: '26px 32px', fontSize: 32, color: N,
            boxShadow: SH, transform: `scale(${b})`, transformOrigin: 'left top', zIndex: 16}}><Ico n="chat" s={56} />Olá! Quero agendar.</div>
        </>;
      }}</Cena>

      {/* 9. cada detalhe pensado pra transformar visita em paciente */}
      <Cena k={8} bg={N} dark>{(f) => {
        const passos: [string, string, number][] = [['zoom', 'Google', W(57)], ['computer', 'Site', W(59)], ['calendar', 'Agenda', W(61)], ['heart', 'Paciente', W(64)]];
        return <>
          <Fala f={f} y={330} linhas={[{de: 57, ate: 60, sz: 84, cor: '#fff'}, {de: 61, ate: 64, sz: 92, peso: 700, cor: L}]} />
          <div style={{position: 'absolute', left: 186, top: 800, width: 6, height: 720 * io(f, W(57), W(64) + 6, 0, 1), background: L, borderRadius: 3}} />
          {passos.map(([n, t, at], i) => {
            const k = sp(f, at - 2);
            return <div key={t} style={{position: 'absolute', left: 80, top: 720 + i * 240, display: 'flex', alignItems: 'center', gap: 40, opacity: 0.25 + 0.75 * k}}>
              <div style={{width: 220, height: 220, borderRadius: 60, background: '#fff', display: 'grid', placeItems: 'center', transform: `scale(${0.85 + 0.15 * k})`}}><Ico n={n} s={140} /></div>
              <div><div style={{fontSize: 24, letterSpacing: '.22em', color: L, fontWeight: 600}}>0{i + 1}</div><div style={{fontSize: 64, fontWeight: 700, color: '#fff', letterSpacing: '-0.03em'}}>{t}</div></div>
            </div>;
          })}
        </>;
      }}</Cena>

      {/* 10. você cuida das pessoas; a gente faz elas chegarem até você */}
      <Cena k={9} bg={G}>{(f) => {
        const t2 = W(69);
        const notes: [number, string][] = [[W(72), 'Qui · 09h'], [W(74), 'Qui · 14h'], [W(75) + 4, 'Sex · 10h30']];
        return <>
          <div style={{opacity: io(f, t2 - 4, t2 + 2, 1, 0)}}>
            <Fala f={f} y={330} linhas={[{de: 65, ate: 66, sz: 110}, {de: 67, ate: 68, sz: 120, peso: 700, cor: A}]} />
            <div style={{position: 'absolute', left: 290, top: 820, transform: `scale(${sp(f, CUT[9] + 3)})`}}>
              <div style={{width: 500, height: 500, borderRadius: '50%', background: '#fff', border: '2px solid #E2EAF4', display: 'grid', placeItems: 'center', boxShadow: SH}}><Ico n="steth" s={320} /></div>
            </div>
          </div>
          <Fala f={f} y={330} linhas={[{de: 69, ate: 72, sz: 96}, {de: 73, ate: 75, sz: 112, peso: 700, cor: A}]} />
          {notes.map(([at, s], i) => (
            <Chip key={i} icon="calendar" t="Nova consulta marcada" sub={s} x={110 + (i % 2) * 60} y={760 + i * 210} k={sp(f, at)} rot={[-2, 2, -1][i]} />
          ))}
        </>;
      }}</Cena>

      {/* 11. fecho: Web Clinic. Manda SITE no direct. */}
      <Cena k={10} bg={A} dark>{(f) => {
        const typ = Math.floor(io(f, W(79), W(79) + 10, 0, 4));
        const fim = sp(f, FIM_VOZ + 4);
        return <>
          <Blob x={90} y={380} w={900} h={800} c={L} o={0.6} />
          <div style={{position: 'absolute', left: 290, top: 380, transform: `scale(${sp(f, W(76) - 2, 11)})`}}><Logo s={500} /></div>
          <Fala f={f} y={960} align="center" linhas={[{de: 76, ate: 77, sz: 120, peso: 700, cor: '#fff'}, {de: 78, ate: 81, sz: 84, cor: '#fff'}]} />
          <div style={{position: 'absolute', left: 80, right: 80, top: 1240, display: 'flex', alignItems: 'center', gap: 20, background: '#fff', borderRadius: 99, padding: '18px 18px 18px 44px', fontSize: 44, color: N,
            opacity: io(f, W(78), W(78) + 6, 0, 1), transform: `translateY(${io(f, W(78), W(78) + 8, 40, 0)}px)`}}>
            <span style={{flex: 1}}><b>{'SITE'.slice(0, typ)}</b><span style={{display: 'inline-block', width: 3, height: 48, background: A, marginLeft: 6, verticalAlign: 'middle', opacity: f % 20 < 10 ? 1 : 0}} /></span>
            <span style={{width: 100, height: 100, borderRadius: '50%', background: A, display: 'grid', placeItems: 'center', transform: `scale(${f >= W(79) + 12 && f < W(79) + 18 ? 0.88 : 1})`}}>
              <svg width={46} height={46} viewBox="0 0 24 24"><path d="M4 12l16-8-6 16-3-7z" fill="#fff" /></svg></span>
          </div>
          <div style={{position: 'absolute', left: 0, right: 0, top: 1420, textAlign: 'center', color: '#fff', opacity: fim, transform: `translateY(${(1 - fim) * 30}px)`}}>
            <div style={{fontSize: 52, fontWeight: 600}}>@webclinicbrasil</div>
            <div style={{fontSize: 40, color: '#DCEBFB', marginTop: 10}}>WhatsApp (51) 98906-1441</div>
          </div>
        </>;
      }}</Cena>
    </AbsoluteFill>
  );
};
