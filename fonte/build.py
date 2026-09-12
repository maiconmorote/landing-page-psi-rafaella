#!/usr/bin/env python3
"""Gera as duas versoes do site a partir de body.src.html:

  ../publicar/index.html -> pagina completa que aponta para ./assets (hospedagem)
  build/artifact.html    -> arquivo unico, imagens embutidas em data: URI
"""
import base64, html, json, mimetypes, pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).parent          # landing-page/fonte
PUB = ROOT.parent / "publicar"                # o que vai para o servidor
ASSETS = PUB / "assets"
BUILD = ROOT / "build"                        # versao de pre-visualizacao
BUILD.mkdir(exist_ok=True)

src = (ROOT / "body.src.html").read_text(encoding="utf-8")

# --- depoimentos (depoimentos.json, preenchido a mao) -----------------------
DADOS = json.loads((ROOT / "depoimentos.json").read_text(encoding="utf-8"))
AMARELO = "#EDBA3D"          # dourado da paleta da marca
VAZIA = "#E3DBD2"

def estrela(cor):
    return (f'<svg viewBox="0 0 24 24" fill="{cor}" aria-hidden="true">'
            '<path d="M12 2.6l2.7 5.9 6.4.7-4.8 4.4 1.3 6.3L12 16.7 6.4 19.9l1.3-6.3L2.9 9.2l6.4-.7z"/>'
            '</svg>')

def estrelas(nota, classe=""):
    """Cinco estrelas douradas, com a ultima recortada na fracao exata.

    A largura do recorte e calculada sobre as estrelas cheias mais os vaos
    entre elas. Usar uma porcentagem simples da faixa inteira faria a fracao
    cair dentro do vao e mostrar meia estrela errada.
    """
    nota = max(0.0, min(5.0, float(nota or 0)))
    lado = 16 if "stars--sm" in classe else 19      # ver .stars svg no CSS
    vao = 3                                          # ver .stars gap no CSS
    inteiras, fracao = divmod(nota, 1)
    inteiras = int(inteiras)
    if fracao == 0:
        largura = inteiras * lado + max(0, inteiras - 1) * vao
    else:
        largura = inteiras * (lado + vao) + fracao * lado

    cls = f"stars {classe}".strip()
    return (f'<span class="{cls}" role="img" aria-label="{nota:.1f} de 5 estrelas">'
            f'<span class="stars__track">'
            f'<span class="stars {classe}" aria-hidden="true">{estrela(VAZIA) * 5}</span>'
            f'<span class="stars__fill" style="width:{largura:.2f}px">'
            f'<span class="stars {classe}" aria-hidden="true">{estrela(AMARELO) * 5}</span></span>'
            f'</span></span>')

LOGO_G = ('<svg width="15" height="15" viewBox="0 0 48 48" aria-hidden="true">'
          '<path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-2.8-.4-4H24v7.5h12.1c-.2 2-1.6 5-4.5 7l6.9 5.4c4.1-3.8 6.6-9.4 6.6-15.9z"/>'
          '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.3l-6.9-5.4c-1.9 1.3-4.4 2.2-7.6 2.2-5.8 0-10.7-3.8-12.5-9.1l-7.1 5.5C8 41.3 15.4 46 24 46z"/>'
          '<path fill="#FBBC05" d="M11.5 28.4c-.5-1.4-.7-2.9-.7-4.4s.3-3 .7-4.4l-7.1-5.5C2.9 17 2 20.4 2 24s.9 7 2.4 9.9z"/>'
          '<path fill="#EA4335" d="M24 10.5c4.1 0 6.9 1.8 8.5 3.3l6.2-6C34.9 4.4 29.9 2 24 2 15.4 2 8 6.7 4.4 14.1l7.1 5.5c1.8-5.3 6.7-9.1 12.5-9.1z"/>'
          '</svg>')

def render_avaliacoes():
    itens = DADOS.get("depoimentos") or []
    perfil = html.escape(DADOS.get("url") or "#")
    nota = DADOS.get("nota")
    total = DADOS.get("total") or 0

    resumo = ""
    if nota and total:
        resumo = f'''    <div class="reviews__summary reveal">
      <div class="reviews__score"><b>{f"{nota:.1f}".replace(".", ",")}</b><span>de 5</span></div>
      <div class="reviews__meta">
        {estrelas(nota)}
        <p>{total} {"avaliação" if total == 1 else "avaliações"} no Google</p>
      </div>
      <span class="reviews__google">{LOGO_G} Publicadas no perfil do Google</span>
      <div class="reviews__cta">
        <a class="btn btn--ghost" href="{perfil}" target="_blank" rel="noopener">Ver todas no Google</a>
      </div>
    </div>'''

    if not itens:
        return resumo + f'''
    <div class="reviews__vazio reveal">
      <strong>Os depoimentos aparecem aqui assim que forem cadastrados.</strong>
      Adicione cada um em <code>fonte/depoimentos.json</code> e rode
      <code>python3 fonte/build.py</code>.
    </div>'''

    cartoes = []
    for av in itens:
        quem = html.escape(av.get("quem") or "")
        # linha em branco no JSON separa paragrafo
        paragrafos = "\n        ".join(
            f"<p>{html.escape(bloco.strip())}</p>"
            for bloco in re.split(r"\n\s*\n", av.get("texto") or "") if bloco.strip())
        cartoes.append(f'''      <article class="review reveal">
        <div class="review__head">
          <div class="review__avatar">{html.escape(quem[:1].upper())}</div>
          <div class="review__who">
            <strong>{quem}</strong>
            {estrelas(av.get("nota", 5), "stars--sm")}
          </div>
        </div>
        {paragrafos}
        <div class="review__source">{LOGO_G} Publicado no Google</div>
      </article>''')

    return resumo + '\n    <div class="reviews__grid">\n' + "\n".join(cartoes) + "\n    </div>"

