#!/usr/bin/env python3
"""Encaixa fotos na moldura do @plagio.zip.

Moldura medida nos posts de exemplo:
 canvas branco 1080x1350 (4:5)
 janela da foto 636x796, em x=222, y=277 (margens 222 px dos lados e 277 px em cima e embaixo)

Uso:
 python3 enquadrar.py FOTO_OU_PASTA [-o PASTA_SAIDA] [--cor] [--contraste 1.25]
            [--foco 0.5,0.5] [--acento 340-20] [--inteira] [--fundo #000000] [--qualidade 95]

Por padrao a foto vira preto e branco com contraste alto, como nos posts do perfil.
Use --cor para manter as cores (acento de cor em look, por exemplo).
Use --acento H1-H2 para P&B com UMA cor de destaque (matiz em graus, 0-360; varias faixas com virgula):
 vermelho 340-20 · laranja/dourado 25-50 · amarelo 45-65 · verde 80-160 · azul 190-250 · roxo/magenta 260-330.
Use --inteira para capas de disco e imagens que nao podem ser cortadas: a imagem entra inteira
 na janela, centralizada, com fundo --fundo (branco por padrao; NUNCA faixa preta).
Use --foco X,Y (0 a 1) para escolher a parte da foto que fica quando o corte e necessario:
 0.5,0.5 centro; 0.5,0.2 mantem mais o topo (rosto); 0.2,0.5 mantem mais a esquerda.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

CANVAS = (1080, 1350)
JANELA_POS = (222, 277)
JANELA_TAM = (636, 796)
EXTENSOES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}


def faixas_acento(texto: str) -> list[tuple[float, float]]:
    return [tuple(float(v) for v in f.split("-")) for f in texto.split(",")]


def mascara_acento(img: Image.Image, faixas: list[tuple[float, float]]) -> Image.Image:
    hsv = np.asarray(img.convert("HSV")).astype(np.float32)
    h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    dentro = np.zeros(h.shape, bool)
    for a, b in faixas:
        dentro |= ((h >= a) & (h <= b)) if a <= b else ((h >= a) | (h <= b))
    forca = np.clip((s - 0.25) / 0.25, 0, 1) * np.clip((v - 0.12) / 0.15, 0, 1) * dentro
    return Image.fromarray((forca * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))


def preparar(img: Image.Image, cor: bool, contraste: float, foco: tuple[float, float],
             inteira: bool = False, fundo: str = "#ffffff", acento: str | None = None) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA", "P"):
        base = Image.new("RGB", img.size, (255, 255, 255))
        rgba = img.convert("RGBA")
        base.paste(rgba, mask=rgba.split()[-1])
        img = base
    else:
        img = img.convert("RGB")

    if not cor:
        original = img
        img = ImageOps.grayscale(img)
        img = ImageOps.autocontrast(img, cutoff=0.5)
        img = ImageEnhance.Contrast(img).enhance(contraste)
        img = img.convert("RGB")
        if acento:
            img = Image.composite(original, img, mascara_acento(original, faixas_acento(acento)))

    if inteira:
        caixa = Image.new("RGB", JANELA_TAM, fundo)
        img = ImageOps.contain(img, JANELA_TAM, method=Image.LANCZOS)
        caixa.paste(img, ((JANELA_TAM[0] - img.width) // 2, (JANELA_TAM[1] - img.height) // 2))
        return caixa
    return ImageOps.fit(img, JANELA_TAM, method=Image.LANCZOS, centering=foco)


def montar(foto: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", CANVAS, (255, 255, 255))
    canvas.paste(foto, JANELA_POS)
    return canvas


def listar(entrada: Path) -> list[Path]:
    if entrada.is_file():
        return [entrada]
    return sorted(p for p in entrada.iterdir() if p.suffix.lower() in EXTENSOES)


def main() -> int:
    ap = argparse.ArgumentParser(description="Encaixa fotos na moldura do @plagio.zip")
    ap.add_argument("entrada", type=Path, help="foto ou pasta com fotos")
    ap.add_argument("-o", "--saida", type=Path, default=Path("saida"), help="pasta de saida")
    ap.add_argument("--cor", action="store_true", help="mantem as cores em vez de P&B")
    ap.add_argument("--contraste", type=float, default=1.25, help="contraste extra no P&B (1.0 = nenhum)")
    ap.add_argument("--foco", default="0.5,0.5", help="ponto de corte X,Y de 0 a 1")
    ap.add_argument("--acento", help="P&B com uma cor de destaque: faixa de matiz H1-H2 (ex.: 340-20 = vermelho)")
    ap.add_argument("--inteira", action="store_true", help="nao corta: imagem inteira na janela com fundo")
    ap.add_argument("--fundo", default="#ffffff", help="cor do fundo da janela com --inteira")
    ap.add_argument("--qualidade", type=int, default=95, help="qualidade do JPG")
    args = ap.parse_args()

    try:
        fx, fy = (float(v) for v in args.foco.split(","))
        if not (0 <= fx <= 1 and 0 <= fy <= 1):
            raise ValueError
    except ValueError:
        print("--foco precisa ser X,Y entre 0 e 1, por exemplo 0.5,0.3", file=sys.stderr)
        return 2

    if not args.entrada.exists():
        print(f"Nao achei {args.entrada}", file=sys.stderr)
        return 2

    arquivos = listar(args.entrada)
    if not arquivos:
        print("Nenhuma imagem encontrada.", file=sys.stderr)
        return 1

    args.saida.mkdir(parents=True, exist_ok=True)
    for arq in arquivos:
        with Image.open(arq) as im:
            foto = preparar(im, args.cor, args.contraste, (fx, fy), args.inteira, args.fundo, args.acento)
        destino = args.saida / f"{arq.stem}_plagio.jpg"
        montar(foto).save(destino, "JPEG", quality=args.qualidade, subsampling=0)
        print(f"{arq.name} -> {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
