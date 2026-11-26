"""10 modelos de escrita (fontes de grafite) pra turma escolher.

uso: python3 modelos.py  -> modelos-escrita/01-....png (1600x1000 cada) + modelos-escrita/todos.jpg
Mesmo acabamento em todos (recheio roxo em degradê, contorno preto, linha branca, 3D uva)
pra comparar só o desenho da letra.
"""
import subprocess
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).parent
OUT = AQUI / "modelos-escrita"
OUT.mkdir(exist_ok=True)

RODADA2 = [(f"{n}.{e}", est, None) for n, e, est in [
    ("bostero", "ttf", "Bloco condensado"), ("break_rebel", "ttf", "Wild leve"), ("bubble_street", "ttf", "Bolha cheia"),
    ("death_stars", "ttf", "Bloco aberto"), ("derans_vandals", "ttf", "Bloco torto"), ("funky_star", "ttf", "Bloco funk"),
    ("gress_down", "otf", "Bloco afiado"), ("hard_zone", "ttf", "Bolha quadrada"), ("high_damage", "otf", "Bolha larga"),
    ("hosters", "otf", "Escorrido leve"), ("urban_vibes", "ttf", "Bloco pingado"), ("metro_marks", "ttf", "Bloco metrô"),
    ("rousael", "ttf", "Bolha mole"), ("seven_venom", "otf", "Wild pesado"), ("smoke_in_the_city", "ttf", "Bloco gordinho"),
    ("street_shade", "ttf", "Bloco inclinado"), ("stretzo", "otf", "Bolha reta"), ("super_fortune", "ttf", "Bolha redonda"),
    ("thomas_2", "otf", "Bloco pesado"), ("weird_3", "otf", "Bloco esticado")]]

MODELOS = [  # (arquivo, nome do estilo, fonte do ano se a da letra não tiver números bons)
    ("beat_mark.ttf", "Bloco clássico", None),
    ("urban_blocker.ttf", "Bolha", None),
    ("drop_shade.ttf", "Escorrido", None),
    ("graffiti_youth.otf", "Bloco gordo", None),
    ("king_jack_style.ttf", "Bolha pesada", None),
    ("urban_heroes.ttf", "Tinta pingando", None),
    ("nightclaw_vandal.ttf", "Pontiagudo", "beat_mark.ttf"),
    ("smashed_graffiti.otf", "Rachado", None),
    ("grime_slime.ttf", "Old school", None),
    ("urban_gear.ttf", "Bloco reto", None),
]

FD = (AQUI / "fontes/dafont").resolve().as_uri()
ROXO, CLARO, ESCURO, UVA = "#996BB3", "#E4CFF7", "#7A4C99", "#3E2353"

