"""Arte das costas: TER / CEI / RÃO empilhado + 2027 + MÃE DE DEUS, com as letras escolhidas.

uso: python3 costas.py [arquivo-da-fonte ...]  -> costas/<n>-<fonte>.png (1500x1800, fundo preto)
                                                 + costas/<n>-<fonte>-transparente.png (pra estampa)
"""
import json, subprocess, sys
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

GAP = 0.02
TIL_D = 'M-150 40 C-140 -60 -60 -90 0 -20 C40 25 80 30 110 -50 L165 -25 C150 90 60 110 0 40 C-40 -5 -80 -10 -95 65 Z'
TIL_ROT, TIL_JOIN, TIL_FILL = -6, 'round', 'url(#gt)'
TIL_ESC = 1.0
ANO_FONTE, ANO_TAM = None, 170  # fonte e tamanho do 2027
ANO_ESTILO = 'branco'  # 'branco' ou 'letras' (mesmo acabamento roxo das letras)
ANO_TXT = '2027'
ANO_INT = None  # dict(txt, fam 'G'|'A', tam, ax, ay, rot, cor 'roxo'|'branco', esc_dy): ano no mesmo plano do adesivo  # respiro extra entre CEI e RÃO (fração da fonte)
LINHAS = [("TER", -5, -15), ("CEI", -3, 15), ("RÃO", -5, 140)]  # texto, giro, deslocamento x


