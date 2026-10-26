#!/usr/bin/env python3
"""Busca imagens grandes, baixa e monta uma folha de contato numerada (folha.jpg) + fontes.txt com títulos.

Uso: python3 tools/buscar-imagens.py "termo em inglês" pasta_saida [quantidade] [bing|aberta]
- bing (padrão): melhores imagens. Faça UMA busca por vez com pausa (~20 s); rajadas fazem o Bing devolver
  resultados aleatórios — confira os títulos em fontes.txt.
- aberta: Openverse (Flickr) + Wikimedia Commons; fotos mais "documentais", também com limite de requisições.
Google e DuckDuckGo exigem desafio anti-robô: não usar.
Projeto fictício de treino: as imagens servem só de teste.
"""
import html, json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw

UA = "DotDesignBot/1.0 (treino de design; github meneghetti27/DOTAGENCIA)"
termo, pasta = sys.argv[1], sys.argv[2]
qtd = int(sys.argv[3]) if len(sys.argv) > 3 else 20
fonte = sys.argv[4] if len(sys.argv) > 4 else "bing"
os.makedirs(pasta, exist_ok=True)
BUA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def get(url, ua=UA):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=40).read()


cands = []
if fonte == "bing":
    for first in (1, 36):
        u = "https://www.bing.com/images/search?" + urllib.parse.urlencode({"q": termo, "form": "HDRSC2", "first": first}) + "&qft=+filterui:imagesize-large"
        page = get(u, BUA).decode("utf-8", "ignore")
        for m in re.findall(r'class="iusc"[^>]*\sm="([^"]+)"', page):
            d = json.loads(html.unescape(m))
            if d.get("murl"):
                cands.append((d["murl"], 0, 0, d.get("t", "")))
        time.sleep(3)
# Openverse (Flickr, Wikimedia, etc.)
for page in ((1, 2) if fonte == "aberta" else ()):
    try:
        q = urllib.parse.urlencode({"q": termo, "page_size": 20, "page": page, "size": "large"})
        for r in json.loads(get("https://api.openverse.org/v1/images/?" + q)).get("results", []):
            if (r.get("width") or 0) >= 1200:
                cands.append((r["url"], r.get("width"), r.get("height"), r.get("title") or ""))
    except Exception:
        pass
# Wikimedia Commons (busca em arquivos, miniatura de 1800 px)
try:
    assert fonte == "aberta"
    q = urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrsearch": termo + " filetype:bitmap",
                                "gsrnamespace": 6, "gsrlimit": 30, "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": 1800})
    for p in json.loads(get("https://commons.wikimedia.org/w/api.php?" + q)).get("query", {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("width", 0) >= 1200:
            cands.append((ii.get("thumburl") or ii["url"], ii["width"], ii["height"], p.get("title", "")))
except Exception:
    pass


def baixar(i_c):
    i, (u, w, h, t) = i_c
    try:
        data = get(u, BUA)
        ext = ".png" if data[:4] == b"\x89PNG" else ".jpg"
        p = os.path.join(pasta, f"{i:02d}{ext}")
        open(p, "wb").write(data)
        im = Image.open(p); im.load()
        return p, im.size, u, t
    except Exception:
        return None


res = [r for r in ThreadPoolExecutor(8).map(baixar, enumerate(cands[: qtd * 2], 1)) if r][:qtd]
with open(os.path.join(pasta, "fontes.txt"), "w") as f:
    for p, s, u, t in res:
        f.write(f"{os.path.basename(p)}\t{s[0]}x{s[1]}\t{t[:60]}\t{u}\n")

cols, cw, ch = 5, 260, 300
sheet = Image.new("RGB", (cols * cw, max(1, (len(res) + cols - 1) // cols) * ch), (20, 20, 28))
d = ImageDraw.Draw(sheet)
for k, (p, s, _, _) in enumerate(res):
    im = Image.open(p).convert("RGBA"); im.thumbnail((cw - 10, ch - 30))
    bg = Image.new("RGBA", im.size, (60, 60, 70, 255)); bg.alpha_composite(im)
    x, y = (k % cols) * cw + 5, (k // cols) * ch + 5
    sheet.paste(bg.convert("RGB"), (x, y))
    d.text((x + 4, y + ch - 24), f"{os.path.basename(p)}  {s[0]}x{s[1]}", fill=(255, 255, 255))
sheet.save(os.path.join(pasta, "folha.jpg"), quality=85)
print(f"{len(res)} imagens em {pasta}")
