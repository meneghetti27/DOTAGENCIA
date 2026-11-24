"""painel da identidade (paleta, fontes, versões do logo, elementos) -> artes/painel-identidade.png"""
import subprocess
from pathlib import Path
from gerar import estrela, til, capelo, pingo, ROXO, BRANCO, PRETO, LILAS, UVA, AQUI
A = AQUI / "artes"
el = "".join([estrela(120, 120, 90, BRANCO), estrela(330, 120, 70, ROXO),
              til(560, 120, 300, BRANCO, giro=-8), capelo(850, 110, 240, ROXO, giro=10)]
             + pingo(1110, 70, 70, 56, ROXO))
sw = [("Roxo turma", ROXO, "principal"), ("Branco", BRANCO, "recheio / brilhos"),
      ("Uva", UVA, "sombra 3D"), ("Lilás", LILAS, "luz (digital)"), ("Preto", "#0A0A0C", "moletom / contorno")]
cards = "".join(f'<div class=sw><i style="background:{c}"></i><b>{n}</b><span>{c.upper()}</span><em>{u}</em></div>' for n, c, u in sw)
html = f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:Bagel;src:url(../fontes/bagel-fat-one.ttf)}}
@font-face{{font-family:Tag;src:url(../fontes/sedgwick-ave-display.ttf)}}
body{{margin:0;width:2400px;background:#0A0A0C;color:#fff;font-family:Bagel}}
.w{{padding:90px 110px}} h1{{font-size:44px;letter-spacing:.2em;color:{ROXO};margin:0 0 40px;font-weight:400}}
.top{{display:grid;grid-template-columns:1.05fr 1fr;gap:80px;align-items:start}}
.logos{{display:grid;grid-template-columns:1fr 1fr;gap:30px}} .logos img{{width:100%;background:#111014;border-radius:28px;padding:30px;box-sizing:border-box}}
.sws{{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;margin-bottom:70px}}
.sw i{{display:block;height:180px;border-radius:24px;border:3px solid #2a2530}} .sw b{{display:block;font-weight:400;font-size:30px;margin-top:16px}}
.sw span{{font-family:monospace;font-size:24px;color:#bbb}} .sw em{{display:block;font-style:normal;font-family:sans-serif;font-size:20px;color:#888;margin-top:6px}}
.f{{background:#111014;border-radius:28px;padding:36px 44px;margin-bottom:26px}} .f small{{font-family:sans-serif;color:#999;font-size:22px;letter-spacing:.1em}}
.f p{{margin:10px 0 0;font-size:84px;line-height:1}} .t p{{font-family:Tag;color:{ROXO}}}
.hz img{{width:100%;margin-top:40px}} svg{{display:block;margin-top:10px}}
</style></head><body><div class=w>
<h1>TERCEIRÃO 2027 · IDENTIDADE VISUAL</h1>
<div class=top><div><div class=logos>
<img src="principal/logo-principal.png"><img src="contorno-branco/logo-principal.png">
<img src="1cor-roxo/logo-principal.png"><img src="1cor-branco/logo-principal.png"></div>
<div class=hz><img src="principal/logo-horizontal.png"></div></div>
<div><h1>CORES</h1><div class=sws>{cards}</div>
<h1>FONTES</h1>
<div class=f><small>LOGO E TÍTULOS · BAGEL FAT ONE (GOOGLE FONTS)</small><p>TERCEIRÃO 2027</p></div>
<div class="f t"><small>NOMES E ASSINATURAS · SEDGWICK AVE DISPLAY (GOOGLE FONTS)</small><p>Ana · Lucas · Duda</p></div>
<h1 style="margin-top:60px">ELEMENTOS</h1>
<svg viewBox="0 0 1200 260" width="1050">{el}</svg>
<div style="display:flex;gap:40px;margin-top:40px;align-items:center"><img src="principal/simbolo-3.png" style="width:300px"><img src="principal/ano-vertical.png" style="height:420px"></div>
</div></div></div></body></html>"""
(A / "_painel.html").write_text(html)
subprocess.run(["node", str(AQUI.parent / "tools/html-to-png.js"), str(A / "_painel.html"), str(A / "painel-identidade.png"), "2400", "1500", "1"], check=True)
(A / "_painel.html").unlink(); print("ok")
