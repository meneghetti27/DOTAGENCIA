#!/usr/bin/env python3
"""Gerador de carrossel da dot (método oficial: cena + título League Gothic + recorte na frente).

Uso: python3 tools/carrossel.py designs/<pasta>/slides.json
O JSON tem {"total": N, "medidor": [...rótulos...] | null, "slides": [ {...}, ... ]}. Campos de cada slide:
  arquivo          nome de saída (sem extensão)
  cena             imagem de fundo 1080x1350 (relativa à pasta do JSON)
  recorte          (opcional) PNG transparente 1080x1350 que fica NA FRENTE do título
  escurecer_topo   0–1, degradê escuro atrás do título (padrão 0.75)
  rotulo           linha pequena acima do título (ex.: "NÍVEL 01 · A PONTA")
  l1, l2           linhas do título; use {b1}X{/b} ou {b2}X{/b} para desfocar letras
  topo_titulo      posição y do título (padrão 190)
  tam1, tam2       tamanhos das linhas (padrão 178 / 206)
  frase            frase de baixo (HTML; <b> branco, <b class=bl> azul)
  rodape           texto pequeno em caixa alta
  medidor          índice ativo do medidor (ou null)
  anotacoes        [{"x":..,"y":..,"lx":..,"ly":..,"texto":".."}]  ponto → rótulo (HUD)
  particulas       "bolhas" | "faiscas" | null
  extra_html       HTML livre (ex.: botão de CTA)
"""
import json, os, re, sys, random

