// Web Clinic, vídeo 2: "A Cláudia não dá conta" (Reels 1080x1920, 30 fps).
// Estilo E aprovado: colagem editorial. Fotos recortadas em P&B com borda de papel branco, azul chapado,
// papel rasgado gelo, fita adesiva, número gigante vazado, etiquetas brancas. Poppins. Sem música, só efeitos.
// Narração ElevenLabs v4 (Moutella), tempo por palavra em audio.json (faster-whisper).
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, Easing, delayRender, continueRender, random} from 'remotion';
import AUD from './audio.json';

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
const A = '#2D7FF0', N = '#0B1F3A', L = '#5AA2FF', M = '#CFE6F7', G = '#EEF5FC', C = '#6B7A90';
const P = AUD as {texto: string; inicio: number; fim: number}[];
const fr = (s: number) => Math.round(s * FPS);
const W = (i: number) => fr(P[i].inicio);
export const DURACAO = fr(P[P.length - 1].fim) + fr(2.6);

// cenas: palavra que abre cada uma
const ABRE = [0, 4, 15, 26, 30, 41, 49, 58, 74, 86];
const CUT = [...ABRE.map((i, k) => (k === 0 ? 0 : W(i) - 4)), DURACAO];

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(0.2, 0.8, 0.2, 1);
const io = (f: number, a: number, b: number, x: number, y: number, e = ease) => interpolate(f, [a, b], [x, y], {...clamp, easing: e});
const sp = (f: number, at: number, damping = 11) => spring({frame: f - at, fps: FPS, config: {damping, mass: 0.6, stiffness: 170}});
const treme = (f: number, amp: number, seed: string) => ({x: (random(`${seed}x${Math.floor(f / 2)}`) - 0.5) * amp, y: (random(`${seed}y${Math.floor(f / 2)}`) - 0.5) * amp});