def html(fonte, estilo, n, fano=None):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:G;src:url('{FD}/{fonte}')}}
@font-face{{font-family:A;src:url('{FD}/{fano or fonte}')}}
@font-face{{font-family:Inter;src:local('Inter'),local('Arial')}}
html,body{{margin:0;width:1600px;height:1000px;background:#0A0A0C;overflow:hidden}}
body{{background:radial-gradient(ellipse 60% 50% at 50% 48%,#1E1229 0%,#0A0A0C 70%)}}
.palco{{position:absolute;left:0;top:0;width:1600px;height:1000px}}
.t{{position:absolute;left:50%;top:430px;transform:translate(-50%,-50%) rotate(-4deg);font-family:G;
   white-space:nowrap;line-height:1;font-size:300px}}
.t span{{position:absolute;left:-.5em;top:0;padding:0 .5em;white-space:nowrap}}
.l1{{-webkit-text-stroke:.17em #fff;color:#fff;paint-order:stroke fill;
     filter:drop-shadow(5px 6px 0 {UVA}) drop-shadow(5px 6px 0 {UVA}) drop-shadow(5px 6px 0 {UVA}) drop-shadow(4px 5px 0 #000)}}
.l2{{-webkit-text-stroke:.085em #0A0A0C;color:#0A0A0C;paint-order:stroke fill}}
.l3{{background:linear-gradient(180deg,{CLARO} 0%,{ROXO} 48%,{ESCURO} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.l4{{color:transparent;background:linear-gradient(180deg,rgba(255,255,255,.55) 0 12%,transparent 12.5%);-webkit-background-clip:text;background-clip:text;opacity:.6}}
.fantasma{{visibility:hidden;position:static!important;padding:0!important}}
.ano{{position:absolute;right:220px;top:640px;transform:rotate(-4deg);font-family:A;font-size:130px;color:#fff;
      -webkit-text-stroke:.16em #0A0A0C;paint-order:stroke fill;filter:drop-shadow(5px 6px 0 {ROXO})}}
.esc{{position:absolute;left:230px;top:700px;transform:rotate(-4deg);font:600 30px/1 Inter,Arial,sans-serif;letter-spacing:.42em;color:{ROXO}}}
.rot{{position:absolute;left:60px;top:52px;font:500 24px/1 Inter,Arial,sans-serif;letter-spacing:.3em;color:#8d7f99}}
.rot b{{color:#fff;font-weight:800;margin-right:14px}}
.st{{position:absolute;width:var(--s);height:var(--s);background:var(--c);
     clip-path:polygon(50% 0,58% 42%,100% 50%,58% 58%,50% 100%,42% 58%,0 50%,42% 42%)}}
</style></head><body><div class=palco>
<div class=rot><b>{n:02d}</b>{estilo.upper()} · <span style="color:#5d5266">{fonte.split('.')[0].replace('_',' ').upper()}</span></div>
<div class=t id=t><span class="fantasma">TERCEIRÃO</span>
<span class=l1>TERCEIRÃO</span><span class=l2>TERCEIRÃO</span><span class=l3>TERCEIRÃO</span><span class=l4>TERCEIRÃO</span></div>
<div class=ano>2027</div>
<div class=esc>MÃE DE DEUS</div>
<i class=st style="--s:70px;--c:#fff;left:150px;top:200px"></i>
<i class=st style="--s:46px;--c:{ROXO};left:1420px;top:230px"></i>
<i class=st style="--s:54px;--c:#fff;left:1440px;top:720px"></i>
<i class=st style="--s:34px;--c:{ROXO};left:120px;top:640px"></i>
</div>
<script>
document.fonts.ready.then(()=>{{const t=document.getElementById('t');let fs=300;
 while(t.getBoundingClientRect().width>1250&&fs>60){{fs-=6;t.style.fontSize=fs+'px'}}
 while(t.getBoundingClientRect().width<1150&&fs<420){{fs+=6;t.style.fontSize=fs+'px'}}}});
</script></body></html>"""


def rodar(lista, pasta, inicio):
    pasta.mkdir(parents=True, exist_ok=True)
    pngs = []
    for i, (f, est, fano) in enumerate(lista, inicio):
        nome = f"{i:02d}-{est.lower().replace(' ', '-')}"
        h = pasta / f"_{nome}.html"
        h.write_text(html(f, est, i, fano))
        png = pasta / f"{nome}.png"
        subprocess.run(["node", str(AQUI.parent / "tools/html-to-png.js"), str(h), str(png), "1600", "1000", "1"], check=True)
        h.unlink(); pngs.append(png); print("ok", png.name)
    linhas = (len(pngs) + 1) // 2
    c = Image.new("RGB", (1600, 500 * linhas), "#0A0A0C")
    for k, p in enumerate(pngs):
        c.paste(Image.open(p).convert("RGB").resize((800, 500)), ((k % 2) * 800, (k // 2) * 500))
    c.save(pasta / "todos.jpg", quality=88)


if __name__ == "__main__":
    import sys
    if "1" in sys.argv[1:] or len(sys.argv) == 1:
        rodar(MODELOS, OUT, 1)
    if "2" in sys.argv[1:] or len(sys.argv) == 1:
        rodar(RODADA2, OUT / "rodada2", 11)
