# Regras do projeto: TikTok da Juliana (@ferreira.bolos)

Idioma: **português do Brasil**. Quem aprova: **Nilton**. Sem `"aprovado": true`, nada sai.

## Como funciona
1. Escrever o carrossel em `conteudo/calendario/semana-AAAA-MM-DD.json` (texto e prompt de cada imagem).
2. Gerar as imagens no ChatGPT (prompt do campo `imagem_prompt`) e salvar em `imagens/<id-do-post>/`.
3. `python3 src/render.py conteudo/calendario/<arquivo>.json` → slides 1080x1920 em `criativos/gerados/`.
4. Mostrar ao Nilton (todos os slides + título + legenda). Depois do OK: `"aprovado": true`, commit e push.
5. O robô (GitHub Actions) envia no horário para a **caixa de entrada do TikTok da Juliana**. Ela abre a notificação, escolhe um **som em alta** e posta.

## Frequência
- **2 carrosséis por dia**. Envio às **11h45** e **19h15** (BRT), para ela postar perto das 12h e das 19h30.
- Produzir em lotes de 3 a 4 dias para nunca faltar post aprovado.

## Último slide: SEMPRE a oferta
- `marca/oferta-final.png` (Fórmula da Confeitaria, R$19,90) entra sozinha como último slide. Não escrever slide de CTA no JSON.
- O penúltimo slide prepara a oferta (prova ou "salva pra não esquecer").

## Hooks (lições da análise do perfil, 12/10/2026)
- O que viralizou: **dinheiro, quantidade ou virada de vida na 1ª frase** (128,5 mil "Há 1 ano eu vendia bolo só pra pagar conta de casa"; 34,3 mil "R$2.000 com bolos de pote"; 12 mil "Você não é pobre"; 7,5 mil "de 5 para 50 bolos por mês").
- **Nunca repetir um hook igual.** Repetidos caíram de 128 mil para 693 e de 12 mil para 441. Reaproveitar a estrutura, nunca a frase.
- **Nunca "link na bio" ou "quer aprender?" na capa.** A venda fica no fim (a oferta).
- Frase bonita sem número ("Um copo bom começa camada por camada") não segura.
- Capa: no máximo 2 linhas na caixa branca + 1 destaque rosa.

## Segmentos (girar)
1. **Dicas/erros** com conta na tela ("4 erros que me faziam vender bolo a R$8").
2. **Mudanças que fazem vender mais** (cardápio, foto, cliente fixa) fechando com prova.
3. **Matemática do pote** (custo, preço, quanto sobra).
4. **Mito x verdade** ("Você não precisa de R$1.000 pra começar").

## Honestidade (obrigatório)
- Números de resultado da Juliana só os que ela já usa: bolo de R$8 → R$15; mais de R$1.800 por semana; de 5 para 50 bolos por mês; R$2.000 com bolo de pote. Nada novo sem ela confirmar.
- Contas de exemplo (custo de receita etc.) aparecem como **exemplo**.
- Imagens são de IA: nunca escrever na tela que a imagem é a produção dela ("olha meu freezer hoje").

## Visual (render.py)
- Fundo: foto gerada no ChatGPT, vertical 9:16, estilo foto de celular realista: bancada de inox, potes transparentes, morango, uva, chocolate, creme, luz natural. **Terço de cima mais limpo** para o texto.
- Texto: caixa branca com letra preta em negrito; destaque rosa `#e2336b`. `*palavra*` vira rosa.
- Área segura do TikTok: texto entre y=250 e y=1450; nada embaixo à direita (botões).

## Tipos de slide no JSON
| tipo | campos |
|---|---|
| capa | `titulo`, `destaque` (opcional), `imagem` |
| item | `num`, `titulo`, `texto`, `imagem` |
| lista | `titulo`, `linhas` [..], `marca` ("✅" ou "❌"), `imagem` |
| prova | `titulo`, `texto` (opcional), `imagem` |

Post: `id`, `publicar_em` (com `-03:00`), `titulo` (até 90 caracteres), `legenda` (com 3 a 5 hashtags), `imagem_prompts` {arquivo: prompt}, `aprovado`.

## Regras fixas
- Nunca colocar token ou senha no repositório. Segredos só no GitHub.
- Nunca editar à mão `estado/published.json`.
- Depois de mudar o calendário: `python3 src/publish.py <arquivo> --dry-run --ignore-time`.
