# Remove o fundo de imagens (inclusive o xadrez falso dos PNGs do pngwing) com rembg.
# Uso: python3 recortar.py entrada.png saida.png [modelo]
# Modelos: isnet-general-use (padrão, melhor na maioria), u2net (objetos com brilho/fogo),
#          u2net_human_seg (pessoas com fundo desfocado). Instalar: pip install "rembg[cpu]".
import sys
from PIL import Image
from rembg import new_session, remove

entrada, saida = sys.argv[1], sys.argv[2]
modelo = sys.argv[3] if len(sys.argv) > 3 else 'isnet-general-use'
out = remove(Image.open(entrada).convert('RGB'), session=new_session(modelo))
out.crop(out.getbbox()).save(saida)
print(saida, out.size)