def html(fonte, fundo=True, til=False):
    LN = [(t.replace('Ã', 'A') if til else t, r, dx) for t, r, dx in LINHAS]
    ANO_HTML = (f'<div class="ano anoL{" anoB" if ANO_ESTILO == "letras-branco" else ""}" id=ano><span class=fantasma>{ANO_TXT}</span>' + ''.join(f'<span class={c}>{ANO_TXT}</span>' for c in ('l1','l2','l3','l4')) + '</div>') if ANO_ESTILO in ('letras', 'letras-branco') else f'<div class=ano id=ano>{ANO_TXT}</div>'
    camadas = lambda t: "".join(f'<span class="{c}">{t}</span>' for c in ("l1", "l2", "l3", "l4"))
    linhas = "".join(
        f'<div class=ln data-t="{t}" data-rot="{r}" data-dx="{dx}"><span class=fantasma>{t}</span>{camadas(t)}</div>'
        for t, r, dx in LN)
    bg = ("background:radial-gradient(ellipse 60% 45% at 50% 45%,#1E1229 0%,#0A0A0C 72%)" if fundo
          else "background:transparent")
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:G;src:url('{FD}/{fonte}')}}
@font-face{{font-family:A;src:url('{FD}/{ANO_FONTE or fonte}')}}
html,body{{margin:0;width:1500px;height:1800px;overflow:hidden;{bg}}}
.ln{{position:absolute;left:0;top:0;font-family:G;white-space:nowrap;line-height:1;font-size:400px}}
.ln span{{position:absolute;left:-.5em;top:0;padding:0 .5em;white-space:nowrap}}
.anoL{{color:transparent!important;-webkit-text-stroke:0!important;filter:none!important;line-height:1;white-space:nowrap}}
.anoB .l3{{background:none!important;color:#FFFFFF!important}} .anoB .l4{{display:none}}
.anoL span{{position:absolute;left:-.5em;top:0;padding:0 .5em;white-space:nowrap}}
.l1{{z-index:1;-webkit-text-stroke:.15em #fff;color:#fff;paint-order:stroke fill;
     filter:drop-shadow(7px 8px 0 {UVA}) drop-shadow(7px 8px 0 {UVA}) drop-shadow(6px 7px 0 {UVA}) drop-shadow(5px 6px 0 #000)}}
.l2{{z-index:2;-webkit-text-stroke:.075em #0A0A0C;color:#0A0A0C;paint-order:stroke fill}}
.l3{{z-index:3;background:linear-gradient(180deg,{CLARO} 0%,{ROXO} 50%,{ESCURO} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.l4{{z-index:4;color:transparent;background:linear-gradient(180deg,rgba(255,255,255,.55) 0 11%,transparent 11.5%);-webkit-background-clip:text;background-clip:text;opacity:.6}}
.fantasma{{visibility:hidden;position:static!important;padding:0!important}}
.ano{{position:absolute;font-family:A;font-size:{ANO_TAM}px;color:#fff;-webkit-text-stroke:.15em #0A0A0C;paint-order:stroke fill;
      filter:drop-shadow(6px 7px 0 {ROXO});transform:rotate(-5deg)}}
.esc{{position:absolute;font:700 40px/1 Arial,sans-serif;letter-spacing:.45em;color:{ROXO};transform:rotate(-5deg)}}
.st{{position:absolute;width:var(--s);height:var(--s);background:var(--c);
     clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%)}}
</style></head><body>
{linhas}
{ANO_HTML}<div class=esc id=esc>MÃE DE DEUS</div>
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
  const TIL={'true' if til else 'false'};
  const LARG=860, SOBRE=0.0;   // largura do desenho de cada linha e quanto uma linha encosta na outra
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
    y+=(m.A+m.D)*(1-SOBRE)+(i==1&&TIL?info[2].fs*{GAP}:0);}});
  const ano=document.getElementById('ano'), esc=document.getElementById('esc');
  const fim=y+alturas[2]*SOBRE;
  const ar=ano.getBoundingClientRect(), er=esc.getBoundingClientRect();
  ano.style.left=(750-ar.width/2+40)+'px'; ano.style.top=(fim+10)+'px';
  esc.style.left=(750-er.width/2+40)+'px'; esc.style.top=(fim+20+ar.height*0.95)+'px';
  if ({'true' if til else 'false'}) {{   // til grafitado por cima do A
    const o=info[2], cvw=t=>{{cv.font=o.fs+'px G';return cv.measureText(t).width;}};
    const ax=(cvw('R')+cvw('RA'))/2, base=(o.fs-(o.m.FA+o.m.FD))/2+o.m.FA;
    cv.font=o.fs+'px G'; const aA=cv.measureText('A').actualBoundingBoxAscent;
    // til gordo preenchido (mesmo acabamento das letras)
    const k=o.fs/520*{TIL_ESC}, d='{TIL_D}';
    const svg=`<svg style="position:absolute;z-index:5;overflow:visible;left:${{ax}}px;top:${{base-aA-o.fs*0.15}}px" width=1 height=1>
      <defs><linearGradient id=gt x1=0 y1=-90 x2=0 y2=110 gradientUnits=userSpaceOnUse><stop offset=0 stop-color="{CLARO}"/><stop offset=.5 stop-color="{ROXO}"/><stop offset=1 stop-color="{ESCURO}"/></linearGradient></defs>
      <g transform="scale(${{k}}) rotate({TIL_ROT})" stroke-linejoin={TIL_JOIN}>
      <path d="${{d}}" fill="{UVA}" stroke="{UVA}" stroke-width="78" transform="translate(18 21)"/>
      <path d="${{d}}" fill="#fff" stroke="#fff" stroke-width="78"/>
      <path d="${{d}}" fill="#0A0A0C" stroke="#0A0A0C" stroke-width="39"/>
      <path d="${{d}}" fill="{TIL_FILL}"/></g></svg>`;
    o.l.insertAdjacentHTML('beforeend', svg);
  }}
  // mesmo plano: gira cada camada em volta do centro da linha (sem criar camada por linha)
  ls.forEach(l=>{{const f=l.querySelector('.fantasma');const ox=f.offsetWidth/2, oy=f.offsetHeight/2;
    [...l.children].forEach(c=>{{if(c.classList.contains('fantasma'))return;
      const cx=ox-(c.offsetLeft||0), cy=oy-(c.offsetTop||0);
      c.style.transformOrigin=cx+'px '+cy+'px'; c.style.transform='rotate('+l.dataset.rot+'deg)';}});}});
  const AI={json.dumps(ANO_INT) if ANO_INT else 'null'};
  if(AI){{ document.getElementById('ano').style.display='none';
    const R=ls[2].getBoundingClientRect(), E=document.getElementById('esc');
    const d=document.createElement('div'); d.className='ln'; d.style.fontFamily=AI.fam; d.style.fontSize=AI.tam+'px';
    const lay=['l1','l2','l3','l4'];
    d.innerHTML='<span class=fantasma>'+AI.txt+'</span>'+lay.map(c=>'<span class='+c+'>'+AI.txt+'</span>').join('');
    document.body.appendChild(d);
    const f=d.querySelector('.fantasma'), w=f.offsetWidth, h=f.offsetHeight;
    d.style.left=(R.left+R.width*AI.ax-w/2)+'px'; d.style.top=(R.bottom-h*0.5+AI.ay)+'px';
    [...d.children].forEach(c=>{{if(c.classList.contains('fantasma'))return;
      c.style.transformOrigin=(w/2-c.offsetLeft)+'px '+(h/2-c.offsetTop)+'px'; c.style.transform='rotate('+AI.rot+'deg)';
      if(AI.cor=='branco'&&c.classList.contains('l3')){{c.style.background='none';c.style.color='#fff';}}
      if(AI.cor=='branco'&&c.classList.contains('l4'))c.style.display='none';
      if(AI.cor=='meio'&&c.classList.contains('l3')){{c.style.background='linear-gradient(180deg,#fff 0 52%,#996BB3 52% 100%)';c.style.webkitBackgroundClip='text';c.style.backgroundClip='text';}}
      if(AI.cor=='lilas'&&c.classList.contains('l3')){{c.style.background='linear-gradient(180deg,#fff,#E4CFF7 60%,#C9A8E6)';c.style.webkitBackgroundClip='text';c.style.backgroundClip='text';}}
      if(AI.cor=='preto'&&c.classList.contains('l3')){{c.style.background='none';c.style.color='#0A0A0C';}}
      if(AI.cor=='preto'&&c.classList.contains('l2')){{c.style.webkitTextStroke='.075em #996BB3';c.style.color='#996BB3';}}}});
    const db=d.querySelector('.l1').getBoundingClientRect();
    E.style.top=(Math.max(db.bottom,R.bottom)+AI.esc_dy)+'px';
    E.style.left=(750-E.offsetWidth/2+40)+'px';
  }}
  // layout pra exportar em vetor (exportar_pdf.py)
  const L=ls.map((l,i)=>{{const o=info[i];const f=l.querySelector('.fantasma');
    const base=(o.fs-(o.m.FA+o.m.FD))/2+o.m.FA;
    return {{t:l.querySelector('.l3').textContent,fs:o.fs,x:parseFloat(l.style.left),y:parseFloat(l.style.top),base,
      rot:+l.dataset.rot,ox:f.offsetWidth/2,oy:f.offsetHeight/2,
      til:(()=>{{const sv=l.querySelector('svg');return sv?{{x:parseFloat(sv.style.left),y:parseFloat(sv.style.top)}}:null}})()}};}});
  const an=document.getElementById('ano'), es=document.getElementById('esc');
  cv.font='{ANO_TAM}px A'; const ma=cv.measureText('2027');
  document.body.dataset.layout=JSON.stringify({{linhas:L,
    ano:{{x:an.offsetLeft,y:an.offsetTop,w:an.offsetWidth,h:an.offsetHeight,FA:ma.fontBoundingBoxAscent,FD:ma.fontBoundingBoxDescent}},
    esc:{{x:es.offsetLeft,y:es.offsetTop,w:es.offsetWidth,h:es.offsetHeight}}}});
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
