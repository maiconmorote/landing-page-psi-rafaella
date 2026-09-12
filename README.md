# Landing page — Rafaella Rodrigues, Psicóloga Infantojuvenil

Site de página única, estático, construído sobre o manual de identidade visual
da marca (*Identidade Visual — Rafaella Rodrigues*, Ravena Luz | Designer de
Marcas, 2026).

## Publicar na Vercel

O site é estático e não tem etapa de build na Vercel: o `vercel.json` já aponta
`publicar/` como diretório de saída.

**1. Subir para o GitHub**

```bash
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git push -u origin main
```

**2. Importar na Vercel**

Em [vercel.com/new](https://vercel.com/new), importe o repositório. Deixe tudo
como vem: o `vercel.json` já define o diretório de saída. Se a Vercel perguntar
o Framework Preset, escolha **Other**.

**3. Ajustar o domínio**

Depois do primeiro deploy, abra `fonte/build.py`, troque a constante `DOMINIO`
pela URL definitiva (sem barra no fim) e rode:

```bash
python3 fonte/build.py
git commit -am "Ajusta domínio" && git push
```

Isso corrige `canonical`, Open Graph, JSON-LD, `robots.txt` e `sitemap.xml`.
Enquanto estiver com o valor de exemplo, o build avisa no terminal.

**Importante:** cada alteração de conteúdo exige rodar `python3 fonte/build.py`
antes do commit. A Vercel publica o que está em `publicar/`, e esse diretório é
gerado, não editado à mão.

## Estrutura da página

1. **Proposta** (hero). Uma frase de conforto dirigida a quem lê, que é o pai ou
   a mãe, mais botão de WhatsApp. Sem promessa de resultado.
2. **O que a terapia pode trazer** (`#beneficios`). Seis benefícios sempre no
   campo do possível: "pode", "costuma", "tende a". Nunca "vai", "garante",
   "resolve". A abertura da seção diz explicitamente que não existe resultado
   garantido em psicoterapia. Fecha com a faixa de para quem é o atendimento.
3. **Sobre mim** (`#sobre`). Abre acolhendo quem está lendo antes de falar de
   formação, e fecha dizendo que a pessoa não precisa chegar com tudo
   organizado na cabeça.
4. **Reflexão** (`#reflexao`). As dores do público em forma de reconhecimento,
   a lista de sinais, um parágrafo sobre mudança e botão de WhatsApp.
5. **Depoimentos** (`#depoimentos`). Identidade preservada. Ver abaixo.
6. **Dúvidas** (`#duvidas`). As quatro etapas do atendimento mais dez perguntas
   frequentes, incluindo formas de pagamento, reembolso e desmarcação.

Depois vêm a malha do Instagram, o bloco de contato e o rodapé.

## Arquivos

```
landing-page/
├── vercel.json        ← configuração de deploy
├── publicar/          ← é só isto que a Vercel publica
│   ├── index.html
│   ├── robots.txt     ← gerado pelo build
│   ├── sitemap.xml    ← gerado pelo build
│   └── assets/        ← logotipos, personagens, fotos e mapa
└── fonte/             ← fontes de edição (não precisa subir)
    ├── body.src.html      conteúdo + CSS (edite aqui)
    ├── build.py           gera publicar/index.html
    ├── extract_assets.py  reextrai os PNGs do PDF da marca
    └── serve.py           servidor local para pré-visualizar
```

## Como editar

Edite `fonte/body.src.html` e depois rode:

```bash
python3 fonte/build.py
```

Para ver no navegador antes de publicar:

```bash
python3 fonte/serve.py
```

E abra <http://127.0.0.1:8777>.

## Preencher antes de publicar

Todos os campos abaixo estão com valores de exemplo. Use "localizar e substituir"
em `fonte/body.src.html` e rode `build.py` de novo.

| Procurar por | Substituir por |
|---|---|
| `Segunda a sexta` / `08h às 19h` | horários reais de atendimento |
| `SEUDOMINIO.com.br` | domínio final (em `build.py`) |

Já preenchidos: WhatsApp **(21) 96902-5509**, endereço da **Av. das Américas,
13.685 — Barra da Tijuca, Rio de Janeiro — RJ, 22785-620**, **CRP 05/69028** e
Instagram **@psi.rafaellarodrigues**.

Além disso:

- ~~**Foto da Rafaella**~~ — já aplicada. Para trocar, salve a nova como
  `publicar/assets/rafaella.jpg` (aceita `.jpg`, `.png` ou `.webp`) e rode
  `python3 fonte/build.py`. O retrato entra sozinho, recortado em 4:5. Sem a
  foto, entra o logotipo como marcador e o build avisa no terminal.

  A foto é recortada pelo centro. Se o enquadramento não ficar bom, ajuste
  `object-position` em `.about__portrait--foto img` no `body.src.html` — por
  exemplo `object-position: center 20%` para subir o corte.

## Fotos

A foto do "Sobre mim" é `publicar/assets/rafaella.jpg` — regata marrom contra o
papel de parede do alfabeto, recortada em 4:5 a partir da original.
Escolhida porque o marrom-vinho da blusa é praticamente o `#71202E` da marca e o
cenário comunica o público infantojuvenil sem precisar de legenda.

Na chamada final, "Vamos conversar", entra `publicar/assets/rafaella_cta.jpg`,
recortada em círculo a partir da **02-blusa-creme-mesa**, por escolha do cliente.
O creme claro dá bom contraste contra o vinho da seção e a arandela rosa ao fundo
conversa com a paleta. Corte quadrado com 10% de deslocamento para o alto, para
centrar o rosto; a foto é 3:4, então não há folga lateral para ajustar.

Para trocar por outra, rode um recorte quadrado da original e salve com o mesmo
nome: a marcação e o CSS não mudam.

As demais estão em `../fotos/selecao/`, numeradas por ordem de recomendação e já
redimensionadas para uso em anúncio e redes:

| # | Foto | Onde usa melhor |
|---|---|---|
| 01 | regata marrom, papel de parede | site (em uso) |
| 02 | blusa creme, mesa, arandela rosa | institucional, LinkedIn — creme + rosa da paleta |
| 03 | verde-sálvia na estante | mostra contexto profissional; sálvia ≈ menta |
| 04 | marrom com cartas T-D-A-H | anúncio e feed — comunica o nicho direto |
| 05 | azul-marinho com xícara | institucional, LinkedIn, conteúdo mais humano |
| 06 | marrom na banqueta | alternativa à 01 |
| 07 | verde-sálvia à mesa | apoio |
| 08 | marrom, cartas T-D-A-H de perto | recorte fechado para story |

**Fora da seleção:** as duas selfies de braço estendido no consultório (servem
para story, não para o site) e uma foto de outra pessoa que veio junto no lote —
mulher de suéter cinza sobre fundo branco, com marca d'água de imagem gerada por
IA. Não é a Rafaella; confira se não está em outro material.

## Malha do Instagram

Salve as imagens dos posts em `publicar/assets/instagram/` (nomeadas `01.jpg`,
`02.jpg`, ...) e rode `python3 fonte/build.py`. São usadas até 6, em ordem
alfabética, recortadas em quadrado. Sem imagens, a seção mostra só o botão de
seguir mais um aviso de configuração, e o build avisa no terminal.

Por padrão os quadros levam ao perfil. Para apontar cada um ao seu post, crie
`fonte/instagram.json`:

```json
{
  "posts": [
    {"arquivo": "01.jpg", "url": "https://instagram.com/p/XXXXXXXX/"},
    {"arquivo": "02.jpg", "url": "https://instagram.com/p/YYYYYYYY/"}
  ]
}
```

Optei por essa via em vez da API do Instagram: a Basic Display foi desativada
pela Meta, e a que restou (Instagram Graph) exige conta Business ligada a uma
Página do Facebook mais um token de longa duração que precisa ser renovado. Para
seis imagens que mudam de vez em quando, a pasta compensa mais. Se preferir a
sincronização automática depois, dá para escrever nos mesmos moldes do
`sync_reviews.py`.

## Depoimentos

Ficam em `fonte/depoimentos.json`, **inseridos à mão**. Para adicionar um, copie
um bloco da lista `depoimentos` e rode `python3 fonte/build.py`:

```json
{
  "quem": "Nome",
  "nota": 5,
  "texto": "Primeiro parágrafo.\n\nSegundo parágrafo."
}
```

Linha em branco (`\n\n`) no campo `texto` separa parágrafo. Os campos `nota` e
`total` no topo do arquivo controlam a faixa de resumo: a nota grande, as
estrelas douradas (`#EDBA3D` da paleta) e a contagem "21 avaliações no Google".

Os depoimentos ficam **empilhados numa coluna de 860px**, não lado a lado. Com
textos de tamanhos muito diferentes, a grade deixaria um cartão quase vazio ao
lado de outro cheio; a coluna também segura a medida de leitura, que em 1100px
ficaria larga demais.

**Não há mais sincronização com o Google.** O `sync_reviews.py` foi removido, e
com ele a necessidade de chave de API, de PLACE_ID e do limite de 5 avaliações
que a API impunha.

**Antes de publicar qualquer depoimento**, tenha autorização por escrito de quem
escreveu, guardada em arquivo.

### A nota agregada não entra nos dados estruturados

As avaliações vivem no perfil do Google, e a política de resultados enriquecidos
do Google não aceita que o site marque como sua uma nota agregada vinda de
terceiro. Marcar isso pode render ação manual em vez de estrelinha na busca. Por
isso o `aggregateRating` está desativado no `build.py`, de propósito. A nota
continua aparecendo na tela para quem visita, o que não tem restrição nenhuma.

### O que continua valendo sobre o CFP

Usar só o primeiro nome resolve a exposição do depoente, que era o ponto mais
grave. Mas a restrição do CFP é sobre **usar depoimento de pessoa atendida na
divulgação profissional**, anonimizado ou não. A decisão é da Rafaella, com o
CRP-05 dela, não da agência.

Se ela preferir o caminho conservador, a seção continua funcionando sem o texto
dos depoimentos: em `fonte/build.py`, na função `render_avaliacoes`, retorne
apenas a variável `resumo`. Fica só a nota, as estrelas e o link para o Google,
que não é depoimento.

Referências: [Nota Técnica CFP nº 1/2022](https://site.cfp.org.br/wp-content/uploads/2022/06/SEI_CFP-0612475-Nota-Tecnica.pdf)
· [CRP-PR, Divulgação Profissional](https://crppr.org.br/orientacoes/divulgacao-profissional/)

## Identidade visual aplicada

- **Cores** — vinho `#71202E`, terracota `#D0442A`, rosa `#FFABCF`,
  menta `#CBE3CB`, azul `#95B0DD`, amarelo `#EDBA3D`, creme `#F4F1EB`.
- **Tipografia** — Inter no texto corrido, conforme o manual. Nos títulos, a
  Neulis do manual é uma fonte licenciada e não pode ser servida pela web sem a
  licença; está usada a **Poppins**, geométrica de `a` de andar único, que é a
  correspondente mais próxima no Google Fonts. Com a licença da Neulis em mãos,
  basta hospedar os arquivos da fonte e trocar a variável `--display` no CSS.
- **Elementos de apoio** — os quatro personagens (coração, balão, cérebro e
  rabisco) e as três versões do logotipo foram extraídos direto do PDF do manual,
  em PNG com fundo transparente, por `extract_assets.py`.

## Símbolo do autismo

O card "Intervenção ABA" usa o **quebra-cabeça clássico de quatro peças**, nas
cores azul, amarelo, verde e vermelho, conforme referência enviada pelo cliente.

É a única parte do site fora da paleta da marca, o que foi decisão consciente:
essas quatro cores são o padrão reconhecido do símbolo. O desenho é uma peça só,
girada 90 graus quatro vezes, então o pino de cada uma entra no encaixe da
vizinha e os pinos externos formam um moinho.

**Contexto para quem for editar:** o quebra-cabeça é o símbolo mais reconhecido
de autismo, mas é rejeitado por parte da comunidade autista e por profissionais
de perspectiva neuroafirmativa, porque sugere alguém incompleto ou um enigma a
ser resolvido. A alternativa adotada pela própria comunidade é o **símbolo do
infinito**, que chegou a ser implementado aqui antes desta versão.

Se um dia a Rafaella quiser trocar, o caminho é substituir o `<svg>` do primeiro
`.who__art` por:

```html
<svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="#71202E"
     stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M12 12c-2-2.67-4-4-6-4a4 4 0 1 0 0 8c2 0 4-1.33 6-4Zm0 0c2 2.67 4 4 6 4a4 4 0 0 0 0-8c-2 0-4 1.33-6 4Z"/>
</svg>
```

## Mapa do consultório

A seção antes do rodapé traz um mapa do Google com o endereço, mais o endereço em
texto e o botão "Abrir no Google Maps".

O `<iframe>` aponta para a **ficha da Rafaella no Google Meu Negócio**, e não
para uma busca por endereço. Isso é melhor: o marcador leva o nome do
consultório, mostra a nota e as avaliações, e continua certo mesmo que o
geocodificador do Google interprete o endereço em texto de outro jeito.

Para gerar um embed novo, se um dia o endereço mudar: abra a ficha no Google
Maps, clique em Compartilhar, aba "Incorporar um mapa", e copie o `src`.

**Para trocar o endereço em texto** e o link do botão, edite `ENDERECO` no
`build.py`. O `src` do iframe é independente e fica no `body.src.html`.

CEP confirmado como **22785-620**, conforme o cadastro da própria ficha no
Google.

### Mapa estático de reserva

Atrás do iframe fica `assets/mapa_consultorio.jpg`, um mapa estático do mesmo
ponto. Ele aparece sempre que o iframe do Google não carrega: bloqueador de
anúncios, rede corporativa que barra o Google, ou política de conteúdo. **A
pré-visualização de artifacts do Claude bloqueia iframes por padrão**, então é
esse mapa que aparece lá. No site hospedado o Google carrega por cima e o mapa
fica interativo.

A imagem é gerada por `fonte/gerar_mapa.py`, que baixa ladrilhos do
OpenStreetMap, recorta em 16:9, desenha o marcador na cor da marca e embute o
crédito exigido pela licença. Só precisa rodar de novo se o endereço mudar:

```bash
python3 fonte/gerar_mapa.py   # requer pillow
```

As coordenadas ficam no topo do arquivo, em `LAT, LON`, e vieram do embed da
ficha do Google.

Os antigos cards de WhatsApp, endereço e horários foram removidos daqui. O
WhatsApp continua no cabeçalho, na seção de reflexão, no bloco final e no balão
flutuante.

**Horários:** saíram da página e também do JSON-LD, porque nunca foram
confirmados. Horário errado nos dados estruturados pode aparecer na busca do
Google como se fosse oficial. Quando a Rafaella confirmar, vale voltar com
`"openingHours"` no `build.py` e, se quiser, com uma linha na seção do mapa.

## Cookies e rastreio

O site tem um aviso de cookies com **Aceitar** e **Recusar**. A escolha fica no
navegador da pessoa (`localStorage`, chave `rr-consentimento-cookies`) e o aviso
não volta a aparecer depois de respondido.

**"Recusar" bloqueia de verdade.** Não é botão decorativo. Toda tag de medição
deve entrar em um único lugar, a função `carregarRastreio()` dentro do
`<script>` do `body.src.html`. Essa função só é chamada quando a pessoa aceita:

```js
function carregarRastreio(){
  if (window.__rastreioCarregado) return;
  window.__rastreioCarregado = true;
  // GA4, Meta Pixel e afins entram aqui
}
```

**Não cole Google Analytics, Meta Pixel ou GTM direto no HTML.** Fora dessa
função, eles carregam antes da escolha e o consentimento vira ficção, o que é
exatamente o que a LGPD proíbe. Para consultar o estado em outro script, use
`window.consentimentoCookies`, que vale `'aceitar'`, `'recusar'` ou `null`.

**Hoje o site não tem rastreio nenhum**: nenhum analytics, nenhum pixel, nenhum
cookie. Enquanto continuar assim, recusar não muda nada na prática, porque não
há o que bloquear. O aviso já fica pronto para quando o tráfego pago entrar.

### Medir campanha sem depender do aceite

Boa parte do que a gestão de tráfego precisa não exige cookie:

- **UTM nos links de anúncio** chegam à URL e podem ser lidos sem consentimento.
- **Cliques no WhatsApp** podem levar um parâmetro na mensagem, identificando a
  origem sem rastrear a pessoa.
- **Conversões pelo lado do servidor** (Conversions API da Meta), que não
  dependem de cookie no navegador.

Ou seja: dá para medir campanha respeitando quem recusou.

## Convenções de texto

- **Sem promessa de resultado.** Em qualquer texto novo, benefício se escreve
  com "pode", "costuma", "tende a". O CFP não permite previsão taxativa de
  resultado, e é o registro da Rafaella que fica exposto.
- **Sem travessões.** Nada de `—` nem `–` no conteúdo do site. Ao editar, prefira
  vírgula, dois-pontos, ponto final ou parênteses. Para separar itens em linhas
  como a do rodapé, o site usa o ponto médio `·`.
- **Texto corrido justificado em todas as larguras**, celular incluído. A regra
  é invertida de propósito: todo parágrafo dentro do conteúdo entra justificado
  por padrão e existe uma lista curta de exceções que saem. Assim uma seção nova
  não nasce desalinhada por esquecimento de cadastrar a classe.
- **Não remova o `lang="pt-BR"`** do `<header>`, `<main>` e `<footer>`. É ele que
  liga a hifenização, e sem hifenização a justificação no celular abre buracos
  grandes entre as palavras. Se criar uma seção fora desses elementos, repita o
  atributo.
- Ficam fora da justificação, de propósito: títulos (`h1`, `h2`, que usam
  `text-wrap: balance`), perguntas do FAQ, rótulos, cartões de contato e rodapé.
- **Abaixo de 760px tudo que é título, botão ou pílula fica centralizado**, e os
  cartões de benefício, etapa, depoimento e contato centralizam o conteúdo. O
  texto corrido continua justificado, porque a regra `main p` é aplicada direto
  no parágrafo e vence a centralização herdada do cartão. O bloco fica no CSS
  sob o comentário "MOBILE: titulos, botoes e cartoes centralizados".

## Observações

- A página é intencionalmente de **tema claro apenas**: os logotipos e
  personagens são artes de linha em vinho sobre fundo transparente e só têm
  contraste sobre base clara.
- O texto foi escrito para respeitar o Código de Ética do Psicólogo: não promete
  resultados nem faz promoções. Sobre os depoimentos, veja a seção de avaliações
  acima.
- `publicar/` é um site estático — funciona em qualquer hospedagem
  (Hostinger, Netlify, Vercel, GitHub Pages, ou um subdomínio no servidor atual).