// ---------- linguagem da colagem ----------
const PAPEL = 'drop-shadow(7px 0 0 #fff) drop-shadow(-7px 0 0 #fff) drop-shadow(0 7px 0 #fff) drop-shadow(0 -7px 0 #fff) drop-shadow(0 26px 30px rgba(11,31,58,.38))';
const PB = 'grayscale(1) contrast(1.18) brightness(1.04)';
const Recorte: React.FC<{src: string; x: number; y: number; w: number; rot?: number; k?: number; cor?: boolean; op?: number; z?: number; extra?: string}> = ({src, x, y, w, rot = 0, k = 1, cor, op = 1, z = 5, extra = ''}) => (
  <Img src={staticFile(src)} style={{position: 'absolute', left: x, top: y, width: w, transform: `rotate(${rot}deg) scale(${k})`, transformOrigin: '50% 100%',
    filter: `${cor ? '' : PB} ${PAPEL} ${extra}`, opacity: op, zIndex: z}} />
);
const Etiqueta: React.FC<{f: number; at: number; x: number; y: number; rot?: number; sz?: number; escuro?: boolean; azul?: boolean; icon?: string; children: React.ReactNode; z?: number; sai?: number}> = ({f, at, x, y, rot = 0, sz = 40, escuro, azul, icon, children, z = 20, sai}) => {
  const s = sp(f, at);
  const o = sai === undefined ? 1 : io(f, sai, sai + 6, 1, 0);
  if (f < at) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg) scale(${(0.4 + s * 0.6) * (0.9 + o * 0.1)})`, opacity: Math.min(1, s * 2) * o, transformOrigin: 'left center', zIndex: z,
      padding: `${sz * 0.5}px ${sz * 0.8}px`, borderRadius: 999, background: escuro ? N : azul ? A : '#fff', color: escuro || azul ? '#fff' : N,
      fontWeight: 600, fontSize: sz, letterSpacing: '-0.02em', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: sz * 0.4,
      boxShadow: '0 18px 34px -10px rgba(11,31,58,.45)'}}>
      {icon ? <span style={{fontSize: sz * 0.95}}>{icon}</span> : null}{children}
    </div>
  );
};
const Fita: React.FC<{x: number; y: number; rot: number; w?: number}> = ({x, y, rot, w = 230}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: 62, background: 'rgba(207,230,247,.82)', transform: `rotate(${rot}deg)`, zIndex: 12,
    boxShadow: '0 4px 10px rgba(11,31,58,.12)', clipPath: 'polygon(2% 0,98% 4%,100% 50%,97% 100%,3% 96%,0 50%)'}} />
);
const borda = (seed: string, n = 22) => {
  const pts: string[] = [];
  for (let i = 0; i <= n; i++) pts.push(`${(i / n) * 100}% ${30 + random(`${seed}${i}`) * 55}%`);
  return `polygon(${pts.join(',')},100% 100%,0 100%)`;
};
// papel rasgado: faixa gelo com borda irregular
const Rasgo: React.FC<{y: number; cor?: string; seed?: string; z?: number}> = ({y, cor = G, seed = 'r', z = 2}) => (
  <>
    <div style={{position: 'absolute', left: -20, right: -20, top: y - 70, height: 90, background: cor, clipPath: borda(seed), zIndex: z, filter: 'drop-shadow(0 -6px 8px rgba(11,31,58,.15))'}} />
    <div style={{position: 'absolute', left: 0, right: 0, top: y, bottom: 0, background: cor, zIndex: z}} />
  </>
);
const Vazado: React.FC<{t: string; x: number; y: number; sz: number; k?: number; cor?: string; op?: number}> = ({t, x, y, sz, k = 1, cor = 'rgba(255,255,255,.85)', op = 1}) => (
  <div style={{position: 'absolute', left: x, top: y, fontWeight: 700, fontSize: sz, lineHeight: 1, letterSpacing: '-0.06em', color: 'transparent', WebkitTextStroke: `6px ${cor}`,
    transform: `scale(${k})`, transformOrigin: '50% 50%', opacity: op, zIndex: 3}}>{t}</div>
);
const Titulo: React.FC<{f: number; at: number; a: string; b: string; y?: number; claro?: boolean; sz?: number}> = ({f, at, a, b, y = 250, claro, sz = 96}) => {
  const o1 = io(f, at, at + 8, 0, 1), o2 = io(f, at + 5, at + 13, 0, 1);
  return (
    <div style={{position: 'absolute', left: 80, right: 80, top: y, zIndex: 25, letterSpacing: '-0.045em', lineHeight: 1.02}}>
      <div style={{fontSize: sz, fontWeight: 300, color: claro ? '#fff' : N, opacity: o1, transform: `translateY(${(1 - o1) * 40}px)`, filter: `blur(${(1 - o1) * 10}px)`}}>{a}</div>
      <div style={{fontSize: sz * 1.08, fontWeight: 700, color: claro ? N : A, opacity: o2, transform: `translateY(${(1 - o2) * 40}px)`, filter: `blur(${(1 - o2) * 10}px)`}}>{b}</div>
    </div>
  );
};
const Grao: React.FC<{f: number}> = ({f}) => (
  <Img src={staticFile(`grao${Math.floor(f / 2) % 4}.jpg`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'multiply', opacity: 0.13, zIndex: 40}} />
);
const LOGO = (c1: string, c2: string, cp: string) => `<svg width="100%" viewBox="26 86 190 100"><text x="120" y="124" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="40" letter-spacing="-1.8"><tspan fill="${c1}">web</tspan><tspan fill="${c2}">clinic</tspan></text><path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke="${cp}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const Marca: React.FC<{claro?: boolean}> = ({claro}) => (
  <div style={{position: 'absolute', top: 140, left: 0, right: 0, display: 'flex', justifyContent: 'center', zIndex: 35}}>
    <div style={{width: 170}} dangerouslySetInnerHTML={{__html: claro ? LOGO('#fff', M, M) : LOGO(N, A, A)}} />
  </div>
);

