# Busca PNGs no pngwing e monta uma folha numerada para escolher.
# Uso: python3 buscar-png.py nome "termo em inglês" pasta_saida
#   -> pasta_saida/nome.jpg (folha com números) e nome.json (links das miniaturas).
# Tamanho cheio: troque "-thumbnail.png" por ".png" no link escolhido (≈920 px).
# Atenção: os PNGs "transparentes" do pngwing vêm com o xadrez desenhado; recorte com recortar.py (rembg).
# Use termos curtos (1–3 palavras); buscas longas voltam vazias.
import sys, re, io, json, subprocess, urllib.parse
baixa = lambda u: subprocess.run(['curl', '-s', '-L', '--max-time', '20', u], capture_output=True).stdout
from PIL import Image, ImageDraw
nome, q, pasta = sys.argv[1], sys.argv[2], sys.argv[3]
u = 'https://www.pngwing.com/en/search?q=' + urllib.parse.quote(q)
h = baixa(u).decode('utf8', 'ignore')
ths = []
for m in re.findall(r'https://w7\.pngwing\.com/pngs/\d+/\d+/png-transparent-[^"\s]*-thumbnail\.png', h):
    if m not in ths: ths.append(m)
ths = ths[:30]
json.dump(ths, open(f'{pasta}/{nome}.json', 'w'))
W = 200
folha = Image.new('RGB', (W * 6, W * 5), (200, 200, 200))
dr = ImageDraw.Draw(folha)
for k, t in enumerate(ths):
    try:
        im = Image.open(io.BytesIO(baixa(t))).convert('RGBA')
        im.thumbnail((W, W))
        folha.paste(im, ((k % 6) * W, (k // 6) * W), im)
    except Exception as e: pass
    dr.rectangle([(k % 6) * W, (k // 6) * W, (k % 6) * W + 28, (k // 6) * W + 22], fill='red')
    dr.text(((k % 6) * W + 4, (k // 6) * W + 4), str(k), fill='white')
folha.save(f'{pasta}/{nome}.jpg')
print(nome, len(ths))
