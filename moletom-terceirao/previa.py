"""prévia das artes sobre o preto do moletom: python3 previa.py pasta saida.jpg"""
import sys
from pathlib import Path
from PIL import Image
pasta, saida = Path(sys.argv[1]), sys.argv[2]
ordem = ["logo-principal", "logo-horizontal", "simbolo-3", "ano-vertical", "estampa-nomes"]
W = 2400
c = Image.new("RGB", (W, 2600), "#0A0A0C")
lay = {"logo-principal": (0, 0, 1100, 1210), "simbolo-3": (1150, 30, 560, 580), "ano-vertical": (1820, 30, 200, 690),
       "logo-horizontal": (1120, 720, 1250, 290), "estampa-nomes": (1150, 1060, 1200, 800)}
for n, (x, y, w, h) in lay.items():
    im = Image.open(pasta / f"{n}.png").convert("RGBA"); im.thumbnail((w, h)); c.paste(im, (x, y), im)
c = c.crop((0, 0, W, 1900)); c.save(saida, quality=90)
