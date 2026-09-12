#!/usr/bin/env python3
"""Extrai logotipos e personagens do manual de identidade visual (PDF)
para PNGs com fundo transparente, em ../publicar/assets/.

Requer: pymupdf, pillow
"""
import io, pathlib
import fitz
from PIL import Image

PDF = "/Users/maiconmorote/Downloads/Identidade Visual - Rafaella Rodrigues - .pdf"
OUT = pathlib.Path(__file__).parent.parent / "publicar" / "assets"
OUT.mkdir(exist_ok=True)

# pagina (0-indexada), retangulo em pontos, cor de fundo a remover, largura final
ITEMS = {
    "logo_horizontal": (12, (128, 427, 655, 903), (255, 171, 207), 760),
    "logo_stacked":    (12, (696, 425, 1223, 901), (244, 241, 235), 680),
    "logo_badge":      (12, (1254, 427, 1781, 903), (203, 227, 203), 620),
    "char_heart":      (10, (140, 460, 505, 820), (255, 255, 255), 340),
    "char_bubble":     (10, (515, 460, 790, 820), (255, 255, 255), 340),
    "char_brain":      (10, (800, 460, 1240, 820), (255, 255, 255), 380),
    "char_scribble":   (10, (1245, 460, 1610, 820), (255, 255, 255), 340),
}

# Abaixo deste alfa o pixel vira totalmente transparente. Sem isso, resta um
# veu uniforme sobre toda a caixa da imagem, invisivel em fundo claro mas
# visivel como um retangulo em fundo escuro.
ALPHA_FLOOR = 30
TOLERANCIA = 55  # distancia de cor ate onde o fundo e considerado fundo


def remove_fundo(img, bg):
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, _ = px[x, y]
            dist = max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2]))
            if dist >= TOLERANCIA:
                continue
            a = int(255 * dist / TOLERANCIA)
            px[x, y] = (r, g, b, 0 if a < ALPHA_FLOOR else a)
    return img


def main():
    doc = fitz.open(PDF)
    for nome, (pagina, rect, bg, largura) in ITEMS.items():
        pix = doc[pagina].get_pixmap(matrix=fitz.Matrix(4, 4), clip=fitz.Rect(*rect))
        img = remove_fundo(Image.open(io.BytesIO(pix.tobytes("png"))), bg)
        img = img.crop(img.split()[3].point(lambda v: 255 if v > 40 else 0).getbbox())
        img = img.resize((largura, round(img.height * largura / img.width)), Image.LANCZOS)
        img.save(OUT / f"{nome}.png", optimize=True)
        print(f"{nome:18} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
