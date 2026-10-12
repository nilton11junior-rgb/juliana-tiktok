# Passo a passo: ligar o robô ao TikTok da Juliana

Feito uma vez só. Depois disso, cada carrossel aprovado chega sozinho como notificação no TikTok da Juliana; ela escolhe o som e publica.

Endereços que você vai usar (já estão no ar pelo GitHub Pages):

| Campo no TikTok | Endereço |
|---|---|
| Termos de uso | https://nilton11junior-rgb.github.io/juliana-tiktok/site/termos.html |
| Política de privacidade | https://nilton11junior-rgb.github.io/juliana-tiktok/site/privacidade.html |
| Redirect URI (Login Kit) | https://nilton11junior-rgb.github.io/juliana-tiktok/site/autorizar.html |
| URL prefix das fotos | https://nilton11junior-rgb.github.io/juliana-tiktok/ |

## 1. Criar o app (Nilton)
1. Entre em https://developers.tiktok.com com a sua conta e vá em **Manage apps → Connect an app**.
2. Nome: `Juliana Carrosséis`. Categoria: ferramenta de criação de conteúdo. Plataforma: **Web**. Coloque um ícone qualquer da marca (pode ser a foto do perfil dela).
3. Preencha Termos e Privacidade com os endereços da tabela.
4. Em **Products**, adicione **Login Kit** (redirect URI da tabela) e **Content Posting API**.
5. Em **Scopes**, marque `user.info.basic` e `video.upload`. Não precisa de `video.publish`.
6. Em **URL properties**, adicione o **URL prefix** da tabela. O TikTok vai dar um arquivo de verificação `.txt`: me mande o arquivo (ou o nome e o conteúdo) que eu coloco no site e você clica em Verify.
7. Envie o app para revisão (**Submit for review**). Na descrição, use: "Ferramenta interna da confeitaria @ferreira.bolos. Envia carrosséis de fotos para a caixa de entrada da própria conta (MEDIA_UPLOAD); a dona do perfil revisa e publica no app." O TikTok costuma pedir um vídeo curto mostrando o fluxo: eu gravo a tela com você quando chegar essa parte.

## 2. Guardar as chaves no GitHub (Nilton)
Depois de aprovado, copie **Client key** e **Client secret** do app e salve em
https://github.com/nilton11junior-rgb/juliana-tiktok/settings/secrets/actions → **New repository secret**:
- `TIKTOK_CLIENT_KEY`
- `TIKTOK_CLIENT_SECRET`

Nunca cole essas chaves no chat.

## 3. A Juliana autoriza a conta (uma vez, vale 1 ano)
Eu gero o link de autorização. Ela abre no celular logada no @ferreira.bolos e toca em **Autorizar**. A página de retorno mostra um código; com ele eu gero o `TIKTOK_REFRESH_TOKEN`, que você salva como terceiro segredo no mesmo lugar.

## 4. Teste
Aprovamos um carrossel de teste com horário para dali a 10 minutos. Ele deve chegar como notificação no TikTok dela.

## Depois
- Para postar 100% sozinho (sem ela tocar em publicar), o TikTok exige uma **auditoria** extra do app para o `video.publish`. Dá para pedir depois que tudo estiver rodando.
- O refresh token vence em 365 dias: a Juliana autoriza de novo uma vez por ano.