// ---------- legenda: palavras da cena entrando no tempo da voz, numa tira de papel ----------
const Legenda: React.FC<{g: number; de: number; ate: number; escuro?: boolean}> = ({g, de, ate, escuro}) => {
  const ws = Array.from({length: ate - de + 1}, (_, j) => de + j);
  const vis = ws.filter((i) => g >= W(i) - 2);
  if (!vis.length) return null;
  // mostra no máximo as últimas 7 palavras faladas
  const mostra = vis.slice(-7);
  return (
    <div style={{position: 'absolute', left: 70, right: 70, top: 1530, display: 'flex', justifyContent: 'center', zIndex: 30}}>
      <div style={{background: escuro ? 'rgba(255,255,255,.96)' : '#fff', padding: '16px 30px', borderRadius: 18, boxShadow: '0 16px 30px -12px rgba(11,31,58,.4)', transform: 'rotate(-1.2deg)',
        fontSize: 46, fontWeight: 600, color: N, letterSpacing: '-0.02em', lineHeight: 1.2, textAlign: 'center', maxWidth: 940}}>
        {mostra.map((i) => {
          const o = io(g, W(i) - 2, W(i) + 3, 0, 1);
          const ativo = g >= W(i) && g < fr(P[i].fim) + 4;
          return <span key={i} style={{display: 'inline-block', marginRight: '0.22em', opacity: o, transform: `translateY(${(1 - o) * 16}px)`, color: ativo ? A : N}}>{P[i].texto}</span>;
        })}
      </div>
    </div>
  );
};