BLOCO_AVALIACOES = render_avaliacoes()



EXTENSOES = (".png", ".jpg", ".jpeg", ".webp")


def achar_asset(name):
    """Devolve o arquivo de assets/ com esse nome, seja qual for a extensao."""
    for ext in EXTENSOES:
        caminho = ASSETS / f"{name}{ext}"
        if caminho.exists():
            return caminho
    return None


def data_uri_arquivo(path):
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def data_uri(name):
    path = achar_asset(name)
    if path is None:
        raise SystemExit(f"Asset nao encontrado: assets/{name}.[png|jpg|jpeg|webp]")
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


# --- malha do Instagram (publicar/assets/instagram/) ------------------------
# Basta soltar as imagens dos posts nessa pasta. Sao usadas em ordem
# alfabetica, ate 6. Para apontar cada quadro para o seu post, crie
# instagram.json aqui em fonte/ assim:
#   {"posts": [{"arquivo": "01.jpg", "url": "https://instagram.com/p/XXXX/"}]}
PERFIL_IG = "https://instagram.com/psi.rafaellarodrigues"
ARROBA_IG = "@psi.rafaellarodrigues"
IG_DIR = ASSETS / "instagram"
IG_FILES = []
if IG_DIR.is_dir():
    IG_FILES = sorted(
        (f for f in IG_DIR.iterdir()
         if f.suffix.lower() in EXTENSOES and not f.name.startswith(".")),
        key=lambda f: f.name.lower(),
    )[:6]

_ig_links = {}
_ig_json = ROOT / "instagram.json"
if _ig_json.exists():
    for post in json.loads(_ig_json.read_text(encoding="utf-8")).get("posts", []):
        if post.get("arquivo") and post.get("url"):
            _ig_links[post["arquivo"]] = post["url"]

ICONE_IG = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<rect x="2" y="2" width="20" height="20" rx="5.5"/>'
            '<circle cx="12" cy="12" r="4"/>'
            '<circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg>')


def render_instagram():
    cabecalho = f'''    <div class="ig__head reveal">
      <a class="ig__handle" href="{PERFIL_IG}" target="_blank" rel="noopener">{ICONE_IG} {ARROBA_IG}</a>
      <div class="ig__cta">
        <a class="btn btn--primary" href="{PERFIL_IG}" target="_blank" rel="noopener">Seguir no Instagram</a>
      </div>
    </div>'''

    if not IG_FILES:
        return cabecalho + f'''
    <div class="ig__vazio reveal">
      <strong>A malha aparece aqui assim que houver imagens.</strong>
      Salve as imagens dos posts em <code>publicar/assets/instagram/</code>
      e rode <code>python3 fonte/build.py</code>.
    </div>'''

    quadros = []
    for i, f in enumerate(IG_FILES):
        destino = html.escape(_ig_links.get(f.name, PERFIL_IG))
        quadros.append(
            f'      <a class="ig__tile reveal" href="{destino}" target="_blank" rel="noopener" '
            f'aria-label="Ver publicacao no Instagram de {ARROBA_IG}">'
            f'<img src="__IGSRC_{i}__" alt="" loading="lazy"></a>'
        )
    return cabecalho + '\n    <div class="ig__grid">\n' + "\n".join(quadros) + "\n    </div>"


BLOCO_INSTAGRAM = render_instagram()

if not IG_FILES:
    print()
    print("  AVISO: nenhuma imagem em publicar/assets/instagram/.")
    print("  A malha do Instagram esta vazia.")
    print()


# --- retrato da secao "Sobre mim" ------------------------------------------
# Basta salvar a foto como publicar/assets/rafaella.jpg (ou .png/.webp) e
# rodar build.py: ela entra sozinha. Sem foto, entra o logotipo como marcador.
FOTO = achar_asset("rafaella")
if FOTO:
    RETRATO = ("""    <figure class="about__portrait about__portrait--foto reveal" style="margin:0">
      <img src="__ASSET_rafaella__" alt="Rafaella Rodrigues, psicóloga infantojuvenil">
    </figure>""")
