"""Kit da identidade em cada letra favorita: linha única, peito (3 + capelo), manga (2027 vertical),
forro de nomes, e um painel juntando tudo com a arte das costas (costas.py).

uso: python3 identidade.py [numero ...]   -> identidade/<n>-<fonte>/{horizontal,peito,manga,forro}.png
                                             + identidade/<n>-<fonte>/painel.jpg + identidade/todos.jpg
As peças saem com fundo transparente (prontas pra estampa no moletom preto).
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from costas import ESCOLHIDAS, ROXO, CLARO, ESCURO, UVA, FD, AQUI

OUT = AQUI / "identidade"
NOMES = ["Ana", "Lucas", "Bia", "Pedro", "Júlia", "Gabi", "Rafa", "Duda", "Theo", "Lari", "Mari", "Caio",
         "Isa", "Lelê", "Vini", "Nina", "Gui", "Malu", "Enzo", "Sofia"]  # EXEMPLO: trocar pela lista da turma

CSS = f"""
html,body{{margin:0;overflow:hidden;background:transparent}}
.it{{position:absolute;left:0;top:0;font-family:G;white-space:nowrap;line-height:1;font-size:300px}}
.it span{{position:absolute;left:-.5em;top:0;padding:0 .5em;white-space:nowrap}}
.l1{{-webkit-text-stroke:.15em #fff;color:#fff;paint-order:stroke fill;
     filter:drop-shadow(.018em .021em 0 {UVA}) drop-shadow(.018em .021em 0 {UVA}) drop-shadow(.015em .018em 0 #000)}}
.l2{{-webkit-text-stroke:.075em #0A0A0C;color:#0A0A0C;paint-order:stroke fill}}
.l3{{background:linear-gradient(180deg,{CLARO} 0%,{ROXO} 50%,{ESCURO} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.l4{{color:transparent;background:linear-gradient(180deg,rgba(255,255,255,.55) 0 11%,transparent 11.5%);-webkit-background-clip:text;background-clip:text;opacity:.6}}
.branco .l3{{background:#fff;-webkit-background-clip:text;background-clip:text}} .branco .l1{{filter:drop-shadow(.02em .024em 0 {ROXO})}}
.chapado span:not(.l3){{display:none}} .chapado .l3{{background:{ROXO};-webkit-background-clip:text;background-clip:text}}
.fantasma{{visibility:hidden;position:static!important;padding:0!important}}
.st{{position:absolute;width:var(--s);height:var(--s);background:var(--c);
     clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%)}}
"""

# JS: cada item {t, cx, cy, w|h (tamanho do desenho), rot, til, cls}
JS = r"""
document.fonts.load('300px G').then(()=>document.fonts.ready).then(()=>{
 const cv=document.createElement('canvas').getContext('2d');
 const med=(t,fs)=>{cv.font=fs+'px G';const m=cv.measureText(t);return {L:m.actualBoundingBoxLeft,R:m.actualBoundingBoxRight,
   A:m.actualBoundingBoxAscent,D:m.actualBoundingBoxDescent,FA:m.fontBoundingBoxAscent,FD:m.fontBoundingBoxDescent,W:m.width}};
 ITENS.forEach(o=>{
   const t=o.til?o.t.replace('Ã','A'):o.t;
   let m=med(t,300), fs=o.w?300*o.w/(m.L+m.R):300*o.h/(m.A+m.D); m=med(t,fs);
   const d=document.createElement('div'); d.className='it '+(o.cls||''); d.style.fontSize=fs+'px';
   const lay=o.cls&&o.cls.includes('chapado')?['l3']:['l1','l2','l3','l4'];
   d.innerHTML='<span class=fantasma>'+t+'</span>'+lay.map(c=>'<span class='+c+'>'+t+'</span>').join('');
   const base=(fs-(m.FA+m.FD))/2+m.FA;
   d.style.left=(o.cx-(m.R-m.L)/2)+'px'; d.style.top=(o.cy-base+(m.A-m.D)/2)+'px';
   d.style.transform='rotate('+(o.rot||0)+'deg)'; d.style.transformOrigin=((m.R-m.L)/2)+'px '+(base-(m.A-m.D)/2)+'px';
   document.body.appendChild(d);
   if(o.til){ // til grafitado à mão por cima do A
     const i=t.indexOf('A'), pre=t.slice(0,i), wpre=med(pre,fs).W, wa=med(pre+'A',fs).W, ax=(wpre+wa)/2;
     cv.font=fs+'px G'; const aA=cv.measureText('A').actualBoundingBoxAscent;
     const k=(wa-wpre)/330, p='M-150 40 C-140 -60 -60 -90 0 -20 C40 25 80 30 110 -50 L165 -25 C150 90 60 110 0 40 C-40 -5 -80 -10 -95 65 Z';
     const chap=lay.length==1;
     d.insertAdjacentHTML('beforeend',`<svg style="position:absolute;z-index:5;overflow:visible;left:${ax}px;top:${base-aA-fs*0.13}px" width=1 height=1>
      <defs><linearGradient id=gt x1=0 y1=-90 x2=0 y2=110 gradientUnits=userSpaceOnUse><stop offset=0 stop-color="#E4CFF7"/><stop offset=.5 stop-color="#996BB3"/><stop offset=1 stop-color="#7A4C99"/></linearGradient></defs>
      <g transform="scale(${k}) rotate(-6)" stroke-linejoin=round>${chap?`<path d="${p}" fill="#996BB3"/>`:
      `<path d="${p}" fill="#3E2353" stroke="#3E2353" stroke-width="78" transform="translate(18 21)"/>
      <path d="${p}" fill="#fff" stroke="#fff" stroke-width="78"/><path d="${p}" fill="#0A0A0C" stroke="#0A0A0C" stroke-width="39"/>
      <path d="${p}" fill="url(#gt)"/>`}</g></svg>`);
   }
 });
});
"""


def pagina(fonte, W, H, itens, extra=""):
    return (f"<!doctype html><html><head><meta charset=utf-8><style>@font-face{{font-family:G;src:url('{FD}/{fonte}')}}"
            f"{CSS}html,body{{width:{W}px;height:{H}px}}</style></head><body>{extra}"
            f"<script>const ITENS={json.dumps(itens, ensure_ascii=False)};{JS}</script></body></html>")


def capelo(x, y, w):
    """chapéu de formatura em SVG (branco + roxo, contorno preto)"""
    return f"""<svg style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{w}" viewBox="-100 -100 200 200">
<g transform="rotate(14)" stroke-linejoin="round" stroke-linecap="round">
<path d="M-62 2 L-62 40 Q0 70 62 40 L62 2Z" fill="{ROXO}" stroke="#fff" stroke-width="30"/>
<path d="M-100 -10 L0 -52 L100 -10 L0 32Z" fill="#fff" stroke="#fff" stroke-width="30"/>
<path d="M-62 2 L-62 40 Q0 70 62 40 L62 2Z" fill="{ROXO}" stroke="#0A0A0C" stroke-width="12"/>
<path d="M-100 -10 L0 -52 L100 -10 L0 32Z" fill="#F3EAFB" stroke="#0A0A0C" stroke-width="12"/>
<path d="M0 -10 L72 2 L76 62" fill="none" stroke="#0A0A0C" stroke-width="14"/><path d="M0 -10 L72 2 L76 62" fill="none" stroke="{ROXO}" stroke-width="6"/>
<circle cx="76" cy="70" r="13" fill="{ROXO}" stroke="#0A0A0C" stroke-width="7"/><circle cx="0" cy="-10" r="8" fill="#0A0A0C"/></g></svg>"""


def estrelas(lista):
    return "".join(f'<i class=st style="--s:{s}px;--c:{c};left:{x}px;top:{y}px"></i>' for x, y, s, c in lista)


def pecas(fonte, til):
    return {
        "horizontal": (2400, 860, [
            dict(t="TERCEIRÃO", cx=1200, cy=430, w=2050, rot=-4, til=til),
            dict(t="2027", cx=1820, cy=730, h=120, rot=-4, cls="branco"),
        ], estrelas([(70, 90, 70, "#fff"), (2280, 130, 50, ROXO), (2300, 600, 44, "#fff"), (120, 560, 36, ROXO)])),
        "peito": (900, 900, [dict(t="3", cx=430, cy=500, h=600, rot=-6)],
                  capelo(470, 40, 330) + estrelas([(90, 170, 70, "#fff"), (760, 720, 52, ROXO), (120, 760, 36, "#fff")])),
        "manga": (420, 1500, [dict(t=c, cx=210 + (18 if i % 2 else -18), cy=230 + i * 340, h=270, rot=(6 if i % 2 else -6), cls="branco")
                              for i, c in enumerate("2027")],
                  estrelas([(40, 40, 50, "#fff"), (330, 1420, 44, ROXO)])),
        "forro": (2400, 900, [dict(t=n, cx=150 + (k % 6) * 400 + (100 if (k // 6) % 2 else 0), cy=110 + (k // 6) * 220,
                                   h=95, rot=(-8, 4, -3, 7, -6, 2)[k % 6], cls="chapado") for k, n in enumerate(NOMES * 2)][:24], ""),
    }


def render(html, W, H, png, transparente=True):
    h = png.with_suffix(".html")
    h.write_text(html)
    subprocess.run(["node", str(AQUI.parent / "tools/html-to-png-exato.js"), str(h), str(png), str(W), str(H), "1",
                    "t" if transparente else ""], check=True)
    h.unlink()


def painel(n, f, nome, pasta):
    """painel no preto: costas grande à esquerda + peças à direita"""
    W, H = 3000, 1800
    c = Image.new("RGB", (W, H), "#0A0A0C")
    def cola(arq, box, pos):
        im = Image.open(arq).convert("RGBA"); im.thumbnail(box); c.paste(im, pos, im); return im.size
    cola(AQUI / "costas" / f"{n:02d}-{f.split('.')[0]}-transparente.png", (1250, 1500), (60, 220))
    cola(pasta / "horizontal.png", (1550, 500), (1380, 200))
    cola(pasta / "peito.png", (560, 560), (1400, 720))
    cola(pasta / "manga.png", (220, 790), (2000, 690))
    fo = Image.open(pasta / "forro.png").convert("RGBA"); fo.thumbnail((700, 263))
    c.paste(fo, (2250, 760), fo)
    d = ImageDraw.Draw(c)
    try:
        ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    except OSError:
        ft = fs = ImageFont.load_default()
    d.text((70, 60), f"{n:02d}  {nome.upper()}", font=ft, fill="#FFFFFF")
    d.text((70, 125), f"TERCEIRÃO 2027 · MÃE DE DEUS · fonte {f.split('.')[0].replace('_', ' ')}", font=fs, fill="#8d7f99")
    for txt, xy in [("COSTAS", (70, 1730)), ("LINHA ÚNICA", (1400, 160)), ("PEITO", (1400, 1310)),
                    ("MANGA", (2000, 1500)), ("FORRO DO CAPUZ (nomes de exemplo)", (2250, 1050))]:
        d.text(xy, txt, font=fs, fill="#996BB3")
    c.save(pasta / "painel.jpg", quality=88)
    return pasta / "painel.jpg"


if __name__ == "__main__":
    filtro = {int(a) for a in sys.argv[1:]}
    paineis = []
    for n, f, nome, til in ESCOLHIDAS:
        if filtro and n not in filtro:
            continue
        pasta = OUT / f"{n:02d}-{f.split('.')[0]}"
        pasta.mkdir(parents=True, exist_ok=True)
        for peca, (W, H, itens, extra) in pecas(f, til).items():
            render(pagina(f, W, H, itens, extra), W, H, pasta / f"{peca}.png")
        paineis.append(painel(n, f, nome, pasta)); print("ok", pasta.name)
    if not filtro:
        col = 2; lin = (len(paineis) + 1) // 2
        c = Image.new("RGB", (1500 * col, 900 * lin), "#0A0A0C")
        for k, p in enumerate(paineis):
            c.paste(Image.open(p).resize((1500, 900)), ((k % col) * 1500, (k // col) * 900))
        c.save(OUT / "todos.jpg", quality=85)