// ---------- cena com corte "rasgando": a nova cena entra subindo por trás de um rasgo de papel ----------
const Cena: React.FC<{k: number; bg: string; children: (f: number, g: number) => React.ReactNode; escuro?: boolean; marcaClara?: boolean; semMarca?: boolean}> = ({k, bg, children, escuro, marcaClara, semMarca}) => {
  const g = useCurrentFrame();
  const a = CUT[k], b = CUT[k + 1];
  if (g < a || g >= b) return null;
  const f = g - a;
  const ent = k === 0 ? 1 : io(f, 0, 10, 0, 1, Easing.out(Easing.cubic));
  const y = (1 - ent) * 1920;
  const zoom = interpolate(f, [0, b - a], [1, 1.035]);
  return (
    <AbsoluteFill style={{fontFamily, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translateY(${y}px)`}}>
        <AbsoluteFill style={{background: bg}} />
        <AbsoluteFill style={{transform: `scale(${zoom})`}}>{children(f, g)}</AbsoluteFill>
        {semMarca ? null : <Marca claro={marcaClara} />}
        <Legenda g={g} de={ABRE[k]} ate={(ABRE[k + 1] ?? P.length) - 1} escuro={escuro} />
        {k > 0 && ent < 1 ? <div style={{position: 'absolute', left: -20, right: -20, top: -80, height: 100, background: bg, clipPath: borda(`c${k}`, 26).replace('100% 100%,0 100%', '100% 100%,0 100%'), transform: 'scaleY(-1)'}} /> : null}
      </AbsoluteFill>
      <Grao f={g} />
    </AbsoluteFill>
  );
};

// ---------- peças ----------
const Relogio: React.FC<{f: number; at: number; x: number; y: number; s: number}> = ({f, at, x, y, s}) => {
  const p = io(f, at, at + 26, 0, 1, Easing.out(Easing.cubic));
  const min = -360 * (1 - p); // ponteiro de minutos dá uma volta e para no 12
  const hora = 160 + p * 20; // ponteiro de horas chega no 6
  return (
    <svg style={{position: 'absolute', left: x, top: y, filter: PAPEL, zIndex: 6}} width={s} height={s} viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="92" fill="#fff" stroke={N} strokeWidth="10" />
      {Array.from({length: 12}, (_, i) => <rect key={i} x="97" y="18" width="6" height={i % 3 ? 10 : 18} rx="3" fill={N} transform={`rotate(${i * 30} 100 100)`} />)}
      <rect x="95" y="50" width="10" height="56" rx="5" fill={N} transform={`rotate(${hora} 100 100)`} />
      <rect x="97" y="26" width="6" height="80" rx="3" fill={A} transform={`rotate(${min} 100 100)`} />
      <circle cx="100" cy="100" r="9" fill={N} />
    </svg>
  );
};
const Fone: React.FC<{x: number; y: number; w: number; tocando: boolean; f: number; rot?: number}> = ({x, y, w, tocando, f, rot = -6}) => {
  const t = tocando ? treme(f, 14, 'fone') : {x: 0, y: 0};
  return (
    <div style={{position: 'absolute', left: x + t.x, top: y + t.y, transform: `rotate(${rot + (tocando ? Math.sin(f * 1.7) * 3 : 0)}deg)`, zIndex: 6}}>
      <Img src={staticFile('telefone.png')} style={{width: w, filter: `${PB} ${PAPEL}`}} />
      {tocando ? [0, 1].map((i) => (
        <svg key={i} style={{position: 'absolute', left: i ? w - 30 : -60, top: -40, transform: i ? 'none' : 'scaleX(-1)'}} width={90} height={120} viewBox="0 0 90 120">
          <g fill="none" stroke="#fff" strokeWidth="9" strokeLinecap="round" opacity={0.6 + Math.sin(f / 2 + i) * 0.4}><path d="M20 30a40 40 0 0 1 0 60" /><path d="M45 15a65 65 0 0 1 0 90" /></g>
        </svg>
      )) : null}
    </div>
  );
};
const Celular: React.FC<{x: number; y: number; w: number; children: React.ReactNode; rot?: number}> = ({x, y, w, children, rot = 0}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, height: w * 2.05, borderRadius: w * 0.14, background: N, padding: w * 0.035, transform: `rotate(${rot}deg)`,
    boxShadow: '0 0 0 8px #fff, 0 50px 80px -20px rgba(0,0,0,.6)', zIndex: 8}}>
    <div style={{width: '100%', height: '100%', borderRadius: w * 0.11, background: '#fff', overflow: 'hidden', position: 'relative'}}>{children}</div>
  </div>
);

// ================== CENAS ==================
export const Video: React.FC = () => {
  const e = (k: number, i: number) => W(i) - CUT[k];
  return (
    <AbsoluteFill style={{background: A}}>
      {/* 1. "Essa é a Cláudia." */}
      <Cena k={0} bg={A} marcaClara>
        {(f) => (
          <>
                        <Rasgo y={1330} seed="a" />
            <Recorte src="claudia-base.png" x={170} y={500 + (1 - sp(f, 2, 13)) * 500} w={740} z={5} />
            <Fita x={150} y={560} rot={-14} />
            <Etiqueta f={f} at={e(0, 3)} x={470} y={760} rot={-5} sz={44} escuro icon="🪪">Cláudia · recepção</Etiqueta>
          </>
        )}
      </Cena>

      {/* 2. telefone, WhatsApp, porta, Instagram */}
      <Cena k={1} bg={G} marcaClara>
        {(f) => (
          <>
            <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 980, background: A}} />
            <Rasgo y={1010} seed="b" />
            <Recorte src="claudia-base.png" x={-60} y={430} w={560} z={4} />
            <Fone x={470} y={1080} w={480} f={f} tocando={f >= e(1, 7) - 2} />
            <Etiqueta f={f} at={e(1, 7)} x={470} y={430} rot={-6} sz={50} icon="☎️">telefone</Etiqueta>
            <Etiqueta f={f} at={e(1, 9)} x={540} y={570} rot={4} sz={50} azul icon="💬">WhatsApp</Etiqueta>
            <Etiqueta f={f} at={e(1, 11)} x={470} y={710} rot={-3} sz={50} icon="🔔">a porta</Etiqueta>
            <Etiqueta f={f} at={e(1, 14)} x={500} y={850} rot={5} sz={50} escuro icon="📷">Instagram</Etiqueta>
          </>
        )}
      </Cena>

      {/* 3. perguntas repetidas */}
      <Cena k={2} bg={A} marcaClara escuro>
        {(f) => {
          const big = sp(f, e(2, 23), 9);
          const t = treme(f, f >= e(2, 23) ? 10 : 0, 'q');
          return (
            <>
              <Etiqueta f={f} at={e(2, 15)} x={90} y={430} rot={-7} sz={54}>Qual o valor?</Etiqueta>
              <Etiqueta f={f} at={e(2, 18)} x={380} y={600} rot={5} sz={54}>Atende convênio?</Etiqueta>
              <Etiqueta f={f} at={e(2, 20)} x={120} y={770} rot={-3} sz={54}>Tem horário hoje?</Etiqueta>
              <Etiqueta f={f} at={e(2, 15) + 6} x={600} y={330} rot={8} sz={34} escuro>Aceita Pix?</Etiqueta>
              <Etiqueta f={f} at={e(2, 18) + 6} x={80} y={940} rot={6} sz={34} escuro>Tem estacionamento?</Etiqueta>
              <Etiqueta f={f} at={e(2, 20) + 6} x={620} y={950} rot={-6} sz={34} escuro>Pode encaixar?</Etiqueta>
              {f >= e(2, 23) ? (
                <div style={{position: 'absolute', left: 60 + t.x, right: 60, top: 1080 + t.y, transform: `rotate(-4deg) scale(${0.3 + big * 0.7})`, transformOrigin: '50% 50%', zIndex: 22,
                  background: '#fff', borderRadius: 40, padding: '40px 30px', textAlign: 'center', fontWeight: 700, fontSize: 112, color: N, letterSpacing: '-0.05em', lineHeight: 1,
                  boxShadow: '0 30px 60px -20px rgba(11,31,58,.6)'}}>QUAL O VALOR?</div>
              ) : null}
              <Fita x={110} y={1060} rot={-18} />
              <Fita x={760} y={1250} rot={14} />
            </>
          );
        }}
      </Cena>

      {/* 4. 47 vezes por dia */}
      <Cena k={3} bg={A} marcaClara>
        {(f) => {
          const n = Math.round(io(f, 0, 16, 1, 47, Easing.out(Easing.cubic)));
          return (
            <>
              <Vazado t={String(n)} x={60} y={330} sz={760} k={0.85 + sp(f, 0, 12) * 0.15} />
              <Rasgo y={1180} seed="d" />
              <Recorte src="claudia-estresse.png" x={40} y={560 + (1 - sp(f, 3, 12)) * 300} w={1000} z={5} />
              <Fita x={70} y={620} rot={-10} />
              <Fita x={790} y={600} rot={12} />
              <Etiqueta f={f} at={e(3, 28)} x={600} y={1260} rot={-4} sz={60} escuro>por dia.</Etiqueta>
              <Etiqueta f={f} at={4} x={90} y={1280} rot={5} sz={36} icon="☎️">47 chamadas</Etiqueta>
            </>
          );
        }}
      </Cena>

      {/* 5. três desistem e marcam no concorrente */}
      <Cena k={4} bg={G} marcaClara>
        {(f) => {
          const des = e(4, 35);
          return (
            <>
              <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 560, background: A}} />
              <Rasgo y={580} seed="e" cor={G} z={1} />
              <Titulo f={f} at={0} a="Enquanto ela" b="atende um..." y={300} claro sz={84} />
              {[0, 1, 2].map((i) => {
                const at = des + i * 4;
                const cinza = io(f, at, at + 8, 0, 1);
                const sai = io(f, e(4, 37) + i * 3, e(4, 37) + i * 3 + 14, 0, 1, Easing.in(Easing.cubic));
                return (
                  <div key={i} style={{position: 'absolute', left: 90 + i * 310 + sai * 900, top: 720 + (i === 1 ? -20 : 0), zIndex: 5, opacity: 1 - sai * 0.4}}>
                    <Img src={staticFile(`paciente${i}.png`)} style={{height: 720, filter: `grayscale(${0.6 + cinza * 0.4}) contrast(1.1) brightness(${1 - cinza * 0.08}) ${PAPEL}`, opacity: 1 - cinza * 0.35}} />
                  </div>
                );
              })}
              <Etiqueta f={f} at={des} x={80} y={660} rot={-6} sz={40} escuro icon="📵">desistiu</Etiqueta>
              <Etiqueta f={f} at={des + 4} x={420} y={640} rot={4} sz={40} escuro icon="📵">desistiu</Etiqueta>
              <Etiqueta f={f} at={des + 8} x={700} y={680} rot={-3} sz={40} escuro icon="📵">desistiu</Etiqueta>
              <Etiqueta f={f} at={e(4, 38)} x={360} y={1340} rot={-3} sz={50} azul>consultório ao lado →</Etiqueta>
            </>
          );
        }}
      </Cena>

      {/* 6. às seis a Cláudia vai pra casa. Merecido. */}
      <Cena k={5} bg={A} marcaClara>
        {(f) => {
          const anda = io(f, e(5, 44), e(5, 48) + 10, 0, 1, Easing.inOut(Easing.cubic));
          return (
            <>
              <Relogio f={f} at={2} x={90} y={360} s={420} />
              <Etiqueta f={f} at={e(5, 42)} x={130} y={830} rot={-5} sz={64} escuro>18:00</Etiqueta>
              <Rasgo y={1200} seed="f" />
              <Recorte src="claudia-tchau.png" x={560 + anda * 120} y={460} w={440} rot={anda * 3} z={5} />
              <Etiqueta f={f} at={e(5, 48)} x={430} y={1260} rot={4} sz={60} icon="💙">merecido.</Etiqueta>
              <Fita x={620} y={480} rot={-12} />
            </>
          );
        }}
      </Cena>

      {/* 7. às dez da noite tem paciente querendo marcar */}
      <Cena k={6} bg={N} marcaClara escuro>
        {(f) => {
          const ok = f >= e(6, 54);
          return (
            <>
              <Vazado t="22:47" x={70} y={330} sz={300} cor="rgba(90,162,255,.7)" />
              <Celular x={250} y={640} w={420} rot={-4}>
                <div style={{position: 'absolute', inset: 0, background: `linear-gradient(180deg, ${G}, #fff)`}} />
                <div style={{position: 'absolute', top: 70, left: 0, right: 0, textAlign: 'center', fontSize: 92, fontWeight: 300, color: N, letterSpacing: '-0.04em'}}>22:47</div>
                <div style={{position: 'absolute', top: 190, left: 0, right: 0, textAlign: 'center', fontSize: 24, color: C}}>domingo</div>
                {ok ? (
                  <div style={{position: 'absolute', top: 280, left: 22, right: 22, background: '#fff', borderRadius: 26, padding: '20px 22px', boxShadow: '0 12px 30px rgba(11,31,58,.18)',
                    transform: `translateY(${(1 - sp(f, e(6, 54))) * -60}px)`, opacity: Math.min(1, sp(f, e(6, 54)) * 2)}}>
                    <div style={{fontSize: 20, color: C, fontWeight: 600}}>💬 WhatsApp · Clínica</div>
                    <div style={{fontSize: 26, color: N, fontWeight: 500, marginTop: 6}}>Oi! Tem horário amanhã?</div>
                    <div style={{fontSize: 20, color: C, marginTop: 10}}>✓✓ enviada · sem resposta</div>
                  </div>
                ) : null}
              </Celular>
              <Etiqueta f={f} at={e(6, 57)} x={440} y={1330} rot={5} sz={44} icon="🌙">recepção fechada</Etiqueta>
            </>
          );
        }}
      </Cena>

      {/* 8. com a Web Clinic o site responde, mostra os horários e marca. Sozinho. */}
      <Cena k={7} bg={G} marcaClara>
        {(f) => {
          const slot = f >= e(7, 68);
          const marca = e(7, 70);
          const carimbo = sp(f, e(7, 72), 8);
          const slots = ['09:00', '10:30', '14:30', '16:00', '17:30', '19:00'];
          return (
            <>
              <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 520, background: A}} />
              <Rasgo y={540} seed="h" cor={G} z={1} />
              <Titulo f={f} at={0} a="Com a" b="Web Clinic" y={290} claro sz={92} />
              <div style={{position: 'absolute', left: 90, top: 640 + (1 - sp(f, 4, 13)) * 400, width: 900, background: '#fff', borderRadius: 34, overflow: 'hidden', zIndex: 6,
                boxShadow: '0 0 0 8px #fff, 0 40px 70px -24px rgba(11,31,58,.45)', transform: 'rotate(-2deg)'}}>
                <div style={{height: 64, background: G, display: 'flex', alignItems: 'center', gap: 10, padding: '0 24px'}}>
                  {['#FA5F6D', '#F5B83D', '#3CC48A'].map((c, i) => <i key={i} style={{width: 14, height: 14, borderRadius: 8, background: c}} />)}
                  <div style={{marginLeft: 16, flex: 1, height: 38, borderRadius: 99, background: '#fff', fontSize: 20, color: C, display: 'flex', alignItems: 'center', padding: '0 18px'}}>suaclinica.com.br/agendar</div>
                </div>
                <div style={{padding: '34px 40px'}}>
                  <div style={{fontSize: 22, fontWeight: 600, letterSpacing: '.2em', color: A}}>AGENDA ONLINE · 24H</div>
                  <div style={{fontSize: 52, letterSpacing: '-0.04em', color: N, margin: '8px 0 24px'}}><b>Escolha</b> <span style={{fontWeight: 300}}>um horário</span></div>
                  <div style={{display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 16}}>
                    {slots.map((s, i) => {
                      const on = slot && i === 2;
                      const k = slot ? sp(f, e(7, 68) + i * 2, 14) : 0;
                      return <div key={s} style={{height: 84, borderRadius: 20, display: 'grid', placeItems: 'center', fontSize: 34, fontWeight: 600,
                        background: on && f >= marca ? A : G, color: on && f >= marca ? '#fff' : N, border: `3px solid ${on ? A : 'transparent'}`, transform: `scale(${0.96 + k * 0.04})`}}>{s}</div>;
                    })}
                  </div>
                  <div style={{marginTop: 26, height: 92, borderRadius: 99, background: `linear-gradient(180deg, ${L}, ${A})`, color: '#fff', fontSize: 38, fontWeight: 600, display: 'grid', placeItems: 'center',
                    transform: `scale(${f >= marca && f < marca + 6 ? 0.95 : 1})`}}>Agendar consulta</div>
                </div>
              </div>
              <Etiqueta f={f} at={e(7, 65)} x={440} y={600} rot={5} sz={36} escuro icon="💬">"R$ 350 · aceita Unimed"</Etiqueta>
              {f >= e(7, 72) ? (
                <div style={{position: 'absolute', left: 170, top: 1140, zIndex: 24, transform: `rotate(-9deg) scale(${2.2 - carimbo * 1.2})`, opacity: Math.min(1, carimbo * 1.6), transformOrigin: '50% 50%',
                  border: `10px solid ${N}`, borderRadius: 24, padding: '18px 40px', fontWeight: 700, fontSize: 78, color: N, letterSpacing: '-0.03em', background: 'rgba(238,245,252,.9)',
                  boxShadow: `inset 0 0 0 6px ${G}, inset 0 0 0 12px ${N}`}}>CONSULTA MARCADA ✓</div>
              ) : null}
              <Etiqueta f={f} at={e(7, 73)} x={640} y={1400} rot={6} sz={48} azul>sozinho.</Etiqueta>
            </>
          );
        }}
      </Cena>

      {/* 9. a Cláudia cuida de quem chega, o site de quem procura */}
      <Cena k={8} bg={A} marcaClara>
        {(f) => (
          <>
            <Rasgo y={1240} seed="i" />
            <Recorte src="claudia-cafe.png" x={40} y={520 + (1 - sp(f, 2, 13)) * 300} w={560} z={5} />
            <Fita x={60} y={560} rot={-12} />
            <div style={{position: 'absolute', left: 600, top: 520 + (1 - sp(f, e(8, 80), 13)) * 600, width: 400, background: '#fff', borderRadius: 28, padding: '26px 26px', zIndex: 6,
              boxShadow: '0 0 0 8px #fff, 0 30px 60px -20px rgba(11,31,58,.5)', transform: 'rotate(4deg)'}}>
              <div style={{fontSize: 20, fontWeight: 600, letterSpacing: '.18em', color: A}}>AGENDA DE AMANHÃ</div>
              {['08:00 · Marta S.', '09:30 · João P.', '11:00 · Ana L.', '14:30 · Rui M.', '16:00 · Bia C.'].map((t, i) => (
                <div key={t} style={{marginTop: 14, padding: '12px 16px', borderRadius: 14, background: G, fontSize: 26, fontWeight: 500, color: N,
                  opacity: io(f, e(8, 80) + 6 + i * 3, e(8, 80) + 10 + i * 3, 0, 1)}}>✓ {t}</div>
              ))}
            </div>
            <Etiqueta f={f} at={e(8, 79)} x={70} y={1290} rot={-4} sz={40} icon="☕">quem chega</Etiqueta>
            <Etiqueta f={f} at={e(8, 85)} x={520} y={1330} rot={4} sz={40} escuro icon="🔎">quem procura</Etiqueta>
          </>
        )}
      </Cena>

      {/* 10. Web Clinic. Manda SITE no direct. */}
      <Cena k={9} bg={G} semMarca>
        {(f) => {
          const s = sp(f, 2, 12);
          const p = io(f, 6, 30, 0, 1, Easing.inOut(Easing.cubic));
          return (
            <>
              <div style={{position: 'absolute', left: 0, right: 0, top: 1100, bottom: 0, background: A}} />
              <Rasgo y={1100} seed="j" cor={A} z={1} />
              <div style={{position: 'absolute', left: 140, right: 140, top: 520, transform: `scale(${0.7 + s * 0.3})`, opacity: Math.min(1, s * 2), zIndex: 6}}>
                <svg width="100%" viewBox="26 86 190 100">
                  <text x="120" y="124" textAnchor="middle" fontFamily="Poppins" fontWeight={700} fontSize={40} letterSpacing={-1.8}><tspan fill={N}>web</tspan><tspan fill={A}>clinic</tspan></text>
                  <path d="M46 158H98L108 138L122 180L134 148L142 158H194" fill="none" stroke={A} strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
                </svg>
              </div>
              <div style={{position: 'absolute', left: 0, right: 0, top: 930, textAlign: 'center', fontSize: 44, fontWeight: 300, color: N, letterSpacing: '-0.03em', opacity: io(f, 10, 20, 0, 1), zIndex: 6}}>
                Sites que viram <b style={{fontWeight: 700, color: A}}>consulta marcada.</b>
              </div>
              <Etiqueta f={f} at={e(9, 88)} x={190} y={1260} rot={-3} sz={58} escuro icon="💬">Manda SITE no direct</Etiqueta>
              <Fita x={150} y={1230} rot={-16} w={180} />
            </>
          );
        }}
      </Cena>

      {/* ---------- som ---------- */}
      <Audio src={staticFile('voz.mp3')} />
      {CUT.slice(1, -1).map((c, i) => <Sequence key={`w${i}`} from={c - 2} durationInFrames={30}><Audio src={staticFile('whoosh.mp3')} volume={0.45} /></Sequence>)}
      {[3, 7, 9, 11, 14, 15, 18, 20, 28, 35, 38, 42, 48, 54, 65, 73, 79, 85, 88].map((i) => <Sequence key={`p${i}`} from={W(i)} durationInFrames={20}><Audio src={staticFile('pop.mp3')} volume={0.5} /></Sequence>)}
      <Sequence from={W(23)} durationInFrames={30}><Audio src={staticFile('impacto.mp3')} volume={0.55} /></Sequence>
      <Sequence from={W(26) - 4} durationInFrames={30}><Audio src={staticFile('impacto.mp3')} volume={0.6} /></Sequence>
      {Array.from({length: 8}, (_, i) => <Sequence key={`t${i}`} from={CUT[5] + 2 + i * 3} durationInFrames={6}><Audio src={staticFile('tique.mp3')} volume={0.35} /></Sequence>)}
      <Sequence from={W(72)} durationInFrames={40}><Audio src={staticFile('impacto.mp3')} volume={0.5} /></Sequence>
      <Sequence from={W(72) + 4} durationInFrames={40}><Audio src={staticFile('ding.mp3')} volume={0.5} /></Sequence>
      <Sequence from={W(86)} durationInFrames={40}><Audio src={staticFile('ding.mp3')} volume={0.45} /></Sequence>
    </AbsoluteFill>
  );
};
