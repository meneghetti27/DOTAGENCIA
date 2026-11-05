#!/usr/bin/env python3
"""Encaixa fotos na moldura do @plagio.zip.

Moldura medida nos posts de exemplo:
 canvas branco 1080x1350 (4:5)
 janela da foto 636x796, em x=222, y=277 (margens 222 px dos lados e 277 px em cima e embaixo)

Uso:
 python3 enquadrar.py FOTO_OU_PASTA [-o PASTA_SAIDA] [--cor] [--contraste 1.25]
            [--foco 0.5,0.5] [--inteira] [--fundo #000000] [--qualidade 95]

Por padrao a foto vira preto e branco com contraste alto, como nos posts do perfil.
Use --cor para manter as cores (acento de cor em look, por exemplo).
Use --inteira para capas de disco e imagens que nao podem ser cortadas: a imagem entra inteira
 na janela, centralizada, com fundo --fundo (preto por padrao).
Use --foco X,Y (0 a 1) para escolher a parte da foto que fica quando o corte e necessario:
 0.5,0.5 centro; 0.5,0.2 mantem mais o topo (rosto); 0.2,0.5 mantem mais a esquerda.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

CANVAS = (1080, 1350)
JANELA_POS = (222, 277)
JANELA_TAM = (636, 796)
EXTENSOES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}


def preparar(img: Image.Image, cor: bool, contraste: float, foco: tuple[float, float],
             inteira: bool = False, fundo: str = "#000000") -> Image.Image:
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA", "P"):
        base = Image.new("RGB", img.size, (255, 255, 255))
        rgba = img.convert("RGBA")
        base.paste(rgba, mask=rgba.split()[-1])
        img = base
    else:
        img = img.convert("RGB")

    if not cor:
        img = ImageOps.grayscale(img)
        img = ImageOps.autocontrast(img, cutoff=0.5)
        img = ImageEnhance.Contrast(img).enhance(contraste)
        img = img.convert("RGB")

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
    ap.add_argument("--inteira", action="store_true", help="nao corta: imagem inteira na janela com fundo")
    ap.add_argument("--fundo", default="#000000", help="cor do fundo da janela com --inteira")
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
            foto = preparar(im, args.cor, args.contraste, (fx, fy), args.inteira, args.fundo)
        destino = args.saida / f"{arq.stem}_plagio.jpg"
        montar(foto).save(destino, "JPEG", quality=args.qualidade, subsampling=0)
        print(f"{arq.name} -> {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
