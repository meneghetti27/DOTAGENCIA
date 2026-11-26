/* HARD × BLOCK — card de pontuação para Stories (1080×1920). Define window.HXB_CARD. */
(function () {
  "use strict";
  var W = 270, H = 480, S = 4;

  function rnd(seed) { var s = seed || 7; return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; }
  function ok(img) { return img && img.complete !== false && (img.naturalWidth || img.width) > 0; }

  function fundo(c) {
    var r = rnd(42);
    // concreto
    var g = c.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, "#0b0b0f"); g.addColorStop(0.55, "#1d1d24"); g.addColorStop(1, "#2a0e0c");
    c.fillStyle = g; c.fillRect(0, 0, W, H);
    var tons = ["#1d1d24", "#34343d", "#0b0b0f"];
    for (var i = 0; i < 900; i++) { c.fillStyle = tons[(r() * 3) | 0]; c.fillRect((r() * W) | 0, (r() * H) | 0, 1, 1); }
    // blocos de parede
    c.fillStyle = "rgba(0,0,0,0.35)";
    for (var y = 0; y < H; y += 24) { c.fillRect(0, y, W, 1); for (var x = (y / 24) % 2 ? 0 : 24; x < W; x += 48) c.fillRect(x, y, 1, 24); }
    // luzes de domo
    [40, 135, 230].forEach(function (x) {
      for (var k = 5; k > 0; k--) { c.fillStyle = "rgba(255,194,61," + (0.03 * (6 - k)) + ")"; c.fillRect(x - k * 8, 6, k * 16, 30 + k * 10); }
      c.fillStyle = "#55555f"; c.fillRect(x - 7, 4, 14, 3);
      c.fillStyle = "#ffc23d"; c.fillRect(x - 5, 7, 10, 3);
      c.fillStyle = "#f4f2ea"; c.fillRect(x - 3, 7, 6, 1);
    });
    // chamas pixeladas na base
    var cols = ["#c7261f", "#f0662a", "#ffc23d"];
    for (var x2 = 0; x2 < W; x2 += 2) {
      var h0 = 30 + Math.sin(x2 * 0.13) * 12 + r() * 22;
      for (var L = 0; L < 3; L++) {
        var hh = (h0 * (1 - L * 0.32)) | 0;
        c.fillStyle = cols[L]; c.fillRect(x2, H - hh, 2, hh);
      }
    }
    // brasas
    for (var j = 0; j < 40; j++) { c.fillStyle = r() > 0.5 ? "#ffc23d" : "#f0662a"; c.fillRect((r() * W) | 0, (H - 60 - r() * 260) | 0, 1, 1); }
  }

  function texto(c, s, x, y, font, cor, sombra, alinh) {
    c.font = font; c.textAlign = alinh || "center"; c.textBaseline = "alphabetic";
    if (sombra) { c.fillStyle = sombra; c.fillText(s, x + 1, y + 1); }
    c.fillStyle = cor; c.fillText(s, x, y);
  }

  function logo(c, img, x, y, maxW, maxH, alt) {
    if (ok(img)) {
      var w = img.naturalWidth || img.width, h = img.naturalHeight || img.height, k = Math.min(maxW / w, maxH / h);
      c.drawImage(img, (x - w * k / 2) | 0, (y - h * k / 2) | 0, (w * k) | 0, (h * k) | 0);
    } else alt();
  }

  function gerar(opts) {
    opts = opts || {};
    var ft = opts.fonteTitulo || "Pirata One", fp = opts.fontePixel || "Silkscreen";
    var esperar = Promise.resolve();
    try {
      if (document.fonts && document.fonts.load) {
        esperar = Promise.all([
          document.fonts.load("32px \"" + ft + "\""), document.fonts.load("8px \"" + fp + "\""), document.fonts.load("bold 8px \"" + fp + "\"")
        ]).catch(function () {});
      }
    } catch (e) {}
    return esperar.then(function () {
      var cv = document.createElement("canvas"); cv.width = W; cv.height = H;
      var c = cv.getContext("2d"); c.imageSmoothingEnabled = false;
      fundo(c);
      var TF = "\"" + ft + "\", serif", PF = "\"" + fp + "\", monospace";

      // logos no topo
      logo(c, opts.logoHard, 70, 38, 100, 34, function () { texto(c, "HARD", 70, 44, "20px " + TF, "#f4f2ea", "#0b0b0f"); });
      texto(c, "\u00d7", 135, 44, "16px " + PF, "#ffc23d", "#0b0b0f");
      logo(c, opts.logoBlock, 200, 38, 100, 34, function () { texto(c, "BLOCK", 200, 44, "8px " + PF, "#f4f2ea", "#0b0b0f"); });

      // título
      texto(c, "HARD \u00d7 BLOCK", W / 2 + 2, 92, "40px " + TF, "#c7261f");
      texto(c, "HARD \u00d7 BLOCK", W / 2, 90, "40px " + TF, "#f4f2ea");

      // pontuação
      texto(c, "SUA PONTUA\u00c7\u00c3O", W / 2, 116, "8px " + PF, "#a6a6ae");
      var pts = String(opts.pontos != null ? opts.pontos : 0);
      texto(c, pts, W / 2 + 2, 152, "32px " + PF, "#c7261f");
      texto(c, pts, W / 2, 150, "32px " + PF, "#ffc23d");
      if (opts.arroba) texto(c, String(opts.arroba), W / 2, 168, "8px " + PF, "#6fd16a", "#0b0b0f");
      texto(c, opts.venceu ? "derrubou a caveira!" : "chegou at\u00e9 a fase " + (opts.fase || 1), W / 2, 182, "8px " + PF, "#d4d4d8", "#0b0b0f");

      // peça
      var cy = 270;
      for (var k = 6; k > 0; k--) { c.fillStyle = "rgba(240,102,42," + 0.04 * (7 - k) + ")"; c.fillRect(W / 2 - k * 14, cy - k * 12, k * 28, k * 24); }
      if (ok(opts.pecaImg)) {
        var im = opts.pecaImg, w = im.naturalWidth || im.width, h = im.naturalHeight || im.height;
        var esc = Math.max(1, Math.floor(Math.min(150 / w, 130 / h))); if (w * esc > 200 || h * esc > 150) esc = Math.min(200 / w, 150 / h);
        c.drawImage(im, Math.round(W / 2 - w * esc / 2), Math.round(cy - h * esc / 2), Math.round(w * esc), Math.round(h * esc));
      } else {
        c.fillStyle = "#3c5a8a"; c.fillRect(W / 2 - 30, cy - 40, 60, 80);
        c.fillStyle = "#0b0b0f"; c.fillRect(W / 2 - 1, cy - 10, 2, 50);
        texto(c, "DROP", W / 2, cy - 18, "8px " + PF, "#f4f2ea");
      }

      // rodap\u00e9
      c.fillStyle = "rgba(11,11,15,0.8)"; c.fillRect(0, 372, W, 46);
      c.fillStyle = "#c7261f"; c.fillRect(0, 372, W, 1); c.fillRect(0, 417, W, 1);
      texto(c, "@block.office \u00d7 @hardjeanssanto", W / 2, 390, "8px " + PF, "#f4f2ea");
      var lk = String(opts.link || "").replace(/^https?:\/\//, "").replace(/[?#].*$/, "");
      if (/^file:/.test(lk)) lk = "";
      var lt = lk ? "JOGUE: " + lk : "JOGUE O HARD \u00d7 BLOCK", fs = 8;
      c.font = fs + "px " + PF; while (fs > 5 && c.measureText(lt).width > W - 12) { fs--; c.font = fs + "px " + PF; }
      if (c.measureText(lt).width > W - 12) { while (lt.length > 8 && c.measureText(lt + "\u2026").width > W - 12) lt = lt.slice(0, -1); lt += "\u2026"; }
      texto(c, lt, W / 2, 406, fs + "px " + PF, "#ffc23d");

      var out = document.createElement("canvas"); out.width = W * S; out.height = H * S;
      var o = out.getContext("2d"); o.imageSmoothingEnabled = false;
      o.drawImage(cv, 0, 0, W * S, H * S);
      return new Promise(function (res, rej) {
        out.toBlob(function (b) { b ? res(b) : rej(new Error("toBlob falhou")); }, "image/png");
      });
    });
  }

  window.HXB_CARD = { gerar: gerar };
})();
