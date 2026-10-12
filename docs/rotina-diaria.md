# Rotina diária (texto da tarefa agendada)

Crie no app do Claude uma tarefa agendada **todo dia às 17h49**, com o computador ligado e a pasta `C:\Users\nilto\OneDrive\juliana-tiktok` conectada, e cole o texto abaixo.

---

ROTINA DIÁRIA: produzir os 2 carrosséis de AMANHÃ do TikTok da Juliana (@ferreira.bolos), pedir aprovação ao Nilton e agendar no TikTok Studio. Sempre em português do Brasil, mensagens curtas.

1. PROJETO: clone nilton11junior-rgb/juliana-tiktok (add_repo com access "push") e leia o CLAUDE.md inteiro. Veja os títulos já usados em conteudo/calendario/*.json: nunca repetir hook nem tema recente; gire os 4 segmentos.
2. ESCREVER: crie/complete conteudo/calendario/semana-AAAA-MM-DD.json com os 2 posts de amanhã (11h45/12h e 19h15/19h30), "aprovado": false, título até 90 caracteres, legenda com 3 a 5 hashtags, 4 a 6 slides (a oferta entra sozinha no fim) e imagem_prompts. Só números da Juliana que estão no CLAUDE.md.
3. IMAGENS: navegador embutido (ferramentas mcp__remote-devices__Claude_Browser__*), ChatGPT, projeto Nexus, chat "Fotos da Juliana". Uma imagem por mensagem, "mesmo estilo, vertical 9:16, mesma cozinha, terço de cima limpo, sem texto, sem logos e sem rostos. Cena: ...".
4. BAIXAR: avise o Nilton por push e clique em Baixar em cada imagem no visualizador do ChatGPT; ele salva na pasta juliana-tiktok. Confira com device_list_dir. Nunca use JavaScript para tirar imagens do ChatGPT.
5. MONTAR: device_stage_files, recorte 1080x1920, salve em imagens/<id>/, rode src/render.py, olhe os slides, rode src/publish.py --dry-run --ignore-time, commit e push. Grave os slides em OneDrive\juliana-tiktok\carrosseis\<DD-MM manha|noite - tema>\.
6. APROVAR: mostre as folhas de contato, título e legenda. Só siga com OK do Nilton.
7. AGENDAR: TikTok Studio (tiktok.com/tiktokstudio/upload?tab=photo) no navegador embutido, conta Juliana Ferreira. Clique em Selecionar fotos e peça ao Nilton para escolher todos os slides da pasta (Ctrl+A). Confira se a contagem de fotos bate. Preencha título e descrição, escolha um som instrumental de comida/confeitaria (sem repetir o do post anterior), confira que Localização está VAZIA, Programar → data de amanhã, 12:00 ou 19:30 → Agendar. Marque "aprovado": true e "agendado_no_studio": true no JSON, commit e push.
