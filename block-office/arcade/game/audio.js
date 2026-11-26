/* HARD × BLOCK — som (Web Audio puro, chiptune original). Define window.HXB_AUDIO. */
(function () {
  "use strict";
  var ctx = null, master = null, musBus = null, sfxBus = null, noiseBuf = null;
  var muted = false;
  try { muted = localStorage.getItem("hxb_mudo") === "1"; } catch (e) {}
  var cur = null;          // {nome, gain, step, nextTime, track}
  var wanted = null;       // track requested
  var timer = null;
  var LOOK = 0.12, TICK = 25;

  // ---- notas ----
  var NOTE = { C: 0, "C#": 1, D: 2, "D#": 3, E: 4, F: 5, "F#": 6, G: 7, "G#": 8, A: 9, "A#": 10, B: 11 };
  function f(n) { // "A4", "C#3"; "-" = pausa
    if (!n || n === "-") return 0;
    var m = /^([A-G]#?)(\d)$/.exec(n); if (!m) return 0;
    return 440 * Math.pow(2, (NOTE[m[1]] + (+m[2] + 1) * 12 - 69) / 12);
  }
  function seq(s) { return s.split(/\s+/).filter(Boolean); }

  // ---- trilhas (16 passos por compasso, semicolcheias) ----
  // drums: k=bumbo s=caixa h=chimbal o=aberto .=nada
  var TRACKS = {
    menu: { bpm: 92, swing: 0.12, wave: "square",
      lead: seq("E4 - - G4 - A4 - - B4 - A4 - G4 - E4 - D4 - - E4 - G4 - - A4 - - - - - - - E4 - - G4 - A4 - - D5 - B4 - A4 - G4 - A4 - - G4 - E4 - - D4 - - - - - - -"),
      bass: seq("E2 - - - E3 - - - C2 - - - C3 - - - D2 - - - D3 - - - B1 - - - B2 - - -"),
      drum: "k...h...s...h.k.k...h...s..hh..o", vol: 0.5 },
    fase1: { bpm: 96, swing: 0.18, wave: "pulse",
      lead: seq("A4 - C5 - - A4 - G4 - E4 - - G4 - A4 - - - - - C5 - D5 - E5 - D5 - C5 - A4 - A4 - C5 - - A4 - G4 - E4 - - D4 - E4 - - - - - G4 - A4 - - - - - - - - -"),
      bass: seq("A1 - - A1 - - A2 - G1 - - - G2 - E1 - F1 - - F1 - - F2 - G1 - - G2 - E2 - D2 -"),
      drum: "k..k..s..kk...s.k..k..s..k..h.s.", vol: 0.55 },
    fase2: { bpm: 150, swing: 0, wave: "square",
      lead: seq("E5 - E5 D5 E5 - G5 - E5 - D5 - B4 - D5 - E5 - E5 D5 E5 - A5 - G5 - E5 - D5 - B4 - C5 - C5 B4 C5 - E5 - D5 - C5 - B4 - G4 - A4 - B4 - D5 - E5 - - - - - - - - -"),
      bass: seq("E2 E3 E2 E3 E2 E3 E2 E3 C2 C3 C2 C3 D2 D3 D2 D3 A1 A2 A1 A2 A1 A2 A1 A2 B1 B2 B1 B2 B1 B2 D2 D3"),
      drum: "k.h.s.h.k.h.s.hhk.h.s.h.kkh.s.so", vol: 0.5 },
    fase3: { bpm: 84, swing: 0, wave: "triangle",
      lead: seq("D4 - - - F4 - - - E4 - D4 - C#4 - - - D4 - - - A4 - - - G#4 - - - A4 - - - F4 - - - E4 - - - D4 - C4 - A3 - - - A#3 - - - A3 - - - G#3 - - - A3 - - -"),
      bass: seq("D2 - - - D2 - - - A#1 - - - A#1 - - - G1 - - - G1 - - - A1 - - - A1 - - -"),
      drum: "k.......s.......k..k....s...h.h.", vol: 0.6 },
    chefe: { bpm: 168, swing: 0, wave: "square",
      lead: seq("C5 C5 - D#5 - C5 G4 - C5 - D5 D#5 - D5 C5 - G5 - F5 - D#5 - D5 - C5 - A#4 - G4 - - - C5 C5 - D#5 - C5 G4 - G#4 - G4 - F4 - D#4 - D4 - F4 - G4 - B4 - D5 - G5 - - -"),
      bass: seq("C2 C2 C3 C2 C2 C3 C2 C3 G#1 G#1 G#2 G#1 A#1 A#2 B1 B2"),
      drum: "kkh.s.hkk.h.s.hskkh.s.hkk.hss.ss", vol: 0.55 },
    fim: { bpm: 132, swing: 0, wave: "square", once: true,
      lead: seq("C5 - E5 - G5 - C6 - - - G5 - C6 - - - - - - - - - - - - - - - - - - -"),
      bass: seq("C3 - - - G2 - - - C3 - - - C2 - - - - - - - - - - - - - - - - - - -"),
      drum: "k...s...k.k.o...................", vol: 0.6 }
  };

  // ---- vozes ----
  var pulseWave = null;
  function getPulse() {
    if (pulseWave) return pulseWave;
    var n = 32, re = new Float32Array(n), im = new Float32Array(n), d = 0.25;
    for (var i = 1; i < n; i++) im[i] = (2 / (i * Math.PI)) * Math.sin(i * Math.PI * d);
    pulseWave = ctx.createPeriodicWave(re, im); return pulseWave;
  }
  function tone(dest, type, freq, t, dur, vol, slideTo) {
    var o = ctx.createOscillator(), g = ctx.createGain();
    if (type === "pulse") o.setPeriodicWave(getPulse()); else o.type = type;
    o.frequency.setValueAtTime(freq, t);
    if (slideTo) o.frequency.exponentialRampToValueAtTime(Math.max(20, slideTo), t + dur);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.005);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(dest); o.start(t); o.stop(t + dur + 0.02);
  }
  function noise(dest, t, dur, vol, hp, lp) {
    var s = ctx.createBufferSource(); s.buffer = noiseBuf;
    var flt = ctx.createBiquadFilter(); flt.type = hp ? "highpass" : "lowpass"; flt.frequency.value = hp || lp || 1000;
    var g = ctx.createGain();
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    s.connect(flt); flt.connect(g); g.connect(dest);
    s.start(t, Math.random() * 0.5); s.stop(t + dur + 0.02);
  }
  function drum(dest, c, t) {
    if (c === "k") tone(dest, "sine", 150, t, 0.16, 0.9, 40);
    else if (c === "s") { noise(dest, t, 0.12, 0.5, 1200); tone(dest, "triangle", 220, t, 0.06, 0.3, 120); }
    else if (c === "h") noise(dest, t, 0.03, 0.18, 7000);
    else if (c === "o") noise(dest, t, 0.18, 0.18, 6000);
  }

  // ---- agendador ----
  function startTrack(nome) {
    var tr = TRACKS[nome]; if (!tr) return;
    var g = ctx.createGain(); g.gain.setValueAtTime(0.0001, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(tr.vol, ctx.currentTime + 0.6);
    g.connect(musBus);
    cur = { nome: nome, gain: g, step: 0, nextTime: ctx.currentTime + 0.08, track: tr };
  }
  function fadeOut(c) {
    if (!c) return;
    try {
      var t = ctx.currentTime;
      c.gain.gain.cancelScheduledValues(t);
      c.gain.gain.setValueAtTime(Math.max(0.0001, c.gain.gain.value), t);
      c.gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.6);
      setTimeout(function () { try { c.gain.disconnect(); } catch (e) {} }, 900);
    } catch (e) {}
  }
  function schedule() {
    if (!ctx || !cur || ctx.state !== "running") return;
    var tr = cur.track, sd = 60 / tr.bpm / 4;
    while (cur.nextTime < ctx.currentTime + LOOK) {
      var i = cur.step, t = cur.nextTime + (i % 2 ? sd * tr.swing : 0), d = cur.gain;
      if (tr.once && i >= tr.lead.length) { cur = null; return; }
      var ln = tr.lead[i % tr.lead.length], lf = f(ln);
      if (lf) {
        var len = 1; while (tr.lead[(i + len) % tr.lead.length] === "-" && len < 4) len++;
        tone(d, tr.wave, lf, t, sd * len * 0.95, 0.16);
      }
      var bn = tr.bass[i % tr.bass.length], bf = f(bn);
      if (bf) tone(d, "triangle", bf, t, sd * 1.8, 0.35);
      drum(d, tr.drum.charAt(i % tr.drum.length), t);
      cur.step++; cur.nextTime += sd;
    }
  }

  function apply() {
    if (!master) return;
    try { master.gain.setTargetAtTime(muted ? 0 : 0.6, ctx.currentTime, 0.03); } catch (e) {}
  }

  var A = {
    init: function () {
      try {
        if (!ctx) {
          var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
          ctx = new AC();
          master = ctx.createGain(); master.gain.value = muted ? 0 : 0.6;
          var comp = ctx.createDynamicsCompressor(); master.connect(comp); comp.connect(ctx.destination);
          musBus = ctx.createGain(); musBus.gain.value = 0.35; musBus.connect(master);
          sfxBus = ctx.createGain(); sfxBus.gain.value = 0.8; sfxBus.connect(master);
          noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
          var dd = noiseBuf.getChannelData(0); for (var i = 0; i < dd.length; i++) dd[i] = Math.random() * 2 - 1;
          timer = setInterval(function () { try { schedule(); } catch (e) {} }, TICK);
          document.addEventListener("visibilitychange", function () {
            try { if (document.hidden) ctx.suspend(); else ctx.resume(); } catch (e) {}
          });
          if (wanted) startTrack(wanted);
        }
        if (ctx.state === "suspended" && !document.hidden) ctx.resume();
      } catch (e) {}
    },
    musica: function (nome) {
      try {
        if (nome != null && !TRACKS[nome]) return;
        if (cur && cur.nome === nome && !TRACKS[nome].once) return;
        wanted = nome || null;
        if (!ctx) return;
        fadeOut(cur); cur = null;
        if (nome) startTrack(nome);
      } catch (e) {}
    },
    sfx: function (nome) {
      try {
        if (!ctx || muted || ctx.state !== "running") return;
        var t = ctx.currentTime + 0.005, d = sfxBus, r = 1 + (Math.random() - 0.5) * 0.12;
        switch (nome) {
          case "rebate": tone(d, "square", 660 * r, t, 0.06, 0.25, 520 * r); break;
          case "quebra": tone(d, "square", 880 * r, t, 0.05, 0.25); tone(d, "square", 1320 * r, t + 0.04, 0.07, 0.2); noise(d, t, 0.1, 0.3, 2500); break;
          case "duro": tone(d, "triangle", 300 * r, t, 0.09, 0.4, 260 * r); tone(d, "square", 1800 * r, t, 0.03, 0.12); break;
          case "troca": tone(d, "pulse", 440 * r, t, 0.08, 0.25); tone(d, "pulse", 660 * r, t + 0.07, 0.1, 0.25); break;
          case "poder": [523, 659, 784, 1047].forEach(function (q, k) { tone(d, "square", q * r, t + k * 0.05, 0.08, 0.22); }); break;
          case "armadilha": tone(d, "square", 400 * r, t, 0.25, 0.25, 90); tone(d, "square", 410 * r, t, 0.25, 0.15, 95); break;
          case "vida": [784, 988, 1175, 1568, 1175, 1568].forEach(function (q, k) { tone(d, "pulse", q * r, t + k * 0.06, 0.07, 0.2); }); break;
          case "perdeu": [494, 466, 440, 330].forEach(function (q, k) { tone(d, "square", q, t + k * 0.13, 0.14, 0.25, k === 3 ? 160 : 0); }); break;
          case "fase": [523, 659, 784, 659, 784, 1047].forEach(function (q, k) { tone(d, "square", q, t + k * 0.08, 0.1, 0.22); }); break;
          case "chefe-dano": noise(d, t, 0.15, 0.5, 0, 1500); tone(d, "square", 200 * r, t, 0.15, 0.35, 70); break;
          case "explode": noise(d, t, 0.6, 0.8, 0, 900); tone(d, "sine", 120, t, 0.5, 0.7, 30); break;
          case "fogo": noise(d, t, 0.35, 0.35, 0, 2500 * r); tone(d, "sawtooth", 90 * r, t, 0.3, 0.15, 60); break;
        }
      } catch (e) {}
    },
    mudo: function (b) {
      muted = !!b;
      try { localStorage.setItem("hxb_mudo", muted ? "1" : "0"); } catch (e) {}
      apply();
    },
    estaMudo: function () { return muted; }
  };
  window.HXB_AUDIO = A;
})();
