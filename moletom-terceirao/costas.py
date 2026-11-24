"""Arte das costas: TER / CEI / RÃO empilhado + 2027 + MÃE DE DEUS, com as letras escolhidas.

uso: python3 costas.py [arquivo-da-fonte ...]  -> costas/<n>-<fonte>.png (1500x1800, fundo preto)
                                                 + costas/<n>-<fonte>-transparente.png (pra estampa)
"""
import subprocess, sys
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).parent
OUT = AQUI / "costas"
OUT.mkdir(exist_ok=True)
FD = (AQUI / "fontes/dafont").resolve().as_uri()
ROXO, CLARO, ESCURO, UVA = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353"

ESCOLHIDAS = [  # (número do modelo, fonte, nome, til à mão)
    (1, "beat_mark.ttf", "Bloco clássico", True),
    (2, "urban_blocker.ttf", "Bolha", True),
    (4, "graffiti_youth.otf", "Bloco gordo", True),
    (9, "grime_slime.ttf", "Old school", False),
    (12, "break_rebel.ttf", "Wild leve", True),   # True = til desenhado à mão (o da fonte vira bolha)
    (26, "street_shade.ttf", "Bloco inclinado", False),
    (29, "thomas_2.otf", "Bloco pesado", False),
]

LINHAS = [("TER", -6, -40), ("CEI", -3, 40), ("RÃO", -5, -10)]  # texto, giro, deslocamento x