else:
    RETRATO = ("""    <figure class="about__portrait reveal" style="margin:0">
      <img src="__ASSET_logo_stacked__" alt="Marca Rafaella Rodrigues, Psicóloga Infantojuvenil">
      <figcaption>Substituir por foto da Rafaella</figcaption>
    </figure>""")
    print()
    print("  AVISO: a foto da Rafaella ainda nao foi adicionada.")
    print("  Salve em publicar/assets/rafaella.jpg e rode build.py de novo.")
    print()

src = src.replace("__DEPOIMENTOS__", BLOCO_AVALIACOES)
src = src.replace("__RETRATO__", RETRATO)
src = src.replace("__INSTAGRAM__", BLOCO_INSTAGRAM)
names = sorted(set(re.findall(r"__ASSET_([A-Za-z0-9_]+)__", src)))

# --- 1. versao Artifact: tudo embutido -------------------------------------
artifact = src
for n in names:
    artifact = artifact.replace(f"__ASSET_{n}__", data_uri(n))
for i, f in enumerate(IG_FILES):
    artifact = artifact.replace(f"__IGSRC_{i}__", data_uri_arquivo(f))
(BUILD / "artifact.html").write_text(artifact, encoding="utf-8")

# --- 2. versao hospedagem: caminhos relativos + <head> completo -------------
standalone_body = src
for i, f in enumerate(IG_FILES):
    standalone_body = standalone_body.replace(
        f"__IGSRC_{i}__", "assets/instagram/" + urllib.parse.quote(f.name))
for n in names:
    caminho = achar_asset(n)
    standalone_body = standalone_body.replace(f"__ASSET_{n}__", f"assets/{caminho.name}")

standalone_body = standalone_body.replace(
    "<title>Rafaella Rodrigues</title>",
    "<title>Rafaella Rodrigues | Psic\u00f3loga Infantojuvenil na Barra da Tijuca</title>")
head, _, body = standalone_body.partition("</style>")
head += "</style>"

# aggregateRating fica de fora do JSON-LD de proposito. As avaliacoes estao no
# perfil do Google, e a politica de resultados enriquecidos do Google nao aceita
# que o site marque como sua a nota agregada vinda de terceiro. Marcar isso
# pode render acao manual em vez de estrelinha na busca.
AGGREGATE = ""

# openingHours ficou fora do JSON-LD: o horario nunca foi confirmado pela
# Rafaella. Horario errado nos dados estruturados pode aparecer na busca do
# Google como se fosse oficial. Quando confirmar, adicione de volta.

# Dominio final do site. Enquanto nao houver dominio proprio, use a URL que a
# Vercel gera (algo como https://rafaella-rodrigues.vercel.app), sem barra no
# fim. Vale para canonical, Open Graph, JSON-LD, robots.txt e sitemap.xml.
DOMINIO = "https://SEUDOMINIO.com.br"

DESC = ("Psicóloga infantojuvenil na Barra da Tijuca, Rio de Janeiro. Atendimento acolhedor "
        "para crianças e adolescentes em TCC e ABA, com orientação para pais.")

page = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{DESC}">
<meta name="author" content="Rafaella Rodrigues">
<meta name="theme-color" content="#F4F1EB">
<link rel="canonical" href="{DOMINIO}/">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="Rafaella Rodrigues · Psicóloga Infantojuvenil">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{DOMINIO}/assets/logo_badge.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo_badge.png">
<link rel="apple-touch-icon" href="assets/logo_badge.png">
{head}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Psychologist",
  "name": "Rafaella Rodrigues · Psicóloga Infantojuvenil",
  "description": "{DESC}",
  "url": "{DOMINIO}/",
  "telephone": "+5521969025509",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Av. das Américas, 13.685",\n    "addressLocality": "Rio de Janeiro",\n    "postalCode": "22785-620",
    "addressRegion": "RJ",
    "addressCountry": "BR"
  }},
  "areaServed": "Rio de Janeiro, RJ"{AGGREGATE}
}}
</script>
</head>
<body>
{body}
</body>
</html>
"""
(PUB / "index.html").write_text(page, encoding="utf-8")

print("assets embutidos:", ", ".join(names))
print("build/artifact.html", (BUILD / "artifact.html").stat().st_size // 1024, "KB")
# --- 3. robots.txt e sitemap.xml -------------------------------------------
import datetime

(PUB / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")

hoje = datetime.date.today().isoformat()
(PUB / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"  <url>\n    <loc>{DOMINIO}/</loc>\n    <lastmod>{hoje}</lastmod>\n"
    "    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>\n"
    "</urlset>\n", encoding="utf-8")

if "SEUDOMINIO" in DOMINIO:
    print()
    print("  AVISO: DOMINIO ainda esta com valor de exemplo no build.py.")
    print("  canonical, Open Graph, sitemap e robots vao sair errados.")
    print()

print("publicar/index.html", (PUB / "index.html").stat().st_size // 1024, "KB")
