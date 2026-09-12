#!/usr/bin/env python3
"""Gera um mapa estatico do consultorio em publicar/assets/mapa-consultorio.png.

Por que existe: o mapa da pagina e um iframe do Google, e iframe nao carrega em
todo lugar (visualizador de artifacts, bloqueador de anuncios, rede que barra o
Google). Essa imagem fica atras do iframe e aparece nesses casos, no lugar de um
retangulo vazio.

Roda uma vez; so precisa rodar de novo se o endereco mudar.
Requer pillow. Ladrilhos do OpenStreetMap, creditados dentro da imagem.
"""
import io
import math
import pathlib
import urllib.request

from PIL import Image, ImageDraw, ImageFont

# coordenadas da ficha da Rafaella no Google Meu Negocio
LAT, LON = -23.0089997, -43.4418045
ZOOM = 16
LARGURA, ALTURA = 1200, 675          # 16:9, mesma proporcao da moldura
SAIDA = pathlib.Path(__file__).parent.parent / "publicar" / "assets" / "mapa_consultorio.jpg"

VINHO = (113, 32, 46)
CREME = (244, 241, 235)
TILE = 256
UA = {"User-Agent": "rafaella-rodrigues-landing/1.0 (mapa estatico, uso unico)"}


def para_pixel(lat, lon, zoom):
    n = 2 ** zoom
    x = (lon + 180.0) / 360.0 * n * TILE
    rad = math.radians(lat)
    y = (1.0 - math.asinh(math.tan(rad)) / math.pi) / 2.0 * n * TILE
    return x, y


def baixar_tile(z, x, y):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


def desenhar_marcador(img, cx, cy):
    """Pino no estilo do site: gota em vinho com furo claro no meio."""
    d = ImageDraw.Draw(img)
    r, h = 17, 46
    d.polygon([(cx - r * 0.72, cy - h + r * 0.62), (cx + r * 0.72, cy - h + r * 0.62), (cx, cy)],
              fill=VINHO)
    d.ellipse([cx - r, cy - h - r + 16, cx + r, cy - h + r + 16], fill=VINHO)
    d.ellipse([cx - 6.5, cy - h + 9.5, cx + 6.5, cy - h + 22.5], fill=CREME)


def creditos(img):
    d = ImageDraw.Draw(img, "RGBA")
    txt = "© OpenStreetMap contributors"
    try:
        fonte = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
    except OSError:
        fonte = ImageFont.load_default()
    cx = d.textbbox((0, 0), txt, font=fonte)
    w, h = cx[2] - cx[0], cx[3] - cx[1]
    d.rectangle([img.width - w - 20, img.height - h - 16, img.width, img.height],
                fill=(255, 255, 255, 205))
    d.text((img.width - w - 10, img.height - h - 11), txt, font=fonte, fill=(60, 60, 60))


def main():
    cx, cy = para_pixel(LAT, LON, ZOOM)
    esq, topo = cx - LARGURA / 2, cy - ALTURA / 2
    tx0, ty0 = int(esq // TILE), int(topo // TILE)
    tx1, ty1 = int((esq + LARGURA) // TILE), int((topo + ALTURA) // TILE)

    mosaico = Image.new("RGB", ((tx1 - tx0 + 1) * TILE, (ty1 - ty0 + 1) * TILE), CREME)
    total = 0
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            try:
                mosaico.paste(baixar_tile(ZOOM, tx, ty), ((tx - tx0) * TILE, (ty - ty0) * TILE))
                total += 1
            except Exception as e:
                print(f"  ladrilho {tx},{ty} falhou: {e}")

    img = mosaico.crop((int(esq - tx0 * TILE), int(topo - ty0 * TILE),
                        int(esq - tx0 * TILE) + LARGURA, int(topo - ty0 * TILE) + ALTURA))
    desenhar_marcador(img, LARGURA // 2, ALTURA // 2 + 20)
    creditos(img)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    img.save(SAIDA, quality=84, optimize=True, progressive=True)
    print(f"{total} ladrilhos | {SAIDA.name} {img.size[0]}x{img.size[1]} "
          f"{SAIDA.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