def html(fonte, fundo=True, til=False):
    LN = [(t.replace('Ã', 'A') if til else t, r, dx) for t, r, dx in LINHAS]
    camadas = lambda t: "".join(f'<span class="{c}">{t}</span>' for c in ("l1", "l2", "l3", "l4"))
    linhas = "".join(
        f'<div class=ln data-t="{t}" data-rot="{r}" data-dx="{dx}"><span class=fantasma>{t}</span>{camadas(t)}</div>'
        for t, r, dx in LN)
    bg = ("background:radial-gradient(ellipse 60% 45% at 50% 45%,#1E1229 0%,#0A0A0C 72%)" if fundo
          else "background:transparent")
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:G;src:url('{FD}/{fonte}')}}
html,body{{margin:0;width:1500px;height:1800px;overflow:hidden;{bg}}}
.ln{{position:absolute;left:0;top:0;font-family:G;white-space:nowrap;line-height:1;font-size:400px}}
.ln span{{position:absolute;left:0;top:0;white-space:nowrap}}
.l1{{-webkit-text-stroke:.15em #fff;color:#fff;paint-order:stroke fill;
     filter:drop-shadow(7px 8px 0 {UVA}) drop-shadow(7px 8px 0 {UVA}) drop-shadow(6px 7px 0 {UVA}) drop-shadow(5px 6px 0 #000)}}
.l2{{-webkit-text-stroke:.075em #0A0A0C;color:#0A0A0C;paint-order:stroke fill}}
.l3{{background:linear-gradient(180deg,{CLARO} 0%,{ROXO} 50%,{ESCURO} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.l4{{color:transparent;background:linear-gradient(180deg,rgba(255,255,255,.55) 0 11%,transparent 11.5%);-webkit-background-clip:text;background-clip:text;opacity:.6}}
.fantasma{{visibility:hidden;position:static!important}}
.ano{{position:absolute;font-family:G;font-size:170px;color:#fff;-webkit-text-stroke:.15em #0A0A0C;paint-order:stroke fill;
      filter:drop-shadow(6px 7px 0 {ROXO});transform:rotate(-5deg)}}
.esc{{position:absolute;font:700 40px/1 Arial,sans-serif;letter-spacing:.45em;color:{ROXO};transform:rotate(-5deg)}}
.st{{position:absolute;width:var(--s);height:var(--s);background:var(--c);
     clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%)}}
</style></head><body>
{linhas}
<div class=ano id=ano>2027</div><div class=esc id=esc>MÃE DE DEUS</div>
<i class=st style="--s:90px;--c:#fff;left:120px;top:250px"></i>
<i class=st style="--s:60px;--c:{ROXO};left:1310px;top:200px"></i>
<i class=st style="--s:70px;--c:#fff;left:1330px;top:1000px"></i>
<i class=st style="--s:44px;--c:{ROXO};left:110px;top:1150px"></i>
<i class=st style="--s:50px;--c:#fff;left:1250px;top:1560px"></i>
<script>
document.fonts.ready.then(()=>{{
  const ls=[...document.querySelectorAll('.ln')];
  const cv=document.createElement('canvas').getContext('2d');
  const med=(t,fs)=>{{cv.font=fs+'px G';const m=cv.measureText(t);return {{
    L:m.actualBoundingBoxLeft,R:m.actualBoundingBoxRight,A:m.actualBoundingBoxAscent,D:m.actualBoundingBoxDescent,
    FA:m.fontBoundingBoxAscent,FD:m.fontBoundingBoxDescent}};}};
  const LARG=860, SOBRE=0.06;   // largura do desenho de cada linha e quanto uma linha encosta na outra
  let info=ls.map(l=>{{const t=l.dataset.t;let m=med(t,400);const fs=400*LARG/(m.L+m.R);return {{l,t,fs,m:med(t,fs)}};}});
  let alt0=info.map(o=>o.m.A+o.m.D).reduce((a,b)=>a+b,0)*(1-SOBRE);
  const k=Math.min(1,1180/alt0);   // se ficar alto demais, encolhe tudo junto
  info=info.map(o=>{{const fs=o.fs*k;return {{...o,fs,m:med(o.t,fs)}};}});
  const alturas=info.map(o=>o.m.A+o.m.D);
  const total=alturas.reduce((a,b)=>a+b,0)*(1-SOBRE)+alturas[2]*SOBRE;
  let y=(1420-total)/2+40;  // bloco centrado entre 150 e ~1420
  info.forEach((o,i)=>{{const {{l,fs,m}}=o; l.style.fontSize=fs+'px';
    const base=(fs-(m.FA+m.FD))/2+m.FA;           // linha de base dentro da caixa (line-height 1)
    l.style.top=(y-(base-m.A))+'px';
    l.style.left=(750-(m.R-m.L)/2+(+l.dataset.dx))+'px';
    l.style.transform=`rotate(${{l.dataset.rot}}deg)`;
    y+=(m.A+m.D)*(1-SOBRE);}});
  const ano=document.getElementById('ano'), esc=document.getElementById('esc');
  const fim=y+alturas[2]*SOBRE;
  const ar=ano.getBoundingClientRect(), er=esc.getBoundingClientRect();
  ano.style.left=(750-ar.width/2+40)+'px'; ano.style.top=(fim+10)+'px';
  esc.style.left=(750-er.width/2+40)+'px'; esc.style.top=(fim+20+ar.height*0.95)+'px';
  if ({'true' if til else 'false'}) {{   // til grafitado por cima do A
    const o=info[2], cvw=t=>{{cv.font=o.fs+'px G';return cv.measureText(t).width;}};
    const ax=(cvw('R')+cvw('RA'))/2, base=(o.fs-(o.m.FA+o.m.FD))/2+o.m.FA;
    cv.font=o.fs+'px G'; const aA=cv.measureText('A').actualBoundingBoxAscent;
    const w=o.fs*0.58, h=w*0.3, d=`M${{-w/2}} ${{h*0.3}} C${{-w*0.32}} ${{-h*0.9}} ${{-w*0.1}} ${{-h*0.7}} 0 0 C${{w*0.1}} ${{h*0.7}} ${{w*0.32}} ${{h*0.9}} ${{w/2}} ${{-h*0.3}}`;
    const sw=h*0.85, svg=`<svg style="position:absolute;overflow:visible;left:${{ax}}px;top:${{base-aA-h*1.1}}px" width=1 height=1>
      <g transform="rotate(-8)" fill=none stroke-linecap=round>
      <path d="${{d}}" stroke="{UVA}" stroke-width="${{sw+o.fs*0.15}}" transform="translate(7 8)"/>
      <path d="${{d}}" stroke="#fff" stroke-width="${{sw+o.fs*0.15}}"/>
      <path d="${{d}}" stroke="#0A0A0C" stroke-width="${{sw+o.fs*0.075}}"/>
      <path d="${{d}}" stroke="{ROXO}" stroke-width="${{sw}}"/>
      <path d="${{d}}" stroke="{CLARO}" stroke-width="${{sw*0.25}}" transform="translate(0 ${{-sw*0.2}})" opacity=.7/></g></svg>`;
    o.l.insertAdjacentHTML('beforeend', svg);
  }}
}});
</script></body></html>"""


def render(h, png):
    subprocess.run(["node", str(AQUI.parent / "tools/html-to-png.js"), str(h), str(png), "1500", "1800", "1",
                    "" if "transparente" not in png.name else "t"], check=True)


if __name__ == "__main__":
    pngs = []
    for n, f, nome, til in ESCOLHIDAS:
        if sys.argv[1:] and f not in sys.argv[1:]:
            continue
        base = f"{n:02d}-{f.split('.')[0]}"
        for fundo, suf in ((True, ""), (False, "-transparente")):
            h = OUT / f"_{base}.html"
            h.write_text(html(f, fundo, til))
            png = OUT / f"{base}{suf}.png"
            render(h, png); h.unlink()
        pngs.append(OUT / f"{base}.png"); print("ok", base)
    col = 4
    lin = (len(pngs) + col - 1) // col
    c = Image.new("RGB", (750 * col, 900 * lin), "#0A0A0C")
    for k, p in enumerate(pngs):
        c.paste(Image.open(p).convert("RGB").resize((750, 900)), ((k % col) * 750, (k // col) * 900))
    c.save(OUT / "comparar.jpg", quality=88)