TPL = r"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=League+Gothic&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;background:#04050A;font-family:Inter,sans-serif;color:#fff;position:relative}
.layer{position:absolute;inset:0}
.scene{background:url(%(cena)s) center/cover}
.top{z-index:1;background:linear-gradient(180deg,rgba(3,5,14,%(esc)s) 0%%,rgba(3,5,14,%(esc2)s) 28%%,rgba(3,5,14,0) 52%%)}
.cut{background:url(%(recorte)s) center/cover;z-index:4}
.head{position:absolute;top:56px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:12px;z-index:8}
.ico{width:44px;height:44px;border-radius:50%%;background:#0B1230;border:1.5px solid rgba(120,160,255,.5);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;letter-spacing:-.05em;box-shadow:0 0 18px rgba(61,110,245,.5)}
.ico i{font-style:normal;color:#3D6EF5}
.who{line-height:1.15}.who b{font-weight:700;font-size:21px;display:flex;align-items:center;gap:7px}.who b svg{width:18px;height:18px}
.who span{font-size:16px;color:#B9C1D6}
.rot{position:absolute;top:%(rot_y)spx;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:14px;z-index:3;font-size:17px;font-weight:600;letter-spacing:.32em;color:#9DB5FF}
.rot:before,.rot:after{content:"";width:46px;height:1.5px;background:linear-gradient(90deg,transparent,#6E98FF)}
.rot:after{transform:scaleX(-1)}
.title{position:absolute;top:%(topo)spx;left:0;right:0;text-align:center;font-family:"League Gothic";text-transform:uppercase;z-index:3;line-height:.86}
.l1,.l2{display:block;white-space:nowrap}
.l1{font-size:%(tam1)spx;color:#fff;letter-spacing:.01em;text-shadow:0 0 30px rgba(120,160,255,.35),0 4px 30px rgba(0,0,0,.5)}
.l2{font-size:%(tam2)spx;letter-spacing:.005em}
.l2 span{background:linear-gradient(90deg,#DCE6FF 12%%,#8FB0FF 38%%,#4F80FF 66%%,#3D6EF5 90%%);background-size:1080px 100%%;background-attachment:fixed;-webkit-background-clip:text;background-clip:text;color:transparent}
.b1{filter:blur(2.5px)}.b2{filter:blur(4px)}
.glow2{position:absolute;top:%(glow_y)spx;left:0;right:0;text-align:center;font-family:"League Gothic";font-size:%(tam2)spx;line-height:.86;color:#3D6EF5;opacity:.6;filter:blur(30px);z-index:2;text-transform:uppercase;white-space:nowrap}
.tools{position:absolute;left:58px;top:300px;display:flex;flex-direction:column;gap:16px;z-index:8;opacity:.7}
.tools svg{width:18px;height:18px;stroke:#E2E8FF;fill:none;stroke-width:1.6}
.parts{z-index:6}
.parts i{position:absolute;border-radius:50%%}
.parts i.f{background:#DDE6FF;box-shadow:0 0 8px 2px rgba(110,155,255,.95)}
.parts i.bo{border:1.5px solid rgba(200,220,255,.7);background:radial-gradient(circle at 35%% 30%%,rgba(255,255,255,.55),rgba(150,190,255,.05) 60%%);box-shadow:0 0 6px rgba(120,160,255,.4)}
.parts i.blur{filter:blur(2px);opacity:.6}
.hud{z-index:7}
.hud .lb{position:absolute;transform:translate(-50%%,-50%%);white-space:nowrap;font-size:17px;font-weight:600;letter-spacing:.04em;padding:9px 16px;border-radius:99px;background:rgba(8,14,36,.72);border:1px solid rgba(143,176,255,.5);box-shadow:0 0 18px rgba(61,110,245,.35);backdrop-filter:blur(6px)}
.hud .lb b{color:#8FB0FF;font-weight:700}
.fade{z-index:5;background:linear-gradient(180deg,transparent 72%%,rgba(3,5,14,.75) 86%%,rgba(3,5,14,.95) 100%%)}
.frase{position:absolute;left:70px;right:70px;bottom:62px;text-align:center;z-index:8;font-size:29px;line-height:1.3;color:#D9DEEA;text-shadow:0 2px 12px rgba(0,0,0,.6)}
.frase b{font-weight:800;color:#fff}.frase b.bl{color:#8FB0FF}
.foot{position:absolute;left:0;right:0;bottom:26px;text-align:center;font-size:14px;letter-spacing:.16em;color:#7A8194;z-index:8}
.count{position:absolute;top:62px;right:58px;z-index:8;font-size:18px;font-weight:600;padding:8px 16px;border-radius:99px;background:rgba(10,16,40,.7);border:1px solid rgba(143,176,255,.35)}
.gauge{position:absolute;right:58px;top:640px;height:500px;width:120px;z-index:8;font-size:15px;font-weight:600;letter-spacing:.08em;color:#8E9CC0}
.gauge .ln{position:absolute;right:0;top:0;bottom:0;width:2px;background:linear-gradient(#8FB0FF,rgba(143,176,255,.12))}
.gauge .tk{position:absolute;right:0;display:flex;align-items:center;gap:10px;transform:translateY(-50%%);white-space:nowrap}
.gauge .tk:after{content:"";width:14px;height:2px;background:#8FB0FF}
.gauge .on{color:#fff;font-size:17px}.gauge .on:after{width:24px;height:3px;background:#fff;box-shadow:0 0 12px #6E98FF}
.gauge .dotm{position:absolute;right:-6px;width:14px;height:14px;border-radius:50%%;background:#fff;box-shadow:0 0 16px 4px #3D6EF5;transform:translateY(-50%%)}
.vig{z-index:5;background:radial-gradient(120%% 90%% at 50%% 45%%,transparent 60%%,rgba(0,0,0,.45) 100%%)}
</style></head><body>
<div class="layer scene"></div>
<div class="layer top"></div>
%(rotulo)s
<div class="glow2">%(l2txt)s</div>
<div class="title"><span class="l1">%(l1)s</span><span class="l2">%(l2)s</span></div>
%(cut)s
<div class="layer fade"></div>
<div class="layer vig"></div>
<div class="layer parts">%(parts)s</div>
<svg class="layer hud" width="1080" height="1350" style="position:absolute;inset:0;z-index:7">%(hud_svg)s</svg>
<div class="layer hud">%(hud_lb)s</div>
<div class="head"><div class="ico">dot<i>.</i></div><div class="who"><b>Agência dot.
<svg viewBox="0 0 24 24"><path fill="#3D8BFF" d="M12 1l2.6 2.2 3.4-.4.9 3.3 3 1.7-1.2 3.2 1.2 3.2-3 1.7-.9 3.3-3.4-.4L12 23l-2.6-2.2-3.4.4-.9-3.3-3-1.7 1.2-3.2L2.1 9.8l3-1.7.9-3.3 3.4.4z"/><path d="M7.5 12.2l3 3 6-6.2" stroke="#fff" stroke-width="2.2" fill="none"/></svg></b>
<span>@marketingdotagency</span></div></div>
<div class="count">%(n)s/%(total)s</div>
<div class="tools">
<svg viewBox="0 0 24 24"><path d="M12 3v18M3 12h18"/></svg><svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="1" stroke-dasharray="3 2"/></svg>
<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M16 16l5 5"/></svg><svg viewBox="0 0 24 24"><path d="M5 3l12 9-6 1-3 6z"/></svg>
<svg viewBox="0 0 24 24"><path d="M6 4h12M12 4v16"/></svg><svg viewBox="0 0 24 24"><path d="M4 20l4-1 11-11-3-3L5 16z"/></svg></div>
%(gauge)s
%(extra)s
<div class="frase">%(frase)s</div>
<div class="foot">%(rodape)s</div>
<script>document.fonts.ready.then(()=>{for(const sel of ['.l1','.l2']){const el=document.querySelector('.title '+sel);let fs=parseFloat(getComputedStyle(el).fontSize);
el.style.display='inline-block';while(el.getBoundingClientRect().width>880&&fs>90){fs-=2;el.style.fontSize=fs+'px';}el.style.display='block';
if(sel=='.l2'){const g=document.querySelector('.glow2');g.style.fontSize=fs+'px';}}
const t=document.querySelector('.title'),g=document.querySelector('.glow2'),l1=document.querySelector('.title .l1');g.style.top=(t.offsetTop+l1.offsetHeight)+'px';document.body.dataset.ok=1;});</script>
</body></html>"""


def letras(t):
    """Divide o texto em <span>s (cada pedaço recebe o degradê da linha 2); {b1}..{/b} e {b2}..{/b} desfocam."""
    out = []
    for cls, txt in _partes(t):
        out.append(f'<span class="{cls}">{txt}</span>' if cls else f"<span>{txt}</span>")
    return "".join(out)


def _partes(t):
    partes, i = [], 0
    for m in re.finditer(r"\{(b\d)\}(.*?)\{/b\}", t):
        if m.start() > i:
            partes.append(("", t[i:m.start()]))
        partes.append((m.group(1), m.group(2))); i = m.end()
    if i < len(t):
        partes.append(("", t[i:]))
    return partes


def particulas(tipo, seed):
    rnd = random.Random(seed); out = []
    if tipo == "bolhas":
        for _ in range(26):
            s = rnd.choice([4, 6, 8, 10, 14, 18]); x = rnd.randint(150, 930); y = rnd.randint(170, 1100)
            out.append(f'<i class="bo{" blur" if s >= 14 and rnd.random() < .5 else ""}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"></i>')
    elif tipo == "faiscas":
        for _ in range(18):
            s = rnd.choice([3, 3, 4, 5, 8]); x = rnd.randint(120, 960); y = rnd.randint(200, 700)
            out.append(f'<i class="f{" blur" if s >= 8 else ""}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"></i>')
    return "".join(out)


def build(cfg_path):
    base = os.path.dirname(os.path.abspath(cfg_path)); cfg = json.load(open(cfg_path))
    total = cfg.get("total", len(cfg["slides"])); med = cfg.get("medidor")
    for i, s in enumerate(cfg["slides"], 1):
        topo = s.get("topo_titulo", 190); t1 = s.get("tam1", 178); t2 = s.get("tam2", 206)
        esc = s.get("escurecer_topo", 0.75)
        svg, lbs = [], []
        for a in s.get("anotacoes", []):
            x, y, lx, ly = a["x"], a["y"], a["lx"], a["ly"]
            mx = lx
            svg.append(f'<path d="M{x} {y} L{mx} {y if abs(ly-y)<4 else ly}" stroke="#8FB0FF" stroke-width="1.6" fill="none" opacity=".9"/>'
                       if abs(ly - y) < 4 else
                       f'<path d="M{x} {y} L{x + (lx - x) * 0.35} {ly} L{lx} {ly}" stroke="#8FB0FF" stroke-width="1.6" fill="none" opacity=".9"/>')
            svg.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff"/><circle cx="{x}" cy="{y}" r="16" fill="none" stroke="#8FB0FF" stroke-width="1.5" opacity=".8"/>'
                       f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="#8FB0FF" stroke-width="1" opacity=".35"/>')
            lbs.append(f'<div class="lb" style="left:{lx}px;top:{ly}px">{a["texto"]}</div>')
        gauge = ""
        if med is not None and s.get("medidor") is not None:
            k = s["medidor"]; n = len(med)
            ticks = "".join(f'<div class="tk{" on" if j == k else ""}" style="top:{j / (n - 1) * 100:.1f}%">{m}</div>' for j, m in enumerate(med))
            gauge = f'<div class="gauge"><div class="ln"></div>{ticks}<div class="dotm" style="top:{k / (n - 1) * 100:.1f}%"></div></div>'
        l2txt = re.sub(r"\{/?b\d?\}", "", s["l2"])
        html = TPL % dict(
            cena=s["cena"], recorte=s.get("recorte", ""), esc=esc, esc2=round(esc * 0.75, 2),
            rot_y=topo - 34, topo=topo, tam1=t1, tam2=t2, glow_y=topo + int(t1 * 0.86),
            rotulo=f'<div class="rot">{s["rotulo"]}</div>' if s.get("rotulo") else "",
            l1=letras(s["l1"]), l2=letras(s["l2"]),
            l2txt=l2txt, cut=f'<div class="layer cut"></div>' if s.get("recorte") else "",
            parts=particulas(s.get("particulas"), i), hud_svg="".join(svg), hud_lb="".join(lbs),
            n=i, total=total, gauge=gauge, extra=s.get("extra_html", ""), frase=s.get("frase", ""), rodape=s.get("rodape", ""))
        open(os.path.join(base, s["arquivo"] + ".html"), "w").write(html)
    # render
    import subprocess
    js = r"""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const f of process.argv.slice(1)){await p.goto('file://'+f);await p.waitForFunction(()=>document.body.dataset.ok==='1');await p.waitForTimeout(400);await p.screenshot({path:f.replace(/\.html$/,'.png')});}await b.close();})();"""
    files = [os.path.join(base, s["arquivo"] + ".html") for s in cfg["slides"] if not sys.argv[2:] or s["arquivo"] in sys.argv[2:]]
    subprocess.run(["node", "-e", js, *files], check=True)
    print("ok", len(files), "slides")


if __name__ == "__main__":
    build(sys.argv[1])
